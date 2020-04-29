from typing import Optional, Tuple, List
import re
from PIL import Image

from .types import Text, Pos
from . import img_factory
from . import meme_db
from . import utils

right_wmark = Text("Made with meme-otron")
right_wmark.position = Pos.SE
right_wmark.fill = (128, 128, 128, 128)
right_wmark.font_size = 0.02
right_wmark.x_range = [0.005, 0.995]
right_wmark.y_range = [0.005, 0.995]

left_wmark = Text()
left_wmark.position = Pos.SW
left_wmark.fill = (128, 128, 128, 128)
left_wmark.font_size = 0.02
left_wmark.x_range = [0.005, 0.995]
left_wmark.y_range = [0.005, 0.995]

simple_text = Text()
simple_text.align = "left"
simple_text.position = Pos.W
simple_text.font_size = 0.04
simple_text.x_range = [0.01, 0.99]
simple_text.y_range = [0.2, 0.8]


def compute(*args: str, left_wmark_text: Optional[str] = None,
            debug: bool = False) -> Tuple[Optional[Image.Image], List[str]]:
    if len(args) < 1:
        return None, ['Not enough arguments']

    parts = utils.split_arguments(args, "-")
    images = []
    errors = []
    for part in parts:
        img, err = compute_part(*part, debug=debug)
        if img is not None:
            images += [img]
        else:
            errors += [err]

    if len(images) == 0:
        return None, errors

    output_image = img_factory.compose_image(images)

    watermarks = [right_wmark]
    if left_wmark_text is not None:
        watermarks += [left_wmark.variant(left_wmark_text)]
    output_image = img_factory.apply_texts(output_image, watermarks, debug=debug)

    return output_image, errors


def compute_part(*args: str, debug: bool = False) -> Tuple[Optional[Image.Image], Optional[str]]:
    meme_id = utils.sanitize_input(args[0])

    if meme_id == "text":
        if len(args) < 2:
            return None, 'Text: not enough arguments'
        texts = [simple_text.variant(arg) for arg in args[1:]]
        return img_factory.build_text_only(texts, debug=debug), None
    elif meme_id == "image":
        return None, 'Image: not yet implemented'
    else:
        meme = meme_db.get_meme(meme_id)
        if meme is None:
            error = f"Template: '{meme_id}' not found."
            proposal = meme_db.find_nearest(meme_id)
            if proposal is not None:
                error += f" Did you mean '{proposal}'?"
            return None, error
        if len(args) > 1:
            c = 0
            for i in range(len(meme.texts)):
                if meme.texts[i].text_ref is None:
                    if c < len(args) - 1:
                        meme.texts[i].text = args[c + 1].replace("\\n", "\n")
                    else:
                        meme.texts[i].text = ""
                    c += 1
                else:
                    meme.texts[i].text = meme.texts[meme.texts[i].text_ref].text
        return img_factory.build_from_template(meme.template, meme.texts, debug=debug), None
