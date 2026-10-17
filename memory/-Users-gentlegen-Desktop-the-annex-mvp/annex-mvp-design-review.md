---
name: annex-mvp-design-review
description: "2026-07-19 design/UX review results — both-worlds verdict, confirmed violations, fix backlog"
metadata: 
  node_type: memory
  type: project
  originSessionId: bbb02cb4-bacc-420f-823a-32ec093c9721
  modified: 2026-07-19T11:43:36.710Z
---

Design review (Fable live-measured + Opus 4.8 full CSS/component audit) against .impeccable/design.json, ui-ux-pro-max rules, and frontend-design distinctiveness:

**VERIFIED clean at runtime:** body contrast (record/night ≈17:1, zero failures on start+briefing with correct oklch canvas parsing); high-contrast mode clears everything; larger-text scales root 16→18px (rem-based); reduce-motion leaves ZERO live transitions (dual .reduce-motion class + media query); focus-visible cyan 2px/3px-offset ring everywhere; 390px: no horizontal scroll, no overflow; motion exactly the 180ms token; mobile rail collapse works; "show trust values" renders "+0" numbers.

**UPDATE 2026-07-19 (later same day): all 6 items below FIXED by Opus executor and REVIEWED-APPROVED with live runtime re-measurement** — essential copy 12px, floors met, chips de-ambered (testimony fog/raised 7.2:1, badges 14.96:1), anomaly 5.79:1, eyebrows sentence-case on investigation+debrief, all targets 44px live, trust causes verified in rendered Log end-to-end incl. run-2 "Residue: Registrar +1, …" line. 18/18 tests (2 new). Trust-delta suffixes are TEXT in event detail (no schema change — old saves load).

**Original violations (all fixed, kept for pattern reference):**
1. Essential copy below 12px: .choice-body small (consequence + "cannot be changed" warning) 11.5px, .inline-confirmation p 11.5px, .event-list p (the logged cause text) 11.2px; trust-label 9.9px; .event-tags span 8.8px floor. Violates repo's own "Record Before Atmosphere" rule.
2. Amber semantic breaks ("amber = action" rule): .evidence-testimony status chip styles.css:1951 (worst), .site-index badges, .tribunal-seal, amber eyebrows.
3. Repeated uppercase-mono eyebrows (explicitly banned in design.json): 3+ per screen on Investigation and Debrief (.section-context, .debrief-section-heading>span).
4. Touch targets <44px: preference-popover labels 28px (the a11y toggles themselves), inline-confirmation buttons 40px, evidence disclosure 36px, "Erase local save" 32px.
5. .evidence-anomaly coral-on-coral-deep = 3.93:1 RUNTIME-MEASURED (below 4.5) at 9.3px.
6. Trust-change causes never logged as events (partial violation of design.json's "show the cause" do) — ties into [[annex-mvp-next-features]] item 3.

**Gotcha recorded:** naive contrast probes misparse oklch computed colors (regex→rgb assumption gave absurd 1.7:1 on white-on-black); always resolve via 1px canvas fillStyle→getImageData. Also React controlled checkboxes ignore form_input DOM sets — use native .click().

Verdict: UX-rigor world HOLDS strongly at runtime; distinctiveness world strong macro (committed municipal-terminal aesthetic, no AI clichés) but drifts generic in the label/eyebrow/stat-tile layer; repo's own constitution PARTIAL (3 named rules broken by its own CSS).
