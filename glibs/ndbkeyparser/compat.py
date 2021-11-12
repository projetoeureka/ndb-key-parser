import six
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def array_frombytes(array, bytes_):
    if six.PY3:
        array.frombytes(bytes_)
    else:
        array.fromstring(bytes_)


def array_tobytes(array):
    if six.PY3:
        return array.tobytes()
    else:
        return array.tostring()
