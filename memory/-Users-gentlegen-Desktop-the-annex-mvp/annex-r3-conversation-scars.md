# R3 conversation pillar — scars (2026-07-31, branch codex/nonlinear-causal-next-level)

## Pattern → detection rule → future brief/test update

- **`data-persona` collided between `PersonaPortrait` chips and a panel wrapper.** A jsdom
  parity harness used `querySelector('[data-persona="shepherd"]')` to ask "is the panel
  open?", matched the portrait chip in the *closed* rail, and therefore never clicked the
  rail button. 8 of 11 tests failed with an empty option list and no clue why.
  → **Rule: harness anchors get their own attribute** (`data-conversation`), never one a
  child component already emits. When a DOM harness reports "it offered: (nothing)",
  suspect the *selector matched something else*, not that the component is broken.

- **A "spike kept as the seed" measures its own generator, not the game.** The R0 disposition
  separation gate re-ran green after R3 without noticing that its state generator only
  dispatched field actions — it could not produce any state the new dialogue reaches.
  Extending the generator to pick uniformly from *every legal move the reducer accepts now*
  changed the numbers materially: dominant pair 35.7% → 26.2%, populated (stance,temper)
  pairs 11/15 → 15/15, `uncertain` share 65.6% → 56.7%.
  → **Rule: when a round adds a new action type, the sampling generator of any distribution
  gate must be extended in the same round, or the gate is stale evidence.**

- **`node:fs` does not typecheck in this repo's `src/**` tests.** `tsconfig.app.json` sets
  `types: ["vite/client"]`, so `node:fs`/`process` are unavailable and `import.meta.url` is
  an http URL under the jsdom environment. Reading a committed evidence file from a test:
  use Vite's `import x from '../../evidence/….json?raw'`, not `readFileSync`.

- **Authored-prose leak guard needs kebab filtering.** A "no raw content id in dialogue"
  assertion false-positives on single-word ids that are also ordinary English (`maintenance`,
  `registry`). Only check ids containing a hyphen.

## Facts established this round

- Save schema **3 → 4** (`conversation` event sourceType). Migration is a no-op; the run's
  conversation events **are** the dialogue's progress, so no new persisted field.
  Corpus proof: `src/game/persistence.v3corpus.test.ts` (70 assertions over the captured
  browser seed + 10 synthesized v3 payloads). Verified in a real browser too: a genuine v3
  save in localStorage on :4545 migrated to 4 with `events` byte-identical.
- `getTrustLabel` **moved** from `engine.ts` to `disposition.ts` and is re-exported from
  engine, to break `engine → conversation → worldLife → disposition → engine`. Same four
  thresholds, no caller changed.
- Case 77 pre-R3 authored **five** negative-trust sources in the whole case and **none** for
  the Defector, so `opposed` was unreachable for shepherd/defector/archivist and `guarded`
  for the defector. Closed by giving each persona two −2 choices on one branch
  (root → pressed → pressed again). All 4 personas × 5 stances now reachable by a greedy
  walk over the real reducer.
- Writing actually landed: **107 prose strings per persona, 428 total, 31,203 characters.**
- Chunk effect: `createAnnexWorld` gz **unchanged** (147.18 kB both sides of the change);
  main `index` chunk 183.83 → 198.66 kB gz (+14.83), CSS 42.55 → 42.86 kB gz.
