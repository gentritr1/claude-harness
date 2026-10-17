---
name: lomn-roadmap-board
description: Live roadmap artifact for the LOMN port — URL, data doc, and the duty to update it as tasks land
metadata:
  type: reference
---
Live board: https://claude.ai/artifact/GyZGve8HMfmWHzJJhx3PyQ (owner asked 2026-10-07 for a real-time roadmap). Page source: scratch workspace `lomn-roadmap.html`; data = ONE db doc `board/state` (fields: updated_at, headline, overall_pct, milestones[], tasks[{status running|review|queued|waiting|done,label,note}], owner[], pace{finished[{id,hours}], in_progress[], remaining_units{low,high}, basis, caveat}, events[{t,text}] newest first). Rules: read view, write owner. Update with ArtifactData `update`/`set` on collection `board`, doc `state`, passing `if_version` (v1 at seed). Local copy: scratchpad/board-live.json, edited by scratchpad/board.py (event/task/addtask/ms/finish/headline/pct); then ArtifactData set with file_path + if_version (currently v53 — track the version returned by each write).
How to apply: after every task completion/review/dispatch, update tasks + events + updated_at (and milestone progress/hours, pace.finished when a milestone closes). ETA = remaining_units × median (low) / slowest (high) milestone hours — keep the caveat honest.
Related: [[lomn-web-port-probes]].
