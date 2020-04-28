from unittest import TestCase
from meme_otron import types


class TestText(TestCase):
    def test_declare(self):
        txt1 = types.Text("txt1")
        self.assertEqual("txt1", txt1.text)
        self.assertIsNone(txt1.angle)
        self.assertEqual((0, 1), txt1.x_range)
        self.assertIsNone(txt1.fill)
        self.assertIsNone(txt1.stroke_width)

    def test_update(self):
        txt1 = types.Text("txt1")
        txt1.stroke_width = 6
        txt2 = types.Text("txt2")
        txt2.angle = 5
        txt2.x_range = (0.5, 0.8)
        txt2.fill = [0, 1, 0]
        txt2.stroke_width = 5
        txt1.update(txt2)
        self.assertEqual("txt1", txt1.text, "text keeped")
        self.assertIsNone(txt1.angle, "angle keeped")
        self.assertEqual((0, 1), txt1.x_range, "position keeped")
        self.assertEqual(txt2.fill, txt1.fill, "fill changed")
        self.assertNotEqual(txt2.stroke_width, txt1.stroke_width, "stroke_width keeped")
        self.assertEqual(6, txt1.stroke_width)

    def test_init(self):
        txt1 = types.Text("txt1")
        txt1.fill = [0, 1, 0]
        txt1.init()
        self.assertIsNotNone((0, 1, 0), txt1.fill)
        self.assertIsNotNone(txt1.stroke_width)


class TestMeme(TestCase):
    def test_declare(self):
        meme1 = types.Meme("meme1")
        self.assertEqual("meme1", meme1.id)
        self.assertIsNone(meme1.template)

    def test_clone(self):
        meme1 = types.Meme("meme1")
        meme1.template = "test1"
        meme2 = meme1.clone()
        meme1.template = "test2"
        self.assertEqual("meme1", meme2.id)
        self.assertEqual("test1", meme2.template)
