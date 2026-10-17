---
name: scratch-cleanup-after-verify
description: Delete frozen verification copies and their caches as soon as the verification is confirmed and ledgered
metadata:
  type: feedback
---
After a controller verification (frozen `git archive` copy, fresh-cache decomp, mutation scratch tree, review scratch copy) is confirmed and its result is written to the SDD ledger, delete that copy and any cache made for it (build/, node_modules (real dirs only, never via a symlink), Ghidra caches/project clones). Keep only small evidence: *.log, REPORT/report files, scripts. Do it in the same step that records the result.

**Why:** owner, 2026-10-08: scratch grew to 12 GB of stale verification copies and the disk hit 100 % full ("make sure u remove those after confirmation so it doesnt pile like this").

**How to apply:** remove with LITERAL absolute paths (the safety check refuses `rm -rf "$VAR/$x"` loops); list the dirs first, then one `rm -rf /abs/path/a /abs/path/b` call.  every verification step ends with: record result in ledger → `rm -rf` the copy's directory (check `-L` first, list paths in a cleanup log) → note freed space. Keep a copy only while its review/fix loop is still open. See [[lomn-process-experiments]].
