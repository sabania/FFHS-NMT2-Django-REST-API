import re
import xml.etree.ElementTree as ET
import os
from tensor2tensor.data_generators import text_problems
from tensor2tensor.data_generators import translate
from tensor2tensor.utils import registry
from tensor2tensor.data_generators import problem
import itertools
from random import randint

# Setup some directories
data_dir = "/storage/t2t/data/var2"
tmp_dir = "/storage/t2t/tmp"
train_dir = "/storage/t2t/train/var2"
var1path = "/storage/t2t/tmp/training"
var1path_dev = "/storage/t2t/tmp/dev"

_ENDE_TRAIN_DATASETS = [
    [
        "http://data.statmt.org/wmt18/translation-task/training-parallel-nc-v13.tgz",  # pylint: disable=line-too-long
        ("training-parallel-nc-v13/news-commentary-v13.de-en.en", "training-parallel-nc-v13/news-commentary-v13.de-en.de")
    ],
    [
        "http://www.statmt.org/wmt13/training-parallel-commoncrawl.tgz",
        ("commoncrawl.de-en.en", "commoncrawl.de-en.de")
    ],
    [
        "http://www.statmt.org/wmt13/training-parallel-europarl-v7.tgz",
        ("training/europarl-v7.de-en.en", "training/europarl-v7.de-en.de")
    ],
]
_ENDE_EVAL_DATASETS = [
    [
        "http://data.statmt.org/wmt17/translation-task/dev.tgz",
        ("dev/newstest2013.en", "dev/newstest2013.de")
    ],
]

"""Problem-Klasse wie sie für das Lösungskonzept der Thesis vewendet wird"""

@registry.register_problem
class var2(translate.TranslateProblem):
    # Anzahl Sub-Wörter des Vokabulars
    @property
    def approx_vocab_size(self):
        return 2 ** 15
    
    @property
    def is_generate_per_split(self):
        return True
    
    def source_data_files(self, dataset_split):
        train = dataset_split == problem.DatasetSplit.TRAIN
        train_datasets = _ENDE_TRAIN_DATASETS
        return train_datasets if train else _ENDE_EVAL_DATASETS

    # Aufbereitung der Traingsdaten, so dass Korrekturen erzeugt werden
    def generate_samples(self, data_dir, tmp_dir, dataset_split):
        train = dataset_split == problem.DatasetSplit.TRAIN
        if(train):
            #Pfad zu der Traingsdatei mit den Sätzen in der Zielsprache
            de_file = open(os.path.join(tmp_dir, "translate_ende_wmt32k-compiled-train.lang2"),encoding="utf8")
            # Pfad zu der Trainingsdatei mit den Sätzen in der Ausgagssprache
            en_file = open(os.path.join(tmp_dir, "translate_ende_wmt32k-compiled-train.lang1"),encoding="utf8")
        else:
            #Pfad zu der Testdati mit den Sätzen in der Zielsprache
            de_file = open(os.path.join(var1path_dev, "newstest2013.de"),encoding="utf8")
            # Pfad zu der Testdati mit den Sätzen in der Ausgangssprache
            en_file = open(os.path.join(var1path_dev, "newstest2013.en"),encoding="utf8")
        for en, de in zip(en_file, de_file):
            de_split = de.split()
            yield {
                "inputs": en.strip(),
                "targets": de.strip()
            }
            if (len(de_split) > 1):
                limit = min(10,len(de_split)-1)
                sp = randint(1, limit)
                de_split_parts = de_split[0:sp]
                de_split_parts_joined = " ".join(de_split_parts)
                #de_split_parts_rest = de_split[sp:len(de_split)]
                input_str = en.strip()+" <trst> "+de_split_parts_joined.strip()
                target_str = de#target_str = " ".join(de_split_parts_rest)
                yield {
                    "inputs": input_str.strip(),
                    "targets": target_str.strip()
                }
        de_file.close()
        en_file.close()
     

        
    @property
    def additional_reserved_tokens(self):
        """Additional reserved tokens. Only for VocabType.SUBWORD.
        Returns:
        List of str tokens that will get vocab ids 2+ (0 and 1 are reserved for
        padding and end-of-string).
        """
        return ["<trst>"]