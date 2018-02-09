"""Definitions for the forms that are shown by the frontend"""

from django.utils.translation import ugettext_lazy as _

from . import models


def get_form_dict(forms):
    """Transform a list of lists into a dict with the first element as key

    Examples
    --------
    >>> items = [
    ...     ("first", "stuff", ["things",]),
    ...     ("second", "mmore stuff", 1)
    ... ]
    >>> get_form_dict(items)
    {
        "first": ["first", "stuff", ["things"]],
        "second": ["second", "more stuff", 1]
    }

    """

    form_dict = {}
    for form in forms:
        form_dict[form[0]] = form
    return form_dict


MANAGEMENT_FORM_NAME = _('occurrencemanagement')
MANAGEMENT_FORM_ITEMS = [
    {
        "key": "id",
        "label": _("id"),
        "type": "integer",
        'readonly': True
    }, {
        "key": "featuretype",
        "label": _("featuretype"),
        "type": "string",
        'readonly': True
    }, {
        "key": "featuresubtype",
        "label": _("featuresubtype"),
        "type": "string",
        'readonly': True
    }, {
        "key": "released",
        "label": _("released"),
        "type": "boolean",
        'readonly': True
    }, {
        "key": "verified",
        "label": _("verified"),
        "type": "boolean",
        'readonly': False
    }, {
        "key": "inclusion_date",
        "label": _("inclusion_date"),
        "type": "string",
        'readonly': True
    }, {
        "key": "version_date",
        "label": _("version_date"),
        "type": "string",
        'readonly': True
    }
]

MANAGEMENT_FORM_ITEMS_PUBLISHER = [
    {
        "key": "id",
        "label": _("id"),
        "type": "integer",
        'readonly': True
    }, {
        "key": "featuretype",
        "label": _("featuretype"),
        "type": "string",
        'readonly': True
    }, {
        "key": "featuresubtype",
        "label": _("featuresubtype"),
        "type": "string",
        'readonly': True
    }, {
        "key": "released",
        "label": _("released"),
        "type": "boolean",
        'readonly': False
    }, {
        "key": "verified",
        "label": _("verified"),
        "type": "boolean",
        'readonly': False
    }, {
        "key": "inclusion_date",
        "label": _("inclusion_date"),
        "type": "string",
        'readonly': True
    }, {
        "key": "version_date",
        "label": _("version_date"),
        "type": "string",
        'readonly': True
    }
]

LAND_ANIMAL = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    ('details', models.LandAnimalDetails, ['details.lifestages']),
    ('details.lifestages', models.AnimalLifestages, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

STREAM_ANIMAL = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.StreamAnimalDetails, [
            'details.lifestages',
            'details.substrate'
        ]
    ),
    ('details.lifestages', models.AnimalLifestages, []),
    ('details.substrate', models.StreamSubstrate, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

PONDLAKE_ANIMAL = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation, [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    ('details', models.PondLakeAnimalDetails, ['details.lifestages']),
    ('details.lifestages', models.AnimalLifestages, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

WETLAND_ANIMAL = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.WetlandAnimalDetails,
        [
            'details.lifestages',
            'details.vegetation'
        ]
    ),
    ('details.lifestages', models.AnimalLifestages, []),
    ('details.vegetation', models.WetlandVetegationStructure, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

SLIMEMOLD = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    ('details', models.SlimeMoldDetails, ['details.lifestages']),
    ('details.lifestages', models.SlimeMoldLifestages, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

CONIFER_PLANT = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.ConiferDetails,
        [
            'details.lifestages',
            'details.earthworm_evidence',
            'details.disturbance_type'
        ]
    ),
    ('details.lifestages', models.ConiferLifestages, []),
    ('details.earthworm_evidence', models.EarthwormEvidence, []),
    ('details.disturbance_type', models.DisturbanceType, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

FERN_PLANT = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.FernDetails,
        [
            'details.earthworm_evidence',
            'details.disturbance_type'
        ]
    ),
    ('details.earthworm_evidence', models.EarthwormEvidence, []),
    ('details.disturbance_type', models.DisturbanceType, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

FLOWERING_PLANT = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.FloweringPlantDetails,
        [
            'details.earthworm_evidence',
            'details.disturbance_type'
        ]
    ),
    ('details.earthworm_evidence', models.EarthwormEvidence, []),
    ('details.disturbance_type', models.DisturbanceType, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

MOSS_PLANT = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.MossDetails,
        [
            'details.earthworm_evidence',
            'details.disturbance_type'
        ]
    ),
    ('details.earthworm_evidence', models.EarthwormEvidence, []),
    ('details.disturbance_type', models.DisturbanceType, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

FUNGUS = [
    ('species', models.Species, ['species.element_species']),
    ('species.element_species', models.ElementSpecies, []),
    (
        'observation',
        models.OccurrenceObservation, [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('voucher', models.Voucher, []),
    (
        'details',
        models.FungusDetails,
        [
            'details.earthworm_evidence',
            'details.disturbance_type',
            'details.other_observed_associations',
            'details.fruiting_bodies_age'
        ]
    ),
    ('details.earthworm_evidence', models.EarthwormEvidence, []),
    ('details.disturbance_type', models.DisturbanceType, []),
    ('details.other_observed_associations', models.ObservedAssociations, []),
    ('details.fruiting_bodies_age', models.FruitingBodiesAge, []),
    ('location', models.TaxonLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]

NATURAL_AREA = [
    (
        'element',
        models.ElementNaturalAreas,
        [
            'element.earthworm_evidence',
            'element.disturbance_type'
        ]
    ),
    (
        'observation',
        models.OccurrenceObservation,
        [
            'observation.reporter',
            'observation.verifier',
            'observation.recorder'
        ]
    ),
    ('observation.reporter', models.PointOfContact, []),
    ('observation.verifier', models.PointOfContact, []),
    ('observation.recorder', models.PointOfContact, []),
    ('element.earthworm_evidence', models.EarthwormEvidence, []),
    ('element.disturbance_type', models.DisturbanceType, []),
    ('location', models.NaturalAreaLocation, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
]
