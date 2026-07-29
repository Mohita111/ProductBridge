---
id: Faqs
title: FAQs 
sidebar_label: FAQs
---


## Custom SMTP & Email Delivery
--------------------------------

### **Q: Will my users miss important emails if my custom SMTP server goes down?**

**A:** No. ProductBridge uses an automatic two-tier fallback system. If your custom SMTP server fails, encounters a timeout, or has invalid credentials, ProductBridge immediately routes the email through our default system mailer. Your notifications, comment alerts, and announcements will always be delivered.

### **Q: Why is my Google Workspace password being rejected during SMTP setup?**

**A:** Google Workspace disables standard account password logins for third-party SMTP connections. To connect Gmail or Google Workspace:

1.  Turn on **2-Step Verification** on your Google Account.
    
2.  Generate a dedicated **App Password** (under Google Account Security $\\rightarrow$ 2-Step Verification $\\rightarrow$ App passwords).
    
3.  Paste that 16-character App Password into ProductBridge instead of your normal password.
    

### **Q: Will setting up Custom SMTP improve my email deliverability?**

**A:** Yes, significantly. Sending emails from your own domain (e.g., updates@yourcompany.com) via your verified SMTP provider (Amazon SES, SendGrid, Postmark) builds domain authority and reduces the likelihood of notifications landing in your customers' spam or promotions folders.

### **Q: Is my SMTP password secure in ProductBridge?**

**A:** Yes. Your SMTP password or API token is fully encrypted at rest using industry-standard encryption algorithms and decrypted only at the exact moment an email is dispatched. It is never logged, exposed in client API calls, or displayed in the user interface after saving.

## SEO & Board Visibility
--------------------------

### **Q: If I turn Search Engine Indexing ON, will search engines index my private or internal boards?**

**A:** No. Search engine indexing applies **only** to boards set to **Public**. Internal boards (team members only) and Segmented boards (specific user segments) require authentication. Google crawlers cannot bypass authentication, so your private feedback remains 100% secure regardless of your SEO settings.

### **Q: What happens to my Google search rankings if I turn indexing OFF?**

**A:** Turning indexing off inserts a  tag into your portal pages. Search engines will gradually remove your portal pages from their search results. Turn this off if you are running a private beta, seeding initial internal content, or operating an internal-only feedback hub.

### **Q: Can I set visibility on individual posts or comments?**

**A:** No. Visibility is inherited strictly from the parent board. Every post and comment created within a specific board inherits that board's access level (Public, Internal, or Segmented Users). If you need private discussions, create a dedicated Internal board.

### **Q: Why isn't my social media preview image (Open Graph image) showing up when I share my portal link?**

**A:** Social platforms (LinkedIn, Twitter/X, Slack) cache preview metadata. If you recently updated your Open Graph image, try the following:

1.  Ensure your uploaded image recommended aspect ratio is **1200×630px**.
    
2.  Run your portal URL through a preview tool like [OpenGraph.xyz](https://www.opengraph.xyz/) or the official Twitter/LinkedIn link debuggers to force platforms to refresh their cache.
    

### **Q: How do user segments work with board visibility?**

**A:** User segments allow you to gate specific boards to matching logged-in end-users (e.g., Beta Testers, Enterprise Tier, EU Customers). If a user does not match the active segment criteria attached to a board, the board will be hidden from their view entirely.

Here is an additional set of advanced FAQs covering edge cases, troubleshooting scenarios, and security considerations that users and system administrators frequently run into.

## Advanced SMTP & Mail Delivery FAQs
--------------------------------------

### **Q: What is the difference between Port 587 and Port 465, and which one should I choose?**

**A:**

*   **Port 587 (Recommended):** Uses **STARTTLS**. The connection starts as plain text and immediately upgrades to an encrypted TLS connection. This is the standard modern port supported by virtually all SMTP providers.
    
*   **Port 465:** Uses **Implicit SSL/TLS**. The connection is encrypted from the very first byte.
    

If your provider supports both, select **Port 587**.

### **Q: I received a "Test Connection Failed" error. What should I check first?**

**A:** Connection failures are usually caused by one of three common issues:

1.  **Incorrect Credentials:** Double-check your username and password/API key for typos or extra trailing spaces.
    
2.  **IP Whitelisting / Firewall:** If your SMTP provider requires IP whitelisting (like Amazon SES or internal mail servers), make sure it accepts connections from external cloud sources.
    
3.  **Authentication Type:** Ensure you are using an **App Password** or **API Token** if your provider enforces multi-factor authentication (MFA) on your primary account.
    

### **Q: Can I use my custom SMTP for specific email types only (e.g., only announcements, but not transactional password resets)?**

**A:** No. When Custom SMTP is active, **all outbound emails** originating from ProductBridge (changelog updates, post notifications, status alerts, invitations, and confirmation emails) route through your SMTP server to maintain consistent domain branding.

## Advanced Visibility, SEO & User Access FAQs
-----------------------------------------------

### **Q: What happens if a search engine already indexed my board before I set it to "Internal" or turned Indexing "OFF"?**

**A:** Once you change a board to **Internal** or disable portal indexing:

*   Non-authenticated users clicking the old search result link will be redirected to a login prompt.
    
*   Search crawlers will receive a noindex tag or a 403 Forbidden response on their next crawl, causing them to drop the page from search results over time.
    
*   To speed up removal from Google immediately, submit a **Removal Request** inside Google Search Console.
    

### **Q: Can users in a "Segmented" board see who else is viewing or commenting on the board?**

**A:** Users can see public display names and comments left by other users _within that same segment_. However, unauthenticated visitors or users outside that segment cannot see the board, its posts, or the user profiles interacting on it.

### **Q: Does ProductBridge support custom domains alongside Custom SMTP?**

**A:** Yes. Connecting your custom SMTP server ensures your emails come from your domain (e.g., feedback@yourdomain.com), while configuring your CNAME records routes portal traffic to your custom Web URL (e.g., roadmap.yourdomain.com). Combining both creates a completely white-labeled customer portal experience.

### **Q: Is there a difference between "Who can see posts" and "Who can create posts"?**

**A:** Yes! They control two distinct permissions on Feedback boards:

*   **Who can see posts:** Controls visibility (Public, Internal, Segmented Users).
    
*   **Who can create posts:** Controls submission rights. For instance, you can set a board's visibility to **Public** (anyone can read) while setting creation rights to **Authenticated Users Only** (prevents anonymous spam submissions).
    

### Q: Can I assign custom permission sets to team members?

**A:* No. ProductBridge relies on four fixed system roles: Owner, Admin, Editor, and Viewer. Custom role definitions and per-board or per-project permission scoping are currently unsupported.

### Q: What happens to historical posts and comments when a team member is permanently removed?

**A:** When a team member is removed, their access is revoked immediately, but all historical data, including created posts, comments, and audit logs, is preserved with original author attribution intact.

### Q: Can I resend a pending workspace invitation if it expires? 

**A:** No direct resend action exists. Active or expired pending invitations must be canceled first under Settings -> Team Members -> Pending Invites, after which a fresh invitation can be issued.

## Single Sign-On (SSO) & Widget Auth

### Q: Will enabling Disable ProductBridge Login affect my internal workspace admins?

**A:** Enabling Disable ProductBridge Login hides the native login form on the public portal. Make sure your external SSO flow is fully verified using the Test Redirect Flow option before enabling this setting to avoid lockouts.

### Question: Is my Widget API Secret safe when generating JWTs? 

**A:* Yes. JWT generation occurs strictly on your application server using your private Widget API Secret. The secret is never sent to or stored in client-side code.

## AI Credits & Billing

### Q: Do unused monthly AI credits roll over to the next billing cycle?

**A:** No. Monthly credit allocations expire every 30 days and do not roll over. However, purchased top-up credit packs never expire and are only deducted after your monthly allocation is completely exhausted.

### Q: What happens when my account runs out of AI credits?

**A:** AI-driven features (Ask AI, AI Search, AI Writer, and automated feedback parsing) pause immediately and show an Out of AI credits prompt. Core application features like feedback boards, roadmaps, and portals continue working normally.

## Roadmap & Changelog

### Q: How does ProductBridge notify users when a requested feature is completed?

**A:** When a changelog entry or roadmap status update is linked to feedback items, ProductBridge automatically sends email or in-app notifications to all end-users who originally submitted or upvoted that feedback.

### Q: Can I retain my parameter inputs if I switch prioritization frameworks?

**A:** Yes. ProductBridge stores parameter inputs independently for all four supported frameworks (RICE, ICE, Impact/Effort, MoSCoW), allowing non-destructive switching between frameworks at any time.

### Q: What happens if an incoming integration ticket matches an existing public feedback post while the AI Moderation Queue is disabled? 

**A:** When the AI Moderation Queue is disabled, the ProductBridge AI pipeline automatically executes an auto-merge operation, linking the new ticket data directly to the existing feedback thread without requiring manual human intervention.

### Q: Can I enable post moderation for direct web users while allowing integration posts to bypass review? 

**A:** Yes. Direct web submissions are controlled independently by the Require approval for posts setting, while integration submissions are governed by the Enable AI moderation queue setting. These two controls operate completely independently.

## Data Privacy & Anonymization:

### Q: If Hide user identities is enabled, can workspace administrators still identify who submitted a specific piece of feedback?

**A:** Yes. User identity masking applies strictly to the public-facing portal. Internal administrators maintain full access to real names, email addresses, and submission histories within the ProductBridge Admin Dashboard to enable support outreach.

### Q: Does enabling user anonymization alter historical data retroactively on the public portal? 

**A:** Yes. Toggling Hide user identities to On immediately replaces all historical and future public display names and avatars with randomized placeholders across all public portal threads.

## Widget Security & Identity:

### Q: What happens if an identify call is made using an email address that does not exist while Identify Mode is set to Update Only?

**A:** The identify call is rejected by ProductBridge. The widget will not create a new user profile, and any feedback submission attempt from that unverified user will be suppressed or blocked.

### Q: Why are identify calls failing after enabling Require user hash for identify calls?

**A:** The standard ProductBridge Widget SDK does not automatically calculate or dispatch the user\_hash HMAC parameter. Enabling this setting requires a custom backend integration using the verify-identity API to calculate and supply the user\_hash directly.

## Roadmap & Prioritization Mechanics:

### Q: What score is assigned to a roadmap item if a team member forgets to fill in one of the RICE framework parameters?

**A:** Any roadmap item with incomplete or missing parameter fields in the active prioritization framework automatically receives a calculated score of 0 and is sorted to the bottom of the table.

### Q: Does changing the active prioritization framework delete parameter values entered under a previous framework?

**A:** No. ProductBridge retains entered parameters independently for each framework. Switching between RICE, ICE, Impact/Effort, and MoSCoW preserves all previously entered data.