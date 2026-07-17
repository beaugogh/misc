# misc

A personal collection of reusable **agentic skills** — workflows, setup recipes,
and runbooks I encounter in daily tasks, captured in a form an AI agent (or my
future self) can pick up and re-run.

## Structure

**My own skills** each live in their own folder under `skills/` and follow the
[Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) format.
Two external collections are mirrored as git submodules —
`anthropic-skills/` (Anthropic's official skills) and `superpowers/` (obra's
methodology skills) — see [below](#external-skill-collections-git-submodules).

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

## External skill collections (git submodules)

Two upstream skill collections are tracked as git submodules, kept separate from
my own `skills/` (read-only; pull updates from upstream, don't edit in place):

| Submodule | Upstream | Pins | What's in it |
|---|---|---|---|
| [`anthropic-skills/`](./anthropic-skills) | [anthropics/skills](https://github.com/anthropics/skills) | `main` | Anthropic's official reference skills — artifacts & document formats (`pdf`, `docx`, `pptx`, `xlsx`), design (`brand-guidelines`, `canvas-design`, `frontend-design`, `theme-factory`), `mcp-builder`, `skill-creator`, and more. Skills live under `anthropic-skills/skills/`. |
| [`superpowers/`](./superpowers) | [obra/superpowers](https://github.com/obra/superpowers) | `v6.1.1` | A software-development *methodology* for coding agents — process skills like `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `requesting-code-review`, `subagent-driven-development`. Skills live under `superpowers/skills/`. Also ships hooks/plugin manifests for several agent harnesses. |

> **Note on superpowers:** as a submodule checked out at a subdirectory, its
> hooks/plugin manifests stay inert. To actually *activate* the methodology in
> Claude Code, install it as a plugin separately (`/plugin install superpowers@…`,
> see the [superpowers README](./superpowers/README.md#installation)). The
> submodule here is for reference and keeping the source on hand.

### Updating a submodule to the latest upstream

```bash
# e.g. for anthropic-skills (tracks main); for superpowers, checkout the release tag or main
git -C <submodule-dir> checkout main
git -C <submodule-dir> pull            # fetch latest upstream
git add <submodule-dir>                # record the new pinned commit
git commit -m "Bump <submodule-dir> submodule"
```

### Cloning this repo with submodules

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
