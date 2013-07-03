#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import url, patterns, include
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from tools import views
admin.autodiscover()


class PlayerViewSet(viewsets.ModelViewSet):
    model = User

class BattleLogViewSet(viewsets.ModelViewSet):
    model = Group

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'battlelogs', views.BattleLogViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kixeye.views.home', name='home'),
    # url(r'^kixeye/', include('kixeye.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
)
