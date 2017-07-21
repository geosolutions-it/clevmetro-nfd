from models import OccurrenceCategory, OccurrenceTaxon
from models import IucnRedListCategory, UsfwsStatus
from models import ElementSpecies, DayTime, Species
from models import Season, RecordOrigin, Preservative, Storage, Repository
from models import Gender
from core.models import TerrestrialSampler, LandAnimalDetails,\
    StreamAnimalDetails, TaxonDetails, OccurrenceObservation, PointOfContact,\
    Voucher, CmStatus, SRank, NRank, GRank, MushroomGroup, RegionalStatus, Marks,\
    DiseasesAndAbnormalities, AquaticSampler, StreamDesignatedUse, ChannelType,\
    LoticHabitatType, HmfeiLocalAbundance, WaterFlowType, TerrestrialStratum,\
    PondLakeType, PondLakeUse, LakeMicrohabitat, ShorelineType, WetlandType,\
    WetlandLocation, WetlandConnectivity, WetlandHabitatFeature, WaterSource,\
    SlimeMoldMedia, SlimeMoldClass
from django.utils import timezone
import reversion
from reversion.models import Version

# mark messages for translations but don't translate then right now 
def _(message): return message


plants = ['plant', 'plant_conifer_or_ally', 'plant_fern_or_ally',
          'plant_flowering_plant', 'plant_moss_or_ally']
slimemold = ['slimemold']
fungus = ['fungus']
animals = ['animal', 'animal_aquatic_animal', 'animal_land_animal',
           'animal_pond_lake_animal', 'animal_stream_animal', 'animal_wetland_animal']
natural_area = ['natural_area']

occurrence_cat_dict = {
    'plant': _('Plant'),
    'fungus': _('Fungus'),
    'slimemold': _('Slime mold'),
    'animal': _('Animal'),
    'natural_area': _('Natural area')
    }


occurrence_subcat = [('co', _('Conifer'), 'plant'),
                     ('fe', _('Fern'), 'plant'),
                     ('fl', _('Flowering plant'), 'plant'),
                     ('pl', _('Plant - generic'), 'plant'), # for other kind of plants such as non-conifer trees
                     ('mo', _('Moss'), 'plant'),
                     ('fu', _('Fungus'), 'fungus'),
                     ('sl', _('Slime mold'), 'slimemold', ),
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
    ("1", _("dried egg shell")),
    ("2", _("dried/pressed/mounted")),
    ("3", _("dried skeletal element")),
    ("4", _("dried skeleton")),
    ("5", _("dried skin")),
    ("6", _("frozen")),
    ("7", _("vial")),
    ("8", _("N/A"))
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

cm_status =  [
    ("CM0", _("Extirpated"), _("No longer found in Cleveland Metroparks or its watersheds")),
    ("CM1", _("Unique"), _("Single occurrence in Park System or its watersheds")),
    ("CM2", _("Exclusive"), _("Several occurrences but in a single watershed")),
    ("CM3", _("Restricted"), _("Several occurrences, more than one watershed, but all east, west or south")),
    ("CM4", _("Occassional"), _("Several occurrences, more than one watershed, any area")),
    ("CM5", _("Common"), _("Common in Cleveland Metroparks but rare elsewhere")),
    ("CM6", _("Special interest"), _("Tracked for specific purposes"))
    ]

g_rank = [
    ("C", _("Element extant only in cultivation/captivity")),
    ("G?", _("Globally unranked")),
    ("G1", _("Globally critically imperiled")),
    ("G1G2", _("Globally imperiled/critically imperiled")),
    ("G2", _("Globally imperiled")),
    ("G2G3", _("Globally vulnerable/imperiled")),
    ("G3", _("Globally vulnerable")),
    ("G3G4", _("Globally vulnerable/apparently secure")),
    ("G4", _("Globally apparently secure")),
    ("G4G5", _("Globally secure/apparently secure")),
    ("G5", _("Globally demonstrably secure")),
    ("GH", _("Historically known, hoping to rediscover")),
    ("GU", _("Globally unrankable")),
    ]

n_rank = [
    ("N1", _("Critically imperiled in US")),
    ("N1B, N2N", _("Breeding population critically imperiled, non-breeding population imperiled in US")),
    ("N1B, N3N", _("Breeding population imperiled, non-breeding population rare or uncommon in US")),
    ("N1B, N4N", _("Breeding population critically imperiled, non-breeding population apparently secure in US")),
    ("N1B, N5N", _("Breeding population critically imperiled, non-breeding population demonstrably secure in US")),
    ("N1N2", _("Between imperiled and critically imperiled in US")),
    ("N2", _("Imperiled in US")),
    ("N2B, N1N", _("Breeding population imperiled, non-breeding population critically imperiled in US")),
    ("N2B, N3N", _("Breeding population imperiled, non-breeding population rare or uncommon in US")),
    ("N2B, N4N", _("Breeding population imperiled, non-breeding population apparently secure in US")),
    ("N2B, N5N", _("Breeding population imperiled, non-breeding population demonstrably secure in US")),
    ("N2N3", _("Between imperiled and rare in US")),
    ("N3", _("Rare or uncommon in US")),
    ("N3B, N1N", _("Breeding population rare or uncommon, non-breeding population critically imperiled in US")),
    ("N3B, N2N", _("Breeding population rare or uncommon, non-breeding population imperiled in US")),
    ("N3B, N4N", _("Breeding population rare or uncommon, non-breeding population apparently secure in US")),
    ("N3B, N5N", _("Breeding population rare or uncommon, non-breeding population demonstrably secure in US")),
    ("N3N4", _("Between uncommon and common in US")),
    ("N4", _("Widespread, abundant, apparently secure in US")),
    ("N4B, N1N", _("Breeding population apparently secure, non-breeding population criticaly imperiled in US")),
    ("N4B, N2N", _("Breeding population apparently secure, non-breeding population imperiled in US")),
    ("N4B, N3N", _("Breeding population apparently secure, non-breeding population rae or uncommon in US")),
    ("N4B, N5N", _("Breeding population apparently secure, non-breeding population demonstrably secure in US")),
    ("N4N5", _("Assumed secure to demonstrably secure in US")),
    ("N5", _("Demonstrably widespread,abundant and secure in US")),
    ("N5B, N2N", _("Breeding population demonstrably secure, non-breeding population imperiled in US")),
    ("N5B, N3N", _("Breeding population demonstrably secure, non-breeding population rare or uncommon in US")),
    ("N5B, N4N", _("Breeding population demonstrably secure, non-breeding population apparently secure in US")),
    ("NA", _("Accidental in US")),
    ("NE", _("Exotic species established in the US")),
    ("NH", _("Historical occurrences only but it is suspected of still being in US")),
    ("NU", _("Unrankable, more information needed")),
    ("NZ", _("Not a conservation concern in the US"))
    ]
    
s_rank = [
    ("S1", _("Critically imperiled")),
    ("S1B, S2N", _("Breeding population criticaly imperiled, non-breeding population imperiled")),
    ("S1B, S3N", _("Breeding population imperiled, non-breeding population rare or uncommon")),
    ("S1B, S4N", _("Breeding population critically imperiled, non-breeding population apparently secure")),
    ("S1B, S5N", _("Breeding population criticaly imperiled, non-breeding population demonstrably secure")),
    ("S1S2", _("Almost critically imperiled")),
    ("S2", _("Imperiled")),
    ("S2B, S1N", _("Breeding population imperiled, non-breeding population critically imperiled")),
    ("S2B, S3N", _("Breeding population imperiled, non-breeding population rare or uncommon")),
    ("S2B, S4N", _("Breeding population imperiled, non-breeding population apparently secure")),
    ("S2B, S5N", _("Breeding population imperiled, non-breeding population demonstrably secure")),
    ("S2S3", _("Rare to almost imperiled in the state")),
    ("S3", _("Vulnerable because of rarity")),
    ("S3B, S1N", _("Breeding population rare or uncommon, non-breeding population critically imperiled")),
    ("S3B, S2N", _("Breeding population rare or uncommon, non-breeding population imperiled")),
    ("S3B, S4N", _("Breeding population rare or uncommon, non-breeding population apparently secure")),
    ("S3B, S5N", _("Breeding population rare or uncommon, non-breeding population demonstrably secure")),
    ("S3S4", _("Between uncommon and common in the state")),
    ("S4", _("Widespread, abundant, apparently secure in the state")),
    ("S4B, S1N", _("Breeding population apparently secure, non-breeding population criticaly imperiled")),
    ("S4B, S2N", _("Breeding population apparently secure, non-breeding population imperiled")),
    ("S4B, S3N", _("Breeding population apparently secure, non-breeding population rae or uncommon")),
    ("S4B, S5N", _("Breeding population apparently secure, non-breeding population demonstrably secure")),
    ("S4S5", _("Almost completely demonstrably secure")),
    ("S5", _("Demonstrably widespread,abundant and secure")),
    ("S5B, S2N", _("Breeding population demonstrably secure, non-breeding population imperiled")),
    ("S5B, S3N", _("Breeding population demonstrably secure, non-breeding population rare or uncommon")),
    ("S5B, S4N", _("Breeding population demonstrably secure, non-breeding population apparently secure")),
    ("SA", _("Accidental in the state")),
    ("SE", _("Exotic species established in the state")),
    ("SH", _("Historical occurrences only but it is suspected of still being in the state")),
    ("SR", _("Reported in the state but occurrence(s) not documented")),
    ("SU", _("Unrankable, more information needed")),
    ("SZ", _("Not a conservation concern in the state"))
    ]

oh_status = [
    ("A", _("A-Added"), _("Recently added for review")),
    ("E", _("E-State Endangered"), _("Threatened with extirpation in Ohio")),
    ("ET", _("ET-Extinct"), _("No longer exists anywhere")),
    ("P", _("P-Potentially Threatened"), _("There are factors that could become threats in Ohio")),
    ("SC", _("SC-Species of concern"), _("May become threatened")),
    ("SI", _("SI-Special interest"), _("Species at edge of distribution")),
    ("T", _("T-State Threatened"), _("There is a threat to its survival in Ohio")),
    ("X", _("X-Extirpated"), _("Known to no longer exist in Ohio")),
    ("Xp", _("XP-Presumed Extirpated"), _("May no longer exist in Ohio"))
]

mushroom_group = [
    ("AG", _("Agaric (gills)")),
    ("BI", _("Bird's Nest (peridioles)")),
    ("BO", _("Bolete (tubes)")),
    ("CH", _("Chanterelle (no true gills)")),
    ("CL", _("Club or Coral (branches)")),
    ("CR", _("Crust (no pores or teeth)")),
    ("CU", _("Cup (no peridioles)")),
    ("EA", _("Earth tongue")),
    ("FT", _("False truffle (gleba not marbled or labyrinthoid)")),
    ("FL", _("Flask")),
    ("JE", _("Jelly (gelatinous)")),
    ("MO", _("Morel or false morel (elfin saddle)")),
    ("PO", _("Polypore (pores or gill-like)")),
    ("PU", _("Puffball (internal spores)")),
    ("ST", _("Stinkhorn (slimy)")),
    ("TE", _("Teeth (tooth-like projections)")),
    ("TR", _("Truffle (marbled or convoluted gleba)"))
]

marks = [
    ("1", _("adhesive tag color")),
    ("2", _("adhesive tag number")),
    ("3", _("band number")),
    ("4", _("collar color")),
    ("5", _("collar number")),
    ("6", _("colorband pattern")),
    ("7", _("dot color")),
    ("8", _("dot pattern")),
    ("9", _("ear clip")),
    ("10", _("ear tag")),
    ("11", _("finclip")),
    ("12", _("microchip number")),
    ("13", _("none")),
    ("14", _("PIT tag")),
    ("15", _("shell notch")),
    ("16", _("tail clip")),
    ("17", _("toe clip")),
    ("18", _("wing tag color")),
    ("19", _("wing tag number"))
]

diseases = [
    ("1", _("discolorations")),
    ("2", _("injuries")),
    ("3", _("evidence of captivity")),
    ("4", _("deformities")),
    ("5", _("erosions")),
    ("6", _("tumors")),
    ("7", _("fungi")),
    ("8", _("lamprey scars")),
    ("9", _("parasites")),
    ("10", _("ranavirus")),
    ("11", _("chytrid")),
    ("12", _("VHS")),
    ("13", _("other abnormalities")),
    ("14", _("none"))
]

aquatic_sampler = [
    ("1", _("automated sound recording")),
    ("2", _("D-frame")),
    ("3", _("dipnet")),
    ("4", _("electrofishing")),
    ("5", _("gill net")),
    ("6", _("hand caught")),
    ("7", _("Hester-Dendy")),
    ("8", _("hookline")),
    ("9", _("leaf bag")),
    ("10", _("seine")),
    ("11", _("surber sampler")),
    ("12", _("sweep net")),
    ("13", _("trammel net")),
    ("14", _("N/A"))
]


stream_designated_use = [
    ("WWH", _("warm water habitat")),
    ("CWH", _("cold water habitat")),
    ("EWH", _("exceptional warm water habitat")),
    ("NODU", _("no designated use"))
    ]

channel_type = [
    ("1", _("manmade, managed")),
    ("2", _("manmade, unmanaged")),
    ("3", _("natural, altered, not restored")),
    ("4", _("natural, past restoration, recovered")),
    ("5", _("natural, past restoration, recovering")),
    ("6", _("natural, recent restoration")),
    ("7", _("natural, unaltered"))
    ]

hmfei_local_abundance = [
    ("A", _("A- Abundant (10-50 individuals)")),
    ("C", _("C- Common (3-9 individuals)")),
    ("R", _("R- Rare (<3 individuals)")),
    ("V", _("V- Very abundant (>50 individuals)"))
]

lotic_habitat_type = [
    ("1", _("rheocrene spring")),
    ("2", _("primary headwater stream")),
    ("3", _("headwater stream")),
    ("4", _("high gradient stream")),
    ("5", _("low gradient stream")),
    ("6", _("river/large stream")),
    ("7", _("ditch")),
    ("8", _("canal")),
    ("9", _("unknown"))
]

water_flow_type = [
    ("1", _("ephemeral")),
    ("2", _("intermittent")),
    ("3", _("interstitial")),
    ("4", _("perennial"))
]

terrestrial_location_or_stratum = [
    ("1", _("air column")),
    ("2", _("canopy")),
    ("3", _("cave")),
    ("4", _("duff")),
    ("5", _("edge of pond or lake")),
    ("6", _("edge of stream")),
    ("7", _("edge of wetland")),
    ("8", _("habitat edge")),
    ("9", _("habitat interior")),
    ("10", _("herbaceous layer")),
    ("11", _("leaf litter")),
    ("12", _("mineral soil")),
    ("13", _("organic soil")),
    ("14", _("rock outcrop or cliff")),
    ("15", _("understory, bushes")),
    ("16", _("understory, saplings")),
    ("17", _("vine tangle")),
    ("18", _("woody debris"))
]

pond_lake_type = [
    ("1", _("natural")),
    ("2", _("manmade, stormwater")),
    ("3", _("manmade, quarry")),
    ("4", _("manmade, aesthetic")),
    ("5", _("manmade, impoundment")),
    ("6", _("manmade, general")),
    ("7", _("unknown"))
    ]

pond_lake_use = [
    ("1", _("fishing")),
    ("2", _("swimming")),
    ("3", _("brood stock")),
    ("4", _("irrigation")),
    ("5", _("stormwater retention")),
    ("6", _("reservoir")),
    ("7", _("boating and kayaking")),
    ("8", _("ice skating")),
    ("9", _("aesthetic")),
    ("10", _("quarry")),
    ("11", _("grain mill")),
    ("12", _("mitigation")),
    ("13", _("wildlife sanctuary")),
    ("14", _("unknown"))
]

pond_lake_shoreline = [
    ("1", _("brush")),
    ("2", _("cliff")),
    ("3", _("grass")),
    ("4", _("gravel")),
    ("5", _("manmade,concrete")),
    ("6", _("manmade, riprap")),
    ("7", _("mud flats")),
    ("8", _("rock")),
    ("9", _("sand")),
    ("10", _("wooded")),
    ("11", _("woody debris"))
    ]

pond_lake_microhabitat = [
    ("1", _("shoreline")),
    ("2", _("beach")),
    ("3", _("shallow water")),
    ("4", _("deep water")),
    ("5", _("overhanging vegetation")),
    ("6", _("aquatic vegetation")),
    ("7", _("muck/sediment")),
    ("8", _("water column")),
    ("9", _("near-shore")),
    ("10", _("breakwall")),
    ("11", _("marina")),
    ("12", _("dock")),
    ("13", _("bay")),
    ("14", _("intake")),
    ("15", _("outflow")),
    ("16", _("surface")),
    ("17", _("air column")),
    ("18", _("riparian zone")),
    ("19", _("bottom")),
    ("20", _("unknown"))
]

wetland_type = [
    ("1", _("natural")),
    ("2", _("enhanced")),
    ("3", _("manmade, mitigation")),
    ("4", _("manmade, stormwater")),
    ("5", _("restored"))
    ]

wetland_location = [
    ("1", _("coastal")),
    ("2", _("floodplain")),
    ("3", _("upland"))
    ]

wetland_connectivity = [
    ("1", _("isolated")),
    ("2", _("riparian/floodplain")),
    ("3", _("upland mosaic"))
]

water_source = [
    ("1", _("upland groundwater")),
    ("2", _("stormwater")),
    ("3", _("perennial stream")),
    ("4", _("seasonal stream")),
    ("5", _("floodplain groundwater")),
    ("6", _("infrastructure (drain tile, pipe, leak, other)"))
    ]

wetland_habitat_feature = [
    ("1", _("air")),
    ("2", _("boardwalk")),
    ("3", _("dam ")),
    ("4", _("edge/margin")),
    ("5", _("litter")),
    ("6", _("muck")),
    ("7", _("open water")),
    ("8", _("riparian zone")),
    ("9", _("sediment")),
    ("10", _("surface")),
    ("11", _("vegetation, emergent")),
    ("12", _("vegetation, floating")),
    ("13", _("vegetation, submerged")),
    ("14", _("vegetation, terrestrial")),
    ("15", _("water column")),
    ("16", _("woody debris"))
    ]

slime_mold_media = [
    ("1", _("Decaying wood")),
    ("2", _("Droppings")),
    ("3", _("Field or prairie")),
    ("4", _("Forest soil")),
    ("5", _("Lawn")),
    ("6", _("Living plant")),
    ("7", _("Other")),
    ("8", _("Under water"))
    ]

slime_mold_class = [
    ("1", _("Cellular slime mold"), _("Dictyostelia")),
    ("2", _("Plasmodial slime mold"), _("Myxogastria")),
    ("3", _("Slime net"), _("Protostelia"))
    ]

def _init_dict_extended_table(model_class, values, ifempty=True, clean=False):
    if clean:
        model_class.objects.all().delete()
    
    if ifempty:
        if model_class.objects.all().count()>0:
            return
        
    for entry in values:        
        c = model_class()
        c.code = entry[0]
        c.name = entry[1]
        c.description = entry[2]
        c.save()

def _init_dict_table(model_class, values, ifempty=True, clean=False):
    if clean:
        model_class.objects.all().delete()

    if ifempty:
        if model_class.objects.all().count()>0:
            return
        
    for entry in values:        
        c = model_class()
        c.code = entry[0]
        c.name = entry[1]
        c.save()

def init_model(ifempty=True, clean=False):
    _init_dict_extended_table(CmStatus, cm_status)
    _init_dict_table(SRank, s_rank)
    _init_dict_table(NRank, n_rank)
    _init_dict_table(GRank, g_rank)
    
    _init_dict_table(IucnRedListCategory, iucn_redlist, ifempty, clean)
    _init_dict_table(UsfwsStatus, usfws_status, ifempty, clean)
    _init_dict_table(RegionalStatus, oh_status)
    _init_dict_table(MushroomGroup, mushroom_group)
    
    _init_dict_table(DayTime, day_time, ifempty, clean)
    _init_dict_table(Season, season, ifempty, clean)
    _init_dict_table(RecordOrigin, record_origin, ifempty, clean)
    _init_dict_table(Preservative, preservative, ifempty, clean)
    _init_dict_table(Gender, gender, ifempty, clean)
    _init_dict_table(TerrestrialSampler, terrestrial_sampler, ifempty, clean)
    
    
    _init_dict_table(Storage, storage)
    _init_dict_table(Marks, marks)
    _init_dict_table(DiseasesAndAbnormalities, diseases)
    
    _init_dict_table(AquaticSampler, aquatic_sampler)
    _init_dict_table(StreamDesignatedUse, stream_designated_use)
    _init_dict_table(ChannelType, channel_type)
    _init_dict_table(HmfeiLocalAbundance, hmfei_local_abundance)
    _init_dict_table(LoticHabitatType, lotic_habitat_type)
    _init_dict_table(WaterFlowType, water_flow_type)
    _init_dict_table(TerrestrialStratum, terrestrial_location_or_stratum)
    
    _init_dict_table(PondLakeType, pond_lake_type)
    _init_dict_table(PondLakeUse, pond_lake_use)
    _init_dict_table(ShorelineType, pond_lake_shoreline)
    _init_dict_table(LakeMicrohabitat, pond_lake_microhabitat)
    
    _init_dict_table(WetlandType, wetland_type)
    _init_dict_table(WetlandLocation, wetland_location)
    _init_dict_table(WetlandConnectivity, wetland_connectivity)
    _init_dict_table(WaterSource, water_source)
    _init_dict_table(WetlandHabitatFeature, wetland_habitat_feature)
    
    _init_dict_table(SlimeMoldMedia, slime_mold_media)
    _init_dict_extended_table(SlimeMoldClass, slime_mold_class)
    
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
        Species.objects.all().delete()
        ElementSpecies.objects.all().delete()
        OccurrenceObservation.objects.all().delete()
        Voucher.objects.all().delete()
    
    iucn_cat = IucnRedListCategory.objects.get(code='LC')
    """    
    plant_cat = OccurrenceCategory.objects.get(code='pl')
    
    with reversion.create_revision():
        element_species = ElementSpecies()
        element_species.iucn_red_list_category = iucn_cat
        element_species.other_code = "qrc_alba"
        #element_species.nrcs_usda_symbol = 
        element_species.save()
        
        species = Species()
        species.tsn = '19290'
        species.first_common = 'White oak'
        species.name_sci = 'Quercus alba'
        species.element_species = element_species
        species.save()
    
    with reversion.create_revision():
        t = OccurrenceTaxon()
        t.occurrence_cat = plant_cat
        t.geom = 'POINT( -81.564302 41.201797 )'
        t.species = species
        t.save()

    with reversion.create_revision():
        t = OccurrenceTaxon()
        t.occurrence_cat = plant_cat
        t.geom = 'POINT( -81.520700 41.243243 )'
        t.species = species
        t.save()

    with reversion.create_revision():
        t = OccurrenceTaxon()
        t.occurrence_cat = plant_cat
        t.geom = 'POINT( -81.575804 41.279632 )'
        t.species = species
        t.save()
    """
    stream_animal_cat = OccurrenceCategory.objects.get(code='st')    
    
    with reversion.create_revision():
        element_species = ElementSpecies()
        element_species.other_code = "lontra_cnd"
        element_species.iucn_red_list_category = iucn_cat
        element_species.save()
        
        species = Species()
        species.tsn = 180549
        species.first_common = 'North American river otter'
        species.name_sci = 'Lontra canadensis'
        species.element_species = element_species
        species.family = 'Mustelidae'
        species.family_common = 'Mustelids'
        species.phylum = 'Chordata'
        species.phylum_common = 'Chordates'
        species.save()
    
    gender = Gender.objects.get(code='fe')
    
    with reversion.create_revision():
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
        t.species = species
        t.occurrence_cat = stream_animal_cat
        t.details = stream_details
        t.observation = observation
        t.save()
    
    with reversion.create_revision():
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
        t.species = species
        t.occurrence_cat = stream_animal_cat
        t.details = stream_details
        t.observation = observation
        t.save()
    
    with reversion.create_revision():
        recorder = PointOfContact()
        recorder.name = "I'm the recorder"
        recorder.save()
        
        observation = OccurrenceObservation()
        observation.observation_date = timezone.now()
        observation.recording_datetime = timezone.now()
        observation.recorder = recorder
        observation.save()
        
        land_animal_cat = OccurrenceCategory.objects.get(code='ln')
        sound_recording = TerrestrialSampler.objects.get(code='sr')
        land_animal_details = LandAnimalDetails()
        land_animal_details.sampler = sound_recording        
        land_animal_details.gender = gender
        land_animal_details.save()
            
        element_species = ElementSpecies()
        element_species.other_code = "bl_bear"
        element_species.iucn_red_list_category = iucn_cat
        element_species.save()
        
        species = Species()
        species.tsn = 180544
        species.first_common = 'American black bear'
        species.name_sci = 'Ursus americanus'
        species.element_species = element_species
        species.family = 'Ursidae'
        species.family_common = 'Bears'
        species.phylum = 'Chordata'
        species.phylum_common = 'Chordate'
        species.save()
        
        t = OccurrenceTaxon()
        t.geom = 'POINT( -81.526814 41.366602 )'
        t.species = species
        t.occurrence_cat = land_animal_cat
        t.details = land_animal_details
        t.observation = observation
        t.save()

        land_animal_details = LandAnimalDetails()
        camera = TerrestrialSampler.objects.get(code='wc')
        land_animal_details.sampler = camera        
        land_animal_details.gender = gender
        land_animal_details.save()
        
        t = OccurrenceTaxon()
        t.geom = 'POINT( -81.226814 41.166602 )'
        t.species = species
        t.occurrence_cat = land_animal_cat
        t.details = land_animal_details
        t.observation = observation
        t.save()
        
        