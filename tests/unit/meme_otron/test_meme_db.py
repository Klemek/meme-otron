from unittest import TestCase
from meme_otron import meme_db
from meme_otron.types import Pos, Text
from random import randint, randrange, choice


def get_rand_raw_text():
    return {
        "font": str(randint(0, pow(10, 10))),
        "x_range": [randrange(-10, 10), randrange(-10, 10)],
        "y_range": [randrange(-10, 10), randrange(-10, 10)],
        "text_ref": randint(-10, 10),
        "style_ref": randint(-10, 10),
        "angle": randrange(-10, 10),
        "font_size": randrange(-10, 10),
        "fill": [randint(-10, 10), randint(-10, 10), randint(-10, 10)],
        "stroke_width": randrange(-10, 10),
        "stroke_fill": [randint(-10, 10), randint(-10, 10), randint(-10, 10)],
        "align": choice(["left", "center", "right"]),
        "position": choice([k.name for k in Pos])
    }


class TestMemeDbLoadText(TestCase):
    object_keys = ["text_ref", "style_ref", "angle", "font_size", "fill",
                   "stroke_width", "stroke_fill", "position", "align"]

    def test_load_text_minimal(self):
        try:
            text = meme_db.load_text(0, {})
            self.assertEqual(f"text 0", text.text)
            for key in self.object_keys:
                self.assertIsNone(getattr(text, key))
        except TypeError as e:
            self.fail(e)

    def test_load_text_normal(self):
        try:
            raw_text = get_rand_raw_text()
            i = randint(-10, 10)
            text = meme_db.load_text(i, raw_text)
            self.assertEqual(f"text {i}", text.text)
            for key in self.object_keys:
                if key == "position":
                    self.assertEqual(getattr(Pos, raw_text[key]), text.position)
                else:
                    self.assertEqual(raw_text[key], getattr(text, key))
        except TypeError as e:
            self.fail(e)

    def test_load_text_base(self):
        try:
            base_text = meme_db.load_text(0, get_rand_raw_text())
            raw_text = {
                "font": str(randint(0, pow(10, 10)))
            }
            text = meme_db.load_text(0, raw_text, base_text)
            self.assertEqual(f"text 0", text.text)
            for key in self.object_keys:
                if key in ["font_size", "fill", "stroke_width", "stroke_fill", "position", "align"]:
                    self.assertEqual(getattr(base_text, key), getattr(text, key))
                elif key == "font":
                    self.assertEqual(raw_text["font"], getattr(text, key))
                else:
                    self.assertIsNone(getattr(text, key))
        except TypeError as e:
            self.fail(e)
