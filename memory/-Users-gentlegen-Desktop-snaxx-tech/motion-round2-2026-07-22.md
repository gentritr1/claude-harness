---
name: motion-round2-2026-07-22
description: Round-2 motion audit+fix pass (plans 005-010) shipped 2026-07-22; what was verified at runtime vs pending human eyeball; testimonials section still hidden.
metadata: 
  node_type: memory
  type: project
  originSessionId: a0526348-b91b-4181-a123-eb1a0c614fcf
  modified: 2026-07-22T19:19:00.471Z
---

Round-2 animation pass executed 2026-07-22 (audit at `ebc0b94`, Opus 4.8 executor, plans/005–010, all DONE, uncommitted at time of writing). Key facts:

- `duration-350/400/800` were silently invalid Tailwind classes (fell back to 150ms) — fixed via `theme.extend.transitionDuration`. VERIFIED in dist CSS + computed styles.
- Reduced-motion block now uses a transition-property allow-list (opacity/visibility/color/bg/border/box-shadow @150ms ease) instead of nuking all transitions; `.page-enter` fade restored to 200ms. Runtime behavior under real `prefers-reduced-motion` is UNVERIFIED (preview pane can't emulate it) — needs a human DevTools/OS toggle check.
- Testimonials section is deliberately hidden (`testimonialsConfig.testimonials: []` — "no testimonials yet"). Its interruptibility fixes (lock removal, hover/focus pause, .pressable controls) were verified by temporarily injecting test data, incl. pre-fix failure repro (2nd rapid click swallowed) — then reverted. When real testimonials are added, the fixes are live.
- Service-row hover wipe rewritten as `::before` scaleX overlay. Note: the positioned pseudo paints ABOVE in-flow content (5% tint — believed invisible); visual confirmation pending eyeball, see [[motion-eyeball-pending]].
- `future.hoverOnlyWhenSupported` is ON — all Tailwind hover: variants now require `(hover:hover) and (pointer:fine)`.
- Old lens-hero CSS, `.snaxx-loaded` wordmark gen-2 CSS, useMouseParallax.ts and 9 dead tailwind keyframes were purged; hero scroll cue back on 3-iteration `.scroll-cue`.
- Backlog (taste, unplanned): testimonial dot progress fill, tokenize 700/800/1200 reveal durations, easing curves declared in 3 places.
- Hero 3D perf audit (same day): measured 120fps locked, zero >12ms frames at DPR 2 fullscreen, idle AND during party-mode + mega burst (M-series Mac). Architecture already right (demand frameloop offscreen/RM, dpr [1,2], shared burst mats, particle caps, no shadows). Applied micro-opts only (lookAt clone removal, hint-ring array hoist, powerPreference) in `b54b10c`. Low-end-mobile behavior UNVERIFIED — only lever left there is dropping mobile DPR cap below 2 (visual-taste call, needs device eyeball).
- Dev-pane console shows pre-existing `R3F: Cannot set "code-path"` errors — the preview harness injects a `code-path` prop that R3F applyProps rejects; CanvasBoundary recovers, canvas renders fine. NOT a site bug, absent in prod builds; verified identical on pre-change code. Related: pane input events report offsetX at half of clientX (0.5 zoom emulation) — R3F raycast clicks in the pane need clientX doubled; real browsers unaffected.
