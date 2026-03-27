#!/usr/bin/env bash
set -euo pipefail

echo "Uninstalling Claude Keitaro..."

# Remove main skill
rm -rf "${HOME}/.claude/skills/keitaro"

# Remove sub-skills
for skill in keitaro-setup keitaro-campaigns keitaro-flows keitaro-reports keitaro-optimize keitaro-landing keitaro-audit; do
    rm -rf "${HOME}/.claude/skills/${skill}"
done

# Remove agents
for agent in campaign-analyzer flow-optimizer landing-generator; do
    rm -f "${HOME}/.claude/agents/${agent}.md"
done

echo "Claude Keitaro uninstalled."
