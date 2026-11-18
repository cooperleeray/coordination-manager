# Changelog

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
