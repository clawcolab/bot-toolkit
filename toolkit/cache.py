"""
JSON File Cache Utility
A simple key-value cache that persists to a JSON file.
"""
import json
import os
from pathlib import Path
from typing import Any, Optional
import time


class FileCache:
    """A file-based cache that stores key-value pairs in JSON."""
    
    def __init__(self, cache_file: str = ".cache.json", ttl: Optional[int] = None):
        """
        Initialize the cache.
        
        Args:
            cache_file: Path to the JSON file for persistence
            ttl: Time-to-live in seconds for cached values (optional)
        """
        self.cache_file = Path(cache_file)
        self.ttl = ttl
        self._cache = self._load()
    
    def _load(self) -> dict:
        """Load cache from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save(self):
        """Save cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self._cache, f, indent=2)
    
    def _is_expired(self, key: str) -> bool:
        """Check if a key has expired based on TTL."""
        if self.ttl is None:
            return False
        if key not in self._cache:
            return True
        entry = self._cache[key]
        if isinstance(entry, dict) and 'expires_at' in entry:
            return time.time() > entry['expires_at']
        return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the cache."""
        if key in self._cache and not self._is_expired(key):
            entry = self._cache[key]
            if isinstance(entry, dict) and 'value' in entry:
                return entry['value']
            return entry
        return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a value in the cache."""
        if ttl is not None or self.ttl is not None:
            expires_at = time.time() + (ttl if ttl is not None else self.ttl)
            self._cache[key] = {'value': value, 'expires_at': expires_at}
        else:
            self._cache[key] = value
        self._save()
    
    def delete(self, key: str) -> bool:
        """Delete a key from the cache."""
        if key in self._cache:
            del self._cache[key]
            self._save()
            return True
        return False
    
    def clear(self):
        """Clear all items from the cache."""
        self._cache = {}
        self._save()
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists and is not expired."""
        return key in self._cache and not self._is_expired(key)
    
    def __len__(self) -> int:
        """Return the number of cached items."""
        return len([k for k in self._cache if not self._is_expired(k)])
