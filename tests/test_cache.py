"""Tests for the FileCache utility."""
import os
import time
import pytest
from toolkit.cache import FileCache


@pytest.fixture
def cache_file(tmp_path):
    return str(tmp_path / "test_cache.json")


@pytest.fixture
def cache(cache_file):
    c = FileCache(cache_file)
    c.clear()
    return c


class TestFileCache:
    def test_set_get_roundtrip(self, cache):
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_delete(self, cache):
        cache.set("key1", "value1")
        result = cache.delete("key1")
        assert result is True
        assert cache.get("key1") is None
    
    def test_clear(self, cache):
        cache.set("key1", "value1")
        cache.clear()
        assert cache.get("key1") is None
    
    def test_file_persistence(self, cache_file):
        cache1 = FileCache(cache_file)
        cache1.set("key1", "value1")
        cache2 = FileCache(cache_file)
        assert cache2.get("key1") == "value1"
    
    def test_ttl(self, tmp_path):
        cache_file = str(tmp_path / "ttl_cache.json")
        cache = FileCache(cache_file, ttl=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        time.sleep(1.5)
        assert cache.get("key1") is None
