# How to use the Coordination Manager

## 1. Set up a coordination workspace (once per project)

Each project gets its own folder. Run the CM there, **not** inside the working sessions' repos.
```bash
mkdir -p ~/coordination/my-project && cd ~/coordination/my-project
claude
```
Why a separate folder: the CM needs its own durable state (ledger, board, deliverables, saved returns). Kept apart, it never pollutes a working repo and never gets compacted together with one.

## 2. Start an engagement

In the Claude Code session:
```
/coordination-manager
You are my Coordination Manager. I'm <name>.
The work: <objective; what "done" means>.
Sessions (as far as I know): <name — surface/path — owns — state>.
Intake: <paths to transcripts, plans, repo zips, specs, pending relays>.
Read-only paths you may inspect directly: <e.g. ~/repos/x, ~/.claude/projects/-Users-me-repos-x/>
```
The CM creates `coord/` and runs the phases, **stopping at every gate**:

| Phase | You do | The CM delivers | Gate |
|---|---|---|---|
| 1 Intake & ACK | supply files and paths | read ledger, objective restatement, session map, findings, what's missing | confirm or correct |
| 2 Grilling | answer ≤12 numbered questions (or "use your recommendation") | recorded answers; open items become decisions (OD-n) | answers given |
| 3 Diagnosis | paste read-only diagnostic relays into each working session; paste returns back | review + corrections | review agreed |
| 4 Plan | read the summary | sessions, phases, gates, relays, decisions, durability, structure | approve summary |
| 5 Deliverables | review files; answer ODs | sequence file(s), relays, operator guide, glossary, structure plan | approve / rev 2 |
| 6 Loop | send relays, paste returns | verify → next relay / correction / decision | until completion |

## 3. The daily loop

1. Ask: **"What's next?"** The CM runs `coord.py next` and shows what's actionable, what's blocked (and why), relays ready to send, and decisions needed.
2. **Send** the relay it names (from `coord/deliverables/<PROJECT>-RELAYS.md`). Tell the CM "R4 sent". It marks it `sent`.
3. **Paste the return.** Tell the CM "R4 returned:" plus the output, or point it to a file. It saves it to `coord/returns/`, runs the return review (are the expected outputs there? did it stay in scope? do the claims check out?), and gives a verdict: proceed, correct, or escalate.
4. **Decide** when asked. Your ruling is recorded verbatim in the ledger.
5. Open `coord/BOARD.md` any time for the one-page picture.

Rule of thumb: **one relay in flight per session.** The linter enforces it.

## 4. Commands the CM uses (you can run them too)

```bash
S=~/.claude/skills/coordination-manager/scripts/coord.py
python3 $S next                       # what can move now
python3 $S board                      # regenerate coord/BOARD.md
python3 $S lint                       # consistency check (exit 1 on errors)
python3 $S glossary                   # regenerate the codes glossary
python3 $S add relay R5 target=S1 phase=P1 purpose="Release docs" expects="commits;report"
python3 $S set relay R5 status=sent
python3 $S set decision OD-2 status=decided ruling="Yes, route PRODUCT items to S3"
python3 $S show phases
```
Code conventions the linter understands: `S1` sessions · `P3`, `P8b` phases · `R4`, `R9b` relays · `OD-6` decisions · `G-P3` gates · `C-2` conflicts · `RK-1` risks · `D-1` deliverables. Project-specific codes (e.g. `RP-1`) are declared as `term` entries.

## 5. Compaction and resume

- **The CM itself:** before every STOP it updates the ledger and board, rewrites `coord/CHECKPOINT.md` with a resume fingerprint, and commits `coord/`. After any compaction or in a new session, `/coordination-manager` finds the ledger and resumes from the checkpoint.
- **Working sessions:** use the compaction trio in `templates/relay.md`: checkpoint relay → `/compact <focus>` → verification relay. If the fingerprint doesn't match, don't continue. Start a fresh session with the verification relay instead.

## 6. Using it on claude.ai instead of Claude Code

The protocol works the same. Differences: the CM can't read your local folders, so you upload files. The ledger lives in the chat's sandbox, so ask the CM to send `ledger.json` and `BOARD.md` to you after each gate and re-attach them in a new chat. For long engagements, prefer Claude Code.

## 7. Tips

- Put every session's ID, path and resume command in the ledger (`where=`). It saves you hunting for them after a crash.
- Name deliverables `<PROJECT>-…` so files from different engagements never mix.
- When another session proposes overriding an approved decision, say "log a conflict". Don't forward it.
- Keep `coord/` in git. `git log` then holds the full history of the coordination.
- Turn this skill's protocol updates into versions (CHANGELOG) so old engagements stay readable.
