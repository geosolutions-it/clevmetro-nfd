# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
from rest_framework.serializers import Serializer
from rest_framework import serializers
from core.models import OccurrenceTaxon, Occurrence, OccurrenceNaturalArea
from djgeojson.views import GeoJSONLayerView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.template.context_processors import request
from featuretype import FeatureTypeSerializer, FeatureInfoSerializer



# Create your views here.
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

"""
def ElementSpeciesSerializer(serializers.Serializer):
    #species = models.ForeignKey(Species, on_delete=models.SET_NULL, blank=True, null=True)
    native = serializers.BooleanField()
    #oh_status = models.ForeignKey(RegionalStatus, on_delete=models.SET_NULL, blank=True, null=True)
    #usfws_status = models.ForeignKey(UsfwsStatus, on_delete=models.SET_NULL, blank=True, null=True)
    #iucn_red_list_category = models.ForeignKey(IucnRedListCategory, on_delete=models.SET_NULL, blank=True, null=True)
    other_code = serializers.TextField()
    #species_category = models.ForeignKey(ElementType, on_delete=models.SET_NULL, blank=True, null=True)
"""
    
"""
def LayerTaxonFeatInfoSerializer(serializers.Serializer):
    element = ElementSpeciesSerializer(required=False)
"""
"""
def LayerTaxonSerializer(serializers.Serializer):
    inclusion_date = serializers.DateTimeField()
    released = serializers.BooleanField()
    #geom = serializers.GeometryField() # we need to import geojson serializer
"""

class DictionarySerializer(Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    
    def __init__(self, instance=None, data=None, **kwargs):
        super(DictionarySerializer, self).__init__(**kwargs)


class LayerTaxonSerializer(Serializer):
    occurrence_cat = DictionarySerializer(required=False)
    
    def __init__(self, instance=None, data=None, **kwargs):
        super(LayerTaxonSerializer, self).__init__(**kwargs)

class PlantLayerView(GeoJSONLayerView):
    properties = ['occurrence_cat']
    use_natural_keys = True
    
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='plant')

class AnimalLayerView(GeoJSONLayerView):
    properties = ['occurrence_cat']
    use_natural_keys = True
    
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='animal')

class SlimeMoldLayerView(GeoJSONLayerView):
    properties = ['occurrence_cat']
    use_natural_keys = True
    
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='slime mold')
                                              
class FungusLayerView(GeoJSONLayerView):
    properties = ['occurrence_cat']
    use_natural_keys = True
    
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='fungus')

class NaturalAreaLayerView(GeoJSONLayerView):
    properties = ['occurrence_cat']
    use_natural_keys = True
    
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='natural area')


@api_view(['GET'])
@permission_classes([])
def get_feature_type(request, occurrence_maincat, feature_id):
    if occurrence_maincat[0]=='n': # natural areas
        feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
    else:
        feat = OccurrenceTaxon.objects.get(pk=feature_id)
    main_cat = feat.occurrence_cat.main_cat
    subcat_code = feat.occurrence_cat.code
    serializer = FeatureTypeSerializer()
    ftdata = serializer.get_feature_type(main_cat, subcat_code)
    return Response(ftdata)

@api_view(['GET'])
@permission_classes([])
def get_feature_info(request, occurrence_maincat, feature_id):
    if occurrence_maincat[0]=='n': # natural areas
        feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
    else:
        feat = OccurrenceTaxon.objects.get(pk=feature_id)
    #main_cat = feat.occurrence_cat.main_cat
    #subcat_code = feat.occurrence_cat.code
    serializer = FeatureInfoSerializer()
    ftdata = serializer.get_feature_info(feat)
    return Response(ftdata)

"""
"""


class TaxonFeatureTypeView(APIView):
    permission_classes = ()
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return OccurrenceTaxon.objects.get(pk=pk)
        except OccurrenceTaxon.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = LayerTaxonSerializer(obj)
        return Response(serializer.data)

class PlantDetail(APIView):
    permission_classes = ()
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return OccurrenceTaxon.objects.get(pk=pk)
        except OccurrenceTaxon.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = LayerTaxonSerializer(obj)
        return Response(serializer.data)
        

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = LayerTaxonSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
"""
    class Meta:
        model = OccurrenceTaxon
        fields = ('inclusion_date', 'released')
"""

plants = ['plant', 'plant_conifer_or_ally', 'plant_fern_or_ally',
          'plant_flowering_plant', 'plant_moss_or_ally']
slime_mold = ['slime_mold']
fungus = ['fungus']
animals = ['animal', 'animal_aquatic_animal', 'animal_land_animal',
           'animal_pond_lake_animal', 'animal_stream_animal', 'animal_wetland_animal']
natural_area = ['natural_area']

layers = plants + slime_mold + fungus + animals + natural_area
"""
# POR TIPO
 element_natural_areas
 
 element_taxon
 element_species
 element_fungus_or_ally
 element_slime_mold # moho
 
 
 element_amphibian
 element_arachnid , 
 element_bird
 element_crustacean (subfilo), filo Arthropoda, reino Animalia
 element_fish (clasific. informal), filo Chordata, reino Animalia
 element_flatworm
 element_insect (clase Insecta), subfilo Hexapoda, Filo  Arthropoda, reino Animalia
 element_mammal (clase Mammalia), Sufilo Vertebrata, filo Chordata, reino Animalia
 element_mollusk (filo Mollusca), reino Animalia. Acuáticos y terrestres (e.g. pulpos y caracoles)
 element_myriapod
 element_reptile
 element_roundworm
 element_segmented_worm
 element_sessile_animal
 
 element_alga
 element_conifer_or_ally
 element_fern_or_ally # helechos
 element_forb # plantas herbáceas no gramináceas
 element_grass
 element_moss_or_ally # musgo
 element_sedge_or_rush # juncos
 element_shrub_or_tree
 
 

# POR ORDEN EN LA DB
 element_natural_areas
 element_species
 element_alga
 element_amphibian
 element_arachnid
 element_bird
 element_conifer_or_ally
 element_crustacean
 element_fern_or_ally
 element_fish
 element_flatworm
 element_forb
 element_fungus_or_ally
 element_grass
 element_insect
 element_mammal
 element_mollusk
 element_moss_or_ally
 element_myriapod
 element_reptile
 element_roundworm
 element_sedge_or_rush
 element_segmented_worm
 element_sessile_animal
 element_shrub_or_tree
 element_slime_mold
 element_taxon

"""


"""
@csrf_exempt
def snippet_list(request):
    #List all code snippets, or create a new snippet.
    
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        #Create and return a new `Snippet` instance, given the validated data.
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #Update and return an existing `Snippet` instance, given the validated data.
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

@csrf_exempt
def snippet_detail(request, pk):
    #Retrieve, update or delete a code snippet.
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
"""
