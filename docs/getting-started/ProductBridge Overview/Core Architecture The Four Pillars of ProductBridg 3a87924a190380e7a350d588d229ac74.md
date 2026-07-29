---
id: index
title: Core Architecture
sidebar_position: 1
sidebar_label: Core Architecture
---

# Core Architecture: The Four Pillars of ProductBridge

ProductBridge is structured around four primary product management modules (pillars) that operate as a continuous feedback loop. These pillars manage the end-to-end lifecycle from initial customer feedback ingestion to feature release communication.

![image.png](/img/Corepillar.png)

## 1. Feedback Collection

**Feedback Collection** acts as the central intake layer for all customer feedback. It aggregates user inputs from public portals, embedded in-app widgets, and third-party communication tools into a unified inbox.

- **Primary Function:** Centralize unstructured and structured user inputs.
- **Supported Inputs:** Web portals, in-app triggers, email, Intercom, Slack, and Zendesk.

Explore configuration details for the Public Portal, In-App Widgets, and Automated Third-Party Ingestion.

## 2. Feedback Intelligence

**Feedback Intelligence** is the processing and analytical layer. It uses machine learning models to automatically parse raw feedback, assign category tags, analyze user sentiment, and detect emerging feature trends.

- **Primary Function:** Extract actionable quantitative and qualitative metrics from feedback data.
- **Key Components:**
    - **Ask AI:** Natural language query interface for customer feedback databases.
    - **Insights Engine:** Automated theme extraction and trend analysis.

Review automatically generated cluster analysis, sentiment trends, and topic summaries.

## 3. Product Roadmap

The **Product Roadmap** layer translates analytical insights into execution plans. Product teams can directly associate user feedback requests with specific roadmap initiatives, enabling data-backed prioritization.

- **Primary Function:** Link user demand directly to feature development boards.
- **Visibility Options:** Internal team views and public customer-facing views.

Learn how to create roadmap items, attach feedback records, and manage public vs. internal visibility.

## 4. Changelog

The **Changelog** layer handles release communication, closing the product management loop. It serves as a public ledger for new feature launches, product improvements, and bug fixes.

- **Primary Function:** Notify customers of product updates linked to their previously submitted feedback.
- **Primary Outcome:** Reduces support inquiry volumes and provides clear visibility into product development velocity.

Learn how to draft, schedule, and publish customer-facing release notes.

## How the Pillars Work Together

The four pillars are not isolated features — they form a continuous cycle. Feedback flows into Intelligence, which informs your Roadmap, which gets communicated through the Changelog, which drives new feedback. This loop ensures your product decisions are always grounded in what users actually need.