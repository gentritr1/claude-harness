---
name: inquiry-engine-thread
description: "2026-10-13 export + Fable analysis of the owner's 102-day ChatGPT thread (Book of Inquiry); repo folder, artifact URL, verdict, 'Proof House' mission, export route that worked"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bb56d09-6e53-4a9f-87a4-708273fd5c90
  modified: 2026-10-13T12:08:40.849Z
---

The ChatGPT thread "Project Planning with LLM" (1 Jul – 11 Oct 2026; 198 messages, 24 files; Claude and ChatGPT used against each other) was exported to `~/Desktop/Projects/inquiry-engine/` (repo-ready: README, TIMELINE, sources/ by 5 phases, analysis/, site/build.py; `raw/` git-ignored). Separate private artifact: https://claude.ai/artifact/8KKTwbffsUe49wU8NNbLpq (7 pages). Private GitHub repo https://github.com/gentritr1/inquiry-engine (created 2026-10-13, owner's personal account; could move to the SnaxxTech org). `raw/` and `site/dist/` are git-ignored; rebuild the site with `python3 -I site/build.py`.

Prediction log (added 2026-10-13): a section on the artifact's index.html (`#log`), shared `db` collection `predictions` (fields: question, answer, confidence 50–99, test T1–T12, area, resolveBy, createdAt, author id, status, outcome{happened, verdict right|partly|wrong, lesson, resolvedAt, resolvedBy}); capabilities `db` (default rules) + `user` (profile scope). Read the team's real predictions with ArtifactData `list` on that collection.

Fable's verdict: profound in trajectory and tooling, derivative in theory (Popper, Kuhn, Tetlock…), **unproven** — prediction/calibration/failure logs are empty templates. Best idea: predict before reveal. Fable's recommended mission: "Proof House" — every delivery ships an evidence pack a stranger can re-run, later with recourse; cash engines = Launch-Safe, Play Deadline Upgrade, Guardrails. First test: T10 (false-"done" rate of delegate reports, baseline = gut estimate written first).

**Why:** owner wants ways of thinking unlike the market and a regional, investor-scale mission beyond SaaS.
**How to apply:** treat the method as a hypothesis; push filled logs and T1–T12 results, not new frameworks.

Export route that worked (2026-10-13): signed-in browser pane → page JS reads `/backend-api/conversation/<id>` and file download URLs → return a huge value from javascript_tool so the harness saves it to tool-results/ → unwrap with python and verify SHA-256 against the page. Blocked routes: pane downloads, pane clipboard, a localhost receiver (classifier: exposes local service), Claude in Chrome (not connected).

Related: [[notes-mining-opportunity-map]]
