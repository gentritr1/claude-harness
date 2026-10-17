---
name: game-spec-7-omits-chamber-centre-offsets
description: "GAME_SPEC §7's camera-fit derivation is incomplete — it omits chamberCenterX/Y, so a centred chamber is ~0.6 units off on a phone"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:09:07.912Z
---

`GAME_SPEC.md` §7 quotes the camera fit as four lines (ortho, visibleWidth, chamberWidth,
failLineY) but **omits the two centre-offset lines** at `GameplayController.cs:527-528`:

```
chamberCenterX = (leftReserve  - rightReserve) * 0.5 * visibleWidth   // = -0.09 * visibleWidth
chamberCenterY = (bottomReserve - topReserve)  * 0.5 * visibleHeight  // = +0.025 * visibleHeight
```

The chamber is deliberately **off-centre** because the left/right reserves are asymmetric
(0.04 vs 0.22 — the HUD column lives on the right). Centring it instead shifts every body, the
aim clamp and the walls by ~0.6 world units on a 19.5:9 phone.

**Why:** implementing §7 as written produces a subtly wrong chamber that no test in the spec would
catch. Reading `GameplayController.cs:505-552` in the read-only reference repo settled it in one
look, which was cheaper than guessing.

**How to apply:** when a brief says "every constant you need is already in the spec", still open the
cited source for any *derivation* (as opposed to a single constant) — a transcribed formula can be
missing terms. `packages/merge-shell/src/chamber/cameraFit.ts` is now the full transcription;
GAME_SPEC §7 should be amended to match.

Related: [[merge-kit-physics-port-seam]]
