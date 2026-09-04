# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## What this repo is

A curated collection of reusable **agentic artifacts** — instruction documents (skills), browser-automation adapters (OpenCLI plugins), and setup recipes — designed for AI agents to pick up and re-run. Targets the Huawei corporate environment (strict firewall/VPN, proxy, Windows 11 + Git Bash).

This is **not a buildable software project**. It is a knowledge repository of Markdown instruction documents with occasional bundled scripts.

## Repository layout

```
skills/              — Own agent skills (growing collection)
opencli-plugins/     — OpenCLI browser-automation adapters
mcps/                — MCP servers (remote install-free + local uvx-launched), packaged for any agent
scripts/             — Repo-level tooling (catalog generation)
anthropic-skills/    — Git submodule (at skills/anthropic-skills): Anthropic's official skills (read-only)
superpowers/         — Git submodule (at skills/superpowers): obra's methodology skills (read-only)
mattpocock-skills/   — Git submodule (at skills/mattpocock-skills): Matt Pocock's engineering skills (read-only)
.venv/               — Python venv (torch, whisper, imageio-ffmpeg) for ML-heavy skills
.env                 — Per-provider API credentials (gitignored, never commit)
CATALOG.md           — Auto-generated catalog of ALL skills + OpenCLI plugins + MCP servers
```

## Skill format

Each skill is a folder containing a `SKILL.md` with YAML frontmatter:

```yaml
---
name: kebab-case-name      # must match the folder name
description: |              # when to use this skill — agent reads this to decide invocation
  Use when ...
---
(instruction body — context first, then concrete steps)
```

Bundled scripts/templates live alongside the `SKILL.md` and are referenced by relative path. Every skill is self-contained and can be followed without an agent.

## Commands

```bash
# Regenerate the catalog (required after adding/removing any skill or plugin)
./scripts/generate-catalog.sh

# Update all submodules to latest upstream main
git submodule update --remote
git add skills/anthropic-skills skills/superpowers skills/mattpocock-skills
git commit -m "Bump submodules to latest upstream main"

# Clone with submodules
git clone --recurse-submodules <repo-url>
# or for existing clone:
git submodule update --init --recursive

# Build an OpenCLI plugin (TypeScript → ESM, committed so install works without esbuild)
cd opencli-plugins/<plugin>
esbuild <cmd>.ts --outfile=<cmd>.js --format=esm --platform=node

# Install an OpenCLI plugin locally
opencli plugin install file://$(pwd)/opencli-plugins/<name>

# Python venv (for meeting-recording-analysis, pip-corporate-proxy, etc.)
source .venv/Scripts/activate
```

## Adding content

### New skill
1. `mkdir skills/<kebab-case-name>`
2. Add `SKILL.md` with `name` (matching folder) and `description` (start with **when to use it**)
3. Bundle scripts/templates alongside, reference by relative path
4. Run `./scripts/generate-catalog.sh` to update `CATALOG.md` (the catalog is the single source of truth — no manual README table row needed)

### New OpenCLI plugin
1. `opencli plugin create <name> --dir opencli-plugins/<name>`
2. Replace sample commands with real adapters
3. Declare the command surface in `opencli-plugin.json` under a `commands` array (`name`, `description`, `args`, `columns`) — this is the catalog source of truth
4. Compile: `esbuild <cmd>.ts --outfile=<cmd>.js --format=esm --platform=node`
5. Verify: `opencli plugin install file://$(pwd)/opencli-plugins/<name>` then `opencli <name> <command>`
6. Run `./scripts/generate-catalog.sh` to update `CATALOG.md`

### New MCP server
1. `mkdir mcps/<kebab-case-name>`
2. Add `mcp-server.json` (manifest: `name`, `transport` (`remote` or `local`), and for remote `url`/`headers` or for local `command`/`environment`/`runtime`; `auth`, `network.no_proxy`, and a `tools[]` array with `name`/`args`/`output_fields`) — this is the catalog source of truth. One manifest = one server; a server may expose one or many tools in `tools[]`. Local servers must declare a `runtime` block (requires/install/note) stating their prerequisites.
3. Write a pure-stdlib `<name>.py` wrapper that speaks the MCP protocol — Streamable HTTP for remote (urllib + json), stdio JSON-RPC for local (subprocess + json). Must run with no `pip install` for the wrapper itself. Remote wrappers bypass the corporate proxy for intranet hosts themselves (use a no-proxy opener, don't rely on `NO_PROXY` env); local wrappers augment `NO_PROXY` for the uvx subprocess.
4. Add `claude-code.mcp.json` and `opencode.mcp.json` ready-to-load configs
5. Add a `README.md` (model on `mcps/huawei-w3-search/README.md` for remote, `mcps/huawei-codehub/README.md` for local — local must state runtime prerequisites up front)
6. Run `./scripts/generate-catalog.sh` to update `CATALOG.md`

## Key conventions

- **Submodules are read-only.** Never edit files inside `skills/anthropic-skills/`, `skills/superpowers/`, or `skills/mattpocock-skills/` directly.
- **Line endings:** All text files normalized to LF (`.gitattributes`). Shell scripts are `text eol=lf`, PowerShell is `text eol=crlf`.
- **LFS:** Harvested paper outputs under `skills/harvest-ai-papers/output/harvested/**` are tracked with Git LFS.
- **Credentials:** `.env` at repo root holds API keys (gitignored). Skills that need credentials use per-skill `.env` files (also gitignored). Use `.env.example` as a template.
- **Catalog is generated:** `CATALOG.md` is auto-generated from `SKILL.md` frontmatter (skills) and `opencli-plugin.json` `commands` arrays (plugins). Never edit it by hand — always run `./scripts/generate-catalog.sh`.
- **Deprecated/in-progress skills** in `skills/mattpocock-skills/` (under `deprecated/` or `in-progress/` subdirs) should be skipped unless explicitly requested.
