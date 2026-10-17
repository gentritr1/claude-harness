---
name: launcher-icon-is-the-off-home-hero
description: assets/icon.png is ALSO the art_v2-OFF home hero image; the I2 icon commit silently changed the flags-OFF home — found only by the device pixel gate
metadata:
  type: project
---

`src/components/StartScreen.tsx` renders `require('../../assets/icon.png')` as the home hero mascot when art_v2 is OFF.
7e4a5b4 (I2 launcher icon, 2026-10-04) replaced that file, so the flags-OFF home lost the 1.4/1.5 globe mascot.
Nothing in the commit or its handoff row mentioned it. The release-gate pixel comparison against v1.5.0 found it on
2026-10-07. The owner chose to keep the new art on home (a2/FINDINGS.md).

**Why:** a shared asset ties two surfaces together, and "flags OFF = BASE" proofs never look at asset-only commits.

**How to apply:** before changing any file under assets/, grep src for its `require(` sites and list every screen
that uses it. Treat a visible change on an OFF path as needing the owner's eyeball.

Related lesson from the same gate: comparing OFF against the last *release* (v1.5.0) differs from comparing against
the BASE commit, because the plan allows unflagged defect fixes (EXECUTION.md:57-59). That gate was re-scoped to
"every difference attributed to a named commit, plus the owner's eyeball". Related:
[[pixel-exact-before-after-screenshots]], [[every-gate-we-write-ships-a-silent-pass]].
