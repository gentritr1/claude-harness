---
name: detector-needs-positive-control
description: W6-07 reported 0/10 crash-record survival, but its detector grepped a __DEV__-only log sink in a release build — a count of zero needs a positive control
metadata:
  type: feedback
---

2026-09-19, W6-07 (Codex): the 10-trial release run counted drained crash records by grepping
`[telemetry] … "name":"error"` in logcat. That console sink is registered only under `__DEV__`
(App.tsx), so the release probe could never print it — the trial logcats held 0 `[telemetry]` lines,
not even `app_open`. "0/10 survive" measured the detector, and the doc was about to state it as fact.

**Why:** a zero count is indistinguishable from a blind instrument unless the same detector is shown
to fire on a known-true case in the same build. Same family as the owner's "state transition never
confirmed" red flag.

**How to apply:** pattern → detection rule → brief update. Any k/N measurement where k can be 0:
(1) check that the detector's signal exists in that build type (dev-only logs, __DEV__ sinks,
PERF-disabled telemetry); (2) require a positive control (force the true case, see the detector
fire) and a negative control before the trials; (3) save full logcats, not only filtered lines.
Put this in every brief that counts on-device events in a release build.
