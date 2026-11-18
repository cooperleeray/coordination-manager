# Relay template

Copy into `<PROJECT>-RELAYS.md` as a fenced block. Register it in the ledger with `coord.py add relay R<n> target=S<n> phase=P<n> expects="a;b;c" changes_files=no`.

```
<Operator> here. <Purpose in one line>. [<phase code> / <relay code>]

Read first, in full (STOP and tell me if anything can't be read): <files, in order>.
Save this message verbatim to <path> before any other work.

Do:
1. <bounded action>
2. <bounded action>

Do not: <no file changes | no edits outside X | no push/deploy | do not start the next phase>

Outputs: <files + report headings, matching the ledger's `expects`>
QA: <checks the session runs before reporting>
Then: report <items> and STOP.
```

## Read-only diagnostic relay (Phase 3 standard)
```
<Operator> here. Bounded diagnostic pause. Do NOT change, create or commit any file. Do NOT continue your task.

Ground everything in your files (plan, decision log, checkpoint, git log/status) and your full transcript at <path>, not your recollection.

Report:
1. WHERE WE ARE: step, status, last commit, git status, my last unanswered message and your last question (verbatim).
2. WHAT IS DONE: per round or step, one line each, with proof (a commit or file).
3. WHAT COMES NEXT: the next 5 actions and what each waits on.
4. OPEN ITEMS: counts per group; orphans (in documents but not in the register, and the reverse).
5. DRIFT: directions raised but unfinished, superseded statements still present, things only in the transcript or memory. Check at minimum: <list>.
6. SELF-AUDIT: decision log vs documents vs transcript mismatches.
7. TERMINOLOGY RISKS for other sessions.
8. CONFIDENCE: what you're unsure of, and why.
End with "Diagnostic complete. No files changed." and STOP.
```

## Compaction trio (for any Claude Code working session)
1. **Checkpoint relay:** "Write CHECKPOINT.md to the standard (incl. the resume fingerprint), commit, report the hash and the fingerprint, STOP."
2. **Command:** `/compact Preserve: phase <P>, state in <files> (committed; the repo is the source of truth over this summary). Keep: standing rules, the last unanswered message, the next action. Drop tool output and file bodies.`
3. **Verification relay:** "You were compacted. Read <plan>, CHECKPOINT.md, git log -5. Answer the fingerprint from the files, not the summary. Report any summary-vs-repo disagreement. STOP."
