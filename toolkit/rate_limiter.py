import asyncio
import time


class RateLimiter:
    """Async rate limiter: max_calls per period_seconds."""

    def __init__(self, max_calls: int, period_seconds: float):
        self.max_calls = max_calls
        self.period = period_seconds
        self._calls: list = []

    async def acquire(self):
        now = time.monotonic()
        # Remove old calls outside the window
        self._calls = [t for t in self._calls if now - t < self.period]
        if len(self._calls) >= self.max_calls:
            raise RuntimeError(f"Rate limit exceeded: {self.max_calls} calls per {self.period}s")
        self._calls.append(now)
