---
name: product-roadmap
description: FJALË scope freeze + 4-phase roadmap (user-set 2026-07-16) — the north star for all future rounds
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a376e78-fea1-4e3f-b833-76f2dbc19ef6
  modified: 2026-07-20T05:52:01.690Z
---

**Promise:** "FJALË 36 — Pesë shkronja. Të 36-at vlejnë." Most trustworthy/polished Albanian daily word game, NOT most modes. Keep "Bright Coffee Break" visual direction — refine, never redesign.

**Phase 1 (beta):** fix round ✓ → git baseline ✓ → linguistic review (native, classify each of 76 words: accepted-guess / practice-answer / daily-quality) + versioned epoch system → trust UX (soft rejection copy "Kjo fjalë nuk është ende në listën tonë.", "Mungon një fjalë?" reporting, post-game word ratings: E drejtë / E vështirë por e drejtë / E rrallë / Nuk e njihja / Ka një gabim) → truthful stats (separate Daily/Archive/Practice/Overall; Daily = identity; Archive/Practice never worsen daily record) → restrained signature polish (digraph snap, passport stamp only on NEW letter, Besa seal only on genuine no-hint daily win, no recurring confetti).

**Phase 2 (launch) blockers:** 365 human-reviewed daily-quality answers, two-reviewer approval, versioned schedule (no historical drift), automated dup/token checks, editorial pipeline before pool < 90-day buffer. Launch package: descriptor "FJALË 36 — Wordle shqip me 36 shkronja" (don't rename yet), canonical URL/sitemap/structured data, OG artwork, PWA install clarity, privacy-respecting measurement, spoiler-safe sharing. Acceptance: digraphs/Ë/Ç self-explanatory to new players, all interactions at 320px, modes independent, archive can't hurt streak, midnight correct, keyboard/contrast/reduced-motion, no data loss, no repeats ≥1 year.

**Phase 3 (after stable launch):** Fjala pas fjalës learning cards (optional EN translation) → private family/friend circles (invite link, no account, hide boards till finished, recovery code) → Fjalori im (save words) → dynamic share cards (WhatsApp/Viber/IG).
Metrics gates before deeper investment: daily completion ≥70%, D1 ≥25%, D7 ≥12%, share ≥10%, legit rejected guesses <1%, challenge-start ≥35%.

**Phase 4:** labeled Gheg/Tosk/Arbëresh collections, classroom groups, community difficulty stats, weekly rare-word puzzle, one Albanian semantic puzzle; native apps/multiplayer only on proven demand.

**NEVER build:** coins/gems/streak-freezes/ad-hints, forced accounts, public leaderboards before circles, generic mode collections, unreviewed AI definitions/pronunciation, flag/folklore decoration, stranger matchmaking, guess-solver.

**Strategic order:** correctness → editorial trust → polished launch → discoverability → private sharing → language learning → community expansion.

**Status 2026-07-20 (launch-hygiene round shipped & deployed):** privacy page /privatesia.html live (footer+settings links), internal docs excluded from deploy, GitHub CI (Node 20/24), golden daily-schedule fixture 2026-07-16..2030-12-31 (regenerate ONLY when appending an epoch), lexicon validator in `npm run check`, report email centralized in src/config.js (branded address = pending user decision), invalid ?sfida= links now warn visibly. **The single blocker now is human:** two Albanian reviewers must work through editorial/review-2026-07.{md,csv} (76 pending answers, 75 nouns) and a second epoch must publish before bardhë repeats on 2026-09-16. See [[daily-pool-immutability]].
