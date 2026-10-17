---
name: polish-round-2026-07-11
description: "Opus-4.8-delegated polish round: system-font fix (TYPO-1), summary restructure (SUM-1), catalog album (CAT-1), How-to-Play (ONB-1) — statuses, open gaps, and the Order-vs-synergy escalation"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0dc1048f-6e5b-4765-aacc-2404dc9d6cd4
---

**Round (2026-07-11, human-directed, on `graduation-flip`):** four briefs implemented by Opus 4.8
subagents, Claude specced/reviewed/committed (the [[reviewer-workflow-opus-split]] pattern).

1. **TYPO-1 (`360af61`) APPROVED.** Font-metrics root cause MEASURED with fonttools: Baloo2 box
   1.602em / Nunito 1.364em, asymmetric → glyphs sit high under constrained lineHeight on iOS.
   Human ruled "standard font": `fonts.ui` = System/sans-serif now carries body/label/coin + new
   `typeScale.stat` role (numeric values); Baloo2 ONLY on display/title/heading. ALL
   `baloo2IconNudge` call sites removed (helper @deprecated, kept exported). Scar superseded:
   [[text-centering-pattern]]'s nudge approach is retired — new numeric UI text uses system face.
2. **SUM-1 (`c0a1d75`) APPROVED w/ review tweaks.** Summary = verdict hero + Panel stats card
   (shared right alignment edge via valueSlot) + gold-accent teaser + staggered reveal. MY BRIEF
   CAUSED A BUG: I specced "always-reserved caption slots, same height whether present or not" →
   card too tall, teaser pushed under the fold. Scar: when speccing fixed-slot layouts, compute the
   TOTAL height budget on the reference device first. OPEN: post-tweak layout + stagger motion need
   one human eyeball at the next natural run end (agent's Day-6 fixture was lost to a sim relaunch).
3. **CAT-1 (`2e76cbb`) APPROVED.** Catalog = trophy album: one-time staggered discovery reveals
   (uniform-scale pop + gold ring, ≤8 animators, session-scoped in-memory set), gold-edged owned
   cards w/ press spring, parchment embossed-? locked cards, runs-gate n/target ticks, header %
   count-up. catalogStore additions PURE (lastRunDiscovery stays unpersisted; saveCatalog payload
   untouched — wipe-scar checked in review). OPEN: "feels premium" = human taste gate.
4. **ONB-1 (`d52cfa5`) APPROVED after round-2 fix.** 7 swipeable pages + menu entry; sim facts
   cited file:line; flags mirrored via new pure seam `src/state/howToPlayView.ts`; `?page=N` deep
   link for per-page sim screenshots. Round-1 REQUEST CHANGES: the Multipliers page CONFLATED row
   auras (item-cast, ×2 gold row glow) with tag synergy (TAG_SYNERGY_LADDER 3+→×1.2…6→×1.8) — a
   wrong mental model. Scar: onboarding/doc copy must be verified rule-by-rule against the sim, not
   read-as-plausible.

5. **Medallion/GearIcon HC re-theme (`1774760`)** — icons.tsx static-palette read converted to
   usePalette() (spawn-task chip, done inline); byte-identical at defaults (resolvePalette identity);
   HC eyeball rides the batched device gate.

**Order-vs-synergy RESOLVED (`dd366f7`)**: human ruled "hide the chip" — orderHudView +
howToPlayTwists now gate on `DEMAND && !tagSynergyEnabled()` (scoring fires order ONLY when the
synergy flag is off); 3 store tests pin the flag world. Sim untouched.

**Round 2 (same day, human feedback on round 1):**
- **ICON-2/SUM-2 (`3cb726b`)**: ALL chrome emoji retired → MaterialCommunityIcons in accent-tinted
  circles; ONE central map `tokens.tagIcon` + `TagIcon` component (never per-screen icon names);
  supplier picker = fixed 96pt 3-col grid; summary captions = letterspaced `RECORD · 25` eyebrows;
  unlock teaser lost its left accent bar (human: "too bad"). glyphs.ts item-sprite fallbacks are
  CONTENT, not chrome — always exempt. Review caught 2 stragglers outside the audit list (menu
  daily button, share card) — scar: emoji sweeps must grep the whole src/app + src/ui, not a file list.
- **CAT-2 (`c5dcf76`)**: catalog = display case — ITEMS/COMBOS segmented tabs w/ counts, rarity
  legend, bands rarest-first over items.json `tier` (1 COMMON cream / 2 FINE sunlight wash /
  3 RARE brass double border / 4 HEIRLOOM gold bed + crown seal; discovered cards only);
  `?tab=combos` deep link; catalogBands pure.
- **@expo/vector-icons 15.1.1 installed — pnpm UNBROKEN**: run pnpm via
  `PATH=~/.nvm/versions/node/v23.3.0/bin:$PATH NODE_OPTIONS=--experimental-sqlite pnpm …`
  (pnpm 11.7 needs node:sqlite; flagged until node 23.4). Vitest still runs on v20.19.4.
- Open eyeball gates: summary (gameOver unreachable by deep link), HEIRLOOM framing on a real
  discovered heirloom, reveal animation post-run, HC pass.
**Round 4 (same day, human feedback on round 3 w/ mockup images):**
- **COMBO-2/LEG-1 (`0ec3e48`, 2 agent rounds)**: combos tab = MEDAL TROPHY SHELF (human picked
  variant 1 of 3 mockups; wood beds + recessed wells + layered-View medals w/ center art + ×N rim
  notch + glint sweep); detail modal w/ derived unlock sentence + `?combo=` link. Revision round
  from human: recipe diagram must use REAL gameplay cards (ItemSprite; tag slots = deterministic
  DISCOVERED example item + TagIcon corner chip, leak-proof by test) + contrast/depth polish on
  wood. **Mockup dressing REJECTED on honesty grounds: Premium banner, first-achieved dates,
  per-combo best scores — none exist in sim/save; never build UI promising unpaid things.**
  Legend = 4 equal flex band chips (LEG-1).
- **PROG-1 (`afd5200`)**: catalog header = Shelf Growth card (human's mockup pick) — 41-well mini
  shelf (7×6, 10pt cells, band-colored fills rarest-first), real n/41, NEXT ON THE SHELF strip =
  honest hook from nextUnlockTeaserView (+pure runs progress field) w/ band-completion fallback;
  mockup's %-milestone rewards NOT built (same honesty rule); iconed stats; ≤8 animators.
- **GLOS-1 (`ec34c4e`)**: "The Words" glossary page (WORDS chip) — 15 flag-gated terms via pure
  howToPlayGlossary(), number-free definitions, 9 withFlagWorld tests.

**Round 3 (same day, human feedback on round 2 — human said "it looks great" on rounds 1-2):**
- **HTP-2 (`33ec85c`)**: How-to-Play chip rail (LOOP·ITEMS·RULES·GLOW·COMBOS·RENT·TWISTS, derived
  from page defs), tap-to-jump + swipe-synced + auto-scrolls active chip into view (round-2 fix);
  section = doubles as rules reference. Chip TAP still needs one human tap.
- **CAT-3/COMBO-1 (`da46ddf`)**: item showcase modal (band-framed sprite bed, tags, value, WHAT IT
  DOES) on discovered stamps; NEW pure `src/state/describeItemRules.ts` verbalizes all 21 ItemRule
  kinds — reviewer spot-checked growsEachDay vs engine/scoring (fluent-but-wrong scar); sentences
  ship only for discovered items. Combos = 2-col RECIPE cards drawing center+adjacent as shelf
  wells (sprites/TagIcons) — "arrangement IS the combo" framing; mystery cards leak nothing.
  `?item=`/`?tab=` deep links kept as verification affordances (expo-router persists params across
  reloads — reuse `luckyshelf:///` first for fresh mounts; sim scar: re-opening a deep link on an
  already-mounted route does NOT re-navigate).
- **HC theming gap CLOSED (`e2d4266` THEME-1)**: B-M9 had themed screens, not shared components.
  Medallion/GearIcon (`1774760`) + SectionLabel (`fd328d6`) + the 11-component batch (sibling
  .styles.ts factories + componentStyles.test.ts two-palette byte-identity lock; Toggle's
  interpolateColor endpoints captured outside the worklet). The whole UI now themes — the batched
  HC device eyeball gate is finally meaningful end-to-end. Detection stays:
  `grep -rn "[{ ]palette[,}]" src/ui` must only hit tokens/prefs/tests.

Related: [[fabric-transform-gotchas]] [[b-m9-theme-migration]] [[expo-router-no-colocated-files]]
