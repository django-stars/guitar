import unittest
import json

from guitar.configurator import Configurator


class TestConfigurator(unittest.TestCase):
    config_path = 'tests/test_config_json.txt'

    maxDiff = None

    def test_configurator(self):
        with open(self.config_path, 'r') as f:
            config = json.loads(f.read())

        file_paths = {
            'settings': 'dummy',
            'urls': 'dummy2',
            'installed_apps': 'dummy',
        }

        configurator = Configurator(config, file_paths)

        answers = [1, 'my_db_name', 'my_db_user', '^test_url/', None]


        for question in configurator:
            answer = answers.pop(0)

            self.assertTrue(question['title'])

            question_answers = question.get('answers', [])

            for _answer in question_answers:
                if _answer['key'] == answer:
                    question.answer(answer)
                    continue

            if question['type'] == 'input':
                question.answer(answer)

        patches = configurator.get_patches()

        patches_expect = {
            u'installed_apps': {
                'file_path': 'dummy',
                'patch': {'item_to_add': u'foo.bar', 'after': u'django.contrib.sessions', 'before': None}
            },
            u'urls': {
                'file_path': 'dummy2',
                'patch': {'item_to_add': u"url(r'^test_url/', include('foo.urls'))", 'after': None, 'before': None}
            },
            u'settings': {
                'file_path': 'dummy',
                'patch': {
                    'item_to_add': u"DATABASES = {\n    'default': {\n        'ENGINE': 'postgresql',\n        'NAME': '',\n        'USER': 'my_db_name',\n        'PASSWORD': 'my_db_user',\n        'HOST': '',\n        'PORT': '',\n    }\n}\n",
                    'after': None,
                    'before': None
                }
            }
        }

        self.assertDictEqual(patches_expect, patches)

    def test_skip_questions(self):
        with open(self.config_path, 'r') as f:
            config = json.loads(f.read())

        file_paths = {
            'settings': 'dummy',
            'urls': 'dummy2',
            'installed_apps': 'dummy',
        }

        configurator = Configurator(config, file_paths)

        answers = [3, '^test_url/', None]

        for question in configurator:
            answer = answers.pop(0)

            self.assertTrue(question['title'])

            question_answers = question.get('answers', [])

            for _answer in question_answers:
                if _answer['key'] == answer:
                    question.answer(answer)
                    continue

            if question['type'] == 'input':
                question.answer(answer)

        patches = configurator.get_patches()

        patches_expect = {
            u'installed_apps': {
                'file_path': 'dummy',
                'patch': {
                    'item_to_add': u'foo.bar',
                    'after': u'django.contrib.sessions',
                    'before': None
                }
            },
            u'urls': {
                'file_path': 'dummy2',
                'patch': {
                    'item_to_add': u"url(r'^test_url/', include('foo.urls'))",
                    'after': None,
                    'before': None}
                },
            u'settings': {
                'file_path': 'dummy',
                'patch': {
                    'item_to_add': u"DATABASES = {\n    'default': {\n        'ENGINE': 'sqlite3',\n        'NAME': '',\n        'USER': '',\n        'PASSWORD': '',\n        'HOST': '',\n        'PORT': '',\n    }\n}\n",
                    'after': None,
                    'before': None
                }
            }
        }

        self.assertDictEqual(patches_expect, patches)
