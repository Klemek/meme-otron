import os
import logging
from os import path
from meme_otron import img_factory as imgf
from meme_otron import meme_db
from meme_otron import utils

logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.WARNING)

imgf.load_fonts()
meme_db.load_memes()

dst_dir = utils.relative_path(__file__, "templates")
templates_dir = utils.relative_path(__file__, "..", "templates")
doc_file = utils.relative_path(__file__, "README.md")

COLUMNS = 3

if path.exists(dst_dir):
    for f in os.listdir(dst_dir):
        if path.isfile(path.join(dst_dir, f)):
            os.unlink(path.join(dst_dir, f))
else:
    os.mkdir(dst_dir)

ids = sorted(meme_db.DATA.keys())

doc_content = "|" * (COLUMNS + 1) \
              + "\n|" + ":---:|" * COLUMNS

info_line = None
img_line = None

i = None
for i, meme_id in enumerate(ids):
    meme = meme_db.get_meme(meme_id)
    if meme is not None:
        img = imgf.make(meme.template, meme.texts, debug=True)
        if img is not None:
            img.save(path.join(dst_dir, meme.template))
            if i % COLUMNS == 0:
                if info_line is not None and img_line is not None:
                    doc_content += info_line + img_line
                info_line = "\n|"
                img_line = "\n|"
            info_line += f"**{meme_id}**"
            if len(meme.aliases) > 0:
                info_line += f"<br>alt: {', '.join(meme.aliases)}"
            if meme.info is not None:
                info_line += f"<br><a href='{meme.info}' target='_blank'>more info</a>"
            info_line += "|"
            img_line += f"<a href='./templates/{meme.template}' target='_blank'>" \
                        f"<img src='./templates/{meme.template}' style='max-height:25vh'/>" \
                        f"</a>|"

doc_content += "|" * (COLUMNS - (i % COLUMNS))

with open(doc_file, mode='r') as f:
    content = "".join(f.readlines())

i0 = content.index("<!--START-->")
i1 = content.index("<!--END-->") + len("<!--END-->")

with open(doc_file, mode='w') as f:
    f.write(content[:i0])
    f.write("<!--START-->\n")
    f.write(doc_content)
    f.write("\n<!--END-->")
    f.write(content[i1:])
