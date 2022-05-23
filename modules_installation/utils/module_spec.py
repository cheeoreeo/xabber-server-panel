import os
from django.apps import apps


def convert_spec(spec):
    return {line.split('=')[0].strip().upper(): line.split('=')[1].strip() for line in spec.splitlines()}


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


default_len_ver = 3  # standard number of digits in split version, example: len('22.05.01'.split('.')) == 3


def sanitize_version(version):
    try:
        version = [int(el.strip()) for el in version.split('.') if int(el) or el == '0']
    except (AttributeError, ValueError):
        return [0, 0, 0]
    if len(version) < default_len_ver:
        missing_numbers = [0 for _ in range(default_len_ver - len(version))]
        version.extend(missing_numbers)
    else:
        version = version[:3]
    return version


def is_older_version(cur_ver, new_ver):
    cur_ver = sanitize_version(cur_ver)
    new_ver = sanitize_version(new_ver)
    for i in range(default_len_ver):
        if cur_ver[i] != new_ver[i]:
            return cur_ver[i] > new_ver[i]
    return True
