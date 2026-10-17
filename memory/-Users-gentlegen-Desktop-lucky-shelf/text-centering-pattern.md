---
name: text-centering-pattern
description: The one place the Baloo2 optical-centering nudge lives (baloo2IconNudge); the context-dependency trap that makes blanket-nudging wrong.
metadata: 
  node_type: memory
  type: project
  originSessionId: 523339a0-35c7-4643-bd36-369320df5b1d
---

2026-07-08 (Opus): consolidated the Baloo2 vertical-centering nudge into a single helper
`baloo2IconNudge(fontSize)` in [src/ui/tokens.ts](../../../../Desktop/lucky-shelf/src/ui/tokens.ts).
Before, the nudge was hand-copied with drifting magic numbers — `translateY` 1/2/5 across CoinCounter,
OfferCard, and restock (2 sites had it MISSING entirely). Formula: `dy = round(0.12 * fontSize)` for iOS
(`translateY`); Android uses `includeFontPadding:false + textAlignVertical:'center'`. Calibrated on the
iOS sim (zoomed): 16px→2, 20px→2, 34px→4. Verified on-device: OfferCall coin "3", HUD pill "0" (was +1,
slightly high → +2 centered), day-total SLAM "1" (was +5 → +4, centered).

**THE TRAP (context-dependency — the reason "check every element and apply the pattern" is dangerous):**
Baloo2 glyphs sit HIGH in their line box, so the downward nudge is needed ONLY when the text is
row-aligned (`alignItems:'center'`) against a SHORTER neighbor — a coin dot, an icon — where the glyph
ends up above the neighbor's center. When the text is the sole centered child of a box (a button label, a
screen title, a phrase inside a pill), flexbox already centers the whole line box and the nudge would push
it LOW. Measured "New Run" button text at +1px (already centered) — blanket-nudging every `<Text>` would
have shoved every button 2px low. Caught `restock.sellValue` ("Sell +5" inside a pill) mid-refactor: looks
like a coin value but is block text → excluded from the helper, kept its own small manual lift.

So the pattern is TWO cases, not one blanket rule: (a) icon-adjacent digit → `baloo2IconNudge`; (b)
block-centered text → nothing (or a tiny bespoke lift), flexbox handles it.

**AppText primitive** (`src/ui/components/AppText.tsx`, commit 7a5e58c): the one block-copy primitive
(variant + align + color), applies a `typeScale` role; deliberately does NOT apply the icon nudge (case b).
Adopted across the shared kit: WoodButton, TopBar, SectionLabel, RentChip, MovesPips. Behavior-preserving
(same typeScale) — verified no regression on the Draft screen. The screen-body `<Text>`→`AppText`
migration (~90 sites) was deliberately left as **adopt-on-touch**: near-zero visible change, high churn;
the primitive + kit already give the guarantee.

**Tag pills** (commit 7098ce8): only TWO were genuine plain tags (OfferCard, restock.shopTag) — folded
into shared `TagChip`. The other four (`signatureBadge`, `spotlightTag`, cascade score `tag`, `auraLabel`)
are distinct colored/positioned status badges, correctly kept separate. Unified size = **9, not 10**:
TagChip had no prior consumer so nothing to match at 10, and 10 wraps "food perishable" in the ~95pt offer
card — 9 reproduces the original look (dedup, zero regression). SCAR: "unify to the shared component's
value" is only right if that component has real consumers; here TagChip was dead, so the offer card's own
size was the real anchor.

restock's shopBuyText/rerollCost are wired to the helper but sit on the LOOP_V2 daily-shop screen (flag
default-OFF), so NOT eyeballed on that screen. Verify via the sim loop in [[ios-ui-verify-on-simulator]];
tokens live in [[design-system]].
