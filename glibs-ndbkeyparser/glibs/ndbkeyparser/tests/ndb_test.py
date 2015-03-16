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
