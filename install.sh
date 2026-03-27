#!/usr/bin/env bash
set -euo pipefail

# Claude Keitaro Installer

main() {
    SKILL_DIR="${HOME}/.claude/skills/keitaro"
    AGENT_DIR="${HOME}/.claude/agents"
    REPO_URL="https://github.com/iso73-ops/claude-keitaro"

    echo "════════════════════════════════════════"
    echo "║   Claude Keitaro - Installer          ║"
    echo "║   Keitaro Tracker Skill for Claude    ║"
    echo "════════════════════════════════════════"
    echo ""

    # Check prerequisites
    command -v git >/dev/null 2>&1 || { echo "Error: Git is required but not installed."; exit 1; }
    echo "  Git detected"

    # Create directories
    mkdir -p "${SKILL_DIR}/references"
    mkdir -p "${SKILL_DIR}/scripts"
    mkdir -p "${AGENT_DIR}"

    # Clone or update
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf ${TEMP_DIR}" EXIT

    echo "  Downloading Claude Keitaro..."
    git clone --depth 1 "${REPO_URL}" "${TEMP_DIR}/claude-keitaro" 2>/dev/null

    # Copy main skill + references
    echo "  Installing skill files..."
    cp "${TEMP_DIR}/claude-keitaro/keitaro/SKILL.md" "${SKILL_DIR}/SKILL.md"
    cp "${TEMP_DIR}/claude-keitaro/keitaro/references/"*.md "${SKILL_DIR}/references/"

    # Copy sub-skills
    echo "  Installing sub-skills..."
    for skill_dir in "${TEMP_DIR}/claude-keitaro/skills"/*/; do
        skill_name=$(basename "${skill_dir}")
        target="${HOME}/.claude/skills/${skill_name}"
        mkdir -p "${target}"
        cp "${skill_dir}SKILL.md" "${target}/SKILL.md"
    done

    # Copy agents
    echo "  Installing subagents..."
    cp "${TEMP_DIR}/claude-keitaro/agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true

    # Copy scripts
    echo "  Installing API helper..."
    cp "${TEMP_DIR}/claude-keitaro/scripts/"*.py "${SKILL_DIR}/scripts/"
    chmod +x "${SKILL_DIR}/scripts/keitaro_api.py"

    # Install Python dependencies
    echo ""
    echo "  Installing Python dependencies..."
    if command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip3"
        command -v pip3 >/dev/null 2>&1 || PIP_CMD="pip"
        ${PIP_CMD} install --break-system-packages -q requests 2>/dev/null \
            || ${PIP_CMD} install -q requests 2>/dev/null \
            && echo "  Python dependencies installed" \
            || echo "  pip install failed — run manually: pip3 install requests"
    else
        echo "  pip not found — install deps manually: pip3 install requests"
    fi

    echo ""
    echo "  Claude Keitaro installed successfully!"
    echo ""
    echo "  Installed:"
    echo "    - 1 main skill (keitaro orchestrator)"
    echo "    - 7 sub-skills (setup, campaigns, flows, reports, optimize, landing, audit)"
    echo "    - 3 agents (campaign-analyzer, flow-optimizer, landing-generator)"
    echo "    - 5 reference files"
    echo "    - 1 API helper script"
    echo ""
    echo "  Setup:"
    echo "    1. Set environment variables:"
    echo "       export KEITARO_URL=\"https://your-tracker.com\""
    echo "       export KEITARO_API_KEY=\"your-api-key\""
    echo ""
    echo "    2. Start Claude Code:  claude"
    echo "    3. Run:                /keitaro setup"
    echo ""
    echo "  Commands:"
    echo "    /keitaro setup       - Connect to tracker"
    echo "    /keitaro campaigns   - Manage campaigns"
    echo "    /keitaro flows       - Manage flows"
    echo "    /keitaro reports     - View analytics"
    echo "    /keitaro optimize    - Auto-optimize"
    echo "    /keitaro landing     - Generate landings"
    echo "    /keitaro audit       - Health check"
    echo ""
    echo "  To uninstall: curl -fsSL ${REPO_URL}/raw/main/uninstall.sh | bash"
}

main "$@"
