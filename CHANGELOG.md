# Changelog

## 1.1.2: 2026-11-18
- **Handoff / port session:** `coord.py handoff [--to TARGET]` writes `HANDOFF-<date>.md` (receiving instructions, next actions, relays in flight, returns awaiting review, open decisions, conflicts, risks, checkpoint and fingerprint, deliverables, verbatim rulings, a section for what the ledger can't hold); protocol §7E (sending and receiving procedure; one active CM per project); `templates/handoff.md` for coordinations without a ledger; HOWTO §8.
- `tests/smoke.sh`: `mktemp` uses an explicit template under `$TMPDIR` (it works in sandboxes); also exercises `handoff`.
- `reference/protocol.md`: rule numbering fixed (10, 11, 12); heading v1.1.

## 1.1.1: 2026-11-18
- `SKILL.md` frontmatter: `license: MIT` and `metadata.version` (Agent Skills fields), so tools can read the version.
- `VERIFY.md` (an install check question + the scripted check) and `tests/smoke.sh` (offline smoke test of the ledger tool).

## 1.1.0: 2026-11-17
- **Public release layout:** the skill folder is the repository root (`SKILL.md` at root), so the repo can be cloned straight into a skills folder or mirrored with `git subtree`.
- Install via clone or symlink (`install.sh`); plugin manifests removed from v1 (they expect a `skills/` folder; may return later).
- MIT licence; docs for strangers; no private references.

## 1.0.0: 2026-11-17
- First release, generalized from a real multi-session architecture project.
- `SKILL.md` + `reference/protocol.md` (six gated phases, operating rules, relay lifecycle, return review, conflicts, cadence).
- Templates: relay (incl. diagnostic + compaction trio), checkpoint, continuation sequence, relays, operator guide, structure plan.
- `scripts/coord.py`: ledger (init/add/set/show/log), board, next, lint (codes, WIP limit, gates, dependencies, rulings), glossary.
