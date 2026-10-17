---
name: rowflare-to-blockrow-rename
description: 2026-07-27 renamed Rowflare → Blockrow (com.blockrow.game); storage now falls back through @rowflare and @block_blaster prefixes
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T19:11:59.424Z
---

2026-07-27: the app was renamed **Rowflare → Blockrow**, done before any Play
publication so the package ID change was free. The user picked the one-word form
over "Block Row" / "Block Blaster"; **"Block Blaster" was rejected on my advice**
because it sits close to the trademarked *Block Blast* (Hungry Studio) and Play
enforcement against near-clones of it is aggressive.

- `com.rowflare.game` → `com.blockrow.game` (ios bundle + android package),
  slug/scheme `blockrow`, wordmark split `ROW|FLARE` → `BLOCK|ROW` in
  `src/config/product.ts`.
- **Third name this app has had.** Storage prefix history is now
  `@block_blaster` → `@rowflare` → `@blockrow`. `storageCore.ts` reads through a
  `LEGACY_PREFIXES` list **newest-first**, so an older prefix only supplies a
  value when every newer one is absent — otherwise a stale Block Blaster score
  would clobber a newer Rowflare one. Any future rename must append to that list,
  not replace it.
- The keystore is still `credentials/rowflare-upload.keystore` with `ROWFLARE_*`
  keys in `keystore.properties`. Names only — keystore identity is independent of
  the package name, so it does not need regenerating. See
  [[release-keystore-setup]].

Verified at APK level (aapt2 on the release build): `package=com.blockrow.game`,
`application-label=Blockrow`. See [[admob-migration]] for the ad-stack change
made in the same session.
