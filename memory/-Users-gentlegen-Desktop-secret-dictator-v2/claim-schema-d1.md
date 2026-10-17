# The claim schema (Discussion Gate D1) — 2026-08-09/10

`src/engine/floor.js` + `test/floor.test.js`, branch `discussion-d1` (3 commits,
NOT pushed; origin/main still at 450d9e0). First deliberate engine *extension*
since the port — new file, the frozen five untouched (md5s re-diffed vs v1).

## The staging rule (load-bearing, will be flipped later)
The handoff wants speech to move bot belief AND wants this gate to change no
event log. Both right, different stages. D1 = **pre-coupling**: utterances are
canonical/validated/analysable, no bot rules-decision reads them. The invariance
test (50 seeds, floor off vs on, identical event logs) is the acceptance. At the
belief-coupling gate, change **that one check** into controlled divergence and
keep the probe beside it (it hands the speech layer `G.rng` and requires
divergence — useful in either direction).

## Resolved spec ambiguities (do not re-litigate silently)
- **C4** "claimed draws exceed deck composition": counted inside a
  reshuffle-free window (deckCount rising = discard went back in), bound read
  from `SD.DECK_REFORM`/`SD.DECK_SEIZE`. Conservative → cannot fire on an honest
  table. Per-claim bound would be vacuous (3 tiles can't exceed 6).
- **C5 vs V4**: V4 makes an unamended second claim unconstructible, so C5's
  literal condition is unreachable via the constructor. Scoped to "amends does
  not name the claim it contradicts"; literal case kept in the flag engine for
  records built elsewhere (replay/wire), with its own fixture.
- **C6** implemented for `basis: enactment` only (two concrete cases). Under-
  implemented on purpose, stated in step-09.

## New detection rules earned here
- **A detail key shadowed the event's own `kind`** (`{power, seat, kind}` renamed
  `power_announced` → `purge`, firing T5 twice per purge). Nothing threw; the
  stream looked plausible. → **When a count and its cause can be counted two
  ways, count them two ways.** `mark()` now throws on shadowing.
- **Comment broke its own grep gate** — the file's header spelled the forbidden
  token while explaining it never uses it. **4th occurrence in this project.**
  Promote: any new grep gate ships with the comment already de-tokenised.
- **Two correct logs differed by a formatting field** (`ev.n` stamped by
  `Driver.playOut`, not by a hand-stepped loop) → invariance "failed" on all 50
  seeds. A real divergence could have hidden behind the same difference. → an
  A/B log comparison must state which side builds the log and how.
- **Zero is a result: print counts next to claims.** T4/T5 opened 0 floors while
  powers/purges happened every seed (the morning ack published a transition and
  swallowed the real one); the obligation cap had 498 opportunities and 0 firings
  (obliged seat appended at the END of a beat order that never gets that far).
  Both invisible without per-trigger and per-cap counters in the output.
- **V5/V6 are checked before kind-specific rules** — a rejection test that reuses
  a seat which already spoke silently asserts V6 while claiming to assert V3/V4.
  Every rejection fixture runs on a fresh floor.

## Facts worth keeping
- The engine has no "government" object; `observe()` derives one from public
  scalars + `G.log` kinds/meta. Cross-checked against the driver's event stream
  (different representation — the cross-check-independence rule again).
- `refs.flag` is the only non-ordinal reference; flag ids are computed
  (`C3:u-4:u-7:g-3`), validated against flags that currently hold. Not an
  address — do not persist one.
- Ledger = lists of ids only; the test asserts no ledger field is a number
  except `seat`. "No score/meter/percentage" is a property, not a promise.
- Fixtures poke the record's fields directly, which is safe *because* the record
  is plain JSON with no private state. If it ever grows a closure, the fixtures
  break — that break is the warning.
- Seed-1000/7p fingerprint re-verified after the gate, node AND Chromium:
  61 steps / 38 decisions / LOYALIST / 81 log lines, `self.SDFloor === undefined`.
