import logging
import sys
import os

from . import img_factory as imgf
from . import meme_db as db
from . import meme_otron

if __name__ == "__main__":
    db.load_memes()
    imgf.load_fonts()
    if len(sys.argv) <= 1 or sys.argv[1].lower().strip() == "help":
        print("python -m meme_otron (meme_id) \"[text 1]\" \"[text 2]\" ... > file.jpg", file=sys.stderr)
    else:
        img = meme_otron.compute(*sys.argv[1:])
        with os.fdopen(os.dup(sys.stdout.fileno())) as output:
            img.save(output, format="jpeg")
