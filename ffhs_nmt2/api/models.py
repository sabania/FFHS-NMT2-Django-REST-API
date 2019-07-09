from django.db import models

# Create your models here.

from django.db import models

# Klasse für eine Übersetzungs-Anfrage
class TranslationRequest():
  def __init__(self, inputs, corrections, model):
    self.inputs = inputs
    self.corrections = corrections
    self.model = model

# Klasse für Antwort der Anfrage
class TranslationResponse(models.Model):
  def __init__(self, inputs, outputs, scores):
    self.inputs = inputs
    self.outputs = outputs
    self.scores = scores