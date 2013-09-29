from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('chord.views_api',
    url(r'^search/(?P<q>.+)/$', 'api_chord_search', name="search"),
    url(r'^chords/(?P<title>[-_\w]+)/$', 'api_chord_config', name="details"),
)