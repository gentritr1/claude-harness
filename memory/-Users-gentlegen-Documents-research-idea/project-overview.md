---
name: project-overview
description: "FairBlocks Daily — fairness-first block puzzle (Expo RN); brand is calm/honest, no hype; baseline committed 2026-07-17."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2b50cf8f-d345-445f-acf6-221a183ff5b7
---

FairBlocks Daily: 8x8 block-placement puzzle where every dealt tray is solver-verified to have at least one full placement sequence ("Every tray has a way"). Local-first, no backend/ads/accounts. Docs: PRODUCT.md (brand + anti-references), ENGINE_SPEC.md (rules + persistence contract), DESIGN.md (tokens).

Baseline MVP committed 2026-07-17 (first commit d21bc97). As of that date: tap-to-place only, zero animations, monochrome pieces, no daily streak/stats/share, default Expo icon.

Brand guardrails that constrain all feel work: no confetti, neon, casino shine, or interruptions; reduced-motion and high-contrast preferences must be respected; tap-to-place must remain as the accessible alternative to any drag interaction. Persistence: PersistedRunV1 is sacred — additive keys only, validate + fall back on corrupt data.

User has ~7.5 Higgsfield credits (Starter plan) earmarked for app icon / splash art. Related: [[node-and-ports]].
