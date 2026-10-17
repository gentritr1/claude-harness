---
name: autonomy-and-knowledge-capture
description: User wants Claude to proceed autonomously on the LOMN port (no confirmations except last resort), experiment/optimize from measured data, and capture RE/porting knowledge in the repo
metadata:
  type: feedback
---
Proceed without asking for confirmation; keep fixing, optimizing and experimenting. Ask only as a last resort.

**Why:** user said 2026-10-07: "make sure that u dont need my confirmation until u just keep fixing and optimizing this and its the last resort … keep this knowledge inside a repo … reverse engineering skills, porting … security audits and performance audits … optimize them not just from thin air without substance".

**How to apply:** approve own plans/reviews and continue; still confirm outward-facing/irreversible steps (deploy, making repo public, running the original exe — never run it myself). Every optimization must cite measured data (perf/history.jsonl, metrics.json, determinism runs). Keep a knowledge base in the repo (playbooks + a reusable skill) and run security + performance audits with evidence. Related: [[claude-only-implementers]], [[lomn-web-port-probes]].
