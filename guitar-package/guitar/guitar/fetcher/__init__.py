FAKE_PACKAGES = (
    'south',
    'django-debug-toolbar',
    'django-extensions',
    'django-social-auth',
    )

class GuitarWebAPI(object):
    def __init__(self, url):
        self.url = url

    def get_config(self, package, version=None):
        # There we should sent request to server and get config :)
        if package in FAKE_PACKAGES:
            return "CONFIG EMULATOR"


fetcher = GuitarWebAPI('http://guitar.djangostars.com')
