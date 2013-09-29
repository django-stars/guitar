from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'chord.views.home', name="home"),
    url(r'', include("chord.urls", namespace='chord')),
    url(r'api/v1/', include("chord.urls_api", namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)
