import os
import logging
from os import path
from meme_otron import img_factory as imgf
from meme_otron import meme_db
from meme_otron import utils

logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.DEBUG)

imgf.load_fonts()
meme_db.load_memes()

dst_dir = utils.relative_path(__file__, "templates")

for f in os.listdir(dst_dir):
    if path.isfile(path.join(dst_dir, f)):
        os.unlink(path.join(dst_dir, f))

for meme_id in meme_db.DATA:
    meme = meme_db.get_meme(meme_id)
    if meme is not None:
        img = imgf.make(meme.template, meme.texts, debug=True)
        if img is not None:
            img.save(path.join(dst_dir, meme.template))
            print(meme_id)
