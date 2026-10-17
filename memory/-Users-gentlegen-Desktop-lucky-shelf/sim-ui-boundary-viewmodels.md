---
name: sim-ui-boundary-viewmodels
description: Screens must not value-import sim/economy/item internals; go through store view models. The sanctioned pattern + how it was sealed (5fe4bd6).
metadata: 
  node_type: memory
  type: project
  originSessionId: a55d034b-799c-4add-95d3-38f4c5c38f10
---

**Rule:** UI screens (`src/app/*`) may import **types** from `@/contracts` (the shared boundary),
but must NOT **value**-import from `@/sim` or `@/items`. Deriving build facts (synergy tag/mult, sell
prices, order progress, reroll cost) belongs behind the store boundary, not on the render path.

**Sanctioned pattern (two flavors, both live in `src/state/store.ts`):**
- Referentially-stable computed selectors on `runSelectors` (e.g. `pendingSupplierTags` returns a shared
  constant or null) → screens subscribe directly via `useRunStore(runSelectors.x)`.
- **View-model builders that return fresh objects** (`sellShelfView`, `synergyHudView`, `orderHudView`,
  + `rerollCost` re-export) → **pure functions of `GameState`**, NOT selectors. Screens `useMemo` them
  over `gameState`. Do NOT put fresh-object builders on `runSelectors` and subscribe — that re-renders on
  every store change. A module-level `selectorItemTable = loadItemTable()` lets a pure builder resolve
  item definitions without threading deps.

**Sealed the last leaks 2026-07-08 (`5fe4bd6`, part of the M4/M5 stabilization pass, NOT new mechanics):**
run.tsx pulled `DEMAND_MULT/TAG_SYNERGY_ELIGIBLE_TAGS/TAG_SYNERGY_LADDER/tagSynergyEnabled`; restock.tsx
pulled `itemDefinition/loadItemTable/REROLL_COST/sellPrice`. Moved `activeSynergy`→`dominantSynergy` into
the store. Grep guard: `grep -rn "^import " src/app src/ui | grep -v "import type" | grep -E "from '(@/(sim|items))'"`
should return nothing.

**Verification scar — some refactored renders are un-eyeballable headlessly.** This was a
behavior-preserving refactor, verified by: VM-output equality (scripted, executed), tsc (wiring), full M0
(101 tests, determinism pin unchanged), and a clean iOS-sim boot (all screens import the store, so a clean
title proves the module graph). **Could NOT pixel-verify** the populated sell view (behind an untappable
Buy/Sell toggle — computer-use to the Simulator is denied) or the HUD synergy/order banners (need seeded
flags + ≥3 tagged items). For a pure refactor that's proportionate; for a *visual* change to those views,
seed + screenshot per [[ios-ui-verify-on-simulator]]. See [[design-system]], and this is the base the
Lane B build-signposting (#5) sits on.
