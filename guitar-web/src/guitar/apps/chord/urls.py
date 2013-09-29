from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('chord.views',
    url(r'^chords/$', 'chord_list', name="list"),
    url(r'^chords/(?P<title>[-_\w]+)/$', 'chord_details', name="details"),
)