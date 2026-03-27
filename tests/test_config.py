"""Tests for config loader."""

import os
from unittest.mock import patch

from toolkit.config import load_config, DEFAULT_CONFIG


def test_load_config_defaults():
    """Test config returns defaults when no env vars are set."""
    env = {k: v for k, v in os.environ.items() if k in ("API_URL", "API_TOKEN", "LOG_LEVEL", "TIMEOUT")}
    # Clear only the vars we control
    with patch.dict(os.environ, {
        "API_URL": "",
        "API_TOKEN": "",
        "LOG_LEVEL": "",
        "TIMEOUT": "",
    }, clear=False):
        # Remove vars if they exist
        for k in ("API_URL", "API_TOKEN", "LOG_LEVEL", "TIMEOUT"):
            os.environ.pop(k, None)
        cfg = load_config()
    
    assert cfg["API_URL"] == DEFAULT_CONFIG["API_URL"]
    assert cfg["API_TOKEN"] == DEFAULT_CONFIG["API_TOKEN"]
    assert cfg["LOG_LEVEL"] == DEFAULT_CONFIG["LOG_LEVEL"]
    assert cfg["TIMEOUT"] == DEFAULT_CONFIG["TIMEOUT"]


def test_load_config_env_override():
    """Test config reads from environment variables."""
    env_vars = {
        "API_URL": "https://custom.api.com",
        "API_TOKEN": "secret-token-123",
        "LOG_LEVEL": "DEBUG",
        "TIMEOUT": "60.0",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        cfg = load_config()
    
    assert cfg["API_URL"] == "https://custom.api.com"
    assert cfg["API_TOKEN"] == "secret-token-123"
    assert cfg["LOG_LEVEL"] == "DEBUG"
    assert cfg["TIMEOUT"] == 60.0


def test_load_config_returns_dict():
    """Test that load_config returns a dict."""
    cfg = load_config()
    assert isinstance(cfg, dict)


def test_load_config_timeout_conversion():
    """Test that TIMEOUT is converted to float."""
    with patch.dict(os.environ, {"TIMEOUT": "15.5"}, clear=False):
        cfg = load_config()
    assert cfg["TIMEOUT"] == 15.5
    assert isinstance(cfg["TIMEOUT"], float)
