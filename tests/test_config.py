import os
import pytest
from toolkit.config import load_config


def test_defaults():
    # Clear any env vars
    for k in ["API_URL", "API_TOKEN", "LOG_LEVEL", "TIMEOUT"]:
        os.environ.pop(k, None)
    config = load_config()
    assert config["API_URL"] == "https://api.clawcolab.com"
    assert config["API_TOKEN"] == ""
    assert config["LOG_LEVEL"] == "INFO"
    assert config["TIMEOUT"] == 30.0


def test_env_override():
    os.environ["API_URL"] = "https://custom.example.com"
    os.environ["LOG_LEVEL"] = "DEBUG"
    config = load_config()
    assert config["API_URL"] == "https://custom.example.com"
    assert config["LOG_LEVEL"] == "DEBUG"
    # Cleanup
    del os.environ["API_URL"]
    del os.environ["LOG_LEVEL"]


def test_returns_dict():
    config = load_config()
    assert isinstance(config, dict)
