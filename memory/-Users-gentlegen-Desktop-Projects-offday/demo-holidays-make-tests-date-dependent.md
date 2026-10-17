---
name: demo-holidays-make-tests-date-dependent
description: "The demo workspace loads real public holidays (US by default), so UI tests counting \"this week\" weekdays fail in holiday weeks"
metadata:
  node_type: memory
  type: project
  originSessionId: 2336fd90-e02c-4aed-9ba0-569ef7381ed7
  modified: 2026-10-13T21:34:55.538Z
---

Demos load real public holidays (date-holidays, US for en-US). Default shifts skip holidays, so tests/shifts.spec.ts "default shift works every weekday" saw 4 not 5 in Columbus Day week (2026-10-12) and failed on every branch that week. Fixed in dacf3ab by reading `.holiday-note` in the Shifts grid header.

**Why:** a test that passes for weeks can go red with no code change; it looks like a regression in whatever PR is open.
**How to apply:** when a test fails on today's week, check holidays in the demo workspace first (query the /tmp/offday-test-*.db for that org). New UI tests about "this week" should derive working days from the page, not assume Mon–Fri. Related: [[preview-demo-id-remap]].
