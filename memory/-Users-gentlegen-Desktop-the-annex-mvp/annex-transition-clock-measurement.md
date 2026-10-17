---
name: annex-transition-clock-measurement
description: Pane getComputedStyle reads the START frame of any CSS-transitioned property — disable transition before probing background-color/opacity
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3cde3ba2-d335-4a55-befd-d33aa1a0aa0b
  modified: 2026-07-21T20:49:32.558Z
---

During the 2026-07-21 arm-state review, `getComputedStyle` in the Browser pane read `.choice-row-armed` background-color as transparent and the sibling opacity as 1 — making it look like the armed fill and sibling-recede weren't applying. They WERE: `.choice-row` declares `transition: background-color 180ms, opacity 180ms`, and the pane (like headless Chrome per the delegate's own finding #2) does not advance the transition clock, so the probe read the transition's START frame. `box-shadow` (no transition) applied instantly, which is what exposed the pattern.

**Proof technique that disambiguates:** set `el.style.transition='none'; void el.offsetHeight;` then re-read getComputedStyle — the resolved TARGET value appears (here bg → `oklch(0.26 0.06 70)`, sibling opacity → `0.42`). Color and font-weight were NOT in the transition list, so those read correctly even mid-transition.

**Why:** I nearly filed a false REQUEST CHANGES against correct CSS. The delegate's report was accurate; the pane was the unreliable party — my own harness rule ("preview ≠ device") in miniature.

**How to apply:** when probing a property that has a CSS `transition` in the browser pane, either disable the transition first (as above) or don't trust a single computed-style read. Safe-to-read-directly (untransitioned) props: color, font-weight, box-shadow, text content, aria-*. Related: [[annex-preview-pane-quirks]], [[browser-pane-stale-screenshot]].
