---
name: tester-feedback-2026-09-07
description: "Testers Community report (no bugs, 4 enhancement asks) and how 1.4.0 (11) answered it; store copy now lives in store/"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8cc01d9f-953c-4c68-8443-67b91ef3a0c2
  modified: 2026-09-07T21:37:52.532Z
---

On 2026-09-07 the Play closed-test "Testers Community" report
(`~/Downloads/com.snaxxtech.geoguesser_feedback.pdf`) found **no crashes or
bugs** and asked for four things: ASO description, onboarding (interactive
tutorial + in-game tips + skip), feature-focused Play screenshots with captions,
and a "Rate your app" path (button + official In-App Review + sensible timing).
Extras: leaderboards/sharing, feedback mechanism, accessibility.

Answered on branch `feat/v1.4-tester-feedback` (version 1.4.0 / versionCode 11):
HowToPlay walkthrough, CoachTip, playerStore, expo-store-review with a pure
`shouldPromptForReview` rule, home-screen footer links, Share on results.
Store-side work (description, captions, "What's new") is drafted in
`store/listing.md` and `store/release-notes.md` — Play has no import, paste it.

Still open after that branch: real device screenshots for the 8-shot caption
plan, and the In-App Review dialog can only be seen on a Play-installed build.
Gentrit offered Higgsfield (image/video MCP) for onboarding art — not used yet;
emoji icons stand in until the flow is eyeballed.

**Why:** the report is the acceptance list for 1.4.0; the docs are where the
store copy must be edited so it doesn't drift from the app.

**How to apply:** when uploading 11, copy the "What's new" block from
`store/release-notes.md` (already ≤500 chars) and the listing text from
`store/listing.md`. See [[geoguesser-release-build-steps]].
