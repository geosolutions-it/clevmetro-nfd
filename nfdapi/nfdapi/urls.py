"""nfdapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from nfdcore import views as coreviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from settings import APP_NAME
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('images', coreviews.PhotoViewSet, 'images')

urlpatterns = [
    url(r'^'+APP_NAME+r'api-token-auth/', obtain_jwt_token),
    url(r'^'+APP_NAME+r'api-token-refresh/', refresh_jwt_token),

    # for testing purposes:
    url(r'^'+APP_NAME, include('django.contrib.auth.urls')),
    url(r'^'+APP_NAME+r'rest-auth/', include('rest_auth.urls')),

    url(r'^'+APP_NAME+r'admin/', admin.site.urls),


    #url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus)/$', coreviews.TaxonLayerList.as_view(), name='taxonList'),


    url(r'^'+APP_NAME+r'layers/naturalarea/$', coreviews.NaturalAreaLayer.as_view(), name='naturalareaLayer'),
    url(r'^'+APP_NAME+r'layers/plant/$', coreviews.PlantLayer.as_view(), name="plantLayer"),
    url(r'^'+APP_NAME+r'layers/animal/$', coreviews.AnimalLayer.as_view(), name="animalLayer"),
    url(r'^'+APP_NAME+r'layers/slimemold/$', coreviews.SlimeMoldLayer.as_view(), name='slimemoldLayer'),
    url(r'^'+APP_NAME+r'layers/fungus/$', coreviews.FungusLayer.as_view(), name="fungusLayer"),

    url(r'^'+APP_NAME+r'list/naturalarea/$', coreviews.NaturalAreaList.as_view(), name='naturalareaList'),
    url(r'^'+APP_NAME+r'list/plant/$', coreviews.PlantList.as_view(), name="plantList"),
    url(r'^'+APP_NAME+r'list/animal/$', coreviews.AnimalList.as_view(), name="animalList"),
    url(r'^'+APP_NAME+r'list/slimemold/$', coreviews.SlimeMoldList.as_view(), name='slimemoldList'),
    url(r'^'+APP_NAME+r'list/fungus/$', coreviews.FungusList.as_view(), name="fungusList"),

    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/$', coreviews.LayerDetail.as_view()),
    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/version/([0-9]+)/$', coreviews.LayerVersionDetail.as_view()),

    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/([0-9]+)/$', coreviews.get_feature_type),
    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/$', coreviews.get_feature_type),
    url(r'^'+APP_NAME+r'species/$', coreviews.SpeciesSearch.as_view()),
    url(r'^'+APP_NAME+r'species/(?P<pk>[0-9]+)/$', coreviews.SpeciesDetail.as_view()),
    url(r'^'+APP_NAME, include(router.urls)),
]
