"""Async rate limiter."""

import asyncio
import time
from typing import List


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass


class RateLimiter:
    """Async rate limiter with max_calls per period.
    
    Example:
        limiter = RateLimiter(max_calls=5, period=60.0)
        async with limiter:
            await do_request()
    """

    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self._calls: List[float] = []

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, *args):
        pass

    async def acquire(self):
        """Acquire a rate limit slot. Raises if limit exceeded."""
        now = time.monotonic()
        # Remove expired entries
        cutoff = now - self.period
        self._calls = [t for t in self._calls if t > cutoff]

        if len(self._calls) >= self.max_calls:
            raise RateLimitExceeded(
                f"Rate limit exceeded: {self.max_calls} calls per {self.period}s"
            )

        self._calls.append(now)

    def reset(self):
        """Reset the rate limiter."""
        self._calls.clear()
