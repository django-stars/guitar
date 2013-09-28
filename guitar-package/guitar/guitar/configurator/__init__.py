
class Configurator(object):

    def __init__(self, config_json):
        self.config_json = config_json

    def get_patches(self):
        return {
            'urls': [
                {'obj': "url(r'^admin/', include(admin.site.urls))"},
            ],
            'middleware': [
                {
                    'obj': 'django.contrib.messages.middleware.MessageMiddleware',
                    'between': ('django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware')
                },
            ],
            'settings': [
                "VAR_A=5",
                "FOO={'a': 'b'}"
            ]
        }
