---
name: payments-via-poland
description: User is Kosovo-based; Google Play merchant/AdMob/Stripe blocked there — they plan to get paid via a friend in Poland
metadata:
  node_type: memory
  type: user
  originSessionId: 5287ce14-6e95-424d-bf36-8f2da33b4435
  modified: 2026-09-29T22:05:19.791Z
---

User (indie dev, Kosovo) plans Android-first apps, then iOS. Kosovo is not supported for Google Play merchant registration (verified on Google's supported-locations page 2026-09-29), and AdMob/Stripe/PayPal/Lemon Squeezy don't work there. User said (2026-09-30) a friend in Poland can receive payments for them, so treat Poland as the billing route.

**Why:** payment rails decided which app ideas were viable in the 2026-09-29 idea research.
**How to apply:** assume Play IAP/AdMob/Stripe are available via the Poland route, but flag account-ownership/tax/trust risks of running billing through a third person. Related: [[kosovo-admob-ban]]
