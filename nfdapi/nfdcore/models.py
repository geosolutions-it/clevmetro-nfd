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
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.db.models.fields.files import ImageField
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image
import reversion

from nfdapi.settings import MEDIA_ROOT

from . import itis

PHOTO_UPLOAD_TO = 'images/%Y/%m/'
PHOTO_THUMB_SIZE=300
FILENAME_MAX_LENGTH=2048


def get_jsonfield_validation_choices(model, field_name, include_values=False):
    """Return the set of legal values for a given JSONField

    In this project we are using JSONField to store arrays of values in order
    to emulate a many-to-many relationship. In order to enforce that only
    legal values are inserted into the JSONField, it is necessary to map
    the many-to-many relationship in an informal way. This function's code
    does just that by keeping a mapping of which model is related to which
    JSONField.

    Parameters
    ----------
    model: django.db.models.base.Model
        The model where the JSONField is defined
    field_name: str
        Name of the JSONField on the model
    include_values: bool, optional
        Whether or not to include both the code and the name for each choice

    """

    jsonfield_mapping = {
        "occurrenceobservation.record_origin": RecordOrigin,
        "location.reservation": Reservation,
        "location.watershed": Watershed,
        "voucher.preservative": Preservative,
        "voucher.storage": Storage,
        "animaldetails.diseases_and_abnormalities": DiseasesAndAbnormalities,
        "animaldetails.marks": Marks,
        "animaldetails.gender": Gender,
        "animaldetails.lifestages": AnimalLifestages,
        "aquaticanimaldetails.sampler": AquaticSampler,
        "landanimaldetails.sampler": TerrestrialSampler,
        "landanimaldetails.stratum": TerrestrialStratum,
        "pondlakeanimaldetails.microhabitat": LakeMicrohabitat,
        "pondlakeanimaldetails.pond_lake_use": PondLakeUse,
        "pondlakeanimaldetails.shoreline_type": ShorelineType,
        "streamanimaldetails.channel_type": ChannelType,
        "streamanimaldetails.hmfei_local_abundance": HmfeiLocalAbundance,
        "streamanimaldetails.lotic_habitat_type": LoticHabitatType,
        "wetlandanimaldetails.water_source": WaterSource,
        "wetlandanimaldetails.habitat_feature": WetlandHabitatFeature,
        "wetlandanimaldetails.wetland_type": WetlandType,
        "slimemolddetails.slime_mold_class": SlimeMoldClass,
        "slimemolddetails.slime_mold_media": SlimeMoldMedia,
        "plantdetails.aspect": Aspect,
        "plantdetails.general_habitat_category": GeneralHabitatCategory,
        "plantdetails.ground_surface": GroundSurface,
        "plantdetails.landscape_position": LandscapePosition,
        "plantdetails.moisture_regime": MoistureRegime,
        "plantdetails.slope": Slope,
        "ferndetails.lifestages": FernLifestages,
        "floweringplantdetails.lifestages": FloweringPlantLifestages,
        "mossdetails.lifestages": MossLifestages,
        "coniferdetails.lifestages": ConiferLifestages,
        "observedassociations.gnat_association": FungalAssociationType,
        "observedassociations.ants_association": FungalAssociationType,
        "observedassociations.termite_association": FungalAssociationType,
        "observedassociations.beetles_association": FungalAssociationType,
        "observedassociations.snow_flea_association": FungalAssociationType,
        "observedassociations.slug_association": FungalAssociationType,
        "observedassociations.snail_association": FungalAssociationType,
        "observedassociations.skunk_association": FungalAssociationType,
        "observedassociations.badger_association": FungalAssociationType,
        "observedassociations.easter_gray_squirrel_association": (
            FungalAssociationType),
        "observedassociations.chipmunk_association": FungalAssociationType,
        "observedassociations.other_small_rodent_association": (
            FungalAssociationType),
        "observedassociations.turtle_association": FungalAssociationType,
        "observedassociations.deer_association": FungalAssociationType,
        "fungusdetails.aspect": Aspect,
        "fungusdetails.apparent_substrate": FungusApparentSubstrate,
        "fungusdetails.landscape_position": LandscapePosition,
        "fungusdetails.mushroom_growth_form": MushroomGrowthForm,
        "fungusdetails.mushroom_odor": MushroomOdor,
        "fungusdetails.mushroom_vertical_location": MushroomVerticalLocation,
        "fungusdetails.slope": Slope,
        "elementnaturalareas.aspect": Aspect,
        "elementnaturalareas.bedrock_and_outcrops": BedrockAndOutcrops,
        "elementnaturalareas.sensitivity": CMSensitivity,
        "elementnaturalareas.glaciar_diposit": GlacialDeposit,
        "elementnaturalareas.pleistocene_glaciar_diposit": (
            GlacialDepositPleistoceneAge),
        "elementnaturalareas.landscape_position": LandscapePosition,
        "elementnaturalareas.leap_land_cover_category": LeapLandCover,
        "elementnaturalareas.condition": NaturalAreaCondition,
        "elementnaturalareas.type": NaturalAreaType,
        "elementnaturalareas.regional_frequency": RegionalFrequency,
        "elementnaturalareas.slope": Slope,
    }
    # due to inheritance, the field may be defined in a parent class of model
    # so we first look in the model and then we try its base classes, in order
    model_class_hierarchy = [model]
    model_class_hierarchy.extend(_get_model_bases(model))
    for model_class in model_class_hierarchy:
        lookup_name = ".".join((model_class.__name__.lower(), field_name))
        dictionary_table_model = jsonfield_mapping.get(lookup_name)
        try:
            if include_values:
                choices = dictionary_table_model.objects.values_list(
                    "code", "name")
            else:
                choices = dictionary_table_model.objects.values_list(
                    "code", flat=True)
        except AttributeError:
            choices = None
        if choices is not None:
            break
    else:
        choices = None
    return choices


def _get_model_bases(model_class):
    current = model_class
    bases = []
    while current is not None:
        current = current.__base__
        if current is not None:
            bases.append(current)
    return bases


def get_img_format(extension):
    if extension[1:].upper() in ('JPG', 'JPEG', 'JPE'):
        return 'JPEG'
    return 'PNG'


def get_occurrence_model(occurrence_maincat):
    try:
        if occurrence_maincat[0]=='n': # natural areas
            return OccurrenceNaturalArea
    except:
        pass
    return OccurrenceTaxon


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
    record_origin = JSONField(blank=True, null=True)
    #recording_station = models.ForeignKey(RecordingStation, on_delete=models.SET_NULL, blank=True, null=True)
    recording_station = models.TextField(blank=True, null=True, default='')
    reporter = models.ForeignKey(PointOfContact, on_delete=models.CASCADE, related_name='reporter')
    recorder = models.ForeignKey(PointOfContact, on_delete=models.CASCADE, blank=True, null=True, related_name='recorder')
    verifier = models.ForeignKey(PointOfContact, on_delete=models.CASCADE, blank=True, null=True, related_name='verifier')


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


class Reservation(DictionaryTable):
    pass


class Watershed(DictionaryTable):
    pass


class Location(models.Model):
    site_description = models.TextField(blank=True, null=True, default='')
    reservation = JSONField(blank=True, null=True)
    watershed = JSONField(blank=True, null=True)
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


@python_2_unicode_compatible
class Note(models.Model):
    """Represents notes set on the UI for each form page"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    occurrence = GenericForeignKey("content_type", "object_id")
    ui_tab = models.CharField(
        max_length=50,
        help_text="Identifier of the UI page where this note should be shown",
    )
    note = models.TextField(
        blank=True,
        help_text="Note to show together with the UI page"
    )

    def __str__(self):
        return "{} - {}".format(self.ui_tab, self.note)


class Occurrence(models.Model):
    geom = PointField()
    version = models.IntegerField(default=0)
    released_versions = models.IntegerField(default=0)
    occurrence_cat = models.ForeignKey(OccurrenceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    released = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    inclusion_date = models.DateTimeField(default=timezone.now)
    observation = models.OneToOneField(OccurrenceObservation, on_delete=models.CASCADE)
    notes = GenericRelation(Note)

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


@python_2_unicode_compatible
@reversion.register()
class Taxon(Element):
    tsn = models.PositiveIntegerField(
        primary_key=True,
        help_text="Taxonomic Serial Number, as found on the Integrated "
                  "Taxonomic Information System (ITIS)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Scientific name for the taxon",
        editable=False
    )
    common_names = JSONField(
        blank=True,
        null=True,
        editable=False
    )
    rank = models.CharField(
        max_length=15,
        editable=False
    )
    kingdom = models.CharField(
        max_length=15,
        editable=False
    )
    upper_ranks = JSONField(
        blank=True,
        null=True,
        editable=False
    )
    native = models.NullBooleanField(default=False)
    leap_concern = models.NullBooleanField(default=False)
    oh_status = models.ForeignKey(
        RegionalStatus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    usfws_status = models.ForeignKey(
        UsfwsStatus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    iucn_red_list_category = models.ForeignKey(
        IucnRedListCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    other_code = models.TextField(blank=True)
    ibp_english = models.CharField(
        max_length=4,
        blank=True,
    )
    ibp_scientific = models.CharField(
        max_length=6,
        blank=True,
    )
    bblab_number = models.CharField(
        max_length=6,
        blank=True,
    )
    nrcs_usda_symbol = models.TextField(blank=True)
    synonym_nrcs_usda_symbol = models.TextField(blank=True)
    epa_numeric_code = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "taxa"

    def __str__(self):
        return "{}(kingdom {}, rank {}, TSN {})".format(
            self.name, self.kingdom, self.rank, self.tsn)

    def save(self, *args, **kwargs):
        """Save an instance in the database

        This method retrieves taxon details from the ITIS database before
        passing control to django's normal save() mechanism

        """

        self.populate_attributes_from_itis()
        return super(Taxon, self).save(*args, **kwargs)

    def populate_attributes_from_itis(self):
        details = itis.get_taxon_details(self.tsn)
        if details is not None:
            self.name = details.name
            self.common_names = details.common_names
            self.rank = details.rank
            if self.rank.lower() == "kingdom":
                self.kingdom = details.name
            else:
                upper_ranks = itis.get_taxon_upper_ranks(self.tsn)
                self.upper_ranks = [i.__dict__ for i in upper_ranks[:-1]]
                self.kingdom = self.upper_ranks[0]["name"]


class Preservative(DictionaryTable):
    pass


class Storage(DictionaryTable):
    pass


class Repository(DictionaryTable):
    # FIXME: repository needs extra attributes
    # (and maybe has to be managed as a non-dictionary table)
    pass


@reversion.register()
class Voucher(models.Model):
    voucher_number = models.PositiveIntegerField(null=True)
    specimen_collected = models.NullBooleanField(default=False)
    parts_collected = models.NullBooleanField(default=False)
    specimen_number = models.NullBooleanField(default=False)
    preservative = JSONField(blank=True, null=True)
    storage = JSONField(blank=True, null=True)
    repository = models.TextField(null=True, blank=True, default='')


class AquaticHabitatCategory(DictionaryTable):
    pass


@reversion.register()
class TaxonDetails(models.Model):
    pass
    #habitat = models.ForeignKey(HabitatCategory, on_delete=models.SET_NULL, blank=True, null=True)


def get_details_class(category_code):
    return {
        "co": ConiferDetails,
        "fe": FernDetails,
        "fl": FloweringPlantDetails,
        "fu": FungusDetails,
        "lk": PondLakeAnimalDetails,
        "ln": LandAnimalDetails,
        "pl": TaxonDetails,  # FIXME
        "mo": MossDetails,
        "na": ElementNaturalAreas,
        "sl": SlimeMoldDetails,
        "st": StreamAnimalDetails,
        "we": WetlandAnimalDetails,
    }.get(category_code)


@reversion.register(follow=['photographs'])
class OccurrenceTaxon(Occurrence):
    voucher = models.OneToOneField(
        Voucher,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    details = models.OneToOneField(
        TaxonDetails,
        on_delete=models.CASCADE,
        null=True
    )
    location = models.OneToOneField(
        TaxonLocation,
        on_delete=models.CASCADE,
        null=True
    )
    photographs = GenericRelation(
        Photograph,
        object_id_field='occurrence_fk'
    )
    taxon = models.ForeignKey(
        Taxon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

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
class AnimalLifestages(DictionaryTable):
    pass


class AnimalDetails(TaxonDetails):
    gender = JSONField(blank=True, null=True)
    marks = JSONField(blank=True, null=True)
    lifestages = JSONField(blank=True, null=True)
    diseases_and_abnormalities = JSONField(blank=True, null=True)
    #id_marks_description #FIXME

    class Meta:
        abstract = True


class AquaticAnimalDetails(AnimalDetails):
    sampler = JSONField(blank=True, null=True)

    class Meta:
        abstract = True


@reversion.register(follow=['taxondetails_ptr'])
class LandAnimalDetails(AnimalDetails):
    sampler = JSONField(blank=True, null=True)
    stratum = JSONField(blank=True, null=True)


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
    pond_lake_use = JSONField(blank=True, null=True)
    shoreline_type = JSONField(blank=True, null=True)
    microhabitat = JSONField(blank=True, null=True)
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
    channel_type = JSONField(blank=True, null=True)
    hmfei_local_abundance = JSONField(blank=True, null=True)
    lotic_habitat_type = JSONField(blank=True, null=True)
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
    wetland_type = JSONField(blank=True, null=True)
    active_management = models.NullBooleanField(blank=True, null=True)
    wetland_location = models.ForeignKey(WetlandLocation, on_delete=models.SET_NULL, blank=True, null=True)
    vegetation = models.OneToOneField(WetlandVetegationStructure, on_delete=models.CASCADE, blank=True, null=True)
    connectivity = models.ForeignKey(WetlandConnectivity, on_delete=models.SET_NULL, blank=True, null=True)
    water_source = JSONField(blank=True, null=True)
    habitat_feature = JSONField(blank=True, null=True)


@reversion.register()
class SlimeMoldLifestages(DictionaryTable):
    pass
    # sclerotium_color = models.TextField(blank=True, null=True)
    # sclerotium_size = models.FloatField(default=0.0, blank=True, null=True)
    # sporangia_color = models.TextField(blank=True, null=True)
    # sporangia_size = models.FloatField(default=0.0, blank=True, null=True)
    # streaming_body_color = models.TextField(blank=True, null=True)
    # streaming_body_size = models.FloatField(default=0.0, blank=True, null=True)


class SlimeMoldClass(DictionaryTableExtended):
    pass


class SlimeMoldMedia(DictionaryTable):
    pass


@reversion.register(follow=['taxondetails_ptr'])
class SlimeMoldDetails(TaxonDetails):
    lifestages = JSONField(blank=True, null=True)
    slime_mold_class = JSONField(blank=True, null=True)
    slime_mold_media = JSONField(blank=True, null=True)


@reversion.register()
class ConiferLifestages(DictionaryTable):
    pass


class FernLifestages(DictionaryTable):
    pass


class FloweringPlantLifestages(DictionaryTable):
    pass


class MossLifestages(DictionaryTable):
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
    moisture_regime = JSONField(blank=True, null=True)
    ground_surface = JSONField(blank=True, null=True)
    tree_canopy_cover = models.ForeignKey(CanopyCover, on_delete=models.SET_NULL, blank=True, null=True)
    #common_trees_and_bushes = models.ForeignKey(CommonTreesAndBushes, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    #common_ground_vegetation = models.ForeignKey(CommonGroundVegetation, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    general_habitat_category = JSONField(blank=True, null=True)
    leap_land_cover_category = models.TextField(blank=True, null=True)
    disturbance_type = models.ForeignKey(DisturbanceType, on_delete=models.CASCADE, blank=True, null=True)
    #invasive_plants = models.ForeignKey(InvasivePlants, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    earthworm_evidence = models.ForeignKey(EarthwormEvidence, on_delete=models.CASCADE, blank=True, null=True)
    landscape_position = JSONField(blank=True, null=True)
    aspect = JSONField(blank=True, null=True)
    slope = JSONField(blank=True, null=True)

    class Meta:
        abstract = True


@reversion.register(follow=['taxondetails_ptr'])
class ConiferDetails(PlantDetails):
    lifestages = JSONField(blank=True, null=True)


@reversion.register(follow=['taxondetails_ptr'])
class FernDetails(PlantDetails):
    lifestages = JSONField(blank=True, null=True)


@reversion.register(follow=['taxondetails_ptr'])
class FloweringPlantDetails(PlantDetails):
    lifestages = JSONField(blank=True, null=True)


@reversion.register(follow=['taxondetails_ptr'])
class MossDetails(PlantDetails):
    lifestages = JSONField(blank=True, null=True)


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
    gnat_association = JSONField(blank=True, null=True)
    ants_association = JSONField(blank=True, null=True)
    termite_association = JSONField(blank=True, null=True)
    beetles_association = JSONField(blank=True, null=True)
    snow_flea_association = JSONField(blank=True, null=True)
    slug_association = JSONField(blank=True, null=True)
    snail_association = JSONField(blank=True, null=True)
    skunk_association = JSONField(blank=True, null=True)
    badger_association = JSONField(blank=True, null=True)
    easter_gray_squirrel_association = JSONField(blank=True, null=True)
    chipmunk_association = JSONField(blank=True, null=True)
    other_small_rodent_association = JSONField(blank=True, null=True)
    turtle_association = JSONField(blank=True, null=True)
    deer_association = JSONField(blank=True, null=True)


@reversion.register(follow=['taxondetails_ptr'])
class FungusDetails(TaxonDetails):
    visible_mycelium = models.NullBooleanField(default=False)
    areal_extent = models.TextField(
        blank=True,
        null=True,
        default=''
    )  # FIXME
    mycelium_description = models.TextField(
        blank=True,
        null=True,
        default=''
    )  # FIXME
    canopy_cover = models.ForeignKey(
        CanopyCover,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    aspect = JSONField(
        blank=True,
        null=True
    )
    slope = JSONField(
        blank=True,
        null=True
    )
    landscape_position = JSONField(
        blank=True,
        null=True
    )
    disturbance_type = models.ForeignKey(
        DisturbanceType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    earthworm_evidence = models.ForeignKey(
        EarthwormEvidence,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    #spore_print boolean, # flag for associated photos
    apparent_substrate = JSONField(
        blank=True,
        null=True
    )
    #potential_plant_hosts character varying, # invasive plants # FIXME
    other_observed_associations = models.OneToOneField(
        ObservedAssociations,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    mushroom_vertical_location = JSONField(
        blank=True,
        null=True
    )
    fruiting_bodies_age = models.ForeignKey(
        FruitingBodiesAge,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    mushroom_growth_form = JSONField(
        blank=True,
        null=True
    )
    mushroom_odor = JSONField(
        blank=True,
        null=True
    )
    mushroom_group = models.ForeignKey(
        MushroomGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


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
    type = JSONField(blank=True, null=True)
    notable_features = models.TextField(blank=True, null=True)
    area = models.FloatField(null=True)
    aspect = JSONField(blank=True, null=True)
    slope = JSONField(blank=True, null=True)
    sensitivity = JSONField(blank=True, null=True)
    condition = JSONField(blank=True, null=True)
    leap_land_cover_category = JSONField(blank=True, null=True)
    disturbance_type = models.ForeignKey(DisturbanceType, on_delete=models.CASCADE, blank=True, null=True)
    #invasive_plants = models.ForeignKey(InvasivePlants, on_delete=models.SET_NULL, blank=True, null=True) # FIXME
    earthworm_evidence = models.ForeignKey(EarthwormEvidence, on_delete=models.CASCADE, blank=True, null=True)
    landscape_position = JSONField(blank=True, null=True)
    glaciar_diposit = JSONField(blank=True, null=True)
    pleistocene_glaciar_diposit = JSONField(blank=True, null=True)
    bedrock_and_outcrops = JSONField(blank=True, null=True)
    regional_frequency = JSONField(blank=True, null=True)
    # soils_ssurgo_wrap # FIXME


@reversion.register(follow=['photographs'])
class OccurrenceNaturalArea(Occurrence):
    #details = models.OneToOneField(NaturalAreaDetails, on_delete=models.CASCADE, null=True)
    element = models.ForeignKey(ElementNaturalAreas, on_delete=models.CASCADE, blank=True, null=True)
    photographs = GenericRelation(Photograph, object_id_field='occurrence_fk')
    location = models.OneToOneField(NaturalAreaLocation, on_delete=models.CASCADE, null=True)
