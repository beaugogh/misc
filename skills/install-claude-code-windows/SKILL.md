---
name: install-claude-code-windows
description: Installs Anthropic's Claude Code CLI and the Claude Code Router (CCR, pinned to v1.x) on Windows 11 behind a strict corporate firewall / VPN, and routes Claude Code to internal OpenAI-compatible model endpoints. Use when setting up Claude Code on a Windows machine where the official install.ps1 fails (proxy returns an HTML block page) or where CCR v2's web UI hangs forever on "loading". Also use when CCR reports "No available models" — usually a BOM-corrupted config.json.
---

# Install Claude Code + CCR on Windows (Corporate Firewall Edition)

## Context
Standard installs break on locked-down corporate networks:

- The official `install.ps1` is fetched via `Invoke-RestMethod`, which the proxy intercepts and replaces with an HTML block page — the installer crashes. **Fix:** install via NPM, which honors proxy settings.
- CCR **v2.0+** forces a Web UI that pulls CDN assets and phones home; behind a firewall it hangs on "加载中" (loading) and ignores `config.json`. **Fix:** pin to the stable **v1.x** line.
- PowerShell's `Set-Content` / `Out-File` silently prepend a **UTF-8 BOM**. Node.js rejects BOM'd JSON, so CCR silently fails with "No available models". **Fix:** write `config.json` via Node's `fs.writeFileSync(..., 'utf8')`, which never emits a BOM.
- The default npm registry (`registry.npmjs.org`) is throttled to ~20 KB/s by the corporate firewall, causing the native binary download (76 MB for win32-x64) to time out. The postinstall script silently fails, leaving a placeholder `bin/claude.exe` that just prints an error. **Fix:** install via the **npmmirror** registry (`registry.npmmirror.com`), which is fast and reliable from within the corporate network.

## Prerequisites
- **Node.js v18+** (v22 LTS recommended). Check with `node -v`; install with `winget install OpenJS.NodeJS`.
- An **active VPN/intranet** connection that can reach the internal model endpoint.
- The internal endpoint must be **OpenAI-compatible** (`/chat/completions` shape).

## Required inputs — ask the user before running
You cannot proceed without these. Ask the user explicitly (do not guess):

1. **`api_base_url`** — the internal OpenAI-compatible endpoint, e.g. `http://internal.host:1234/chat/completions`.
2. **`api_key`** — the key for that endpoint, e.g. `sk-...`.
3. **Model names** the endpoint exposes (used in `Providers[].models` and the `Router` routes). Confirm at least one model for each of: `default`, `background`, `think`, `longContext`.

The bundled script has sensible placeholder defaults (`huawei` provider, qwen/glm/deepseek/kimi models) — treat them as **examples to replace**, not real values.

## How to run

### Option A — run the bundled script (fastest)
1. Read `setup.ps1` in this skill directory.
2. Edit the **CONFIG** block at the top with the user's `API_BASE_URL`, `API_KEY`, provider name, models, and route mappings. Use the Edit tool on the file — do not hand-type the whole script.
3. Have the user run it in PowerShell:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```
   (Suggest the `! ` prefix in this session, or have them run it in their own terminal — installing global npm packages and starting a long-lived proxy is best done in the user's shell, not via the agent.)

### Option B — run the steps manually
If the user prefers step-by-step control, run these in order:

```powershell
# 1. Claude Code CLI via npmmirror (default registry is throttled by the firewall)
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com

# 2. CCR pinned to v1.x (NOT v2 — its web UI hangs behind firewalls)
npm install -g "@musistudio/claude-code-router@1" --registry=https://registry.npmmirror.com
```

Then write a **BOM-free** `config.json` via Node (replace the placeholders). Keep `transformer: { use: ['openai'] }` minimal — complex schema objects fail v1 validation:

```powershell
node -e "const fs=require('fs'),path=require('path');const config={LOG:true,PORT:3456,API_TIMEOUT_MS:600000,Providers:[{name:'huawei',api_base_url:'YOUR_BASE_URL',api_key:'YOUR_KEY',models:['glm-5.2','deepseek-v4-flash'],transformer:{use:['openai']}}],Router:{default:'huawei,glm-5.2',background:'huawei,deepseek-v4-flash',think:'huawei,glm-5.2',longContext:'huawei,glm-5.2'}};const dir=path.join(process.env.USERPROFILE,'.claude-code-router');fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'config.json'),JSON.stringify(config,null,2),'utf8');console.log('wrote BOM-free config.json');"
```

## Verify
```powershell
claude --version   # must print e.g. "2.1.207 (Claude Code)"
ccr start          # must log "Loaded JSON config from ..."
ccr code           # launches Claude Code through the router
```
If `ccr start` says **"No available models"**, the config is BOM-corrupted or malformed — re-write it via the Node step above (never via `Set-Content`/`Out-File`).

## Alternative: Offline Sideload (if all registries are blocked)

If even npmmirror is inaccessible, you can sideload the native binary from an unrestricted network:

1. **On an unrestricted machine**, download the platform-specific package:
   ```powershell
   npm pack @anthropic-ai/claude-code-win32-x64@<VERSION>
   ```
2. **Transfer** the resulting `.tgz` to the corporate machine.
3. **On the corporate machine**, install locally into the main package directory:
   ```powershell
   cd (npm root -g)\@anthropic-ai\claude-code
   npm install ./path-to/anthropic-ai-claude-code-win32-x64-<VERSION>.tgz
   node install.cjs    # extracts the binary into bin\
   ```
4. **Verify** `claude --version` works.

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `install.ps1` returns HTML / crashes | Proxy blocks the download | Use `npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com` |
| `npm install` times out / hangs | Default registry throttled by firewall | Use `--registry=https://registry.npmmirror.com` flag |
| `'claude' is not recognized` after install | Native binary (76 MB) not downloaded — postinstall silently failed | Reinstall with `--registry=https://registry.npmmirror.com`; this downloads the platform-specific binary (e.g. `@anthropic-ai/claude-code-win32-x64`) as an optional dependency |
| `claude.exe` is not a valid Win32 application | `bin/claude.exe` is a placeholder shell script, not the real binary | Same fix — reinstall via npmmirror so the real native binary is pulled down |
| CCR web UI stuck on "loading" | v2.x CDN/telemetry blocked | `npm install -g @musistudio/claude-code-router@1` |
| "No available models" | `config.json` has a BOM, or bad JSON | Rewrite via `fs.writeFileSync(...,'utf8')` (Node), not PowerShell |
| v1 validation error | `transformer` block too complex | Use exactly `transformer: { use: ['openai'] }` |
| Port 3456 in use | Old CCR still running | `ccr stop`; if still stuck, find & kill that PID only (the bundled script no longer blanket-kills all `node` processes, to avoid nuking unrelated apps like VS Code) |

## Notes
- The config file lives at `%USERPROFILE%\.claude-code-router\config.json`.
- `ccr start` runs the proxy in the foreground; `ccr code` launches Claude Code pointed at it.
- The `Router` block maps Claude Code's request types to `<provider>,<model>` pairs — `background` is used for cheap/async tasks, `longContext` for huge contexts, `think` for reasoning, `default` for everything else.
