# <PROJECT> / <SESSION>: continuation sequence v<N> (agent-readable)

**Audience:** the agent in <session>. Only this session's work.
**Issued by:** <Operator>, <date> (rev <n>).
**Relationship to the session's own plan:** merge this into <its plan file> as plan v<N>. That file stays the single plan the agent maintains. Save this file verbatim under <answers folder>.

## A. Resume protocol additions
1. Run the existing resume protocol.
2. Read CHECKPOINT.md; answer its fingerprint; **the files win over the summary**.
3. Treat every STOP as a possible compaction point: plan + checkpoint current and committed first.

## B. Standing rules added
1. <terminology crosswalks across sessions>
2. <triage tags required on every open item>
3. <publication / push rule>
4. <anything frozen until a later phase>

## C. Sequence
| Phase | Title | Old step | Status |
|---|---|---|---|
| P0 | Pre-compaction: diagnostic, registers, checkpoint, compact, verify | new | IN PROGRESS |
| P1 | … | … | NEXT |

### P<n> <title>
- **Input:** … · **Do:** … · **Outputs:** … · **Gate P<n>:** … · checkpoint refresh

## D. Checkpoint standard: see CHECKPOINT template (fingerprint required)
## E. Open-item triage tags
| Tag | Meaning | Resolved by | When |
|---|---|---|---|
| ARCH / CORE | … | Operator in this session | … |
| PRODUCT / EXTERNAL | … | <other session> | … |
| DEFER | later, with an owner and a trigger | Operator confirms | any time |
| INPUT | waits on material | the named input | its phase |
| DONE | answered (cite where) | — | — |
## F. Drift watchlist
## G. QA additions
## H. Change log
