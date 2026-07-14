# misc

A personal collection of reusable **agentic skills** — workflows, setup recipes,
and runbooks I encounter in daily tasks, captured in a form an AI agent (or my
future self) can pick up and re-run.

## Structure

Each skill lives in its own folder under `skills/` and follows the
[Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) format:

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
