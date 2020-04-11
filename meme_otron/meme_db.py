import json
import logging

from .types import Pos, Text, Meme
from . import utils

DATA_FILE = "../memes.json"

DATA = {}
ALIASES = {}

logger = logging.getLogger("meme_db")


def load_memes():
    """
    TODO
    """
    try:
        with open(DATA_FILE) as f:
            content = "".join(f.readlines())
        raw_data = json.loads(content)
        if not (isinstance(raw_data, list)):
            raise TypeError(f"Root is not a list")
        for i in range(len(raw_data)):
            load_item(i, raw_data[i])
    except OSError as e:
        logger.error(f"Could not read data file: {e}")
    except json.decoder.JSONDecodeError as e:
        logger.error(f"Wrong JSON syntax '{DATA_FILE}': {e}")
    except TypeError as e:
        logger.error(f"Invalid data file: {e}")


def load_item(i, item):
    """
    TODO

    :param (int) i:
    :param (dict) item:
    """
    item_id = ""
    try:
        if not (isinstance(item, dict)):
            raise TypeError(f"root is not a dict")
        item_id = utils.read_key(item, "id")
        if item_id in DATA:
            raise NameError(f"id '{item_id}' already existing")
        based_on = utils.read_key_safe(item, "based_on")
        abstract = utils.read_key_safe(item, "abstract", False)
        aliases = utils.read_key_safe(item, "aliases", [])
        if not utils.is_list_of(aliases, [str]):
            raise TypeError(f"'aliases' is not a list of str")
        template = None
        font = None
        font_size = None
        texts = None
        if based_on is not None:
            if based_on in DATA:
                template = DATA[based_on].template
                font = DATA[based_on].font
                font_size = DATA[based_on].font_size
                texts = DATA[based_on].clone_texts()
            else:
                raise NameError(f"Reference '{based_on}' not found in data, make sur it's placed before this one")
        if not abstract:
            template = utils.read_key(item, "template", template)
        font = utils.read_key_safe(item, "font", font)
        font_size = utils.read_key_safe(item, "font_size", font_size)
        raw_texts = utils.read_key(item, "texts", texts)
        if texts is None:
            if not (isinstance(raw_texts, list)):
                raise TypeError(f"'texts' is not a list")
            texts = []
            for j in range(len(raw_texts)):
                raw_text = raw_texts[j]
                try:
                    texts += [load_text(j, raw_text)]
                except TypeError as e:
                    logger.warning(f"Item '{item_id}'({i}) / Text {j}: {e}")
        if font is not None:
            if not (isinstance(font, str)):
                raise TypeError(f"'font' is not a str")
            for text in texts:
                if text.font is None:
                    text.font = font
        if font_size is not None:
            if not (isinstance(font_size, float)):
                raise TypeError(f"'font_size' is not a float")
            for text in texts:
                if text.font_size is None:
                    text.font_size = font_size
        if len(texts) == 0:
            logger.warning(f"Item '{item_id}'({i}): no texts loaded")
        else:
            DATA[item_id] = Meme(item_id, aliases, abstract, template, font, font_size, texts)
            for alias in aliases:
                ALIASES[alias] = item_id
            logger.info(f"Loaded meme '{item_id}' with {len(texts)} texts")
    except KeyError as e:
        logger.warning(f"Item '{item_id}'({i}): key {e} not found")
    except TypeError as e:
        logger.warning(f"Item '{item_id}'({i}): {e}")
    except NameError as e:
        logger.warning(f"Item '{item_id}'({i}): {e}")


def load_text(j, raw_text):
    """
    TODO

    :param (int) j:
    :param (dict) raw_text:
    :raises TypeError:
    :rtype: Text
    :return:
    """
    if not (isinstance(raw_text, dict)):
        raise TypeError(f"root is not a dict")
    text = Text(f"text {j+1}")
    if "font" in raw_text:
        if not (isinstance(raw_text["font"], str)):
            raise TypeError(f"'font' is not a str")
        text.font = raw_text["font"]
    if "x_range" in raw_text:
        if not (utils.is_list_of(raw_text["x_range"], [int, float], 2)):
            raise TypeError(f"'x_range' is not a list of 2 float")
        text.x_range = raw_text["x_range"]
    if "y_range" in raw_text:
        if not (utils.is_list_of(raw_text["y_range"], [int, float], 2)):
            raise TypeError(f"'y_range' is not a list of 2 float")
        text.y_range = raw_text["y_range"]
    if "position" in raw_text:
        if raw_text["position"] not in [p.name for p in Pos]:
            raise TypeError(f"'position' is not a valid position (ex: NW, E, SE, ...)")
        text.position = [p for p in Pos if p.name == raw_text["position"]][0]
    if "font_size" in raw_text:
        if not (isinstance(raw_text["font_size"], float)):
            raise TypeError(f"'font_size' is not a float")
        text.font_size = raw_text["font_size"]
    if "fill" in raw_text:
        if not (utils.is_list_of(raw_text["fill"], [int], 3)):
            raise TypeError(f"'fill' is not a list of 3 int")
        text.fill = raw_text["fill"]
    if "stroke_width" in raw_text:
        if not (isinstance(raw_text["stroke_width"], float)):
            raise TypeError(f"'stroke_width' is not a float")
        text.stroke_width = raw_text["stroke_width"]
    if "stroke_fill" in raw_text:
        if not (utils.is_list_of(raw_text["stroke_fill"], [int], 3)):
            raise TypeError(f"'stroke_fill' is not a list of 3 int")
        text.stroke_fill = raw_text["stroke_fill"]
    if "align" in raw_text:
        if raw_text["align"] not in ["left", "center", "right"]:
            raise TypeError(f"'align' is not 'left', 'center' or 'right'")
        text.align = raw_text["align"]
    return text


def get_meme(name):
    """
    TODO

    :param (str) name:
    :rtype: Meme|None
    :return:
    """
    if name in DATA and not DATA[name].abstract:
        return DATA[name].clone()
    elif name in ALIASES:
        return DATA[ALIASES[name]].clone()
    else:
        return None
