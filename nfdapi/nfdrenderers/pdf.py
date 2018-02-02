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
                if value not in already_there and parameter in item.keys():
                    rowspan = counts[value]
                    row.append(
                        TableCell(value=value, rowspan=rowspan, colspan=1))
                    already_there.append(value)
            else:
                if group_by_month:
                    for month, occurrences in item["months"].items():
                        row.append(TableCell(value=occurrences, rowspan=rowspan, colspan=1))
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
                if param not in ("occurrences", "months"):
                    counts.setdefault(value, 0)
                    counts[value] += 1
        return counts


class PdfLayerDetailRenderer(BaseRenderer):
    """PDF renderer for individual layer detail"""

    media_type = "application/pdf"
    format = "pdf"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data["geom"] is not None:
            geom = json.loads(data["geom"])
            lat, lon = geom["coordinates"]
        else:
            lat = None
            lon = None
        gender = models.Gender.objects.get(code=data["details.gender"])
        no_data = "-"
        return render_to_pdf(
            "nfdrenderers/pdf/layer_detail.html",
            {
                "species": {
                    "common_name": data["species.first_common"],
                    "name": data["species.name_sci"],
                    "tsn": data["species.tsn"],
                    "family": data["species.family"],
                },
                "observation": {
                    "observation_date": data["observation.observation_date"],
                    "daytime": data["observation.daytime"] or no_data,
                    "season": data["observation.season"] or no_data,
                    "reporter_name": data["observation.reporter.name"],
                    "reporter_email": data["observation.reporter.email"],
                },
                "details": {
                    "gender": gender.name.capitalize(),
                    "marks": data["details.marks"] or no_data,
                    "abnormalities": data[
                        "details.diseases_and_abnormalities"] or no_data,
                },
                "location": {
                    "lat": lat,
                    "lon": lon,
                },
                "images": [im["image"] for im in data["images"]]
            }
        )
