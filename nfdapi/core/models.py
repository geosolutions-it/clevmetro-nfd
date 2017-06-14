# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import reversion
from django.contrib.gis.db.models.fields import PointField

class Versioned(models.Model):
    identity = models.BigIntegerField()
    version_birth_date = models.DateTimeField()
    version_start_date = models.DateTimeField()
    version_end_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        abstract = True

class DictionaryTable(models.Model):
    code = models.TextField()
    name = models.TextField()
    
    class Meta:
        abstract = True
    
class DictionaryTableExtended(models.Model):
    code = models.TextField()
    name = models.TextField()
    description = models.TextField()
    
    class Meta:
        abstract = True

class OccurrenceCategory(DictionaryTable):
    # natural_area, plant, animal, fungus, slimemold
    pass

class Occurence(models.Model):
    geom = PointField()
    occurrence_cat = models.ForeignKey(OccurrenceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    released = models.BooleanField(default=False)
    inclusion_date = models.DateTimeField()
    class Meta:
        abstract = True

     
class CmStatus(models.Model):
    status = models.TextField()

    
class SRank(models.Model):
    srank = models.TextField()


class NRank(models.Model):
    nrank = models.TextField()


class GRank(models.Model):
    grank = models.TextField()

class Element(models.Model):
    cm_status = models.ForeignKey(CmStatus, on_delete=models.SET_NULL, blank=True, null=True)
    s_rank = models.ForeignKey(SRank, on_delete=models.SET_NULL, blank=True, null=True)
    n_rank = models.ForeignKey(NRank, on_delete=models.SET_NULL, blank=True, null=True)
    g_rank = models.ForeignKey(GRank, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        abstract = True
        
class Family(models.Model):
    tsn = models.IntegerField(blank=True)
    name_sci = models.TextField()
    common_name = models.TextField()
    second_common = models.TextField()
    third_common = models.TextField()

class Species(models.Model):
    tsn = models.IntegerField(blank=True)
    name_sci = models.TextField()
    synonym = models.TextField()
    first_common = models.TextField()
    second_common = models.TextField()
    third_common = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True)

class RegionalStatus(DictionaryTableExtended):
    pass

class UsfwsStatus(DictionaryTable):
    pass

class IucnRedListCategory(DictionaryTable):
    pass

class ElementType(DictionaryTable):
    # alga, arachnid, bird, conifer, etc
    pass

class ElementSpecies(models.Model):
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, blank=True, null=True)
    native = models.BooleanField(default=True)
    oh_status = models.ForeignKey(RegionalStatus, on_delete=models.SET_NULL, blank=True, null=True)
    usfws_status = models.ForeignKey(UsfwsStatus, on_delete=models.SET_NULL, blank=True, null=True)
    iucn_red_list_category = models.ForeignKey(IucnRedListCategory, on_delete=models.SET_NULL, blank=True, null=True)
    other_code = models.TextField()
    species_category = models.ForeignKey(ElementType, on_delete=models.SET_NULL, blank=True, null=True)

class ToxicSpecies(models.Model):
    epa_numeric_code = models.TextField()
    class Meta:
        abstract = True

class ElementPlant(ElementSpecies, ToxicSpecies):
    # nota: las plantas todas tienen el codigo toxico EPA salvo: Conifer, Fern, Moss
    nrcs_usda_symbol = models.TextField()
    synonym_nrcs_usda_symbol = models.TextField()

class ElementBird(ElementSpecies):
    ibp_english = models.CharField(max_length=4)
    ibp_scientific = models.CharField(max_length=6)
    bblab_number = models.CharField(max_length=6)

class ElementCrustacean(ElementSpecies, ToxicSpecies):
    pass

class ElementFlatworm(ElementSpecies, ToxicSpecies):
    pass

class MushroomGroup(DictionaryTable):
    pass

class ElementFungus(ElementSpecies, ToxicSpecies):
    nrcs_usda_symbol = models.TextField()
    synonym_nrcs_usda_symbol = models.TextField()
    mushroom_group = models.ForeignKey(MushroomGroup, on_delete=models.SET_NULL, blank=True, null=True) 
    
class ElementNaturalAreas(Element):
    natural_area_code_nac = models.TextField()
    general_description = models.TextField()
    area = models.FloatField()
    landscape_position =  models.TextField() #FIXME

class ElementInsect(ElementSpecies, ToxicSpecies):
    pass

class ElementMolusc(ElementSpecies, ToxicSpecies):
    pass

class ElementRoundworm(ElementSpecies, ToxicSpecies):
    pass

class ElementSegmentedWorm(ElementSpecies, ToxicSpecies):
    pass

class ElementSessileAnimal(ElementSpecies, ToxicSpecies):
    pass

@reversion.register()    
class Voucher(models.Model):
    voucher_number = models.PositiveIntegerField()
    specimen_collected = models.BooleanField(default=False)
    parts_collected = models.BooleanField(default=False)
    specimen_number = models.BooleanField(default=False)
    minumero = models.IntegerField(default=0)
    mitextin = models.IntegerField( blank=True, null=True, default=None)

"""
class HabitatCategory(DictionaryTable):
    pass
"""

class AquaticHabitatCategory(DictionaryTable):
    pass

class TaxonDetails(models.Model):
    pass
    #habitat = models.ForeignKey(HabitatCategory, on_delete=models.SET_NULL, blank=True, null=True)

@reversion.register()
class OccurenceTaxon(Occurence):
    voucher = models.ForeignKey(Voucher, blank=True, null=True, on_delete=models.CASCADE)
    species_element = models.ForeignKey(ElementSpecies, on_delete=models.SET_NULL, blank=True, null=True)
    details = models.ForeignKey(TaxonDetails, on_delete=models.SET_NULL, blank=True, null=True)

@reversion.register()
class OccurenceNaturalArea(Occurence):
    natural_area_element = models.ForeignKey(ElementNaturalAreas, on_delete=models.SET_NULL, blank=True, null=True)

class Gender(DictionaryTable):
    pass

class Marks(DictionaryTable):
    pass

class DiseasesAndAbnormalities(DictionaryTable):
    pass

class TerrestrialSampler(DictionaryTable):
    pass

class AquaticSampler(DictionaryTable):
    pass


class TerrestrialStratum(DictionaryTable):
    pass

class AnimalLifestages(models.Model):
    egg = models.IntegerField()
    egg_mass = models.IntegerField()
    nest = models.IntegerField()
    early_instar_larva = models.IntegerField()
    larva = models.IntegerField()
    late_instar_larva = models.IntegerField()
    early_instar_nymph = models.IntegerField()
    nymph = models.IntegerField()
    late_instar_nymph = models.IntegerField()
    early_pupa = models.IntegerField()
    pupa = models.IntegerField()
    late_pupa = models.IntegerField()
    juvenile = models.IntegerField()
    immature = models.IntegerField()
    subadult = models.IntegerField()
    adult = models.IntegerField()
    adult_pregnant_or_young = models.IntegerField()
    senescent = models.IntegerField()
    unknown = models.IntegerField()
    na = models.IntegerField()

class AnimalDetails(TaxonDetails):
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True)
    marks = models.ForeignKey(Marks, on_delete=models.SET_NULL, blank=True, null=True)
    lifestages = models.ForeignKey(AnimalLifestages, on_delete=models.CASCADE, blank=True, null=True)
    diseases_and_abnormalities = models.ForeignKey(DiseasesAndAbnormalities, on_delete=models.SET_NULL, blank=True, null=True)
    #id_marks_description #FIXME
    class Meta:
        abstract = True

class AnimalAquaticDetails(AnimalDetails):
    sampler = models.ForeignKey(AquaticSampler, on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        abstract = True

class AnimalLandDetails(AnimalDetails):
    sampler = models.ForeignKey(TerrestrialSampler, on_delete=models.SET_NULL, blank=True, null=True)
    stratum = models.ForeignKey(TerrestrialStratum, on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        abstract = True

class PondLakeType(DictionaryTable):
    pass

class PondLakeUse(DictionaryTable):
    pass

class ShorelineType(DictionaryTable):
    pass

class LakeMicrohabitat(DictionaryTable):
    pass

class LenticSize(models.Model):
    lentic_size_acres_aprox = models.IntegerField()
    lentic_size_squaremeters_aprox = models.IntegerField()
    lentic_size_acres_exact = models.DecimalField(max_digits=6, decimal_places=1)
    lentic_size_squaremeters_exact = models.DecimalField(max_digits=8, decimal_places=1)

    class Meta:
        abstract = True
        
class PondLakeAnimalDetails(AnimalAquaticDetails, LenticSize):
    pond_lake_name = models.TextField()
    pond_lake_type = models.ForeignKey(PondLakeType, on_delete=models.SET_NULL, blank=True, null=True)
    pond_lake_use = models.ForeignKey(PondLakeUse, on_delete=models.SET_NULL, blank=True, null=True)
    shoreline_type = models.ForeignKey(ShorelineType, on_delete=models.SET_NULL, blank=True, null=True)
    microhabitat = models.ForeignKey(LakeMicrohabitat, on_delete=models.SET_NULL, blank=True, null=True)
    microhabitat_comments = models.TextField()
    

class StreamDesignatedUse(DictionaryTable):
    pass

class ChannelType(DictionaryTable):
    pass

class HmfeiLocalAbundance(DictionaryTable):
    pass

class LoticHabitatType(DictionaryTable):
    pass

class StreamSubstracte(models.Model):
    artificial = models.FloatField()
    bedrock = models.FloatField()
    boulder = models.FloatField()
    boulder_slab = models.FloatField()
    clay_hardpan = models.FloatField()
    cobble = models.FloatField()
    fine_detritus = models.FloatField()
    gravel = models.FloatField()
    leafpack_woody_debris = models.FloatField()
    muck = models.FloatField()
    sand = models.FloatField()
    silt = models.FloatField()

class WaterFlowType(DictionaryTable):
    pass

class StreamAnimalDetails(AnimalAquaticDetails):
    stream_name_1 = models.TextField()
    stream_name_2 = models.TextField()
    pemso_code = models.TextField()
    designated_use = models.ForeignKey(StreamDesignatedUse, on_delete=models.SET_NULL, blank=True, null=True)
    channel_type = models.ForeignKey(ChannelType, on_delete=models.SET_NULL, blank=True, null=True)
    hmfei_local_abundance = models.ForeignKey(HmfeiLocalAbundance, on_delete=models.SET_NULL, blank=True, null=True)
    lotic_habitat_type = models.ForeignKey(LoticHabitatType, on_delete=models.SET_NULL, blank=True, null=True)
    substrate = models.ForeignKey(StreamSubstracte, on_delete=models.CASCADE, blank=True, null=True)
    water_flow_type = models.ForeignKey(WaterFlowType, on_delete=models.SET_NULL, blank=True, null=True)

class WetlandType(DictionaryTable):
    pass

class WetlandLocation(DictionaryTable):
    pass

class WetlandVetegationStructure(models.Model):
    buttonbush = models.FloatField()
    cattail = models.FloatField()
    ferns = models.FloatField()
    forbs = models.FloatField()
    phragmites = models.FloatField()
    sedges = models.FloatField()

class WetlandConnectivity(DictionaryTable):
    pass

class WaterSource(DictionaryTable):
    pass

class WetlandHabitatFeature(DictionaryTable):
    pass
    
class WetlandAnimalDetails(AnimalAquaticDetails, LenticSize):
    wetland_name = models.TextField()
    wetland_type = models.ForeignKey(WetlandType, on_delete=models.SET_NULL, blank=True, null=True)
    active_management = models.NullBooleanField(blank=True, null=True)
    wetland_location = models.ForeignKey(WetlandLocation, on_delete=models.SET_NULL, blank=True, null=True)
    vegetation = models.ForeignKey(WetlandVetegationStructure, on_delete=models.CASCADE, blank=True, null=True)
    connectivity = models.ForeignKey(WetlandConnectivity, on_delete=models.SET_NULL, blank=True, null=True)
    water_source = models.ForeignKey(WaterSource, on_delete=models.SET_NULL, blank=True, null=True)
    habitat_feature = models.ForeignKey(WetlandHabitatFeature, on_delete=models.SET_NULL, blank=True, null=True)

class SlimeMoldLifestages(DictionaryTable):
    pass

class SlimeMoldClass(DictionaryTable):
    pass

class SlimeMoldMedia(DictionaryTable):
    pass

class SlimeMoldDetails(TaxonDetails):
    lifestages = models.ForeignKey(SlimeMoldLifestages, on_delete=models.SET_NULL, blank=True, null=True)
    slime_mold_class = models.ForeignKey(SlimeMoldClass, on_delete=models.SET_NULL, blank=True, null=True)
    slime_mold_media = models.ForeignKey(SlimeMoldMedia, on_delete=models.SET_NULL, blank=True, null=True)

class PlantDetails(TaxonDetails):
    """
    AQUI ME QUEDO: HAY QUE DEFINIR MODELO PARA PlaintDetails y sus subclases
    """
    class Meta:
        abstract = True

    

plants = ['plant', 'plant_conifer_or_ally', 'plant_fern_or_ally',
          'plant_flowering_plant', 'plant_moss_or_ally']
slime_mold = ['slime_mold']
fungus = ['fungus']
animals = ['animal', 'animal_aquatic_animal', 'animal_land_animal',
           'animal_pond_lake_animal', 'animal_stream_animal', 'animal_wetland_animal']
natural_area = ['natural_area']