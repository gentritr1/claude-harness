---
name: za-fleet-build
description: "The parallel-agent build of the full ZA! Arcade spec — what shipped, what was deliberately deviated, process scars"
metadata: 
  node_type: memory
  type: project
  originSessionId: 36810674-ff73-4118-8cbb-668e7af1b950
  modified: 2026-08-08T11:22:43.343Z
---

On 2026-08-07 the full ZA! Arcade handoff (design/design_handoff_za_arcade/README.md, vendored in-repo) was implemented via three parallel Opus worktree agents (table layout + scrollable hand; nine effects + WebAudio sounds.js; the Regulars + the Receipt) plus a read-only compliance auditor, with Fable reviewing/merging. 49 tests. Six regular portraits + trophy in public/assets/{regulars,sprites}.

**Deliberate spec deviations (do not "fix"):** dimmed hand cards ~85% not 40% (user readability request); minis 20px not 60px (60 breaks seat stacks); card keyline via --suit var not currentColor border (visually identical); scanlines over popovers (kit's own picker mock is scanlined); six roster tiles not five (spec self-contradicts); no vocal samples (README §9); no shout timing scores or PENALTY-n totals (not client-observable / no such server state); RND tile hidden until the wire ever carries a round number.

**Process scars:**
- Bash tool cwd PERSISTS between calls — a `cd` into an agent worktree made later "main" commits land on the agent branch. Always `git -C` / absolute paths when multiple checkouts exist.
- `git add -A` scoops `.claude/worktrees` embedded repos; `.claude/` is now gitignored but prefer `git add -u` + explicit paths.
- Worktree agents may also apply their edits to the shared checkout; diff both before assuming.
- Agents sharing the one browser pane fight over tabs; the hidden pane freezes CSS animations AND rAF — "observed" animations may have advanced 0ms (verify via WAAPI seeking), and entry-animated content screenshots as invisible until animations finish.
- A stray `pkill -f "node server"` from one agent killed a sibling's server; give agents distinct ports AND tell them to kill by port, not pattern.

**Cabinet handoff (PR #1, 2026-08-08):** design_handoff_za_cabinet vendored (PROMPT-marquee.md then PROMPT-cabinet.md, direction 1A). Marquee landed via Opus worktree agent (merge 3f61543): five-chevron chase carries direction (reverse flips DELAY order, not glyphs), three colour moments in one padding-driven box, utilities are bezel screws below the hand, `.shell` (display:contents) owns width policy. Murals cabinet-left/right.png generated (chef toss / oven mouth, four-colour vinyl). New scars:
- **A present CSS custom property NEVER triggers `var()` fallback** even when its value is unusable in context (calc with `none`) — consumers silently compute `auto`. The shell gates arithmetic behind `--play-cap` (always a length) while `--play-max: none` stays documentation. Keep that split.
- **Browser-pane click coordinates can be uniformly scaled vs page coords** (observed 2.43×: clicked 640,300 → page 1553,728). Calibrate: arm a document-level pointerdown recorder, click a known point, divide. Ref-based clicks used the same wrong mapping — calibrate before trusting ANY click, and re-calibrate after resizes.
- Trusted (real) clicks give user activation → `navigator.clipboard.writeText` succeeds where agents' `element.click()` gets NotAllowedError; closing an agent's clipboard caveat needs a calibrated real click.
- **Chalkboard-special interpretation (deliberate):** the game has no round modifiers; the cabinet chalkboard shows the live current topping as "today's special" rather than rendering empty. User notified, not yet explicitly approved.

**Juice pass (PR #1, branch `juice`, 2026-08-07):** the 14-tile Juice board implemented via a two-iteration Opus loop judged by the `.agents/skills/review-animations` skill (installed via `npx skills add emilkowalski/skill`). Punch card deliberately unbuilt (designer's note). New red-flag promoted from this session: **a forced layout read (offsetWidth/clientWidth) between node insertion and setting transitionDelay resolves @starting-style and silently kills the stagger** — the deal cascade had been dead since it shipped, detectable only by probing computed delays at runtime. Also: `@starting-style` loses to any higher-specificity opacity rule (dimmed cards never faded in); check specificity AND document order.
