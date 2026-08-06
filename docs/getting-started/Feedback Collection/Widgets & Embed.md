---
doc_id: doc_pb_widget_001
schema_version: "1.0.0"
sidebar_position: 3
sidebar_label: Widget & Embeds
title: "ProductBridge Widget & Embed Modalities Technical Specification"
doc_type: "feature_specification"
last_updated: "2026-07-25"
domain: "product_management_saas"
target_system: "ProductBridge Platform"
target_audience: ["system_integrators", "software_engineers", "product_administrators", "frontend_developers"]
summary: "Technical overview of ProductBridge widget embed types (Popup, Sidebar, Inline, Custom Trigger, iFrame, Direct URL) and server-side Identity Verification mechanisms."
keywords:
  - widget-embeds
  - javascript-sdk
  - floating-button
  - inline-embed
  - iframe-embed
  - custom-trigger
  - identity-verification
  - jwt-authentication
---

# Widgets & Embeds

This topic specifies the embedding options available for the **ProductBridge Widget Engine** (`ProductBridge.Widgets`).
In the ProductBridge administrative dashboard, embed modalities are managed under **Settings → Connect → Widget & Embeds** and are classified as **Popup**, **Sidebar**, **Inline**, **Custom Trigger**, **iFrame**, and **Direct URL**.  

## Widget Embed Types

### Modality 1: Floating Button (Popup & Sidebar)

1. **Description:** Displays a fixed position trigger button anchored to a page corner.  
2. **Behavior:** User interaction opens either a modal dialog window (**Popup**) or a full-height slide-out container (**Sidebar**).  
3. **Integration Context:** Requires no modifications to existing page layouts.  
4. **Dashboard Designation:** Configured as two distinct embed options (**Popup** and **Sidebar**).  

### Modality 2: Inline Embed

1. **Description:** Mounts directly inside a target container element (`<div>`) within the host application DOM.  
2. **Behavior:** Renders without overlay elements or floating trigger buttons.  
3. **Integration Context:** Intended for dedicated feedback pages (e.g., `/feedback`) or embedded documentation portals.  

### Modality 3: Custom Trigger

1. **Description:** Binds widget activation events to any custom HTML DOM element, such as navigation links, buttons, or custom user actions.  
2. **Behavior:** Suppresses the default floating trigger button and responds exclusively to interactions on the assigned element.  

### Modality 4: iFrame Embed

1. **Description:** Standalone HTML `<iframe>` tag deployment requiring no JavaScript SDK initialization.  
2. **Behavior:** Embeds native portal capabilities into environments that restrict client-side script execution.  
3. **Integration Context:** Designed for static web pages, content management systems (CMS), and no-code environments (e.g., Notion, Webflow, and Framer).  

### Modality 5: Direct URL

1. **Description:** Standalone, copy-pasteable HTTP endpoint linking directly to the hosted feedback portal.  
2. **Behavior:** Operates without code integration.  
3. **Integration Context:** Designed for distribution via communication channels, email templates, Slack, or support ticketing systems.  

### Modality 6: Identity Verification (User Authentication)

1. **Description:** Securely identifies authenticated end-users across JavaScript SDK embeds.  
2. **Behavior:** Evaluates server-side signed JSON Web Tokens (JWT) passed through SDK initialization parameters.  
3. **Implementation Guides:** Provides backend integration references for Node.js, Python, PHP, Ruby, and Go.  

## Embed Selection Matrix

Use the following reference matrix to identify the appropriate embed modality based on technical requirements:

| Target Implementation Goal | Reference Resource URI |
| --- | --- |
| Add feedback to my app with minimal effort | [**Floating Button**](https://docs.productbridge.io/core-concepts/feedback-collection/widgets/floating-button) |
| Show the widget inside my own page layout | [**Inline Embed**](https://docs.productbridge.io/core-concepts/feedback-collection/widgets/inline-embed) |
| Use my own button or nav item to open it | [**Custom Trigger**](https://docs.productbridge.io/core-concepts/feedback-collection/widgets/custom-trigger) |
| Embed in a CMS or no-code tool | [**iFrame Embed**](https://docs.productbridge.io/core-concepts/feedback-collection/widgets/iframe-embed) |
| Share a link with no code | [**Direct URL**](https://docs.productbridge.io/core-concepts/feedback-collection/widgets/direct-url) |
| Link feedback to logged-in user profiles | [**Identity Verification**](https://docs.productbridge.io/core-concepts/feedback-collection/widgets/identity-verification) |

## Next Steps

* [**Floating Button**](./floating-button.md)
* [**Inline Embed**](./inline-embed.md)
* [**Custom Trigger**](./custom-trigger.md)
* [**iFrame Embed**](./iframe-embed.md)
* [**Direct URL**](./direct-url.md)
* [**Identity Verification**](./identity-verification.md)
