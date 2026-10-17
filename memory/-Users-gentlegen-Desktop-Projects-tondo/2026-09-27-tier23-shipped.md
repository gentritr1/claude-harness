---
name: 2026-09-27-tier23-shipped
description: Tondo Tier 2/3 shipped on branch next-level (PR #1) — 11 tasks, what closed each, and the device-only items that remain open
metadata:
  type: project
---

2026-09-27: Tier 2 and Tier 3 of `docs/NEXT-LEVEL.md` shipped on branch
`next-level`, 29 commits, opened as
[PR #1](https://github.com/gentritr1/tondo/pull/1). Not merged — the user
chose a PR so they can read it first.

**Shipped:** catchable bot personalities (0.50 callout windows/round measured);
action-card legibility; wild/TONDO/callout motion; the round boundary (deal from
the opener, pie sweep, banner placement); the top seat clearing the MATCH
plaque; one tap to a table (invite auto-join, One quick pie at 68ms, rejoin,
two-stage forget); four a11y defects; gated haptics; plain-text share;
`npm run shoot --check` with 26 assertions. Suite 44/11/20/22/19 = **116**.

**Open, and only a human can close them** (also in NEXT-LEVEL §7):
nobody has watched any motion, heard the sound, felt a haptic, or run a screen
reader; iOS is unverified for audio unlock, the gesture-gated clipboard and the
non-secure-origin textarea fallback.

**Known measured defects left in:** `wild` at 320x568 overlaps the plaque by
12.6px (the stage is at its 180px floor — even deleting the seat's pill leaves
the tile overlapping by 1.8px, so it wants a small-phone layout pass, not a
nudge); `wild` at 1280x800 clears by 1.4px; the strip's toggles are 38.5x44.

**Process notes worth reusing.** Subagent per task + independent reviewer per
diff worked, but two things mattered more than the structure: every task's probe
had to FAIL on the old code first, and reviewers barred from `git checkout`
proved their instrument by *sabotage* — injecting page-level CSS/JS to re-create
the defect and watching checks flip — which is a good technique for any
read-only review. Delegates twice declined a controller instruction with
evidence and were right both times; see [[delegate-overrode-my-ruling]].

Related: [[text-that-leaves-the-app]], [[2026-09-26-live-region-same-tick]],
[[shared-tree-agent-collision]], [[design-skills-for-ui-work]]
