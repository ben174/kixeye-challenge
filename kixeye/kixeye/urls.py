#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import viewsets, routers
from tools import views
from tools.models import Player
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

urlpatterns = patterns('tools.views',
    url(r'^users/$', 'player_list'),
    url(r'^users/(?P<pk>[0-9]+)$', 'player_detail', name='player_detail'),
    url(r'^users/search/$', 'player_search'),
    url(r'^battles/$', 'battle_list'),
)

