import unittest
from glibs.ndbkeyparser import ndb


class KeyTest(unittest.TestCase):

    def test_from_urlsafe_to_key(self):
        urlsafe = "agpzfmdlZWtpZWlkchkLEgxPcmdhbml6YXRpb24YgICA9Oe81AsM"
        key = ndb.Key(urlsafe=urlsafe)

        self.assertEqual(6563974870990848, key.id())
        self.assertEqual("Organization", key.kind())
        self.assertEqual("s~geekieid", key.app())
        self.assertEqual(key, ndb.Key("Organization", 6563974870990848, app="s~geekieid"))

    def test_from_key_to_urlsafe(self):
        urlsafe = "agpzfmdlZWtpZWlkchkLEgxPcmdhbml6YXRpb24YgICA9Oe81AsM"

        key = ndb.Key("Organization", 6563974870990848, app="s~geekieid")
        self.assertEqual(urlsafe, key.urlsafe())
        self.assertEqual(key, ndb.Key(urlsafe=urlsafe))


class ConverterHelperTest(unittest.TestCase):

    def setUp(self):
        super(ConverterHelperTest, self).setUp()
        self._ndb_app = "ndb_app"
        self.converter = ndb.ConverterHelper(self._ndb_app)

    def test_ensure_key_returns_the_same_key_if_no_kind_was_provided(self):
        value = ndb.Key("Model", 1, app=self._ndb_app).urlsafe()
        self.assertEqual(value, self.converter.ensure_key(value, kind=None))

    def test_ensure_key_returns_the_same_key_if_kind_is_the_same(self):
        value=ndb.Key("Model", 1, app=self._ndb_app).urlsafe()
        self.assertEqual(value, self.converter.ensure_key(value, kind="Model"))

    def test_ensure_key_returns_correct_key_id_string_id_and_kind_provided(self):
        value="1"
        expected_result=ndb.Key("Model", 1, app=self._ndb_app).urlsafe()
        self.assertEqual(expected_result, self.converter.ensure_key(value, kind="Model"))

    def test_ensure_key_returns_correct_key_id_numeric_id_and_kind_provided(self):
        value=1
        expected_result=ndb.Key("Model", 1, app=self._ndb_app).urlsafe()
        self.assertEqual(expected_result, self.converter.ensure_key(value, kind="Model"))

    def test_ensure_key_raises_if_kind_provided_but_different_from_the_urlsafe_provided(self):
        value=ndb.Key("Model", 1, app=self._ndb_app).urlsafe()
        with self.assertRaises(ValueError):
            self.converter.ensure_key(value, kind="Not-Model")

    def test_ensure_key_raises_if_value_is_not_urlsafe_and_kind_not_provided(self):
        with self.assertRaises(TypeError):
            self.converter.ensure_key(value="1", kind=None)

    def test_ensure_key_raises_if_value_is_not_urlsafe_and_is_not_an_int(self):
        with self.assertRaises(ValueError):
            self.converter.ensure_key(value="some_value", kind="Model")

    def test_ensure_id_returns_stringfyied_value_of_numeric_id_provided(self):
        self.assertEqual("1", self.converter.ensure_id(1))

    def test_ensure_id_returns_same_string_if_is_int(self):
        self.assertEqual("1", self.converter.ensure_id("1"))

    def test_ensure_id_returns_stringfyied_id_of_urlsafe(self):
        value=ndb.Key("Model", 1, app=self._ndb_app).urlsafe()
        self.assertEqual("1", self.converter.ensure_id(value))

    def test_ensure_id_raises_if_not_int_nor_urlsafe(self):
        with self.assertRaises(ValueError):
            self.converter.ensure_id("blah")
