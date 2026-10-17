---
name: mapillary-token-baked-in
description: Since 1.2.2 the Mapillary token is hardcoded in mapillary.ts; .env is only an override
metadata: 
  node_type: memory
  type: project
  originSessionId: a067363c-ba38-4d38-8a74-8d9d95ca553e
  modified: 2026-08-08T13:25:58.837Z
---

As of v1.2.2 (versionCode 7, committed 2026-08-08), the Mapillary client token is hardcoded as `BUNDLED_TOKEN` in `src/services/mapillary.ts` because release builds repeatedly shipped without the `.env` value being inlined. `EXPO_PUBLIC_MAPILLARY_TOKEN` in `.env` still overrides it when set (`||` fallback). The token is public/client-side by design — EXPO_PUBLIC_* vars were always inlined into the shipped JS bundle anyway. Rotate at mapillary.com/dashboard/developers and update the constant if needed.

**Why:** "hard times with it" — missing-.env builds broke imagery loading in production.
**How to apply:** Don't "fix" the hardcoded token back to env-only; verify release bundles by grepping the Hermes bundle for the token id (see [[release-verification-recipe]]).
