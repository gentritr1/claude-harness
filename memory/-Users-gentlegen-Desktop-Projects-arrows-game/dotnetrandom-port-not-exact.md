---
name: dotnetrandom-port-not-exact
description: "The JS DotNetRandom port does not wrap int32 like .NET for |seed| > 161803398; draws 3+ can leave [0,1)"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-26T15:06:23.411Z
---

Found by the W3-10 implementer (2026-09-26): src/core's `DotNetRandom` (port of Unity/.NET System.Random) does not wrap int32 arithmetic for |seed| > MSEED (161803398). 4,651 of 20,000 campaign seeds draw outside [0, 1) within 50 draws (values from −10.8 to +12.1). Draws 1–2 are always in range (0 bad in 3M seeds), so v1's shape pick and target are safe, but `fillMask` is skewed on about a quarter of levels in v1 and the daily.

**Why:** v1 boards and the daily are frozen (fingerprints d01abbd8, daily ff12d7b5): players already have those levels, so the port must NOT be "fixed" for v1.

**How to apply:** any new consumer of DotNetRandom (v2, new features) must either keep seeds inside the exact range or use an exact int32-wrapping RNG; detect by scanning the internal state. v2 needs an exact RNG before W3-21 (queued as V2-RNG). Related: [[game-design-truths-measured]].

**Resolved for v2 (V2-FINISH, 2026-09-26):** v2 now draws from `ExactDotNetRandom` (Int32Array + `| 0`, proven equal to a BigInt transcription of .NET; 0 of 50M draws out of range over 1M seeds). Gotchas found: (1) most divergent legacy streams differ from .NET by only a few units in 2^31 and change no pick, so a positive control must use seeds whose legacy draws actually leave [0,1); (2) the defect carves short arrows: the ~23% affected v1 boards have ~10-16% more arrows, and W3-14's ceiling (339 vs 250 arrows) was measured on defect boards; on the exact stream everything up to base 370 stays at or under 210 arrows. Any v2 size/ceiling number measured before V2-FINISH part 2 is stale.
