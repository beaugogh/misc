---
name: huawei-skill-forge
description: Acts on retro-scope's findings to create/modify skills and memories that address the user's recurring time sinks and painpoints, so the user can solve those problems easily next time and avoid wasting time. Also extracts long-term memory from sessions, updates existing skills based on new experience, recommends/installs market skills, and checks skill versions. Component of huawei-auto-buddy — invoked by the parent skill, not directly by the user.
---

# skill-forge

The **act** phase of huawei-auto-buddy's diagnose→act pipeline. retro-scope
identifies where time goes and what keeps recurring; skill-forge creates or
modifies skills and memories so those problems are easier to solve next time.

## Prerequisites

All prerequisites use detect-and-skip: unavailable tools are reported in the
output, never block the core workflow.

| Dependency | Check | Auto-repair | Skip impact |
|---|---|---|---|
| retro-scope findings | `huawei-auto-buddy/output/` exists with report data | None — user must run retro-scope first | Core input missing; skill-forge can still analyze sessions directly but loses pipeline context |
| Python 3 | `python --version` | None | Fatal — cannot run |
| skill-creator | `{SKILLS_DIR}/skill-creator/SKILL.md` exists with `init_skill.py` | None (collision risk with Anthropic's skill-creator submodule — see below) | Degrade to direct file-writing mode |
| agentcenter CLI | `agentcenter --version` | Auto-reinstall (see below) | Skip skill recommendation + version-check (Tasks 4-5) |
| welink-cli | `welink-cli` in PATH; `auth status` | Auto-install + auto-refresh (see below) | Skip WeLink data collection |
| git | `git --version` | None | Skip git commit analysis |

### agentcenter auto-repair

If `agentcenter --version` fails (command not found or module not found), auto-reinstall
without prompting the user:

```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com npm install -g @aimarket/agentcenter \
  --@aimarket:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ \
  --strict-ssl=false
```

Three critical details: must use `product_npm` registry (not `npm-all`, which 401s);
must set `NO_PROXY` for the intranet host; must use `--strict-ssl=false` (corporate
proxy does TLS interception). If npm reports `407 Proxy Authentication Required`, clear
proxy env vars before installing. If `command not found` after install, add npm's global
bin (`%APPDATA%\npm` on Windows) to PATH.

### welink-cli auto-install + token refresh

If welink-cli is not in PATH, auto-install:

```bash
npm install -g @welink/welink-cli \
  --registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ \
  --strict-ssl=false --ignore-scripts
```

`--ignore-scripts` skips a broken PowerShell postinstall bug. If token is expired
(`auth status` shows EXPIRED), auto-refresh: `welink-cli auth login` (connects to WeLink
PC client non-interactively). Both must fail before skipping WeLink data.

### skill-creator collision risk

Two different `skill-creator` skills exist: the agentcenter one (has `init_skill.py`,
preferred) and the Anthropic submodule at `skills/anthropic-skills/skills/skill-creator/`
(lacks `init_skill.py`, different workflow). Detection by filename alone collides. Always
check for `init_skill.py` in the same directory as `SKILL.md`.

## Configuration

### SKILLS_DIR auto-detection

The skills directory varies by AI client. Detect automatically:

| Client | SKILLS_DIR (Windows) | Detection signal |
|---|---|---|
| claudecode | `%USERPROFILE%\.claude\skills` | Path contains `.claude` |
| codeagent (new) | `%USERPROFILE%\.cac\skills` | Path contains `.cac` |
| codeagent (legacy) | `%USERPROFILE%\.config\opencode\skills` | Path contains `.config\opencode` |
| cac | `%USERPROFILE%\.cac\skills` | Path contains `.cac` |

Primary detection: infer from this skill's own path. `huawei-auto-buddy/skill-forge/SKILL.md`
lives under `{SKILLS_DIR}/huawei-auto-buddy/skill-forge/`, so SKILLS_DIR is two levels up
from the `skill-forge/` directory. If that fails, check each candidate directory in order.

### Output directory

Default: `huawei-auto-buddy/output/` (shared with retro-scope). Override via
`SKILL_FORGE_OUTPUT_DIR` env var. Created skills go in
`huawei-auto-buddy/output/auto-buddy-created-*/`.

### Watermark

`huawei-auto-buddy/output/last_analysis.txt` — stores the millisecond timestamp of the
last analysis. Used for two-axis incremental analysis (new sessions + new messages in
old sessions). If the file is missing or zero, treat as first run.

## Codeagent dual instances

The user may have TWO codeagent installations with different data stores. Both must be
read if present.

### Legacy instance (`nga` command)
- Data store: SQLite DB at `~/.local/share/opencode/db/ngagent.db`
  - Tables: `session` (id, title, time_created millis, directory), `message` (id,
    session_id, time_created millis, data JSON with role), `part` (id, message_id,
    session_id, time_created millis, data JSON with type)
  - Timestamps: INTEGER milliseconds
  - Two-axis incremental: axis 2 = `message.time_created > last_timestamp` (efficient SQL)
- Skills dir: `~/.config/opencode/skills/`

### New instance (`codeagent` command)
- Data store: JSONL files at `~/.cac/projects/<project-slug>/<session-uuid>.jsonl`
  - Schema: Claude Code-style, one JSON per line. Types: user, assistant, tool_use,
    tool_result, thinking, text. Fields: type, timestamp (ISO 8601 string), sessionId,
    cwd, gitBranch, message.role, message.content
  - Timestamps: ISO 8601 strings (NOT millis — convert before comparing to watermark)
  - Two-axis incremental: axis 2 = scan JSONL lines for `timestamp > last_timestamp`
    (more expensive than SQL — must read files, not just query)
- Per-project memory: `~/.cac/projects/<slug>/memory/` — MEMORY.md + feedback_*.md.
  The new codeagent already has its own feedback-harvesting system. Do NOT build a
  parallel system that conflicts — read from it, don't overwrite it.
- Skills dir: `~/.cac/skills/` (primary going forward)

### Timestamp normalization

Legacy uses milliseconds (INTEGER). New uses ISO 8601 (string). Claude Code uses seconds
(INTEGER). Normalize all to milliseconds before comparison: `iso8601 → parse → epoch millis`;
`claude_seconds → * 1000`.

## Workflow

### Step 1: Determine analysis scope

Read `huawei-auto-buddy/output/last_analysis.txt` (millis timestamp).

- **First run** (file missing or 0): analyze all sessions. If data is large, batch:
  max 20 sessions per run, record the watermark, tell the user to run again.
- **Incremental run**: two-axis analysis:
  - Axis 1: new sessions — `session.time_created > last_timestamp`
  - Axis 2: new messages in old sessions — `session.time_created <= last_timestamp`
    AND `message.time_created > last_timestamp`
- Exclude the currently-running session (incomplete), but **extract user feedback
  from it** — the current session has the freshest feedback signals.

### Step 2: Read retro-scope findings

Read retro-scope's output from `huawei-auto-buddy/output/`:
- `report_*.html` — multi-horizon time analysis with top time sinks, root-cause
  narratives, and per-kind breakdowns
- `session_records/*.json` — detailed per-task evidence with event timelines
- `trends` — recurring time-consumption patterns (persistent, declining, increasing,
  automation candidates)

These are the **primary input**. skill-forge does NOT re-export sessions or re-compute
time accounting — retro-scope already did that with 14 source adapters. skill-forge
consumes the findings and acts on them.

If retro-scope has not been run, skill-forge can still analyze sessions directly
(Steps 3-4) but loses the pipeline context.

### Step 3: Collect supplementary data (optional, detect-and-skip)

Data sources beyond what retro-scope already collected. Each is optional — detect,
use if available, skip if not, report what was skipped.

1. **git commits** — `git log --author="<name>" --since="<start>" --until="<end>" --all
   --format="%h %ai %s" --no-merges` in project dirs (discovered from session `cwd`/`directory`
   or memory). Cross-verify with retro-scope's git adapter findings.
2. **welink-cli chat** — `welink-cli im query-recent-conversation --count 50`, then
   `welink-cli im query-history-message --group-id <ID> --query-count 50`. Read max 3
   conversations concurrently (batch-serial) to avoid context overflow. Summarize
   immediately after each batch.
3. **CodeHub/GitHub MCP** — self-contained scripts at `mcp-tools/huawei-codehub/codehub.py`
   and `mcp-tools/github/github_mcp.py`. Use for MR reviews (recurring review comments =
   recurring mistakes). Requires `CODEHUB_TOKEN`/`GITHUB_TOKEN` in `.env`. Internal hosts
   need `NO_PROXY`; external hosts need proxy through `proxyuk.huawei.com:8080`.
4. **W3 search** — `python3 mcp-tools/huawei-w3-search/w3_search.py "<name>" --size 10 --json`
   (self-contained, no install needed).
5. **CloudDevOps Wiki** — `python3 mcp-tools/huawei-wiki/wiki_mcp.py search-wiki-documents
   --url <url> --search-range knowledge --search-key "<name>" --json` (read operations need
   no auth).

### Step 4: Analyze and extract long-term memory

Extract from sessions + retro-scope findings + supplementary data:

**User preferences and habits:**
- Repeatedly emphasized work methods
- Explicit requirements on AI behavior
- Communication style preferences

**Development environment:**
- New environment characteristics, tool config changes, new gotchas

**Projects and team:**
- New project info, team changes, collaboration patterns

**Important decisions:**
- Technical choices, approach trade-offs, process improvements

**Exclusion rules:**
- Don't extract one-time operation details (specific git commands)
- Don't extract info already in the memory skill
- Don't extract secrets (passwords, tokens, keys)
- **Preserve user's exact words (一字不改)** — don't summarize, paraphrase, or rewrite
  what the user said. Only AI behavior should be summarized.

**Memory skill location:** `huawei-auto-buddy/output/auto-buddy-created-global-memory/SKILL.md`.
If it doesn't exist (first run), create it with the categories above. If it exists,
append new info (don't delete existing). If new info contradicts existing, replace with
new.

**First-run identity initialization:** If the memory skill doesn't exist, ask the user
for their name and employee ID. Don't hardcode any identity.

### Step 5: Discover patterns and create/update skills

This is the core job — turning recurring problems into reusable skills.

#### Historical bug retrospection (mandatory, not optional)

Before analyzing new sessions, scan ALL history (not just incremental) for reported bugs.
Keywords: `bug`, `问题`, `修复`, `出错`, `不对`, `遗漏`, `又出现`, `老问题`, `没修`, `没更新`.

For each historical bug, verify:
1. **Code/script fixed?** — if the bug involved a script, check the fix exists
2. **SKILL.md constraint added?** — if the root cause was AI behavior, check a rule exists
3. **Already-broken state fixed?** — if the bug produced wrong results, check they're corrected
4. **Project norm files updated?** — if the project has `for_ai_to_read/`, `.cursorrules`,
   `CLAUDE.md`, check the rule is documented there too

If any is missing, fix it immediately. Don't just list it in a report.

#### Pattern identification criteria (any one triggers)

1. **Cross-session recurrence:** same task type in ≥2 sessions
2. **Single-session complexity:** ≥5 autonomous tool-call rounds for one task type
3. **Fixed workflow:** task has ≥3 fixed steps
4. **Error-prone:** AI made mistakes that rules can prevent
5. **Low human-decision needed:** flow is mostly mechanical

#### Forced generalization (举一反三)

When identifying a pattern, check all 4 dimensions:

| Dimension | Question | Action |
|---|---|---|
| Same-structure, different-domain | Does this pattern exist in other domains? | Extend skill scope or create universal skill |
| Same-domain, different-layer | Does this apply at coarser/finer granularity? | Add to skill or create companion |
| Same-tool, different-scenario | Does the tool need fixed flow in other scenarios? | Extend skill description + triggers |
| Anti-pattern generalization | Could the same error occur in similar scenarios? | Add prevention rule to all related skills |

**Over-generalize rather than under-generalize.** Missed generalizations don't auto-correct;
over-generalizations can be narrowed by user feedback.

Good: `auto-buddy-created-stats-collector` (triggers: token stats, code line stats, MR stats, Wiki stats)
Bad: `auto-buddy-created-token-stats` (only token stats)

#### User feedback sedimentation

Any user feedback must be sedimented into a skill — 1 occurrence is enough, don't wait
for repetition. Feedback includes (not just explicit corrections):

| Expression | Meaning |
|---|---|
| "又忘了xxx" | Rule exists but ineffective — needs strengthening |
| "不对吧" / "你没有xxx" | AI behavior doesn't match expectation |
| "下次记得xxx" / "以后要xxx" | Explicit new rule request |
| "这个skill应该xxx" | Direct skill improvement suggestion |
| "你怎么没xxx" / "你这次没xxx" | Points out an omission |
| "是不是应该xxx" | Implies current behavior is wrong |

**3-correction threshold:** if the user corrects the same skill's behavior ≥3 times in one
session, the skill has a systemic deficiency — must update its SKILL.md with prevention
rules immediately.

**Rule exists ≠ rule effective.** If the AI violates an existing rule, the rule needs
strengthening, not just existence:

1. **Promote rule position** — move from list middle to step-0 gate
2. **Add gating mechanism** — change "should do" to "must confirm before continuing"
3. **Add counter-example** — write the AI's specific violation as a ❌ forbidden case
4. **Split the rule** — if too broad, split into specific sub-rules

#### Creating new skills

- Name prefix: `auto-buddy-created-`
- Location: `huawei-auto-buddy/output/auto-buddy-created-<name>/`
- **Must use skill-creator** if available (6-step flow: understand → plan resources →
  init_skill.py → edit SKILL.md → validate → iterate). If skill-creator unavailable,
  degrade to direct directory + SKILL.md creation.
- SKILL.md frontmatter: `description` must list function + trigger words + scenarios
  (this is the only field AI uses to decide when to activate the skill)
- Body: imperative form, <500 lines, progressive disclosure (details in references/)

#### Updating existing skills

- Only modify `auto-buddy-created-*` skills and this skill's own SKILL.md
- **Must NOT modify** third-party or manually-installed skills (skill-creator, mr-reviewer, etc.)
- When updating a skill's script files, **sync the install directory** — skills typically
  have two copies (repo + installed). Edit one, sync to the other.

#### Self-update

skill-forge must update its own SKILL.md from methodology learnings. Distinguish:
- **Universal methodology → this SKILL.md:** lessons that help any user (bug retrospection,
  generalization, rule strengthening)
- **Personal preference → memory skill:** user-specific habits (build commands, project deps)

Test: if you strip user identity and project context, does the lesson still help any user?
Yes → methodology; No → personal preference.

### Step 6: Record watermark

Write the current timestamp to `huawei-auto-buddy/output/last_analysis.txt`:

```python
import time
with open("huawei-auto-buddy/output/last_analysis.txt", 'w') as f:
    f.write(str(int(time.time() * 1000)))
```

### Step 7: Report

Report to the user:
1. How many sessions analyzed (incremental count)
2. Which data sources collected, which skipped and why
3. What memory was updated (new entries, replaced entries)
4. Which new skills created (name + purpose)
5. Which existing skills updated (what changed)
6. Which retro-scope findings were acted upon (automation candidates → skills created)

### Step 8: Recommend market skills (optional, requires agentcenter)

Based on analysis + retro-scope findings:
1. Generate 3-5 search keywords from work scenarios, tool frequency, pain points
2. Search: `agentcenter search skill --keyword <term> --json`
3. Filter: exclude already-installed, exclude overlapping with auto-buddy-created skills
4. Show top 5 (name, version, description, recommendation reason)
5. **User confirms** before installing — never auto-install

Install with the `--client` trick to keep skills local:
```bash
agentcenter skill add <name> --client huawei-auto-buddy --path skills/huawei-auto-buddy -f
```
Must use non-built-in `--client` value (not `claudecode`/`opencode`/`cac`) + `--path`
to install to the local directory. Built-in clients ignore `--path` and install globally.

### Step 9: Check skill versions (optional, requires agentcenter)

1. Scan `huawei-auto-buddy/` for installed skills with SKILL.md
2. For non-`auto-buddy-created-*` skills, search agentcenter for latest version
3. Compare versions; mark outdated skills
4. **User confirms** before updating
5. Before updating, check for local modifications (diff against market version) — warn if
   local changes will be overwritten

## Error handling

| Scenario | Handling |
|---|---|
| retro-scope not run, no output/ dir | Proceed with direct session analysis; warn that pipeline context is missing |
| Both codeagent stores empty | Tell user to use an AI coding tool first |
| Sessions exist but no incremental data | Tell user no new sessions since last analysis |
| agentcenter unavailable | Auto-reinstall; if reinstall fails, skip Tasks 8-9 |
| agentcenter auth expired | Try `agentcenter auth`; if fails, skip Tasks 8-9 |
| welink-cli not installed | Auto-install; if fails, skip WeLink data |
| welink-cli token expired | Auto-refresh via `welink-cli auth login`; if fails, skip WeLink data |
| skill-creator not found | Degrade to direct file-writing mode; warn about lower quality |
| skill install/update fails | Report failure reason; don't block other tasks |
| First-run data too large | Batch: max 20 sessions per run; record watermark; tell user to run again |
| Memory skill creation fails | Check directory permissions, retry once; if still fails, tell user to create manually |

## Constraints

- **See-and-act, don't just diagnose.** Finding an unfixed bug or missing rule → fix it
  immediately. Don't list problems in a report and wait for the user to say "fix it."
- **Iterative analysis — don't do too much in one run.** Complete incremental analysis and
  report first. Deeper retrospection can happen on the next run. Don't try to do
  incremental + full retrospection + create 5 skills + update 10 files in one pass.
- **No hardcoded user paths or identity.** All paths auto-detected. Identity initialized
  from user input on first run, not baked in.
- **Open-source only.** No paywalled or closed-source dependencies.
- **User confirms all installs/updates.** Never install or update skills without explicit
  user confirmation.
- **Don't duplicate retro-scope's work.** retro-scope does session analysis, time accounting,
  and source collection with 14 adapters. skill-forge consumes those findings, doesn't
  re-export sessions or re-compute time.
