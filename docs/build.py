import os
import logging
import PIL
from os import path
from meme_otron import img_factory
from meme_otron import meme_db
from meme_otron import utils

logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.WARNING)

img_factory.load_fonts()
meme_db.load_memes()

templates_dir = utils.relative_path(__file__, "templates")
preview_dir = utils.relative_path(__file__, "preview")
doc_file = utils.relative_path(__file__, "README.md")

COLUMNS = 3
IMG_HEIGHT = 400


def make_empty(target_dir: str):
    if path.exists(target_dir):
        for file in os.listdir(target_dir):
            if path.isfile(path.join(target_dir, file)):
                os.unlink(path.join(target_dir, file))
    else:
        os.mkdir(target_dir)


make_empty(templates_dir)
make_empty(preview_dir)

id_list = sorted(meme_db.LIST)

doc_content = "|" * (COLUMNS + 1) \
              + "\n|" + ":---:|" * COLUMNS

info_line = None
img_line = None

i = None
for i, meme_id in enumerate(id_list):
    meme = meme_db.get_meme(meme_id)
    img = img_factory.build_from_template(meme.template, meme.texts, debug=True)
    if img is not None:
        img.save(path.join(templates_dir, meme.template))
        size = (round(img.size[0] * IMG_HEIGHT / img.size[1]), IMG_HEIGHT)
        img2 = img.resize(size, resample=PIL.Image.LANCZOS)
        img2.save(path.join(preview_dir, meme.template))
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
        img_line += f"" \
                    f"<a href='./templates/{meme.template}' target='_blank'>" \
                    f"<img alt='enlarge' src='./preview/{meme.template}'/>" \
                    f"</a>|"
        print(i, meme_id)

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
