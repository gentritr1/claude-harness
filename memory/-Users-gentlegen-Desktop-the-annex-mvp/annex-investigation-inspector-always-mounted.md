---
name: annex-investigation-inspector-always-mounted
description: "Field-site methods/room live in an always-mounted inspector, not gated behind the world-view closeup; base CTAs on room phase, not camera state"
metadata: 
  node_type: memory
  type: project
  originSessionId: cfd70c10-d2b5-4f9e-9dca-9742bc8c5707
  modified: 2026-07-23T21:05:20.955Z
---

In `Investigation.tsx`, the `.site-record.site-inspector` (right column) renders the
selected site's close-read room (custody rail / classification / acoustic shadow) and
its two canonical methods **unconditionally** — it is NOT gated behind "entering" the
site via the world-view (Case 77's concourse) closeup. Registry intake in fact has no
`closeup` plate at all, so `shownCloseup` is permanently falsy there.

**Scar (UX fix pass 2026-07, F-5 state-aware CTA):** I first keyed the footer CTA's
"entered vs not" on `Boolean(shownCloseup)`. It stuck on "Enter Registry intake"
forever because the camera never enters a closeup that doesn't exist. Fix: drive the
CTA off the **room phase** the room reports up (`custodyPresentation.phase`, etc.) —
`methods` / `unlocked` / `route-ready` = terminal → methods visible → hide the CTA;
earlier phases → name that step. See `src/game/fieldCta.ts` (pure, unit-tested).

**How to apply:** for anything that asks "has the player entered/opened this site?",
read the room's derived phase, not the world-view/closeup transition state. The
world-view is decorative camera; the inspector is the real interaction surface.

Related: [[annex-preview-pane-quirks]] (el.click() needed; vite serves 4174 not the
assigned port), [[annex-campaign-decisions]].

Also (same pass): `react-hooks/set-state-in-effect` ESLint rule bans a synchronous
`setState` inside a `useEffect` body — use the render-phase "adjust state on prop
change" pattern (like CaseRail's `prevTrust`) instead. Retiring the persistent trust
▲/▼ marker on the next commit had to move from an effect into an `else if` in render.
