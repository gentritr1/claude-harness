---
name: fixed-overlay-narrow-viewport
description: position:fixed overlays centered via left:50% break at narrow viewports — shrink-to-fit uses only half the viewport; always verify overlays at 320/375px
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2292c2f0-72df-48de-8be3-5f18015153bb
---

A fixed-position banner centered with `left: 50%` + `translateX(-50%)` computes shrink-to-fit width against the space to the RIGHT of `left` — only half the viewport. At 800px it renders perfectly; at 375px the content collapses to one-word-per-line and buttons clip off-screen. Shipped broken in FJALË's update banner (verified only at ~800px), caught days later in a 375px review pass.

**Why:** the CSS trap is render-invisible at wide viewports, and overlays that appear only on rare triggers (SW update prompts, toasts) escape routine mobile checks.

**How to apply:** any `position: fixed` overlay must be verified at 320px and 375px before release, with rare-trigger overlays force-shown via DOM (`el.hidden = false`). Prefer `inset-inline: 0` + `margin-inline: auto` + `width: fit-content` over `left: 50%` centering. Related: [[localhost-port-collision]].
