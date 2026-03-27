"""Tests for config loader."""
import os
import pytest
from toolkit.config import load_config


def test_load_config_defaults():
    """Test defaults when no env vars set."""
    # Clear relevant env vars
    for var in ["API_URL", "API_TOKEN", "LOG_LEVEL", "TIMEOUT"]:
        os.environ.pop(var, None)
    
    config = load_config()
    
    assert config["api_url"] == "http://localhost:8000"
    assert config["api_token"] == ""
    assert config["log_level"] == "INFO"
    assert config["timeout"] == 30


def test_load_config_from_env(monkeypatch):
    """Test loading from environment variables."""
    monkeypatch.setenv("API_URL", "https://api.example.com")
    monkeypatch.setenv("API_TOKEN", "secret123")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TIMEOUT", "60")
    
    config = load_config()
    
    assert config["api_url"] == "https://api.example.com"
    assert config["api_token"] == "secret123"
    assert config["log_level"] == "DEBUG"
    assert config["timeout"] == 60


def test_load_config_overrides(monkeypatch):
    """Test explicit args override env vars."""
    monkeypatch.setenv("API_URL", "https://env-url.com")
    
    config = load_config(api_url="https://arg-url.com")
    
    assert config["api_url"] == "https://arg-url.com"


def test_convenience_accessors(monkeypatch):
    """Test lambda accessors."""
    from toolkit.config import API_URL, API_TOKEN, LOG_LEVEL, TIMEOUT
    
    monkeypatch.setenv("API_URL", "https://test.com")
    monkeypatch.setenv("API_TOKEN", "tok")
    monkeypatch.setenv("LOG_LEVEL", "WARN")
    monkeypatch.setenv("TIMEOUT", "45")
    
    assert API_URL() == "https://test.com"
    assert API_TOKEN() == "tok"
    assert LOG_LEVEL() == "WARN"
    assert TIMEOUT() == 45
