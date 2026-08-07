---
title: Error Handling
sidebar_position: 4
---

# Error Handling

Production integrations fail. Networks partition, APIs rate-limit, channels reject payloads, and data drifts. This guide teaches you to handle every failure mode in the ProductBridge API with resilience, not fragility.

---

## Understanding the Error Contract

Every error response follows this structure:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "details": "Limit: 100 requests/minute. Retry after 45 seconds"
  }
}
```

| Field | Type | Purpose |
|-------|------|---------|
| `code` | `string` | Machine-readable identifier. Use this for branching logic, not `message`. |
| `message` | `string` | Human-readable summary. Safe to log and display. |
| `details` | `string \| null` | Context-specific explanation. May contain request IDs or variable data. |

**Rule:** Branch on `code`. Display `message`. Log `details`.

---

## HTTP Status Codes and Recovery Actions

| Status | Meaning | Retry? | Action |
|--------|---------|--------|--------|
| `400` | Bad Request | No | Fix the request body or query parameters |
| `401` | Unauthorized | No | Check or rotate your API key |
| `404` | Not Found | No | Verify the resource ID; may have been deleted |
| `409` | Conflict | Maybe | Check `details`; retry if transient (e.g., sync in progress) |
| `422` | Validation Error | No | Fix the request payload against the schema |
| `429` | Rate Limit Exceeded | **Yes** | Read `Retry-After` header; back off |
| `500` | Internal Server Error | **Yes** | Retry with exponential backoff; contact support if persistent |
| `502` / `503` / `504` | Gateway / Service Unavailable | **Yes** | Retry with exponential backoff; check `/health` |

---

## Retry Strategy: Exponential Backoff with Jitter

Never retry immediately. Use exponential backoff to avoid thundering herds.

### Algorithm

```python
import random
import time

def sleep_with_backoff(attempt, base_delay=1.0, max_delay=60.0):
    # Calculate sleep duration with exponential backoff and full jitter.
    # attempt: 0-indexed retry count
    exponential = base_delay * (2 ** attempt)
    capped = min(exponential, max_delay)
    jittered = random.uniform(0, capped)
    time.sleep(jittered)
```

### Recommended Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `base_delay` | `1.0` second | Fast enough for UX; slow enough to not hammer |
| `max_delay` | `60.0` seconds | Prevents multi-hour hangs |
| `max_retries` | `5` | Total of 6 attempts (initial + 5 retries) |
| `retryable_statuses` | `[429, 500, 502, 503, 504]` | Do not retry 4xx client errors |

### Python Implementation

```python
import requests
import time
import random

class ProductBridgeClient:
    def __init__(self, api_key, base_url="https://api.productbridge.io/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Accept": "application/json",
        })

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        max_retries = 5
        base_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                response = self.session.request(method, url, timeout=30, **kwargs)
            except requests.exceptions.Timeout:
                if attempt == max_retries:
                    raise
                self._backoff(attempt, base_delay)
                continue
            except requests.exceptions.ConnectionError:
                if attempt == max_retries:
                    raise
                self._backoff(attempt, base_delay)
                continue

            if response.status_code in (429, 500, 502, 503, 504):
                if attempt == max_retries:
                    response.raise_for_status()

                # Respect Retry-After if present (especially for 429)
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    time.sleep(int(retry_after))
                else:
                    self._backoff(attempt, base_delay)
                continue

            # Non-retryable 4xx or success
            return response

        return response  # Should not reach here

    def _backoff(self, attempt, base_delay):
        delay = min(base_delay * (2 ** attempt), 60.0)
        jitter = random.uniform(0, delay)
        time.sleep(jitter)

    def get_product(self, product_id):
        resp = self.request("GET", f"/products/{product_id}")
        resp.raise_for_status()
        return resp.json()
```

### JavaScript/TypeScript Implementation

```typescript
class ProductBridgeClient {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string, baseUrl = "https://api.productbridge.io/v1") {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private backoff(attempt: number, baseDelay = 1000): number {
    const exponential = baseDelay * Math.pow(2, attempt);
    const capped = Math.min(exponential, 60000);
    return Math.random() * capped; // Full jitter
  }

  async request(
    method: string,
    path: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const url = `${this.baseUrl}${path}`;
    const maxRetries = 5;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const response = await fetch(url, {
          ...options,
          method,
          headers: {
            "X-API-Key": this.apiKey,
            "Accept": "application/json",
            "Content-Type": "application/json",
            ...options.headers,
          },
        });

        if ([429, 500, 502, 503, 504].includes(response.status)) {
          if (attempt === maxRetries) {
            throw new Error(`HTTP ${response.status}: ${await response.text()}`);
          }

          const retryAfter = response.headers.get("Retry-After");
          if (retryAfter) {
            await this.sleep(parseInt(retryAfter) * 1000);
          } else {
            await this.sleep(this.backoff(attempt));
          }
          continue;
        }

        return response;
      } catch (err) {
        if (attempt === maxRetries) throw err;
        await this.sleep(this.backoff(attempt));
      }
    }

    throw new Error("Max retries exceeded");
  }

  async getProduct(productId: string) {
    const resp = await this.request("GET", `/products/${productId}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return resp.json();
  }
}
```

---

## Handling Rate Limits (`429`)

Rate limiting is not an error — it is a signal to slow down.

### Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Requests allowed per minute |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |
| `Retry-After` | Seconds to wait before retrying (present on `429` only) |

### Strategy

1. **Always check `Retry-After` first.** If present, sleep for exactly that duration.
2. **If `Retry-After` is missing,** fall back to exponential backoff.
3. **Proactive throttling:** Monitor `X-RateLimit-Remaining`. If it drops below 10, slow down your request rate before hitting the limit.

```python
remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
if remaining < 10:
    time.sleep(1)  # Add artificial delay to stay under the limit
```

---

## Idempotency: Safe Retries for Write Operations

`POST`, `PATCH`, and `DELETE` are not inherently safe to retry. A network timeout may leave you uncertain whether the operation succeeded.

### The Problem

```
Client → POST /products (create widget) → Network timeout
Client unsure: Did the product get created?
Client retries → POST /products → 409 Conflict (duplicate SKU)
```

### The Solution: Idempotency Keys

ProductBridge does not natively support idempotency keys. You must implement client-side idempotency for write operations.

#### Pattern: Client-Generated Idempotency

1. Generate a UUID for each logical operation
2. Store the UUID and the API response in a local cache (Redis, database, or in-memory with TTL)
3. Before making a request, check the cache
4. If the same UUID was used recently, return the cached response instead of calling the API again

```python
import uuid
import hashlib
from datetime import datetime, timedelta

class IdempotentClient(ProductBridgeClient):
    def __init__(self, api_key, cache, ttl_seconds=300):
        super().__init__(api_key)
        self.cache = cache  # e.g., Redis client
        self.ttl = ttl_seconds

    def create_product(self, payload):
        # Generate idempotency key from payload content
        key = f"idempotency:create:{self._hash_payload(payload)}"

        cached = self.cache.get(key)
        if cached:
            return cached  # Already created; return cached result

        response = self.request("POST", "/products", json=payload)

        if response.status_code == 201:
            data = response.json()
            self.cache.setex(key, self.ttl, data)
            return data
        elif response.status_code == 409:
            # Product may already exist; fetch by SKU to confirm
            return self._resolve_conflict(payload["sku"])
        else:
            response.raise_for_status()

    def _hash_payload(self, payload):
        return hashlib.sha256(str(payload).encode()).hexdigest()[:16]

    def _resolve_conflict(self, sku):
        # List products filtered by SKU to find the existing record
        resp = self.request("GET", f"/products?q={sku}")
        products = resp.json()["data"]
        return products[0] if products else None
```

**TTL recommendation:** 5 minutes. This covers transient network failures without polluting the cache.

---

## Handling Specific Error Codes

### `DUPLICATE_SKU` (`409` on `POST /products`)

**Cause:** A product with this SKU already exists.  
**Recovery:**

1. Fetch the existing product by SKU: `GET /products?q={sku}`
2. If the existing product matches your intent, treat as success
3. If it differs, decide: update the existing product (`PATCH`) or use a different SKU

```python
def create_or_update_product(client, payload):
    try:
        return client.create_product(payload)
    except ConflictError as e:
        if "DUPLICATE_SKU" in str(e):
            existing = client.find_by_sku(payload["sku"])
            return client.update_product(existing["id"], payload)
        raise
```

### `RESOURCE_LOCKED` (`409` on `DELETE`)

**Cause:** Product has active orders.  
**Recovery:**

1. Do not retry the delete
2. Archive the product instead: `PATCH /products/{id}` with `{ "status": "archived" }`
3. Schedule a background job to delete once orders complete

### `VALIDATION_ERROR` (`422`)

**Cause:** Request body violates the schema.  
**Recovery:**

1. Parse `details` for the specific field failure
2. Fix the payload
3. Do not retry blindly — it will fail identically

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": "Field 'price' must be a positive number, got -5.00"
  }
}
```

### `RATE_LIMIT_EXCEEDED` (`429`)

**Cause:** Too many requests.  
**Recovery:**

1. Read `Retry-After` header
2. Sleep for that duration
3. Retry the exact same request

---

## Network-Level Failures

Not all failures come from ProductBridge. Handle these at the transport layer:

| Failure | Symptom | Action |
|---------|---------|--------|
| **DNS resolution failure** | `getaddrinfo ENOTFOUND` | Retry; may be transient ISP issue |
| **Connection timeout** | `ETIMEDOUT` after ~30s | Retry with backoff |
| **TLS handshake failure** | `SSL_ERROR_SYSCALL` | Do not retry; check system clock and certificates |
| **Read timeout** | Request sent, no response body | **Dangerous to retry for writes** — use idempotency keys |

### Timeout Configuration

```python
# Python requests
timeout = (5, 30)  # 5s connect, 30s read

# Node.js fetch
const controller = new AbortController();
setTimeout(() => controller.abort(), 30000);
const resp = await fetch(url, { signal: controller.signal });
```

---

## Circuit Breaker Pattern

If ProductBridge returns repeated `500`/`503` errors, stop calling it temporarily to prevent cascading failures.

### Simple Circuit Breaker (Python)

```python
from enum import Enum
import time

class State(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = State.CLOSED
        self.failures = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = State.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failures = 0
        self.state = State.CLOSED

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = State.OPEN
```

**Usage:**

```python
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

try:
    product = breaker.call(client.get_product, "prod_123")
except Exception as e:
    # Serve stale cache or queue for later processing
    product = cache.get("prod_123")
```

---

## Observability: Logging and Metrics

Every API client should emit structured logs. Here is the minimum viable logging strategy:

### Required Log Fields

```json
{
  "timestamp": "2026-08-06T17:15:00Z",
  "level": "ERROR",
  "service": "inventory-sync",
  "event": "api_request_failed",
  "method": "POST",
  "path": "/v1/products/prod_123/sync",
  "status_code": 429,
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 45,
  "request_id": "req_abc123",
  "duration_ms": 120,
  "attempt": 3
}
```

### Metrics to Track

| Metric | Why It Matters |
|--------|---------------|
| `api_requests_total` (labeled by method, path, status) | Spot trends in error rates |
| `api_request_duration_seconds` | Detect latency degradation |
| `api_retries_total` | Identify flaky endpoints |
| `api_rate_limit_hits` | Capacity planning signal |
| `sync_job_duration_seconds` | End-to-end sync health |

### Alerting Thresholds

| Condition | Severity | Action |
|-----------|----------|--------|
| Error rate > 5% for 5 minutes | Warning | Page on-call engineer |
| Error rate > 20% for 2 minutes | Critical | Escalate; check ProductBridge status page |
| `429` rate > 10% | Warning | Review request batching logic |
| Sync job failure rate > 1% | Warning | Check channel credentials and mappings |

---

## Decision Tree: What to Do When a Request Fails

```
Request fails
│
├─→ Is it a network error (timeout, DNS, connection)?
│   ├─→ Yes: Retry with exponential backoff (max 5 attempts)
│   └─→ No: Continue
│
├─→ Is status 429?
│   ├─→ Yes: Read Retry-After, sleep, retry
│   └─→ No: Continue
│
├─→ Is status 5xx?
│   ├─→ Yes: Retry with exponential backoff (max 5 attempts)
│   │         If persistent, open circuit breaker
│   └─→ No: Continue
│
├─→ Is status 409 with DUPLICATE_SKU?
│   ├─→ Yes: Fetch existing product, treat as success or PATCH
│   └─→ No: Continue
│
├─→ Is status 400, 401, 404, 422?
│   └─→ Yes: Do NOT retry. Fix client code or data.
│
└─→ Log structured error, emit metric, alert if threshold crossed
```

---

## Summary

| Principle | Implementation |
|-----------|---------------|
| **Retry safely** | Exponential backoff + jitter; respect `Retry-After` |
| **Never retry blindly** | Branch on `error.code`, not status alone |
| **Make writes idempotent** | Cache responses keyed by operation hash |
| **Fail fast at the edge** | Circuit breaker prevents cascade failures |
| **Observe everything** | Structured logs and metrics for every request |
| **Handle the long tail** | Network timeouts, TLS failures, and read timeouts need explicit handling |

---

## See Also

- [Authentication](./authentication.md) — Key rotation and permission management
- [Getting Started](./getting-started.md) — End-to-end integration walkthrough
- **API Reference** — Complete OpenAPI specification
