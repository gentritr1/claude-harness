---
name: blockrow-to-block-destroy-rename
description: 2026-07-27 store name is Block Destroy but package is locked to com.blockrow.game; only the display name may change from now on
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T20:37:26.084Z
---

2026-07-27, same day as [[rowflare-to-blockrow-rename]]: renamed again to
**Block Destroy** — but this time the Play listing had already been created, so
the package ID is **permanently `com.blockrow.game`**. The user confirmed that
value directly from Play Console before anything was rebuilt.

**Rule from here on: change the display name only.** Renamed:
`app.json` name + web name/shortName, `PRODUCT.name`, the wordmark, docs.
Deliberately NOT renamed (invisible to players, and churn/risk for nothing):
`slug`, `scheme`, `com.blockrow.game`, the `@blockrow` storage prefix, the
`BlockrowAdMobAds` native module, and `credentials/rowflare-upload.keystore`.

The rename was done with `perl -pi -e 's/\bBlockrow\b/Block Destroy/g'` — the
word boundary is what protects `BlockrowAdMobAds` (no boundary before `A`) and
lowercase `blockrow` identifiers. A naive case-insensitive sed would have broken
the native module name and the storage prefix.

**Visual regression this caused, caught only by screenshot:** "BLOCKDESTROY" is
12 characters and **wrapped mid-word to "BLOCKDEST / ROY"** on a 320pt viewport.
tsc and 40 passing tests were all green. Fixed by adding
`PRODUCT.wordmarkStacked`, which puts BLOCK over DESTROY in the home and splash
lockups (the in-game header stays inline at a reduced 16/13pt). Verified by
screenshot at 320px before and after.

→ **Detection rule: any product-name change must be re-screenshotted at 320pt.**
A longer name is a layout change, not a string change. Same class as the
existing scar that visual work needs eyeballs, now with a concrete trigger.
