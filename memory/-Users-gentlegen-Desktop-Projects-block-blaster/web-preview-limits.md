---
name: web-preview-limits
description: Claude browser pane cannot click RN-web Pressables in this app; visual-only evidence
metadata: 
  node_type: memory
  type: project
  originSessionId: 2051cf29-c6f2-47e3-8fbd-76df141b5684
  modified: 2026-08-31T21:51:25.253Z
---

In the Claude Code browser pane, `computer` left_click on the Expo web build (launch config `blockrow-web`, port 8081) times out and synthetic PointerEvents via JS do not fire RN Pressable handlers. Screenshots and read_page work fine. So web preview evidence here is layout/visual-existence only; anything interactive (starting a run, drags, combos, game-over flow) is device/simulator-only verification. Matches the global scar: preview ≠ device for gesture code.
