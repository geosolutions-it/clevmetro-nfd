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

from core import views as coreviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from settings import APP_NAME

urlpatterns = [
    url(r'^'+APP_NAME+r'api-token-auth/', obtain_jwt_token),
    url(r'^'+APP_NAME+r'api-token-refresh/', refresh_jwt_token),
    
    url(r'^'+APP_NAME, include('django.contrib.auth.urls')),
    # for testing purposes:
    url(r'^'+APP_NAME+r'admin/', admin.site.urls),
    # rest auth
    #    url(r'^'+APP_NAME+r'rest-auth/', include('rest_auth.urls')),
    #url(r'^'+APP_NAME+r'api-token-auth/', views.obtain_auth_token),
    
    url(r'^'+APP_NAME+r'test/', coreviews.test_url),
    url(r'^'+APP_NAME+r'test2/', coreviews.test_url2),
    url(r'^'+APP_NAME+r'test3/', coreviews.test_url3),
    
    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus)/$', coreviews.TaxonLayerList.as_view(), name='taxonList'),
    url(r'^'+APP_NAME+r'layers/(naturalarea)/$', coreviews.NaturalAreaLayerList.as_view(), name='naturalareaList'),
    
    url(r'^'+APP_NAME+r'layers/(plant|animal|slimemold|fungus|naturalarea)/([0-9]+)/$', coreviews.LayerDetail.as_view()),
    
    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/([0-9]+)/$', coreviews.get_feature_type),
    url(r'^'+APP_NAME+r'featuretypes/([a-z]+)/$', coreviews.get_feature_type),
    url(r'^'+APP_NAME+r'species/$', coreviews.SpeciesSearch.as_view()),
    url(r'^'+APP_NAME+r'species/(?P<pk>[0-9]+)/$', coreviews.SpeciesDetail.as_view()),
    
    
] 
