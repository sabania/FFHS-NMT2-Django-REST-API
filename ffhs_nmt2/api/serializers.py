from rest_framework import serializers
from . import models

"""Klassen für das Serialisiern von Anfragen und Antworten"""

class TranslationRequestSerializer(serializers.Serializer):
    inputs = serializers.CharField(max_length=2000)
    corrections = serializers.CharField(max_length=2000,required=False)
    model = serializers.CharField(max_length=20)

class TranslationResponseSerializer(serializers.Serializer):
    inputs = serializers.CharField(max_length=2000)
    outputs = serializers.CharField(max_length=2000)
    scores = serializers.FloatField()