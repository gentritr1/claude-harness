---
name: w3-21-v2-freeze
description: "W3-19 admission + W3-21 v2 freeze committed 85dda6b (local, unpushed 2026-10-06); over-install route and open items"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-10-06T02:46:56.067Z
---

85dda6b (2026-10-06): House/Teacup/Bell/Umbrella admitted to v2 (17 of 30); v2 frozen — fresh 1c4cd1f4, existing 849961f1, five goldens; never re-pin. v1 d01abbd8 / daily ff12d7b5 unchanged.

Over-install proof on emulator-5556 used current-code v2-off build A, NOT da93dcd (da93dcd bundles the live LevelPlay key and no test publisher id, so it can't be proven test-ads). Level 12 v1 Bolt 54 → level 13 v2 Heart 96, switch=12; teeth build C re-dealt 12 as v2 Rocket.

**Why:** the flag flip still waits on W3-17 (doc doesn't exist yet) + owner yes; promo art in artifacts/W3-21/promo-art awaits owner approval (Crescent is Normal-tier because v2 never deals a Super Hard Crescent; Flower reads weakly as a flower).
**How to apply:** don't re-pin v2; GEN_V2_ENABLED is a source constant only (test builds use throwaway edits). Related: [[re-ceiling-gotchas]], [[w3-15-w7-09-gotchas]].
