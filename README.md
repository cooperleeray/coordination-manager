# coordination-manager

A Claude skill (Agent Skills format) that turns a Claude session into a **Coordination Manager**: a deterministic coordinator for complex work spread across many agent sessions and surfaces (Claude Code, claude.ai, Cowork, other agents).

It doesn't do the work. It keeps an exact, durable picture of every session, phase, gate, relay, decision, conflict and risk in a ledger; designs a gated plan to completion; writes self-contained relays; reviews every returned output; and stops drift. **You make the decisions; it recommends.**

## Install

**Claude Code (personal skill):**
```bash
git clone https://github.com/cooperleeray/coordination-manager.git ~/.claude/skills/coordination-manager
# or clone anywhere and run ./install.sh (symlinks into ~/.claude/skills)
```
Start a new Claude Code session and run `/coordination-manager`, or just ask Claude to coordinate your project.

**Other agents that support Agent Skills:** place this folder in that agent's skills directory.

**claude.ai:** zip this folder and upload it as a skill (Settings → Capabilities → Skills). The ledger script needs code execution.

**Inside another repo (mirror):**
```bash
git subtree add --prefix=skills/coordination-manager https://github.com/cooperleeray/coordination-manager.git main --squash
```

## What's inside
```
SKILL.md                 entry point (what Claude loads)
reference/protocol.md    the full operating protocol: rules, six gated phases, relay lifecycle, return review
templates/               relay, checkpoint, continuation sequence, relays, operator guide, structure plan
scripts/coord.py         ledger tool (Python 3.9+, stdlib only): init · add · set · board · next · lint · glossary
docs/HOWTO.md            step-by-step usage
docs/FEATURES.md         every feature, its reason and its status
```

## Quick start
```bash
mkdir -p ~/coordination/my-project && cd ~/coordination/my-project && claude
> /coordination-manager  Coordinate my project. Sessions: … Intake files: …
```

## Requirements
Python 3.9+ and git (for the ledger tool). Works without them in a reduced, Markdown-only mode.

## Licence
MIT. See `LICENSE`.
