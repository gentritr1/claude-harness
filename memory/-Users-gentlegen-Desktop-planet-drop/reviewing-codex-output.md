---
name: reviewing-codex-output
description: "How to review Codex's Unity work — verify claimed fixes/tests hit the REAL failing path, not the unit it touched"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 03b57214-d236-47ce-a59d-f567125c1022
---

Codex (the coder in this workflow, see [[planet-drop-orchestrator-workflow]]) reported a fix "done, tests pass" that did NOT work: in Chunk 5a it "fixed the save-wipe" and added a test, but the test exercised `Migration.Migrate` in isolation while the real wipe happened earlier, in `SaveService.Load`'s checksum gate — so the test passed and saves still wiped on real load (see [[save-additive-schema-safety]]).

**Why:** Codex's batchmode compile/test often can't fully run (Unity licensing reconnect), and it tends to test the unit it changed rather than the end-to-end path that fails. "Compile-clean + tests pass" is NOT runtime verification.

**How to apply:**
- Trace the ACTUAL runtime/failing path, not just the changed function. For save/load bugs follow `Load()` start-to-finish including checksum + version gates; for visuals, reason about render order/bloom/material sharing.
- Confirm any added test enters through that real path (e.g. a file on disk through `Load()`), not an isolated helper.
- Personally verify hand-authored Unity YAML cross-references: `.meta`/`.asset` guids and sprite `fileID: 21300000` must resolve (grep the guids against the source `.meta`s). Codex CAN author `.meta`/`.asset` and Resources-load ScriptableObjects to avoid manual Unity wiring — but one wrong guid silently yields a missing reference.
- Always have the user runtime-verify save-touching and visual changes from Boot.unity BEFORE committing; only commit after that. The per-chunk review → user-verify → commit cadence is what caught these.
