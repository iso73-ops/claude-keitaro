# Claude Keitaro Installer for Windows PowerShell

$ErrorActionPreference = "Stop"

$SKILL_DIR = "$env:USERPROFILE\.claude\skills\keitaro"
$AGENT_DIR = "$env:USERPROFILE\.claude\agents"
$REPO_URL = "https://github.com/iso73-ops/claude-keitaro"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Claude Keitaro - Installer" -ForegroundColor Cyan
Write-Host "   Keitaro Tracker Skill for Claude" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is required but not installed." -ForegroundColor Red
    exit 1
}
Write-Host "  Git detected"

# Create directories
New-Item -ItemType Directory -Force -Path "$SKILL_DIR\references" | Out-Null
New-Item -ItemType Directory -Force -Path "$SKILL_DIR\scripts" | Out-Null
New-Item -ItemType Directory -Force -Path $AGENT_DIR | Out-Null

# Clone
$TEMP_DIR = Join-Path $env:TEMP "claude-keitaro-install"
if (Test-Path $TEMP_DIR) { Remove-Item -Recurse -Force $TEMP_DIR }

Write-Host "  Downloading Claude Keitaro..."
git clone --depth 1 $REPO_URL $TEMP_DIR 2>$null

# Copy main skill + references
Write-Host "  Installing skill files..."
Copy-Item "$TEMP_DIR\keitaro\SKILL.md" "$SKILL_DIR\SKILL.md" -Force
Copy-Item "$TEMP_DIR\keitaro\references\*.md" "$SKILL_DIR\references\" -Force

# Copy sub-skills
Write-Host "  Installing sub-skills..."
Get-ChildItem "$TEMP_DIR\skills" -Directory | ForEach-Object {
    $target = "$env:USERPROFILE\.claude\skills\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Copy-Item "$($_.FullName)\SKILL.md" "$target\SKILL.md" -Force
}

# Copy agents
Write-Host "  Installing subagents..."
Copy-Item "$TEMP_DIR\agents\*.md" "$AGENT_DIR\" -Force -ErrorAction SilentlyContinue

# Copy scripts
Write-Host "  Installing API helper..."
Copy-Item "$TEMP_DIR\scripts\*.py" "$SKILL_DIR\scripts\" -Force

# Install Python dependencies
Write-Host ""
Write-Host "  Installing Python dependencies..."
try {
    pip3 install -q requests 2>$null
    Write-Host "  Python dependencies installed"
} catch {
    try {
        pip install -q requests 2>$null
        Write-Host "  Python dependencies installed"
    } catch {
        Write-Host "  pip install failed - run manually: pip3 install requests" -ForegroundColor Yellow
    }
}

# Cleanup
Remove-Item -Recurse -Force $TEMP_DIR -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "  Claude Keitaro installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "  Setup:"
Write-Host '    $env:KEITARO_URL = "https://your-tracker.com"'
Write-Host '    $env:KEITARO_API_KEY = "your-api-key"'
Write-Host ""
Write-Host "  Then: claude → /keitaro setup"
