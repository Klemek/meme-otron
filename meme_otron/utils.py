import re
import select
import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
import os.path as path
from typing import List, Optional, Union, Tuple, BinaryIO
from Levenshtein import distance


# region path utils


def relative_path(file: str, *args: str) -> str:
    return path.realpath(path.join(path.dirname(path.realpath(file)), *args))


# endregion

# region dict utils


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


# endregion

# region type utils


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


# endregion

# region args utils


args_regex = re.compile('"([^"]*)"|\'([^\']*)\'|([^ ]+)')


def parse_arguments(src: str) -> List[str]:
    def get_found_match(m: list) -> str:
        f = [g for g in m if len(g) > 0]
        if len(f) > 0:
            return f[0]
        return ""

    return [get_found_match(m) for m in args_regex.findall(src)]


def read_argument(args: List[str], *names: str, valued: bool = False, delete: bool = False):
    for i, arg in enumerate(args):
        if arg.lower() in names:
            if delete:
                del args[i]
                i -= 1
            if not valued:
                return True
            else:
                v = None
                if i + 1 < len(args):
                    v = args[i + 1]
                    if delete:
                        del args[i + 1]
                return v
    if valued:
        return None
    else:
        return False


def split_arguments(args: Union[List[str], Tuple[str]], separator: str) -> List[List[str]]:
    output = [[]]
    for argument in args:
        if argument == separator:
            output += [[]]
        else:
            output[-1] += [argument]
    return [part for part in output if len(part) > 0]


# endregion

# region lang utils


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


def sanitize_input(src: str) -> str:
    return re.sub(r'[^A-Za-z0-9 _]', "", src.lower().strip())


# endregion

# region format utils

def justify_text(src: str, n_lines: int) -> Optional[str]:
    spaces_indexes = find_all(src, " ")
    if n_lines - 1 > len(spaces_indexes):
        return None  # impossible
    if n_lines - 1 == len(spaces_indexes):
        return replace_at(src, "\n", spaces_indexes, 1)
    breaks_positions = [k * (len(src) - 1) / n_lines for k in range(1, n_lines)]
    break_indexes = place_line_breaks(breaks_positions, spaces_indexes)
    return replace_at(src, "\n", break_indexes, 1)


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


# endregion

# region string utils


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


def safe_index(src: Union[str, list], pattern, start: int = 0):
    try:
        return src.index(pattern, start)
    except ValueError:
        return None


# endregion

# region stream utils


def is_stdin_ready() -> bool:
    """
    https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
    """
    return sys.stdin.isatty() and select.select([sys.stdin, ], [], [], 0.0)[0]


def read_stream(stream: BinaryIO) -> bytes:
    output_data = bytearray()
    for line in stream:
        output_data += line
    return output_data


# endregion


# region web utils


def read_web_file(url: str, *, timeout: float = 5,
                  max_file_size: Optional[int] = None) -> Tuple[Optional[bytes], Optional[str]]:
    if not validate_url(url):
        return None, 'Invalid URL'
    try:
        with urlopen(url, None, timeout) as web_file:
            if max_file_size is not None and int(web_file.info()['Content-Length']) > max_file_size:
                return None, 'File too big'
            return web_file.read(), None
    except HTTPError as e:
        return None, f'Could not connect: {e}'
    except URLError:
        return None, f'Could not connect to server'


def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme != "" and parsed.netloc != ""

# endregion
