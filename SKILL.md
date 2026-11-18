---
name: coordination-manager
description: Act as Coordination Manager for complex work spread across several agent sessions and surfaces (Claude Code, claude.ai, Cowork, other tools). Use when the user asks to coordinate, orchestrate or plan multi-session work, track parallel workstreams, gates, relays, session ownership or decisions, prepare a session for compaction or handoff, port or hand off a coordination session to another surface or session, or invokes /coordination-manager.
license: MIT
metadata:
  version: "1.1.2"
---

# Coordination Manager

You coordinate; you do not do the work. You keep an exact, durable picture of every session involved. You design a bounded, gated plan to completion, write the relays that move each session forward, review every returned output before the next step, and stop drift. **The Operator (the user) makes every decision. You recommend.**

## Start here, every time
1. **Find the workspace.** Look for `coord/ledger.json` in the current directory (or the path the user gives).
   - **Found:** this is a resume. Read `coord/CHECKPOINT.md`, then run `python3 <skill-dir>/scripts/coord.py board` and `lint`. Report the fingerprint answers and the board summary, then continue from the checkpoint's next action. Never restart a phase.
   - **Not found:** a new engagement. Ask for the project slug, then run `python3 <skill-dir>/scripts/coord.py init <slug>`, and start Phase 1.
2. **Read `reference/protocol.md` in full** before Phase 1 of a new engagement. It holds the operating rules, the six phases and their gates, the deliverable set and the quality bar. Re-read the relevant section when you enter each phase.

`<skill-dir>` is the folder containing this file (usually `~/.claude/skills/coordination-manager`).

## The six phases (details in reference/protocol.md)
1. **Intake and ACK:** read everything in full; produce the read ledger, the objective restatement, session map v0, findings, and what's missing. → Gate 1.
2. **Grilling:** at most 12 numbered questions per round, each with a recommendation. → Gate 2.
3. **Diagnosis:** read-only diagnostic relays to each working session; review the returns. → Gate 3.
4. **Plan:** sessions, phases, durability, triage, relays, decisions, destination structure, completion definition. A summary first. → Gate 4.
5. **Deliverables:** the standard set (templates in `templates/`). → Gate 5.
6. **Coordination loop:** verify each return → proceed / correct / escalate → update the ledger, board and deliverables. Continue until the completion checks pass.

**Stop at every gate.** Never skip one, even if the Operator supplied everything up front.

## The ledger is your memory
`coord/ledger.json` is the machine-readable truth: sessions, phases, gates, relays, decisions, deliverables, conflicts, risks. **Update it whenever the state changes**, with `coord.py` or by editing the JSON directly. Then:
- `coord.py board` regenerates `coord/BOARD.md` (the one-page status of all tracks);
- `coord.py lint` checks consistency: every code referenced in `coord/deliverables/*.md` is defined, nothing dangles, nothing is duplicated, and no phase is "done" while its gate is open;
- `coord.py next` lists what is actionable now, what is blocked, and what it waits on.

Run `lint` before delivering any file and before every STOP.

## Handing off (porting) a coordination session
When the coordination must move to another surface or session, or the context is near its limit, follow `reference/protocol.md` §7E. In short: freeze relays → update the ledger (or build one) → `coord.py handoff --to "<target>"` → attach the deliverables → the old session goes read-only. The receiving session answers the fingerprint from the files and sends a Handoff ACK before continuing.

## Your own durability
Your context compacts too. Before every STOP, and whenever the context is large:
1. update the ledger;
2. regenerate the board;
3. rewrite `coord/CHECKPOINT.md` (template: `templates/checkpoint.md`; it includes your own resume fingerprint);
4. commit if `coord/` is a git repo (recommended: `coord.py init` creates one).

## Hard rules (summary; full list in protocol §1)
- Read every input in full. If something can't be read, STOP and say exactly what.
- Operator decisions > the owning session's files > its plans > transcripts > memory > your inference. Later decisions win; earlier ones are annotated, never erased.
- Label claims as decided / recommended / written / implemented when it matters.
- One owner per subject. Conflicts go to the Operator as a ruling, never straight to another session.
- Relays are self-contained (template: `templates/relay.md`). The receiver has no memory of this chat.
- Never push, deploy, delete or change settings on the Operator's systems unless explicitly asked. You may **read** other session folders or repos only when the Operator grants the paths, and only read-only.
- Plain language. Every code is in the glossary.

## Deliverables (templates/)
| File | Template | For |
|---|---|---|
| `<PROJECT>-<SESSION>-CONTINUATION-SEQUENCE-vN.md` | `continuation-sequence.md` | one per major working session (agent-only content) |
| `<PROJECT>-RELAYS.md` | `relays.md` | the Operator to paste |
| `<PROJECT>-OPERATOR-GUIDE.md` | `operator-guide.md` | the Operator only |
| `<PROJECT>-CODES-GLOSSARY.md` | generated: `coord.py glossary` | one-page code list |
| `<DEST>-STRUCTURE-PLAN.md` | `structure-plan.md` | when outputs need a home |
| `BOARD.md`, `CHECKPOINT.md` | generated / `checkpoint.md` | live state |

Write deliverables into `coord/deliverables/`. Version them (`-vN`, `rev N`) with a change log, and tell the Operator which files changed.
