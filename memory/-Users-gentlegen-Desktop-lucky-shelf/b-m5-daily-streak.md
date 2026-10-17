---
name: b-m5-daily-streak
description: B-M5 Part 1 daily-streak landed (e69b3a6); Parts 2-3 (silhouettes+teaser) implemented 2026-07-09 awaiting Fable; catalog-wipe scar reappeared on the streak record path
metadata: 
  node_type: memory
  type: project
  originSessionId: 0d698d1d-51eb-448a-9532-ddfa7c13cd82
---

B-M5 Part 1 (daily streak) implemented on 2026-07-08, headlessly green (25 new tests, full
suite 179), NOT committed. Deliverable: `docs/review-packets/B-M5-retention-surfaces-review.md`.
Additive `streak?: {count, lastDate}` on `DailyRecordSchema` (`.strict()` + `.optional()` = old
saves load loss-free, no version bump, no wipe risk, determinism pin untouched). Pure helpers in
`src/persistence/daily.ts`: `previousDateString` (local Date calendar-normalise → no DST/ms math),
`advanceStreak`, `displayStreakCount` (shows count only while last-play is today/yesterday, else 0;
surfaces gate at ≥2). Surfaces: title button `· 🔥 N`, summary line, share-card line.

**Scar (third firing of the [[m6-round-review]] catalog-wipe pattern): `recordDaily` advances the
streak from in-memory state, so a cold-relaunch-into-finished-run would read `streak:null` and reset
a live multi-day streak to 1.** Fix = load-guard inside `recordDaily` (`if (!loaded) await
loadDaily()`) AND make `loadDaily` carry the persisted streak forward even when the record is from a
prior day (new day = "not played today" but the streak must survive to increment). Regression test:
`dailyStore.test.ts` "does not wipe a live streak when recording before the store is loaded".
Detection rule: **any lazily-loaded store whose record path reads prior in-memory state to compute
the next persisted value must load-guard AND preserve the carried-forward field across the reset
condition** — not just guard the merge.

Part 1 LANDED as `e69b3a6`. A-M7 unlock ladder also landed (`b735ea5` + `ef1efae` graduation gate),
which unblocked Parts 2-3.

**Parts 2-3 implemented 2026-07-09** (packet `docs/review-packets/B-M5-retention-surfaces-parts-2-3-review.md`,
awaiting Fable; NOT committed). Pure view-models in `catalogStore.ts`: `buildCatalogView` gained
`locked`/`unlockHint` per item (flag `UNLOCK_LADDER_ENABLED`; off → byte-identical, proven by test);
`nextUnlockTeaserView` for the summary "one more run" row (prefers nearest `runsPlayed` gate, null
off/exhausted). `formatUnlockHint` = display-only prose over the sim predicate (no unlock logic in
Lane B). Catalog `LockedStamp` = real sprite `tintColor: palette.inkFaint` silhouette + hint (locked
≠ undiscovered "?"). Hints resolve item/combo ids via table/combos. Gotcha: transform-target items
aren't in `UNLOCK_LADDER` → guard `predicate !== undefined` so they stay "?", not silhouettes.
Known visual risk (device gate): long combo hints may truncate on the 22%-width card; fallback =
short card-only hint form. Full suite 259/259, tsc + greps clean (node 20.19.4; shell default v14 too old).

**B-M11 gate status:** B-M11 (combo discovery moments) requires "B-M5 Parts 2-3 landed on `main`".
Still NOT met — Parts 2-3 are implemented but await Fable + merge. Tree entangles 3 lanes (Lane A +
B-M10 + B-M5 P2-3); `summary.tsx` carries BOTH B-M10 seed-label AND B-M5 teaser, so no clean
`git add` split. Recommend landing B-M10 first, then B-M5 P2-3. Never `git commit` here unilaterally
(sweeps other lanes + self-sign-off). See [[b-m10-share-polish]], [[reviewer-workflow-opus-split]].
