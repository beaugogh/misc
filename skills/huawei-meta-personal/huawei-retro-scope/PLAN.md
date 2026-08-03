# PLAN — huawei-retro-scope implementation roadmap

**Status as of 2026-08-03: Phases 0a–12 are BUILT and verified. All planned items complete.** 522 tests pass (5 skipped).
14 source adapters registered; 13 detect on the author's machine. The pipeline runs
end-to-end via `python run.py` with multi-horizon analysis (90d/30d/7d/1d default),
content-driven root-cause narratives, human-involvement detection, three-way time
accounting (wall/active/human), parallel-task detection, three-valued success, and
stage-by-stage drill-down. Phase 9 (backup routes) built via 6 parallel sub-agents across 3
waves; Phase 10 (model frontiers) built via 3 parallel sub-agents in 1 wave + integration;
Phase 11 (human time sinks + content-driven analysis) built iteratively across multiple
commits. See the dispatch records below.

Each phase produces a working, testable increment. Phases are ordered by dependency: earlier
phases unblock or inform later ones. Items within a phase are roughly independent.

---

## Phase 0a — Bug fixes that improve output correctness  [no new deps] ✅ DONE

- [x] **0a.1 Fix explicit-task scope under-bounding.** Track open tasks by `taskId` across
      the whole session; close on session end if no update arrives; mark
      `task_status="unknown"` rather than `None`. *(Fixed: 0 tasks ≤5s, was most of them.)*
- [x] **0a.2 Thread `tool_use_id` onto tool_result.** Carry `tool_use_id` through so
      tool_result events link back to their tool_use. *(Fixed: 100% of 8,195 tool_results
      now carry tool_use_id.)*

---

## Phase 0b — Architectural refactor + tooling  [no new deps] ✅ DONE

- [x] **0b.1 Tests.** 14 tests in `tests/test_pipeline.py` (stdlib `unittest`): synthetic
      JSONL fixture, explicit/implicit segmentation, boundary heuristics, aggregation,
      classifier, timestamp normalization. Pinned before refactor, pass after.
- [x] **0b.2 Adapter registry abstraction.** `SourceAdapter` protocol + `SourceRegistry`
      in `sources.py`. 10 adapters registered. Pattern proven (Memacs/Plaso).
- [x] **0b.3 Unified event schema.** `make_event()` in `sources.py` with `source_kind`
      discriminator (ai_session/vcs/browser/filesystem/meeting/comm/doc_authoring/auxiliary).
      All adapters emit via `make_event()`.
- [x] **0b.4 `run.py` entrypoint.** Single CLI: `--granularity`, `--json`, `--since/--until`,
      `--task <id>`, `--sources`, `--check`, `--persist`, `--rebuild`.

---

## Phase 1 — Second source: git / CodeHub  [no new deps] ✅ DONE

- [x] **1.1 `git_adapter.py`.** `git log --numstat` (commits with insertions/deletions/files)
      + `git reflog` (branch checkouts). `source_kind=vcs`. Timestamps from `%cI`.
- [x] **1.2 Project-dir discovery.** `discover_git_roots()` from session `cwd` values;
      deduplicates nested roots (41 cwds → ~6 real repos).
- [x] **1.3 Effort signal from git.** `--numstat` gives per-file insertions/deletions;
      captured per commit event. AI-effort discounting deferred to Phase 4 (needs cross-ref
      of diffs vs AI outputs).
- [x] **1.4 Coarse cross-source linking (MVP, throwaway-by-design).** `cross_source.py`:
      same-cwd + time-window heuristic. 28 tasks linked to git commits. Labeled as
      scaffolding — replaced by Phase 4.4 Leiden linker (which runs after it).

---

## Phase 2 — Output persistence + incremental/watermark  [no new deps] ✅ DONE

- [x] **2.1 Task-log persistence.** `persistence.py`: `output/tasks.jsonl` (append-only,
      merge by task id). `output/` gitignored.
- [x] **2.2 Watermark file.** `output/last_run.txt` (epoch seconds). Two-axis incremental:
      new sessions + new messages in old sessions.
- [x] **2.3 Incremental adapter contract.** `collect_since(watermark)` on `SourceAdapter`;
      JSONL adapters scan per-file; git adapter uses `--since`.
- [x] **2.4 `--rebuild` flag.** Ignores watermark, full reparse.

---

## Phase 3 — Richer task-model fields + report depth  [no new deps] ✅ DONE

- [x] **3.1 Effort estimation (active vs idle).** `_compute_active_seconds()`: inter-event
      span summation with gap threshold excision. Collar-based per-event padding was
      deliberately removed (see `segment_tasks.py` docstring). Reports both
      `wall_clock_seconds` and `active_seconds`.
- [x] **3.2 Success/failure attribution.** `_determine_success()`: per-task-type table
      (explicit: TaskUpdate status + is_error; implicit: stop_reason + corrections).
      `success` (bool|None) + `success_evidence` (str) on every task.
- [x] **3.3 Input capture.** `_extract_inputs()`: user prompts, Read files, WebFetch URLs,
      WebSearch queries, Grep patterns. `inputs` list on every task.
- [x] **3.4 Output capture (fuller).** Write/Edit paths, Bash artifact-producing commands
      (mkdir/curl/wget/touch/cp/mv), NotebookEdit, git commits. `outputs` list capped at 20.
- [x] **3.5 Report: task drill-down.** `--task <id>` via `render_task_detail()`: full
      detail (subject, status, success, time, effort, tools, inputs, outputs, git commits).
      Weekly report shows wall/active time + success rates per kind.

---

## Phase 4 — Cross-source identity + better segmentation  [deps: ruptures, sklearn, igraph] ✅ DONE

- [x] **4.1 Library verification + install.** `ruptures`, `scikit-learn`, `igraph`
      installed from tuna mirror. `splink` failed to install (silent failure) — used the
      documented igraph+Leiden alternative. `pm4py`, `wittgenstein`, `prov` also installed
      (for Phases 5/7). Documented in `research-findings.md`.
- [x] **4.2 PELT boundary detection.** `advanced_segment.py`: PELT (`ruptures`) on
      multivariate features (timestamp + kind one-hot + cwd hash). Penalty β = 10 × n_features
      (heuristic; needs tuning against a labeled benchmark). Falls back to naive for <20 or
      >5000 events.
- [x] **4.3 GMM inter-arrival threshold.** `learn_gap_threshold()`: 2-component GMM
      (`sklearn`) on log inter-arrival times. Learns a personalized threshold per user;
      falls back to 30 min if <30 events.
- [x] **4.4 Cross-source identity (Leiden via igraph).** `entity_resolution.py`: temporal-
      decay graph (`w_ij = sim * exp(-λΔt)`) + Leiden community detection. 943 tasks → 278
      clusters (52 multi-task). Splink unavailable; igraph path used as documented fallback.
      Over-merges some clusters (59-task cluster) — semantic similarity on cwd is coarse;
      needs tuning.
- [x] **4.5 Evaluation harness.** WindowDiff + Collar-Based F1 against a hand-labeled
      benchmark. Built in Phase 9.8 — `eval_segmentation.py` (22 tests, pure stdlib),
      `--eval` flag live. Baseline: WindowDiff=0.417, F1=0.222 (recall 14.3% — PELT β
      under-segments; this is the baseline to tune against). Fixture at
      `tests/fixtures/eval_benchmark.json` (4 sessions, 1711 events, 21 boundaries).

---

## Phase 5 — Storage migration to OCEL 2.0  [dep: pm4py] ✅ DONE

- [x] **5.1 OCEL 2.0 schema mapping.** Object types: task, file, commit, session. Event
      types: task_started, task_ended, file_edited, committed. E2O relations mapped.
- [x] **5.2 Migrate to OCEL SQLite via `pm4py`.** `ocel_store.py`: `build_ocel()` builds
      an OCEL from tasks; `save_ocel_sqlite()` writes to `output/ocel.sqlite`. JSONL log
      kept as fallback.
- [x] **5.3 Relational queries.** `relational_query_files_multi_task()`: "files touched by
      >1 task" — returns 134 files (top: `wushan_assistant_brainstorm` at 41 tasks). This
      is the query a flat timeline can't answer.

**Note:** pm4py is AGPL v3 — commercial use requires open-sourcing. The JSONL fallback
remains available if that's a concern.

---

## Phase 6 — More sources  [selective deps] ✅ DONE

- [x] **6.1 New-codeagent adapter** (`~/.cac/projects/`). `CodeagentAdapter` subclass of
      `ClaudeCodeAdapter` — reuses the JSONL parser, relabels `source="codeagent"`.
- [x] **6.2 Legacy-codeagent adapter** (`ngagent.db` SQLite). Built in Phase 9.5 —
      `LegacyCodeagentAdapter` reads `ngagent.db` SQLite (opencode DB). Verified schema:
      session/message/part/project/metrics tables, millis timestamps. Emits
      user_message/assistant_message/tool_use/tool_result/reasoning events. First SQL
      adapter — first real SQL-level incremental (`WHERE time_created > ?` in millis).
      263 events extracted live. 19 tests.
- [x] **6.3 Browser history adapter** (Chrome/Edge). `browser_adapter.py`: copy-then-read
      (Chrome locks while running). Emits visit/download/search events. Chrome-epoch
      (micros-since-1601) normalized to Unix epoch.
- [x] **6.4 VSCode Local History adapter.** `more_adapters.py`: parses `entries.json` per-
      file edit versions with millis timestamps.
- [x] **6.5 iCalendar (.ics) adapter.** `more_adapters.py`: stdlib VEVENT parser (no dep).
      Detects `.ics` in `output/`, `~/Calendar/`, `~/Documents/`. Needs the user to export
      their calendar. → enhanced in Phase 9.2 (auto-discovery + WeLink/Outlook export help).
- [x] **6.6 WeLink Meeting recordings.** `more_adapters.py`: walks `D:\MeetingRecordings`,
      emits meeting_recording events with file mtime. (`.lnk` parsing uses mtime fallback;
      `ffprobe` duration extraction not yet implemented — would give actual meeting length.)
      → ffprobe duration extraction folded into Phase 9.1.
- [x] **6.7 welink-cli adapter.** `welink_cli_adapter.py`: `WeLinkCLIAdapter` — one tool,
      four domains. **Live-verified 2026-07-30** against a real authenticated instance:
      `meeting query-list` (39 meetings w/ start_time+end_time millis = **direct meeting
      DURATION** — the #1 ranked gap in SKILL.md; page-size max 30), `calendar list` (53
      events w/ ISO start/end), `mail list` (23 emails inbox+sent), `im query-history-message`
      (666 chat messages, two-step: enumerate conversations then fetch). Defensive envelope
      parsing (`{data:{data:[]}}`, `{conversation_info:[]}`, `{respData:{chatInfo:[]}}`),
      API-error detection, CARD_MSG text extraction. `detect()` checks `welink-cli` in PATH.
      IM is now **enabled by default** (`enable_im=True` in `default_registry()` —
      Phase 11.4 enabled it after the user noticed it was missing; 790 IM messages
      collected live). 19 tests pinning the parsing contract. **This single adapter retires the meeting-
      duration gap and partially retires the Outlook/Graph email+calendar blocker** (6.10)
      for colleagues with welink-cli.
- [x] **6.8 Windows Recent.** `more_adapters.py`: `.lnk` files with mtime + target-from-name.
      Jump Lists (`.automaticDestinations-ms`) not yet parsed — lower priority.
- [x] **6.9 3ms adapter.** `more_adapters.py`: `ThreeMsAdapter` — detector-only (`detect()`
      checks for `opencli` in PATH). `collect()` is a no-op placeholder; the plugin doesn't
      expose publish timestamps in a structured way yet.
- [x] **6.10 Unverified sources.** Built in Phase 6.10 — `unverified_adapters.py` with
      5 adapters: `CodexAdapter` (~/.codex/sessions/, JSONL, defensive parsing for both
      Claude-Code-style and Codex-style schemas), `OpenclawAdapter` (~/.openclaw/,
      JSONL+SQLite), `HermesAgentAdapter` (~/.hermes-agent/, JSONL+SQLite),
      `CloudDevOpsWikiAdapter` (via opencli, detector-only placeholder),
      `W3Adapter` (via opencli, detector-only placeholder). Each detect() returns False
      when the tool isn't present — silently skips on machines without them, works for
      colleagues who do use them. 19 tests.

---

## Phase 7 — Categorization + reporting polish  [deps: sklearn, wittgenstein] ✅ DONE

- [x] **7.1 Domain detection from file paths + package manifests.** `categorize.py`:
      `detect_domain()` infers business domain (auth, api, ui, data, test, docs, config,
      ml, skill, meeting) from file paths + package-config filenames. 15 categories vs
      the crude classifier's 4.
- [x] **7.2 Auto-taxonomy.** `cluster_tasks_ppmi()`: PPMI embeddings + K-means (sklearn).
      Produces 8 clusters from 964 tasks.
- [x] **7.3 LLM labeling.** Built in Phase 7.3 — `llm_labeling.py` with `LLMLabeler`
      class. Auto-detects 3 local LLM backends: Ollama (preferred, `ollama run`),
      llama-cpp-python (GGUF), Hugging Face transformers (pipeline). Falls back
      gracefully to None when no LLM is installed — the rule-based path (7.1 + 7.4)
      stands alone. `label_tasks()` adds `task["llm_label"]` — a 3-5 word
      natural-language label grounded in the task's actual content (subject, inputs,
      tools, errors, narrative). Wired into run.py as an optional post-processing step.
      18 tests (1 skipped: integration test needs a real LLM).
- [x] **7.4 RIPPER interpretable fallback.** `train_ripper_rules()`: trains `wittgenstein`
      RIPPER on labeled tasks, emits auditable if-then rules.
- [x] **7.5 Report formats.** Built in Phase 9.7 — `render_markdown()` + `--output`,
      `render_table()` + `--format table`, `render_html()` (self-contained HTML with inline
      CSS + SVG chart). All five formats work: stdout text, JSON, Markdown, table, HTML.

---

## Phase 8 — Sharing hardening  [no new deps] ✅ DONE

- [x] **8.1 Platform path abstraction.** `platform_paths.py`: per-OS paths for Claude Code,
      codeagent, Chrome, Edge, VSCode, Outlook, Windows Recent, WeLink recordings. Win/Mac/
      Linux covered.
- [x] **8.2 Per-run discovery report.** `--sources` and `--check` flags show found/used/
      skipped with reasons.
- [x] **8.3 No-hardcoded-identity audit.** `audit_no_hardcoded_identity()` checks source
      code for hardcoded user paths. Returns clean.
- [x] **8.4 Packaging.** `requirements.txt` (optional deps clearly separated from stdlib
      core), README Quick Start, `--check` one-line install check.

---

## Phase 9 — welink-cli backup route + remaining TODOs  [mixed deps] ✅ DONE

**Goal:** the skill must deliver the same four data domains (meetings / calendar / mail /
IM) on machines that do NOT have welink-cli installed. welink-cli becomes the preferred
path when present; the adapters below are fallbacks that the registry runs when welink-cli
is absent (or in addition, for cross-validation). Per SKILL.md, the alternatives already
ranked by promise are:

| welink-cli domain | Backup path (no welink-cli) | Status after Phase 9 |
|-------------------|-----------------------------|----------------------|
| meetings (duration) | WeLink recordings + ffprobe; sdkcache.db (encrypted — stretch) | ✅ ffprobe duration extraction built (9.1); ffprobe installed on author's machine |
| calendar | iCalendar `.ics` export (Outlook/WeLink manual export) | ✅ auto-discovery + RRULE + TZID built (9.2); needs manual export |
| mail | Outlook OST (libpff/pffexport) or Graph API | ✅ Outlook COM adapter built + live (123 emails) (9.3) |
| IM (chat) | **No local store exists** (verified: 52 WeLink Desktop .db files, zero message tables) | No fallback possible — IM is welink-cli-only by design; surfaced honestly (9.4) |

The IM row is a hard constraint, not a gap to close: without welink-cli there is no chat
history to collect, period. The skill says so clearly in its discovery report (9.4) rather
than pretend otherwise.

### 9.1 Meeting-duration backup: ffprobe on WeLink recordings  [dep: ffprobe, optional] ✅
- [x] **9.1.1** `WeLinkRecordingsAdapter` enhanced: `_ffprobe_duration()` calls ffprobe,
      falls back to mtime-only when absent. `duration_seconds` in `tool_input` + `extra`.
      ffprobe IS installed on the author's machine — duration extraction is live.
- [x] **9.1.2** `_parse_recording_filename()` regex extracts date/time/meeting-ID from
      `20260713 09.55.29 会议 99997299.lnk` and `20260713_111710_meeting_record.*.pdf`.
- [x] **9.1.3** 6 filename-parser tests + 7 adapter tests (ffprobe present/absent/failing).

### 9.2 Calendar backup: iCalendar auto-discovery + export guidance  [no new deps] ✅
- [x] **9.2.1** `ICalendarAdapter` broadened: scans `~/Downloads` + `RETRO_SCOPE_ICS_PATHS`
      env var. RFC 5545 line unfolding added.
- [x] **9.2.2** Export-guidance messaging deferred to SKILL.md docs (Agent D added the
      "Data sources without welink-cli" section with export steps).
- [x] **9.2.3** 12 tests: RRULE DAILY/WEEKLY/MONTHLY expansion, TZID parsing, UTC, folding.

### 9.3 Mail backup: Outlook OST reader  [dep: Outlook COM] ✅
- [x] **9.3.1** Investigation verdict: **Outlook COM works** (libpff failed to install on
      Windows; Graph needs admin consent). COM via `pywin32`/`win32com.client` connects to
      the running Outlook instance. Recorded in SKILL.md.
- [x] **9.3.2** `OutlookAdapter` built: iterates mail stores, finds Inbox + Sent Items,
      emits `email` events matching the welink-cli mail shape. **Live: 123 emails collected.**
      `detect()` checks for `.ost` files. Defensive against locked/corrupt stores.
- [x] **9.3.3** Tests in `test_outlook.py` (detector + event shape + COM mock).

### 9.4 IM honesty: discovery-report messaging  [no new deps] ✅
- [x] **9.4.1** `--sources` output now prints a multi-line NOTE when welink-cli is absent:
      "IM/chat history is UNAVAILABLE. WeLink stores no messages locally; welink-cli is
      the only path to chat data." Plus backup-route pointer for meetings/calendar/mail.

### 9.5 Legacy-codeagent adapter (carried from 6.2)  [no new deps] ✅
- [x] **9.5.1** `LegacyCodeagentAdapter` built: reads `ngagent.db` SQLite. **Real DB found**
      at `~/.local/share/opencode/db/ngagent.db` (opencode DB). Verified schema: session/
      message/part/project/metrics tables, millis timestamps. Emits user_message/
      assistant_message/tool_use/tool_result/reasoning events. **First SQL adapter** —
      first real SQL-level incremental (`WHERE time_created > ?` in millis). 263 events
      extracted live.
- [x] **9.5.2** 19 tests: synthetic `ngagent.db` fixture, watermark filtering, schema
      resilience.

### 9.6 Jump List parsing (carried from 6.8)  [no new deps] ✅
- [x] **9.6.1** `JumpListAdapter` built: heuristic UTF-16LE byte-scan of
      `.automaticDestinations-ms` files, extracts file paths + mtime. 14 tests.

### 9.7 Report formats (carried from 7.5)  [no new deps] ✅
- [x] **9.7.1** `render_markdown()` + `--output <path>` (format inferred from extension).
- [x] **9.7.2** `render_table()` + `--format table` (fixed-width ASCII, stdlib only).
- [x] **9.7.3** `render_html()` — self-contained HTML with inline CSS + inline SVG bar
      chart, no external resources/JS. `--format html`. 39 tests total.

### 9.8 Evaluation harness (carried from 4.5)  [no new deps] ✅
- [x] **9.8.1** Hand-labeled 2026-07-14 (4 sessions, 1711 events, 21 reference boundaries).
      Fixture at `tests/fixtures/eval_benchmark.json`.
- [x] **9.8.2** `eval_segmentation.py`: WindowDiff + Collar-Based F1, pure stdlib (no
      segeval dep). 22 tests.
- [x] **9.8.3** `--eval` flag in `run.py`. Baseline metrics: WindowDiff=0.417, F1=0.222
      (recall 14.3% — current PELT β under-segments; this is the baseline to tune against).

### 9.9 Welink-cli install hardening doc  [no new deps] ✅
- [x] **9.9.1** "Installing welink-cli (optional)" section added to SKILL.md + README:
      both Windows gotchas (NO_PROXY for intranet registry; `--ignore-scripts` for the
      postinstall PowerShell bug), auth steps, `mail autodiscover` prerequisite.

---

## Parallelism: Phase 9 dispatch record (executed 2026-07-30)

Phase 9 was built via 6 parallel sub-agents across 3 waves. The table records the dispatch
plan AND the outcome. Each agent was scoped to disjoint files with explicit "do not touch"
constraints to prevent edit conflicts.

| Track | Tasks | Files touched | Agent | Outcome |
|-------|-------|---------------|-------|---------|
| **P1+P2+P8** | 9.1, 9.2, 9.6 (ffprobe + .ics + Jump Lists) | `more_adapters.py`, `tests/test_adapters.py` | A | ✅ 39 tests. ffprobe live. RRULE+TZID. JumpListAdapter. |
| **P3** | 9.5 (legacy codeagent) | new `legacy_codeagent_adapter.py`, `tests/test_legacy_codeagent.py` | B | ✅ 19 tests. Real ngagent.db found (opencode). 263 events. First SQL incremental. |
| **P5** | 9.7 (report formats) | `aggregate.py`, `run.py`, `tests/test_reports.py` | C | ✅ 39 tests. Markdown/table/HTML + `--format`/`--output`. |
| **P7** | 9.4 + 9.9 (IM-honesty + install doc) | `SKILL.md`, `scripts/README.md` | D | ✅ Install guide + backup-route table + IM-honesty in SKILL.md. |
| **P4** | 9.3 (Outlook OST) | new `outlook_adapter.py`, `tests/test_outlook.py`, SKILL.md | E | ✅ COM verdict. 123 emails live. Functional adapter. |
| **P6** | 9.8 (eval harness) | new `eval_segmentation.py`, `tests/test_eval.py`, `run.py` (`--eval`) | F | ✅ 22 tests. 21-boundary benchmark. Baseline F1=0.222. |
| **Integration** | Register all + IM-honesty code + verify | `sources.py`, `run.py` | main | ✅ 14 adapters registered. 186 tests pass (now 272 after Phase 10). Pipeline end-to-end. |

**Waves:**
- **Wave 1 (4 agents: A, B, C, D):** all touched disjoint files. Completed in ~2–10 min each.
- **Wave 2 (2 agents: E, F):** launched after C freed `run.py`. E investigated then built;
  F labeled then implemented. Both touched `run.py` but at different points (F added
  `--eval`, main added `--sources` IM-honesty post-hoc).
- **Wave 3 (main agent):** registered LegacyCodeagentAdapter + OutlookAdapter + JumpListAdapter
  in `sources.py`; added IM-honesty messaging to `--sources`; ran full suite (186 pass, now 272
  after Phase 10); verified pipeline end-to-end (267 tasks, all categories present).

---

## Parallelism: Phase 10 dispatch record (executed 2026-07-30)

Phase 10 was built via 3 parallel sub-agents in 1 wave + main-agent integration.

| Track | Tasks | Files touched | Agent | Outcome |
|-------|-------|---------------|-------|---------|
| **10.1** | Parallel-task intervals | new `parallel_tasks.py`, `tests/test_parallel.py`, `run.py` | A | ✅ 19 tests. detect_parallel_tasks + compute_exclusive_time. |
| **10.2** | Drill-down & root-cause | new `drill_down.py`, `tests/test_drill_down.py`, `run.py` (`--drill`) | B | ✅ 33 tests. detect_stages + detect_markers + narrative. |
| **10.3** | Three-valued success | `segment_tasks.py`, `tests/test_success.py`, `run.py` | C | ✅ 34 tests. succeeded/failed/unknown + refine_success. |
| **Integration** | Wire all into pipeline + verify | `run.py`, `sources.py` | main | ✅ refine_success + detect_parallel_tasks + compute_exclusive_time wired. 272 tests pass. Pipeline end-to-end. |

**Waves:**
- **Wave 1 (3 agents: A, B, C):** all touched disjoint files except `run.py` (coordinated via
  explicit integration points). Completed concurrently.
- **Wave 2 (main agent):** wired all three modules into `run.py` (refine_success after
  cross-source linking; detect_parallel_tasks + compute_exclusive_time before reporting;
  `--drill` mode for drill_down); ran full suite (272 pass).

---

## Cross-cutting: decisions resolved by doing the work

- **Storage shape** → ✅ resolved: OCEL 2.0 (Phase 5) for relational; JSONL interim (Phase 2) kept as fallback.
- **Incremental/watermark** → ✅ resolved (Phase 2): `output/last_run.txt`, two-axis incremental.
- **Output/report format** → ✅ resolved (Phase 9.7): stdout text, JSON, Markdown, table, HTML.
- **MVP scope** → ✅ done (Phases 0a–0b + built spine).
- **Implicit-task boundary heuristics** → ✅ resolved (Phase 4): PELT + GMM replace naive rules.
- **Cross-source identity** → ✅ resolved (Phase 4): Leiden graph clustering (splink unavailable).
- **Effort vs. time** → ✅ resolved (Phase 3): report both; active vs idle via interval union.
- **Task taxonomy** → ✅ resolved (Phase 7): domain detection + PPMI clustering + RIPPER.
- **Meeting-duration gap** → ✅ resolved for welink-cli users (Phase 6.7); Phase 9.1 closes
  it for non-welink-cli users via recording ffprobe duration.
- **welink-cli dependency** → Phase 9: backup routes ensure the skill works without
  welink-cli for 3 of 4 domains (meetings/calendar/mail). IM is welink-cli-only by design
  (no local store exists) — surfaced honestly in the discovery report (9.4). Phase 11.4
  enabled IM by default since the user explicitly wanted it.
- **Human vs machine time** → ✅ resolved (Phase 11.2): `human_involvement.py` detects
  human actions and computes `human_engaged_seconds` separately from `active_seconds`.
  Time sinks ranked by human cost, not raw active time.
- **Root-cause narrative quality** → ✅ resolved (Phase 11.1): `summarize.py` reads the
  actual event content (prompts, diagnostics, errors) and produces grounded narratives.
  Structured rendering (Phase 11.3.3) breaks them into labeled parts.
- **8h/day assumption** → ✅ resolved (Phase 11.2.4): `compute_actual_working_hours()`
  derives the denominator from real human activity.

---

## Phase 10 — Model frontiers: parallelism, drill-down, honest success  [no new deps] ✅ DONE

Born from the first real end-to-end analysis of the author's own data (2026-07-30). Three
limitations surfaced that are not edge cases — they are the frontier the skill must cross to
fulfill its mission (see the Constitution in SKILL.md). Built via 3 parallel sub-agents +
main-agent integration.

### 10.1 Parallel-task intervals  [no new deps] ✅
- [x] **10.1.1** `parallel_tasks.py`: `detect_parallel_tasks()` refines the flat task list
      into overlapping intervals with `thread_id` (foreground / background:<tool_use_id> /
      session:<id> / browser).
- [x] **10.1.2** Detects parallel via: (a) TaskCreate/TaskOutput/TaskStop background
      lifecycle, (b) concurrent AI-session JSONL files, (c) browser visits during ai_session
      coding tasks.
- [x] **10.1.3** `compute_exclusive_time()`: sweep-line interval union. Reports exclusive
      (non-overlapping bandwidth), wall-span, active-total, overlap, and parallel-group count.
      Wired into the text report footer. 19 tests.
- [x] **10.1.4** Tests: background split, concurrent sessions, browser-during-coding,
      exclusive-time math (10:00-12:00 + 11:00-13:00 = 3h exclusive, not 4h).

### 10.2 Multi-resolution drill-down & root-cause analysis  [no new deps] ✅
- [x] **10.2.1** `drill_down.py`: `detect_stages()` runs PELT recursively within a task
      (penalty 2×n_features, lower than task-boundary 10×n_features) or heuristic fallback
      (cwd-shift, tool-cluster change, user correction, >10min gap).
- [x] **10.2.2** `detect_markers()`: error clusters (≥2 consecutive is_error), retry loops
      (same tool+input >1× in 5min), user corrections (EN+CN signals), time sinks
      (idle: high-wall/low-active; hard: top-quartile active).
- [x] **10.2.3** `--task <id> --drill` mode in run.py: stage-by-stage timeline with inline
      markers + narrative generation for >2h tasks. `_events_for_task()` reconstructs the
      event list (segment() doesn't attach it). 33 tests.
- [x] **10.2.4** Tests: retry loop, error cluster, user correction, time sink, narrative
      coherence, simple-task no-marker case.

### 10.3 Honest three-valued success attribution  [no new deps] ✅
- [x] **10.3.1** Success is now `"succeeded"` / `"failed"` / `"unknown"` (not bool|None).
      `unknown` EXCLUDED from the success-rate denominator. Report shows `success%` (over
      known) and `unknown%` separately. All-unknown categories render "n/a (all unknown)"
      instead of misleading "0%". Constants in segment_tasks.py.
- [x] **10.3.2** Per-type signals: AI-coding (TaskUpdate+errors), vcs (commit landed),
      research (follow-up artifact), email (reply sent), meeting/conversation (follow-up
      action). `refine_success()` post-pass upgrades unknown→succeeded using cross-task
      context (git commits, research→coding within 1h, meeting→action within 24h).
- [x] **10.3.3** 34 tests. Existing test_pipeline.py needed 0 assertion updates (no
      success-value assertions existed). Wired: run.py calls `refine_success()` after
      cross-source linking.

---

## Phase 11 — Human time sinks + content-driven analysis  [no new deps] ✅ DONE

Born from the user's feedback that the report output was "bordering on useless" — generic
pattern-bucket labels, no distinction between human and machine time, meetings with zero
human interaction dominating the top 5. Four commits across an iterative cycle:

### 11.1 Content-driven root-cause narratives  [no new deps] ✅
- [x] **11.1.1** `summarize.py`: reads the ACTUAL event text (user prompts, assistant
      diagnostic messages, error texts, browser titles, meeting subjects) and produces
      grounded narratives. Replaces generic labels like "blocker: command timeout (21 of
      46 errors)" with "Goal: sync local main with remote. The fetch failed with a 407
      proxy auth error. Key failure: 'git fetch origin' → CONNECT tunnel failed, response
      407."
- [x] **11.1.2** `_pair_errors_with_commands()`: matches `tool_use_id` to pair each error
      with the exact command that caused it. `_explain_difficulty()` synthesizes WHY the
      problem was hard: "command timeouts + user rejecting tool uses kept recurring despite
      99 retries — the root cause was not addressed by the attempted fixes."
- [x] **11.1.3** Per-source_kind narratives: ai_session (goal+struggle+difficulty+time),
      browser (visited pages+downloads+idle tabs), meeting (subject+organizer+location+
      multi-day cap), comm (email+IM), vcs (commits), filesystem (files).
- [x] **11.1.4** `_clean_user_goal()`: strips conversational prefixes ("what do you mean by
      install X" → "Install X") and system-reminder wrappers. `_clean_subject_text()` in
      segment_tasks.py applies the same cleaning to task subjects.
- [x] **11.1.5** 40 tests in `test_summarize.py`.

### 11.2 Human-involvement detection  [no new deps] ✅
- [x] **11.2.1** `human_involvement.py`: identifies HUMAN actions (user messages, interrupts,
      rejections, browser revisits, emails sent, IM messages, commits, filesystem events)
      and computes `human_engaged_seconds` — time between consecutive human actions where
      gaps ≤30min (human stepped away for longer gaps).
- [x] **11.2.2** `machine_autonomous_seconds`: active time NOT attributable to human
      engagement. `human_involvement` level: high (50+ actions), moderate (10+), low (<10),
      none (0 — e.g. meeting from calendar data alone, idle browser tabs).
- [x] **11.2.3** Time sinks RE-RANKED BY HUMAN ENGAGED TIME, not raw active time. Meetings
      with 0 human interaction are gone from the top 5. Autonomous agent runs flagged as
      "LOW human involvement — mostly autonomous agent work."
- [x] **11.2.4** `compute_actual_working_hours()`: derives the working-hour denominator
      from real human activity instead of assuming flat 8h/day.
- [x] **11.2.5** 26 tests in `test_human_involvement.py`.

### 11.3 Three-way time accounting + structured root cause  [no new deps] ✅
- [x] **11.3.1** Three-way time: Wall (total clock span) → Active (work detected) → Human
      (user engaged). Summary header shows all three with percentages: "Wall: 15501.8h |
      Active: 712.5h (5% of wall) | Human: 291.4h (41% of active, 2% of wall)".
- [x] **11.3.2** Top tasks table: columns for Human, %W, Active, %W, Wall, Involvement —
      showing all three time types per task with percentages relative to Wall.
- [x] **11.3.3** `render_structured_root_cause()`: breaks the narrative into labeled HTML
      blocks (🎯 Goal / ⚠️ Struggle / 🔥 Difficulty / ⏱️ Time) with color coding, instead
      of a single lump of text.
- [x] **11.3.4** Per-kind breakdown: "0.3h human / 379.4h active" per task, with structured
      root cause under each item.

### 11.4 WeLink IM enabled + multi-horizon + working-day %  [no new deps] ✅
- [x] **11.4.1** `enable_im=True` in `default_registry()` — IM collection now runs by
      default. 790 messages collected; IM conversations appear as comm tasks in the report.
      `is_human_action()` recognizes `chat_message` events; `_summarize_comm` includes IM
      summary ("237 IM message(s) in <conversation>. 5 participant(s). 5.9h of messaging.").
- [x] **11.4.2** Multi-horizon analysis (carried from earlier session): default
      `python run.py` generates 4 HTML reports (90d/30d/7d/1d) + dashboard index page.
      `--horizons` flag for custom ranges. Data-availability section per source.
- [x] **11.4.3** Working-day percentages: `_as_working_days()` and `_working_day_pct()`
      throughout the UI. Summary header: "Working-day basis: 291h actual" (from human
      activity, not flat 8h/day).

---

## Phase 12 — Genuine interaction detection & content investigation  [no new deps] ✅ DONE

Born from rubrics 54-60: the skill must distinguish genuine human interaction from
forgotten/abandoned sessions, and investigate the actual content of coding sessions,
browser pages, WeLink chats, and file edits to explain WHY they took time.

### 12.1 Idle session detection foundation  [no new deps] ✅
- [x] **12.1.1** `human_involvement.py`: added `is_genuine_time_sink` field — True when
      `human_action_count >= 5` AND `human_engaged_seconds > 300` (5+ actions, 5+ min engaged).
      Tasks that don't meet this threshold are flagged as "被遗忘/非活跃使用".
- [x] **12.1.2** `aggregate.py render_html()`: top 10 filtered to genuine time sinks only.
      Low-engagement tasks listed in a separate "低参与度任务" section.

### 12.2 Coding session content investigation (rubric 56) ✅
- [x] **12.2.1** Idle coding session detection: if `human_engaged_seconds < 0.1 * active_seconds`
      (user engaged < 10% of active time), narrative says "agent自主运行，人工参与度低".
- [x] **12.2.2** Content investigation: extract top 3 user prompts (not just the first)
      as `user_prompts` in context, shown in the narrative as evidence.
- [x] **12.2.3** Specific error evidence: when errors exist, show the actual error text
      (not just pattern classification) as verifiable evidence.

### 12.3 Browser content analysis (rubric 54) ✅
- [x] **12.3.1** Topic inference from page titles: categorize pages (CodeHub=代码仓库,
      稼先社区=内部知识搜索, Google Gemini=AI工具, 3MS搜索=文档搜索, etc.)
- [x] **12.3.2** For top-interacted pages, explain WHY based on inferred topic:
      "「AgentCenter」是华为内部AI Agent开发平台，表明用户在密集配置或调试Agent".
- [x] **12.3.3** Evidence references: cite visit count + Chrome visit_count as verifiable
      evidence.

### 12.4 WeLink chat content summarization (rubric 58) ✅
- [x] **12.4.1** Topic synthesis from message texts: extract keywords, summarize as
      1-sentence description ("讨论涉及学位证明报销流程").
- [x] **12.4.2** Explain WHY it took long: "需要与5位参与者确认，消息往返228条".
- [x] **12.4.3** Forgotten chat detection: low human engagement → "非活跃使用".

### 12.5 File editing content investigation (rubric 60) ✅
- [x] **12.5.1** Genuine editing detection: file appearing in multiple events with different
      timestamps = genuine editing (VSCode Local History saves versions).
- [x] **12.5.2** File type inference: .py=Python, .md=文档, .pptx=演示文稿, .xlsx=表格.
- [x] **12.5.3** Edit version count: more versions = more editing, shown in narrative.
- [x] **12.5.4** Explain WHY: "频繁编辑 rubrics.md（4个版本），表明用户在反复修改评估标准".



- **No live tracking.** Ever. Retrospective-only is a hard requirement.
- **No manager-analyzing-team deployment.** Opt-in self-analysis only.
- **No closed-source/paywalled dependencies.** All optional libs are OSS. (pm4py is AGPL v3
  — noted; JSONL fallback exists if copyleft is a concern.) libpff is OSS — the mail backup
  prefers it over Graph API (which needs admin consent).
- **No pretending IM exists without welink-cli.** Verified: no local WeLink message store.
  The skill says so plainly rather than silently dropping the category.
- **No CloudDevOps Wiki / W3 until access paths are verified.** They stay as `[unverified]`
  in the catalog rather than being committed to prematurely.
