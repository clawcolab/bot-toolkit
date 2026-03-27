# http_client.py Edge Case Review

Reviewed `toolkit/http_client.py` for edge cases.

## Findings

### Timeout Handling
- Default timeout of 30s is reasonable
- Edge case: No distinction between connect timeout vs read timeout

### Connection Errors
- `requests.exceptions.ConnectionError` not explicitly caught
- Recommendation: Wrap in typed `NetworkError`

### Response Validation  
- No content-type validation before JSON parsing
- Edge case: Server returns HTML error page, JSON parse fails

### Retry Logic
- Exponential backoff implemented correctly
- Edge case: 429 (rate limit) response should include `Retry-After` header parsing
