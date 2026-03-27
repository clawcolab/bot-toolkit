import os
from typing import Any, Dict


def load_config() -> Dict[str, Any]:
    """Load config from environment variables with defaults."""
    return {
        "API_URL": os.environ.get("API_URL", "https://api.clawcolab.com"),
        "API_TOKEN": os.environ.get("API_TOKEN", ""),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
        "TIMEOUT": float(os.environ.get("TIMEOUT", "30.0")),
    }
