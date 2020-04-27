import re
import sys
import os.path as path
from Levenshtein import distance


def relative_path(file, *args):
    """
    Get the full path from a starting file and a relative path

    :param (str) file:
    :param (str) args:
    :rtype str
    :return:
    """
    return path.realpath(path.join(path.dirname(path.realpath(file)), *args))


def read_key_safe(d, k, default=None, *, types=None, is_list=False, is_list_size=None):
    """
    Read a value from a dict or return the default value if not found.
    Can also check the type of the value.

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
    Read a value from a dict or return the default value or throw an error if the default is None.
    Can also check the type of the value.

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
    Check the type from a list of possibilities.
    Can check the types of all elements of a list.

    :param obj:
    :param (list of type|None) types: types to check
    :param (bool) is_list: if the type is a list of types
    :param (int|None) is_list_size: size of the list to enforce or None
    :raises TypeError:
    :return:
    """
    if is_list:
        if not is_list_of(obj, types, is_list_size):
            if is_list_size is not None:
                raise TypeError(f"not a list of {is_list_size} {types[0].__name__}")
            else:
                raise TypeError(f"not a list of {types[0].__name__}")
    else:
        if not is_list_of([obj], types):
            raise TypeError(f"not a {types[0].__name__}")


def is_list_of(obj, types, length=None):
    """
    Check the types of all elements of a list.

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
    Split a string into separates arguments

    :param (str) s:
    :rtype: list of str
    :return:
    """

    def get_found_match(m):
        f = [g for g in m if len(g) > 0]
        if len(f) > 0:
            return f[0]
        return ""

    return [get_found_match(m) for m in args_regex.findall(s)]


def find_nearest(word, wlist, threshold=5):
    """
    Find the nearest word in a list

    :param (str) word:
    :param (list of str) wlist:
    :param (int) threshold:
    :rtype: str | None
    :return:
    """
    found = min([(distance(word, w) - abs(len(w) - len(word)), w) for w in wlist], key=lambda v: v[0])
    if found[0] > threshold:
        return None
    return found[1]


def safe_index(src, pattern, start=0):
    """
    :param (list|str) src:
    :param pattern:
    :param (int) start:
    """
    try:
        return src.index(pattern, start)
    except ValueError:
        return None


def find_all(src, pattern):
    """
    :param (str) src:
    :param (str) pattern:
    :rtype: list of int
    """
    o = []
    i = safe_index(src, pattern)
    while i is not None:
        o += [i]
        i = safe_index(src, pattern, i + 1)
    return o


def replace_at(src, pattern, indexes, remove):
    """
    :param (str) src:
    :param (str) pattern:
    :param (list of int) indexes:
    :param (int) remove:
    :rtype: str
    """
    o = ""
    last = 0
    for i in indexes:
        o += src[last:i] + pattern
        last = i + remove
    o += src[last:]
    return o


def break_text(src, n):
    """
    :param (str) src:
    :param (int) n:
    :rtype: str
    """
    spaces = find_all(src, " ")
    if n - 1 > len(spaces):
        return None
    if n - 1 == len(spaces):
        return replace_at(src, "\n", spaces, 1)
    ideal = [k * (len(src) - 1) / n for k in range(1, n)]
    indexes = best_fit(ideal, spaces)
    return replace_at(src, "\n", indexes, 1)


def best_fit(a, b):
    """
    :param (list of float) a:
    :param (list of int) b:
    :rtype: list of int
    """
    a = a[::]
    o = []
    dist = sys.maxsize
    for i, value in enumerate(b):
        if not len(a):
            break
        if dist < abs(value - a[0]):
            o += [b[i - 1]]
            a.pop(0)
        else:
            dist = abs(value - a[0])
    if len(a):
        o += [b[-1]]
    return o
