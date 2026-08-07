---
title: Getting Started
sidebar_position: 3
---

# Getting Started

This guide walks you through your first complete integration with the ProductBridge API. By the end, you will create a product, sync it to a sales channel, update its inventory, and handle errors gracefully.

**Time required:** 15 minutes  
**Prerequisites:** A ProductBridge account with API access and a valid API key

---

## Before You Begin

### Verify Your Setup

Run these commands to confirm your environment is ready:

```bash
# Check that curl is installed
curl --version

# Verify your API key is set
# (Never hardcode keys in scripts — use environment variables)
echo $PB_API_KEY
```

If `$PB_API_KEY` is empty, set it now:

```bash
export PB_API_KEY="pb_live_your_actual_key_here"
```

### Confirm API Connectivity

```bash
curl -s https://api.productbridge.io/v1/health | jq .
```

You should see `status: healthy`. If not, check your network or contact support.

---

## Step 1: Create Your First Product

Create a product in `draft` status. We will publish it to Shopify in the next step.

```bash
curl -X POST https://api.productbridge.io/v1/products \
  -H "X-API-Key: $PB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "DEMO-SKU-001",
    "name": "Acme Wireless Mouse",
    "description": "Ergonomic wireless mouse with 2.4GHz connectivity",
    "price": 29.99,
    "currency": "USD",
    "inventory_count": 100,
    "category": "Electronics",
    "channels": ["shopify"],
    "attributes": {
      "color": "Graphite",
      "wireless": "true",
      "dpi": "1600"
    }
  }'
```

**Expected response (`201 Created`):**

```json
{
  "id": "prod_7a3f9e2d",
  "sku": "DEMO-SKU-001",
  "name": "Acme Wireless Mouse",
  "price": 29.99,
  "currency": "USD",
  "status": "draft",
  "inventory_count": 100,
  "channels": ["shopify"],
  "created_at": "2026-08-06T17:10:00Z",
  "updated_at": "2026-08-06T17:10:00Z"
}
```

**Save the `id` value.** You will need `prod_7a3f9e2d` for the remaining steps.

### What Just Happened

- ProductBridge created the product in `draft` status
- It is associated with the `shopify` channel but not yet synced
- The `channel_status` field is not shown in the `POST` response; we will inspect it in Step 2

---

## Step 2: Inspect the Product

Retrieve the full product record to see its channel sync state:

```bash
curl -s https://api.productbridge.io/v1/products/prod_7a3f9e2d \
  -H "X-API-Key: $PB_API_KEY" | jq .
```

Look for the `channel_status` object:

```json
{
  "channel_status": {
    "shopify": {
      "status": "not_connected",
      "last_synced_at": null,
      "external_id": null
    }
  }
}
```

`not_connected` means the product exists in ProductBridge but has never been pushed to Shopify. This is expected — we have not triggered a sync yet.

---

## Step 3: Sync to Shopify

Trigger a sync to push the product live:

```bash
curl -X POST https://api.productbridge.io/v1/products/prod_7a3f9e2d/sync \
  -H "X-API-Key: $PB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "channels": ["shopify"],
    "force": false
  }'
```

**Expected response (`202 Accepted`):**

```json
{
  "job_id": "job_9c4b8d1e",
  "status": "queued",
  "channels": ["shopify"],
  "estimated_completion": "2026-08-06T17:11:30Z"
}
```

Sync is asynchronous. The API returns immediately with a `job_id`. You poll for completion.

---

## Step 4: Poll for Sync Completion

Check the job status every few seconds until it completes:

```bash
curl -s https://api.productbridge.io/v1/sync/jobs/job_9c4b8d1e \
  -H "X-API-Key: $PB_API_KEY" | jq .
```

**While running:**

```json
{
  "job_id": "job_9c4b8d1e",
  "status": "running",
  "channels": [
    { "name": "shopify", "status": "syncing" }
  ]
}
```

**When complete:**

```json
{
  "job_id": "job_9c4b8d1e",
  "status": "completed",
  "channels": [
    {
      "name": "shopify",
      "status": "synced",
      "external_id": "gid://shopify/Product/9876543210"
    }
  ]
}
```

**Save the `external_id`.** This is the Shopify product ID. If you need to debug on the Shopify side, this is your anchor.

### Polling Strategy

In production, do not poll in a tight loop. Use exponential backoff:

| Attempt | Delay | Total Elapsed |
|---------|-------|---------------|
| 1 | 1s | 1s |
| 2 | 2s | 3s |
| 3 | 4s | 7s |
| 4 | 8s | 15s |
| 5 | 15s | 30s |
| 6+ | 15s | — |

Stop polling after **5 minutes** and surface a timeout error to your user.

---

## Step 5: Update Inventory

A customer buys a unit on Shopify. Decrement inventory in ProductBridge:

```bash
curl -X PATCH https://api.productbridge.io/v1/products/prod_7a3f9e2d \
  -H "X-API-Key: $PB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inventory_count": 99
  }'
```

**Expected response (`200 OK`):**

```json
{
  "id": "prod_7a3f9e2d",
  "inventory_count": 99,
  "updated_at": "2026-08-06T17:12:00Z"
}
```

ProductBridge automatically propagates inventory changes to connected channels. You do not need to trigger a manual sync for standard field updates.

### When Auto-Sync Fails

If the auto-sync fails (e.g., Shopify API is temporarily down), ProductBridge:

1. Retries up to 3 times with exponential backoff
2. Marks the channel status as `failed`
3. Queues the sync for the next scheduled batch run

Check the product's `channel_status` to confirm:

```bash
curl -s https://api.productbridge.io/v1/products/prod_7a3f9e2d \
  -H "X-API-Key: $PB_API_KEY" | jq '.channel_status'
```

---

## Step 6: Clean Up

Delete the demo product to avoid clutter:

```bash
curl -X DELETE https://api.productbridge.io/v1/products/prod_7a3f9e2d \
  -H "X-API-Key: $PB_API_KEY"
```

**Expected response:** `204 No Content`

If you receive `409 Conflict`, the product may have active orders. Archive it instead by setting `status: archived` via `PATCH`.

---

## Full Lifecycle Script

Here is the complete flow as a single Bash script. Save it as `productbridge_demo.sh`, make it executable (`chmod +x`), and run it:

```bash
#!/usr/bin/env bash
set -euo pipefail

API_KEY="${PB_API_KEY:?Environment variable PB_API_KEY is required}"
BASE_URL="https://api.productbridge.io/v1"

# 1. Create product
echo "=== Creating product ==="
PRODUCT=$(curl -s -X POST "$BASE_URL/products" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "DEMO-SKU-'"$(date +%s)"'",
    "name": "Acme Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": 29.99,
    "currency": "USD",
    "inventory_count": 100,
    "category": "Electronics",
    "channels": ["shopify"]
  }')

PRODUCT_ID=$(echo "$PRODUCT" | jq -r '.id')
echo "Created product: $PRODUCT_ID"

# 2. Sync to Shopify
echo "=== Syncing to Shopify ==="
SYNC=$(curl -s -X POST "$BASE_URL/products/$PRODUCT_ID/sync" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{'"channels'":['"shopify'"]}')

JOB_ID=$(echo "$SYNC" | jq -r '.job_id')
echo "Sync job: $JOB_ID"

# 3. Poll for completion
echo "=== Polling sync status ==="
for i in {1..10}; do
  STATUS=$(curl -s "$BASE_URL/sync/jobs/$JOB_ID" -H "X-API-Key: $API_KEY" | jq -r '.status')
  echo "Attempt $i: $STATUS"
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    break
  fi
  sleep 2
done

# 4. Update inventory
echo "=== Updating inventory ==="
curl -s -X PATCH "$BASE_URL/products/$PRODUCT_ID" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{'"inventory_count'":99}' | jq .

# 5. Delete
echo "=== Deleting product ==="
curl -s -X DELETE "$BASE_URL/products/$PRODUCT_ID" -H "X-API-Key: $API_KEY"
echo "Deleted."
```

---

## Common First-Time Pitfalls

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `401` on every call | Using staging key on production URL | Match key prefix to base URL (`pb_live_*` → `api.productbridge.io`) |
| `422` on create | Missing required field `currency` | Check the `ProductCreate` schema; `currency` is required even if price is 0 |
| Sync stays `queued` forever | Channel not connected in dashboard | Go to **Settings → Channels** and authenticate Shopify before syncing |
| `409` on delete | Product has active orders | `PATCH` to `archived` instead, or wait for orders to complete |
| Inventory update not reflected | Polling too fast after `PATCH` | Wait 2–3 seconds; auto-sync is near-realtime but not instantaneous |

---

## Production Checklist

Before deploying your integration:

- [ ] API key stored in secret manager, not code or `.env` files in production
- [ ] Retry logic with exponential backoff implemented for all idempotent requests
- [ ] Rate limit headers (`X-RateLimit-Remaining`) monitored and logged
- [ ] Sync job polling capped at 5 minutes with timeout handling
- [ ] Webhook endpoint configured to receive async sync completion events (recommended over polling)
- [ ] Error responses parsed and surfaced to your observability stack
- [ ] `sku` values are globally unique within your ProductBridge account
- [ ] Sandbox/staging environment tested end-to-end before production deployment

---

## Next Steps

- **[Authentication](./authentication.md)** — Key rotation, permissions, and security best practices
- **[Error Handling](./error-handling.md)** — Retry strategies, circuit breakers, and idempotency
- **API Reference** — Complete endpoint documentation generated from our OpenAPI spec
