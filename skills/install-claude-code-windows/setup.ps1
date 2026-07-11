# =====================================================================
# Claude Code + Claude Code Router (CCR) setup — Corporate Firewall Edition
#
# Edit the CONFIG block below, then run in PowerShell:
#     powershell -ExecutionPolicy Bypass -File setup.ps1
#
# Why this script exists (see SKILL.md for full context):
#   - install.ps1 is proxy-blocked  -> install Claude Code via NPM
#   - default npm registry throttled -> use npmmirror registry
#   - CCR v2 web UI hangs on VPN     -> pin CCR to v1.x
#   - PowerShell writes a UTF-8 BOM  -> write config.json via Node (no BOM)
# =====================================================================

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# CONFIG — replace with your internal endpoint + credentials
# ---------------------------------------------------------------------
$API_BASE_URL  = "http://YOUR_INTERNAL_ENDPOINT:1234/chat/completions"
$API_KEY       = "sk-YOUR_API_KEY"
$ProviderName  = "huawei"

$Models = @("qwen3.7-max", "glm-5.2", "deepseek-v4-flash", "kimi-k2.6")

$RouteDefault     = "$ProviderName,glm-5.2"
$RouteBackground  = "$ProviderName,deepseek-v4-flash"
$RouteThink       = "$ProviderName,glm-5.2"
$RouteLongContext = "$ProviderName,glm-5.2"
# ---------------------------------------------------------------------

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }

# 0. Preflight: Node.js is required (v18+, v22 LTS recommended)
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js not found. Install it first:" -ForegroundColor Red
    Write-Host "  winget install OpenJS.NodeJS" -ForegroundColor Yellow
    exit 1
}

# 0b. Ensure npm global bin is in PATH for this session
$npmBin = (npm prefix -g) | Out-String | ForEach-Object { $_.Trim() }
if ($env:Path -notlike "*$npmBin*") {
    $env:Path = "$env:Path;$npmBin"
    Write-Host "Added $npmBin to PATH for this session." -ForegroundColor DarkGray
}

# 1. Stop any running CCR (clean — does NOT blanket-kill all node.exe,
#    which would nuke VS Code / other node apps)
Write-Step "Stopping any running CCR instance"
if (Get-Command ccr -ErrorAction SilentlyContinue) {
    ccr stop 2>$null
} else {
    Write-Host "ccr not installed yet — skipping stop." -ForegroundColor DarkGray
}

# 2. Install Claude Code CLI via npmmirror (default registry is throttled by the firewall)
Write-Step "Installing Claude Code CLI via NPM (npmmirror)"
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com

# 2b. Verify the native binary landed
$claudeCmd = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claudeCmd) {
    Write-Host "ERROR: 'claude' command not found after install." -ForegroundColor Red
    Write-Host "  The npm global bin directory may not be in your PATH." -ForegroundColor Yellow
    Write-Host "  Run: `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')" -ForegroundColor Yellow
    exit 1
}
$claudeVer = & claude --version 2>&1
Write-Host "  claude --version => $claudeVer" -ForegroundColor Green

# 3. Install CCR pinned to stable v1.x (v2 web UI hangs behind firewalls)
Write-Step "Installing Claude Code Router (v1.x)"
npm install -g "@musistudio/claude-code-router@1" --registry=https://registry.npmmirror.com

# 4. Write a BOM-free config.json via Node.
#    PowerShell's Set-Content/Out-File prepend a hidden UTF-8 BOM that
#    Node rejects -> CCR silently fails with "No available models".
#    Node's fs.writeFileSync(..., 'utf8') never emits a BOM.
Write-Step "Writing BOM-free config.json via Node"

# ConvertTo-Json collapses a single-element array to a bare string, so
# force the array form when there's only one model.
if ($Models.Count -eq 1) {
    $modelsJson = "[`"$($Models[0])`"]"
} else {
    $modelsJson = $Models | ConvertTo-Json -Compress
}

$nodeScript = @"
const fs = require('fs');
const path = require('path');
const config = {
  LOG: true,
  PORT: 3456,
  API_TIMEOUT_MS: 600000,
  Providers: [{
    name: '$ProviderName',
    api_base_url: '$API_BASE_URL',
    api_key: '$API_KEY',
    models: $modelsJson,
    transformer: { use: ['openai'] }   // keep minimal — complex schemas fail v1 validation
  }],
  Router: {
    default: '$RouteDefault',
    background: '$RouteBackground',
    think: '$RouteThink',
    longContext: '$RouteLongContext'
  }
};
const dir = path.join(process.env.USERPROFILE, '.claude-code-router');
fs.mkdirSync(dir, { recursive: true });
const target = path.join(dir, 'config.json');
fs.writeFileSync(target, JSON.stringify(config, null, 2), 'utf8');   // utf8 => NO BOM
console.log('=> Wrote ' + target);
"@
node -e $nodeScript

# 5. Start the router service (in background so the script can continue)
Write-Step "Starting the router service"
Start-Process -FilePath "ccr" -ArgumentList "start" -WindowStyle Hidden
Start-Sleep -Seconds 2

# 6. Final verification
Write-Step "Verification"
$ccrStatus = & ccr status 2>&1
if ($ccrStatus -match "Running") {
    Write-Host "  CCR is running." -ForegroundColor Green
} else {
    Write-Host "  WARNING: CCR does not appear to be running. Try 'ccr start' manually." -ForegroundColor Yellow
}

Write-Host "`nDone. Launch Claude Code through the router with:" -ForegroundColor Green
Write-Host "    ccr code`n" -ForegroundColor Green
