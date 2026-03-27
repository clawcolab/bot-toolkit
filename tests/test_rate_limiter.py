import asyncio
import pytest
from toolkit.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_allows_within_limit():
    rl = RateLimiter(max_calls=5, period_seconds=60)
    for _ in range(5):
        await rl.acquire()


@pytest.mark.asyncio
async def test_raises_when_exceeded():
    rl = RateLimiter(max_calls=3, period_seconds=60)
    for _ in range(3):
        await rl.acquire()
    with pytest.raises(RuntimeError, match="Rate limit exceeded"):
        await rl.acquire()


@pytest.mark.asyncio
async def test_resets_after_period():
    rl = RateLimiter(max_calls=2, period_seconds=0.1)
    await rl.acquire()
    await rl.acquire()
    await asyncio.sleep(0.15)
    await rl.acquire()  # Should succeed after period
