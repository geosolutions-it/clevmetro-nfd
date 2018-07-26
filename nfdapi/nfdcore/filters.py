#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Filterset classes for clevmetro"""

from django.db.models import Q
from django_filters import rest_framework as django_filters
from rest_framework.filters import BaseFilterBackend

from . import constants
from . import models


class OccurrenceTaxonFilterSet(django_filters.FilterSet):
    featuresubtype = django_filters.filters.CharFilter(
        name="occurrence_cat__code"
    )
    taxon = django_filters.filters.CharFilter(
        method="filter_ranks",
    )
    reservation = django_filters.filters.CharFilter(
        name="location__reservation",
        lookup_expr="icontains",
    )
    watershed = django_filters.filters.CharFilter(
        name="location__watershed",
        lookup_expr="icontains",
    )
    cm_status = django_filters.filters.ModelChoiceFilter(
        name="taxon__cm_status__code",
        queryset=models.CmStatus.objects.all()
    )

    def filter_ranks(self, queryset, name, value):
        """Filter for the input name in all available hierarchical ranks

        This method builds a chained OR lookup using django's Q objects. This
        is suitable for searching in a Taxon's taxonomic ranks, which are
        stored in a JSONField on ``models.Taxon``. This enables  searching
        for a name in any of the taxon's ranks.

        """

        lookup_pattern = "taxon__upper_ranks__{}__name__icontains"
        q_object = Q(
            **{lookup_pattern.format(constants.TAXON_RANKS[0]): value})
        for rank in constants.TAXON_RANKS[1:]:
            q_object = q_object | Q(**{lookup_pattern.format(rank): value})
        return queryset.filter(q_object)

    class Meta:
        model = models.OccurrenceTaxon
        fields = ['location', 'released', 'verified', 'taxon']


class NaturalAreaFilter(django_filters.FilterSet):
    featuresubtype = django_filters.filters.CharFilter(
        name="occurrence_cat__code")
    cm_status = django_filters.filters.ModelChoiceFilter(
        name="element__cm_status__code",
        queryset=models.CmStatus.objects.all()
    )

    class Meta:
        model = models.OccurrenceNaturalArea
        fields = ['released', 'verified']


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ReportTaxonFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get("category").lower()
        result = queryset.filter(occurrence_cat__main_cat__iexact=category)
        rank_name = request.query_params.get("rank_name", "species").lower()
        rank_value = request.query_params.get("rank_value")
        if rank_value:
            lookup = "taxon__upper_ranks__{}__name__icontains".format(
                rank_name)
            result = result.filter(**{lookup: rank_value})
        return result


class BaseOccurrenceReportFilterSet(django_filters.FilterSet):
    reservation = django_filters.CharFilter(method="filter_reservation")
    watershed = django_filters.CharFilter(method="filter_watershed")
    observer = django_filters.CharFilter(name="observation__reporter__name")
    observation_date = django_filters.DateFromToRangeFilter(
        name="observation__observation_date")

    def filter_reservation(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "location__reservation__icontains")

    def filter_watershed(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "location__watershed__icontains")

    def _filter_json_field(self, queryset, name, value, lookup_pattern):
        filter_values = [i.strip() for i in value.split(",")]
        q_object = Q(**{lookup_pattern: filter_values[0]})
        for filter_value in filter_values[1:]:
            q_object = q_object | Q(**{lookup_pattern: filter_value})
        print("q_object: {}".format(q_object))
        return queryset.filter(q_object)

    class Meta:
        model = models.OccurrenceTaxon
        fields = [
            "reservation",
            "watershed",
            "observer",
            "observation_date",
        ]


class OccurrenceTaxonReportFilterSet(BaseOccurrenceReportFilterSet):
    global_status = django_filters.CharFilter(method="filter_global_status")
    state_status = django_filters.CharFilter(method="filter_state_status")
    cm_status = django_filters.CharFilter(method="filter_cm_status")
    county = CharInFilter(name="location__county")
    quad_name = CharInFilter(name="location__quad_name")
    quad_number = CharInFilter(name="location__quad_number")

    def filter_global_status(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "taxon__g_rank__code__icontains")

    def filter_state_status(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "taxon__s_rank__code__icontains")

    def filter_cm_status(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "taxon__cm_status__code__icontains")

    class Meta:
        model = models.OccurrenceTaxon
        fields = [
            "reservation",
            "watershed",
            "county",
            "quad_name",
            "quad_number",
            "global_status",
            "state_status",
            "cm_status",
            "observer",
            "observation_date",
        ]


class OccurrenceNaturalAreaReportFilterSet(BaseOccurrenceReportFilterSet):
    global_status = django_filters.CharFilter(method="filter_global_status")
    state_status = django_filters.CharFilter(method="filter_state_status")
    cm_status = django_filters.CharFilter(method="filter_cm_status")

    def filter_global_status(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "element__g_rank__code__icontains")

    def filter_state_status(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "element__s_rank__code__icontains")

    def filter_cm_status(self, queryset, name, value):
        return self._filter_json_field(
            queryset, name, value, "element__cm_status__code__icontains")

    class Meta:
        model = models.OccurrenceNaturalArea
        fields = [
            "reservation",
            "watershed",
            "global_status",
            "state_status",
            "cm_status",
            "observer",
            "observation_date",
        ]
