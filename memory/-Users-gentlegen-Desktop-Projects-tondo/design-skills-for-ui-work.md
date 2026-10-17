---
name: design-skills-for-ui-work
description: On Tondo the user wants the design skills (emil-design-eng, frontend-design, ui-ux-pro-max, apple-design) folded into UI/feel work, not just hand-rolled judgement
metadata:
  type: feedback
---

2026-09-26: while the Tier 2/3 plan was running, the user said to also use the
installed design skills — emil-design-eng, frontend-design, ui-ux-pro-max,
apple-design — for anything needing UI tweaks, rather than deciding motion and
layout ad hoc.

**Why:** the briefs I write are the spec the implementer follows, and a brief
written without the motion/UX playbook ships defaults nobody chose. The user
treats these skills as part of the house style, not optional reference.

**How to apply:** load the fitting skill BEFORE writing a task brief that
touches visible UI, and carry its concrete rules into the brief's acceptance
criteria (exact easing curve, duration band, origin, press feedback, stagger
window) so the reviewer can check them. emil-design-eng for motion and press
feel, frontend-design / ui-ux-pro-max for new surfaces (lobby, share card),
apple-design for gesture and sheet behaviour. Note that Tondo's stylesheet
already encodes most of the Emil checklist from an earlier pass — ease-in is
banned in-file, hover is gated behind `(hover: hover) and (pointer: fine)`,
no `transition: all`, no `scale(0)` entries, `:active` press scale on every
pressable — so the payoff is on NEW surfaces, not on re-auditing old ones.

Related: [[2026-08-animation-pass]], [[2026-09-16-action-legibility-fx]]
