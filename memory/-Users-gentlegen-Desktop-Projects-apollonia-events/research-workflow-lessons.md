---
name: research-workflow-lessons
description: What the 30-agent Apollonia research pass taught about vetting kill-rates, invented numbers, and font-fix assumptions
metadata:
  type: feedback
---

From the 2026-09-09 "next level" research workflow (30 agents, 63 ideas, 4 killed).

**Pattern → detection rule → brief update:**

1. **A 2-of-3 majority kill rule produces a 6% kill rate.** Reviewers strongly prefer REVISE to
   KILL, so almost everything survives and the survivor list reads as "validated" when it is only
   "well specified". *Rule:* state the kill rate in the deliverable and describe survivors as
   "specified well enough to argue about". *Brief update:* require each vetter to nominate its
   single weakest idea for KILL regardless of majority, so the tier has a floor.

2. **Agents invent audience statistics.** A wave rationale asserted "roughly 70% of this audience
   is on a phone" for a site with **zero analytics**. Nothing in the repo could produce that
   number. *Rule:* grep every generated deliverable for `N% of (audience|users|traffic)` and
   `roughly N%` before shipping. *Brief update:* "if you state a percentage about visitors, name
   the query that produced it or write UNKNOWN."

3. **The obvious fix may not exist.** The Greek section markers (Α΄ Β΄ Γ΄ Δ΄) fall back to Times.
   The natural fix — `subsets: ["greek"]` — is impossible: **Cormorant Garamond has no Greek
   subset**, nor do Cormorant or Cormorant Infant. Only EB Garamond does. *Rule:* before
   recommending a font/library/API fix, query the provider (`curl` the Google Fonts CSS API and
   read the subset comments) rather than assuming availability. Verified by observation, not memory.

4. **Attributing bundle weight needs a bundle analysis.** I nearly reported "Sentry is 130 KB of
   your bundle"; that chunk contains React DOM too. *Rule:* a chunk containing a library's name is
   not evidence of that library's size — it is a measurement task.

See [[stale-design-docs-trap]] for the fifth lesson: a repo doc propagated a wrong premise into
eleven agent prompts before anyone checked it.
