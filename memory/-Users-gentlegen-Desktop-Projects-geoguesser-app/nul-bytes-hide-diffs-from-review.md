---
name: nul-bytes-hide-diffs-from-review
description: A text file with raw NUL bytes is diffed by git as binary — a test deletion inside it was invisible to the diff-based review package
metadata:
  type: feedback
---

On 2026-09-16 an implementer's fix quietly deleted two existing unit tests from `tests/releaseGuard.test.ts`,
and the diff-based review package showed only `Bin 7108 -> 20705` for that file: it contained raw NUL
bytes (a fixture byte string), so `git diff` treated it as binary. The re-reviewer only found the deletion
with `git diff --text`. A mutant then survived because the deleted test had been its only guard.

**Why:** superpowers' review-package and every reviewer read `git diff` output. Any text file git classifies
as binary is a blind spot where test deletions and weakened assertions pass unseen — the exact red flag in
the owner's CLAUDE.md §6 ("a diff that quietly deletes, weakens, or bypasses an existing test").

**How to apply:** before dispatching a reviewer, byte-scan the changed text files for NUL — `git diff --numstat`
alone is NOT enough: git's binary heuristic only reads the first 8000 bytes, so a NUL further in slips past it
(confirmed on the A2 fix: numstat was numeric while grep still called the file binary). Also check
`git diff --numstat BASE HEAD | awk '$1=="-"'` for files git already hides; regenerate with `git diff --text`.
Root cause seen: unicode escapes typed into an agent's tool call were decoded into raw bytes — tell implementers
to write NUL as an escape inside the file and to byte-scan after writing fixtures. In test fixtures,
write NUL as an escape (`'\0'`, `'\x00'`, `Buffer.from([0])`), never a raw byte. A byte-level scan of tracked
text files: `git ls-files -z | python3 -c` counting `b"\x00"` per file (BSD/ugrep `grep -P '\x00'` missed it here).

Related: [[playerstore-wipes-profile-on-slow-read]], [[gradle-bundle-ignores-expo-public-env]]
