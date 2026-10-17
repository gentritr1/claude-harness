---
name: env-fail-closed-ads
description: Local .env is missing banner ad unit + privacy/support URLs; release fails closed
metadata: 
  node_type: memory
  type: project
  originSessionId: 2051cf29-c6f2-47e3-8fbd-76df141b5684
  modified: 2026-09-02T15:07:51.675Z
---

Updated 2026-09-02. The **banner unit is no longer an env var** — at the user's request it ships as a source constant `ANDROID_BANNER_AD_UNIT_ID` in `src/config/ads.ts` (`ca-app-pub-9813131856455133/1393454168`), with the env var kept as an optional override and `__DEV__` still forced to Google's test unit. `scripts/release-preflight.mjs` validates that constant by reading the file (regex), so the gate still rejects a test/malformed unit.

Still MISSING in local `.env` as of 2026-09-02: `EXPO_PUBLIC_PRIVACY_POLICY_URL` and `EXPO_PUBLIC_SUPPORT_URL` (APP_ID, REWARDED, INTERSTITIAL are present and correctly shaped). These fail closed — product URLs become null, so in-app privacy/support links do nothing, and Play requires a privacy URL on the listing.

**Why:** EXPO_PUBLIC_* values are inlined into the JS bundle at build time — fixing .env after building does nothing.

**How to apply:** Before `gradlew bundleRelease` for a real store build, get the banner unit ID + URLs from the user, or explicitly note the gap in release notes.
