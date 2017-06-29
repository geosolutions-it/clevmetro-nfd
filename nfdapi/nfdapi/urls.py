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
from core.models import OccurrenceTaxon, OccurrenceNaturalArea

from settings import APP_NAME

urlpatterns = [
    url(r'^'+APP_NAME+r'admin/', admin.site.urls),
    url(r'^'+APP_NAME+r'rest-auth/', include('rest_auth.urls')),
    url(r'^'+APP_NAME+r'api-token-auth/', views.obtain_auth_token),
    
    url(r'^'+APP_NAME+r'test/', coreviews.test_url),
    url(r'^'+APP_NAME+r'test2/', coreviews.test_url2),
    url(r'^'+APP_NAME+r'test3/', coreviews.test_url3),
    
    url(r'^'+APP_NAME+r'layers/plants/$', coreviews.TaxonLayerList.as_view(), name='plantList'),
    url(r'^'+APP_NAME+r'layers/animals/$', coreviews.TaxonLayerList.as_view(), name='animalList'),
    url(r'^'+APP_NAME+r'layers/slimemolds/$', coreviews.TaxonLayerList.as_view(), name='slimemoldList'),
    url(r'^'+APP_NAME+r'layers/fungi/$', coreviews.TaxonLayerList.as_view(), name='fungiList'),
    url(r'^'+APP_NAME+r'layers/naturalareas/$', coreviews.NaturalAreaLayerList.as_view(), name='naturalareaList'),
    
    url(r'^'+APP_NAME+r'layers/(plants|animals|slimemolds|fungui|naturalareas)/([0-9]+)/$', coreviews.LayerDetail.as_view()),
    #url(r'^'+APP_NAME+r'layers/(animals)/([0-9]+)/$', coreviews.LayerDetail.as_view()),
    #url(r'^'+APP_NAME+r'layers/(slimemolds)/([0-9]+)/$', coreviews.LayerDetail.as_view()),
    #url(r'^'+APP_NAME+r'layers/(fungi)/([0-9]+)/$', coreviews.get_feature_info),
    #url(r'^'+APP_NAME+r'layers/(naturalareas)/([0-9]+)/$', coreviews.get_feature_info),
    
    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/([0-9]+)/$', coreviews.get_feature_type),
] 
