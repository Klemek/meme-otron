import os
import stat
import time
import datetime
import logging
from os import path
from meme_otron import img_factory
from meme_otron import meme_db
from meme_otron import utils

logging.basicConfig(format="%(message)s", level=logging.WARNING)

img_factory.load_fonts()

db_file = utils.relative_path(__file__, "..", meme_db.DATA_FILE)
templates_dir = utils.relative_path(__file__, "..", "templates")
dst_dir = utils.relative_path(__file__, "tmp")

if not path.exists(dst_dir):
    os.mkdir(dst_dir)

last = None

while True:
    while os.stat(db_file)[stat.ST_MTIME] == last:
        time.sleep(0.1)
    last = os.stat(db_file)[stat.ST_MTIME]
    time.sleep(0.1)
    meme_db.load_memes(purge=True)
    count = 0
    for meme_id in meme_db.LIST:
        meme = meme_db.get_meme(meme_id)
        img = img_factory.build_image(meme.template, meme.texts, debug=True)
        if img is not None:
            img.save(path.join(dst_dir, meme.template))
            count += 1
    print(f"{datetime.datetime.now():%H:%M:%S} / {count} registered templates / {len(os.listdir(templates_dir))} files")
