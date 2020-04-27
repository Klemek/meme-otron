import re
import sys
import os.path as path
from typing import List, Optional, Union
from Levenshtein import distance


def relative_path(file: str, *args: str) -> str:
    return path.realpath(path.join(path.dirname(path.realpath(file)), *args))


def read_key_safe(d: dict, k: str, default=None, *,
                  types: Optional[List[type]] = None,
                  is_list: bool = False,
                  is_list_size: Optional[int] = None):
    try:
        return read_key(d, k, default, types=types, is_list=is_list, is_list_size=is_list_size)
    except KeyError:
        return default


def read_key(d: dict, k: str, default=None, *,
             types: Optional[List[type]] = None,
             is_list: bool = False,
             is_list_size: Optional[int] = None):
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


def check_type(obj, types: List[type], is_list: bool = False, is_list_size: Optional[int] = None):
    if is_list:
        if not is_list_of(obj, types, is_list_size):
            if is_list_size is not None:
                raise TypeError(f"not a list of {is_list_size} {types[0].__name__}")
            else:
                raise TypeError(f"not a list of {types[0].__name__}")
    else:
        if not is_list_of([obj], types):
            raise TypeError(f"not a {types[0].__name__}")


def is_list_of(obj, types: List[type], length: Optional[int] = None) -> bool:
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


def parse_arguments(src: str) -> List[str]:
    def get_found_match(m: list) -> str:
        f = [g for g in m if len(g) > 0]
        if len(f) > 0:
            return f[0]
        return ""

    return [get_found_match(m) for m in args_regex.findall(src)]


def find_nearest(word: str, wlist: List[str], threshold: int = 5) -> Optional[str]:
    distances = [
        (distance(word, w),  # distance
         abs(len(w) - len(word)),  # length diff
         w)
        for w in wlist]
    distances.sort(key=lambda v: v[1])  # sort by length diff to get the closest (in length) first
    found = min(distances, key=lambda v: v[0] - v[1])  # get the closest in lev. distance
    if found[0] - found[1] > threshold:  # distance is too much
        return None
    return found[2]


def justify_text(src: str, n_lines: int) -> Optional[str]:
    spaces_indexes = find_all(src, " ")
    if n_lines - 1 > len(spaces_indexes):
        return None  # impossible
    if n_lines - 1 == len(spaces_indexes):
        return replace_at(src, "\n", spaces_indexes, 1)
    breaks_positions = [k * (len(src) - 1) / n_lines for k in range(1, n_lines)]
    break_indexes = place_line_breaks(breaks_positions, spaces_indexes)
    return replace_at(src, "\n", break_indexes, 1)


def find_all(src: str, pattern: str) -> List[int]:
    indexes = []
    i = safe_index(src, pattern)
    while i is not None:
        indexes += [i]
        i = safe_index(src, pattern, i + 1)
    return indexes


def replace_at(src: str, pattern: str, indexes: List[int], remove: int) -> str:
    output = ""
    start_index = 0
    for i in indexes:
        output += src[start_index:i] + pattern
        start_index = i + remove
    output += src[start_index:]
    return output


def place_line_breaks(breaks_positions: List[float], spaces_indexes: List[int]) -> List[int]:
    breaks_positions = breaks_positions[:]
    breaks_indexes = []
    dist = sys.maxsize
    for i, value in enumerate(spaces_indexes):
        if not len(breaks_positions):
            break
        if dist < abs(value - breaks_positions[0]):
            breaks_indexes += [spaces_indexes[i - 1]]
            breaks_positions.pop(0)
        else:
            dist = abs(value - breaks_positions[0])
    if len(breaks_positions):
        breaks_indexes += [spaces_indexes[-1]]
    return breaks_indexes


def safe_index(src: Union[str, list], pattern, start: int = 0):
    try:
        return src.index(pattern, start)
    except ValueError:
        return None
