from models import OccurrenceCategory, OccurenceTaxon
from models import IucnRedListCategory, UsfwsStatus
from models import ElementSpecies, ElementPlant, ElementBird, Species

plants = ['plant', 'plant_conifer_or_ally', 'plant_fern_or_ally',
          'plant_flowering_plant', 'plant_moss_or_ally']
slime_mold = ['slime_mold']
fungus = ['fungus']
animals = ['animal', 'animal_aquatic_animal', 'animal_land_animal',
           'animal_pond_lake_animal', 'animal_stream_animal', 'animal_wetland_animal']
natural_area = ['natural_area']


occurrence_cat = [('pl', 'plant'),
                  ('an', 'animal'),
                  ('fu', 'fungus'),
                  ('sl', 'slime mold'),
                  ('na', 'natural area')]

occurrence_subcat = [('co', 'Conifer', 'pl'),
                     ('fe', 'Fern', 'pl'),
                     ('fl', 'Flowering plant', 'pl'),
                     ('pl', 'Plant - generic', 'pl'), # for other kind of plants such as non-conifer trees
                     ('mo', 'Moss', 'pl'),
                     ('fu', 'Fungus', 'fu'),
                     ('sl', 'Slime mold', 'sl'),
                     ('ln', 'Land animal', 'an'),
                     ('lk', 'Pond lake animal', 'an'),
                     ('st', 'Stream animal', 'an'),
                     ('we', 'Wetland animal', 'an'),
                     ('na', 'Natural area', 'na')
    ]

iucn_redlist = [('CR', 'CR: Critically endangered'),
                ('DD', 'DD: Data deficient'),
                ('EN', 'EN: Endangered'),
                ('LC', 'LC: Least concern'),
                ('NA', 'NA: Not applicable'),
                ('NE', 'NE: Not evaluated'),
                ('NT', 'NT: Near threatened'),
                ('VU', 'VU: Vulnerable')]

usfws_status = [('C', 'Candidate'),
                ('D', 'Delisted'),
                ('EE', 'Emergency endangered'),
                ('LE', 'Endangered'),
                ('E(S/A)', 'Endangered due to similar appearance'),
                ('NL', 'Not Listed'),
                ('PE', 'Proposed endangered'),
                ('PT', 'Proposed threatened'),
                ('RT', 'Resolved Taxon'),
                ('SC', 'Species of Concern'),
                ('LT', 'Threatened'),
                ('T(S/A)', 'Threatened due to similar appearance'),
                ('UR', 'Under Review')]

def init_model():
    if OccurrenceCategory.objects.count()==0:
        for entry in occurrence_subcat:        
            c = OccurrenceCategory()
            c.code = entry[0]
            c.name = entry[1]
            c.main_cat = entry[2]
            c.save()
    
    if IucnRedListCategory.objects.count()==0:
        for entry in iucn_redlist:        
            c = IucnRedListCategory()
            c.code = entry[0]
            c.name = entry[1]
            c.save()
    
    if UsfwsStatus.objects.count()==0:
        for entry in usfws_status:        
            c = UsfwsStatus()
            c.code = entry[0]
            c.name = entry[1]
            c.save() 

def insert_test_data():
    plant_cat = OccurrenceCategory.objects.get(code='pl')
    iucn_cat = IucnRedListCategory.objects.get(pk=4)
    
    species = Species()
    species.tsn = '19290'
    species.first_common = 'White oak'
    species.name_sci = 'Quercus alba'
    species.save()
    
    sp_elem = ElementPlant()
    sp_elem.other_code = "qrc_alba"
    sp_elem.species = species
    sp_elem.iucn_red_list_category = iucn_cat
    #sp_elem.nrcs_usda_symbol = 
    sp_elem.save()

    t = OccurenceTaxon()
    t.occurrence_cat = plant_cat
    t.geom = 'POINT( -81.564302 41.201797 )'
    t.species_element = sp_elem
    t.save()

    t = OccurenceTaxon()
    t.occurrence_cat = plant_cat
    t.geom = 'POINT( -81.520700 41.243243 )'
    t.species_element = sp_elem
    t.save()
    
    t = OccurenceTaxon()
    t.occurrence_cat = plant_cat
    t.geom = 'POINT( -81.575804 41.279632 )'
    t.species_element = sp_elem
    t.save()
    
    stream_animal_cat = OccurrenceCategory.objects.get(code='st')
    
    species = Species()
    species.tsn = '180549'
    species.first_common = 'North American river otter'
    species.name_sci = 'Lontra canadensis'
    species.save()
    
        
    sp_elem = ElementSpecies()
    sp_elem.other_code = "lontra_cnd"
    sp_elem.species = species
    sp_elem.iucn_red_list_category = iucn_cat
    sp_elem.save()
    
    t = OccurenceTaxon()
    t.geom = 'POINT( -81.554282 41.379035 )'
    t.species_element = sp_elem
    t.occurrence_cat = stream_animal_cat
    t.save()
    
    t = OccurenceTaxon()
    t.geom = 'POINT( -81.546814 41.386602 )'
    t.species_element = sp_elem
    t.occurrence_cat = stream_animal_cat
    t.save()