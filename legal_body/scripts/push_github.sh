#!/usr/bin/env bash
# push_github.sh — push the legal_body module to your ORVION repo
# Usage: ./scripts/push_github.sh "feat(legal): ORVION Persona — Agent Incorporation Engine"
set -euo pipefail

MSG="${1:-feat(legal): ORVION Persona — Agent Incorporation Engine}"
BRANCH="${2:-feat/orvion-persona}"

git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
git add legal_body/ vitrine/ pitch_deck/ 2>/dev/null || git add legal_body/
git add main.py README.md 2>/dev/null || true
git commit -m "$MSG" || echo "(nothing to commit)"
git push -u origin "$BRANCH"
echo "✅ Pushed to branch '$BRANCH'. Open a PR to main when ready."
