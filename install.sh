#!/usr/bin/env bash
# Install coordination-manager as a personal Claude Code skill (symlink by default; --copy for a frozen copy).
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DEST="$DEST_DIR/coordination-manager"
mkdir -p "$DEST_DIR"
if [ "$SRC" = "$DEST" ]; then echo "Already installed in place: $DEST"; exit 0; fi
if [ -e "$DEST" ] || [ -L "$DEST" ]; then mv "$DEST" "$DEST.bak.$(date +%s)"; echo "Backed up existing $DEST"; fi
if [ "${1:-}" = "--copy" ]; then cp -R "$SRC" "$DEST"; echo "Copied to $DEST"; else ln -s "$SRC" "$DEST"; echo "Linked $DEST -> $SRC"; fi
chmod +x "$SRC/scripts/coord.py"
echo "Done. Start a new Claude Code session and run: /coordination-manager"
