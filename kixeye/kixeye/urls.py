from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from tools import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kixeye.views.home', name='home'),
    # url(r'^kixeye/', include('kixeye.foo.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/(?P<player_id>\d+)/$', views.edit_player), 
    url(r'^users/', views.player), 
)
