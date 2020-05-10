"""
Test the namedict
"""
import pytest

from gopher_render._namedict import namedict


def test_wrap():
    d = {}
    d = namedict(d)

    e = namedict({})


def test_access():
    d = namedict({})

    d["t"] = "present"
    assert d.t == "present"


def test_access_failure():
    d = namedict({})

    with pytest.raises(AttributeError):
        d.xxx
    with pytest.raises(KeyError):
        d["xxx"]


def test_set():
    d = namedict({})

    d.t = "set"
    assert d["t"] == "set"


def test_del():
    d = namedict({})

    d.x = 100
    del d.x
    with pytest.raises(AttributeError):
        assert d.x == 100
    with pytest.raises(KeyError):
        assert d["x"] == 100


def test_del_failure():
    d = namedict({})

    with pytest.raises(AttributeError):
        del d.xxx
    with pytest.raises(KeyError):
        del d["xxx"]
