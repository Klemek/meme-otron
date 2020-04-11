from PIL import Image, ImageFont, ImageDraw
import os
import os.path as path
import logging

from . import utils

DEFAULT_FONT = "arial"
DEFAULT_FONT_SIZE = 0.05

FONT_DIR = utils.relative_path(__file__, "..", "fonts")
TEMPLATES_DIR = utils.relative_path(__file__, "..", "templates")

FONTS = {}

logger = logging.getLogger("img_factory")


def load_fonts():
    """
    TODO
    """
    for file in [f for f in os.listdir(FONT_DIR) if path.isfile(path.join(FONT_DIR, f))]:
        split = path.splitext(file)
        if split[-1] == ".ttf":
            try:
                FONTS[split[0]] = ImageFont.truetype(path.join(FONT_DIR, file))
                logger.info(f"Loaded font '{split[0]}'")
            except OSError:
                logger.error(f"Could not load font '{split[0]}'")


def make(template, texts, debug=False):
    """
    TODO

    :param (str) template:
    :param (list of Text) texts:
    :param (bool) debug:
    :rtype: PIL.Image.Image
    :return:
    """
    try:
        img = Image.open(path.join(TEMPLATES_DIR, template))
    except OSError as e:
        logger.error(f"Could not read template file '{template}': {e}")
        return None
    draw = ImageDraw.Draw(img)

    for text in texts:
        draw_text(draw, img.size, text, debug=debug)

    return img


def draw_text(draw, size, text, debug=False):
    """
    TODO

    :param (PIL.ImageDraw.ImageDraw) draw: source image canvas
    :param (int,int) size: source image size
    :param (Text) text:
    :param (bool) debug:
    """
    # TODO rotation
    # https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil
    if text.text is not None and len(text.text.strip()) > 0:
        if text.font is None:
            text.font = DEFAULT_FONT
        if text.font in FONTS:
            text.text, font = fit_text(size, text)
            draw.text(get_pos(size, text, font), text.text, fill=text.fill, align=text.align, font=font,
                      stroke_width=round(text.stroke_width * font.size), stroke_fill=text.stroke_fill)
            if debug:
                draw.rectangle([(text.x_range[0] * size[0], text.y_range[0] * size[1]),
                                (text.x_range[1] * size[0], text.y_range[1] * size[1])],
                               None,
                               (128, 128, 128))
        else:
            logger.warning(f"Invalid font '{text.font}'")


def fit_text(size, text):
    """
    :param (int,int) size: source image size
    :param (Text) text:
    :rtype: (str, PIL.ImageFont.FreeTypeFont)
    :return:
    """
    max_width = round(size[0] * (text.x_range[1] - text.x_range[0]))
    max_height = round(size[1] * (text.y_range[1] - text.y_range[0]))
    text_size = None
    if text.font_size is None:
        text.font_size = DEFAULT_FONT_SIZE
    font_size = round(text.font_size * min(size)) + 1
    font = FONTS[text.font]
    t = ""
    while (text_size is None or text_size[1] >= max_height) and font_size > 1:
        font_size -= 1
        font = font.font_variant(size=font_size)
        words = text.text.split(" ")
        t = ""
        for word in words:
            spacer = " "
            if len(t) == 0:
                spacer = ""
            text_size = font.getsize_multiline(t + spacer + word, stroke_width=text.stroke_width * font_size)
            if text_size[0] >= max_width:
                t += "\n" + word
            else:
                t += spacer + word
        text_size = font.getsize_multiline(t, stroke_width=text.stroke_width * font_size)
    return t, font


def get_pos(size, text, font):
    """
    TODO

    :param (int,int) size: source image size
    :param (Text) text:
    :param (PIL.ImageFont.FreeTypeFont) font:
    :rtype (int,int)
    :return:
    """
    min_x = round(text.x_range[0] * size[0])
    max_x = round(text.x_range[1] * size[0])
    min_y = round(text.y_range[0] * size[1])
    max_y = round(text.y_range[1] * size[1])
    pos_x = 0
    pos_y = 0
    text_size = font.getsize_multiline(text.text, stroke_width=text.stroke_width * font.size)

    if int(text.position.value) // 3 == 0:
        pos_y = min_y
    elif int(text.position.value) // 3 == 1:
        pos_y = round((min_y + max_y) / 2 - text_size[1] / 2)
    else:
        pos_y = max_y - text_size[1]

    if int(text.position.value) % 3 == 0:
        pos_x = min_x
    elif int(text.position.value) % 3 == 1:
        pos_x = round((min_x + max_x) / 2 - text_size[0] / 2)
    else:
        pos_x = max_x - text_size[0]

    return pos_x, pos_y
