---
doc_id: doc_pb_fi_001
schema_version: "1.0.0"
sidebar_position: 2
sidebar_label: Feedback Collection
title: "ProductBridge Feedback Intelligence Technical Specification"
doc_type: "feature_specification"
last_updated: "2026-07-27"
domain: "product_management_saas"
target_system: "ProductBridge Platform"
target_audience: ["system_integrators", "software_engineers", "product_administrators", "product_managers"]
summary: "Technical architecture specification for ProductBridge Feedback Intelligence, detailing automated categorization, sentiment analysis, trend detection, deduplication, and roadmap linking."
keywords:
  - feedback-intelligence
  - sentiment-analysis
  - trend-detection
  - deduplication
  - ask-ai
  - insight
---
# Feedback Collection

Learn how ProductBridge collects user feedback from three sources such as public portal, in-app widgets, and automatic ingestion from third-party tools.

# **One Inbox for All Feedback**

ProductBridge centralizes feedback from every channel into a single, searchable inbox. No matter where your users share their thoughts — a public page, your app, or a support tool — everything arrives in one place, ready for analysis.

You configure the channels that fit your workflow, and ProductBridge handles the rest.

# **What Happens Next**

Once feedback is collected from any channel, ProductBridge passes it to [**Feedback Intelligence**](https://docs.productbridge.io/core-concepts/feedback-intelligence) for automated analysis. Every item is categorized, scored for sentiment, and linked to emerging trends — so you can move from raw input to actionable insight without manual triage.

All feedback sources flow into the same unified inbox. You can filter by source, category, sentiment, or user segment to focus on what matters most.

### Explore Collection Channels

* [**Public Portal**](./public-portal.md)
* [**Collecting Feedback from Integrations**](./collecting-feedback-from-integrations.md)
* [**Widgets & Embeds**](./widgets-and-embeds/index.md)