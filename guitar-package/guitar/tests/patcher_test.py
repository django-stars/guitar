import unittest
import shutil
import os
from guitar.patcher import Patcher, SettingsPatcher


class TestPatcher(unittest.TestCase):
    settings_py_path = 'tests/settings_py_copy.txt'
    settings_py_expect_path = 'tests/settings_py_expect.txt'

    def setUp(self):
        # Copy settings example
        print shutil.copy2('tests/settings_py.txt', self.settings_py_path)

    def tearDown(self):
        # Remove settings example
        os.remove(self.settings_py_path)

    def test_patcher(self):
        patcher_obj = {
            'settings': {
                'file_path': self.settings_py_path,
                'patch': ["FOO='BAR'", "APP_DATA = {'x': 5, 'y':['1','2','3']}"]
            }
        }

        Patcher().patch(patcher_obj)

        with open(self.settings_py_path, 'r') as f:
            content = f.read()

        with open(self.settings_py_expect_path, 'r') as f:
            content_expect = f.read()

        self.assertEqual(content_expect, content)


class TestPatchSettings(unittest.TestCase):
    settings_py = """
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'
"""
    settings_py_after_patch = """
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'

FOO='BAR'
APP_DATA = {'x': 5, 'y':['1','2','3']}
"""

    def test_patch_settings(self):
        patch_obj = ["FOO='BAR'", "APP_DATA = {'x': 5, 'y':['1','2','3']}"]
        new_settings_py = SettingsPatcher().apply_patch(self.settings_py, patch_obj)
        self.assertEqual(self.settings_py_after_patch, new_settings_py)



