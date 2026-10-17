---
name: reward-path-2026-10-04
description: Reward path (direction A) is built and committed behind EXPO_PUBLIC_META_REWARD_PATH, default OFF; direction B (points and a shop) is next; Codex plan-audit pattern
metadata:
  type: project
---

**Owner rulings, 2026-10-04:**
- Direction A first: a fixed reward path with no currency. Direction B (spending points in a collection book) comes later, and A must not block it.
- Astra is a 3D model tool used for theme concepts only, never board art.
- Sound packs are parked.

**Screens approved from mockups:**
- the progress pill;
- the reveal card ("Play with X" switches style and plays on);
- the picker split into "Your styles" and "Coming up".

**Where it lives:**
- Spec: docs/superpowers/specs/2026-10-04-reward-path-design.md
- Plan: docs/superpowers/plans/2026-10-04-reward-path.md
- Code: commit 680370b. Review: ec90fa9 (REWARD-01).

**Pending:**
- A phone test build with the flag on.
- The owner's look review.
- The two amendments (picker-seen key; "unlocked on level L" subtitle) were stated to the owner but never explicitly approved.

**Delegation pattern:** Codex audited each plan task against the live code before implementing it. It stopped 6 times on real conflicts:
- spec vs plan;
- test-file identity;
- an RN import in the Node jest project;
- panel shadow;
- the "new" dot;
- a source-order anchor.

How to apply: briefs should tell Codex to stop and report conflicts. Answer each by amending the plan in a commit, not in chat, so the fix lives in the repo.

Related: [[art-skins-08-review]], [[codex-delegation-setup]]

**Direction B (collection book):**
- Built and committed: 853ec1a, plus the controller follow-up efbdada. Behind EXPO_PUBLIC_META_REWARD_BOOK, default OFF.
- Owner rulings: choice; no rewarded ads; petals equal points; prices 10/20/35; a 10-petal welcome gift; the path skips owned styles; layout B (tabs plus an album grid).
- Codex stopped 6 times on real plan conflicts; each was fixed by a plan/spec commit.

**Pending:**
- a phone build with the path and book flags on;
- the owner's look review.

**Seasons, owner-approved 2026-10-04 (bounded design, no spec file yet):**
- Seasonal styles are book-only and cost 20 petals.
- A catalogue `season` window uses the phone's date; owner choice "A": unbought styles leave the book and return each year; owned styles are kept forever.
- No new saved keys; new skin ids start at 18.
- The phone-date risk is accepted.
- It sits behind its own flag, inside the book flag.

**Year plan:**

| Pack | Window | Styles |
| --- | --- | --- |
| Halloween (first) | 1 Oct–7 Nov | Pumpkin, Ghost, Candy Corn |
| Snowy Winter | 1 Dec–15 Jan | |
| New Year | 26 Dec–10 Jan | |
| Sweetheart | 1–20 Feb | |
| Spring Garden | 15 Mar–30 Apr | |
| Summer Beach | 15 Jun–31 Aug | |
| Autumn Leaves (optional) | | |
| Lantern Nights (optional, Ramadan/Eid, no religious symbols) | | |

Flow: the owner generates concepts in Astra, then picks; Codex translates them into specs. If Halloween goes well, run the big all-year Astra prompt.

**2026-10-04:** the owner lost Astra access, so only the Halloween pack goes ahead for now (HALLOWEEN-01 brief: seasons feature + Pumpkin 18 / Ghost 19 / Candy Corn 20, concepts in artifacts/HALLOWEEN-CONCEPT-01). Other packs are paused. Option for later: Claude draws SVG concept sheets on a canvas using the big prompt's palettes.

**HALLOWEEN-01 committed (cd10d12) behind EXPO_PUBLIC_META_SEASONS**, done by a Claude subagent while Codex was unavailable.
- Dark tint #2A2140 fails the missed-mark 3:1 row; #221A36 passes (3.17). The stock #13111C is used meanwhile; owner ruling pending.
- Look finding: Pumpkin reads as orange beads (caterpillar) rather than a ribbed tube.

**Gotcha:** a session killed mid-contract-run leaves diagnostic classes in the product module and a skinTest type in android/. Always check the product module's file list before a normal build. The build script now refuses to build when they are present.

**2026-10-04 owner ruling change:** rewarded ads for petals are now WANTED (this reverses 'no rewarded ads for now'). The button sits in the Book and on the short-of-petals buy screen. Reward +3 petals per ad, cap 5 per day. No ad loaded: the button is greyed with 'No ad available right now' and never grants free petals. Behind its own flag. Implemented as PETAL-ADS-01.

**W3-19 (2026-10-06):** the owner ruled the 4 new shapes (House, Teacup, Bell, Umbrella) recognisable by his own judgement, not by a blind test; recorded in docs/silhouette-naming-2026-10-06.md. Next: admit the 4 ids to V2_ADMITTED_SHAPE_IDS (re-pin both v2 fingerprints), then W3-21 freeze prep. The flag flip still waits on W3-17 (first-time-player test) and the owner's yes.

**2026-10-06/07 seasonal:** owner picked Halloween+ Mummy A + Potion Slime B (ids 21/22 planned, Halloween book, 20 petals); Little Bat deferred until a general head-ears field exists (fangs via blush field read too weakly). Next season pack proposed: Winter/New Year (Candy Cane, Gingerbread, Snowman, Frosty Glass, Confetti Night), ~12-01..01-15, not started.
