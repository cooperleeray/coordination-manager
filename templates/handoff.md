# HANDOFF (manual): <project> → <receiving session/surface>

Use this when the coordination ran **without a ledger** (e.g. in a chat) and `coord.py handoff` can't generate the packet. Fill in every section. "None" is a valid answer; a blank is not.

## 1. Receiving instructions
Read this file and every attached deliverable in full. If you can, run `coord.py init <project>` and load these facts into the ledger (`add` sessions, phases, relays, decisions, risks). Answer the fingerprint (§7) from the files, send the Operator a Handoff ACK, and wait for confirmation. Then continue at §2. Do not restart Phase 1.

## 2. Next actions (ordered)
1. …

## 3. Sessions
| Code | Surface / path / ID | Owns | State | Waiting on |

## 4. Phases and gates
| Phase | Owner | Status | Gate | Blocked by |

## 5. Relays
| Relay | Target | Status (drafted/sent/returned) | Awaited outputs |

## 6. Decisions
| ID | Question | Status | Ruling (verbatim) or recommendation |

## 7. Resume fingerprint
| # | Question | Answer |
| 1 | Current phase per session? | |
| 2 | Next action? | |
| 3 | Relays in flight? | |
| 4 | Open decisions (blocking)? | |
| 5 | Latest version of each deliverable? | |
| 6 | The rule most at risk right now? | |

## 8. Deliverables (attach the latest versions)
| File | Version | Audience | Status |

## 9. Not in any file
- Reasoning behind open recommendations:
- Operator preferences (format, effort, cadence, surfaces):
- Pitfalls learned:
- Not transferred (and why):
