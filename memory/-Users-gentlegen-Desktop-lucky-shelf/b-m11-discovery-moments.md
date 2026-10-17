---
name: b-m11-discovery-moments
description: "B-M11 combo discovery moments — pure model + cascade toast/stamp/jingle/slow-beat, catalog new accent"
metadata: 
  node_type: memory
  type: project
  originSessionId: fe3ed2ec-1ac1-4973-b113-f9c43b788d90
---

B-M11 (combo discovery moments) **Fable-APPROVED 2026-07-10 + pushed** (`1ef39b8`, `110b491`,
`b44400a` + packet `9f37094`; verdict in `docs/review-packets/FABLE-REVIEWS-2026-07-10-round6.md`).
Reviewer independently re-ran suite (289 green), re-read the timing/persistence diffs, reproduced the
greps. **Open:** bespoke discovery-jingle mp3 (placeholder = payout sting — required before
feel-complete; one-constant swap in audio.ts) + device recordings (batched gate, round-6 doc). Noted
non-blocking risk: `useRunStartAchievedCombos` has no load-guard (safe via _layout boot hydration;
worst case cosmetic; harden with `loadStatus === 'loaded'` gate if it ever fires).

**Model:** `src/juice/cascade/discoveryModel.ts` — pure `classifyDiscoveries(events, {achievedBeforeRun,
seenPriorThisRun})` → per-comboNamed `repeat|first-this-run|first-ever` + eventIndex (= player stepIndex,
no second clock). `slowBeatStepIndices(moments, enabled)` + `stepDurationMs(base, speed, slow)` live here
too (pure, node-safe) — the player imports them.

**Key architecture wins (non-obvious):**
- juice→@/state would be CIRCULAR (state→juice already exists via store.ts). So CascadeLayer can't read
  the catalog store; `achievedBeforeRun` is threaded as a PROP from run.tsx (`useRunStartAchievedCombos`
  snapshot in catalogStore.ts).
- `cascadeMount.gameState = beforeOpenShop` (PRE-scoring), so `gameState.catalogDelta.discoveredComboIds`
  IS "prior-days combos this run" cleanly — no subtraction, no cross-day edge. Discovered by reading
  `phaseRouting.cascadeMountAfterOpenShop`.
- `catalog.achievedComboIds` only merges at run END (`recordRunEnd`/summary), so reading it live DURING a
  run = run-start snapshot. `discoveredComboIds` = ALL combos matched this run (NOT first-ever-flagged) —
  first-ever needs the achieved snapshot.

**Slow-beat:** `motion.discoverySlowBeat = 1.2` token; player multiplies the CURRENT step's dwell only
when `slowBeatIndices.has(stepIndex)`. Reduce-motion → caller passes empty set → `stepDurationMs(...,false)
=== Math.round(base/speed)` (byte-identical cadence, proven).

**Catalog "new" accent:** in-memory `lastRunDiscovery` on catalogStore (computed in recordRunEnd vs the
pre-merge `previous` — the only place pre-merge achieved survives), mirrors `prevRunStats`, NO persistence.
`buildCatalogView` gains pure `isNew` flag. DROPPED "until first viewed" (needs view-tracking persistence)
per brief fallback.

**Scars/gotchas:**
- Pure helpers imported by tests must NOT transitively import RN-ecosystem modules. `stepDurationMs` had
  to move OUT of useCascadePlayer.ts (which imports haptics→expo-haptics, unavailable in node) into
  discoveryModel.ts. Same class of trap as [[b-m9-theme-migration]] (.styles.ts split).
- Jingle mp3 doesn't exist → `DISCOVERY_JINGLE_SOURCE` placeholder = cascade sting (avoid breaking the
  bundle with a missing require); dedicated asset is a deferred audio gate.
- Adding a required field (`isNew`) to a view-model interface (CatalogComboRow): buildCatalogView always
  sets it (default false) so consumers don't break; update any equality/snapshot tests.
- Editing a B-M9 `.styles.ts` (catalog) means updating its `.styles.test.ts` expected() too.
- run.tsx WAS edited (2 lines, additive) — it was clean/committed by B-M11 time; juice can't self-source.
See [[goal-horizon-vs-resource-cadence]], [[cascade-self-fire-pop]].
