from unittest import TestCase
from meme_otron import utils


class TestUtilsPath(TestCase):
    def test_relative_path(self):
        self.assertEqual(__file__, utils.relative_path(__file__, ".", "test_utils.py"))


class TestUtilsType(TestCase):
    def test_is_list_of(self):
        self.assertFalse(utils.is_list_of(None, [str]))
        self.assertFalse(utils.is_list_of("", [int]))
        self.assertFalse(utils.is_list_of(None, [float]))
        self.assertTrue(utils.is_list_of([], [str]))
        self.assertTrue(utils.is_list_of(["test", "test2"], [str]))
        self.assertTrue(utils.is_list_of(["test", 2.0], [str, float]))
        self.assertFalse(utils.is_list_of(["test", 2.0], [int]))
        self.assertTrue(utils.is_list_of(["test", "test2"], [str], length=2))
        self.assertFalse(utils.is_list_of(["test", "test2", "test3"], [str], length=2))

    def test_check_type(self):
        try:
            utils.check_type("", [str])
        except TypeError as e:
            self.fail(str(e))
        try:
            utils.check_type(0, [str, float])
            self.fail("no exception")
        except TypeError as e:
            self.assertEqual("not a str", str(e))
        try:
            utils.check_type("", [str], is_list=True)
            self.fail("no exception")
        except TypeError as e:
            self.assertEqual("not a list of str", str(e))
        try:
            utils.check_type([1, 0.2, 2], [float, int], is_list=True)
            utils.check_type([1, 0.2, 2], [float, int], is_list=True, is_list_size=3)
        except TypeError as e:
            self.fail(str(e))
        try:
            utils.check_type([1, 0.2, 2, 2.5], [float, str], is_list=True)
            self.fail("no exception")
        except TypeError as e:
            self.assertEqual("not a list of float", str(e))
        try:
            utils.check_type([1, 0.2, 2, 2.5], [float, int], is_list=True, is_list_size=3)
            self.fail("no exception")
        except TypeError as e:
            self.assertEqual("not a list of 3 float", str(e))


class TestUtilsDict(TestCase):
    def test_read_key(self):
        d = {
            "test1": 5,
            "test2": [1, 3, ""]
        }
        self.assertEqual(5, utils.read_key(d, "test1"))
        self.assertEqual([1, 3, ""], utils.read_key(d, "test2"))
        self.assertEqual("default", utils.read_key(d, "test3", "default"))
        try:
            utils.read_key(d, "test3")
            self.fail("no exception")
        except KeyError as e:
            self.assertEqual("'test3'", str(e))
        try:
            utils.read_key(d, "test1", types=[str])
            self.fail("no exception")
        except TypeError as e:
            self.assertEqual("'test1' is not a str", str(e))
        try:
            utils.read_key(d, "test2", types=[str, int], is_list=True, is_list_size=2)
            self.fail("no exception")
        except TypeError as e:
            self.assertEqual("'test2' is not a list of 2 str", str(e))

    def test_read_key_safe(self):
        d = {
            "test1": 5,
            "test2": [1, 3, ""]
        }
        self.assertEqual(5, utils.read_key_safe(d, "test1"))
        self.assertEqual([1, 3, ""], utils.read_key_safe(d, "test2"))
        self.assertEqual("default", utils.read_key_safe(d, "test3", "default"))
        self.assertIsNone(utils.read_key_safe(d, "test3"))


class TestUtilsLang(TestCase):
    def test_find_nearest(self):
        self.assertEqual("test", utils.find_nearest("tost", ["test", "example", "what"]))
        self.assertIsNone(utils.find_nearest("unknown", ["test", "example", "what"], threshold=2))
        self.assertEqual("test", utils.find_nearest("unknown", ["test", "example", "what"], threshold=200))

    def test_sanitize_input(self):
        self.assertEqual("", utils.sanitize_input(""))
        self.assertEqual("a b_c", utils.sanitize_input("  A+=¤$ bé_cè:*  "))


class TestUtilsArgs(TestCase):
    def test_parse_arguments(self):
        self.assertEqual([], utils.parse_arguments(""))
        self.assertEqual(["test"], utils.parse_arguments("test"))
        self.assertEqual(["test1", "test2"], utils.parse_arguments("test1 test2"))
        self.assertEqual(["test1", "test 2", "test 3"], utils.parse_arguments("test1 'test 2' \"test 3\""))
        self.assertEqual(["test1", "", ""], utils.parse_arguments("test1 '' \"\""))

    def test_read_argument(self):
        self.assertFalse(utils.read_argument(["test", "-o", "test"], "--output"))
        self.assertTrue(utils.read_argument(["test", "-O", "test"], "--output", "-o"))
        self.assertIsNone(utils.read_argument(["test", "-o"], "-o", valued=True))
        self.assertEqual("test1", utils.read_argument(["test", "-o", "test1", "-o", "test2"], "-o", valued=True))
        args = ["test", "-o", "test1"]
        self.assertTrue(utils.read_argument(args, "-o", delete=True))
        self.assertEqual(["test", "test1"], args)
        args = ["test", "-o", "test1"]
        self.assertEqual("test1", utils.read_argument(args, "-o", valued=True, delete=True))
        self.assertEqual(["test"], args)
        args = ["test", "-o"]
        self.assertIsNone(utils.read_argument(args, "-o", valued=True, delete=True))
        self.assertEqual(["test"], args)

    def test_split_arguments(self):
        self.assertEqual([["test", "-o", "test"]], utils.split_arguments(["test", "-o", "test"], "-"))
        self.assertEqual([["test1"], ["test2"]], utils.split_arguments(["test1", "-", "test2"], "-"))
        self.assertEqual([["test1"], ["test2"]], utils.split_arguments(["-", "test1", "-", "-", "test2", "-"], "-"))
        self.assertEqual([], utils.split_arguments([], "-"))


class TestUtilsString(TestCase):
    def test_safe_index(self):
        self.assertEqual(0, utils.safe_index("a", "a"))
        self.assertEqual(0, utils.safe_index([0], 0))
        self.assertEqual(2, utils.safe_index("cbaa", "a"))
        self.assertEqual(3, utils.safe_index("cbaa", "a", 3))
        self.assertEqual(1, utils.safe_index(["a", 0, 0], 0))
        self.assertEqual(2, utils.safe_index(["a", 0, 0], 0, 2))
        self.assertIsNone(utils.safe_index("a", "b"))
        self.assertIsNone(utils.safe_index("a", "a", 2))
        self.assertIsNone(utils.safe_index(["a", 0, 0], 0, 3))

    def test_find_all(self):
        self.assertEqual([], utils.find_all("abc", "n"))
        self.assertEqual([0], utils.find_all("abc", "a"))
        self.assertEqual([0, 2], utils.find_all("aba", "a"))

    def test_replace_at(self):
        self.assertEqual("abcd", utils.replace_at("abc", "d", [3], 0))
        self.assertEqual("abd", utils.replace_at("abc", "d", [2], 1))
        self.assertEqual("ddd", utils.replace_at("abc", "d", [0, 1, 2], 1))
        self.assertEqual("a nice_plac_", utils.replace_at("a nice place", "_", [6, 11], 1))


class TestUtilsFormat(TestCase):
    def test_break_text(self):
        self.assertIsNone(utils.justify_text("abcd", 2))
        self.assertIsNone(utils.justify_text("abcd efgh", 3))
        self.assertEqual("abcd", utils.justify_text("abcd", 1))
        self.assertEqual("abcd\nefgh", utils.justify_text("abcd efgh", 2))
        self.assertEqual("ab cd\nef gh", utils.justify_text("ab cd ef gh", 2))
        self.assertEqual("ab\ncd ef\ngh", utils.justify_text("ab cd ef gh", 3))

    def test_place_line_breaks(self):
        self.assertEqual([5, 9, 15], utils.place_line_breaks([5.2, 14.3, 15.2], [3, 5, 9, 15, 18]))
        self.assertEqual([5, 9, 15, 18], utils.place_line_breaks([5.2, 14.3, 14.5, 15.2], [3, 5, 9, 15, 18]))
        self.assertEqual([5, 9, 15, 18], utils.place_line_breaks([5.2, 14.3, 14.5, 15.2], [3, 5, 9, 15, 18, 20]))


class TestUtilsWeb(TestCase):
    def test_validate_url(self):
        self.assertTrue(utils.validate_url("https://google.com/page#anchor?key=value&query"))
        self.assertFalse(utils.validate_url("https:google.com/page#anchor?key=value&query"))
        self.assertFalse(utils.validate_url(""))
        self.assertFalse(utils.validate_url("google.com"))

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
