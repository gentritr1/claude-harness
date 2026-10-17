---
name: tester-feedback-rulings-2026-10-13
description: "Owner rulings on the Testers Community feedback PDF (2026-10-13) — build system theme, Rate row, How-to-play row; prep daily/review/settings/share for flip; title \"Calm Arrow Puzzle\"; notifications still rejected"
metadata:
  node_type: memory
  type: project
  originSessionId: 7f3e90ac-14e8-4f0c-91cc-d27cf9b7988e
  modified: 2026-10-13T12:40:28.971Z
---

Source: ~/Desktop/com.danteb.arrows_feedback.pdf (generic Testers Community template; no bugs found).
Its "no tutorial" was true for the Play build they had: FTUE default-ON landed only 2026-10-06 (afb0819) on next-level.

Owner rulings 2026-10-13 (structured question):
- BUILD (each behind a default-OFF flag, screenshot acceptance first): theme Light/Dark/Follow phone
  (existing players keep their pick; new installs follow phone), "Rate Arrows" Settings row (opens Play page,
  not the quota-limited in-app review), "How to play" Settings row (replays the tutorial boards).
- PREP FOR FLIP (screenshot approval): META_DAILY, META_REVIEW_PROMPT, META_SETTINGS_SHEET, META_SHARE_CARD
  (share card now ruled IN — previously un-ruled, see [[owner-rulings-next-level-2026-09-16]]).
- LISTING: title "Arrows – Calm Arrow Puzzle" + natural keywords, still obeying ruling W7-9 banned phrases.
- Notifications: still REJECTED.

**Why:** re-asking wastes owner time; these supersede the 2026-09-16 "share card pending" status.
**How to apply:** treat any notification/reminder in a brief as a review failure; flips still need per-feature screenshot yes.

**Owner YES 2026-10-13 (later the same day):** all built features approved, notifications excluded. The vc17 release recipe (artifacts/ART-SKINS-08/release/build-aab17.sh) ALREADY exports DAILY, REVIEW_PROMPT, SETTINGS_SHEET and SHARE_CARD. Next recipe adds THEME_SYSTEM, SETTINGS_RATE, SETTINGS_HOW_TO_PLAY. Lesson: when saying whether a flag is "on", read the latest release recipe, not featureFlags.ts defaults (the approval page got this wrong). META_NAV_BAR_THEME is not yet approved (still verifying).

**Round 2 rulings 2026-10-13 ("make sure all feedback is addressed"):** META_NAV_BAR_THEME approved for release. BUILD behind flags: high contrast that FOLLOWS Android's "High contrast text" setting (no Settings row); Share on the campaign (level) win panel too. NOT NOW: daily leaderboards (Play Games sign-in, competitive vs calm), screen-reader playable board (would give answers away; needs its own design) — but every button/panel must be labelled. Performance monitoring = Play Android vitals (AAB carries proguard.map); in-app telemetry stays off.

**vc18 built 2026-10-13 22:46** from 45c08f6 (local tag release/vc18): ~/Desktop/arrows-vc18-45c08f6.aab, sha256 9f2ed02d…, archived in artifacts/ART-SKINS-08/release/. Recipe build-aab18.sh adds THEME_SYSTEM, SETTINGS_RATE, SETTINGS_HOW_TO_PLAY, NAV_BAR_THEME, HIGH_CONTRAST, SHARE_CARD_LEVEL (all owner-approved). prove-aab18.sh PROOF OK. Not uploaded (owner's step). Proof gotchas: `echo "$X" | grep -q` under pipefail fakes misses (use here-strings); Google test ids are ALWAYS in a release bundle via the ads library's TestIds table (vc15 too) — gate on "only table ids + no ADMOB_TEST_ADS in env", not on zero. vc17's AAB was never archived (prebuild --clean wiped it).
