"""Test retry backoff timing for fetch_with_retry."""

import asyncio
from unittest.mock import AsyncMock, patch, ANY

import pytest
import httpx

from toolkit.http_client import fetch_with_retry


class FakeResponse:
    status_code = 200

    def raise_for_status(self):
        pass


@pytest.mark.asyncio
async def test_retry_backoff_timing():
    """Test that fetch_with_retry waits with exponential backoff between retries."""
    expected_delays = []
    for i in range(3):
        # Delays: 2^0=1s, 2^1=2s, 2^2=4s (for max_retries=3)
        expected_delays.append(2 ** i)

    call_count = 0

    async def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.HTTPError("transient error")
        return FakeResponse()

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get = mock_get
        mock_client_class.return_value = mock_client

        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.side_effect = AsyncMock()

            result = await fetch_with_retry("https://example.com", max_retries=3)

            assert call_count == 3
            assert result.status_code == 200

            # Verify sleep was called with exponential backoff
            assert mock_sleep.call_count == 2
            for i, expected_delay in enumerate(expected_delays[:-1]):
                actual_delay = mock_sleep.call_args_list[i][0][0]
                assert actual_delay == expected_delay, f"Retry {i+1}: expected {expected_delay}s, got {actual_delay}s"


@pytest.mark.asyncio
async def test_no_sleep_on_success():
    """Test that no sleep occurs when fetch succeeds on first attempt."""
    async def mock_get(*args, **kwargs):
        return FakeResponse()

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get = mock_get
        mock_client_class.return_value = mock_client

        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.side_effect = AsyncMock()

            result = await fetch_with_retry("https://example.com")

            assert result.status_code == 200
            mock_sleep.assert_not_called()


@pytest.mark.asyncio
async def test_raises_after_max_retries():
    """Test that HTTPError is raised after exhausting retries."""
    async def mock_get(*args, **kwargs):
        raise httpx.HTTPError("permanent error")

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get = mock_get
        mock_client_class.return_value = mock_client

        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.side_effect = AsyncMock()

            with pytest.raises(httpx.HTTPError):
                await fetch_with_retry("https://example.com", max_retries=3)

            assert mock_sleep.call_count == 2
