---
doc_id: doc_pb_qs_001
schema_version: "1.0.0"
title: "ProductBridge Platform Onboarding and Integration Specification"
sidebar_position: 2
sidebar_label: Quickstart
doc_type: "procedure_guide"
last_updated: "2026-07-25"
domain: "product_management_saas"
target_system: "ProductBridge Platform"
target_audience: ["system_integrators", "software_engineers", "product_administrators"]
summary: "Technical procedure for initial account provision, workspace onboarding, feedback ingestion pathway initialization (Public Portal, In-App SDK Widget, Third-Party Integrations), and dashboard navigation."
keywords:

- onboarding
- account-setup
- feedback-ingestion
- widget-sdk
- integration-api
---

# Quick Start: ProductBridge Onboarding & Setup

This guide walks you through setting up your ProductBridge account, completing initial workspace onboarding, configuring feedback channels, and navigating the admin dashboard.

## **Prerequisites**

Before starting the setup process, ensure you meet the following requirements:

• **Web Browser:** A modern browser (Chrome, Firefox, Safari, or Edge) with JavaScript enabled.

• **Email Address:** A valid work email address for account creation and domain verification.

• **Deployment Access:** Administrative access to your web application HTML if embedding the widget SDK.

:::note

ProductBridge is a cloud-native SaaS application. No local software installation is required.
:::

## **Account Registration & Onboarding**

### **Register an Account:**

Navigate to [app.productbridge.io/signup](https://app.productbridge.io/signup), enter your full name, work email address, and a strong password, then click **Create Account**.


### **Verify Email Address:**

Open the verification link sent to your email address. Upon successful confirmation, log into the ProductBridge Dashboard.


### **Complete the Automated Onboarding Workflow:**

Complete the initial workspace setup wizard:

1. **Enter Domain URL:** Input your primary organization domain (e.g., `company.com`).
2. **Verify Brand Details:** Review the auto-populated brand metadata (scraped via URL enrichment) and confirm details.
3. **Select Default Boards:** Choose the initial feedback board templates for your account.
4. **Initialize Metadata Scanning:** Confirm selection to allow ProductBridge to personalize default feedback categories.

Upon completion, you will be directed to the primary **Feedback Board** list view.

## **Configure Feedback Ingestion Channels**

Configure how customer inputs will flow into your centralized inbox.

- **Configure Feedback Sources:**
Select and enable one or more of the following ingestion pathways
- **Public Portal:** Hosted web portal for open user submissions and feature voting (enabled by default).
- **In-App Widget:** Embedded JavaScript SDK for direct feedback submission within your SaaS product.
- **Third-Party Integrations:** Automated synchronization with Intercom, Slack, Zendesk, or Jira.

<aside>
💡

Start with the Public Portal, which is on by default and gives you a shareable feedback page immediately.

</aside>

## Dashboard Architecture Overview

The ProductBridge Admin Console is divided into three functional areas:

- **Modules**
    - **Feedback:** Central inbox containing all aggregated user requests and submissions.
    - **Roadmap:** Feature prioritization boards linked to user demand metrics.
    - **Changelog:** Public release notes editor and publishing platform.
    - **Moderation:** Triage, filter, and approve incoming user posts.
- **Intelligence**
    - **Analytics:** Quantitative reports on feedback volume, velocity, and user sentiment.
    - **Insights:** Automated topic clustering, trend detection, and recurring theme extraction.
    - **Ask AI:** Natural language query interface for search and retrieval across feedback databases.
- **Workspace**
    - **Users:** Manage team member roles, permissions, and seat allocations.
    - **Settings:** Configure organization metadata, custom domains, and security.
    - **Connect Sources:** Manage API connections and third-party data pipelines.

## Next Steps

1. Configure automated sentiment tracking and natural language search capabilities.
2. Set up third-party integrations with support suites and issue tracking boards.