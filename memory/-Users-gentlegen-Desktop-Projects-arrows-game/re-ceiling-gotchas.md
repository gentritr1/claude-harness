---
name: re-ceiling-gotchas
description: "v2 ceiling: arrow cap allows 450 on the exact RNG (452 by arrows; >450 breaks the steady bag); OWNER PICKED 354/354 (scan-matched, option B) 2026-09-27; harness gotchas"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-27T01:45:00.000Z
---

RE-CEILING (2026-09-27, docs/next-level/reports/RE-CEILING.md): on ExactDotNetRandom the arrow rule (<= 250 over the (e) sample AND every index 0-9999) gives 452; round 1 put **450** in the tree because Super Hard targets above 809 (Hexagon) leave 5-shape saturated windows and the bag's O(1) steady state needs >= 6 (cold pick at 20,000: 124 ms jitless vs 2 ms). The probe encodes that ("window >= 6 shapes"). (Round-1 pins a54d5f48 / f2fdde04 were never committed.)

**Why it matters:** 450 made saturated v2 boards +33% arrows vs v1, ~1.3x v1 on the scan proxy, 6 of 26 shapes, +45% node gen per level. **Resolved 2026-09-27: owner picked option B, CEILING = V1_FLOOR = 354** (floor now calibrated on the scan proxy: `--v1-floor` prints both units; 354 = 1.000, at the instrument's resolution). Pins: v2 fresh 71dc3369, existing ea5e4bf5. Typical saturated v2 level still +9% gen time vs v1 (p95 -6%); existing players 0.94-1.04 on the proxy; 13 of 26 shapes.

**How to apply / gotchas:**
- Arrow parity is not scan parity: at equal arrow medians v2 scans ~0.91 of v1 (plain shapes + v1's RNG-defect boards). Any "match v1" floor must say which unit.
- `until ! pgrep -f "<pattern>"` in a zsh loop never exits: the loop's own `zsh -c` command line contains the pattern. Wait on an output marker instead.
- jest's testMatch `**/src/**/__tests__/**` used to pick up `artifacts/*/snapshot/src/...` copies other tasks leave; fixed by ccb8d06 (jest.config ignores artifacts/).
- An isolated jest copy of src/core needs a `.d.ts` with `/// <reference types="node" />` and `declare var __DEV__: boolean;` (the repo gets both from scripts/ and App.tsx), plus src/ui/boardCamera.ts for shapeBag.test.ts.
