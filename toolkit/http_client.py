import httpx
import asyncio


async def fetch_with_retry(url: str, max_retries: int = 3, timeout: float = 30.0) -> httpx.Response:
    """Fetch a URL with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                return resp
        except (httpx.HTTPError, httpx.TimeoutException) as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
    raise RuntimeError("Unreachable")
