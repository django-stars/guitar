import urllib2
import json

FAKE_PACKAGES = (
    'south',
    'django-debug-toolbar',
    'django-extensions',
    'django-social-auth',
    )

class GuitarWebAPI(object):
    def __init__(self, url):
        self.url = url

    def search(self, q):
        url  =self.url + 'search/' + q + '/'
        res = urllib2.urlopen(url)
        return json.loads(res.read())

    def get_config(self, package, version=None):
        url  =self.url + 'search/' + package + '/'
        print url
        res = urllib2.urlopen(url)
        print res



fetcher = GuitarWebAPI('http://localhost:8000/api/v1/')
