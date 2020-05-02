from typing import Optional
import json
import logging

from .types import Pos, Text, Meme
from . import utils

DATA_FILE = utils.relative_path(__file__, "..", "memes.json")

DATA = {}
ALIASES = {}
LIST = []

logger = logging.getLogger("meme_db")


def load_memes(purge: bool = False):
    global DATA, ALIASES, LIST
    if purge:
        DATA.clear()
        ALIASES.clear()
        LIST = []
    try:
        with open(DATA_FILE) as input_file:
            content = "".join(input_file.readlines())
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


def load_item(i: int, item: dict):
    global LIST
    # TODO reduce complexity
    item_id = ""
    try:
        if not (isinstance(item, dict)):
            raise TypeError(f"root is not a dict")
        item_id = utils.read_key(item, "id", types=[str])
        if len(item_id.strip()) == 0:
            return
        if item_id in DATA:
            raise NameError(f"id '{item_id}' already existing")
        based_on = utils.read_key_safe(item, "based_on", types=[str])
        if based_on is not None:
            if based_on in DATA:
                meme = DATA[based_on].clone()
                meme.id = item_id
            else:
                raise NameError(f"Reference '{based_on}' not found in data, make sur it's placed before this one")
        else:
            meme = Meme(item_id)
        meme.abstract = utils.read_key_safe(item, "abstract", False, types=[bool])
        meme.aliases = utils.read_key_safe(item, "aliases", [], types=[str], is_list=True)
        meme.info = utils.read_key_safe(item, "info", types=[str])
        meme.text_base = load_text(0, item, meme.text_base)
        if not meme.abstract:
            meme.template = utils.read_key(item, "template", meme.template, types=[str])
        raw_texts = utils.read_key(item, "texts", meme.texts, types=[dict], is_list=True)
        if "texts" in item:
            meme.texts = []
            current_text = 1
            for j in range(len(raw_texts)):
                raw_text = raw_texts[j]
                try:
                    text = load_text(current_text, raw_text)
                    if text.text_ref is None:
                        current_text += 1
                    elif text.text_ref < 1 or text.text_ref > len(meme.texts):
                        logger.warning(
                            f"Item '{item_id}'({i + 1}) / Text {j + 1}: invalid text reference {text.text_ref}")
                        continue
                    else:
                        text.text_ref -= 1
                        text.text = meme.texts[text.text_ref].text
                    if text.style_ref is not None:
                        if text.style_ref < 1 or text.style_ref > len(meme.texts):
                            logger.warning(
                                f"Item '{item_id}'({i + 1}) / Text {j + 1}: invalid style reference {text.style_ref}")
                        else:
                            text.style_ref -= 1
                            text.update(meme.texts[text.style_ref])
                    meme.texts += [text]
                    meme.texts_len = current_text - 1
                except TypeError as e:
                    logger.warning(f"Item '{item_id}'({i + 1}) / Text {j + 1}: {e}")
            for text in meme.texts:
                text.update(meme.text_base)
        else:
            DATA[item_id] = meme
            if not meme.abstract:
                LIST += [item_id]
                ALIASES[item_id] = item_id
                for alias in meme.aliases:
                    if alias in ALIASES:
                        logger.warning(
                            f"Item '{item_id}'({i + 1}): alias '{alias}' already registered by '{ALIASES[alias]}'")
                    else:
                        ALIASES[alias] = item_id
            logger.info(f"Loaded meme '{item_id}' with {len(meme.texts)} texts")
    except KeyError as e:
        logger.warning(f"Item '{item_id}'({i + 1}): key {e} not found")
    except TypeError as e:
        logger.warning(f"Item '{item_id}'({i + 1}): {e}")
    except NameError as e:
        logger.warning(f"Item '{item_id}'({i + 1}): {e}")


def load_text(current_text: int, raw_text: dict, text: Optional[Text] = None) -> Text:
    if text is None:
        text = Text(f"text {current_text}")
    text.font = utils.read_key_safe(raw_text, "font", text.font, types=[str])
    text.x_range = utils.read_key_safe(raw_text, "x_range", types=[float, int], is_list=True, is_list_size=2)
    text.y_range = utils.read_key_safe(raw_text, "y_range", types=[float, int], is_list=True, is_list_size=2)
    text.text_ref = utils.read_key_safe(raw_text, "text_ref", types=[int])
    text.style_ref = utils.read_key_safe(raw_text, "style_ref", types=[int])
    text.angle = utils.read_key_safe(raw_text, "angle", types=[float, int])
    text.font_size = utils.read_key_safe(raw_text, "font_size", text.font_size, types=[float, int])
    text.fill = utils.read_key_safe(raw_text, "fill", text.fill, types=[int], is_list=True, is_list_size=3)
    text.stroke_width = utils.read_key_safe(raw_text, "stroke_width", text.stroke_width, types=[float, int])
    text.stroke_fill = utils.read_key_safe(raw_text, "stroke_fill", text.stroke_fill, types=[int], is_list=True,
                                           is_list_size=3)
    if "position" in raw_text:
        if raw_text["position"] not in [p.name for p in Pos]:
            raise TypeError(f"'position' is not a valid position (ex: NW, E, SE, ...)")
        text.position = getattr(Pos, raw_text["position"])
    if "align" in raw_text:
        if raw_text["align"] not in ["left", "center", "right"]:
            raise TypeError(f"'align' is not 'left', 'center' or 'right'")
        text.align = raw_text["align"]
    return text


def get_meme(name: str) -> Optional[Meme]:
    name = name.lower().strip().replace(" ", "_")
    if name in ALIASES:
        return DATA[ALIASES[name]].clone()
    else:
        return None


def find_nearest(word: str) -> str:
    word = word.lower().strip().replace(" ", "_")
    return utils.find_nearest(word, list(ALIASES))
