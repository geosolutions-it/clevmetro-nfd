from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework.routers import DefaultRouter

from nfdcore import views
from nfdcore import dicttable_views
from .settings import APP_NAME

router = DefaultRouter()
router.register("images", views.PhotoViewSet, "images")
router.register("stats", views.OccurrenceAggregatorViewSet, "stats")
router.register("featuretypes", views.FeatureTypeFormViewSet, "featuretypes")
router.register("taxon", views.TaxonViewSet, "taxon")
router.register("taxon_search", views.ItisBackedSearchViewSet, "taxon_search")
router.register(
    "report_taxon", views.OccurrenceTaxonReportViewSet, "report_taxon")
router.register(
    "report_natural_area",
    views.OccurrenceNaturalAreaReportViewSet,
    "report_natural_area"
)
router.register("taxon_ranks", views.TaxonRanksViewSet, "taxon_ranks")

# dicttable-based views
for cls_name in [i for i in dir(dicttable_views) if i.endswith("ViewSet")]:
    route_name = cls_name.lower().replace("viewset", "")
    router.register(
        route_name,
        getattr(dicttable_views, cls_name),
        route_name
    )



urlpatterns = [
    url(r'^'+APP_NAME+r'api-token-auth/', obtain_jwt_token),
    url(r'^'+APP_NAME+r'api-token-refresh/', refresh_jwt_token),

    # for testing purposes:
    url(r'^'+APP_NAME, include('django.contrib.auth.urls')),
    url(r'^'+APP_NAME+r'rest-auth/', include('rest_auth.urls')),
    url(
        r'^'+APP_NAME+r'api-auth/',
        include('rest_framework.urls', namespace="rest_framework")
    ),

    url(r'^'+APP_NAME+r'admin/', admin.site.urls),


    #url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus)/$', coreviews.TaxonLayerList.as_view(), name='taxonList'),


    url(r'^'+APP_NAME+r'layers/naturalarea/$', views.NaturalAreaLayer.as_view(), name='naturalareaLayer'),
    url(r'^'+APP_NAME+r'layers/plant/$', views.PlantLayer.as_view(), name="plantLayer"),
    url(r'^'+APP_NAME+r'layers/animal/$', views.AnimalLayer.as_view(), name="animalLayer"),
    url(r'^'+APP_NAME+r'layers/slimemold/$', views.SlimeMoldLayer.as_view(), name='slimemoldLayer'),
    url(r'^'+APP_NAME+r'layers/fungus/$', views.FungusLayer.as_view(), name="fungusLayer"),

    url(
        r'^'+APP_NAME+r'list/naturalarea/$',
        views.OccurrenceNaturalAreaList.as_view(),
        name='naturalareaList'
    ),
    url(
        r'^'+APP_NAME+r'list/plant/$',
        views.OccurrencePlantList.as_view(),
        name="plantList"
    ),
    url(
        r'^'+APP_NAME+r'list/animal/$',
        views.OccurrenceAnimalList.as_view(),
        name="animalList"
    ),
    url(
        r'^'+APP_NAME+r'list/slimemold/$',
        views.OccurrenceSlimeMoldList.as_view(),
        name='slimemoldList'
    ),
    url(
        r'^'+APP_NAME+r'list/fungus/$',
        views.OccurrenceFungusList.as_view(),
        name="fungusList"
    ),

    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/$', views.LayerDetail.as_view()),
    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/version/([0-9]+)/$', views.LayerVersionDetail.as_view()),
    # url(r'^'+APP_NAME+r'species/$', views.SpeciesSearch.as_view()),
    # url(r'^'+APP_NAME+r'species/(?P<pk>[0-9]+)/$', views.SpeciesDetail.as_view()),
    url(r'^'+APP_NAME, include(router.urls)),
]
