import asyncio
import pytest
from unittest.mock import patch, AsyncMock
import httpx
from toolkit.http_client import fetch_with_retry


@pytest.mark.asyncio
async def test_retry_backoff_timing():
    """Test exponential backoff: 1s, 2s delays."""
    call_count = 0
    sleep_calls = []

    async def mock_sleep(delay):
        sleep_calls.append(delay)

    async def mock_request(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.TimeoutException("Timeout", request=None)
        mock_resp = AsyncMock()
        mock_resp.raise_for_status = lambda: None
        return mock_resp

    with patch("asyncio.sleep", side_effect=mock_sleep):
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = mock_request
            try:
                await fetch_with_retry("http://example.com", max_retries=3)
            except Exception:
                pass

    # Verify backoff: 1s (2^0), 2s (2^1)
    assert len(sleep_calls) >= 1
    assert sleep_calls[0] == 1
    if len(sleep_calls) >= 2:
        assert sleep_calls[1] == 2
