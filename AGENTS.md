# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## What this repo is

A curated collection of reusable **agentic artifacts** — instruction documents (skills), browser-automation adapters (OpenCLI plugins), and setup recipes — designed for AI agents to pick up and re-run. Targets the Huawei corporate environment (strict firewall/VPN, proxy, Windows 11 + Git Bash).

This is **not a buildable software project**. It is a knowledge repository of Markdown instruction documents with occasional bundled scripts.

## Repository layout

```
skills/              — Own agent skills (growing collection)
opencli-plugins/     — OpenCLI browser-automation adapters
scripts/             — Repo-level tooling (catalog generation)
anthropic-skills/    — Git submodule: Anthropic's official skills (read-only)
superpowers/         — Git submodule: obra's methodology skills (read-only)
mattpocock-skills/   — Git submodule: Matt Pocock's engineering skills (read-only)
.venv/               — Python venv (torch, whisper, imageio-ffmpeg) for ML-heavy skills
.env                 — Per-provider API credentials (gitignored, never commit)
CATALOG.md           — Auto-generated catalog of ALL skills + OpenCLI plugins
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
git add anthropic-skills superpowers mattpocock-skills
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

## Key conventions

- **Submodules are read-only.** Never edit files inside `anthropic-skills/`, `superpowers/`, or `mattpocock-skills/` directly.
- **Line endings:** All text files normalized to LF (`.gitattributes`). Shell scripts are `text eol=lf`, PowerShell is `text eol=crlf`.
- **LFS:** Harvested paper outputs under `skills/harvest-ai-papers/output/harvested/**` are tracked with Git LFS.
- **Credentials:** `.env` at repo root holds API keys (gitignored). Skills that need credentials use per-skill `.env` files (also gitignored). Use `.env.example` as a template.
- **Catalog is generated:** `CATALOG.md` is auto-generated from `SKILL.md` frontmatter (skills) and `opencli-plugin.json` `commands` arrays (plugins). Never edit it by hand — always run `./scripts/generate-catalog.sh`.
- **Deprecated/in-progress skills** in `mattpocock-skills/` (under `deprecated/` or `in-progress/` subdirs) should be skipped unless explicitly requested.
