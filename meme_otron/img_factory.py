from typing import List, Optional, Tuple
from PIL import Image, ImageFont, ImageDraw
import os
import os.path as path
import logging
import sys

from . import utils
from .types import Text

FONT_DIR = utils.relative_path(__file__, "..", "fonts")
TEMPLATES_DIR = utils.relative_path(__file__, "..", "templates")

FONTS = {}

TEXT_IMAGE_WIDTH = 800

logger = logging.getLogger("img_factory")


def load_fonts():
    for file in [f for f in os.listdir(FONT_DIR) if path.isfile(path.join(FONT_DIR, f))]:
        split = path.splitext(file)
        if split[-1] == ".ttf":
            try:
                FONTS[split[0]] = ImageFont.truetype(path.join(FONT_DIR, file))
                logger.info(f"Loaded font '{split[0]}'")
            except OSError:
                logger.error(f"Could not load font '{split[0]}'")


def compose_image(images: List[Image.Image]) -> Image.Image:
    if len(images) == 1:
        return images[0]
    width = min([img.size[0] for img in images])
    for i, img in enumerate(images):
        if img.size[0] != width:
            images[i] = img.resize((width, round(img.size[1] * width / img.size[0])), resample=Image.LANCZOS)
    height = sum([img.size[1] for img in images])
    output_image = Image.new('RGB', (width, height))
    current_height = 0
    for img in images:
        output_image.paste(img, (0, current_height))
        current_height += img.size[1]
    return output_image


def build_from_template(template: str, texts: List[Text], debug: bool = False) -> Optional[Image.Image]:
    try:
        img = Image.open(path.join(TEMPLATES_DIR, template)).convert(mode='RGBA')
    except OSError as e:
        logger.error(f"Could not read template file '{template}': {e}")
        return None
    img = apply_texts(img, texts, debug=debug)
    return img


def build_text_only(texts: List[Text], debug: bool = False) -> Image.Image:
    heights = []
    for text in texts:
        text.init()
        text.text, font = fit_text((TEXT_IMAGE_WIDTH, sys.maxsize), text)
        text_size = font.getsize_multiline(text.text, stroke_width=text.stroke_width * font.size)
        heights += [round(text_size[1] / (text.y_range[1] - text.y_range[0]))]
    max_height = sum(heights)
    for i, text in enumerate(texts):
        range_factor = heights[i] / max_height
        start = sum(heights[:i]) / max_height
        text.y_range = (start + text.y_range[0] * range_factor, start + text.y_range[1] * range_factor)
        pass
    txt_img = Image.new('RGBA', (TEXT_IMAGE_WIDTH, max_height), (255, 255, 255))
    return apply_texts(txt_img, texts, debug=debug)


def apply_texts(img: Image.Image, texts: List[Text], debug: bool = False) -> Image.Image:
    if img.mode != 'RGBA':
        img = img.convert(mode='RGBA')
    draw = ImageDraw.Draw(img)
    for text in texts:
        draw_text(draw, img, text, debug=debug)
    return img.convert(mode='RGB')


def draw_text(draw: ImageDraw.ImageDraw, img: Image.Image, text: Text, debug: bool = False):
    if text.text is not None and len(text.text.strip()) > 0:
        text.init()  # load default values
        if text.font in FONTS:
            text.text, font = fit_text(img.size, text)
            if text.angle == 0:
                draw.text(get_text_pos(img.size, text, font), text.text, fill=text.fill, align=text.align, font=font,
                          stroke_width=round(text.stroke_width * font.size), stroke_fill=text.stroke_fill)
                if debug:
                    draw.rectangle([(text.x_range[0] * img.size[0], text.y_range[0] * img.size[1]),
                                    (text.x_range[1] * img.size[0], text.y_range[1] * img.size[1])],
                                   None, (128, 128, 128))
            else:
                width = round((text.x_range[1] - text.x_range[0]) * img.size[0])
                height = round((text.y_range[1] - text.y_range[0]) * img.size[1])
                center_x = (text.x_range[0] + text.x_range[1]) * img.size[0] / 2
                center_y = (text.y_range[0] + text.y_range[1]) * img.size[1] / 2
                txt_img = Image.new('RGBA', (width, height))
                txt_draw = ImageDraw.Draw(txt_img)
                txt_draw.text(get_text_pos(img.size, text, font, relative=True), text.text, fill=text.fill,
                              align=text.align, font=font, stroke_width=round(text.stroke_width * font.size),
                              stroke_fill=text.stroke_fill)
                if debug:
                    txt_draw.rectangle([(0, 0), (width - 1, height - 1)],
                                       None, (128, 128, 128))
                txt_img = txt_img.rotate(text.angle, expand=1, resample=Image.BILINEAR)
                img.paste(txt_img,
                          (round(center_x - txt_img.size[0] / 2), round(center_y - txt_img.size[1] / 2)),
                          txt_img)
        else:
            logger.warning(f"Invalid font '{text.font}'")


def fit_text(size: Tuple[int, int], text: Text) -> Tuple[str, ImageFont.FreeTypeFont]:
    max_width = round(size[0] * (text.x_range[1] - text.x_range[0]))
    max_height = round(size[1] * (text.y_range[1] - text.y_range[0]))
    text_size = None
    font_size = round(text.font_size * size[0]) + 1
    font = FONTS[text.font]
    text_content = ""
    while (text_size is None or text_size[0] > max_width or text_size[1] > max_height) and font_size > 1:
        font_size -= 1
        font = font.font_variant(size=font_size)
        n_lines = 0
        while n_lines == 0 or (text_content is not None and text_size[0] >= max_width):
            n_lines += 1
            text_content = utils.justify_text(text.text, n_lines)
            if text_content is not None:
                text_size = font.getsize_multiline(text_content, stroke_width=text.stroke_width * font_size)
        if text_content is None:
            # max break attained
            text_size = None  # retry
    return text_content, font


def get_text_pos(size: Tuple[int, int], text: Text,
                 font: ImageFont.FreeTypeFont, relative: bool = False) -> Tuple[int, int]:
    min_x = round(text.x_range[0] * size[0])
    max_x = round(text.x_range[1] * size[0])
    min_y = round(text.y_range[0] * size[1])
    max_y = round(text.y_range[1] * size[1])
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
    if relative:
        return pos_x - min_x, pos_y - min_y
    else:
        return pos_x, pos_y
