import re
import os.path as path


def relative_path(file, *args):
    return path.realpath(path.join(path.dirname(path.realpath(file)), *args))


def read_key_safe(d, k, default=None):
    """
    TODO

    :param (dict) d: source dict
    :param (str) k: key to read
    :param default: default value
    :return:
    """
    if k in d:
        return d[k]
    else:
        return default


def read_key(d, k, default=None):
    """
    TODO

    :param (dict) d: source dict
    :param (str) k: key to read
    :param default: default value
    :return:
    """
    if k in d:
        return d[k]
    elif default is not None:
        return default
    else:
        raise KeyError(k)


def is_list_of(obj, types, length=None):
    """
    TODO

    :param obj:
    :param (list of type) types:
    :param (int) length:
    :rtype: bool
    :return:
    """
    if not (isinstance(obj, list)):
        return False
    for item in obj:
        found = False
        for t in types:
            if isinstance(item, t):
                found = True
                break
        if not found:
            return False
    if length is not None and len(obj) != length:
        return False
    return True


def is_url(s):
    """
    TODO

    :param (str) s:
    :rtype: bool
    :return:
    """
    return False  # TODO


args_regex = re.compile('"([^"]*)"|\'([^\']*)\'|([^ ]+)')


def parse_arguments(s):
    """
    TODO

    :param (str) s:
    :rtype: list of str
    :return:
    """
    return [[g for g in m if len(g) > 0][0] for m in args_regex.findall(s)]
