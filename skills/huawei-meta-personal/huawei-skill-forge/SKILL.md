---
name: huawei-skill-forge
description: Auto-evolve the user's skill ecosystem by analyzing personal data traces (opencode/codeagent sessions, git commits, WeLink chat, token metrics, 3ms/Wiki authoring). Extracts long-term memory, creates and updates skills, recommends/installs market skills, and checks skill versions. Invoke when the user says "evolve", "分析session", "update skills", "review recent work", "自演进", "总结一下最近的工作", etc.
---

# huawei-skill-forge

Auto-evolves the user's skill ecosystem from personal data traces. Adapted from — but not
identical to — the source `auto-evolve` skill studied at
`C:\Users\b00563677\Downloads\auto-evolve\SKILL.md` (v0.0.1, 706 lines).

## What it does
1. **Update long-term memory** — extract preferences, environment, decisions, patterns worth
   remembering; write to the shared memory skill.
2. **Create new skills** — for recurring patterns or complex task flows (≥5 tool rounds).
3. **Update existing skills** — from user feedback and new experience.
4. **Recommend & install skills** from the agentcenter market (user-confirmed).
5. **Check skill versions** and offer updates (user-confirmed).

## Scope boundary
Writes ONLY to: `auto-evolve-created-*` skills, this skill's own SKILL.md, and the shared
memory skill. Must NOT modify third-party or manually-installed skills.

## Data sources

### Shared timestamped activity traces (the personal data traces)
All 7 emit *occurrence* (when) and *category* (what kind). They are the input this skill
mines for patterns, feedback, and recurring workflows.

| Source | Access | Status (2026-07-25) | What P1 extracts |
|--------|--------|---------------------|------------------|
| opencode/codeagent sessions | see "Codeagent dual instances" below — TWO stores | both present | corrections, tool-call sequences, feedback, recurring workflows |
| git / CodeHub commits | `git log --author --since --until`; project dirs from session `directory`/`cwd` or memory | git present | recurring dev patterns, work verification |
| welink-cli (WeLink chat) | `welink-cli im query-recent-conversation` / `query-history-message`; needs auth + NO_PROXY for `open.inner.welink.huawei.com` and `cmc.centralrepo.rnd.huawei.com` | **not installed** (source gives no install instructions) | decisions, TODOs, meeting conclusions |
| nga.cmd (token metrics) | `nga.cmd session list` / `metrics <id>` | **legacy only** — see dual-instances | AI-usage stats (optional for P1) |
| CloudDevOps Wiki | `clouddevops-wiki` skill **or** CloudDevOps REST API (**NOT MCP**) | not available (access path unknown) | professional domain, methodology |
| 3ms | existing `huawei-3ms` plugin (search + read) — **not used by source skill, our addition** | plugin present in this repo | knowledge-sharing patterns |
| W3 search | "MCP 工具或 API" | not available (access path unknown) | background / professional context |

**Local-CLI-to-remote-service ≠ local store.** welink-cli and nga.cmd hit remote services
needing auth + proxy. Group by where data lives / what network+auth it needs, not where the
binary sits. Only the opencode/codeagent session stores are genuinely local.

### P1-only tooling and reference (not data traces — not shared with huawei-retro-scope)
| Source | Access | Status | Purpose |
|--------|--------|--------|---------|
| agentcenter CLI | npm `@aimarket/agentcenter` from `cmc.centralrepo.rnd.huawei.com`; Node ≥18 | not installed (Node v22 present) | skill marketplace: search, install, version-check |
| agentcenter-skill-finder | `agentcenter skill add agentcenter-skill-finder -g` | not installed | bridge: installs skill-creator (3-hop chain: agentcenter → skill-finder → skill-creator) |
| skill-creator | `agentcenter-skill-finder install skill-creator` → `{SKILLS_DIR}/skill-creator/` | not installed | scaffolds new skills (`scripts/init_skill.py`). **NOT the same as `anthropic-skills/skills/skill-creator` submodule** — that one lacks `init_skill.py` and has a different workflow. Detection-by-filename collision risk: the Anthropic version passes the `{SKILLS_DIR}/skill-creator/SKILL.md` check but lacks `init_skill.py`. |
| project norm files | `for_ai_to_read/`, `.cursorrules`, `CLAUDE.md` (per-project, static) | varies by project | read to judge rule-violations; "rule exists ≠ rule effective". No timestamps. |

The skills repertoire is **bidirectional within P1**: a write sink for new skills AND a read
source for market version-diff / memory-dedup. It is not a data trace (emits no timestamped
user activity).

## Codeagent dual instances (verified 2026-07-25)

The user has TWO codeagent installations with completely different data stores, schemas, and
skills dirs. The environment is mid-migration (migration flag dated 2026-07-23). The source
auto-evolve skill only knows about the legacy store — it is incomplete for this environment.
**Both stores must be read.**

### Legacy instance (`nga` command)
- **Install dir:** `D:\CodingAgentCLI\` (launcher: `nga.cmd` → `ngagent.cmd` → `bin\codeagent.exe`)
- **Version:** 1.2602.12-IN.1
- **Data store:** opencode-style SQLite DB at `~/.local/share/opencode/db/ngagent.db`
  (resolved via `NGA_DATA_HOME` env var → `XDG_DATA_HOME`)
  - Verified present: 1 session, 97 messages, 313 parts
  - Schema: `session` (id, title, time_created millis, time_updated, directory, ...),
    `message` (id, session_id, time_created millis, data JSON with role),
    `part` (id, message_id, session_id, time_created millis, data JSON with type)
  - Timestamps: INTEGER milliseconds
- **Skills dir:** `~/.config/opencode/skills/` (1 skill: lingxi-miner)
- **`nga.cmd` referenced in the source skill = THIS legacy instance.** When the source says
  `nga.cmd session list` / `nga.cmd metrics <id>`, it's the legacy codeagent's CLI. Whether
  the new `codeagent` command has equivalent metrics subcommands is unverified.

### New instance (`codeagent` command)
- **Install dir:** `D:\CodingAgentCLI3\` (launcher: `codeagent.bat` → `bin\codeagentcli.exe`)
- **Version:** 1.2605.03-IN.1
- **Data store:** file-based under `~/.cac/`
  - Sessions: per-project JSONL at `~/.cac/projects/<project-slug>/<session-uuid>.jsonl`
    - Verified: 3 session files across 3 projects
    - Schema: Claude Code-style JSONL, one JSON per line. Types: `user`, `assistant`,
      `tool_use`, `tool_result`, `thinking`, `text`, `system`, `file-history-snapshot`,
      `custom-title`, `agent-name`, `queue-operation`, `last-prompt`, `file_unchanged`,
      `create`, `message`
    - Key fields: `type`, `uuid`, `parentUuid`, `timestamp` (ISO 8601 string), `sessionId`,
      `cwd`, `gitBranch`, `version`, `message.role`, `message.content`, `permissionMode`,
      `isUserPrompt`
    - Timestamps: ISO 8601 strings (e.g. `"2026-07-23T08:57:07.631Z"`) — NOT millis
  - Session index: `~/.cac/projects/observable-cac.jsonl` (sessionId → sessionLogPath)
  - Prompt history: `~/.cac/history.jsonl` (display text, timestamp millis, project, sessionId)
  - **Per-project memory:** `~/.cac/projects/<slug>/memory/` — MEMORY.md + `feedback_*.md`
    files. **The new codeagent already has its own feedback-harvesting memory system** —
    per-project, not global. This overlaps with P1 and is a key integration point (don't
    build a parallel system that conflicts).
  - Settings: `~/.cac/settings.json`; migration flag: `~/.cac/.migration-flag.json`
    (2026-07-23, migrated 0 items — fresh start, not a data migration)
- **Skills dir:** `~/.cac/skills/` (9 skills: sdd-*) ← **primary going forward**

### Three skills dirs, not one
- `~/.config/opencode/skills/` — legacy (1 skill)
- `~/.cac/skills/` — new codeagent (9 skills) ← primary going forward
- `~/.claude/skills/` — claude code (1 skill)
Decide which to scan/write; `~/.cac/skills/` is primary, but legacy skills may still be
referenced.

## Methodology (key insights from the source skill)

1. **Two-axis incremental analysis.** "New since last watermark" has two independent
   dimensions, both must be queried:
   - Axis 1: new sessions — `session.time_created > last_timestamp`
   - Axis 2: new messages in OLD sessions — `session.time_created <= last_timestamp` AND
     `message.time_created > last_timestamp`
   Querying only `session.time_created` silently drops every message added to an ongoing
   session after the last run. Join `message`/`part` on `time_created` and trace back via
   `session_id`. **Differs per store** (see below).

2. **Historical bug retrospection is mandatory, not optional.** Every run re-scans ALL
   history (not just incremental) for reported bugs and verifies each was fully fixed.

3. **"Fix a bug = fix three (now four) things":** code/script + SKILL.md constraint rule +
   already-broken state + project norm files. Missing any → the bug recurs.

4. **"Rule exists ≠ rule effective":** if the AI keeps violating a rule that's already
   written, strengthen it (promote to step-0 gate, add ❌ counter-examples, split it) — don't
   skip because "the rule is there." AI violating an existing rule once is enough to trigger
   strengthening.

5. **Forced generalization (举一反三).** 4-dimension checklist per pattern found:
   - same-structure different-domain
   - same-domain different-layer
   - same-tool different-scenario
   - anti-pattern
   "Over-generalize rather than under-generalize" — missed generalizations don't auto-correct.

6. **5-round tool-call threshold.** ≥5 autonomous tool rounds for a task type in one session
   → candidate to solidify into a skill.

7. **User corrections sediment immediately.** 1 occurrence is enough; don't wait for
   repetition. User feedback (not just explicit corrections) must be sedimented — including
   "又忘了", "不对吧", "下次记得", "你怎么没xxx", etc.

8. **Self-update.** Distinguish universal methodology (→ this skill) from personal preference
   (→ memory skill). Test: if you strip user identity and project context, does the lesson
   still help any user? Yes → methodology; No → personal preference. The engine must update
   its own SKILL.md from user corrections — it cannot be the one skill that never auto-updates.

9. **See-and-act, don't just diagnose.** Finding an unfixed bug or missing rule → fix it
   immediately, don't just list it in a report.

### Two-axis analysis differs per codeagent store
- **Legacy:** axis 2 queries `message.time_created > last_timestamp` in SQL (efficient).
- **New:** must scan JSONL files for lines with `timestamp > last_timestamp`. The
  `observable-cac.jsonl` index gives session creation times but NOT last-message-time, so
  axis 2 (new messages in old sessions) requires reading the JSONL files' last lines or
  scanning all lines — more expensive than a SQL query.

### Two adapters needed
- **Legacy adapter:** SQL queries on `ngagent.db` (session/message/part tables, millis).
- **New adapter:** JSONL parsing of `~/.cac/projects/*/<uuid>.jsonl` (Claude Code-style
  events, ISO 8601). Timestamp format differs (millis INTEGER vs ISO 8601 string) — normalize.

## Environment status (2026-07-25)
- opencode/codeagent stores: both present (core input works)
- Skills dirs present: `~/.config/opencode/skills`, `~/.cac/skills`, `~/.claude/skills`
- Node v22: present (agentcenter install prerequisite met)
- Absent (would skip/degrade): agentcenter CLI, skill-finder, skill-creator, welink-cli,
  nga.cmd, W3 MCP, clouddevops-wiki
- `.npmrc` points at `registry.npmmirror.com` with corporate proxy set; agentcenter install
  overrides registry to cmc internal one — may need proxy cleared per source's 407 note
  (`407 Proxy Authentication Required` → clear `HTTP_PROXY`/`HTTPS_PROXY` or set
  `NO_PROXY=cmc.centralrepo.rnd.huawei.com`).

## Open questions
- How to install/access: W3 search MCP, CloudDevOps Wiki (skill or REST API?), welink-cli,
  nga.cmd / new `codeagent` metrics subcommands.
- Should legacy `ngagent.db` be read as live or treated as frozen historical data after
  migration?
- How to integrate with the new codeagent's existing per-project memory system
  (`~/.cac/projects/<slug>/memory/`) without duplicating or conflicting?
- Canonical internal starting point for the toolchain:
  `https://3ms.huawei.com/km/blogs/details/22148443` (Node.js install blog — likely links
  onward to the rest).
