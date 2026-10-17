---
name: deeper-version-planning-prompt
description: "Owner wants a \"deeper, not bigger\" pass on every plan or design before it is presented — 4 questions, then rewrite"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 085731ec-3fcf-4cd7-933c-43b37ee3cc1b
  modified: 2026-10-15T12:41:15.403Z
---

When planning or designing, run a "deeper version, not a bigger one" pass before presenting the plan:
1. What would a top professional in this field do here that the owner did not ask for?
2. What is the rawest material they would start from, instead of an already-digested summary?
3. Which specific methods and tools would they use?
4. What, other than the owner or Claude, would show the result is right (an independent check)?
Then rewrite the plan or brief to ask for exactly that, keeping the scope the same: deeper, not wider.

**Why:** The owner saw this prompt (from a 15 Oct 2026 X post) and asked on 15 Oct 2026 to "use this more often when we plan things". On Proof Runner it changed the design: hash the raw per-fault trace rather than only the counts, add a fresh random seed alongside the regression seeds, and require a second-machine re-run.

**How to apply:** Now a global rule in ~/.claude/CLAUDE.md §6 ("Deeper, not bigger", owner approved 15 Oct 2026 for every project). This note keeps only the origin and the Proof Runner example.
