#!/bin/sh
# Smoke test: init a throwaway workspace, add entries, render the board, lint, write a handoff packet. No network, no git.
set -eu
HERE="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d "${TMPDIR:-/tmp}/cm-smoke.XXXXXX")"
trap 'rm -rf "$T"' EXIT
C="python3 $HERE/scripts/coord.py --dir $T/coord"
$C init smoke --no-git >/dev/null
$C add session S1 name=demo where=local owns=demo >/dev/null
$C add phase P1 title=demo owner=S1 gate=G-P1 >/dev/null
$C add relay R1 target=S1 phase=P1 purpose=demo expects="report" >/dev/null
$C board >/dev/null
test -f "$T/coord/BOARD.md"
$C lint >/dev/null
$C handoff --to "smoke-target" >/dev/null
ls "$T/coord/" | grep -q '^HANDOFF-.*\.md$'
echo "SMOKE PASS"
