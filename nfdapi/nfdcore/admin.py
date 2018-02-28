# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from . import models


@admin.register(models.Taxon)
class TaxonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rank",
        "kingdom",
    )
    readonly_fields = (
        "name",
        "common_names",
        "rank",
        "kingdom",
        "_upper_ranks",
    )
    fieldsets = (
        (
            None,
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "tsn",
                    "name",
                    "common_names",
                    "rank",
                    "kingdom",
                ),
            }
        ),
        (
            "Other taxonomic ranks",
            {
                "classes": (
                    "collapse",
                    "wide",
                ),
                "fields": (
                    "_upper_ranks",
                ),
            }
        ),
        (
            "Statuses",
            {
                "classes": (
                    "collapse",
                    "wide",
                ),
                "fields": (
                    "cm_status",
                    "s_rank",
                    "n_rank",
                    "g_rank",
                    "native",
                    "leap_concern",
                    "oh_status",
                    "usfws_status",
                    "iucn_red_list_category",
                    "other_code",
                    "ibp_english",
                    "ibp_scientific",
                    "bblab_number",
                    "nrcs_usda_symbol",
                    "synonym_nrcs_usda_symbol",
                    "epa_numeric_code",
                )
            }
        )
    )

    def _upper_ranks(self, instance):
        upper_ranks = instance.upper_ranks
        if upper_ranks is not None:
            result = self._get_pretty_json(upper_ranks)
        else:
            result = None
        return result
    _upper_ranks.short_description = "Upper ranks"

    def _get_pretty_json(self, data):
        to_prettify = json.dumps(data, indent=4)
        formatter = HtmlFormatter(style="colorful")
        highlighted = highlight(to_prettify, JsonLexer(), formatter)
        style = "<style>{}</style><br>".format(formatter.get_style_defs())
        return mark_safe(style + highlighted)


admin.site.register(models.OccurrenceCategory)
admin.site.register(models.DayTime)
admin.site.register(models.Season)
admin.site.register(models.RecordOrigin)
admin.site.register(models.RecordingStation)
admin.site.register(models.CmStatus)
admin.site.register(models.SRank)
admin.site.register(models.NRank)
admin.site.register(models.GRank)
admin.site.register(models.RegionalStatus)
admin.site.register(models.UsfwsStatus)
admin.site.register(models.IucnRedListCategory)
admin.site.register(models.ElementType)
admin.site.register(models.MushroomGroup)
admin.site.register(models.Preservative)
admin.site.register(models.Storage)
admin.site.register(models.Repository)
admin.site.register(models.AquaticHabitatCategory)
admin.site.register(models.Gender)
admin.site.register(models.Marks)
admin.site.register(models.DiseasesAndAbnormalities)
admin.site.register(models.TerrestrialSampler)
admin.site.register(models.AquaticSampler)
admin.site.register(models.TerrestrialStratum)
admin.site.register(models.PondLakeType)
admin.site.register(models.PondLakeUse)
admin.site.register(models.ShorelineType)
admin.site.register(models.LakeMicrohabitat)
admin.site.register(models.StreamDesignatedUse)
admin.site.register(models.ChannelType)
admin.site.register(models.HmfeiLocalAbundance)
admin.site.register(models.LoticHabitatType)
admin.site.register(models.WaterFlowType)
admin.site.register(models.WetlandType)
admin.site.register(models.WetlandLocation)
admin.site.register(models.WetlandConnectivity)
admin.site.register(models.WaterSource)
admin.site.register(models.WetlandHabitatFeature)
admin.site.register(models.SlimeMoldClass)
admin.site.register(models.SlimeMoldMedia)
admin.site.register(models.PlantCount)
admin.site.register(models.MoistureRegime)
admin.site.register(models.GroundSurface)
admin.site.register(models.CanopyCover)
admin.site.register(models.GeneralHabitatCategory)
admin.site.register(models.LandscapePosition)
admin.site.register(models.Aspect)
admin.site.register(models.Slope)
admin.site.register(models.FernLifestages)
admin.site.register(models.FloweringPlantLifestages)
admin.site.register(models.MossLifestages)


