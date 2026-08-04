---
name: retro-scope
description: Record the time/effort the user spends on different tasks, aggregatable by day/week/month/year, so the user can see how time/effort is distributed across task kinds and identify the most time-consuming work. Component of huawei-auto-buddy — invoked by the parent skill, not directly by the user.
---

# retro-scope

Records the user's time/effort across task kinds, aggregatable by day / week / month / year,
to reveal which kinds of work consume the most time/effort. Beyond time, it reconstructs a
**task model** per task: input, output, and success/failure — not just duration.

## Constitution / Mission

**The purpose of this skill is to show a person where their time and effort actually go, and
to surface opportunities to automate or eliminate the work that consumes the most of it.**

Time tracking is not the end goal — productivity insight is. A time log that says "you spent
60h coding, 20h in meetings, 8h on email" is a starting point, not a deliverable. The
deliverable is answers to questions like: "Which task ate 12h and why? Could it have been 2h?
Was it stuck, and on what? Did it succeed? Is the same kind of task repeatedly slow?" The
skill exists to make those answers visible from the activity traces a person already leaves
behind, without any manual logging.

To serve that mission, the skill must be:

1. **Multi-resolution, drill-down-able.** A person should be able to see the month, click into
   a week, click into a day, click into a task, and click into the *stages within that task* —
   what was attempted, what failed, what was retried, where the wall-clock went vs. the active
   effort. A flat "top-20 tasks" list is the overview; the value is in the drill-down to root
   cause. (Implemented in Phase 10 — see "Implemented capabilities" below.)

2. **Honest about parallelism.** Real work is not sequential. A person fires off a background
   coding agent, then does their own research in the foreground; both are active at once. The
   model must represent overlapping task intervals, not force everything into a single
   non-overlapping timeline. Aggregation must distinguish *exclusive* time (only one task
   active) from *overlapping* time (multiple tasks active — the person is coordinating, not
   doing each serially). (Implemented in Phase 10 — see "Implemented capabilities" below.)

3. **Honest about success.** A success rate of "0%" for meetings or research is not a finding —
   it's a measurement failure. Success is three-valued: **succeeded / failed / unknown**.
   "Unknown" must not be counted in the denominator. For task types where no success signal
   exists yet, the report must say "success not measured" rather than implying failure. The
   goal is to *narrow* the unknown over time by finding real signals (commit landed, build
   passed, user didn't correct, follow-up artifact produced), never to fabricate a number.
   (Implemented in Phase 10 — see "Implemented capabilities" below.)

4. **Informative toward automation.** The highest-value output is not "you spent N hours on X"
   but "X keeps recurring, takes N hours each time, and follows a predictable pattern — here's
   a candidate for automation." The skill should surface repeat task shapes, time sinks, and
   stuck loops (repeated errors, retries, corrections) as automation candidates, not just
   aggregate them silently.

5. **Retrospective only, opt-in, portable.** No live tracking, no always-on watchers (hard
   requirement). No manager-analyzing-team. No closed-source dependencies. Runs on whatever
   sources a colleague has, detects them, and reports the gaps honestly.

## Implemented capabilities (Phase 10)

The three frontiers below were the main growth areas for the skill. All three are now
implemented (Phase 10). They are documented here so users understand what the
skill does, not what it aspires to do.

### Parallel tasks

The model represents tasks as *intervals* (start, end) that may overlap others, not slots in
a single timeline. Key signals for parallel-task detection (all implemented in
`parallel_tasks.py`):
- **Background task lifecycle:** `TaskCreate`/`TaskOutput`/`TaskStop` tool calls mark a
  sub-agent task running in the background while the foreground session continues. The
  background task's events are separated by `tool_use_id` / session thread, not by timestamp.
- **Multiple concurrent sessions:** two AI-session JSONL files with overlapping timestamp
  ranges = two tasks running in parallel (e.g. one on a server, one locally).
- **Foreground/background split by source_kind:** a `browser` visit during an `ai_session`
  coding task = the person researching while the agent works.

**Aggregation.** `compute_exclusive_time()` reports both *exclusive time* (sum of
non-overlapping intervals — the person's "bandwidth") and *wall-clock span* (first-event to
last-event). A day with 8h coding + 4h research overlapping = 8h exclusive (not 12h).

### Drill-down & root-cause analysis

The task model is multi-resolution: `--task <id> --drill` shows a stage-by-stage timeline
within a task (implemented in `drill_down.py`).
- **Month → week → day → task → stage → tool call.** Each level is a drill-down into the one
  above.
- **Stage detection within a task:** `detect_stages()` runs PELT recursively within a task
  (penalty 2×n_features, lower than task-boundary 10×n_features) or heuristic fallback
  (cwd-shift, tool-cluster change, user correction, >10min gap).
- **Root-cause markers:** `detect_markers()` surfaces (a) error clusters (≥2 consecutive
  `is_error` tool results), (b) retry loops (same tool+input attempted >1× in 5min),
  (c) user corrections (EN+CN signals), (d) time sinks (idle: high-wall/low-active; hard:
  top-quartile active).
- **"Why was this slow?" answer:** for any task over 2h active, the drill-down offers a
  generated narrative — "stages 2–3 retried the build 4× (40min), then a user correction
  redirected the approach, then stage 5 succeeded in 10min" — so the person sees the root
  cause, not just the duration.

### Success attribution

Success is three-valued: `succeeded` / `failed` / `unknown` (constants in `segment_tasks.py`).
`unknown` is excluded from the success-rate denominator. Per task type, the signals narrow the
unknown:
- **AI coding:** `TaskUpdate(completed)` + no `is_error` + no user correction → succeeded.
  `TaskUpdate(failed/cancelled)` or `is_error` cluster → failed.
- **Manual coding (git):** commit landed → succeeded; commit reverted → failed.
- **Research:** an artifact (doc written, code changed, email sent) follows the browsing
  cluster → succeeded. Browsing with no follow-up → unknown (not failure — maybe it was
  reading).
- **Meeting:** a follow-up message/commit/action references the meeting's decision →
  succeeded. No follow-up → unknown.
- **Email:** reply sent or thread marked resolved → succeeded. Thread abandoned → unknown.
- **Report rendering:** shows `success%` only over tasks where success is *known*; shows
  `unknown%` separately. All-unknown categories render "n/a (all unknown)" instead of
  misleading "0%". A `refine_success()` post-pass upgrades unknown→succeeded using
  cross-task context (git commits, research→coding within 1h, meeting→action within 24h).

## Remaining limitations

- **2h proximity window for background-task pairing:** `BG_PROXIMITY_WINDOW = 2 * 3600` in
  `parallel_tasks.py` — background task stops are not paired with creates more than 2h apart.
  This is a heuristic, not a hard boundary, and may miss long-running background tasks.
- **PELT penalty tuning:** the PELT change-point penalty (β = 10 × n_features for task
  boundaries, 2 × n_features for stages) is a heuristic. The evaluation harness
  (`--eval`, Phase 9.8) provides baseline metrics (WindowDiff=0.417, F1=0.222) but no labeled
  benchmark exists yet to tune against.

## Audience
Shared across the author's colleagues, not personal-only. Each colleague's environment
differs, so the skill is a **detector-based catalog**: every supported source is tried, used
if present, skipped if absent. The skill must never assume a specific user, path, or
platform. Per-run, report which sources were found / used / skipped so the colleague can see
gaps (e.g. "welink-cli not installed — meeting data missing").

## Installing welink-cli (optional)

welink-cli is the preferred source for four data domains (meetings, calendar, mail, IM) but
is **optional** — the skill works without it via [backup routes](#data-sources-without-welink-cli).
If a colleague does not install it, 3 of 4 domains have fallbacks; IM has none (see below).

**Install command:**

```bash
npm install -g @welink/welink-cli \
  --registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ \
  --strict-ssl=false \
  --ignore-scripts
```

**Gotcha 1 — proxy hang (npm hangs fetching from the intranet registry).** npm routes
intranet traffic through the external corporate proxy and hangs silently. Fix: exclude the
intranet registry host from the proxy:

```bash
# Option A: env var (recommended — survives across npm invocations)
NO_PROXY="cmc.centralrepo.rnd.huawei.com,127.0.0.1"

# Option B: npm flag (one-shot)
npm install -g @welink/welink-cli --registry=... --noproxy="cmc.centralrepo.rnd.huawei.com"
```

**Gotcha 2 — postinstall PowerShell bug (install fails with a `UIntPtr` type-cast error).**
The welink-cli postinstall script runs a PowerShell snippet to auto-add the CLI to PATH.
That snippet has a `UIntPtr` type-cast bug on some Windows configurations and the script
exits non-zero, failing the install. Fix: install with `--ignore-scripts` — this skips the
broken postinstall entirely. The `.CMD` shim still lands in npm's global `bin` directory
(normally already on PATH), so `welink-cli` works immediately. Verify:

```bash
welink-cli --version
```

If `welink-cli` is not found after install, add npm's global bin to PATH (find it with
`npm config get prefix` → `<prefix>` on Windows is usually under
`%APPDATA%\npm`).

**Auth:** `welink-cli auth login` opens a WeLink mobile scan-to-login QR. Token is valid
~30 min and auto-refreshed by the CLI. No password stored locally.

**Mail/calendar prerequisite:** before `calendar list` or `mail list` work, run this once
to discover the Exchange server:

```bash
welink-cli mail autodiscover --email <you>@huawei.com
```

This records the Exchange endpoint (e.g. `imailie.email.huawei.com`) the CLI needs for
mail/calendar subcommands. Without it, those subcommands return empty or error. `meeting`
and `im` subcommands do not require autodiscover.

## Data sources without welink-cli

welink-cli is the preferred path for four communication domains, but it is opt-in (npm
install + scan-to-login) and many colleagues will not have it. The skill must reach the same
domains via alternative paths. Three of four have fallbacks; **IM has none** — this is a
verified hard constraint, not a gap to close.

| Domain | welink-cli (preferred) | Backup (no welink-cli) | Coverage |
|--------|------------------------|------------------------|----------|
| **Meetings (duration)** | `meeting query-list` (start+end millis → direct duration) | WeLink recordings + ffprobe duration; iCalendar `.ics` (scheduled, may differ from actual) | Partial — recordings give actual duration only if ffprobe is installed; `.ics` gives scheduled duration |
| **Calendar** | `calendar list` (ISO start/end, subject, location, organizer) | iCalendar `.ics` export (manual one-time export from Outlook or WeLink) | Full — but requires a one-time manual export step |
| **Mail** | `mail list` (send/receive times, subjects, senders) | Outlook OST via COM/MAPI (`outlook_adapter.py`) — **works** (pywin32) | Full — requires Outlook desktop installed (Windows-only); 50 inbox + 38 sent items readable on author's machine |
| **IM (chat)** | `im query-history-message` | **No backup exists** | None — IM is welink-cli-only |

### IM is welink-cli-only by design

Verified: 52 WeLink Desktop `.db` files exist on the machine across
`~/.AppData/Roaming/WeLink_Desktop/appdata/**/*.db`, and **zero** contain message tables.
They hold config, login state, UI state, and adaptiveCard configs only. There is no local
store of WeLink chat history. Without welink-cli, the chat category is simply unavailable —
the skill reports this honestly in the `--sources` discovery output rather than silently
dropping it.

### Backup-route status (Phase 9 — built)

These routes are built and working (see the parallelism
table):

- **`.ics` parser** — works. `ICalendarAdapter` in `more_adapters.py` parses VEVENT entries
  with RRULE expansion + TZID parsing. Auto-discovers `.ics` files in `~/Downloads` and
  `RETRO_SCOPE_ICS_PATHS` env var. Requires the user to manually export their calendar
  (Outlook: File → Open & Export → Import/Export → Calendar; WeLink: check calendar export).
- **WeLink recordings adapter** — works, with ffprobe duration. `WeLinkRecordingsAdapter`
  walks `D:\MeetingRecordings` and emits meeting-occurrence events with ffprobe-extracted
  duration (falls back to mtime-only when ffprobe is absent). Filename parsing extracts
  date/time/meeting-ID from recording filenames.
- **Outlook OST adapter** — **WORKS (Phase 9.3, 2026-07-29).** `OutlookAdapter` in
  `outlook_adapter.py` uses Outlook COM/MAPI via pywin32 to read Inbox + Sent Items.
  Investigation verdict: libpff/pffexport FAILED on Windows (C build error, no prebuilt
  wheel); Outlook COM WORKS (pywin32 installs from tuna, Dispatch succeeds, real mail
  data readable). OST file found at custom path `D:\Email\bogao@huawei.com.ost` (206.9 MB)
  — the SKILL.md note "Not present on author's machine" was outdated. The adapter emits
  `kind="email"`, `source_kind="comm"` events matching the welink-cli mail event shape.
  COM requires Outlook desktop installed with a configured profile; Windows-only. 34 tests
  pass (31 unit + 3 live integration against real Outlook data).
- **IM** — no fallback, by design (see above).

### Discovery report

`python run.py --sources` shows which sources are available on the current machine and
which are missing, so a colleague can see their gaps at a glance. When welink-cli is
absent, the report explicitly states: "IM/chat history is unavailable — welink-cli is the
only source of WeLink messages; no local store exists." No silent gap.

## What it does
1. **Discover & collect activity traces** from all supported sources present in the current
   environment (see "Source catalog").
2. **Detect task boundaries** — group activity into tasks (explicit via `TaskCreate` or
   inferred from user-message turns — see "Task model").
3. **Classify each task** into a task kind (taxonomy — see open question).
4. **Estimate duration/effort** per task (see "The core challenge: duration").
5. **Capture input & output** per task (prompts, files, code, command results, artifacts).
6. **Determine success/failure** per task (task status, tool errors, user corrections).
7. **Aggregate** by day / week / month / year and report which task kinds are most
   time/effort-consuming, with task counts, success rates, and I/O samples.

## Source catalog

**Open discovery.** The catalog is a set of known source shapes (each a detector + reader),
not a closed list. Unknown sources that match a recognizable shape (e.g. a `~/.<tool>/`
dir containing `projects/*/*.jsonl` session transcripts, or a SQLite DB with
`session`/`message` tables) are **discovered and adopted automatically** — the skill detects
the shape, infers the reader, and uses it. Sources that don't match any known shape are
reported as "unrecognized — ask user to identify" rather than silently ignored.

This means a colleague's tool the catalog doesn't name yet can still contribute time data if
its storage shape resembles a known one (JSONL transcripts, SQLite session tables, browser
`History` DB, `.lnk` recent-files). New shapes encountered in the wild should be folded back
into the catalog so future runs recognize them.

Schemas below are marked **[verified]** = confirmed on at least one real environment, or
**[unverified]** = expected but layout not confirmed (a colleague who has it should fill in
the real shape on first encounter — the skill should detect the dir and prompt for inspection).
Additional verified subtypes: **[verified-encrypted]** = file exists but is encrypted/proprietary
(not directly readable), **[verified-format]** = file format confirmed and parser built,
**[verified-COM]** = accessible via COM/MAPI (not direct file parse), **[verified legacy-only]**
= confirmed but only for legacy versions, **[verified — no messages]** = confirmed present but
contains no useful data, **[verified plugin]** = confirmed via a plugin adapter.

**Architectural references** (see `research-findings.md`): **Memacs** (novoid/Memacs,
GPL-3.0) uses the identical adapter-registry pattern — independent Python modules per source
parsing historical records into a normalized timeline. **Plaso** (log2timeline) is the
industrial-strength version of the same pattern: decoupled parsers → normalized
microsecond-epoch → deduped storage, battle-tested in forensics. Our open-discovery catalog
follows this proven shape (Memacs for the personal-data module shape, Plaso for the
normalization/dedup machinery). The task-model layer (TaskCreate/TaskUpdate/usage/is_error
from AI session JSONL) is our differentiator — none of the surveyed tools do it, because they
predate AI coding agents.

### A. AI coding-agent sessions & memory

| Source | Detector | Data layout | Time signal | Memory |
|--------|----------|-------------|-------------|--------|
| **Claude Code** [verified] | `~/.claude/projects/<slug>/*.jsonl` | JSONL, Claude Code-style events (user/assistant/tool_use/thinking/text), ISO 8601 `timestamp`, `cwd`+`gitBranch` per line. Also `~/.claude/history.jsonl` (prompt log, millis). Richest store on the author's machine (32 sessions, 39,925 lines, 8,102 tool_use blocks). | per-message ts → span; **per-message `usage` tokens = effort signal** | `~/.claude/projects/<slug>/memory/` (MEMORY.md + feedback_*.md). Pattern/feedback data — auxiliary context, and a **success signal** (user correction = task didn't fully succeed). |
| **Codeagent (new, `codeagent` cmd)** [verified] | `~/.cac/projects/<slug>/<uuid>.jsonl` | Same JSONL schema as Claude Code (user/assistant/tool_use/thinking, ISO 8601, cwd+gitBranch). Plus `~/.cac/history.jsonl`, `~/.cac/projects/observable-cac.jsonl` (session index). | per-message ts → span; per-message `usage` tokens | `~/.cac/projects/<slug>/memory/` (MEMORY.md + feedback_*.md). Auxiliary + success signal. |
| **Codeagent (legacy, `nga` cmd)** [verified] | `~/.local/share/opencode/db/ngagent.db` (SQLite; path via `NGA_DATA_HOME`→`XDG_DATA_HOME`) | Tables `session`/`message`/`part`; millis INTEGER timestamps; `directory` on session row. | per-message ts → span | none (predates per-project memory) |
| **Codex** [unverified] | `~/.codex` (expected) | unknown — likely JSONL or SQLite under `~/.codex/sessions/` | unknown | unknown |
| **Openclaw** [unverified] | unknown — search `~/.openclaw`, `~/.open-claw` | unknown | unknown | unknown |
| **Hermes-agent** [unverified] | unknown — search `~/.hermes*` | unknown | unknown | unknown |

**Two adapters are required** for the verified codeagent split:
- Legacy: SQL on `ngagent.db` (millis). Incremental axis-2 = efficient `WHERE time_created > ?`.
- New/Claude Code: JSONL parse (ISO 8601). `observable-cac.jsonl` gives session creation times but NOT last-message-time, so "old sessions with new messages" requires scanning JSONL files' last lines — more expensive than SQL.
Timestamp formats differ (millis INTEGER vs ISO 8601 string) — normalize to a common representation.

**Session JSONLs carry a rich task model already** (verified in Claude Code, applies to new-codeagent too). Per assistant message: `message.usage` (input_tokens, output_tokens, cache_*, server_tool_use web_search/fetch counts) = per-step effort; `message.stop_reason` (end_turn / tool_use / stop_sequence) = step progression. `tool_use` blocks include `TaskCreate` (subject + description + activeForm = task boundary + input), `TaskUpdate` (taskId + status: in_progress/completed = task status/success), `TaskOutput`/`TaskStop` (background task lifecycle), `EnterPlanMode`/`ExitPlanMode` (planning phase boundaries). `tool_result` blocks carry `is_error: true/false` = per-step success/failure. Session line types `ai-title`/`custom-title`/`agent-name` give per-session task title and agent. See "Task model" for how these combine.

**`memory` stores are pattern/feedback data, not time data.** They don't carry duration. For
time-tracking they're only useful as auxiliary context (which project a session belonged to).

### B. AI token/runtime metrics

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **Per-message `usage` tokens** [verified] | `assistant.message.usage` in Claude Code / new-codeagent session JSONL | input_tokens, output_tokens, cache_creation/read_input_tokens, server_tool_use (web_search_requests, web_fetch_requests) per assistant message | **primary effort signal for AI-coding tasks** — per-step, richer than per-session. Replaces the nga.cmd dependency for these stores. Sum over a task's messages = task effort. |
| **nga.cmd** [verified legacy-only] | `nga.cmd` in PATH (lives in legacy codeagent's `D:\CodingAgentCLI\`) | `nga.cmd session list` / `metrics <id>` — reports runtime + token counts | effort signal for **legacy** codeagent sessions only (those lack per-message `usage`). Whether the new `codeagent` command has equivalent metrics subcommands is **unverified**. |
| **Codeagent (new) metrics** [unverified] | `codeagent --help` for metrics/session subcommands | unknown | if present, would be a cross-check on the per-message `usage` sum. |

**Effort signal hierarchy:** per-message `usage` (Claude Code / new-codeagent) > nga.cmd
(legacy only) > wall-clock span (any). nga.cmd is no longer "the one source" — it's the
fallback for the one store that lacks per-message tokens.

### C. Code & version control

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **git / CodeHub** [verified] | `git --version`; project dirs from session `cwd`/`directory` or memory | `git log --author --since --until` (commits, per-commit author + timestamp) **+ `git reflog`** (branch-checkout timestamps — finer "when you switched to working on X" signal than commits; a coding-task boundary signal). Technique borrowed from Hourgit. | commit/checkout occurrence; coding-task category from messages. Duration inferred from commit clustering + reflog gaps, not direct. Also a **task-output signal**: the commit is the artifact a coding task produced. |
| **VSCode Local History** [verified] | `~/.AppData/Roaming/Code/User/History/**/entries.json` (Windows; platform-specific elsewhere) | Per-file edit versions with millis `timestamp`. E.g. `wushan_assistant_brainstorm_phase1_v2.md` edited at 1784947010863. | **direct coding-activity signal** — when you edited which file. Cleaner than inferring from session transcripts. Also a **task-output signal**: edited files are task artifacts. |
| **VSCode workspaceStorage** [verified] | `~/.AppData/Roaming/Code/User/workspaceStorage/` | Recently opened workspaces | workspace-open events |
| **VSCode globalStorage/storage.json** [verified] | `~/.AppData/Roaming/Code/User/globalStorage/storage.json` | Recently opened workspaces list | workspace-open events |

### D. Communication, meetings & email

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **welink-cli (WeLink IM + meetings + calendar + mail)** [verified] | `welink-cli` in PATH; `auth status` | A single npm CLI (OAuth2 scan-to-login) exposing **four** domains via subcommands: `meeting query-list` (meetings w/ start_time/end_time in millis-epoch — **direct meeting DURATION**), `calendar list` (calendar events w/ ISO start/end, end-exclusive date ranges), `mail list` (inbox + sentitems, send/receive times + subjects + senders), `im query-history-message` (chat messages, two-step: enumerate conversations then fetch history). All support `--format json`. **No chat history is stored locally** — verified: 52 WeLink Desktop .db files, zero contain message tables; welink-cli is the only path to messages. Install instructions + gotchas: [Installing welink-cli](#installing-welink-cli-optional). | **the highest-value communication source**: meetings give actual duration (start+end millis), calendar gives scheduled duration + subject/location/organizer, mail gives communication occurrence + subject, IM fills gaps between coding sessions. One tool retires the meeting-duration gap + the Outlook/Graph email+calendar blocker for colleagues with welink-cli. Adapter: `welink_cli_adapter.py`. **Optional** — 3 of 4 domains have [backup routes](#data-sources-without-welink-cli); IM is welink-cli-only by design. |
| **WeLink Meeting sdkcache.db** [verified-encrypted] | `~/.AppData/Roaming/WeLink Meeting/hwdata/sdkcache.db` | SQLite-shaped but `file is not a database` on open — **encrypted or proprietary format**. Meeting SDK cache. | **potential meeting-duration signal** — now lower priority since welink-cli `meeting query-list` gives duration directly. Needs a decryption/access path or a different reader; not directly readable as SQLite. |
| **WeLink Meeting recordings** [verified] | `D:\MeetingRecordings\` + `Recent/*会议*.lnk`, `Recent/*meeting*record*.lnk` | Meeting recording files (video/audio) + `.lnk` shortcuts with embedded timestamps. E.g. `20260713 09.55.29 会议 99997299.lnk`, `20260713_111710_meeting_record.*.pdf`. | **meeting occurrence + duration** — recording file mtime/duration = meeting time; `.lnk` timestamp = meeting date. A real meeting-time signal independent of welink-cli. Recording duration extracted via ffprobe = actual meeting length. **Backup for welink-cli `meeting query-list`** (see [backup routes](#data-sources-without-welink-cli)); ffprobe duration extraction built (Phase 9.1), falls back to mtime-only when ffprobe absent. |
| **WeLink Meeting plugin config** [verified] | `~/.AppData/Roaming/WeLinkMeetingPlugin/`, `~/.AppData/Roaming/WelinkeShare/` | Meeting plugin config/cache | supplementary meeting metadata |
| **Outlook (Exchange) OST/PST** [verified-COM] | `~/AppData/Local/Microsoft/Outlook/*.ost` (Windows default). Mac: `~/Library/Group Containers/UBF8T346G9.Office/Outlook/`. **9.3 verdict (2026-07-29):** OST EXISTS at custom path `D:\Email\bogao@huawei.com.ost` (206.9 MB) — the SKILL.md note "Not present on author's machine" is **outdated**. The default `~/AppData/Local/Microsoft/Outlook/` dir has only RoamCache + spscoll.dat (no .ost there), but the real OST is at `D:\Email\` alongside 6 seasonal PST archives. **Access path: Outlook COM/MAPI works** via pywin32 (`pip install pywin32` from tuna mirror succeeds). `Outlook.Application` Dispatch succeeds; Inbox (50 items) and Sent Items (38 items) are readable with subject, sender, received time, attachments. libpff/pffexport/pypff FAILED on Windows (C build error in pyproject.toml — no prebuilt wheel). Graph API not tested (needs admin consent). Adapter: `outlook_adapter.py` — **functional, emits `kind="email"` events matching welink-cli mail shape**. COM requires Outlook desktop installed with a configured profile; Windows-only. |
| **Outlook Web / Exchange via Graph API** [unverified] | Microsoft Graph API (requires Azure app registration + consent) | Calendar events, mail messages, tasks via REST | same data as OST, accessible without desktop Outlook. **[unverified]** — requires org admin consent for Graph access; may be blocked in corporate env. **Now lower priority**: welink-cli covers email+calendar without admin consent for colleagues who have it. |
| **iCalendar (.ics) export** [verified-format] | User exports calendar to `.ics` (Outlook: File → Open & Export → Import/Export → Calendar; WeLink: check calendar export) | Open-format calendar file — VEVENT entries with DTSTART/DTEND, SUMMARY, ATTENDEES. Parsed by Memacs (`memacs_ical.py`) and any iCalendar library. | **low-friction meeting-duration signal** — sidesteps both OST-parsing (proprietary) and Graph-API (admin consent) blockers. User-triggered export, then retrospective parse. Now a fallback for colleagues without welink-cli; welink-cli `calendar list` gives the same data without a manual export step. Weaker for email (only calendar events, not mail). **Backup for welink-cli `calendar list`** (see [backup routes](#data-sources-without-welink-cli)); parser built with auto-discovery + RRULE/TZID support (Phase 9.2). |
| **WeLink Desktop (local app data)** [verified — no messages] | `~/.AppData/Roaming/WeLink_Desktop/appdata/**/*.db` (52 DBs) | config / login / UI state / adaptiveCard configs only | none for time-tracking |

**Meeting-duration sources, ranked by promise:** welink-cli `meeting query-list`
(actual start_time+end_time in millis — direct duration, no inference needed) > iCalendar
`.ics` export (open format, low friction, sidesteps OST + Graph blockers — technique from
Memacs) > Outlook OST/Graph (colleagues who use it, higher friction) > WeLink Meeting
recordings (present here, needs ffprobe duration extraction) > welink-cli `calendar list`
(scheduled duration, may differ from actual) > sdkcache.db (encrypted, uncertain).

### E. Browsing & downloads

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **Chrome history** [verified] | `~/.AppData/Local/Google/Chrome/User Data/Default/History` (SQLite; copy-then-read — Chrome holds a lock while running) | tables `urls`, `visits` (visit_time = micros-since-1601, Chrome epoch), `downloads` (start_time/end_time/target_path), `keyword_search_terms` (search queries) | page-visit occurrence; download events with start+end; search queries = research activity. Categorize by URL/title. |
| **Edge history** [verified] | `~/.AppData/Local/Microsoft/Edge/User Data/Default/History` | same schema as Chrome | same — if the colleague uses Edge too |

### F. Filesystem activity

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **Windows Recent** [verified] | `~/.AppData/Roaming/Microsoft/Windows/Recent/*.lnk` (175 files on author's machine) | `.lnk` files — each embeds a timestamp inside (not just mtime); must parse shell-link format. Sample shows PPTX, PDF, meeting recordings, SVG assets. | file-open occurrence; category from file type + path |
| **Jump Lists** [verified] | `~/.AppData/Roaming/Microsoft/Windows/Recent/AutomaticDestinations/*.automaticDestinations-ms` | Per-app recent docs, grouped by application | richer than Recent — app + doc pairs |

### G. Remote knowledge authoring (publish-timestamp sources)

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **CloudDevOps Wiki** [unverified] | `clouddevops-wiki` skill or CloudDevOps REST API (NOT MCP) | unknown — access path needs investigation | doc-authoring task instances ("documentation work" category, from publish/edit timestamps) |
| **3ms** [verified plugin] | `huawei-3ms` plugin in this repo (search + read) | 站内知识, wiki, doc library | knowledge-sharing task instances (from post/edit timestamps) |
| **W3 search** [unverified] | "MCP 工具或 API" | unknown | marginal (publish dates) |

### H. Auxiliary (lifecycle / background — weak time signal)

| Source | Detector | Data layout | Time signal |
|--------|----------|-------------|-------------|
| **Claude Code daemon.log** [verified] | `~/.claude/daemon.log` | supervisor log with timestamps (daemon start, worker spawns) | background task timing — weak |
| **Claude Code tasks/jobs** [verified] | `~/.claude/tasks/<uuid>/`, `~/.claude/jobs/` | background task/job records | background task timing — weak |
| **Claude Code shell-snapshots** [verified] | `~/.claude/shell-snapshots/` | timestamped bash snapshots | shell-session timing — weak |
| **Claude Code file-history** [verified] | `~/.claude/file-history/<uuid>/` | per-session file edit history | file-edit timing (redundant with VSCode Local History if both present) |
| **Codeagent equivalents** [verified] | `~/.cac/file-history/`, `~/.cac/shell-snapshots/`, `~/.cac/tasks/` if present | same shapes | same — weak |

**Local-CLI-to-remote-service ≠ local store.** welink-cli, nga.cmd, and Graph API hit remote
services needing auth + proxy (`NO_PROXY` for `open.inner.welink.huawei.com`,
`cmc.centralrepo.rnd.huawei.com`; Azure consent for Graph). Group by where data lives / what
network+auth it needs, not where the binary sits.

## Task model

A **task** is the unit of work being tracked — not a session, not a single tool call. The
goal is to reconstruct, per task: boundaries, duration, effort, input, output, success. Tasks
come in two flavors:

### Explicit tasks (from `TaskCreate` / `TaskUpdate`)
Where the AI used the task tools, the model is given directly. Verified in Claude Code
sessions (50 TaskCreate, 99 TaskUpdate, 121 TaskOutput, 51 TaskStop). A task instance:

| Field | Source | Example |
|-------|--------|---------|
| **id** | `TaskCreate` input (or synthesized) | taskId "1" |
| **subject** | `TaskCreate.input.subject` | "Archive V3.2 refs, install V3.3 master as baseline" |
| **description / input** | `TaskCreate.input.description` + preceding `user` message | "Create references/archive-v3.2/, move 5 V3.2 reports..." |
| **start** | timestamp of the `TaskCreate` tool_use | ISO 8601 from the line |
| **end** | timestamp of `TaskUpdate(status=completed)` or last event in the task's thread | ISO 8601 |
| **duration (wall-clock)** | end − start | minutes/hours |
| **duration (effort)** | sum of `assistant.message.usage.output_tokens` over the task's messages; nga.cmd runtime for legacy | token count |
| **output** | `tool_result` contents + `Write`/`Edit` target paths + final assistant text + any `git` commit that follows | file paths, command output, commit hash |
| **success** | `TaskUpdate(status=completed)` AND absence of `tool_result.is_error=true` AND no user correction in following messages | three-valued (succeeded/failed/unknown) + evidence |
| **sub-stages** | `EnterPlanMode`/`ExitPlanMode` = planning phase; `TaskOutput`/`TaskStop` = background sub-tasks | phase markers |

### Implicit tasks (inferred when no `TaskCreate`)
Most sessions don't use task tools. For these, infer task boundaries from **user-message
turns**: each user message that introduces a new goal starts a task; the task ends at the
next user-message turn or session end. A single session may contain several implicit tasks.
This is noisier — a 10-message thread might be one task or three. Heuristics to refine:
- A user message that's a correction/continuation ("no, do X instead", "now also Y") extends
  the current task; a message with a new subject starts a new one.
- Long gaps between messages (e.g. >30min) suggest a task boundary.
- Tool-call clusters serving one goal = one task; a shift in tool target (different file/
  project) = new task.

### Tasks outside AI sessions
Meetings, manual coding, doc-writing in a browser, email — these have no `TaskCreate`. Their
boundaries come from:
- **Meetings:** Outlook calendar events (start/end) or WeLink Meeting recordings (timestamp +
  duration). Subject = meeting title. Output = recording/notes. Success = harder (attended?
  decision reached? — infer from follow-up messages).
- **Email:** Outlook send/receive times + thread subjects. Each email thread = a task
  instance (category "communication"). Duration is weak (send time ≠ composing time).
- **Manual coding:** VSCode Local History edits + git commits outside any AI session. Output
  = edited files / commits. Success = commit landed / tests pass (if detectable).
- **Browsing/research:** Chrome/Edge visits + `keyword_search_terms`. A cluster of visits on
  one topic = a research task. Duration inferred from visit-density.

### Success/failure signals (per task type)
| Task type | Success signal | Failure signal | Unknown (default) |
|-----------|----------------|----------------|-------------------|
| AI coding (explicit task) | `TaskUpdate(completed)` + no `is_error` | `TaskUpdate` to failed/cancelled, or `tool_result.is_error=true`, or user correction following | no terminal TaskUpdate |
| AI coding (implicit) | assistant `stop_reason=end_turn` + user doesn't correct | user correction ("不对", "又错了", "you didn't...") in next message | stop_reason other than end_turn with no errors |
| Meeting | follow-up message references a decision/outcome | (no failure signal defined) | no follow-up detected |
| Email | reply sent / thread resolved | (no failure signal defined) | thread abandoned (no reply detected) |
| Manual coding | commit lands / build passes | commit reverted / build fails | no commit detected |
| Research | a doc/action follows the browsing (output produced) | (no failure signal defined) | browsing with no follow-up artifact |

**Memory stores as a success signal:** the new-codeagent / Claude Code per-project memory
holds `feedback_*.md` files — user corrections harvested by those tools. A correction = the
task that preceded it didn't fully succeed. Mine these as cross-cutting success/failure
evidence (auxiliary, not primary).

## The core challenge: duration is not given, it must be inferred

Almost all sources emit *occurrence* (when) and *category* (what kind). Direct duration
signals are rare and source-specific:

- **Wall-clock from timestamps** — span from first-to-last event in a task. Inflates: a
  session open 4h with 3 messages isn't 4h of work. Good for meetings (calendar start/end).
- **Per-message `usage` tokens** (Claude Code / new-codeagent) — sum over a task's messages
  = AI effort. Per-step, rich. But measures AI-effort, not human-effort (under-counts
  thinking time the AI never sees).
- **nga.cmd runtime** — legacy codeagent only; AI runtime per session.
- **Event-density** — messages/commits/edits per window as an engagement proxy.
- **Meeting recording duration** — extractable from recording file metadata = actual meeting
  length. Stronger than calendar start/end (which may not match actual attendance).
- **Outlook calendar start/end** — meeting duration as scheduled (may differ from actual).

The effort signal hierarchy: per-message `usage` (Claude Code / new-codeagent) > nga.cmd
(legacy) > wall-clock span (any). VSCode Local History and browser downloads give cleaner
file-level events than session transcripts, but still occurrence, not duration.


## Storage shape
A time log is structured time-series data. It does NOT fit in a SKILL.md (prose guidance).
Needs its own data file under this skill's dir.

**Leading candidate: OCEL 2.0 (Object-Centric Event Log)** via `pm4py`. A flat timeline
(Memacs/Plaso shape) cannot represent many-to-many event↔object relations without duplication
— but "a task touches multiple files, and a file is touched by multiple tasks" is exactly
that. OCEL 2.0's E2O/O2O relational model handles it natively. This likely replaces "flat
timeline" as the fusion-target schema. (See `research-findings.md` → "Deep research results",
find #1.) Alternative: flat SQLite timeline (Plaso-style) — simpler but loses relational
structure. Underlying format question (SQLite vs JSON) is secondary to the schema-model
choice.

Open: whether the log is committed to the repo — a personal time log is sensitive performance
data, and for a shared skill each colleague's log is their own.

## Open questions

Each question lists candidate methods from the deep research (see `research-findings.md` →
"Deep research results" and `Task Reconstruction Research Methods.md`). Listed as candidates,
not commitments.

- **Task taxonomy:** derive automatically (from session `ai-title`/`custom-title`,
  `TaskCreate.subject`, tool-call patterns, commit messages, chat topics, browser URL
  domains, email subjects, **file paths + package-config manifests** — domain detection from
  touched files/packages is a stronger signal than commit subjects, per Git Timeline MCP) vs.
  let the user define it? Likely hybrid: auto-derive a draft taxonomy, let the user
  merge/rename. *Candidate methods:* PPMI embeddings + K-means/DBSCAN for unsupervised
  clustering; LLM + RAG for consistent human-readable labels; RIPPER rules (`wittgenstein`)
  as an interpretable, user-auditable fallback.
- **Implicit-task boundary heuristics:** what gap threshold / subject-shift rule best splits
  a session into tasks? *Candidate methods:* PELT change-point detection (`ruptures`) on
  multivariate activity features; 2-component GMM on log inter-arrival times to learn a
  personalized gap threshold; adaptive-windowing concept-drift detection. Failure mode to
  watch: over-segmentation (a chat reply flagged as a new task). Needs experimentation
  against real sessions, validated with WindowDiff / Collar-Based F1 (`segeval`).
- **Cross-source task identity:** when an AI session, a git commit, and a browser visit
  belong to one task, how do we link them? *Candidate methods:* Fellegi-Sunter probabilistic
  record linkage (`Splink`, unsupervised EM, DuckDB-backed) — watch for conditional-
  independence violation on correlated URL+title; temporal-decay graph + Leiden community
  detection (`igraph`) — watch for embedding cost and decay-param tuning.
- **Effort vs. time:** which dominates? Per-message `usage` tokens give effort; wall-clock
  gives time. Which does the log optimize for? Likely report both. *Candidate method for
  active-vs-idle:* Allen's Interval Algebra (13 relations) to union overlapping/meeting
  intervals and excise gaps. *Candidate for human-vs-AI effort:* discount diffs that match
  preceding AI outputs (see research find #3).
- **Task I/O + success attribution:** *Candidate methods:* PROV-O provenance graph (`prov`
  library) — `used` for inputs, `wasGeneratedBy` for outputs; Semantic Role Labeling + a
  heuristic state machine for success/failure (error code → stack-trace prompt = "Failure /
  Retry"; commit + passing tests = "Success"). Open-ended/research tasks default to
  "Completed/Abandoned" on temporal expiry.
- **Evaluation / ground truth:** how to validate reconstructed tasks with no labels?
  *Candidate methods:* manually annotate a small benchmark subset (one day of logs), then
  tune with WindowDiff, Pk, Boundary Edit Distance, Collar-Based F1 (`segeval`, `chunkseg`);
  unsupervised intrinsic metrics (Silhouette, Modularity) for ER cluster quality; LOOCV for
  rule-induction generalization.
- **Storage shape (schema):** OCEL 2.0 (`pm4py`) vs flat SQLite (Plaso-style) — see
  "Storage shape" above. Decide before implementation.
- **Incremental processing / watermark:** how to avoid reprocessing full history each run?
  The skill-forge component uses `last_run.txt` with two-axis incremental analysis
  (new sessions + new messages in old sessions). retro-scope needs an equivalent — especially
  for Claude Code's growing store (39,925 lines). Affects adapter design. Not yet specified.
- **Output / report format:** ✅ RESOLVED (Phase 9.7) — stdout text, JSON, Markdown file,
  CLI table, and self-contained HTML (with inline CSS + SVG bar chart) all built. `--format`
  and `--output` flags control output.
- **MVP scope / phasing:** the first working slice is BUILT (see `scripts/` and
  `scripts/README.md`). It covers Claude Code sessions only → task boundaries (explicit via
  TaskCreate + implicit via user-message turns + gap heuristics) → time aggregation by
  day/week/month → text report. Standard library only, no external deps. Verified against the
  author's data: 32 sessions, 48,575 events → 856 tasks, 128.9h across 4 weeks. Next layers:
  (a) richer task-model fields (effort via usage tokens — sparse in current data; success via
  tool errors; outputs via Write/Edit targets), (b) a second source adapter (git), (c) cross-
  source identity, (d) the research-informed methods (PELT, OCEL 2.0, etc.).
- **WeLink Meeting sdkcache.db access:** it's SQLite-shaped but `file is not a database` on
  open — encrypted or proprietary. **Now lower priority** — welink-cli `meeting query-list`
  gives meeting duration (start_time+end_time millis) directly, sidestepping sdkcache.db
  entirely. Finding a reader remains a nice-to-have for offline/cross-check use.
- **WeLink Meeting recording duration:** ✅ RESOLVED (Phase 9.1) — ffprobe duration
  extraction built and live on the author's machine. Falls back to mtime-only when ffprobe
  is absent.
- **Outlook/Exchange access path:** ✅ RESOLVED (Phase 9.3, 2026-07-29). Three paths
  investigated: (1) libpff/pffexport/pypff — FAILED on Windows (C build error in
  pyproject.toml, no prebuilt wheel available from tuna mirror); (2) Outlook COM/MAPI via
  pywin32 — WORKS (`pip install pywin32` succeeds, Dispatch succeeds, Inbox/Sent Items
  readable with subject/sender/timestamps); (3) Graph API — not tested (needs admin
  consent, lowest priority). The adapter (`outlook_adapter.py`) uses the COM path.
  Key finding: the OST file exists at `D:\Email\bogao@huawei.com.ost` (custom location,
  206.9 MB), NOT at the default `~/AppData/Local/Microsoft/Outlook/` (which has only
  RoamCache + spscoll.dat). The COM Stores collection discovers OST/PST files at any path.
  Limitation: COM is Windows-only and requires Outlook desktop with a configured profile.
- **welink-cli calendar subcommands:** ✅ RESOLVED — welink-cli exposes `calendar list/get/
  create` (ISO start/end, end-exclusive date ranges) alongside `im`, `meeting`, `mail`,
  `contact`, `search`, `onebox`. The full subcommand surface is documented in the WeLink
  CLI skill article (2026-05-21). Adapter `welink_cli_adapter.py` collects all four
  relevant domains (meeting/calendar/mail/im).
- **nga.cmd / new codeagent metrics:** does new `codeagent` have metrics subcommands? (Now
  lower priority — per-message `usage` covers new-codeagent; nga.cmd is legacy-only fallback.)
- **Unverified sources to confirm when a colleague has them:** codex (`~/.codex`), openclaw,
  hermes-agent, CloudDevOps Wiki access path, W3 access path, Outlook/Graph.
- **Platform paths:** catalog paths are Windows-centric (verified on the author's Win11).
  Mac/Linux equivalents (e.g. `~/Library/Application Support/...` for VSCode/Chrome,
  `~/Library/Group Containers/UBF8T346G9.Office/Outlook/` for Mac Outlook) need adding for
  colleagues on other platforms.
- **Library verification:** confirm the core libs install before committing — `plaso`,
  `pm4py`, `ruptures`, `Splink`, `igraph`, `wittgenstein`, `prov`, `segeval`. (GoldenMatch
  and llm-context-ts confirmed by the other agent but not independently verified; methods
  available independently of those packages regardless.)
- Canonical internal starting point for the toolchain:
  `https://3ms.huawei.com/km/blogs/details/22148443` (Node.js install blog — likely links
  onward to the rest).

