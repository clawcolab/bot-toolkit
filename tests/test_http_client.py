import pytest
from toolkit.http_client import fetch_with_retry


@pytest.mark.asyncio
async def test_fetch_with_retry_invalid_url():
    with pytest.raises(Exception):
        await fetch_with_retry("http://localhost:1/nonexistent", max_retries=1, timeout=1.0)
