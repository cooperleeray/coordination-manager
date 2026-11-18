# Features: reason and disposition

**Disposition key:** **Core** = in v1 and always on · **Opt-in** = in v1, used when the engagement needs it · **Deferred** = designed for, not built (with the trigger to build it) · **Rejected** = considered and excluded (with the reason).

## Carried over from the original protocol
| Feature | Reason | Disposition |
|---|---|---|
| Six gated phases (intake → grilling → diagnosis → plan → deliverables → loop) | Plans built before intake and clarification are wrong in ways that are expensive to undo | Core |
| Read-in-full rule, STOP if unreadable | Stops the CM from "summarizing" files it never read | Core |
| Truth precedence + "decided ≠ recommended ≠ written ≠ implemented" | The main source of cross-session drift is a recommendation treated as a decision | Core |
| Standard deliverable set (sequence, relays, operator guide, glossary, structure plan) | Separates what the agent needs from what the human needs; each file has one audience | Core |
| Read-only diagnostic relay | Verifies a working session's own understanding before planning around it | Core |
| Compaction trio + resume fingerprint | Context loss is silent; a fingerprint makes a wrong resume detectable in seconds | Core |
| Open-item triage tags | Routes each question to the session that should answer it, which shrinks the Operator's backlog | Core |

## New in the skill
| # | Feature | Reason | Disposition |
|---|---|---|---|
| 1 | **Ledger** (`coord/ledger.json`) as the CM's machine-readable state | In a chat-only CM, the state of 10+ relays and decisions lives in context and dies with compaction. A file survives, can be diffed, and lets tools check it | Core |
| 2 | **Workspace as its own git repo** (`coord.py init`) | Gives a full, timestamped history of the coordination; cheap to roll back; never mixed into working repos | Core |
| 3 | **Generated board** (`BOARD.md`) | One page that answers "where is everything?" without scrolling chats; generated, so it can't drift from the ledger | Core |
| 4 | **`next` command:** actionable / blocked-by / ready-to-send / decisions needed | Parallel work fails at the hand-offs; computing what can move from dependencies and open decisions removes guesswork | Core |
| 5 | **Linter:** undefined codes in deliverables, unknown targets, phase done with an open gate, rulings missing, dependency errors | Exactly the failure seen in practice: a plan revised in one file but not in the relays or glossary. Machine checks catch it before you do | Core |
| 6 | **Relay lifecycle** (drafted → sent → returned → reviewed → closed/superseded) with `expects` | Tells you at a glance what is in flight, and makes the return review objective (was each expected output delivered?) | Core |
| 7 | **WIP limit:** one relay in flight per session | Two outstanding relays to one session create crossed instructions and unclear state | Core (lint error) |
| 8 | **Return review checklist** | Consistent verification: completeness, scope, claim checks, drift, STOP respected | Core |
| 9 | **Conflict register + verbatim rulings** | Turns inter-session disagreements into explicit Operator decisions instead of silent overrides | Core |
| 10 | **Generated codes glossary** | The glossary always matches the ledger; no hand-maintained code list to go stale | Core |
| 11 | **CM self-checkpoint** (the CM's own CHECKPOINT + fingerprint) | The CM compacts too; it must resume as deterministically as the sessions it manages | Core |
| 12 | **Read-only reach** to granted folders and transcripts (Claude Code) | Lets the CM inspect repos, git logs and session transcripts directly, so you don't have to paste, while never writing outside `coord/` | Opt-in (paths granted per engagement) |
| 13 | **Risk register** reviewed at gates | Risks (cost, compaction, external dependencies) otherwise only appear when they bite | Opt-in |
| 14 | **Saved returns** (`coord/returns/`) | Keeps the evidence each review was based on; useful for audits and for resuming after a crash | Core |
| 15 | **Multi-project isolation** (one workspace per project) | Prevents cross-project contamination of codes and decisions | Core |
| 16 | **Install paths** (personal skill via clone or symlink, git subtree mirror, claude.ai upload; plugin marketplace deferred) | You work across surfaces; the same skill should follow you | Core |
| 22 | **Handoff / port session** (`coord.py handoff`, protocol §7E, `templates/handoff.md`) | Long coordinations outgrow one session or surface; moving them by hand loses decisions and relays in flight | Core (1.1.2) |
| 17 | **Scheduled check-ins** (e.g. a daily "what's next" via scheduled tasks) | Useful for long engagements where sessions run unattended | Deferred: trigger, an engagement with unattended sessions; uses the surface's scheduling tools, no code change needed |
| 18 | **Sync to GitHub Issues / Projects or Notion** | A visual board for teams | Deferred: trigger, a second human joins an engagement. The files stay the source of truth; a sync would be one-way export |
| 19 | **Relay packet export** (relay text + attachment list as one file per send) | Fewer manual steps when a relay needs several attachments | Deferred: trigger, frequent multi-attachment relays; easy addition to `coord.py` |
| 20 | **Automatic dispatch** (the CM sending relays to other sessions itself) | Would remove copy-paste | Rejected for now: it removes your gate between sessions, which is the core anti-drift control; revisit only for read-only relays with explicit per-engagement approval |
| 21 | **Database or server backend** | Not needed at this scale; JSON + git is portable, diffable and dependency-free | Rejected |
