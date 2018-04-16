#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""View classes for models that inherit from `models.DictionaryTable`"""

from rest_framework import viewsets

from . import models
from .serializers import GenericDictTableSerializer


def dict_table_viewset_factory(dict_table_model):
    """A class factory for generating viewsets for dicttable based models

    This function acts as a class factory. It generates classes that derive
    from django-rest-framework's ``viewsets.ReadOnlyModelViewSet``.
    It returns a viewset class that can be used to generate API endpoints for
    the various models that are based on ``nfdcore.models.DictionaryTable``.

    The code used here is somewhat obscure, as it is based on meta-programming
    techniques. This approach was chosen in order to reduce the number of
    lines of code that would need to be written in order to generate viewsets
    for all of the existing dicttable models.

    The code itself just calls ``type()`` with the correct arguments in order
    to generate a class at runtime.

    Examples
    --------

    The following example defines the ``ReservationViewSet`` class:

    >>> ReservationViewSet = dict_table_viewset_factory(models.Reservation)

    Without the current function, the equivalent code would be:

    >>> Class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    ...     queryset = models.Reservation.objects.all()
    ...     serializer_class = GenericDictTableSerializer
    ...
    ...     def get_serializer(self, *args, **kwargs):
    ...         return self.serializer_class(
    ...             model=models.Reservation, *args, **kwargs)

    """

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(model=dict_table_model, *args, **kwargs)

    cls_name = "{}ViewSet".format(dict_table_model.__name__)
    cls_attrs = {
        "queryset": dict_table_model.objects.all(),
        "serializer_class": GenericDictTableSerializer,
        "get_serializer": get_serializer,
    }

    return type(
        cls_name,
        (viewsets.ReadOnlyModelViewSet,),
        cls_attrs
    )


_MODELS_TO_SERIALIZE = [
    models.AnimalLifestages,
    models.AquaticHabitatCategory,
    models.AquaticSampler,
    models.Aspect,
    models.BedrockAndOutcrops,
    models.CanopyCover,
    models.ChannelType,
    models.CMSensitivity,
    models.CmStatus,  # this is extended
    models.ConiferLifestages,
    models.DayTime,
    models.DiseasesAndAbnormalities,
    models.ElementType,
    models.FernLifestages,
    models.FloweringPlantLifestages,
    models.FungalAssociationType,
    models.FungusApparentSubstrate,
    models.Gender,
    models.GeneralHabitatCategory,
    models.GlacialDeposit,
    models.GlacialDepositPleistoceneAge,
    models.GroundSurface,
    models.GRank,
    models.HmfeiLocalAbundance,
    models.IucnRedListCategory,
    models.LakeMicrohabitat,
    models.LandscapePosition,
    models.LeapLandCover,
    models.LoticHabitatType,
    models.Marks,
    models.MoistureRegime,
    models.MossLifestages,
    models.MushroomGroup,
    models.MushroomGrowthForm,
    models.MushroomOdor,
    models.MushroomVerticalLocation,
    models.NaturalAreaCondition,
    models.NaturalAreaType,
    models.NRank,
    models.OccurrenceCategory,
    models.PlantCount,
    models.PondLakeType,
    models.PondLakeUse,
    models.Preservative,
    models.RecordOrigin,
    models.RecordingStation,
    models.RegionalFrequency,
    models.RegionalStatus,  # this is extended
    models.Repository,
    models.Reservation,
    models.Season,
    models.ShorelineType,
    models.SlimeMoldClass,  # this is extended
    models.SlimeMoldMedia,
    models.Slope,
    models.SRank,
    models.Storage,
    models.StreamDesignatedUse,
    models.TerrestrialSampler,
    models.TerrestrialStratum,
    models.UsfwsStatus,
    models.WaterFlowType,
    models.WaterSource,
    models.Watershed,
    models.WetlandConnectivity,
    models.WetlandHabitatFeature,
    models.WetlandLocation,
    models.WetlandType,
]

for cls_model in _MODELS_TO_SERIALIZE:
    serializer_cls = dict_table_viewset_factory(cls_model)
    # put serializer_cls in module's namespace so it can be easily accessed
    globals()[serializer_cls.__name__] = serializer_cls
