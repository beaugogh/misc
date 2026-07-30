# huawei-retro-scope scripts

Retrospective task & time reconstruction from multiple activity-trace sources.
Reads historical records (no live tracking), fuses them into tasks with
boundaries/duration/effort/input/output/success, and aggregates by day/week/month.

## Quick Start

```bash
# Check which sources are available on your machine:
python run.py --check

# Weekly time report (default):
python run.py --granularity week

# Daily report, JSON output:
python run.py --granularity day --json

# Filter by date range:
python run.py --granularity week --since 2026-07-01 --until 2026-07-31

# Task drill-down (full detail: inputs, outputs, success, effort):
python run.py --task explicit-1

# Stage-by-stage drill-down with root-cause markers + narrative:
python run.py --task explicit-1 --drill

# Find your biggest time sinks (bridges aggregation -> drill-down):
python run.py --top 10 --since 2026-07-01 --until 2026-07-31
# then drill into any of them:
python run.py --task <id-from-above> --drill

# Output formats: text (default), table, markdown, html, json:
python run.py --granularity week --format markdown
python run.py --granularity week --format html --output report.html

# Evaluate segmentation quality against labeled benchmark:
python run.py --eval

# Persist tasks to output/tasks.jsonl + write watermark for incremental next run:
python run.py --granularity week --persist

# Force full reparse (ignore watermark):
python run.py --granularity week --rebuild

# Show which sources were found/used/skipped:
python run.py --sources
```

## Optional dependencies

The core pipeline runs on Python stdlib only. For advanced features:

```bash
pip install -r scripts/requirements.txt
```

This enables: PELT boundary detection (ruptures), GMM gap threshold (scikit-learn),
Leiden cross-source identity (igraph), OCEL 2.0 storage (pm4py), RIPPER categorization
rules (wittgenstein), PROV-O provenance (prov).

## Sources (auto-detected)

| Source | Kind | Status |
|--------|------|--------|
| Claude Code | ai_session | verified |
| Codeagent (new) | ai_session | verified |
| Codeagent (legacy, nga) | ai_session | verified (SQLite) |
| Git / CodeHub | vcs | verified (commits + reflog) |
| Chrome history | browser | verified (visits, downloads, searches) |
| Edge history | browser | verified |
| VSCode Local History | filesystem | verified (per-file edit timestamps) |
| welink-cli (meetings/calendar/mail/IM) | meeting/comm | verified (live-verified 2026-07-30) |
| iCalendar (.ics) | meeting | user-exported calendar (backup for welink-cli calendar; auto-discovery + RRULE/TZID) |
| WeLink Meeting recordings | meeting | verified (backup for welink-cli meetings; ffprobe duration extraction built) |
| Outlook OST (COM/MAPI) | comm | verified-COM (backup for welink-cli mail; 123 emails live) |
| Windows Recent | filesystem | verified (.lnk shortcuts) |
| Jump Lists | filesystem | verified (.automaticDestinations-ms, app+doc pairs) |
| 3ms | doc_authoring | detector-only (plugin gated) |

Codex, openclaw, hermes-agent, CloudDevOps Wiki, W3: detectors added in Phase 6.10 — they
surface "found unrecognized" rather than silently ignoring. Schemas filled in as colleagues
provide them.

### welink-cli (optional, preferred for communication data)

welink-cli is an npm CLI that exposes four data domains: meetings (duration), calendar,
mail, and IM chat history. It is **optional** — the skill works without it via backup
routes (3 of 4 domains; IM has no backup). See SKILL.md "Installing welink-cli" and
"Data sources without welink-cli" for full details.

```bash
npm install -g @welink/welink-cli \
  --registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ \
  --strict-ssl=false \
  --ignore-scripts
```

Two Windows gotchas: (1) set `NO_PROXY="cmc.centralrepo.rnd.huawei.com"` or npm hangs on
the intranet registry; (2) `--ignore-scripts` skips a broken postinstall PowerShell
snippet — the `.CMD` shim still lands on PATH. After install: `welink-cli auth login`
(scan-to-login), then `welink-cli mail autodiscover --email <you>@huawei.com` (one-time,
enables calendar/mail subcommands).

## Pipeline architecture

```
sources (auto-detected)
    |
    v  [SourceAdapter.detect/collect]  — registry runs all detected adapters
normalized events
    |
    v  [segment_tasks.segment]         — explicit (TaskCreate) + implicit (PELT/GMM) tasks
task objects (with boundaries, duration, effort, I/O, three-valued success)
    |
    v  [cross_source + entity_resolution] — link git commits + Leiden clustering
    |
    v  [segment_tasks.refine_success]  — upgrade unknown→succeeded via cross-task context
    |
    v  [parallel_tasks.detect_parallel_tasks] — split foreground/background, assign thread_id
    v  [parallel_tasks.compute_exclusive_time] — sweep-line interval union
    |
    v  [categorize.classify_task_advanced] — domain detection from file paths
    |
    v  [aggregate.aggregate]           — by day/week/month/year x kind
    |
    v  [run.py]                        — text/table/markdown/html/JSON report
                                      — --task <id> --drill: stage-by-stage drill-down
```

## Files

- `run.py` — single CLI entrypoint (collect → segment → link → aggregate → report)
- `sources.py` — SourceAdapter protocol + SourceRegistry + default_registry()
- `claude_code_adapter.py` — Claude Code + Codeagent JSONL adapter
- `welink_cli_adapter.py` — welink-cli adapter (meetings, calendar, mail, IM)
- `legacy_codeagent_adapter.py` — legacy codeagent SQLite (ngagent.db) adapter
- `outlook_adapter.py` — Outlook OST adapter via COM/MAPI (pywin32)
- `git_adapter.py` — git log + reflog adapter
- `browser_adapter.py` — Chrome/Edge history adapter
- `more_adapters.py` — VSCode History, iCalendar, Windows Recent, WeLink recordings, 3ms, Jump Lists
- `segment_tasks.py` — explicit + implicit task segmentation + three-valued success + refine_success
- `advanced_segment.py` — PELT (ruptures) + GMM (sklearn) boundary detection
- `parallel_tasks.py` — parallel-task detection + exclusive-time computation (Phase 10.1)
- `drill_down.py` — multi-resolution drill-down: stages, markers, narrative (Phase 10.2)
- `eval_segmentation.py` — evaluation harness: WindowDiff + Collar-Based F1 (Phase 9.8)
- `cross_source.py` — naive cross-source linker (Phase 1.4 scaffolding)
- `entity_resolution.py` — Leiden graph clustering for cross-source identity (Phase 4.4)
- `aggregate.py` — aggregation + report rendering + task drill-down
- `categorize.py` — domain detection + PPMI clustering + RIPPER rules (Phase 7)
- `persistence.py` — JSONL task log + watermark (Phase 2)
- `ocel_store.py` — OCEL 2.0 storage via pm4py (Phase 5)
- `platform_paths.py` — per-OS path abstraction (Phase 8)
- `tests/` — 272 tests across multiple test modules
- `requirements.txt` — optional deps for advanced features

## Platform support

- **Windows**: all sources verified.
- **Mac**: paths in platform_paths.py; Claude Code, codeagent, Chrome, Edge, VSCode,
  Outlook Mac paths included.
- **Linux**: Chrome, Edge, VSCode paths included.

## What this does NOT do

- No live tracking (retrospective only — a hard requirement).
- No manager-analyzing-team deployment (opt-in self-analysis only).
- No closed-source/paywalled dependencies.
