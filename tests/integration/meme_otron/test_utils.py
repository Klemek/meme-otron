from unittest import TestCase
from meme_otron import utils


class TestUtilsLang(TestCase):
    def test_find_nearest(self):
        self.assertEqual("test", utils.find_nearest("tost", ["test", "example", "what"]))
        self.assertIsNone(utils.find_nearest("unknown", ["test", "example", "what"], threshold=2))
        self.assertEqual("test", utils.find_nearest("unknown", ["test", "example", "what"], threshold=200))


class TestUtilsWeb(TestCase):
    def test_read_web_file(self):
        out, err = utils.read_web_file("http:invalid.url")
        self.assertIsNone(out)
        self.assertEqual('Invalid URL', err)
        out, err = utils.read_web_file("http://unknown.domain/")
        self.assertIsNone(out)
        self.assertEqual('Could not connect to server', err)
        out, err = utils.read_web_file("http://httpbin.org/status/418")
        self.assertIsNone(out)
        self.assertEqual('Could not connect: HTTP Error 418: I\'M A TEAPOT', err)
        out, err = utils.read_web_file("http://httpbin.org/bytes/1024", max_file_size=1000)
        self.assertIsNone(out)
        self.assertEqual('File too big', err)
        # out, err = utils.read_web_file("http://httpbin.org/delay/1", timeout=0.1)
        # self.assertIsNone(out)
        # self.assertEqual('Could not connect to server', err)
        out, err = utils.read_web_file("http://httpbin.org/base64/dGVzdA==")
        self.assertIsNone(err)
        self.assertEqual('test', out.decode("utf-8"))
