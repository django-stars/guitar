import os
from django.test import TestCase
from django.conf import settings
from configurator.utils import prepare_configuration_json

__all__ = [
    'TestOpenConfig'
]

TESTS_PATH = os.path.join(settings.PROJECT_DIR, 'configurator', 'tests')


class TestOpenConfig(TestCase):
    def test_open(self):
        app_name = 'test'
        config_json = prepare_configuration_json(app_name)

        with open(os.path.join(TESTS_PATH, 'test_open_config_expect.txt'), 'r') as expect:
            self.assertEqual(expect.read(), config_json + '\n')
