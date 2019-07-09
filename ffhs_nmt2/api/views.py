# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from . import  serializers
from . import models
from . import translator
import  os

"""@api_view(['POST'])
def translate(request):
  if request.method == 'POST':
    test = request.POST.get("test", "")
    return Response("worked!!!")"""


class TranslationCreate(generics.CreateAPIView):
  serializer_class = serializers.TranslationRequestSerializer
  """
      Concrete view for creating a model instance.
      """

  """
  Postmethode: empfägt als request den Ausgagssatz als inputs, die Korrekturen als corrections und den Namen des Models als model (var2)
  liefert als Rückgabewert die Übeersetzung
  """
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def create(self, request, *args, **kwargs):
    #Serializer-Instanz, serlialisiert Daten aus request
    trreqserializer = serializers.TranslationRequestSerializer(data=request.data)
    trreqserializer.is_valid(raise_exception=False)
    transl = translator.Translator(
      # Pfad zum Ordner der Problem-Klasse des Lösungskonzepts
      t2t_usr_dir='/home/ubuntu/ffhs_nmt2/tensorTotensor/code/MyProblems',
      # Server und Port wo das Modell in Tensorflow Serving deployed ist
      server='localhost:8500',
      # Name des Models auf Tensorflow Serving
      servable_name=trreqserializer.data['model'],
      # Name der Problem-Klasse
      problem=trreqserializer.data['model'],
      # Pfad zum Ordner wo das Vokabular zu finden ist
      data_dir='/home/ubuntu/ffhs_nmt2/tensorTotensor/data/var2')
    # Ausgangssatz
    inputs = trreqserializer.data['inputs']
    if('corrections' in trreqserializer.data):
      # Ausgagssatz mit Token und Korrekturen
      inputs = inputs+' <trst> '+ trreqserializer.data['corrections']
    # Schickt inputs zum Modell auf Tensorflow serving und erhält Resultat
    result = transl.translate(inputs)
    response = models.TranslationResponse(inputs=trreqserializer.data['inputs'], outputs=result['outputs'], scores=result['scores'])
    responseserializer = serializers.TranslationResponseSerializer(response)
    headers = self.get_success_headers(responseserializer.data)
    return Response(responseserializer.data, status=status.HTTP_201_CREATED, headers=headers)