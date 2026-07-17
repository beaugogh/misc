# misc

A personal collection of reusable **agentic skills** — workflows, setup recipes,
and runbooks I encounter in daily tasks, captured in a form an AI agent (or my
future self) can pick up and re-run.

## Structure

**My own skills** each live in their own folder under `skills/` and follow the
[Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) format.
Anthropic's official skills are mirrored separately as a git submodule under
`anthropic-skills/` (see below).

```
skills/
  <skill-name>/
    SKILL.md        # YAML frontmatter (name + description) + agent instructions
    ...             # optional bundled scripts, templates, references
```

- `SKILL.md` frontmatter:
  - `name` — lowercase-kebab-case, must match the folder name.
  - `description` — **when to use this skill**; the agent reads this to decide whether to invoke it.
- The body is progressive: context first, then concrete steps an agent can follow.

## Skills

| Skill | Purpose |
|---|---|
| [`install-claude-code-windows`](./skills/install-claude-code-windows) | Install Claude Code + Claude Code Router (CCR v1.x) on Windows behind a corporate firewall/VPN, routed to internal OpenAI-compatible endpoints. |
| [`pip-corporate-proxy`](./skills/pip-corporate-proxy) | Install Python pip packages behind a corporate proxy when pip stalls forever on large wheels or fails with 407 — downloads big wheels via curl (stall-killing + 407 retry), then pip-installs locally. |
| [`meeting-recording-analysis`](./skills/meeting-recording-analysis) | Analyze meeting recordings (video + audio) — transcribe speech to a timestamped transcript and extract key frames from screen-share video, then summarize / pull action items / answer questions. Built for WeLink recordings but works on any video. |
| [`git-corporate-proxy-lfs`](./skills/git-corporate-proxy-lfs) | Fix `git clone`/`pull` failures behind a corporate proxy on Windows — the 443 timeout, the schannel revocation-check hang, LFS crawling at KB/s, and interrupted clones leaving files as LFS pointers. |
| [`verify-model-endpoints`](./skills/verify-model-endpoints) | Smoke-test any OpenAI-compatible chat endpoint (DashScope, DeepSeek, Moonshot/Kimi, Zhipu/GLM, SiliconFlow, OpenRouter, OpenAI, local Ollama) — fire a prompt, print the reply. Per-provider credentials live in the skill's gitignored `.env`. |

## Anthropic skills (git submodule)

[`anthropic-skills/`](./anthropic-skills) is a git submodule tracking Anthropic's
official [skills repo](https://github.com/anthropics/skills). It provides
reference skills (artifacts, document formats, design, MCP building, etc.) that I
reuse rather than reinvent. The actual skills live under
`anthropic-skills/skills/`.

This keeps the two concerns separate: **my own skills** in `skills/`, **Anthropic's
upstream skills** in `anthropic-skills/` (read-only; pull updates from upstream,
don't edit in place).

### Updating the submodule to the latest upstream

```bash
git -C anthropic-skills checkout main
git -C anthropic-skills pull            # fetch latest upstream
git add anthropic-skills                # record the new pinned commit
git commit -m "Bump anthropic-skills submodule"
```

### Cloning this repo with the submodule

```bash
git clone --recurse-submodules <repo-url>
# or, for an existing clone:
git submodule update --init --recursive
```

## Using these skills

### In Claude Code
Copy (or symlink) a skill folder into your personal skills directory so Claude
Code can discover it:

```bash
# Windows (Git Bash)
ln -s "$(pwd)/skills/install-claude-code-windows" "$HOME/.claude/skills/install-claude-code-windows"
```

Then ask naturally — e.g. *"set up Claude Code on this Windows box behind the
corporate VPN"* — and the matching skill's `description` triggers it.

### Standalone
Every skill is self-contained. Open its `SKILL.md`, read the steps, and run any
bundled scripts directly — no agent required.

## Adding a new skill
1. `mkdir skills/<kebab-case-name>`
2. Add a `SKILL.md` with `name` (matching the folder) and a `description` that
   starts with **when to use it**.
3. Bundle any scripts/templates alongside it and reference them by relative path.
4. Add a row to the table above.
