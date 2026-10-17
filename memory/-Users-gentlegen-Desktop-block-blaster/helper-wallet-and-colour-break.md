---
name: helper-wallet-and-colour-break
description: "2026-07-27 Break now destroys a whole colour, and helpers became a persisted wallet — the per-run refill was silently making the rewarded ad worthless"
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-28T18:55:10.792Z
---

Two changes requested by the user in Albanian after playing the build:
"Break le te prish 1 ngjyr jo 1 bllok" and "Shuffle edhe break edhe hint jan tu
reset tu ba 3 gjith kur po ja nis new game".

**Break destroys a colour.** `cellsWithColorAt(board, row, col)` in
`src/game/logic.ts` collects every cell sharing the tapped cell's `colorIndex`.
Test worth keeping: **`colorIndex` 0 is a real colour and is falsy** — a
truthiness check would have made the first colour un-breakable. Empty taps
return `[]` and never spend the helper.

**Helpers are now a persisted wallet, and this was a revenue bug, not a polish
item.** `restart()` called `createStartingHelpers()`, so every new run handed
back all 9 uses free. The rewarded ad only appears when a helper hits 0 *during*
a run — so a player could always just tap Play Again instead of watching an ad,
and the whole rewarded placement could never earn. The user spotted this from
play, not from the code.

Now: `@blockrow/helpers_v1` holds the wallet, 3 of each on first install only.
Leftovers carry across runs; spend and ad-grant both write through; only the
per-run rewarded cap resets, so each run can still earn +1 per helper. Chosen
over "small drip per run" and "no per-run cap" after presenting the options.
Storage is **additive** — existing run saves and high scores untouched, no wipe
risk. `SavedRunState.helpers` still exists but is now ignored in favour of the
wallet; kept for save-format compatibility rather than bumping the run schema.

**Device-verified on emulator (not just tests):** spent one Shuffle (3→2),
force-stopped and relaunched the app → still x2 (proves it reached disk), then
started a new run → still x2 (proves the refill is gone). Break on one of four
orange cells destroyed all four and left the two green cells untouched, with
Break going 3→2.

Balance consequence to watch: a player who burns all 9 uses now has none until
they watch ads, one per helper per run. That is the intent, but it is harsher
than the old behaviour — the "drip" variant is a small change from here if it
plays badly. Related: [[interstitial-on-game-over]], [[admob-migration]].
