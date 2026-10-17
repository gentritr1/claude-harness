---
name: playerstore-wipes-profile-on-slow-read
description: playerStore data-loss bug (a slow cold read wiped the profile) — fixed 2026-09-09 (edf2b36, then c122551 profile writer); tests/player-store.test.ts Case 1 guards it
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-09T18:05:34.760Z
---

`src/store/playerStore.ts` destroys real player data on any slow cold storage read.
**Reproduced 2026-09-09** against the unmodified file with only `AsyncStorage` shimmed
to be slower than its own timeout:

```
ON DISK BEFORE: { walkthroughSeen: true, gamesCompleted: 47, lastReviewPromptAt: 1756000000000 }
IN MEMORY after timeout: ready = true | gamesCompleted = 0 | lastReviewPromptAt = null
ON DISK AFTER one game:  { walkthroughSeen: true, gamesCompleted: 1, lastReviewPromptAt: null }
```

The chain: `playerStore.ts:101-105` catches the 700 ms read timeout by setting
`{...DEFAULTS, walkthroughSeen: true, ready: true}` — **`ready: true` while holding
default data**; `recordGameCompleted()` at `:119-124` has **no `ready` guard**;
`GameSummary.tsx:278-281` calls it ungated from a mount effect; and `persist()` at
`:78-87` writes the **whole object**.

**Why:** today the blast radius is only a reset review cooldown and a wrong
`gamesCompleted`. The moment a streak, XP or passport field joins that store it becomes
lost, unearnable player progress — the classic one-star review.

**FIXED 2026-09-09.** `commit()` now gates every write on `hasKnownStoredProfile`,
retries the read with a patient 5 s timeout, replays pending changes onto the real
record, and serializes writes. No schema change. Originally guarded by
`npm run check:player-store` (REMOVED in c122551; the guard now lives in tests/player-store.test.ts, Case 1 is
the original bug - verified by the D3-1 reconciliation 2026-10-05), which ran the real module with AsyncStorage stubbed and
fails 6 checks against the pre-fix file.

Two defects in the first attempt were caught by that script, not by review: the recovery
read inheriting the 700 ms UI timeout (so a slow device never recovered and the counter
stopped advancing), and a rebase that clobbered a concurrent mutation. **When adding a
background retry, never reuse a timeout that exists for UI responsiveness.**

**How to apply:** same rule for any future persisted field. Gate every writer on
`ready`, and make the storage layer read-modify-write through a single owner instead of
whole-object overwrite. Note the trap: a spec claiming "these actions are protected by
`if (!get().ready) return`" is **false** for `recordGameCompleted` — verify the guard
exists rather than trusting the claim. The live AsyncStorage backend is the **legacy Java
`AsyncStorageModule`** (transactional `multiSet`). `useNextStorage` defaults to false
(`async-storage/android/config.gradle:15`) and this app never sets
`AsyncStorage_useNextStorage`. `newArchEnabled=true` does NOT switch to the Kotlin
`next/StorageModule.kt` — it only changes TurboModule wiring. (An earlier version of this
memory claimed the opposite; corrected 2026-09-16.)

Related: [[play-targetsdk-36-blocks-updates]], [[seed-store-from-browser-for-visual-qa]]

**Review lesson, 2026-09-16 (A1 storage foundation, REQUEST CHANGES):** the "unreadable stored best" guard
only protected the case where the new best was exactly 0, so a finite stored best the parser rejected
(e.g. "28000" above today's 25,000 max) was lowered by the first positive game. Detection rule: probe
every "keep the unreadable original" guard with a FINITE out-of-range value and a positive new value, not
just garbage and zero. Brief rule: pin "never write a best below any finite stored number" with one test
per key. Also from that review: a mutation pass found two recovery guarantees with no test that failed
when they broke — recovery after a *failed retry* is the edf2b36 bug class and needs its own test.
