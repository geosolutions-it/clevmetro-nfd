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
    t.ocurrence_cat = plant_cat
    t.geom = poly='POINT( 10 10)'
    t.species_element = sp_elem
    t.save()

    t = OccurenceTaxon()
    t.ocurrence_cat = plant_cat
    t.geom = poly='POINT( 20 35)'
    t.species_element = sp_elem
    t.save()