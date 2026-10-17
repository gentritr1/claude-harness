---
name: za-table-and-log
description: table branch complete — PR #3 open to main (auto-deploys on merge); Kitchen Log conventions; scars from 2026-08-08/09
metadata: 
  node_type: memory
  type: project
  originSessionId: 36810674-ff73-4118-8cbb-668e7af1b950
  modified: 2026-08-09T19:30:31.028Z
---

As of 2026-08-09: branch `table` (tip 8c03ccf, pushed) holds the counter/queue
seating rework, all playtest fixes, the full audit program, ship-review fixes,
and the three motion changes (portrait/plate snap, still numeral, 1400ms belt)
— user APPROVED the motion A/B on 2026-08-09 ("keep the proposed one"), so the
parked-motion question is closed. PR #3 (github.com/gentritr1/za-game/pull/3) opened
2026-08-09 at user's request, table→main; MERGE IS THE USER'S CLICK and
auto-deploys to Render. Post-select-screen fixes on the tip: considered-tile
ring as ::before overlay (inset box-shadow paints under child imgs — scar),
and all 12 regular portraits made transparent (1cr each) over one shared
--cabinet-hi ground (baked per-file navies read as mismatched squares in a
row). ~14.7 Higgsfield credits remain. Landed on top: mural CSS-background removal + ZINE ZA!→game link (2cde5ff),
NONNA'S RECIPES zine wing (85dc760, recipes wing now ABOVE dev notes per user),
and — after two art iterations the user rejected (plain photos, then 1970s
nostalgic photos) — the slots settled as CABINET VINYL: flat 4-colour
screen-print per design/design_handoff_za_cabinet/ART.md's exact language,
each with a two-frame arcade flip (art-slot-flip, 1800ms steps(1,end), B over
opaque A, reduced-motion parks on A) (f7fb567). User's standing art rule:
"arcade throughout" — new imagery should be kit-palette vinyl, not photos.
Higgsfield: 28 of 66.7 credits spent (~38.7 left); nano_banana_pro 2cr/image;
image-to-image with a prior job_id preserves composition for restyles and for
frame-B generation. Tip 909504a: roster idle frames (6 pairs, 12cr) grew into the 3A player-select
screen (design/design_handoff_za_roster) — 192px stage, filmstrip, two-act
touch select; the 48px tile flip that "read as blinking" is deleted. New scars:
roster/hire panel is built once per page load (stale tab = old UI, tell user
to reload before "it doesn't work"); resizing the pane mid-open leaves stale
device emulation and open-time state (reload before judging pointer-dependent
UI); Chrome CSS nesting gives every style rule a truthy .cssRules — check
selectorText FIRST when walking CSSOM. Scars: worktree stale-base fired a 7th time (both agents
fast-forwarded safely — ancestor case only); Chrome NEVER loads loading=lazy
images while a pane is hidden (flip to eager at runtime to verify wiring);
recipe pages run ~2.6-2.7 viewports at 375×812 vs the ~2 target — structural
(masthead+pager+footer+two figures), user hasn't judged it yet. Everything general-purpose on it (sliver
contrast, chatter ticker, lobby minmax, seam bleeds) would need cherry-picking
if seating is rejected. `docs/KITCHEN-LOG.md` (main, 5df65f1) is the public
engineering log — extend it as new incidents resolve; entries need provenance
lines. New scars this cycle, promoted into the log's house rules: transparent
two-frame loops must counter-phase; bare `1fr` tracks can't shrink below
min-content (use minmax(0,1fr)); floats over a felt lose to grid rows on short
screens; the pit engages only when measured density demands it ([[za-fleet-build]]).
