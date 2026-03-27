import os
import tempfile
import pytest
from toolkit.cache import FileCache


@pytest.fixture
def cache(tmp_path):
    return FileCache(str(tmp_path / "test_cache.json"))


def test_set_and_get(cache):
    cache.set("key", "value")
    assert cache.get("key") == "value"


def test_get_missing_returns_none(cache):
    assert cache.get("missing") is None


def test_delete_removes_key(cache):
    cache.set("key", "value")
    cache.delete("key")
    assert cache.get("key") is None


def test_clear_empties_cache(cache):
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None


def test_persists_between_instances(tmp_path):
    path = str(tmp_path / "persist.json")
    c1 = FileCache(path)
    c1.set("foo", "bar")
    c2 = FileCache(path)
    assert c2.get("foo") == "bar"
