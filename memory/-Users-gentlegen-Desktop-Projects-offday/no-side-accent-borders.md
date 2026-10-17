---
name: no-side-accent-borders
description: User hates thick coloured left-border accents on cards/callouts — never use that pattern
metadata:
  type: feedback
---

Never style cards, callouts, alerts or rows with a thick coloured `border-left` (or inline-start) accent stripe. Use an even 1px border with a soft tint, an icon and type weight for emphasis instead.

**Why:** the user said "that border left i hate it… remove as pattern and never use that" (2026-10-04, on the coverage warning card).

**How to apply:** in any UI work for this user, don't propose or ship side-accent borders; plain 1px neutral column dividers are fine. Offday's DESIGN.md records the same rule.
