---
name: mockup-code-is-not-trusted-math
description: "My HTML globe mockup's clipping shortcut was ported into ART-1 and broke the globe in a dozen time zones; reference code from a mockup needs a ground-truth oracle"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-04T22:16:11.995Z
---

On 2026-10-05 the ART-1 review found that globe polygon clipping pushed hidden vertices radially to the rim with no rim arc.
- A gore from 3-4 days ago lit half the globe (49.8% of the disc vs 0.2% true).
- Land and ocean inverted at UTC+7:30..+9:15, -11..-9:45 and +13..+14.

The implementer had ported this from MY globe-concepts.html mockup, because the brief told them to treat its script as "a working reference". It only looked right at the view angles I happened to pick. The test harness pinned the time zone to UTC+2, so no gate swept the angle.

**Why:** a mockup is built to look right once, at chosen angles. Its math was never tested.

**How to apply:**
- Never hand mockup code to an implementer as trusted logic. Name a proven algorithm instead (here, d3-geo's clipCircle and rejoin) and require a ground-truth oracle test: a per-pixel inverse projection, swept over the whole input space (every UTC offset, every state).
- When a harness pins an input (time zone, clock), add one test that sweeps it.

Related: [[every-gate-we-write-ships-a-silent-pass]], [[gates-recompute-never-trust-report-flags]].
