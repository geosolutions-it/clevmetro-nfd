# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import logging
import os
import tempfile
import time

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models.fields import PointField
from django.contrib.gis.db.models.fields import PolygonField
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.db.models.fields.files import ImageField
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image
import reversion

from nfdapi.settings import MEDIA_ROOT


@python_2_unicode_compatible
class DictionaryTable(models.Model):
    code = models.TextField(unique=True)
    name = models.TextField()
    
    def __str__(self):
        return "{0}-{1}".format(self.code, self.name) 
    
    class Meta:
        abstract = True

@python_2_unicode_compatible    
class DictionaryTableExtended(models.Model):
    code = models.TextField(unique=True)
    name = models.TextField()
    description = models.TextField()
    
    def __str__(self):
        return "{0}-{1}".format(self.code, self.name)
       
    class Meta:
        abstract = True

class OccurrenceCategory(DictionaryTable):
    # natural_area, plant, animal, fungus, slimemold
    main_cat = models.TextField()
    
    def natural_key(self):
        return (self.main_cat, self.code, self.name)

@reversion.register()    
class PointOfContact(models.Model):
    name = models.TextField(blank=False)
    affiliation = models.TextField(blank=True, null=True, default='')
    phone1 = models.TextField(blank=True, null=True, default='')
    phone2 = models.TextField(blank=True, null=True, default='')
    email = models.TextField(blank=True, null=True, default='')
    street_address = models.TextField(blank=True, null=True, default='')


class DayTime(DictionaryTable):
    pass

class Season(DictionaryTable):
    pass

class RecordOrigin(DictionaryTable):
    pass

class RecordingStation(DictionaryTable):
    pass

@reversion.register()
class OccurrenceObservation(models.Model):
    observation_date = models.DateField(blank=True, null=True)
    recording_datetime = models.DateField(blank=True, null=True)
    daytime = models.ForeignKey(DayTime, on_delete=models.SET_NULL, blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, blank=True, null=True)
    record_origin = models.ForeignKey(RecordOrigin, on_delete=models.SET_NULL, blank=True, null=True)
    #recording_station = models.ForeignKey(RecordingStation, on_delete=models.SET_NULL, blank=True, null=True)
    recording_station = models.TextField(blank=True, null=True, default='')
    reporter = models.ForeignKey(PointOfContact, on_delete=models.CASCADE, related_name='reporter')
    recorder = models.ForeignKey(PointOfContact, on_delete=models.CASCADE, blank=True, null=True, related_name='recorder')
    verifier = models.ForeignKey(PointOfContact, on_delete=models.CASCADE, blank=True, null=True, related_name='verifier')

PHOTO_UPLOAD_TO = 'images/%Y/%m/'
PHOTO_THUMB_SIZE=300
FILENAME_MAX_LENGTH=2048

def get_img_format(extension):
    if extension[1:].upper() in ('JPG', 'JPEG', 'JPE'):
        return 'JPEG'
    return 'PNG'

def get_thumbnail_and_date(input_image, input_path, thumbnail_size=(PHOTO_THUMB_SIZE, PHOTO_THUMB_SIZE)):
    """
    Create a thumbnail of an existing image
    :param input_image:
    :param thumbnail_size:
    :return:
    """
    if not input_image or input_image == "":
        return

    image = Image.open(input_image)
    date = None
    try:
        # get date from exif data
        if image._getexif:
            for (exif_key, exif_value) in image._getexif().iteritems():
                if exif_key == 0x9003: # "DateTimeOriginal", decimal: 36867
                    date = datetime.strptime(exif_value, "%Y:%m:%d %H:%M:%S") # 2016:08:01 00:15:47 format
                    break
                elif exif_key == 0x0132: # "DateTime", decimal: 306
                    if not date:
                        date = datetime.strptime(exif_value, "%Y:%m:%d %H:%M:%S")
    except:
        logging.exception("Error getting exif date")
    try:
        if not date:
            date = timezone.now()

        # create target directory
        thumb_dirname = os.path.join(MEDIA_ROOT, time.strftime(PHOTO_UPLOAD_TO))
        if not os.path.exists(thumb_dirname):
            os.makedirs(thumb_dirname, mode=0775)

        # create thumbnail
        image.thumbnail(thumbnail_size)
        basename = os.path.basename(input_path)
        name, ext = os.path.splitext(basename)
        (fd,thumb_fullpath) = tempfile.mkstemp(suffix=ext, prefix='thumb_', dir=thumb_dirname)
        thumb_file = os.fdopen(fd, "w")
        image.save(thumb_file, get_img_format(ext))
        thumb_file.close()
        image.close()
        os.chmod(thumb_fullpath, 0774)
        thum_relpath = os.path.relpath(thumb_fullpath, MEDIA_ROOT)
        return (thum_relpath, date)
    except:
        logging.exception("Error creating thumbnail")

@reversion.register()
class Photograph(models.Model):
    image = ImageField(upload_to=PHOTO_UPLOAD_TO, height_field='image_height', width_field='image_width', max_length=1000)
    thumbnail = ImageField(upload_to=PHOTO_UPLOAD_TO, height_field='thumb_height', width_field='thumb_width', max_length=1000, blank=True)
    image_width = PositiveIntegerField()
    image_height = PositiveIntegerField()
    thumb_width = PositiveIntegerField(null=True)
    thumb_height = PositiveIntegerField(null=True)
    description = models.TextField(blank=True, null=True, default='')
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True, default='')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    occurrence_fk = models.PositiveIntegerField(blank=True, null=True)
    occurrence = GenericForeignKey('content_type', 'occurrence_fk')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            (thumb, date) = get_thumbnail_and_date(self.image, self.image.path)
            self.thumbnail = thumb
            self.date = date
        except:
            pass
        super(Photograph, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

def get_occurrence_model(occurrence_maincat):
    try:
        if occurrence_maincat[0]=='n': # natural areas
            return OccurrenceNaturalArea
    except:
        pass
    return OccurrenceTaxon

class Reservation(DictionaryTable):
    pass

class Watershed(DictionaryTable):
    pass

class Location(models.Model):
    site_description = models.TextField(blank=True, null=True, default='')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, blank=True, null=True)
    watershed = models.ForeignKey(Watershed, on_delete=models.SET_NULL, blank=True, null=True)
    directions = models.TextField(blank=True, null=True, default='')
    polygon = PolygonField(null=True)
    class Meta:
        abstract = True

@reversion.register()
class NaturalAreaLocation(Location):
    pass

@reversion.register()
class TaxonLocation(Location):
    parcel = models.TextField(blank=True, null=True, default='')
    city_township = models.TextField(blank=True, null=True, default='')
    county = models.TextField(blank=True, null=True, default='')
    quad_name = models.TextField(blank=True, null=True, default='')
    quad_number = models.TextField(blank=True, null=True, default='')

class Occurrence(models.Model):
    geom = PointField()
    version = models.IntegerField(default=0)
    released_versions = models.IntegerField(default=0)
    occurrence_cat = models.ForeignKey(OccurrenceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    released = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    inclusion_date = models.DateTimeField(default=timezone.now)
    observation = models.OneToOneField(OccurrenceObservation, on_delete=models.CASCADE)
    class Meta:
        abstract = True

     
class CmStatus(DictionaryTableExtended):
    pass

    
class SRank(DictionaryTable):
    pass


class NRank(DictionaryTable):
    pass


class GRank(DictionaryTable):
    pass

class Element(models.Model):
    cm_status = models.ForeignKey(CmStatus, on_delete=models.SET_NULL, blank=True, null=True)
    s_rank = models.ForeignKey(SRank, on_delete=models.SET_NULL, blank=True, null=True)
    n_rank = models.ForeignKey(NRank, on_delete=models.SET_NULL, blank=True, null=True)
    g_rank = models.ForeignKey(GRank, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        abstract = True

class RegionalStatus(DictionaryTableExtended):
    pass

class UsfwsStatus(DictionaryTable):
    pass

class IucnRedListCategory(DictionaryTable):
    pass

class ElementType(DictionaryTable):
    # alga, arachnid, bird, conifer, etc
    pass


class MushroomGroup(DictionaryTable):
    pass

@reversion.register()
class ElementSpecies(Element):
    native = models.NullBooleanField(default=True)
    oh_status = models.ForeignKey(RegionalStatus, on_delete=models.SET_NULL, blank=True, null=True)
    usfws_status = models.ForeignKey(UsfwsStatus, on_delete=models.SET_NULL, blank=True, null=True)
    iucn_red_list_category = models.ForeignKey(IucnRedListCategory, on_delete=models.SET_NULL, blank=True, null=True)
    other_code = models.TextField(blank=True, null=True)
    #species_category = models.ForeignKey(ElementType, on_delete=models.SET_NULL, blank=True, null=True)
    ibp_english = models.CharField(max_length=4, blank=True, null=True, default='')
    ibp_scientific = models.CharField(max_length=6, blank=True, null=True, default='')
    bblab_number = models.CharField(max_length=6, blank=True, null=True, default='')
    nrcs_usda_symbol = models.TextField(blank=True, null=True, default='')
    synonym_nrcs_usda_symbol = models.TextField(blank=True, null=True, default='')
    epa_numeric_code = models.TextField(blank=True, null=True, default='')
    mushroom_group = models.ForeignKey(MushroomGroup, on_delete=models.SET_NULL, blank=True, null=True)


@reversion.register()
class Species(models.Model):
    first_common = models.TextField()
    name_sci = models.TextField()
    tsn = models.PositiveIntegerField(null=True)
    synonym = models.TextField(blank=True, default='', null=True)
    second_common = models.TextField(blank=True, default='', null=True)
    third_common = models.TextField(blank=True, default='', null=True)
    family = models.TextField(blank=True, default='')
    family_common = models.TextField(blank=True, default='')
    phylum = models.TextField(blank=True, default='')
    phylum_common = models.TextField(blank=True, default='')
    element_species = models.ForeignKey(ElementSpecies, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name_sci


class Preservative(DictionaryTable):
    pass

class Storage(DictionaryTable):
    pass

class Repository(DictionaryTable):
    #FIXME: repository needs extra attributes (and maybe has to be managed as a non-dictionary table)
    pass

@reversion.register()
class Voucher(models.Model):
    voucher_number = models.PositiveIntegerField(null=True)
    specimen_collected = models.NullBooleanField(default=False)
    parts_collected = models.NullBooleanField(default=False)
    specimen_number = models.NullBooleanField(default=False)
    preservative = models.ForeignKey(Preservative, on_delete=models.SET_NULL, blank=True, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, blank=True, null=True)
    repository = models.TextField(null=True, blank=True, default='')


class AquaticHabitatCategory(DictionaryTable):
    pass

@reversion.register()
class TaxonDetails(models.Model):
    pass
    #habitat = models.ForeignKey(HabitatCategory, on_delete=models.SET_NULL, blank=True, null=True)

def get_details_class(category_code):
    if category_code=='co':
        return ConiferDetails
    elif category_code=='fe':
        return FernDetails
    elif category_code=='fl':
        return FloweringPlantDetails
    elif category_code=='pl':
        return TaxonDetails #FIXME
    elif category_code=='mo':
        return MossDetails
    elif category_code=='fu':
        return FungusDetails
    elif category_code=='sl':
        return SlimeMoldDetails
    elif category_code=='ln':
        return LandAnimalDetails
    elif category_code=='lk':
        return PondLakeAnimalDetails
    elif category_code=='st':
        return StreamAnimalDetails
    elif category_code=='we':
        return WetlandAnimalDetails
    elif category_code=='na':
        return ElementNaturalAreas

@reversion.register(follow=['photographs'])
class OccurrenceTaxon(Occurrence):
    voucher = models.OneToOneField(Voucher, blank=True, null=True, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, blank=True, null=True)
    details = models.OneToOneField(TaxonDetails, on_delete=models.CASCADE, null=True)
    location = models.OneToOneField(TaxonLocation, on_delete=models.CASCADE, null=True)
    photographs = GenericRelation(Photograph, object_id_field='occurrence_fk')
            
    def get_details_class(self):
        if self.occurrence_cat:
            return get_details_class(self.occurrence_cat.code)
        
    def get_details(self):
        """
        Gets the taxon details using the right model for the concrete instance. By default,
        Django will return the generic model instance (TaxonDetails) instead of an instance
        of LandAnimalDetails, PondLakeAnimalDetails, etc.
        """
        try:
            if self.details and self.occurrence_cat:
                return get_details_class(self.occurrence_cat.code).objects.get(pk=self.details.id)
        except:
            pass

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

@reversion.register()
class AnimalLifestages(models.Model):
    egg = models.FloatField(default=0.0, blank=True, null=True)
    egg_mass = models.FloatField(default=0.0, blank=True, null=True)
    nest = models.FloatField(default=0.0, blank=True, null=True)
    early_instar_larva = models.FloatField(default=0.0, blank=True, null=True)
    larva = models.FloatField(default=0.0, blank=True, null=True)
    late_instar_larva = models.FloatField(default=0.0, blank=True, null=True)
    early_instar_nymph = models.FloatField(default=0.0, blank=True, null=True)
    nymph = models.FloatField(default=0.0, blank=True, null=True)
    late_instar_nymph = models.FloatField(default=0.0, blank=True, null=True)
    early_pupa = models.FloatField(default=0.0, blank=True, null=True)
    pupa = models.FloatField(default=0.0, blank=True, null=True)
    late_pupa = models.FloatField(default=0.0, blank=True, null=True)
    juvenile = models.FloatField(default=0.0, blank=True, null=True)
    immature = models.FloatField(default=0.0, blank=True, null=True)
    subadult = models.FloatField(default=0.0, blank=True, null=True)
    adult = models.FloatField(default=0.0, blank=True, null=True)
    adult_pregnant_or_young = models.FloatField(default=0.0, blank=True, null=True)
    senescent = models.FloatField(default=0.0, blank=True, null=True)
    unknown = models.FloatField(default=0.0, blank=True, null=True)
    na = models.FloatField(default=0.0, blank=True, null=True)

class AnimalDetails(TaxonDetails):
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True)
    marks = models.ForeignKey(Marks, on_delete=models.SET_NULL, blank=True, null=True)
    lifestages = models.OneToOneField(AnimalLifestages, on_delete=models.CASCADE, blank=True, null=True)
    diseases_and_abnormalities = models.ForeignKey(DiseasesAndAbnormalities, on_delete=models.SET_NULL, blank=True, null=True)
    #id_marks_description #FIXME
    class Meta:
        abstract = True

class AquaticAnimalDetails(AnimalDetails):
    sampler = models.ForeignKey(AquaticSampler, on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        abstract = True

@reversion.register(follow=['taxondetails_ptr'])
class LandAnimalDetails(AnimalDetails):
    sampler = models.ForeignKey(TerrestrialSampler, on_delete=models.SET_NULL, blank=True, null=True)
    stratum = models.ForeignKey(TerrestrialStratum, on_delete=models.SET_NULL, blank=True, null=True)

class PondLakeType(DictionaryTable):
    pass

class PondLakeUse(DictionaryTable):
    pass

class ShorelineType(DictionaryTable):
    pass

class LakeMicrohabitat(DictionaryTable):
    pass

class LenticSize(models.Model):
    # FIXME: should we include it as additional tab instead of
    # integrating it on the PondLakeAnimalDetails tab??
    lentic_size_acres_aprox = models.IntegerField(blank=True, null=True)
    lentic_size_squaremeters_aprox = models.IntegerField(blank=True, null=True)
    lentic_size_acres_exact = models.DecimalField(blank=True, null=True,max_digits=6, decimal_places=1)
    lentic_size_squaremeters_exact = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=1)

    class Meta:
        abstract = True

@reversion.register(follow=['taxondetails_ptr'])
class PondLakeAnimalDetails(AquaticAnimalDetails, LenticSize):
    pond_lake_name = models.TextField(blank=True, null=True)
    pond_lake_type = models.ForeignKey(PondLakeType, on_delete=models.SET_NULL, blank=True, null=True)
    pond_lake_use = models.ForeignKey(PondLakeUse, on_delete=models.SET_NULL, blank=True, null=True)
    shoreline_type = models.ForeignKey(ShorelineType, on_delete=models.SET_NULL, blank=True, null=True)
    microhabitat = models.ForeignKey(LakeMicrohabitat, on_delete=models.SET_NULL, blank=True, null=True)
    microhabitat_comments = models.TextField(default='', blank=True, null=True)
    

class StreamDesignatedUse(DictionaryTable):
    pass

class ChannelType(DictionaryTable):
    pass

class HmfeiLocalAbundance(DictionaryTable):
    pass

class LoticHabitatType(DictionaryTable):
    pass

@reversion.register()
class StreamSubstrate(models.Model):
    artificial = models.FloatField(default=0.0, blank=True, null=True)
    bedrock = models.FloatField(default=0.0, blank=True, null=True)
    boulder = models.FloatField(default=0.0, blank=True, null=True)
    boulder_slab = models.FloatField(default=0.0, blank=True, null=True)
    clay_hardpan = models.FloatField(default=0.0, blank=True, null=True)
    cobble = models.FloatField(default=0.0, blank=True, null=True)
    fine_detritus = models.FloatField(default=0.0, blank=True, null=True)
    gravel = models.FloatField(default=0.0, blank=True, null=True)
    leafpack_woody_debris = models.FloatField(default=0.0, blank=True, null=True)
    muck = models.FloatField(default=0.0, blank=True, null=True)
    sand = models.FloatField(default=0.0, blank=True, null=True)
    silt = models.FloatField(default=0.0, blank=True, null=True)

class WaterFlowType(DictionaryTable):
    pass

@reversion.register(follow=['taxondetails_ptr'])
class StreamAnimalDetails(AquaticAnimalDetails):
    stream_name_1 = models.TextField(blank=True, null=True)
    stream_name_2 = models.TextField(blank=True, null=True)
    pemso_code = models.TextField(blank=True, null=True)
    designated_use = models.ForeignKey(StreamDesignatedUse, on_delete=models.SET_NULL, blank=True, null=True)
    channel_type = models.ForeignKey(ChannelType, on_delete=models.SET_NULL, blank=True, null=True)
    hmfei_local_abundance = models.ForeignKey(HmfeiLocalAbundance, on_delete=models.SET_NULL, blank=True, null=True)
    lotic_habitat_type = models.ForeignKey(LoticHabitatType, on_delete=models.SET_NULL, blank=True, null=True)
    substrate = models.ForeignKey(StreamSubstrate, on_delete=models.CASCADE, blank=True, null=True)
    water_flow_type = models.ForeignKey(WaterFlowType, on_delete=models.SET_NULL, blank=True, null=True)

class WetlandType(DictionaryTable):
    pass

class WetlandLocation(DictionaryTable):
    pass

@reversion.register()
class WetlandVetegationStructure(models.Model):
    buttonbush = models.FloatField(default=0.0, blank=True, null=True)
    cattail = models.FloatField(default=0.0, blank=True, null=True)
    ferns = models.FloatField(default=0.0, blank=True, null=True)
    forbs = models.FloatField(default=0.0, blank=True, null=True)
    phragmites = models.FloatField(default=0.0, blank=True, null=True)
    sedges = models.FloatField(default=0.0, blank=True, null=True)

class WetlandConnectivity(DictionaryTable):
    pass

class WaterSource(DictionaryTable):
    pass

class WetlandHabitatFeature(DictionaryTable):
    pass

@reversion.register(follow=['taxondetails_ptr'])
class WetlandAnimalDetails(AquaticAnimalDetails, LenticSize):
    wetland_name = models.TextField(blank=True, null=True)
    wetland_type = models.ForeignKey(WetlandType, on_delete=models.SET_NULL, blank=True, null=True)
    active_management = models.NullBooleanField(blank=True, null=True)
    wetland_location = models.ForeignKey(WetlandLocation, on_delete=models.SET_NULL, blank=True, null=True)
    vegetation = models.OneToOneField(WetlandVetegationStructure, on_delete=models.CASCADE, blank=True, null=True)
    connectivity = models.ForeignKey(WetlandConnectivity, on_delete=models.SET_NULL, blank=True, null=True)
    water_source = models.ForeignKey(WaterSource, on_delete=models.SET_NULL, blank=True, null=True)
    habitat_feature = models.ForeignKey(WetlandHabitatFeature, on_delete=models.SET_NULL, blank=True, null=True)

@reversion.register()
class SlimeMoldLifestages(models.Model):
    sclerotium_color = models.TextField(blank=True, null=True)
    sclerotium_size = models.FloatField(default=0.0, blank=True, null=True)
    sporangia_color = models.TextField(blank=True, null=True)
    sporangia_size = models.FloatField(default=0.0, blank=True, null=True)
    streaming_body_color = models.TextField(blank=True, null=True)
    streaming_body_size = models.FloatField(default=0.0, blank=True, null=True)

class SlimeMoldClass(DictionaryTableExtended):
    pass

class SlimeMoldMedia(DictionaryTable):
    pass

@reversion.register(follow=['taxondetails_ptr'])
class SlimeMoldDetails(TaxonDetails):
    lifestages = models.ForeignKey(SlimeMoldLifestages, on_delete=models.SET_NULL, blank=True, null=True)
    slime_mold_class = models.ForeignKey(SlimeMoldClass, on_delete=models.SET_NULL, blank=True, null=True)
    slime_mold_media = models.ForeignKey(SlimeMoldMedia, on_delete=models.SET_NULL, blank=True, null=True)

@reversion.register()
class ConiferLifestages(models.Model):
    vegetative = models.FloatField(default=0.0, blank=True, null=True)
    immature_ovulate_cones = models.FloatField(default=0.0, blank=True, null=True)
    mature_ovulate_cones = models.FloatField(default=0.0, blank=True, null=True)
    spent_ovulate_cones = models.FloatField(default=0.0, blank=True, null=True)
    immature_pollen_cones = models.FloatField(default=0.0, blank=True, null=True)
    mature_pollen_cones = models.FloatField(default=0.0, blank=True, null=True)
    spent_pollen_cones = models.FloatField(default=0.0, blank=True, null=True)

class FernLifestages(DictionaryTable): # FIXME: probably is not a dict table
    pass

class FloweringPlantLifestages(DictionaryTable): # FIXME: probably is not a dict table
    pass

class MossLifestages(DictionaryTable): # FIXME: probably is not a dict table
    pass

class PlantCount(DictionaryTable):
    pass

"""
class SoilType(DictionaryTable):
    # FIXME: probably is not a dict table
    pass
"""

class MoistureRegime(DictionaryTable):
    pass

class GroundSurface(DictionaryTable):
    pass

class CanopyCover(DictionaryTable):
    pass
"""
class CommonTreesAndBushes(DictionaryTable):
    # FIXME: probably is not a dict table
    pass

class CommonGroundVegetation(DictionaryTable):
    # FIXME: probably is not a dict table
    pass
"""
class GeneralHabitatCategory(DictionaryTable):
    pass

@reversion.register()
class DisturbanceType(models.Model):
    browse = models.FloatField(default=0.0, blank=True, null=True)
    collecting = models.FloatField(default=0.0, blank=True, null=True)
    disease_pest = models.FloatField(default=0.0, blank=True, null=True)
    mowing = models.FloatField(default=0.0, blank=True, null=True)
    trampling = models.FloatField(default=0.0, blank=True, null=True)
    vehicle_traffic = models.FloatField(default=0.0, blank=True, null=True)
    woody_plant_removal = models.FloatField(default=0.0, blank=True, null=True)

"""
class InvasivePlants(DictionaryTable):
    # FIXME: probably is not a dict table
    pass
"""

@reversion.register()
class EarthwormEvidence(models.Model):
    casting_piles = models.FloatField(default=0.0, blank=True, null=True)
    compacted_soil = models.FloatField(default=0.0, blank=True, null=True)
    individuals = models.FloatField(default=0.0, blank=True, null=True)
    layered_castings = models.FloatField(default=0.0, blank=True, null=True)
    middens = models.FloatField(default=0.0, blank=True, null=True)
    no_evidence = models.FloatField(default=0.0, blank=True, null=True)

class LandscapePosition(DictionaryTable):
    pass

class Aspect(DictionaryTable):
    pass

class Slope(DictionaryTable):
    pass

class PlantDetails(TaxonDetails):
    plant_count = models.ForeignKey(PlantCount, on_delete=models.SET_NULL, blank=True, null=True)
    area_ranges = models.TextField(blank=True, null=True)
    #soil_type = models.ForeignKey(SoilType, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    moisture_regime = models.ForeignKey(MoistureRegime, on_delete=models.SET_NULL, blank=True, null=True)
    ground_surface = models.ForeignKey(GroundSurface, on_delete=models.SET_NULL, blank=True, null=True)
    tree_canopy_cover = models.ForeignKey(CanopyCover, on_delete=models.SET_NULL, blank=True, null=True)
    #common_trees_and_bushes = models.ForeignKey(CommonTreesAndBushes, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    #common_ground_vegetation = models.ForeignKey(CommonGroundVegetation, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    general_habitat_category = models.ForeignKey(GeneralHabitatCategory, on_delete=models.SET_NULL, blank=True, null=True)
    leap_land_cover_category = models.TextField(blank=True, null=True)
    disturbance_type = models.ForeignKey(DisturbanceType, on_delete=models.CASCADE, blank=True, null=True)
    #invasive_plants = models.ForeignKey(InvasivePlants, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    earthworm_evidence = models.ForeignKey(EarthwormEvidence, on_delete=models.CASCADE, blank=True, null=True)
    landscape_position = models.ForeignKey(LandscapePosition, on_delete=models.SET_NULL, blank=True, null=True)
    aspect = models.ForeignKey(Aspect, on_delete=models.SET_NULL, blank=True, null=True)
    slope = models.ForeignKey(Slope, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        abstract = True
        
@reversion.register(follow=['taxondetails_ptr'])
class ConiferDetails(PlantDetails):
    lifestages = models.ForeignKey(ConiferLifestages, on_delete=models.SET_NULL, blank=True, null=True)
    
@reversion.register(follow=['taxondetails_ptr'])
class FernDetails(PlantDetails):
    lifestages = models.ForeignKey(FernLifestages, on_delete=models.SET_NULL, blank=True, null=True)

@reversion.register(follow=['taxondetails_ptr'])
class FloweringPlantDetails(PlantDetails):
    lifestages = models.ForeignKey(FloweringPlantLifestages, on_delete=models.SET_NULL, blank=True, null=True)

@reversion.register(follow=['taxondetails_ptr'])
class MossDetails(PlantDetails):
    lifestages = models.ForeignKey(MossLifestages, on_delete=models.SET_NULL, blank=True, null=True)

class FungusApparentSubstrate(DictionaryTable):
    pass

class MushroomVerticalLocation(DictionaryTable):
    pass

class MushroomGrowthForm(DictionaryTable):
    pass

class MushroomOdor(DictionaryTable):
    pass

@reversion.register()
class FruitingBodiesAge(models.Model):
    aged_diam_cm = models.FloatField(null=True)
    aged_count = models.PositiveIntegerField(null=True)
    buttons_diam_cm = models.FloatField(null=True)
    buttons_count = models.PositiveIntegerField(null=True)
    decomposing_diam_cm = models.FloatField(null=True)
    decomposing_count = models.PositiveIntegerField(null=True)
    emergents_diam_cm = models.FloatField(null=True)
    emergents_count = models.PositiveIntegerField(null=True)
    mature_diam_cm = models.FloatField(null=True)
    mature_count = models.PositiveIntegerField(null=True)
    young_diam_cm = models.FloatField(null=True)
    young_count = models.PositiveIntegerField(null=True)
    
class FungalAssociationType(DictionaryTable):
    pass
    
@reversion.register()
class ObservedAssociations(models.Model):
    #gnat_association_present = models.NullBooleanField(default=False) # FIXME, needed??
    gnat_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="gnat")
    ants_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="ants")
    termite_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="termite")
    beetles_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="beetles")
    snow_flea_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="snow_flea")
    slug_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="slug")
    snail_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="snail")
    skunk_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="skunk")
    badger_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="badger")
    easter_gray_squirrel_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="easter_gray_squirrel")
    chipmunk_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="chipmunk")
    other_small_rodent_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="other_small_rodent")
    turtle_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="turtle")
    deer_association = models.ForeignKey(FungalAssociationType, on_delete=models.SET_NULL, blank=True, null=True, related_name="deer")

@reversion.register(follow=['taxondetails_ptr'])
class FungusDetails(TaxonDetails):
    visible_mycelium = models.NullBooleanField(default=False)
    areal_extent = models.TextField(blank=True, null=True, default='') #FIXME
    mycelium_description = models.TextField(blank=True, null=True, default='') #FIXME
    canopy_cover = models.ForeignKey(CanopyCover, on_delete=models.SET_NULL, blank=True, null=True)
    aspect = models.ForeignKey(Aspect, on_delete=models.SET_NULL, blank=True, null=True)
    slope = models.ForeignKey(Slope, on_delete=models.SET_NULL, blank=True, null=True)
    landscape_position = models.ForeignKey(LandscapePosition, on_delete=models.SET_NULL, blank=True, null=True)
    disturbance_type = models.ForeignKey(DisturbanceType, on_delete=models.CASCADE, blank=True, null=True)
    earthworm_evidence = models.ForeignKey(EarthwormEvidence, on_delete=models.CASCADE, blank=True, null=True)
    landscape_position = models.ForeignKey(LandscapePosition, on_delete=models.SET_NULL, blank=True, null=True)
    #spore_print boolean, # flag for associated photos 
    apparent_substrate = models.ForeignKey(FungusApparentSubstrate, on_delete=models.SET_NULL, blank=True, null=True)
    #potential_plant_hosts character varying, # invasive plants # FIXME
    other_observed_associations = models.ForeignKey(ObservedAssociations, on_delete=models.CASCADE, blank=True, null=True)
    mushroom_vertical_location = models.ForeignKey(MushroomVerticalLocation, on_delete=models.SET_NULL, blank=True, null=True)
    fruiting_bodies_age = models.ForeignKey(FruitingBodiesAge, on_delete=models.CASCADE, blank=True, null=True) 
    mushroom_growth_form = models.ForeignKey(MushroomGrowthForm, on_delete=models.SET_NULL, blank=True, null=True)
    mushroom_odor = models.ForeignKey(MushroomOdor, on_delete=models.SET_NULL, blank=True, null=True)

class CMSensitivity(DictionaryTable):
    pass

class NaturalAreaCondition(DictionaryTable):
    pass

class GlacialDepositPleistoceneAge(DictionaryTable):
    pass

class GlacialDeposit(DictionaryTable):
    pass

class NaturalAreaType(DictionaryTable):
    pass

class LeapLandCover(DictionaryTable):
    pass

class BedrockAndOutcrops(DictionaryTable):
    pass

class RegionalFrequency(DictionaryTable):
    pass

@reversion.register()
class ElementNaturalAreas(Element):
    natural_area_code_nac = models.TextField(blank=True, null=True, default='')
    general_description = models.TextField(blank=True, null=True, default='')
    type = models.ForeignKey(NaturalAreaType, on_delete=models.SET_NULL, blank=True, null=True)
    notable_features = models.TextField(blank=True, null=True)
    area = models.FloatField(null=True)
    aspect = models.ForeignKey(Aspect, on_delete=models.SET_NULL, blank=True, null=True)
    slope = models.ForeignKey(Slope, on_delete=models.SET_NULL, blank=True, null=True)
    sensitivity = models.ForeignKey(CMSensitivity, on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey(NaturalAreaCondition, on_delete=models.SET_NULL, blank=True, null=True)
    leap_land_cover_category = models.ForeignKey(LeapLandCover, on_delete=models.SET_NULL, blank=True, null=True)
    disturbance_type = models.ForeignKey(DisturbanceType, on_delete=models.CASCADE, blank=True, null=True)
    #invasive_plants = models.ForeignKey(InvasivePlants, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    earthworm_evidence = models.ForeignKey(EarthwormEvidence, on_delete=models.CASCADE, blank=True, null=True)
    landscape_position = models.ForeignKey(LandscapePosition, on_delete=models.SET_NULL, blank=True, null=True)
    glaciar_diposit = models.ForeignKey(GlacialDeposit, on_delete=models.SET_NULL, blank=True, null=True)
    pleistocene_glaciar_diposit = models.ForeignKey(GlacialDepositPleistoceneAge, on_delete=models.SET_NULL, blank=True, null=True)
    bedrock_and_outcrops = models.ForeignKey(BedrockAndOutcrops, on_delete=models.SET_NULL, blank=True, null=True)
    regional_frequency = models.ForeignKey(RegionalFrequency, on_delete=models.SET_NULL, blank=True, null=True)
    # soils_ssurgo_wrap # FIXME

@reversion.register(follow=['photographs'])
class OccurrenceNaturalArea(Occurrence):
    #details = models.OneToOneField(NaturalAreaDetails, on_delete=models.CASCADE, null=True)
    element = models.ForeignKey(ElementNaturalAreas, on_delete=models.CASCADE, blank=True, null=True)
    photographs = GenericRelation(Photograph, object_id_field='occurrence_fk')
    location = models.OneToOneField(NaturalAreaLocation, on_delete=models.CASCADE, null=True)
