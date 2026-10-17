---
name: typed-date-intermediate-values
description: Chrome date inputs emit partial years ("0002","0020","0202") while typing — any client loop keyed on the year must compare numbers and bound to 2000–2100; UI tests must type dates, not fill them
metadata:
  type: feedback
---
Half days PR SnaxxTech/offday#28 (2026-10-04): `yearBalance` looped `for (y = first; ; y++)` until `String(y) === year`. Typing "2027" into a date input with the keyboard passes "0002-10-05" first, so the loop never ended and the tab froze. Tests that used `.fill()` with whole dates, a security review and the task tests all missed it; the final whole-branch reviewer caught it by typing in Chrome.

**Why:** `.fill()` sets a finished value. A person typing goes through partial values.

**How to apply:**
- Treat every value the client derives from a date input as possibly "0002…" or empty.
- Compare years as numbers and bound loops (the app allows 2000–2100).
- Every form with date inputs gets one UI test that types the date with `page.keyboard.type`.
- Chrome's date field order follows the OS locale (dd/mm on this machine), not the page locale, so assert the year (`/^2027-/`), not an exact date.

Related: [[undo-windows-and-side-effects]], [[ci-build-only]]
