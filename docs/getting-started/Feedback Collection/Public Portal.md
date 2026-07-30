---
doc_id: doc_pb_portal_001
schema_version: "1.0.0"
sidebar_position: 1
sidebar_label: Public Portal
title: "ProductBridge Public Portal Configuration Guide"
doc_type: "feature_specification"
last_updated: "2026-07-25"
domain: "product_management_saas"
target_system: "ProductBridge Platform"
target_audience: ["system_integrators", "software_engineers", "product_administrators", "product_managers"]
summary: "Technical guide for configuring the ProductBridge Public Portal based on admin dashboard UI controls and provided specifications."
keywords:
  - public-portal
  - custom-domain
  - cname-configuration
  - feedback-collection
  - portal-customization
---

# Public Portal


Learn how to set up and customize the ProductBridge Public Portal such as a branded, public-facing page where users submit feedback, vote on requests, and engage with your product roadmap. 

Let's test it.

The **ProductBridge Public Portal** (`ProductBridge.PublicPortal`) is a dedicated, branded page where users can submit feedback, vote on existing requests, leave comments, and view your product roadmap. 

# Your Public Feedback Hub

The Public Portal is a dedicated, branded page where users can submit feedback, vote on existing requests, and leave comments. It gives your users a transparent space to share ideas and see what others request regarding building community and trust around your product.

:::tip Single Sign-On & Authentication

Users sign in to post, vote, and comment—with email and password, Google, or GitHub. You can also configure an [SSO redirect](../configuration-and-settings/sso.md) so your own users are logged in automatically.

:::

# Set Up Your Portal

1. **Find Your Portal**

Your portal is on by default at **`https://{your-subdomain}.productbridge.io`**.

Configure it under **Settings → Organization → Public Portal**. To take the portal offline, use the **Disable Public Portal** toggle under **Portal access**.

**Customize Appearance**

Configure your portal to match your brand:

- **Visible tabs**: Toggle the Feedback, Roadmap, and Changelog tabs individually, and pick the default landing tab
- **Brand colors**: Set colors for light and dark mode, plus the default theme
- **Custom domain** — Optionally map your own domain (e.g., **`feedback.yourproduct.com`**) via a CNAME record under **Settings → Custom Domain**

Your logo is managed under **Settings → Organization → Brand Settings**.

1. **Configure Categories**

Set up feedback categories so users can tag their submissions (e.g., Feature Request, Bug Report, Improvement). Categories help you organize and filter feedback in your inbox.

1. **Share with Users**

Embed the portal link in your app, website footer, email signatures, or help docs. Users land on the portal and can submit feedback immediately.

# Portal Features

### Feedback Submission

Signed-in users can submit new feedback with a title, description, and category. Optionally, they can attach screenshots or files to provide more context. Signed-in (or allowed guest) users submit feedback with a title, description, category, and optional file/screenshot attachments.

### Voting

Voting lets your community prioritize requests organically. Users can upvote existing feedback items, and the most-requested features rise to the top automatically. Voting is one of the most powerful feedback signals. A post with 50 votes tells you more than 50 individual submissions saying the same thing.

### **Comments and Discussion**

Users can comment on existing feedback posts to add context, share use cases, or +1 a request with additional detail. Comments create a conversation around each feedback item.

### Roadmap and Changelog Tabs

Optionally expose your [**Product Roadmap**](https://docs.productbridge.io/core-concepts/product-roadmap) and [**Changelog**](https://docs.productbridge.io/core-concepts/changelog) as portal tabs. Users can see what is planned, in progress, completed, and shipped — reducing "when will this ship?" questions and building transparency. Set which tab visitors land on first with the default landing tab setting.

### Status Updates

When a feedback post's status changes (e.g., from "Under Review" to "Planned"), users who voted or commented are notified. This closes the feedback loop and shows users their input drives real product decisions.

### Analytics

Track visitor behavior and measure portal engagement:  
• **Google Analytics 4:** Add GA4 tracking to all portal pages.  
• **Google Tag Manager:** Add your GTM container to all portal pages.  
****

### Support

Add live chat widgets directly to your portal pages:  
• **Intercom:** Add Intercom live chat widget to your portal pages.

# Customization Options

Configure these under **Settings → Organization → Public Portal**:

| **Setting** | **Description** |
| --- | --- |
| Visible tabs | Show or hide the Feedback, Roadmap, and Changelog tabs individually |
| Default landing tab | Which tab visitors see first |
| Brand colors | Portal colors for light and dark mode |
| Default theme | Whether the portal defaults to light or dark |
| Feedback collection | Toggles for the feedback form and feedback agent |
| Analytics | Portal analytics settings |
| Support | Support contact settings for your portal |

Your logo lives under **Settings → Organization → Brand Settings**, and custom domains are mapped via CNAME under **Settings → Organization → Custom Domain**. To let your own users sign in automatically, configure [**SSO**](https://docs.productbridge.io/settings/sso).

:::Note

The public portal is fully responsive and works on mobile, tablet, and desktop browsers.

:::

import DocCardList from '@theme/DocCardList';

## Next Steps

<DocCardList />