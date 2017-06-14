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
from core.models import OccurenceTaxon, OccurenceNaturalArea


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^test0/', coreviews.current_datetime),
    url(r'^layers/taxon/$', GeoJSONLayerView.as_view(model=OccurenceTaxon), name='taxon'),
    url(r'^layers/plant/$', coreviews.PlantLayerView.as_view(model=OccurenceTaxon), name='plantList'),
    url(r'^layers/plant/([0-9]+)/$', coreviews.PlantDetail.as_view(), name='plantDetail'),
    url(r'^layers/animal/$', coreviews.AnimalLayerView.as_view(model=OccurenceTaxon), name='animalList'),
    url(r'^layers/natural-areas/$', GeoJSONLayerView.as_view(model=OccurenceNaturalArea), name='naturalarea'),
] 
