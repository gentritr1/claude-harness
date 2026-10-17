---
name: cascade-self-fire-pop
description: Cascade renders self-scoring ruleFires (source===target) as an on-slot ×N/+N pop instead of a zero-length arrow nub.
metadata: 
  node_type: memory
  type: project
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

Lane B polish (2026-07-07) for the depth-lever prototypes ([[front-window-spotlight]], [[todays-order-demand]]): the spotlight/order multipliers emit `ruleFire` events with sourceSlot === targetSlot, which the cascade drew as a zero-length "arrow nub" (a glitch).

Fix in [CascadeLayer.tsx](src/juice/cascade/CascadeLayer.tsx): any `ruleFire` where source === target renders a new `SlotPop` badge (springs in, ×N for a mult / +N for a flat) instead of `CascadeArrow`; multi-slot fires still draw arrows. The test is **geometric, not a ruleId allowlist** — so it also fixed latent nubs on the pre-existing self-scoring rules **lonerBonus** and the **Antique Clock** (multIfAdjacentMinTotal), and auto-handles any future self-scoring rule. Colors: spotlight→goldDeep, order→tealDark, others→slot arrow hue.

Pure decision logic extracted to [popModel.ts](src/juice/cascade/popModel.ts) (`isSelfFire`, `deltaLabel`) so it's unit-testable without RN/Reanimated — [popModel.test.ts](src/juice/cascade/popModel.test.ts) covers the helpers AND ties the classification back to real `resolveOpenShop` emissions (spotlight/order fires are self-fires; cross-slot fires aren't).

**Verified:** tsc clean; 67/67 tests; independent Opus reviewer APPROVE (enumerated all 9 scoring ruleFire sites). **UNVERIFIED:** device feel of the pop animation — the human's gate (web can't prove the cascade, see [[lane-b-web-verification]]).
