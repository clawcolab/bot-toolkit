"""Config loader from environment variables."""

import os
from typing import Dict


DEFAULT_CONFIG = {
    "API_URL": "https://api.clawcolab.com",
    "API_TOKEN": None,
    "LOG_LEVEL": "INFO",
    "TIMEOUT": 30.0,
}


def load_config() -> Dict:
    """Load configuration from environment variables with defaults.
    
    Supports: API_URL, API_TOKEN, LOG_LEVEL, TIMEOUT.
    Falls back to defaults for any missing env vars.
    """
    return {
        "API_URL": os.environ.get("API_URL", DEFAULT_CONFIG["API_URL"]),
        "API_TOKEN": os.environ.get("API_TOKEN", DEFAULT_CONFIG["API_TOKEN"]),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", DEFAULT_CONFIG["LOG_LEVEL"]),
        "TIMEOUT": float(os.environ.get("TIMEOUT", DEFAULT_CONFIG["TIMEOUT"])),
    }
