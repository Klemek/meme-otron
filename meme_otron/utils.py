import re
import os.path as path


def relative_path(file, *args):
    """
    TODO

    :param (str) file:
    :param (str) args:
    :rtype str
    :return:
    """
    return path.realpath(path.join(path.dirname(path.realpath(file)), *args))


def read_key_safe(d, k, default=None, *, types=None, is_list=False, is_list_size=None):
    """
    TODO

    :param (dict) d: source dict
    :param (str) k: key to read
    :param default: default value
    :param (list of type|None) types: types to check
    :param (bool) is_list: if the type is a list of types
    :param (int|None) is_list_size: size of the list to enforce or None
    :raises TypeError:
    :return:
    """
    try:
        return read_key(d, k, default, types=types, is_list=is_list, is_list_size=is_list_size)
    except KeyError:
        return default


def read_key(d, k, default=None, *, types=None, is_list=False, is_list_size=None):
    """
    TODO

    :param (dict) d: source dict
    :param (str) k: key to read
    :param default: default value
    :param (list of type|None) types: types to check
    :param (bool) is_list: if the type is a list of types
    :param (int|None) is_list_size: size of the list to enforce or None
    :raises TypeError:
    :raises KeyError:
    :return:
    """
    if k in d:
        v = d[k]
        if types is not None:
            try:
                check_type(v, types, is_list, is_list_size)
            except TypeError as e:
                raise TypeError(f"'{k}' is {e}")
        return v
    elif default is not None:
        return default
    else:
        raise KeyError(k)


def check_type(obj, types, is_list=False, is_list_size=None):
    """
    TODO

    :param obj:
    :param (list of type|None) types: types to check
    :param (bool) is_list: if the type is a list of types
    :param (int|None) is_list_size: size of the list to enforce or None
    :raises TypeError:
    :return:
    """
    if is_list:
        if not is_list_of(obj, types, is_list_size):
            if is_list_size is None:
                raise TypeError(f"not a list of {is_list_size} {types[0].__name__}")
            else:
                raise TypeError(f"not a list of {types[0].__name__}")
    else:
        if not is_list_of([obj], types):
            raise TypeError(f"not a {types[0].__name__}")


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


args_regex = re.compile('"([^"]*)"|\'([^\']*)\'|([^ ]+)')


def parse_arguments(s):
    """
    TODO

    :param (str) s:
    :rtype: list of str
    :return:
    """
    return [[g for g in m if len(g) > 0][0] for m in args_regex.findall(s)]
