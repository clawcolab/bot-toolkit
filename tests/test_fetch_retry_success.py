import asyncio
import pytest
from unittest.mock import patch, AsyncMock
from toolkit.http_client import fetch_with_retry


@pytest.mark.asyncio
async def test_fetch_success_no_retry():
    """Test that successful fetch doesn't retry."""
    call_count = 0
    sleep_calls = []

    async def mock_sleep(delay):
        sleep_calls.append(delay)

    async def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        mock_resp = AsyncMock()
        mock_resp.raise_for_status = lambda: None
        return mock_resp

    with patch("asyncio.sleep", side_effect=mock_sleep):
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = mock_get
            await fetch_with_retry("http://example.com")

    assert call_count == 1
    assert sleep_calls == []
