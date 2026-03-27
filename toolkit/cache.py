import json
import os
from typing import Any, Optional


class FileCache:
    """Simple JSON file-based key-value cache with optional TTL."""

    def __init__(self, path: str):
        self.path = path
        self._data: dict = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self._data, f)

    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)

    def set(self, key: str, value: Any):
        self._data[key] = value
        self._save()

    def delete(self, key: str):
        self._data.pop(key, None)
        self._save()

    def clear(self):
        self._data = {}
        self._save()
