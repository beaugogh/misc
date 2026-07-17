# misc

A personal collection of reusable **agentic skills** — workflows, setup recipes,
and runbooks I encounter in daily tasks, captured in a form an AI agent (or my
future self) can pick up and re-run.

## Structure

**My own skills** each live in their own folder under `skills/` and follow the
[Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) format.
Three external collections are mirrored as git submodules —
`anthropic-skills/` (Anthropic's official skills), `superpowers/` (obra's
methodology skills), and `mattpocock-skills/` (Matt Pocock's engineering
practice skills) — see [below](#external-skill-collections-git-submodules).

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
| [`karpathy-guidelines`](./skills/karpathy-guidelines) | Behavioral guidelines to reduce common LLM coding mistakes — think before coding, simplicity first, surgical changes, goal-driven execution. Vendored (MIT) from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), derived from Andrej Karpathy's observations on LLM coding pitfalls. |
| [`caveman`](./skills/caveman) | Ultra-compressed communication mode — cut output tokens ~65% by speaking terse "caveman" while keeping all technical substance, code, and errors byte-for-byte exact. Intensity levels (lite/full/ultra/wenyan), with an auto-clarity carve-out that drops terse mode for security warnings and irreversible actions. Vendored (MIT) from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). |
| [`caveman-compress`](./skills/caveman-compress) | Compress natural-language memory files (`CLAUDE.md`, todos, docs) into caveman format to save input tokens — preserves code blocks, URLs, paths, and frontmatter exactly; backs up the original as `FILE.original.md`. Bundles a `scripts/` package (`python3 -m scripts <file>`) that calls Claude via CLI or `ANTHROPIC_API_KEY`. Vendored (MIT) from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). |

## External skill collections (git submodules)

Three upstream skill collections are tracked as git submodules, kept separate from
my own `skills/` (read-only; pull updates from upstream, don't edit in place):

| Submodule | Upstream | Tracks | What's in it |
|---|---|---|---|
| [`anthropic-skills/`](./anthropic-skills) | [anthropics/skills](https://github.com/anthropics/skills) | `main` | Anthropic's official reference skills — artifacts & document formats (`pdf`, `docx`, `pptx`, `xlsx`), design (`brand-guidelines`, `canvas-design`, `frontend-design`, `theme-factory`), `mcp-builder`, `skill-creator`, and more. Skills live under `anthropic-skills/skills/`. |
| [`superpowers/`](./superpowers) | [obra/superpowers](https://github.com/obra/superpowers) | `main` | A software-development *methodology* for coding agents — process skills like `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `requesting-code-review`, `subagent-driven-development`. Skills live under `superpowers/skills/`. Also ships hooks/plugin manifests for several agent harnesses. |
| [`mattpocock-skills/`](./mattpocock-skills) | [mattpocock/skills](https://github.com/mattpocock/skills) | `main` | Hands-on *engineering practice* skills from Matt Pocock — `tdd`, `code-review`, `diagnosing-bugs`, `codebase-design`, `domain-modeling`, `implement`, `research`, `prototype`, `wayfinder`, `to-spec`/`to-tickets`. Skills live under `mattpocock-skills/skills/` (grouped into `engineering/`, `productivity/`, `misc/`, `personal/`). |

> **Note on superpowers & mattpocock-skills:** as submodules checked out at a
> subdirectory, their hooks/plugin manifests stay inert. To actually *activate*
> them in Claude Code, install them as plugins separately (e.g.
> `/plugin install superpowers@…`, or `npx skills@latest add mattpocock/skills` —
> see their respective READMEs). The submodules here are for reference and
> keeping the source on hand.

### Updating the submodules (all three track upstream `main`)

All three submodules are configured to track their upstream `main`, so a single
command updates all of them:

```bash
git submodule update --remote       # fetch + move each checkout to main's tip
git add anthropic-skills superpowers mattpocock-skills
git commit -m "Bump submodules to latest upstream main"
git push
```

To update just one, name it: `git submodule update --remote mattpocock-skills`.
To only *check* for updates without moving anything, `git -C <submodule-dir> fetch origin`
then compare `git rev-list --count HEAD..origin/main`.

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
