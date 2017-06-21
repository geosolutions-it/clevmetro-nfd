from models import OccurrenceCategory, OccurrenceTaxon
from models import IucnRedListCategory, UsfwsStatus
from models import ElementSpecies, DayTime
from models import Season, RecordOrigin, Preservative, Storage, Repository
from models import Gender
from core.models import TerrestrialSampler, LandAnimalDetails,\
    StreamAnimalDetails, TaxonDetails, OccurrenceObservation, PointOfContact
from django.utils import timezone

# mark messages for translations but don't translate then right now 
def _(message): return message


plants = ['plant', 'plant_conifer_or_ally', 'plant_fern_or_ally',
          'plant_flowering_plant', 'plant_moss_or_ally']
slime_mold = ['slime_mold']
fungus = ['fungus']
animals = ['animal', 'animal_aquatic_animal', 'animal_land_animal',
           'animal_pond_lake_animal', 'animal_stream_animal', 'animal_wetland_animal']
natural_area = ['natural_area']

occurrence_cat_dict = {
    'plant': _('Plant'),
    'fungus': _('Fungus'),
    'slime_mold': _('Slime mold'),
    'animal': _('Animal'),
    'natural_area': _('Natural area')
    }


occurrence_subcat = [('co', _('Conifer'), 'plant'),
                     ('fe', _('Fern'), 'plant'),
                     ('fl', _('Flowering plant'), 'plant'),
                     ('pl', _('Plant - generic'), 'plant'), # for other kind of plants such as non-conifer trees
                     ('mo', _('Moss'), 'plant'),
                     ('fu', _('Fungus'), 'fungus'),
                     ('sl', _('Slime mold'), 'slime_mold', ),
                     ('ln', _('Land animal'), 'animal'),
                     ('lk', _('Pond lake animal'), 'animal'),
                     ('st', _('Stream animal'), 'animal'),
                     ('we', _('Wetland animal'), 'animal'),
                     ('na', _('Natural area'), 'natural_area')
    ]

iucn_redlist = [('CR', _('CR: Critically endangered')),
                ('DD', _('DD: Data deficient')),
                ('EN', _('EN: Endangered')),
                ('LC', _('LC: Least concern')),
                ('NA', _('NA: Not applicable')),
                ('NE', _('NE: Not evaluated')),
                ('NT', _('NT: Near threatened')),
                ('VU', _('VU: Vulnerable'))]

usfws_status = [('C', _('Candidate')),
                ('D', _('Delisted')),
                ('EE', _('Emergency endangered')),
                ('LE', _('Endangered')),
                ('E(S/A)', _('Endangered due to similar appearance')),
                ('NL', _('Not Listed')),
                ('PE', _('Proposed endangered')),
                ('PT', _('Proposed threatened')),
                ('RT', _('Resolved Taxon')),
                ('SC', _('Species of Concern')),
                ('LT', _('Threatened')),
                ('T(S/A)', _('Threatened due to similar appearance')),
                ('UR', _('Under Review'))]

day_time = [("da", _("Dawn")),
            ("em", _("Early morning")),
            ("mo", _("Morning")),
            ("lm", _("Late morning")),
            ("no", _("Noon")),
            ("ea", _("Early afternoon")),
            ("af", _("Afternoon")),
            ("la", _("Late afternoon")),
            ("du", _("Dusk")),
            ("ee", _("Early evening")),
            ("ev", _("Evening")),
            ("le", _("Late evening")),
            ("ln", _("Late night/after midnight")),
            ("un", _("Unknown"))]


season = [
    ("eg", _("Early spring")),
    ("mg", _("Mid spring")),
    ("lg", _("Late spring")),
    ("es", _("Early summer")),
    ("ms", _("Mid summer")),
    ("ls", _("Late summer")),
    ("ef", _("Early fall")),
    ("mf", _("Mid fall")),
    ("lf", _("Late fall")),
    ("ew", _("Early winter")),
    ("mw", _("Mid winter")),
    ("lw", _("Late winter"))
    ]
 
record_origin = [
    ("bi", _("bioblitz")),
    ("ct", _("camera trap")),
    ("co", _("checking casual observer report")),
    ("hr", _("checking historical record")),
    ("in", _("incidental")),
    ("mc", _("monitoring, census")),
    ("mi", _("monitoring, initial")),
    ("ml", _("monitoring, long term")),
    ("mp", _("monitoring, property assessment")),
    ("se", _("searching"))
    ]

preservative = [
    ("et", _("ethanol")),
    ("fd", _("formaldehyde")),
    ("fi", _("formalin")),
    ("ft", _("formalternate")),
    ("is", _("isopropanol")),
    ("na", _("N/A"))
    ]

storage = [
    ("es", _("dried egg shell")),
    ("dp", _("dried/pressed/mounted")),
    ("se", _("dried skeletal element")),
    ("ds", _("dried skeleton")),
    ("ds", _("dried skin")),
    ("fr", _("frozen")),
    ("vi", _("vial")),
    ("na", _("N/A"))
]

gender = [
    ("fe", _("female")),
    ("fp", _("female (parthenogenic)")),
    ("gy", _("gynandromorphic")),
    ("he", _("hermaphroditic")),
    ("hp", _("hermaphroditic (parthenogenic)")),
    ("ml", _("male")),
    ("na", _("n/a")),
    ("un", _("unknown"))
    ]

terrestrial_sampler = [
    ("av", _("aspirator/vacuum")),
    ("at", _("audio transect")),
    ("bt", _("baited box/cage trap")),
    ("bf", _("Berlese funnel")),
    ("fo", _("fogger")),
    ("ft", _("funnel trap")),
    ("ga", _("glue trap alone")),
    ("gf", _("glue trap with drift fence")),
    ("hc", _("hand collecting")),
    ("ht", _("harp trap")),
    ("lg", _("light trap")),
    ("ln", _("line transect")),
    ("mt", _("Malaise trap")),
    ("mn", _("mist net")),
    ("ms", _("mustard soil extraction")),
    ("pa", _("pitfall trap alone")),
    ("pf", _("pitfall trap with drift fence")),
    ("sn", _("snare")),
    ("sr", _("sound recording")),
    ("st", _("stovepipe trap")),
    ("wc", _("wildlife camera")),
    ("wt", _("windowpane trap")),
    ("yt", _("yellow pan trap"))
    ]

def _init_dict_table(model_class, values, clean=True):
    if clean:
        model_class.objects.all().delete()
        
    for entry in values:        
        c = model_class()
        c.code = entry[0]
        c.name = entry[1]
        c.save()

def init_model(clean=True):

    _init_dict_table(IucnRedListCategory, iucn_redlist, clean)
    _init_dict_table(UsfwsStatus, usfws_status, clean)
    _init_dict_table(DayTime, day_time, clean)
    _init_dict_table(Season, season, clean)
    _init_dict_table(RecordOrigin, record_origin, clean)
    _init_dict_table(Preservative, preservative, clean)
    _init_dict_table(Gender, gender, clean)
    _init_dict_table(TerrestrialSampler, terrestrial_sampler, clean)
    
    if clean:
        OccurrenceCategory.objects.all().delete()
    for entry in occurrence_subcat:        
        c = OccurrenceCategory()
        c.code = entry[0]
        c.name = entry[1]
        c.main_cat = entry[2]
        c.save()

def insert_test_data(clean=True):
    if clean:
        OccurrenceTaxon.objects.all().delete()
        TaxonDetails.objects.all().delete()
        ElementSpecies.objects.all().delete()
        OccurrenceObservation.objects.all().delete()
        
    plant_cat = OccurrenceCategory.objects.get(code='pl')
    iucn_cat = IucnRedListCategory.objects.get(code='LC')
    
    species = ElementSpecies()
    species.tsn = '19290'
    species.first_common = 'White oak'
    species.name_sci = 'Quercus alba'
    species.other_code = "qrc_alba"
    species.species = species
    species.iucn_red_list_category = iucn_cat
    #sp_elem.nrcs_usda_symbol = 
    species.save()

    t = OccurrenceTaxon()
    t.occurrence_cat = plant_cat
    t.geom = 'POINT( -81.564302 41.201797 )'
    t.species_element = species
    t.save()

    t = OccurrenceTaxon()
    t.occurrence_cat = plant_cat
    t.geom = 'POINT( -81.520700 41.243243 )'
    t.species_element = species
    t.save()
    
    t = OccurrenceTaxon()
    t.occurrence_cat = plant_cat
    t.geom = 'POINT( -81.575804 41.279632 )'
    t.species_element = species
    t.save()
    
    stream_animal_cat = OccurrenceCategory.objects.get(code='st')    
        
    species = ElementSpecies()
    species.tsn = '180549'
    species.first_common = 'North American river otter'
    species.name_sci = 'Lontra canadensis'
    species.other_code = "lontra_cnd"
    species.iucn_red_list_category = iucn_cat
    species.save()
    
    gender = Gender.objects.get(code='fe')
    
    stream_details = StreamAnimalDetails()
    stream_details.gender = gender
    stream_details.stream_name_1 = 'Ramdom stream name1'
    stream_details.save()
    
    reporter = PointOfContact()
    reporter.name = "I'm the reporter"
    reporter.save()
    
    observation = OccurrenceObservation()
    observation.observation_date = timezone.now()
    observation.recording_datetime = timezone.now()
    observation.reporter = reporter
    observation.save()
    
    t = OccurrenceTaxon()
    t.geom = 'POINT( -81.554282 41.379035 )'
    t.species_element = species
    t.occurrence_cat = stream_animal_cat
    t.details = stream_details
    t.observation = observation
    t.save()
    
    stream_details = StreamAnimalDetails()
    stream_details.gender = gender
    stream_details.stream_name_1 = 'Ramdom stream name2'
    stream_details.save()
    
    recorder = PointOfContact()
    recorder.name = "I'm the recorder2"
    recorder.save()
    
    observation = OccurrenceObservation()
    observation.observation_date = timezone.now()
    observation.recording_datetime = timezone.now()
    observation.recorder = recorder
    observation.save()
    
    
    t = OccurrenceTaxon()
    t.geom = 'POINT( -81.546814 41.386602 )'
    t.species_element = species
    t.occurrence_cat = stream_animal_cat
    t.details = stream_details
    t.observation = observation
    t.save()
    
    recorder = PointOfContact()
    recorder.name = "I'm the recorder"
    recorder.save()
    
    observation = OccurrenceObservation()
    observation.observation_date = timezone.now()
    observation.recording_datetime = timezone.now()
    observation.recorder = recorder
    observation.save()
    
    land_animal_cat = OccurrenceCategory.objects.get(code='ln')
    land_animal_details = LandAnimalDetails()
    sound_recording = TerrestrialSampler.objects.get(code='sr')
    land_animal_details.sampler = sound_recording
    
    land_animal_details.gender = gender
    land_animal_details.save()
        
    species = ElementSpecies()
    species.tsn = '180544'
    species.first_common = 'American black bear'
    species.name_sci = 'Ursus americanus'
    species.other_code = "bl_bear"
    species.species = species
    species.iucn_red_list_category = iucn_cat
    species.save()
    
    t = OccurrenceTaxon()
    t.geom = 'POINT( -81.526814 41.366602 )'
    t.species_element = species
    t.occurrence_cat = land_animal_cat
    t.details = land_animal_details
    t.observation = observation
    t.save()
    
    