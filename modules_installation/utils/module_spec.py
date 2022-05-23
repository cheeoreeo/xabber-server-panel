import os
from django.apps import apps


def convert_spec(spec):
    return {line.split('=')[0].strip(): line.split('=')[1].strip() for line in spec.splitlines()}


def get_spec(module):
    spec = {}
    try:
        path_to_spec = os.path.join(apps.get_app_config(module).path, 'module.spec')
    except LookupError:
        return spec
    if os.path.isfile(path_to_spec):
        with open(path_to_spec, 'r') as f:
            spec = convert_spec(f.read())
    return spec


def is_older_version(cur_ver, new_ver):
    default_len_ver = 3  # standard number of digits in split version, example: len('22.05.01'.split('.')) == 3
    try:
        cur_ver = cur_ver.split('.')
        new_ver = new_ver.split('.')
        for split_ver in cur_ver, new_ver:
            if len(split_ver) < default_len_ver:
                missing_numbers = [0 for _ in range(default_len_ver - len(split_ver))]
                split_ver.extend(missing_numbers)
        for i in range(default_len_ver):
            if int(cur_ver[i]) != int(new_ver[i]):
                return int(cur_ver[i]) > int(new_ver[i])
        return True
    except (AttributeError, ValueError):
        return True
