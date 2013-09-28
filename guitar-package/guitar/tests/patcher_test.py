import unittest
import shutil
import os
from guitar.patcher import Patcher, SettingsPatcher, MiddlewarePatcher


class TestPatcher(unittest.TestCase):
    settings_py_path = 'tests/settings_py_copy.txt'
    settings_py_expect_path = 'tests/settings_py_expect.txt'

    def setUp(self):
        # Copy settings example
        shutil.copy2('tests/settings_py.txt', self.settings_py_path)

    def tearDown(self):
        # Remove settings example
        os.remove(self.settings_py_path)

    def test_patcher(self):
        patcher_obj = {
            'settings': {
                'file_path': self.settings_py_path,
                'patch': ["FOO='BAR'", "APP_DATA = {'x': 5, 'y':['1','2','3']}"]
            },
            # 'middleware': {
            #     'file_path': self.settings_py_path,
            #     'patch': ["FOO='BAR'", "APP_DATA = {'x': 5, 'y':['1','2','3']}"]
            # }
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


class TestMiddlewarePatcher(unittest.TestCase):
    settings_py = """
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'
"""

    def test_patch_after(self):
        settings_py_append_after = """
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'foo.middleware.bar',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'
"""

        patch_obj = {'before': None, 'after': 'django.middleware.csrf.CsrfViewMiddleware', 'middleware': 'foo.middleware.bar'}
        new_settings_py = MiddlewarePatcher().apply_patch(self.settings_py, patch_obj)
        self.assertEqual(settings_py_append_after, new_settings_py)

    def test_append_before(self):
        settings_py_append_before = """
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'foo.middleware.bar',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'
"""
        patch_obj = {'after': None, 'before': 'django.middleware.csrf.CsrfViewMiddleware', 'middleware': 'foo.middleware.bar'}
        new_settings_py = MiddlewarePatcher().apply_patch(self.settings_py, patch_obj)
        self.assertEqual(settings_py_append_before, new_settings_py)

    def test_append_first(self):
        settings_py_append_before = """
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'foo.middleware.bar',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'
"""
        patch_obj = {'after': None, 'before': 'django.middleware.common.CommonMiddleware', 'middleware': 'foo.middleware.bar'}
        new_settings_py = MiddlewarePatcher().apply_patch(self.settings_py, patch_obj)
        self.assertEqual(settings_py_append_before, new_settings_py)

    def test_append_last(self):
        settings_py_append_before = """
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'foo.middleware.bar',
)

ROOT_URLCONF = 'guitar.urls'

WSGI_APPLICATION = 'guitar.wsgi.application'
"""
        patch_obj = {'before': None, 'after': 'django.contrib.messages.middleware.MessageMiddleware', 'middleware': 'foo.middleware.bar'}
        new_settings_py = MiddlewarePatcher().apply_patch(self.settings_py, patch_obj)
        self.assertEqual(settings_py_append_before, new_settings_py)



