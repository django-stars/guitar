class Configurator(object):

    def __init__(self, config_json):
        self.config_json = config_json

    def get_patches(self):
        return {
            'urls': {
                'patch': {'obj': "url(r'^admin/', include(admin.site.urls))"},
                'file_path': 'urls.py'
            },
            'middleware': {
                'patch': [
                    {
                        'obj': 'django.contrib.messages.middleware.MessageMiddleware',
                        'between': ('django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware'),
                        # or
                        'before': 'django.middleware.common.CommonMiddleware',
                        # or
                        'after': 'django.middleware.common.CommonMiddleware',
                    },
                ],
                'file_path': 'middleware.py'
            },
            'settings': {
                'patch': [
                    "VAR_A=5",
                    "FOO={'a': 'b'}"
                ],
                'file_path': 'settings.py'

            }
        }
