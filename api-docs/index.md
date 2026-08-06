---
title: ProductBridge API Documentation
sidebar_position: 1
---

# ProductBridge API

Connect, sync, and manage product catalogs across multiple sales channels from a single platform.

## What ProductBridge Does

ProductBridge acts as the central hub between your inventory system and marketplaces like Shopify, Amazon, eBay, Walmart, and Etsy. Instead of managing product data in five different dashboards, you manage it here — and we push changes everywhere.

**Typical workflow:**

1. Create a product in ProductBridge (`POST /products`)
2. Connect it to your sales channels
3. Sync it live (`POST /products/{id}/sync`)
4. Update inventory or pricing — changes propagate automatically

---

## Quickstart

Make your first API call in under two minutes.

### 1. Get an API key

Contact your account manager or generate a key from the [ProductBridge dashboard](https://app.productbridge.io/settings/api). You need the **Standard** tier or higher.

### 2. Test the health endpoint

The `/health` endpoint requires no authentication. Use it to verify connectivity:

```bash
curl -X GET https://api.productbridge.io/v1/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "1.2.0",
  "timestamp": "2026-08-06T13:52:00Z",
  "services": {
    "database": "up",
    "cache": "up",
    "queue": "up"
  }
}
```

If you see `status: healthy`, the API is reachable.

### 3. List your products

Now make an authenticated request. Replace `$PB_API_KEY` with your actual key:

```bash
curl -X GET https://api.productbridge.io/v1/products \
  -H "X-API-Key: $PB_API_KEY" \
  -H "Accept: application/json"
```

Expected response:

```json
{
  "data": [
    {
      "id": "prod_8f3a9b2c",
      "sku": "WH-1000XM5-BLK",
      "name": "Sony WH-1000XM5 Wireless Headphones",
      "price": 348.00,
      "currency": "USD",
      "status": "active",
      "inventory_count": 142
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 847,
    "total_pages": 43,
    "has_next": true,
    "has_prev": false
  }
}
```

If you receive a `200 OK` with product data, your integration is working.

---

## Base URLs

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.productbridge.io/v1` |
| Staging | `https://api.staging.productbridge.io/v1` |

All requests must use HTTPS. Unencrypted HTTP requests are rejected with a `400 Bad Request`.

---

## Authentication

Every request (except `/health`) requires an `X-API-Key` header. See [Authentication](./authentication.md) for details on key management, permissions, and rotation.

---

## Rate Limits

| Tier | Limit | Window |
|------|-------|--------|
| Standard | 100 requests | per minute |
| Enterprise | 1,000 requests | per minute |

We return the following headers with every response:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Requests allowed per window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

If you exceed the limit, you receive `429 Too Many Requests` with a `Retry-After` header.

---

## Errors

All errors follow a consistent structure:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Product not found",
    "details": "No product exists with ID prod_invalid123"
  }
}
```

| HTTP Status | Meaning | Typical Cause |
|-------------|---------|---------------|
| `400` | Bad Request | Invalid query parameters or malformed JSON |
| `401` | Unauthorized | Missing or invalid API key |
| `404` | Not Found | Resource does not exist |
| `409` | Conflict | Resource conflict (e.g., duplicate SKU) |
| `422` | Validation Error | Request body failed schema validation |
| `429` | Rate Limit Exceeded | Too many requests; check `Retry-After` |
| `503` | Service Unavailable | API degraded; check `/health` |

---

## Pagination

List endpoints return paginated results. Use `page` and `limit` query parameters:

```bash
curl -X GET "https://api.productbridge.io/v1/products?page=3&limit=50" \
  -H "X-API-Key: $PB_API_KEY"
```

- `page` starts at `1`
- `limit` defaults to `20`, maximum is `100`
- Use `has_next` in the response to determine if more pages exist

**Best practice:** Do not construct URLs from `total_pages`. Rely on `has_next` and the current query parameters.

---

## SDKs and Tools

We do not provide official SDKs. We recommend:

- **[OpenAPI Generator](https://openapi-generator.tech/)** — Generate client libraries in 50+ languages from our spec
- **[Postman](https://www.postman.com/)** — Import our OpenAPI spec for interactive testing
- **[HTTPie](https://httpie.io/)** — A user-friendly alternative to `curl`

---

## Changelog

### v1.2.0 (Current)
- Added `channel_status` to product responses
- Added `force` flag to sync endpoint
- Improved error detail granularity

### v1.1.0
- Added Walmart and Etsy channel support
- Added `updated_since` filter to `GET /products`

### v1.0.0
- Initial release

---

## Support

- **Documentation issues:** Open a ticket at [developer.productbridge.io/support](https://developer.productbridge.io/support)
- **API status:** [status.productbridge.io](https://status.productbridge.io)
- **Emergency:** Email `devsupport@productbridge.io` with "[URGENT]" in the subject line
