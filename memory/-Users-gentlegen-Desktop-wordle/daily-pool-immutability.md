---
name: daily-pool-immutability
description: FJALË daily pool is pinned at 62 words by SHA test — append-only rules for word catalog
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a376e78-fea1-4e3f-b833-76f2dbc19ef6
---

The daily puzzle draws from the first `DAILY_POOL_SIZE = 62` entries of `ANSWERS` in src/words.js. tests/words.test.js pins those 62 words with a SHA-256 digest (`PUBLISHED_CATALOG_SHA256`). New answer entries may only be APPENDED (index ≥ 62) — they feed practice and challenge modes without changing any past or future daily word or breaking existing challenge links.

**Why:** changing order/content of the first 62 silently changes which word every player gets on a given day, and clients update at different times (network-first SW), so the same date could show different words.

**How to apply:** never reorder/edit the first 62; growing the *daily* pool itself requires an epoch-based scheme (e.g. "from date X, pool = N") and is a user decision. See [[dev-environment-gotchas]].
