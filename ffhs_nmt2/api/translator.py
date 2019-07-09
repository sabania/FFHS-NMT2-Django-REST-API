from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ipywidgets import widgets
from IPython.core.display import display, HTML
import os
from IPython.display import display

from oauth2client.client import GoogleCredentials
from six.moves import input  # pylint: disable=redefined-builtin

from tensor2tensor import problems as problems_lib  # pylint: disable=unused-import
from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import registry
from tensor2tensor.utils import usr_dir
from tensor2tensor.utils.hparam import HParams
import tensorflow as tf

"""
t2t_usr_dir = "/storage/t2t/code/MyProblems"
server="ec2-54-190-141-233.us-west-2.compute.amazonaws.com:9000"
servable_name="var2"
problem="variante2"
data_dir = "C:\\Users\\arben.sabani\\Documents\\Private\\FFHS\Bachelor-Thesis\\FS2019\\Productiv\\Tests\\t2t\\data\\var2"
"""
class Translator():
  def __init__(self, t2t_usr_dir, server, servable_name, problem, data_dir):
    self.t2t_usr_dir = t2t_usr_dir
    self.server = server
    self.servable_name = servable_name
    self.problem = problem
    self.data_dir = data_dir
    usr_dir.import_usr_dir(t2t_usr_dir)

  def make_request_fn(self):
    """Returns a request function."""
    request_fn = serving_utils.make_grpc_request_fn(
      servable_name=self.servable_name,
      server=self.server,
      timeout_secs=10)
    return request_fn

  # Methode die für das Übersetzen der Eingabe mit Hilfe des Modells auf Tensorflow Serving zustädig ist
  def translate(self,inputs):
    # Registrierung der Problem-Klasse
    problem = registry.problem(self.problem)
    # Instanziierung des HPrams-Objekts
    hparams = HParams(
      data_dir=os.path.expanduser(self.data_dir))
    problem.get_hparams(hparams)
    request_fn = self.make_request_fn()
    inputs = inputs
    # Prediction
    outputs = serving_utils.predict([inputs], problem, request_fn)
    outputs, = outputs
    output, score = outputs
    score_text = score
    return {'inputs': inputs, 'outputs':output, 'scores':score}