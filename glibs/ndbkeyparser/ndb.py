import base64
import binascii
import six

from . import entity_pb
from . import ProtocolBuffer


class Key(object):
    def __init__(self, *args, **kwargs):
        if "urlsafe" in kwargs:
            serialized = _DecodeUrlSafe(kwargs["urlsafe"])
            ref = _ReferenceFromSerialized(serialized)
            el = ref.path().element_list()[0]
            self._pair = el.type().decode("utf-8"), int(el.id())
            self._app = ref.app().decode("utf-8")
        else:
            assert len(args) == 2, "exactly one pair given"
            assert "app" in kwargs, "app given explicitly"
            self._pair = args
            self._app = kwargs["app"]

    def id(self):
        return self._pair[1]

    def app(self):
        return self._app

    def kind(self):
        return self._pair[0]

    def urlsafe(self):
        ref = _ReferenceFromPairs([self._pair], app=self._app)
        return (
            base64.b64encode(ref.Encode())
            .rstrip(b"=")
            .replace(b"+", b"-")
            .replace(b"/", b"_")
            .decode("utf-8")
        )

    def __eq__(self, other):
        return isinstance(other, Key) and (self._pair, self._app) == (
            other._pair,
            other._app,
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        id = self.id() if type(self.id()) == int else "'{}'".format(self.id())
        return "Key('{kind}', {id}, app='{app}')".format(
            kind=self.kind(), id=id, app=self.app()
        )


class ConverterHelper(object):
    def __init__(self, ndb_app):
        self._ndb_app = ndb_app

    def ensure_key(self, value, kind=None):
        try:
            key = Key(urlsafe=value)
            if kind and kind != key.kind():
                raise ValueError("urlsafe is not the from the kind {}".format(kind))
            return value
        except (ProtocolBuffer.ProtocolBufferDecodeError, TypeError):
            if not kind:
                raise TypeError("expected kind when value is not urlsafe")
            return Key(kind, int(value), app=self._ndb_app).urlsafe()

    def ensure_id(self, value):
        try:
            int(value)
            return str(value)
        except ValueError:
            try:
                return str(Key(urlsafe=value).id())
            except (ProtocolBuffer.ProtocolBufferDecodeError, TypeError):
                raise ValueError


# Everything from here on is ndb's code


def _ReferenceFromPairs(pairs, app):
    """Construct a Reference from a list of pairs.

    If a Reference is passed in as the second argument, it is modified
    in place.    The app and namespace are set from the corresponding
    keyword arguments, with the customary defaults.
    """
    reference = entity_pb.Reference()
    path = reference.mutable_path()
    last = False
    for kind, idorname in pairs:
        if last:
            raise Exception("Incomplete Key entry must be last")

        elem = path.add_element()
        elem.set_type(kind)
        elem.set_id(idorname)

    # Always set the app id, since it is mandatory.
    reference.set_app(app)

    namespace = ""  # _DefaultNamespace()

    if namespace:
        reference.set_name_space(namespace)
    return reference


def _DecodeUrlSafe(urlsafe):
    """Decode a url-safe base64-encoded string.

    This returns the decoded string.
    """
    if not isinstance(urlsafe, six.string_types):
        raise TypeError("urlsafe must be a string; received %r" % urlsafe)
    if isinstance(urlsafe, six.text_type):
        urlsafe = urlsafe.encode("utf8")
    padding = b"=" * (-len(urlsafe) % 4)
    urlsafe += padding
    # This is 3-4x faster than urlsafe_b64decode()
    try:
        return base64.b64decode(urlsafe.replace(b"-", b"+").replace(b"_", b"/"))
    except binascii.Error:
        raise ProtocolBuffer.ProtocolBufferDecodeError


def _ReferenceFromSerialized(serialized):
    """Construct a Reference from a serialized Reference."""
    if not isinstance(serialized, six.binary_type):
        raise TypeError("serialized must be a bytestring; received %r" % serialized)
    elif isinstance(serialized, six.text_type):
        serialized = serialized.encode("utf8")
    return entity_pb.Reference(serialized)
