---
name: annex-prototype-qa-scars
description: "QA scars: class-collision invisible to text assertions; reduced-motion advance-paced; harness must include user's real play width; pumped-rAF rigs prove logic not liveness; loop predicates need input state"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0b1a5b43-8b07-44a8-89d7-cc7036f27cf1
  modified: 2026-07-30T23:45:44.306Z
---

Two scars from the scene-first prototype builds (committed 47f570c, c5bb083):

1. **Class-name collision between a content class and a layout class is invisible to every DOM/text assertion.** The deposition prototype's dialogue lines used class `ellis`, colliding with the Ellis figure cutout's `.ellis` (absolute positioning) — all staged text piled unreadably over the figure while `textContent` checks stayed green the whole time. Only a screenshot caught it. **How to apply:** visual review of at least one screenshot per distinct screen state is mandatory even for "text layout" work; grep new class names against existing selectors before reusing a semantic word (character names especially).

2. **Reduced-motion staged text must be advance-paced, never auto-timed.** The Small Archive prototype's reduce-motion path auto-flushed chained beats (3rd refusal + slips) before they could be read. Contract: under reduced motion, render lines fully and wait for the user to advance. Also: clearing a beat and revealing zones must happen in one transition callback or text flashes.

3. **The verification matrix must include the user's actual play width.** Every harness tested only 1280×800 + 375×812 through eleven approved rounds; the user plays at ~2000px wide, where the docked console ate the photograph's bottom, zone markers (fixed 17px at opacity 0.58) became unfindable on a huge plate, and chrome pills sat on the image — none of it caught (reported by the user with a screenshot, 2026-07-26). **How to apply:** before approving any layout round, ask "what width does the user actually play at?" and require it in the harness matrix; fixed-px UI elements over scalable art must scale (clamp) with the container.

4. **A pumped/fake rAF rig proves logic, never liveness (2026-07-31, walkable round 1).** The implementer verified WASD walking by replacing requestAnimationFrame with a manual `__pump(frames)` (needed because the Browser pane is a background tab where rAF never fires). Every per-frame number converged perfectly — and in a real browser walking was completely dead: keydown scheduled ONE frame, that frame ran with dt=0 so velocity stayed 0, the loop-continuation predicate (`walkSpeedNow() > 0.0001`) saw no motion and stopped, and OS auto-repeat was filtered by `pressedKeys.has()`. Same family as the RN reanimated headless-invisible scars. **Detection rule:** any claim that continuous motion works must come from real-rAF runtime (headless Chrome via the repo's CDP evidence-script pattern — swiftshader flags, Node 24 for global WebSocket) with trusted CDP input, asserting a position delta over a real held key. **Brief update:** motion acceptance criteria must name the real-rAF harness and the minimum delta (e.g. `realKeyWalk.forwardDelta ≥ 1.5 m/s-held`); pumped-clock evidence is auto-tagged UNVERIFIED for motion.

5. **Loop-continuation predicates must include INPUT state, not just derived motion state.** The round-1 bug shape generalizes: "keep animating while velocity > ε" self-deadlocks when velocity can only grow during animated frames. Continuation must OR in the causes (keys held, stick deflected, response playing), not only the effects.

Related: [[annex-scene-opacity-strand]], [[annex-review-scar-clamped-counters]], [[annex-transition-clock-measurement]], [[annex-campaign-decisions]].
