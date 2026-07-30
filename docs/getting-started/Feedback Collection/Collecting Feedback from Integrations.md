---
doc_id: doc_pb_int_001
schema_version: "1.0.0"
sidebar_position: 2
sidebar_label: Integration
title: "ProductBridge Third-Party Data Integrations & Auto-Ingestion Specification"
doc_type: "feature_specification"
last_updated: "2026-07-25"
domain: "product_management_saas"
target_system: "ProductBridge Platform"
target_audience: ["system_integrators", "software_engineers", "product_administrators", "product_managers"]
summary: "Technical guide for configuring third-party communication, support, and review platform integrations, defining auto-ingestion import rules, and mapping data attributes into ProductBridge."
keywords:
  - integrations
  - auto-ingestion
  - communication-channels
  - review-platforms
  - data-mapping
  - deduplication
---

# Collecting Feedback from Integrations

ProductBridge connects directly to third-party support platforms, messaging services, review sites, and call transcription tools.

Auto-ingestion runs continuously to import feedback from connected channels into the central inbox within minutes, deduplicating records and tagging each item with its source origin.

<<<<<<< HEAD
=======
This is an example in order to test if Vale is checking our PRs.
>>>>>>> 3814434e42a4c9da0084966b612b80a2d7d72da4

# Integration Pathways

ProductBridge supports the following native communication and public review connectors:

### Step 1: Communication & Support Channels

1. **Intercom:** Imports support conversations and notes tagged as feedback.
2. **Slack:** Collects feedback directly from designated Slack channels.
3. **Zendesk:** Imports support tickets tagged with specific feedback labels.
4. **Discord:** Captures feedback from configured Discord server channels.
5. **Freshdesk:** Imports support tickets filtered by category or priority.
6. **Gong:** Converts sales and customer call transcripts into structured feedback items.

### Step 2: Public Review Platforms

1. **TrustPilot:** Imports reviews published on your TrustPilot business profile.
2. **AppSumo:** Imports user reviews from your AppSumo listing.
3. **App Store:** Ingests iOS app store customer reviews.
4. **Play Store:** Ingests Android Google Play Store customer reviews.

# Auto-Ingestion Workflow Setup

1. **Connect Source Tools:** Navigate to **Connect Sources** in the sidebar and select the tool to connect. Follow the integration-specific authentication and authorization steps.
2. **Configure Import Rules:** Define filtering rules to determine which messages, tickets, or reviews import as feedback using tags, categories, channel rules, or AI-based detection.
3. **Automated Continuous Synchronization:** Once configured, feedback is imported continuously. Each item is tagged with its source (e.g., "via Intercom", "via TrustPilot") and linked to a user profile when possible.

# Imported Data Schema

The table below outlines the specific data fields captured during auto-ingestion:

| **Data Field** | **Schema Mapping & Description** |
| --- | --- |
| **Feedback Content** | Raw body text of the message, support ticket, or public review payload. |
| **Source Tag** | Origin identifier indicating the originating platform tool. |
| **User Identity** | User name, email address, or profile object linked when available. |
| **Metadata** | Timestamps, star ratings, tags, or categories extracted from the source tool. |

# Deduplication Protocol

All imported feedback passes through an automated deduplication pipeline. If a user submits similar feedback across multiple channels, ProductBridge aggregates the items together to present consolidated user demand without duplicate entries.

# Implementation Actions

1. Browse the complete index of available integration connectors under **Integrations**.
2. Learn how imported feedback items are processed and categorized by **Feedback Intelligence**.

