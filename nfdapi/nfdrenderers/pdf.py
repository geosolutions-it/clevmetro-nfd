"""PDF renderers

Rendering is done by using django-easy-pdf, which takes a django template and
a context and renders it to PDF. Not all HTML is valid for using with
django-easy-pdf though, specially CSS.

"""

from collections import namedtuple
import datetime as dt
import json

from django.template.defaultfilters import date
from easy_pdf.rendering import render_to_pdf
from rest_framework.renderers import BaseRenderer

from nfdcore import models

TableCell = namedtuple("TableCell", [
    "value",
    "rowspan",
    "colspan",
])


class PdfOccurrenceStatsRenderer(BaseRenderer):
    """PDF Renderer for Occurrence stats

    This renderer mostly prepares the serialized data in such a way as to
    make it suitable for an HTML table.

    """

    media_type = "application/pdf"
    format = "pdf"

    # this attribute denotes the order of columns in the HTML table
    ORDERING = ["category", "subcategory", "phylum", "family", "species"]

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            entry = data["items"][0]
        except IndexError:
            context = {
                "header_rows": [],
                "content_rows": [],
                "total": 0,
                "title": data["title"],
            }
        else:
            group_by_month = entry.has_key("months")
            context = {
                "total": data["total_occurrences"],
                "title": data["title"],
                "header_rows": self.get_header_rows(
                    entry,
                    year=data.get("year"),
                    group_by_month=group_by_month
                ),
                "content_rows": self.get_content_rows(
                    data["items"],
                    group_by_month=group_by_month
                ),
            }
        return render_to_pdf(
            "nfdrenderers/pdf/aggregation_stats.html",
            context
        )

    def get_header_rows(self, entry, year=None, group_by_month=False):
        header_rows = []
        first = []
        rowspan = 2 if group_by_month else 1
        existing_params = entry.keys()
        for item in self.ORDERING:
            if item in existing_params:
                first.append(TableCell(value=item, rowspan=rowspan, colspan=1))
        header_rows.append(first)
        if group_by_month:
            first.append(
                TableCell(value=year or "months", rowspan=1, colspan=12))
            second = []
            for month_index in range(1, 13):
                month_name = date(dt.datetime(2000, month_index, 1), "F")
                second.append(
                    TableCell(value=month_name, rowspan=1, colspan=1))
            header_rows.append(second)
        else:
            first.append(
                TableCell(value="Occurrences", rowspan=rowspan, colspan=1))
        return header_rows

    def get_content_rows(self, items, group_by_month=False):
        counts = self._get_counts(items)
        already_there = []
        content_rows = []
        for item in items:
            row = []
            for parameter in self.ORDERING:
                try:
                    value = item[parameter]
                except KeyError:
                    continue
                if value is None:
                    row.append(
                        TableCell(value="-", rowspan=1, colspan=1))
                elif value not in already_there:
                    rowspan = counts.get(value, 1)
                    row.append(
                        TableCell(value=value, rowspan=rowspan, colspan=1))
                    if value != "Not Specified":
                        already_there.append(value)
            else:
                if group_by_month:
                    for month, occurrences in item["months"].items():
                        row.append(TableCell(value=occurrences,
                                             rowspan=rowspan,
                                             colspan=1))
                else:
                    row.append(TableCell(value=item["occurrences"],
                                         rowspan=rowspan, colspan=1))
            content_rows.append(row)
        return content_rows


    def _get_counts(self, occurrences):
        """Counts the number of times that each value occurs in the input.

        This is a helper function for determining the rowspan of elements
        that should be used when rendering an HTML table.

        Parameters
        ----------
        occurrences: list
            A sequence of dicts in which each value is to be counted

        Returns
        -------
        dict
            A mapping with individual values and the number of times they
            appear on the input

        """

        counts = {}
        for occurrence in occurrences:
            for param, value in occurrence.items():
                if param not in ("occurrences", "month",):
                    counts.setdefault(value, 0)
                    counts[value] += 1
        return counts


class PdfLayerDetailRenderer(BaseRenderer):
    """PDF renderer for individual layer detail"""

    media_type = "application/pdf"
    format = "pdf"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data.get("geom") is not None:
            geom = json.loads(data["geom"])
            lat, lon = geom["coordinates"]
        else:
            lat = None
            lon = None
        no_data = "-"
        if data.get("details") is not None:
            details = {
                "gender": models.Gender.objects.get(
                    code=data["details.gender"]),
                "marks": data["details.marks"] or no_data,
                "abnormalities": data[
                    "details.diseases_and_abnormalities"] or no_data,
            }
        else:
            details = {
                "gender":  no_data,
                "marks":  no_data,
                "abnormalities":  no_data,
            }
        name = data["taxon.name"]
        rank = data["taxon.rank"]
        tsn = data["taxon.tsn"]
        return render_to_pdf(
            "nfdrenderers/pdf/layer_detail.html",
            {
                "taxon": {
                    "name": name,
                    "rank": rank,
                    "tsn": tsn,
                    "taxonomic_units": self.get_taxonomic_units(tsn),
                },
                "observation": {
                    "observation_date": data["observation.observation_date"],
                    "daytime": data["observation.daytime"] or no_data,
                    "season": data["observation.season"] or no_data,
                    "reporter_name": data["observation.reporter.name"],
                    "reporter_email": data["observation.reporter.email"],
                },
                "details": details,
                "location": {
                    "lat": lat,
                    "lon": lon,
                },
                "images": [im["image"] for im in data["images"]]
            }
        )

    def get_taxonomic_units(self, tsn):
        taxon = models.Taxon.objects.get(pk=tsn)
        result = []
        for rank, rank_details in taxon.upper_ranks.items():
            result.append((rank, rank_details["name"]))
        result.append((taxon.rank, taxon.name))
        return result


class BaseOccurrenceReportRenderer(BaseRenderer):
    """Base PDF renderer for occurrences reports"""

    media_type = "application/pdf"
    format = "pdf"

    def get_filters(self, query_params):
        return {
            "reservation": query_params.get("reservation"),
            "watershed": query_params.get("watershed"),
            "global_status": _get_status_field(
                query_params, "global_status", models.GRank),
            "state_status": _get_status_field(
                query_params, "state_status", models.SRank),
            "cm_status": _get_status_field(
                query_params, "cm_status", models.CmStatus),
            "observer": query_params.get("observer"),
            "observation_date": _get_observation_date(query_params),
        }


class OccurrenceTaxonReportRenderer(BaseOccurrenceReportRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        occurrences = []
        for index, occ in enumerate(data):
            occurrence = _get_occurrence(occ)
            try:
                common_name = occ.get(
                    "common_names", {}).get("English", [])[0]
            except IndexError:
                common_name = None
            occurrence.update(
                index=index+1,
                common_name=common_name
            )
            occurrences.append(occurrence)
        query_params = renderer_context["request"].query_params.dict()
        rank_name = query_params.get("rank_name")
        rank_value = query_params.get("rank_value")
        filters = self.get_filters(query_params)
        filters.update(
            feature=" ".join((rank_name, rank_value)) if rank_value else None,
            county=query_params.get("county"),
            quad=_get_quad(query_params),
        )
        return render_to_pdf(
            "nfdrenderers/pdf/taxon_occurrence_report.html",
            context={
                "occurrences": occurrences,
                "filters": {k: v for k, v in filters.items() if v},
            }
        )


class OccurrenceNaturalAreaReportRenderer(BaseOccurrenceReportRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        occurrences = []
        for index, occ in enumerate(data):
            occurrence = _get_occurrence(occ)
            occurrence.update(index=index+1)
            occurrences.append(occurrence)
        query_params = renderer_context["request"].query_params.dict()
        filters = self.get_filters(query_params)
        print("filters: {}".format(filters))
        filters.update(
            natural_area_code_nac=query_params.get("natural_area_code_nac"),
            general_description=query_params.get("general_description"),
            notable_features=query_params.get("notable_features"),
        )
        return render_to_pdf(
            "nfdrenderers/pdf/natural_area_occurrence_report.html",
            context={
                "occurrences": occurrences,
                "filters": {k: v for k, v in filters.items() if v},
            }
        )


def get_status_description(status_model, code):
    result = []
    for status_code in code.split(","):
        try:
            instance = status_model.objects.get(code=status_code)
        except status_model.DoesNotExist:
            pass
        else:
            result.append(" - ".join((instance.code, instance.name)))
    return ", ".join(result)


def _get_quad(query_params):
    quad_name = query_params.get("quad_name")
    quad_number = query_params.get("quad_number")
    return " ".join([i for i in (quad_name, quad_number) if i]) or None


def _get_observation_date(query_params):
    start_date = query_params.pop("observation_date_0", None)
    end_date = query_params.pop("observation_date_1", None)
    if start_date or end_date:
        observation_date = " / ".join((start_date or "-", end_date or "-"))
    else:
        observation_date = None
    return observation_date


def _get_status_field(query_params, status_field, dict_table_model):
    status_code = query_params.get(status_field)
    if status_code is not None:
        result = get_status_description(dict_table_model, status_code)
    else:
        result = None
    return result


def _get_dict_table_field(collection, show_name=True, show_code=False):
    item = collection if isinstance(collection, dict) else collection[0]
    parts = []
    if show_code:
        parts.append(item["code"])
    if show_name:
        parts.append(item["name"])
    return " - ".join(parts) if any(parts) else None


def _get_occurrence(occurrence_data):
    occurrence = occurrence_data.copy()
    reservation = occurrence_data["reservation"]
    watershed = occurrence_data["watershed"]
    state_status = occurrence_data["state_status"]
    fed_status = occurrence_data["federal_status"]
    global_status = occurrence_data["global_status"]
    cm_status = occurrence_data["cm_status"]
    occurrence.update(
        reservation=_get_dict_table_field(
            reservation) if reservation else None,
        watershed=_get_dict_table_field(
            watershed) if watershed else None,
        state_status=_get_dict_table_field(
            state_status, show_code=True) if state_status else None,
        federal_status=_get_dict_table_field(
            fed_status, show_code=True) if fed_status else None,
        global_status=_get_dict_table_field(
            global_status, show_code=True) if global_status else None,
        cm_status=_get_dict_table_field(
            cm_status, show_code=True) if cm_status else None,
    )
    return occurrence
