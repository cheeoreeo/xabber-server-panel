import os
from django.apps import apps
import configparser


def is_older_version(cur_ver, new_ver):
    cur_ver = tuple(cur_ver.split('.'))
    new_ver = tuple(new_ver.split('.'))
    return cur_ver > new_ver


def get_config(module):
    spec_path = os.path.join(apps.get_app_config(module).path, 'module.spec')
    with open(spec_path, 'r') as f:
        spec = f.read()
    return init_string_config(spec)


def init_string_config(string_config):
    config = configparser.ConfigParser()
    config.read_string('[SPEC]\n{}'.format(string_config))
    return config
