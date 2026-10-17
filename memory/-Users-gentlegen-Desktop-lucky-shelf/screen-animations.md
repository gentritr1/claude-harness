---
name: screen-animations
description: "Subtle UI animations added (press/select springs, ambient loops, Entrance) and the scar that expo-router already animates screens."
metadata: 
  node_type: memory
  type: project
  originSessionId: 523339a0-35c7-4643-bd36-369320df5b1d
---

2026-07-08 (Opus, commit 30857b0): the gameplay/juice layer was richly animated but every `app/*.tsx`
screen was static. Added subtle, reduced-motion-gated motion in the existing token vocabulary (durations/
easings/springs in tokens.ts; helpers in juice/motion.ts):

- **WoodButton** press → springs to 0.96 on `motion.springs.grab` (was an instant opacity flick; the code
  comment had promised this "M1" wiring for ages). Uses `Animated.createAnimatedComponent(Pressable)`.
- **OfferCard** selection lift (1.03) + press (0.96) are spring-animated, not static jumps. Removed the
  static `transform` from `styles.selected`; the animated `scale` owns it now.
- **CoinCounter** HUD pill ticks (1.06) on any coin change; slam (1.22) unchanged. Extended the existing
  `punch` value rather than adding a second.
- **RentChip** breathes ~3% when `dueInDays <= 1` (kickoff §6 "rent must be felt"). Static otherwise.
- **Title cat** slow breathe loop (same vocabulary as ItemSprite's shipped breathe).
- **Entrance** primitive (`juice/Entrance.tsx`): fade + 8px rise on mount, staggered by `index`.

**SCAR → detection rule:** don't add a screen-mount entrance without checking what already animates the
mount. Verified via `simctl recordVideo` + ffmpeg filmstrip that **expo-router runs its own native slide
on `router.push`**, and the **cold-launch splash masks the root mount** — so the blanket `Entrance` on
screens is largely REDUNDANT/masked. It only shows on in-place reveals (a panel toggling, `router.replace`
navs with no slide). Kept it on title+draft but flagged for review. Rule: an entrance animation earns its
place only where nothing else transitions the content in.

**Verification reality (per [[ios-ui-verify-on-simulator]] + the juice feel-gate rule):** confirmed all
animated components render without crashing (title/draft/arrange), card selection moves correctly, rent
chip does NOT pulse when calm (gating correct). The subtle MOTION itself + the rent pulse in alarm state
(needs day-3 to reach) are a **device feel-gate call for the user** — recorded filmstrips can't really
prove ~3-4% subtle motion, and feel acceptance is the user's per the harness. typecheck + 117 tests green,
no engine/economy change.
