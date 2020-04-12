import logging

from .types import Text, Pos
from . import img_factory as imgf
from . import meme_db as db

logger = logging.getLogger("meme_otron")

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


def compute(*args, left_wmark_text=None, debug=False):
    """
    TODO

    :param (str) left_wmark_text:
    :param (bool) debug:
    :param (str) args:
    :rtype: PIL.Image.Image
    :return:
    """
    if len(args) < 1:
        return None
    meme_id = args[0]
    meme = db.get_meme(meme_id)
    if meme is None:
        logger.warning(f"Meme template '{meme_id}' not found")
        return None
    if len(args) > 1:
        for i in range(len(meme.texts)):
            if i < len(args) - 1:
                meme.texts[i].text = args[i + 1]
            else:
                meme.texts[i].text = ""
    meme.texts += [right_wmark]
    if left_wmark_text is not None:
        left_wmark.text = left_wmark_text
        meme.texts += [left_wmark]
    return imgf.make(meme.template, meme.texts, debug=debug)
