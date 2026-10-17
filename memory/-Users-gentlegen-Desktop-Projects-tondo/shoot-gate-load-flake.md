---
name: shoot-gate-load-flake
description: npm run shoot's banner-clear premise can fail under machine load; the frame-count and settle floors carry no jitter allowance
metadata:
  type: project
---

2026-10-06: `npm run shoot` failed once with
`banner-clear mock:roundOver@390x844  valid=false` while `bannerVisible=true`,
`seats=3`, `overlaps=[]` — i.e. the probe's PREMISE failed, not its verdict.
Run in isolation immediately afterwards: `valid=true, pass=true`, frames 158
and 121 against floors of 60 and 45. A clean re-run of the whole gate with my
own server shut down and zero stray Chrome processes: exit 0, 3/3.

**How to read this shape.** `valid=false` with healthy-looking sub-values means
the scene did not set up, never that the thing under test broke. The
round-boundary probe's `valid` requires `next.frames >= 60`, `lobby.frames >= 45`
and `yourTurnMeasuredAt < 700` — all wall-clock sensitive, all with **no jitter
allowance**, which is the §6 red flag about thresholds compared without an
allowance for measurement resolution. Under load (my own server plus several
Chrome instances from measurement sweeps running alongside the gate) those
floors are reachable.

**Mechanism is INFERRED, not proven**: one failure under load, two passes clean.
I did not reproduce the failure deliberately by loading the machine.

**Rule.** A single red gate run is not a finding and not dismissable either:
re-run it clean (no other servers, no stray Chrome) before concluding anything,
and never accept one isolated green re-run of the *probe alone* as clearing a
red run of the *gate* — that is the shortcut that produced a false green earlier
the same day ([[2026-09-27-tier23-shipped]] records that one). If this flake
recurs, give the frame floors a tolerance or make the gate retry a `valid=false`
row once and report both attempts.

Related: [[cdp-capture-harness]], [[2026-09-26-live-region-same-tick]]

---

**2026-10-06, later the same day — it recurred, and the verdict still could not
say why.** Two gate runs failed at `banner-clear mock:roundOver@390x844`, the
second with nothing else running, which looked like a regression rather than a
flake. Diagnosing it cost a separate probe run, which passed with frames 157 and
122 — because the premises that go soft under load are the rAF sample-count
floors, and an isolated run has the machine to itself. The next gate run passed
3/3. Intermittent, as before.

**Fixed the instrument rather than re-learning this a third time** (804cbe6):
`round-boundary.js` now computes `valid` from a NAMED premise object and returns
`failedPremises`, and the gate's banner-clear line prints those names plus
`frames next=N/60 lobby=N/45` whenever `valid` is false. A bare `valid=false`
over fourteen anded conditions is not a diagnosis, it is a round-trip.

The standing recommendation above — give the floors a tolerance, or retry a
`valid=false` row once and report both attempts — is still **not done**. Next
recurrence, do that instead of diagnosing again.
