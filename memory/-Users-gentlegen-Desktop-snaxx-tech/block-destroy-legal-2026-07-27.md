---
name: block-destroy-legal-2026-07-27
description: "App renamed Rowflare→Blockrow→Block Blaster→Block Destroy; AdMob-only, canonical /<slug>/<kind> URLs, old slugs aliased, package name stays com.blockrow.game"
metadata: 
  node_type: memory
  type: project
  originSessionId: b62b1de2-f7a8-4456-9ed0-e02fe8e3cc49
  modified: 2026-07-27T21:18:41.157Z
---

2026-07-27: the Android game is now **Block Destroy** (publisher Snaxxtech) — an offline block puzzle. It shipped previously as Rowflare, then Blockrow, then Block Blaster. **Package name is `com.blockrow.game` and is deliberately NOT "corrected"** — user instruction, treat any impulse to fix it as a bug.

Product facts stated in the live policy (user-supplied, not code-verified): Google AdMob is the only ad provider, consent via Google UMP, re-openable from "Ad Privacy Choices" in the in-app Privacy & Support screen; ads are rewarded-only and user-initiated (a "Watch Ad" tap for one extra helper use), Android-only; no account/sign-in/cloud save/backend; local data = active run, high score, best combo, sound preference, tutorial status; general audience.

Site structure in `src/legal/content.ts` + `src/App.tsx`:
- Canonical URLs are `/<slug>/privacy|terms|support`; the older `/privacy/<slug>` and `/terms/<slug>` routes are kept. `LEGACY_SLUGS` maps rowflare, blockrow, block-blaster, blockblaster → block-destroy, so every previously published URL still resolves. **Never delete these aliases** — Play Console/AdMob may point at any of them.
- `buildPrivacy`/`buildTerms` are **shared with Arrows**, which still ships Unity Ads. Per-app switches live on `LegalProfile`: `adProvider`, `rewardedAdsOnly`, `noBackend`, `generalAudience`, `privacyEmail`. Privacy section titles are unnumbered and numbered by `numberSections()`.
- `AppLegal.support` is optional; an app without it 404s on `/<slug>/support` (verified for Arrows). Contact card picks `privacyEmail` / `supportEmail` / `contactEmail` per kind.
- Emails: privacy@snaxxtech.com (privacy), techsnaxx@gmail.com (studio + support). Support response time stated as 2–3 business days — **assumed, not user-confirmed**.

**Why:** these pages are the Play Console privacy/support URLs, so a wrong or stale claim is a store-review and Data Safety risk, not a cosmetic issue.

**How to apply:** before submitting, re-verify the release APK bundles only the Google Mobile Ads SDK — the text asserts AdMob is the *only* provider. See [[snaxxtech-hosting-and-app-ads]] for the app-ads.txt setup and the apex-vs-www redirect. See [[apps-contain-unity-ads]] for the Arrows contrast.
