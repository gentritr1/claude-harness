---
name: every-gate-we-write-ships-a-silent-pass
description: "Three log readers on this branch, three silent-pass holes — assume the gate we just wrote has one and attack it before reading its tests"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-01T11:37:05.344Z
---

Every custom gate built on feat/next-level shipped a way to pass without measuring anything:

1. **C1a's coverage check** trusted a `reconciled` flag in its own report: passed with n=240 against 18,432.
2. **B1-4's `read-hud-log.mjs`** printed PASS three times on `values=[]`, and its one reconciliation
   (`changes <= observations`) was vacuous by construction.
3. **B1-5's `read-commit-log.mjs`** validated flag *values* but not flag *names*: `--stmap 180` instead
   of `--stamp` made a log whose ring was cut off in 3 of 4 commits exit 0, `ALL CHECKS PASSED` — and the
   header echoed `rounds`, `hold`, `mode` but not `stamp`, so the skipped check was invisible. It also
   reconciled *lines* against rounds but never *commits*, so a run that was 80% empty read clean.

Each was written by a careful agent, and each hole was found only because someone fed the gate a
synthetic input instead of reading its tests. The tests always passed — they tested the shapes the
author had thought of.

**Why:** a gate's author writes the rejection cases they can imagine. The failure is always the case
they could not imagine *being* a case — a flag name, an empty list, a count that cannot coexist.

Later instances (2026-10-02): **#7** B2-5's `--ready-log` reader silently dropped loads that ended abandoned or
renderer-dead (right-censored), so it would have proposed a timeout below loads it watched still pending. **#8** B3-1's
slot tests passed with the home banner's reserved slot moved outside its padded, curtain-held container (reviewer's X2,
full suite 1090/1090). Also a pattern: a **measurement protocol** can be a silent pass too — B3-1's device steps ran with
animations off, which snaps the sheet, so the close-path check could not fail. Ask of every protocol step: "what
state must the device be in for this to be able to fail?"
**#9** (B3-4): the consent device step logged the geography from the env var while the code silently sent `{}`
when it could not map it — from Kosovo UMP answers NOT_REQUIRED and the step would have read "owner-gated". Log
what was actually SENT, not what was configured.
**#10** (C1b-1): derive-timeouts' three new shape refusals could all be deleted with its tests green. And a
related trap: when a constant shrinks (DRAW_MAX_REQUESTS 5 -> 2), re-expressing a fixture "for any k" silently drops
the ORDERINGS the old longer fixture covered ([503, malformed, EMPTYx3] became [503, malformed] — no test left an empty
answer after a failure). When a test is re-expressed, list every ordering the old fixture exercised and keep each.
**#11-#12** (C1b-3's --ruled check): a throttle self-check that looked only at COMPLETED samples called a link
that censored 19 of 20 requests "inert" and passed; and an --exclude flag silently dropped sessions the rule needed.
Censored and failed samples are evidence of slowness, never missing data — rank them as infinitely slow.
**#13**: an ESM script's `import.meta.url === pathToFileURL(process.argv[1])` main-module test is false when run
through a symlink (macOS /tmp, /var), so the whole script exits 0 with no output. Realpath argv[1]; a gate must fail
loudly when it did not run.
**#14** (C2-2): the "flag OFF writes what BASE wrote" test compared byte-for-byte — but never seeded the new
optional map, so a write that normalised a newer build's non-number values passed it. An OFF=BASE proof must seed every
shape the NEW code reads (including foreign/garbage values), not only the shapes BASE knew.
**#15-#16** (C2-3): tests of a NEW rule (v2 gold) used only inputs where old and new rules agree, so a screen still
deciding gold the old way passed 1611/1611 — and the device protocol picked the same agreeing rounds. A test of a
changed rule needs inputs where the two rules DISAGREE (a hinted Pinpoint; a 0.6 km Same city).

**How to apply:**
- Before trusting any reader/gate, **attack it with synthetic inputs before reading its tests**: an empty
  measurement with healthy-looking counters, a mistyped flag, a count that cannot coexist with another,
  a correct count in the wrong order, a missing line.
- A gate must **reject unknown arguments**, not just bad values, and **echo every optional check's
  parameter in its output header** so a skipped check is visible in the evidence.
- Reconcile the thing being measured against the run, not just the lines: `n` lines is not `n` events.
- Any brief that commissions a reader must name the **mistyped-flag case** and the **all-empty case** as
  required rejection tests.

Related: [[gates-recompute-never-trust-report-flags]], [[a-min-over-a-sampled-matrix-is-an-artefact]].

**Fourth hole (2026-10-09, ART-4g device pass 2).** The `[globe] spin frames` line computes `expected = window / median delta` (globeSpin.ts:262). A steady 20 fps sweep therefore prints `n=20 expected=20.3` and "n == expected" passes. The device agent caught it by reconciling against window / 16.67 ms. Rule: an "expected" count must come from the display's period (or a fixed 16.67 ms), never from the measured frames themselves.
