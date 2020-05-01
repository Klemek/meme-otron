import os
import logging
from typing import List
import PIL
from os import path
from meme_otron import img_factory
from meme_otron import meme_db
from meme_otron import utils
from meme_otron import meme_otron

logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(module)s] %(message)s", level=logging.WARNING)

img_factory.load_fonts()
meme_db.load_memes()

templates_dir = utils.relative_path(__file__, "templates")
preview_dir = utils.relative_path(__file__, "preview")
doc_template_file = utils.relative_path(__file__, "README-template.md")
doc_file = utils.relative_path(__file__, "README.md")

COLUMNS = 3
IMG_HEIGHT = 400


def main():
    make_empty(templates_dir)
    make_empty(preview_dir)

    with open(doc_template_file, mode='r') as f:
        content = "".join(f.readlines())

    full_list = sorted(meme_db.LIST)
    template_list = [meme_id for meme_id in full_list if len(meme_db.get_meme(meme_id).texts) > 0]
    reaction_list = [meme_id for meme_id in full_list if meme_id not in template_list]

    content = produce_template_list(content, "LIST1", template_list)
    content = produce_template_list(content, "LIST2", reaction_list)

    content = produce_example(content, "EXAMPLE1", "example1.jpg", "",
                              "brain3",
                              "Making memes using an image editor",
                              "Making memes using a Python script",
                              "Making memes using a Discord bot")

    content = produce_example(content, "EXAMPLE2", "example2.jpg",
                              "The 5th text is not set and the 3rd is explicitly set to empty",
                              "see_that_guy",
                              "See that guy over there?",
                              "He uses an image editor to make memes",
                              "",
                              "meme-otron dev")

    content = produce_example(content, "EXAMPLE3", "example3.jpg",
                              "Note how texts make paragraphs",
                              "text",
                              "*Meme has a 'made with meme-otron' watermark*",
                              "reddit: ...",
                              "9gag: ...",
                              "meme-otron dev:",
                              "-",
                              "culture",
                              "meme otron")

    # TODO example 4 : complex composition

    with open(doc_file, mode='w') as f:
        f.write(content)


def make_empty(target_dir: str):
    if path.exists(target_dir):
        for file in os.listdir(target_dir):
            if path.isfile(path.join(target_dir, file)):
                os.unlink(path.join(target_dir, file))
    else:
        os.mkdir(target_dir)


def produce_template_list(content: str, tag: str, id_list: List[str]):
    if len(id_list) == 0:
        return content
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
    return inject_content(doc_content, content, tag)


def produce_example(content: str, tag: str, file_name: str, note: str, *args: str):
    doc_content = f"> {note}\n\n" \
                  "```\n" + \
                  " \n".join(['"' + a + '"' if ' ' in a or len(a) == 0 else a for a in args]) + \
                  "\n```\n\n" \
                  f"![]({file_name})"
    img, err = meme_otron.compute(*args)
    if img is not None:
        img.save(utils.relative_path(__file__, file_name))
    return inject_content(doc_content, content, tag)


def inject_content(new_content, content, tag):
    start_str = f"<!--{tag}-START-->"
    end_str = f"<!--{tag}-END-->"
    i0 = content.index(start_str)
    i1 = content.index(end_str) + len(end_str)
    return content[:i0] + start_str + "\n" + new_content + "\n" + end_str + content[i1:]


if __name__ == '__main__':
    main()
