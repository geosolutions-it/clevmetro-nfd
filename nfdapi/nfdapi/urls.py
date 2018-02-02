from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework.routers import DefaultRouter

from nfdcore import views
from .settings import APP_NAME

router = DefaultRouter()
router.register('images', views.PhotoViewSet, 'images')
router.register('stats', views.OccurrenceAggregatorViewSet, "stats")

urlpatterns = [
    url(r'^'+APP_NAME+r'api-token-auth/', obtain_jwt_token),
    url(r'^'+APP_NAME+r'api-token-refresh/', refresh_jwt_token),

    # for testing purposes:
    url(r'^'+APP_NAME, include('django.contrib.auth.urls')),
    url(r'^'+APP_NAME+r'rest-auth/', include('rest_auth.urls')),

    url(r'^'+APP_NAME+r'admin/', admin.site.urls),


    #url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus)/$', coreviews.TaxonLayerList.as_view(), name='taxonList'),


    url(r'^'+APP_NAME+r'layers/naturalarea/$', views.NaturalAreaLayer.as_view(), name='naturalareaLayer'),
    url(r'^'+APP_NAME+r'layers/plant/$', views.PlantLayer.as_view(), name="plantLayer"),
    url(r'^'+APP_NAME+r'layers/animal/$', views.AnimalLayer.as_view(), name="animalLayer"),
    url(r'^'+APP_NAME+r'layers/slimemold/$', views.SlimeMoldLayer.as_view(), name='slimemoldLayer'),
    url(r'^'+APP_NAME+r'layers/fungus/$', views.FungusLayer.as_view(), name="fungusLayer"),

    url(r'^'+APP_NAME+r'list/naturalarea/$', views.NaturalAreaList.as_view(), name='naturalareaList'),
    url(r'^'+APP_NAME+r'list/plant/$', views.PlantList.as_view(), name="plantList"),
    url(r'^'+APP_NAME+r'list/animal/$', views.AnimalList.as_view(), name="animalList"),
    url(r'^'+APP_NAME+r'list/slimemold/$', views.SlimeMoldList.as_view(), name='slimemoldList'),
    url(r'^'+APP_NAME+r'list/fungus/$', views.FungusList.as_view(), name="fungusList"),

    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/$', views.LayerDetail.as_view()),
    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/version/([0-9]+)/$', views.LayerVersionDetail.as_view()),

    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/([0-9]+)/$', views.get_feature_type),
    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/$', views.get_feature_type),
    url(r'^'+APP_NAME+r'species/$', views.SpeciesSearch.as_view()),
    url(r'^'+APP_NAME+r'species/(?P<pk>[0-9]+)/$', views.SpeciesDetail.as_view()),
    url(r'^'+APP_NAME, include(router.urls)),
]
