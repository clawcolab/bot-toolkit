"""
Configuration loader from environment variables.
"""
import os
from typing import Optional


def load_config(
    api_url: Optional[str] = None,
    api_token: Optional[str] = None,
    log_level: Optional[str] = None,
    timeout: Optional[int] = None,
) -> dict:
    """
    Load configuration from environment variables with defaults.
    
    Args:
        api_url: API_URL env var (default: "http://localhost:8000")
        api_token: API_TOKEN env var (default: "")
        log_level: LOG_LEVEL env var (default: "INFO")
        timeout: TIMEOUT env var in seconds (default: 30)
    
    Returns:
        dict with configuration values
    """
    return {
        "api_url": api_url or os.getenv("API_URL", "http://localhost:8000"),
        "api_token": api_token or os.getenv("API_TOKEN", ""),
        "log_level": log_level or os.getenv("LOG_LEVEL", "INFO"),
        "timeout": timeout or int(os.getenv("TIMEOUT", "30")),
    }


# Convenience accessors
API_URL = lambda: os.getenv("API_URL", "http://localhost:8000")
API_TOKEN = lambda: os.getenv("API_TOKEN", "")
LOG_LEVEL = lambda: os.getenv("LOG_LEVEL", "INFO")
TIMEOUT = lambda: int(os.getenv("TIMEOUT", "30"))
