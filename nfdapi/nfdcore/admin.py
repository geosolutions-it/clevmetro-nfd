# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from nfdcore.models import *

# Register your models here.
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_common',
                     'name_sci',
                     'tsn',
                     'synonym',
                     'second_common',
                     'third_common'
    )
    search_fields = ['first_common',
                     'name_sci',
                     'tsn',
                     'synonym',
                     'second_common',
                     'third_common'
    ]
    
admin.site.register(Species, SpeciesAdmin)

admin.site.register(OccurrenceCategory)
admin.site.register(DayTime)
admin.site.register(Season)
admin.site.register(RecordOrigin)
admin.site.register(RecordingStation)
admin.site.register(CmStatus)
admin.site.register(SRank)
admin.site.register(NRank)
admin.site.register(GRank)
admin.site.register(RegionalStatus)
admin.site.register(UsfwsStatus)
admin.site.register(IucnRedListCategory)
admin.site.register(ElementType)
admin.site.register(MushroomGroup)
admin.site.register(Preservative)
admin.site.register(Storage)
admin.site.register(Repository)
admin.site.register(AquaticHabitatCategory)
admin.site.register(Gender)
admin.site.register(Marks)
admin.site.register(DiseasesAndAbnormalities)
admin.site.register(TerrestrialSampler)
admin.site.register(AquaticSampler)
admin.site.register(TerrestrialStratum)
admin.site.register(PondLakeType)
admin.site.register(PondLakeUse)
admin.site.register(ShorelineType)
admin.site.register(LakeMicrohabitat)
admin.site.register(StreamDesignatedUse)
admin.site.register(ChannelType)
admin.site.register(HmfeiLocalAbundance)
admin.site.register(LoticHabitatType)
admin.site.register(WaterFlowType)
admin.site.register(WetlandType)
admin.site.register(WetlandLocation)
admin.site.register(WetlandConnectivity)
admin.site.register(WaterSource)
admin.site.register(WetlandHabitatFeature)
admin.site.register(SlimeMoldLifestages)
admin.site.register(SlimeMoldClass)
admin.site.register(SlimeMoldMedia)
admin.site.register(SlimeMoldDetails)
admin.site.register(PlantDetails)
