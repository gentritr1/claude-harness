---
name: brief-must-not-reverse-owner-decisions
description: ART-4 v1 brief re-proposed time-zone globe facing that the owner had already replaced (weekGlobe.ts) and a sun model that already existed (core.ts) — read the module headers first
metadata:
  type: feedback
---

On 2026-10-07 I drafted the ART-4 brief (home globe spin and day/night) without first reading the globe modules.
The v1 brief:
- settled the spin on a time-zone longitude, although the owner had approved a FIXED 55 N view that explicitly
  "supersedes time-zone longitude facing" (src/utils/weekGlobe.ts:5-9, guarded by the tz tests);
- asked for a new NOAA sun model although `subsolarPoint` and `nightRegion` already exist and are tested
  (src/design/globe/core.ts:203-284);
- added a second entrance on top of the existing homeHero FadeIn;
- reversed the spin direction.

Fable 5.1's review caught all four.

**Why:** a brief that contradicts a recorded owner decision costs an owner round-trip and erodes trust; existing
code comments in this repo record owner rulings ("OWNER-APPROVED ...").

**How to apply:** before writing any brief, grep the touched modules' headers for "owner", "OWNER-APPROVED" and
"supersedes", and list the existing functions a brief would duplicate. Get an independent review (Fable or Opus)
of briefs about visual or motion work before showing them to the owner. Related: [[mockup-code-is-not-trusted-math]].
