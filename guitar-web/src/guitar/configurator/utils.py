from django.conf import settings
import os
import json


def prepare_configuration_json(app_name):
    path = os.path.join(settings.APPS_CONFIGS_PATH, app_name)
    print path
    if not os.path.exists(path):
        # We haven't config for given app_name
        return None

    with open(os.path.join(path, 'config.json'), 'r') as config_file:
        config = json.loads(config_file.read())

    validate_config(config)

    # Load templates from files
    for patch_config in config:
        if patch_config.get('template_type') == 'file':
            with open(os.path.join(path, '%s.tpl' % patch_config['type']), 'r') as template_file:

                patch_config['template'] = template_file.read()

    return json.dumps(config)


def validate_config(config):
    # TODO: do it)
    return True
