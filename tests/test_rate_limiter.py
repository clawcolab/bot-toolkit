"""Tests for RateLimiter."""

import asyncio
import time
from unittest.mock import patch

import pytest

from toolkit.rate_limiter import RateLimiter, RateLimitExceeded


@pytest.mark.asyncio
async def test_rate_limiter_allows_within_limit():
    """Test that calls within limit are allowed."""
    limiter = RateLimiter(max_calls=5, period=60)
    for _ in range(5):
        await limiter.acquire()
    # 5th call should not raise


@pytest.mark.asyncio
async def test_rate_limiter_raises_after_limit():
    """Test that RateLimitExceeded is raised after max_calls."""
    limiter = RateLimiter(max_calls=3, period=60)
    for _ in range(3):
        await limiter.acquire()
    
    with pytest.raises(RateLimitExceeded):
        await limiter.acquire()


@pytest.mark.asyncio
async def test_rate_limiter_resets_after_period():
    """Test that calls are allowed again after the period expires."""
    limiter = RateLimiter(max_calls=2, period=0.1)
    
    await limiter.acquire()
    await limiter.acquire()
    
    with pytest.raises(RateLimitExceeded):
        await limiter.acquire()
    
    # Wait for period to elapse
    await asyncio.sleep(0.15)
    
    # Should be allowed again
    await limiter.acquire()


@pytest.mark.asyncio
async def test_rate_limiter_context_manager():
    """Test using rate limiter as async context manager."""
    limiter = RateLimiter(max_calls=2, period=60)
    async with limiter:
        pass  # should not raise
    async with limiter:
        pass  # should not raise
    # Third entry should raise
    with pytest.raises(RateLimitExceeded):
        async with limiter:
            pass  # should not reach here


def test_rate_limiter_reset():
    """Test that reset clears call history."""
    limiter = RateLimiter(max_calls=1, period=60)
    
    async def do_calls():
        await limiter.acquire()
        await limiter.acquire()  # raises
    
    # Consume the one allowed call
    limiter._calls.append(time.monotonic())
    
    limiter.reset()
    assert len(limiter._calls) == 0
