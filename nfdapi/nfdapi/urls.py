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

from rest_framework.authtoken import views
from core import views as coreviews
from djgeojson.views import GeoJSONLayerView
from core.models import OccurrenceTaxon, OccurrenceNaturalArea

from settings import APP_NAME

urlpatterns = [
    url(r'^'+APP_NAME+r'/admin/', admin.site.urls),
    url(r'^'+APP_NAME+r'/rest-auth/', include('rest_auth.urls')),
    url(r'^'+APP_NAME+r'/api-token-auth/', views.obtain_auth_token),
    url(r'^'+APP_NAME+r'/test0/', coreviews.current_datetime),
    url(r'^'+APP_NAME+r'/layers/taxon/$', GeoJSONLayerView.as_view(model=OccurrenceTaxon), name='taxon'),
    url(r'^'+APP_NAME+r'/layers/plants/$', coreviews.PlantLayerView.as_view(model=OccurrenceTaxon), name='plantList'),
    url(r'^'+APP_NAME+r'/layers/plants/([0-9]+)/$', coreviews.PlantDetail.as_view(), name='plantDetail'),
    url(r'^'+APP_NAME+r'/layers/animals/$', coreviews.AnimalLayerView.as_view(model=OccurrenceTaxon), name='animalList'),
    url(r'^'+APP_NAME+r'/layers/slimemolds/$', coreviews.SlimeMoldLayerView.as_view(model=OccurrenceTaxon), name='slimemoldList'),
    url(r'^'+APP_NAME+r'/layers/animals/$', coreviews.AnimalLayerView.as_view(model=OccurrenceTaxon), name='animalList'),
    url(r'^'+APP_NAME+r'/layers/fungi/$', coreviews.FungusLayerView.as_view(model=OccurrenceTaxon), name='fungiList'),
    url(r'^'+APP_NAME+r'/layers/naturalareas/$', coreviews.NaturalAreaLayerView.as_view(model=OccurrenceNaturalArea), name='naturalareaList'),
    url(r'^'+APP_NAME+r'/featuretypes/([a-z]+)/([0-9]+)/$', coreviews.get_feature_type),
] 
