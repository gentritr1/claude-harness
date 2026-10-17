---
name: timer-floor-assertions-need-slack
description: "A test asserting elapsed >= N against an N ms timer, measured with Date.now(), fails ~1 ms early at random — it was the 904/905 flake"
metadata:
  type: feedback
---

On 2026-10-02 the one-in-six full-suite flake on feat/next-level turned out to be `tests/graph-probe.test.ts` asserting
`censored.ms >= 40` against a 40 ms timer and `afterMs >= 400` against a 400 ms timer. Node fires timers on libuv's
monotonic clock, the test measured with `Date.now()` (a separate wall clock), and both floor to whole ms, so an on-time
timer read 399. Fixed in 72d23bb with `TIMER_TOLERANCE_MS = 5`.

**Why:** the early read is rare and NOT driven by load: 40 runs with every core saturated gave 80/80 readings at or
above the floor. Isolated reruns (60/60 green) cannot reproduce it, so "the rerun passed" proves nothing. My suspect
before reading evidence (a cross-test leak) was wrong.

**How to apply:**
- Any `elapsed >= timerMs` assertion needs a few ms of slack, sized well below the gap the test exists to tell apart.
  Check the slack still fails a planted bug (fires immediately; reports at the ceiling).
- Upper bounds are already safe in this direction; lower bounds at exactly the timer value are the trap.
- When stress-testing with CPU spinners from a background zsh, kill them by parent pid (`pkill -P`): `jobs -p` came back
  empty and left the load average at ~110.

Related: [[gate-commits-on-the-exit-code]], [[every-gate-we-write-ships-a-silent-pass]].

**Second instance (2026-10-04, D2-3 -> found at D2-4's gate):** `drain = () => sleep(150)` waited for netLog lines printed 25 ms apart; under full-suite load the last line (`[share] rounds=`) had not printed yet — 1 failure in 2 full runs, 0 in 15 isolated runs. A fixed sleep before reading a log is the same bug as a zero-slack timer floor. Rule: wait on the producer's own completion (`await flushNetLog()` until the buffer is empty), never on wall time; and run a new test file under concurrent load before trusting "15/15 isolated".

