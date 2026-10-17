---
name: save-additive-schema-safety
description: Adding any SaveModel field can silently wipe all existing saves via the checksum gate — how to evolve the schema safely
metadata: 
  node_type: memory
  type: project
  originSessionId: 03b57214-d236-47ce-a59d-f567125c1022
---

Planet Drop's `SaveService.Load` originally validated the SHA-256 checksum BEFORE the schema-version check. The stored checksum is computed over the serialized `SaveModel`, so adding ANY field (e.g. the `themes` section in Chunk 5a) makes every existing save's stored checksum mismatch the re-serialized model → `Defaults()` → silent data wipe (coins/progress lost), and the migration never even ran.

Fixed (commit `afa1d9e`): only checksum-validate when `schemaVersion == CurrentSchemaVersion`; older-schema saves skip the checksum and route straight to the additive `Migration` (preserves data + `Normalize()`s in new defaults). `Save()` re-checksums on the next write. Tamper detection is therefore enforced only for current-schema saves, which is the right trade.

**RECURRED 2026-07-13 (playability-audit delegate):** an agent added `settings.reduceMotion` to SaveModel WITHOUT bumping `CurrentSchemaVersion` (still 3) — every existing v3 save would checksum-mismatch on next Load() → full wipe. Its new tests (roundtrip + defaults) all passed while missing the failing path, and its report claimed "compiled cleanly" as evidence. Caught in review by checking this memory. Detection rule: ANY diff line adding a field inside SaveModel classes → immediately grep `CurrentSchemaVersion` for a bump in the same diff + demand a full-Load() legacy-file test for the PREVIOUS version. Fixed same day: bump to 4 (no registered migration needed — Migration's additive-defaults branch handles unregistered old versions) + `Load_V3FileMissingReduceMotion_PreservesDataDespiteStaleChecksum`.

When adding a SaveModel field in future: bump `CurrentSchemaVersion`, give the field a sensible default + handle it in `Normalize()`, and confirm `SaveServiceTests.Load_LegacyFileMissingNewFields_PreservesDataDespiteStaleChecksum` still passes — it writes a real legacy themes-less JSON with a stale checksum through the FULL `Load()` path. Never test save migration only via `Migration.Migrate` in isolation; that bypasses the checksum gate that actually fails. See [[reviewing-codex-output]].
