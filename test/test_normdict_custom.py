import re
import pytest
from   headerparser import NormalizedDict

def normdash(s): return re.sub(r'[-_\s]+', '-', s.lower())

def test_empty():
    nd = NormalizedDict(normalizer=normdash)
    assert dict(nd) == {}
    assert nd.body is None
    assert len(nd) == 0
    assert not bool(nd)

def test_one():
    nd = NormalizedDict({"A Key": "bar"}, normalizer=normdash)
    assert dict(nd) == {"A Key": "bar"}
    assert nd.body is None
    assert len(nd) == 1
    assert bool(nd)

def test_get_cases():
    nd = NormalizedDict({"A Key": "bar"}, normalizer=normdash)
    assert nd["A Key"] == "bar"
    assert nd["A Key"] == nd["a_key"] == nd["A-KEY"] == nd["A - key"]

def test_set():
    nd = NormalizedDict(normalizer=normdash)
    assert dict(nd) == {}
    nd["A Key"] = "bar"
    assert dict(nd) == {"A Key": "bar"}
    assert nd["A Key"] == "bar"
    assert nd["A Key"] == nd["a_key"] == nd["A-KEY"] == nd["A - key"]
    nd["A-Key"] = "quux"
    assert dict(nd) == {"A-Key": "quux"}
    assert nd["A Key"] == "quux"
    assert nd["A Key"] == nd["a_key"] == nd["A-KEY"] == nd["A - key"]

def test_del():
    nd = NormalizedDict(
        {"A Key": "bar", "Another-Key": "FOO"},
        normalizer=normdash,
    )
    del nd["A Key"]
    assert dict(nd) == {"Another-Key": "FOO"}
    del nd["ANOTHER_KEY"]
    assert dict(nd) == {}

def test_del_nexists():
    nd = NormalizedDict(
        {"A Key": "bar", "Another-Key": "FOO"},
        normalizer=normdash,
    )
    with pytest.raises(KeyError):
        del nd["AKey"]

def test_eq_empty():
    nd = NormalizedDict(normalizer=normdash)
    nd2 = NormalizedDict(normalizer=normdash)
    assert nd == nd2

def test_eq_cases():
    nd = NormalizedDict({"A Key": "bar"}, normalizer=normdash)
    nd2 = NormalizedDict({"a_key": "bar"}, normalizer=normdash)
    assert nd == nd2

def test_neq():
    assert NormalizedDict({"A Key": "A Value"}, normalizer=normdash) \
        != NormalizedDict({"A Key": "a_value"}, normalizer=normdash)

def test_normalized():
    nd = NormalizedDict({"A Key": "BAR"}, normalizer=normdash)
    nd2 = nd.normalized()
    assert isinstance(nd2, NormalizedDict)
    assert dict(nd2) == {"a-key": "BAR"}
    assert nd.body is None
    assert nd == nd2

def test_normalized_with_body():
    nd = NormalizedDict({"A Key": "BAR"}, body='Foo Baz', normalizer=normdash)
    nd2 = nd.normalized()
    assert isinstance(nd2, NormalizedDict)
    assert dict(nd2) == {"a-key": "BAR"}
    assert nd.body == 'Foo Baz'
    assert nd == nd2

def test_normalized_dict():
    nd = NormalizedDict({"A Key": "BAR"}, normalizer=normdash)
    nd2 = nd.normalized_dict()
    assert isinstance(nd2, dict)
    assert nd2 == {"a-key": "BAR"}

def test_eq_dict():
    nd = NormalizedDict({"A Key": "BAR"}, normalizer=normdash)
    assert nd == {"A Key": "BAR"}
    assert {"A Key": "BAR"} == nd
    assert nd == {"A_KEY": "BAR"}
    assert {"A_KEY": "BAR"} == nd
    assert nd == {"a-key": "BAR"}
    assert {"a-key": "BAR"} == nd
    assert nd != {"A Key": "bar"}
    assert {"A Key": "bar"} != nd

def test_body_neq_dict():
    nd = NormalizedDict({"A Key": "BAR"}, body='', normalizer=normdash)
    assert nd != {"A Key": "BAR"}
    assert {"A Key": "BAR"} != nd

def test_eq_body():
    nd = NormalizedDict({"A Key": "bar"}, body='', normalizer=normdash)
    nd2 = NormalizedDict({"a_KEY": "bar"}, body='', normalizer=normdash)
    assert nd == nd2

def test_neq_body():
    nd = NormalizedDict({"A Key": "bar"}, body='yes', normalizer=normdash)
    nd2 = NormalizedDict({"a_KEY": "bar"}, body='no', normalizer=normdash)
    assert nd != nd2

def test_init_list():
    nd = NormalizedDict(
        [("A Key", "bar"), ("Another-Key", "baz"), ("A_KEY", "quux")],
        normalizer=normdash,
    )
    assert dict(nd) == {"A_KEY": "quux", "Another-Key": "baz"}
