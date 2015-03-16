import base64
from . import entity_pb


class Key(object):

    def __init__(self, *args, **kwargs):
        if "urlsafe" in kwargs:
            serialized = _DecodeUrlSafe(kwargs["urlsafe"])
            ref = _ReferenceFromSerialized(serialized)
            el = ref.path().element_list()[0]
            self._pair = el.type(), int(el.id())
            self._app = ref.app()
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
        return base64.b64encode(ref.Encode()).rstrip('=').replace('+', '-').replace('/', '_')

    def __eq__(self, other):
        return isinstance(other, Key) and (self._pair, self._app) == (other._pair, other._app)

    def __ne__(self, other):
        return not self.__eq__(other)


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
            raise datastore_errors.BadArgumentError(
                'Incomplete Key entry must be last'
            )

        elem = path.add_element()
        elem.set_type(kind)
        elem.set_id(idorname)

    # Always set the app id, since it is mandatory.
    reference.set_app(app)

    namespace = ''  # _DefaultNamespace()

    if namespace:
        reference.set_name_space(namespace)
    return reference


def _DecodeUrlSafe(urlsafe):
    """Decode a url-safe base64-encoded string.

    This returns the decoded string.
    """
    if not isinstance(urlsafe, basestring):
        raise TypeError('urlsafe must be a string; received %r' % urlsafe)
    if isinstance(urlsafe, unicode):
        urlsafe = urlsafe.encode('utf8')
    mod = len(urlsafe) % 4
    if mod:
        urlsafe += '=' * (4 - mod)
    # This is 3-4x faster than urlsafe_b64decode()
    return base64.b64decode(urlsafe.replace('-', '+').replace('_', '/'))


def _ReferenceFromSerialized(serialized):
    """Construct a Reference from a serialized Reference."""
    if not isinstance(serialized, basestring):
        raise TypeError('serialized must be a string; received %r' % serialized)
    elif isinstance(serialized, unicode):
        serialized = serialized.encode('utf8')
    return entity_pb.Reference(serialized)
