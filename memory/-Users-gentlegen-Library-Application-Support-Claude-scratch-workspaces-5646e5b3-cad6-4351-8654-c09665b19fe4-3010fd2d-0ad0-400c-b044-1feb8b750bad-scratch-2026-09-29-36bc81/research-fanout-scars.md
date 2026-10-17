---
name: research-fanout-scars
description: Pattern → detection rule → brief update lines from the 2026-09-29/30 multi-agent idea research (tool starvation, picks overturned by primary data, generic-founder assumption, interrupted agents, full disk)
metadata:
  type: feedback
---

From the two-round idea research (round one 2026-09-29, round two 2026-09-30).

1. **A shared rate-limited tool starved nine agents for ~40 min.** My wrapper treated every HTTP error's `x-ratelimit-reset`
   header as a penalty and slept inside the global lock. *Rule:* only 429 is a rate limit; clamp any wait; never sleep long
   while holding a shared lock; readers must not wait behind a downloader. *Brief update:* before a fan-out, run the shared
   tool with 3+ parallel callers and one deliberately failing call.
2. **All three round-one picks fell once primary data was pulled** (Shopify App Store scan, the game licence PDF, a
   revenue base-rate sample). Round one had ranked them on second-hand evidence. *Rule:* before recommending a pick, fetch the
   one primary source that could kill it (licence text, marketplace scan, base rate). *Brief update:* every pick names its kill-check and who ran it.
3. **Round one treated the founders as generic.** Sibling project memories showed an existing studio with shipped Android
   games, a live Albanian word game, client work and AdMob via Poland. *Rule:* skim `~/.claude/projects/*/memory/MEMORY.md`
   before writing the first brief; score founder fit as its own column.
4. **Foreground agents were killed four times by the user's follow-up messages.** *Rule:* long research agents run in the
   background; tell agents to save notes within their first 20 tool calls.
5. **The disk was nearly full (other sessions' Android emulators), causing ENOSPC in three agents.** *Rule:* `df -h` before a
   fan-out; agents write notes atomically and keep caches small; tell the user early.
6. **Agents resumed with SendMessage after finishing can only hand back once;** their second delivery arrives as a plain
   message. Read it; do not wait for a second hand-back.

7. **The final fact-check's most common defect was a true fact on the wrong link** (3 of 9 findings) plus drift in qualifier
   words ("no app" for "no pollen app"; "best entrant" when a faster one existed). *Rule:* verifiers check the qualifier words
   and the link target of each claim, not only its numbers.
8. **A computed threshold hid its selection filter** (a median install pace of 830 only reproduced for apps at least three
   months old; all entrants gave 663). *Rule:* every computed threshold prints its filter and n next to the number.

**Why:** each cost real time or produced a wrong recommendation that had to be withdrawn.
**How to apply:** fold 1–5 into the next multi-agent research brief. Related: [[reddit-access-recipe]], [[idea-research-state]]
