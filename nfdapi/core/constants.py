from django.utils.translation import ugettext_lazy as _

occurrence_cat_dict = {
    'plant': _('Plant'),
    'fungus': _('Fungus'),
    'slime_mold': _('Slime mold'),
    'animal': _('Animal'),
    'natural_area': _('Natural area')
    }


occurrence_subcat = [('co', 'Conifer', 'plant', _('Conifer')),
                     ('fe', 'Fern', 'plant', _('Fern')),
                     ('fl', 'Flowering plant', 'plant', _('Flowering plant')),
                     ('pl', 'Plant - generic', 'plant', _('Plant - generic')), # for other kind of plants such as non-conifer trees
                     ('mo', 'Moss', 'plant', _('Moss')),
                     ('fu', 'Fungus', 'fungus', _('Fungus')),
                     ('sl', 'Slime mold', 'slime_mold', _('Slime mold')),
                     ('ln', 'Land animal', 'animal', _('Land animal')),
                     ('lk', 'Pond lake animal', 'animal', _('Pond lake animal')),
                     ('st', 'Stream animal', 'animal', _('Stream animal')),
                     ('we', 'Wetland animal', 'animal', _('Wetland animal')),
                     ('na', 'Natural area', 'natural_area', _('Natural area'))
    ]



point_of_contact_items = [{
		"key": "name",
		"label": "Name",
		"type": "string"
	},{
		"key": "affiliation",
		"label": "Affiliation",
		"type": "string"
	},{
		"key": "phone1",
		"label": "Phone",
		"type": "string"
	},{
		"key": "phone2",
		"label": "Other Phone",
		"type": "string"
	},{
		"key": "email",
		"label": "Email",
		"type": "string"
	},{
		"key": "street_address",
		"label": "Street address",
		"type": "string"
	}]

verifier = {
	"formlabel": "Verifier",
	"formname": "verifier",
	"formitems": point_of_contact_items 
}

recorder = {
	"formlabel": "Recorder",
	"formname": "recorder",
	"formitems": point_of_contact_items 
}

reporter = {
	"formlabel": "Reporter",
	"formname": "reporter",
	"formitems": point_of_contact_items 
}

observation = {
	"formlabel": "Observation",
	"formname": "observation",
	"formitems": [
		{
		"key": "recording_datetime",
		"label": "Street address",
		"type": "datetime"
	}, {
		"key": "day_time",
		"label": "Day time",
		"type": "stringcombo"
	},{
		"key": "season",
		"label": "Season",
		"type": "stringcombo"
	},{
		"key": "record_origin",
		"label": "Record origin",
		"type": "stringcombo"
	},{
		"key": "recording_station",
		"label": "Recording station",
		"type": "stringcombo"
	}]
}

animal_detail_items = [{
		"key": "gender",
		"label": "Gender",
		"type": "stringcombo"
	},{
		"key": "marks",
		"label": "Marks",
		"type": "stringcombo"
	},{
		"key": "diseases_and_abnormalities",
		"label": "Diseases and abnormalities",
		"type": "stringcombo"
	}]

land_animal_details = {
	"formlabel": "Details",
	"formname": "land_animal_details",
	"formitems": [{
		"key": "sampler",
		"label": "Sampler",
		"type": "stringcombo"
	},{
		"key": "stratum",
		"label": "Stratum",
		"type": "stringcombo"
	}]+animal_detail_items
}

animal_lifestages = {
	"formlabel": "Animal lifestages",
	"formname": "animal_lifestages",
	"formitems": [{
		"key": "egg",
		"label": "Egg",
		"type": "double"
	},{
		"key": "egg_mass",
		"label": "Egg mass",
		"type": "double"
	},{
		"key": "nest",
		"label": "Nest",
		"type": "double"
	},{
		"key": "early_instar_larva",
		"label": "Early instar larva",
		"type": "double"
	},{
		"key": "larva",
		"label": "Larva",
		"type": "double"
	},{
		"key": "late_instar_larva",
		"label": "Late instar larva",
		"type": "double"
	},{
		"key": "early_instar_nymph",
		"label": "Early instar nymph",
		"type": "double"
	},{
		"key": "nymph",
		"label": "Nymph",
		"type": "double"
	},{
		"key": "late_instar_nymph",
		"label": "Late instar nymph",
		"type": "double"
	},{
		"key": "early_pupa",
		"label": "Early pupa",
		"type": "double"
	},{
		"key": "pupa",
		"label": "Pupa",
		"type": "double"
	},{
		"key": "juvenile",
		"label": "Juvenile",
		"type": "double"
	},{
		"key": "immature",
		"label": "Immature",
		"type": "double"
	},{
		"key": "subadult",
		"label": "Subadult",
		"type": "double"
	},{
		"key": "adult",
		"label": "Adult",
		"type": "double"
	},{
		"key": "adult_pregnant_or_young",
		"label": "Adult pregnant / with young",
		"type": "double"
	},{
		"key": "senescent",
		"label": "Senescent",
		"type": "double"
	},{
		"key": "unknown",
		"label": "Unknown",
		"type": "double"
	},{
		"key": "na",
		"label": "n/a",
		"type": "double"
	}] # FIXME: code the remaining form items
}


featureTypes = {
	"landanimal": {
		"forms": [
			land_animal_details,
			animal_lifestages,
			observation,
			reporter,
			recorder,
			verifier
			]
	}
}