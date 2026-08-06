#!/usr/bin/env python3
"""retro-scope — single CLI entrypoint for the full pipeline.

Runs: collect (via registry) → segment → aggregate → report.

Usage:
    python run.py                         # multi-horizon: 90d, 30d, 7d, 1d (default)
    python run.py --horizons 90d,30d,7d   # custom horizons
    python run.py --granularity week      # single-range (legacy mode)
    python run.py --granularity day --json
    python run.py --granularity month --since 2026-07-01 --until 2026-07-31
    python run.py --granularity week --format table
    python run.py --granularity week --format markdown --output report.md
    python run.py --granularity week --output report.html   # format inferred from .html
    python run.py --sources          # list detected + skipped sources
    python run.py --check            # verify environment + adapters, no analysis
    python run.py --provision        # auto-provision welink-cli + git identity
    python run.py --top 10           # biggest time sinks by active time (prints task IDs for --drill)
    python run.py --task <id> --drill  # root-cause drill-down on one task (Phase 10.2)

Flags:
    --horizons 90d,30d,7d,1d              multi-horizon mode (DEFAULT): generate one
                                          HTML report per horizon ending at --until (or now).
                                          Each report includes a data-availability section
                                          showing per-source coverage. Sources with no data
                                          in a horizon are listed as "No data in range".
    --output-dir <dir>                    directory for multi-horizon reports (default: ../../output/ i.e. huawei-auto-pal/output/)
    --granularity {day,week,month,year}   aggregation period (single-range mode; default: week)
    --format {text,table,markdown,html,json}  output format (single-range; default: text)
    --json                                emit raw JSON (equivalent to --format json; takes precedence)
    --output <path>                       write report to file instead of stdout (single-range)
    --since YYYY-MM-DD                    single-range mode: only tasks starting on/after this date
    --until YYYY-MM-DD                    end date for both modes (default: today).
                                          In multi-horizon: horizons end at this date.
                                          In single-range: only tasks starting on/before this date.
    --sources                             report which sources were found/used/skipped, then exit
    --check                               environment + adapter check, then exit
    --provision                           auto-provision welink-cli (install + auth login) and git identity
    --rebuild                             ignore any watermark, do full reparse (Phase 2 placeholder)
    --eval                                run segmentation evaluation against the labeled benchmark (Phase 9.8)
    --task <id>                           show full detail for a single task
    --drill                               with --task: stage-by-stage root-cause analysis (Phase 10.2)
    --top N                               list the top N tasks by active time (prints task IDs for --drill)
"""

from __future__ import annotations

import sys
import os
import json
import re
import argparse
import time
import tempfile
import subprocess
from bisect import bisect_left, bisect_right
from datetime import datetime, timezone

# Windows console defaults to the system codepage (e.g. cp936/GBK on Chinese
# Windows), which cannot encode the em-dashes, arrows, and CJK characters that
# appear in reports and drill-down output — causing UnicodeEncodeError on print.
# Reconfigure stdout/stderr to UTF-8 so the skill just works on Windows without
# requiring PYTHONUTF8=1. errors="replace" is a last-resort safety net so a
# stray character never crashes the run.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass  # stream doesn't support reconfigure (e.g. redirected/closed) — leave as-is

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Short hints shown by `--check` when an adapter is not detected, so a new user
# knows what they lose and where to look for setup guidance.  Keep one line each.
_ADAPTER_HINTS = {
    "claude_code": "AI sessions — works with zero setup if Claude Code is installed",
    "codeagent": "AI sessions — works with zero setup if Codeagent is installed",
    "git": "commits — ensure git is on PATH and 'git config user.email' is set; see README.md",
    "chrome": "browser history — works with zero setup if Chrome is installed",
    "edge": "browser history — works with zero setup if Edge is installed",
    "vscode_history": "file edits — works with zero setup if VS Code is used",
    "icalendar": "calendar — set RETRO_SCOPE_ICS_PATHS to .ics file path(s); see README.md",
    "windows_recent": "recent files — works with zero setup on Windows",
    "jump_list": "app/doc history — works with zero setup on Windows",
    "welink_recordings": "meeting recordings — uses default Windows folder; set WELINK_RECORDINGS_DIR to override; see README.md",
    "welink_cli": "WeLink meetings/chat/mail/calendar — install welink-cli and run 'welink-cli auth login'; see README.md §welink-cli",
    "legacy_codeagent": "legacy Codeagent sessions — works with zero setup if nga.db exists",
    "outlook": "email/calendar via Outlook — requires pywin32 + Outlook; see README.md",
    "codex": "Codex AI sessions — works with zero setup if Codex is installed",
    "openclaw": "OpenClaw AI sessions — works with zero setup if OpenClaw is installed",
    "hermes_agent": "Hermes AI sessions — works with zero setup if Hermes is installed",
    "clouddevops_wiki": "CloudDevOps Wiki — requires OpenCLI plugin; see README.md §optional-tools",
    "w3": "W3 portal — requires OpenCLI plugin; see README.md §optional-tools",
}

from sources import default_registry
from segment_tasks import segment
from aggregate import aggregate, render_report, render_markdown, render_table, render_html


def render_check_output(adapters, hints=None):
    """Render the --check status report as a string.

    Pure function: takes an iterable of adapter objects (each with .name,
    .detect(), optional .detector_only, and optional .auth_status()) and an
    optional hints dict. Does NOT call collect() on any adapter. Used by
    --check and by tests.
    """
    if hints is None:
        hints = _ADAPTER_HINTS
    lines = [
        "# retro-scope environment check",
        "# READY = detected and collection implemented",
        "# NOT AUTHENTICATED = detected but needs auth/config to produce events",
        "# DETECTOR-ONLY = tool detected, but collect() yields no events yet",
        "# NOT DETECTED = collection exists but source is absent; see README.md",
        "",
    ]
    for adapter in adapters:
        is_detector_only = getattr(adapter, "detector_only", False)
        hint = hints.get(adapter.name, "")
        try:
            ok = adapter.detect()
        except Exception as e:
            lines.append(f"  {adapter.name:20s} ERROR: {e}")
            continue
        if not ok:
            status = "NOT DETECTED"
            line = f"  {adapter.name:20s} {status}"
            if hint:
                line += f"  ({hint})"
        elif is_detector_only:
            status = "DETECTOR-ONLY"
            line = f"  {adapter.name:20s} {status}"
            if hint:
                line += f"  ({hint})"
        else:
            # Detected and not detector-only — probe auth status.
            auth_fn = getattr(adapter, "auth_status", None)
            if auth_fn is not None:
                try:
                    result = auth_fn()
                except Exception:
                    result = None  # auth probe failed — treat as READY, don't block
            else:
                result = None
            if result is not None and result[0] != "ok":
                status = "NOT AUTHENTICATED"
                auth_hint = result[1] if result[1] else hint
                line = f"  {adapter.name:20s} {status}"
                if auth_hint:
                    line += f"  ({auth_hint})"
            else:
                status = "READY"
                line = f"  {adapter.name:20s} {status}"
        lines.append(line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# --provision: auto-provision welink-cli and git identity
# ---------------------------------------------------------------------------

# Approved Huawei intranet npm registry for welink-cli.  --strict-ssl=false is
# permitted for this single command only when TLS interception blocks the
# approved intranet registry; never persist it or use it for public hosts.
_WELINK_NPM_REGISTRY = (
    "https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/"
)
_WELINK_NPM_PACKAGE = "@welink/welink-cli"


def _run_command(cmd: list[str], env: dict | None = None,
                 timeout: int = 120, dry_run: bool = False) -> tuple[int, str, str]:
    """Run a command, return (returncode, stdout, stderr).

    In dry-run mode, print the command and return (0, "", "") without executing.
    """
    import shlex
    label = " ".join(shlex.quote(c) for c in cmd)
    if env:
        env_labels = [f"{k}={v}" for k, v in env.items()
                      if k not in ("PATH", "PATHEXT", "SYSTEMROOT", "TEMP", "TMP",
                                   "APPDATA", "LOCALAPPDATA", "USERPROFILE",
                                   "HOMEDRIVE", "HOMEPATH", "OS", "COMPUTERNAME",
                                   "USERNAME", "USERDOMAIN", "PROCESSOR_ARCHITECTURE")]
        if env_labels:
            label = " ".join(env_labels) + " " + label
    if dry_run:
        print(f"  [dry-run] {label}")
        return (0, "", "")
    print(f"  $ {label}")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env or os.environ.copy(),
    )
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.stderr.strip():
        print(result.stderr.rstrip(), file=sys.stderr)
    return (result.returncode, result.stdout, result.stderr)


def _run_interactive(cmd: list[str], timeout: int = 120,
                     dry_run: bool = False) -> int:
    """Run an interactive command with stdout/stderr inherited from the terminal.

    Unlike _run_command, this does NOT capture output — the user sees QR codes
    and prompts in real-time. Used for 'welink-cli auth login'.
    Returns the exit code (0 = success). On timeout, prints a message and returns 1.
    """
    import shlex
    label = " ".join(shlex.quote(c) for c in cmd)
    if dry_run:
        print(f"  [dry-run] {label}")
        return 0
    print(f"  $ {label}")
    try:
        result = subprocess.run(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"  ERROR: command timed out after {timeout}s.", file=sys.stderr)
        return 1
    return result.returncode


def _provision_welink_cli(dry_run: bool = False) -> bool:
    """Install welink-cli if missing, then run auth login.

    Returns True if welink-cli is installed and authenticated after provisioning.
    """
    import shutil as _shutil

    # Step 1: check Node.js
    node = _shutil.which("node")
    if not node:
        print("  ERROR: Node.js not found on PATH. Install Node.js >= 18 first:")
        print("    https://nodejs.org/ (or your corporate package manager)")
        return False
    # Verify version >= 18
    rc, out, _ = _run_command([node, "--version"], timeout=10, dry_run=False)
    if rc != 0:
        print("  ERROR: 'node --version' failed.")
        return False
    version_str = out.strip().lstrip("v")
    try:
        major = int(version_str.split(".")[0])
    except (ValueError, IndexError):
        print(f"  ERROR: cannot parse Node.js version '{version_str}'.")
        return False
    if major < 18:
        print(f"  ERROR: Node.js {version_str} is too old. welink-cli requires >= 18.")
        return False
    print(f"  Node.js v{version_str} — OK")

    # Step 2: install welink-cli if not in PATH
    if _shutil.which("welink-cli"):
        print("  welink-cli already installed.")
    else:
        print("  Installing welink-cli from Huawei intranet registry...")
        env = os.environ.copy()
        # Intranet registry must bypass the corporate proxy.
        env["NO_PROXY"] = "cmc.centralrepo.rnd.huawei.com"
        cmd = [
            "npm", "install", "-g", _WELINK_NPM_PACKAGE,
            "--strict-ssl=false",
            f"--@welink:registry={_WELINK_NPM_REGISTRY}",
        ]
        rc, _, _ = _run_command(cmd, env=env, timeout=180, dry_run=dry_run)
        if rc != 0:
            print("  ERROR: welink-cli installation failed.")
            return False
        if not dry_run:
            # Verify install
            if not _shutil.which("welink-cli"):
                print("  ERROR: welink-cli installed but not found on PATH.")
                print("    You may need to restart your terminal or add the npm global bin to PATH.")
                return False
        print("  welink-cli installed.")

    # Step 3: check auth status
    from welink_cli_adapter import WeLinkCLIAdapter
    adapter = WeLinkCLIAdapter()
    status = adapter.auth_status()
    if status is None or status[0] == "ok":
        print("  welink-cli authenticated — OK")
        return True

    # Step 4: run auth login (interactive — QR code or WeLink PC client)
    # Use _run_interactive (not _run_command) so the QR code is visible in
    # real-time. capture_output=True would buffer it until timeout.
    print("  Starting welink-cli auth login...")
    print("  (Scan the QR code in your terminal, or approve in WeLink PC client.)")
    rc = _run_interactive(["welink-cli", "auth", "login"], timeout=120, dry_run=dry_run)
    if rc != 0:
        print("  ERROR: 'welink-cli auth login' failed.")
        return False

    # Step 5: re-check auth
    if dry_run:
        print("  [dry-run] would re-check auth status")
        return True
    status = adapter.auth_status()
    if status is None or status[0] == "ok":
        print("  welink-cli authenticated — OK")
        return True
    print(f"  ERROR: welink-cli auth still not ready: {status[1]}")
    return False


def _provision_git(email: str | None, name: str | None,
                   dry_run: bool = False) -> bool:
    """Set git user.email and user.name globally if not configured.

    Returns True if git identity is configured after provisioning.
    """
    import shutil as _shutil

    if not _shutil.which("git"):
        print("  ERROR: git not found on PATH. Install git first:")
        print("    https://git-scm.com/ (or your corporate package manager)")
        return False

    # Check current global email
    rc, current_email, _ = _run_command(
        ["git", "config", "--global", "user.email"], timeout=10, dry_run=False)
    current_email = current_email.strip()
    effective_email = current_email if (rc == 0 and current_email) else email
    if rc == 0 and current_email:
        print(f"  git user.email already set: {current_email}")
    else:
        if not email:
            print("  ERROR: git user.email is not set and no --git-email was provided.")
            print("    The agent should ask the user for their email and pass it via --git-email.")
            return False
        rc, _, _ = _run_command(
            ["git", "config", "--global", "user.email", email], timeout=10, dry_run=dry_run)
        if rc != 0:
            print(f"  ERROR: failed to set git user.email to '{email}'.")
            return False
        print(f"  git user.email set to: {email}")

    # Check current global name
    rc, current_name, _ = _run_command(
        ["git", "config", "--global", "user.name"], timeout=10, dry_run=False)
    current_name = current_name.strip()
    if rc == 0 and current_name:
        print(f"  git user.name already set: {current_name}")
    elif name:
        rc, _, _ = _run_command(
            ["git", "config", "--global", "user.name", name], timeout=10, dry_run=dry_run)
        if rc != 0:
            print(f"  ERROR: failed to set git user.name to '{name}'.")
            return False
        print(f"  git user.name set to: {name}")
    else:
        # Derive name from email if possible (e.g. "bo.gao@huawei.com" → "Bo Gao")
        if effective_email and "@" in effective_email:
            local = effective_email.split("@")[0]
            if "." in local:
                derived = " ".join(part.capitalize() for part in local.split("."))
            else:
                derived = local
            rc, _, _ = _run_command(
                ["git", "config", "--global", "user.name", derived], timeout=10, dry_run=dry_run)
            if rc == 0:
                print(f"  git user.name set to: {derived} (derived from email)")
            else:
                print(f"  WARNING: could not set git user.name. Set it manually if needed.")
        else:
            print("  NOTE: git user.name not set. Set it manually if needed: "
                  "'git config --global user.name <Your Name>'")

    return True


def cmd_provision(git_email: str | None = None,
                  git_name: str | None = None,
                  only: str | None = None,
                  dry_run: bool = False) -> int:
    """Auto-provision welink-cli and git identity.

    Called by --provision. Prints progress to stdout. Returns exit code
    (0 = success, 1 = any failure).
    """
    print("# huawei-auto-pal — auto-provisioning")
    print("# This installs welink-cli (from the approved Huawei intranet registry)")
    print("# and configures git identity (user.email / user.name).")
    if dry_run:
        print("# [DRY RUN] — commands will be printed but not executed.")
    print()

    success = True

    if only != "git":
        print("== welink-cli ==")
        if not _provision_welink_cli(dry_run=dry_run):
            success = False
        print()

    if only != "welink":
        print("== git identity ==")
        if not _provision_git(email=git_email, name=git_name, dry_run=dry_run):
            success = False
        print()

    # Re-run --check to show updated status
    print("== updated environment check ==")
    from sources import default_registry as _reg
    reg = _reg(session_cwds=[])
    print(render_check_output(reg._adapters))

    if success:
        print()
        print("# Provisioning complete. Re-run huawei-auto-pal to use the new sources.")
        return 0
    else:
        print()
        print("# Provisioning completed with errors. See messages above.")
        return 1


def _parse_date(s: str) -> float:
    """Parse YYYY-MM-DD to epoch seconds (UTC start of day)."""
    dt = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.timestamp()


def _remap_task_ids(tasks: list[dict]) -> list[dict]:
    """Assign stable task IDs that survive across incremental runs.

    C7 fix: segment_tasks.py generates IDs like ``explicit-N`` and ``implicit-N``
    where N is re-numbered from 1 on each run. In incremental mode this causes
    ID collisions — an unrelated task in run 2 gets the same ID as a task in run 1,
    silently overwriting it in ``save_tasks(mode='merge')``.

    New format: ``{flavor}-{session_id}-{start_timestamp}``.
    For tasks without a session_id: ``{flavor}-nosession-{start_timestamp}``.
    Tasks created by parallel_tasks.py (background, browser_research) and other
    flavors already have unique-ish IDs; we only remap explicit/implicit ones.
    """
    for t in tasks:
        flavor = t.get("flavor", "")
        if flavor in ("explicit", "implicit"):
            sid = t.get("session_id") or "nosession"
            start = int(t.get("start") or 0)
            t["id"] = f"{flavor}-{sid}-{start}"
    return tasks


def _filter_tasks_by_watermark(tasks: list[dict], watermark: float) -> list[dict]:
    """Keep only tasks that have at least one event with timestamp > watermark.

    C7 fix: in incremental mode, collect_since() now yields ALL events from sessions
    that have any post-watermark event. This means segment() may produce tasks that
    are entirely before the watermark (already processed in a prior run). Filter
    them out here so they aren't re-persisted or double-counted.
    """
    result = []
    for t in tasks:
        start = t.get("start") or 0
        end = t.get("end") or start
        # A task overlaps the post-watermark window if its end > watermark.
        # (start <= watermark is fine — the task spans the boundary.)
        if end > watermark:
            result.append(t)
    return result


def _resolve_proxy() -> str | None:
    """Resolve proxy URL for page enrichment.

    Precedence (same as webpage-to-markdown skill):
    1. HTTPS_PROXY / HTTP_PROXY env vars (and lowercase variants).
    2. git config --get http.proxy.
    3. npm config get proxy / https-proxy.

    Returns None if no proxy is configured.
    """
    import os as _os
    for var in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
        val = _os.environ.get(var)
        if val:
            return val
    # Git config.
    try:
        import subprocess as _sp
        r = _sp.run(["git", "config", "--get", "http.proxy"],
                     capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    # npm config.
    try:
        import subprocess as _sp
        for key in ("proxy", "https-proxy"):
            r = _sp.run(["npm", "config", "get", key],
                         capture_output=True, text=True, timeout=5)
            val = r.stdout.strip()
            if r.returncode == 0 and val and val.lower() not in ("null", "undefined", "false"):
                return val
    except Exception:
        pass
    return None


def _events_for_task(task: dict, all_events: list[dict]) -> list[dict]:
    """Reconstruct the events belonging to a task.

    segment() doesn't attach events to task dicts — it only stores aggregates.
    For drill-down we need the raw events. Match by session_id + time range;
    if no session_id, match by time range alone (less precise but workable).

    For zero-length background tasks (start == end, from parallel_tasks.py),
    widen the window to the session's max timestamp so we capture the full
    event stream. If the session max can't be determined, fall back to a
    4-hour window after start as a reasonable bound.
    """
    start = task.get("start") or 0
    end = task.get("end") or (task.get("wall_clock_seconds") and start + task["wall_clock_seconds"]) or start
    session_id = task.get("session_id")
    source = task.get("source")

    # C6 fix: zero-length background tasks (start == end) get a widened window.
    zero_length = end <= start
    if zero_length:
        if session_id:
            # Scan all_events for the max timestamp in the same session.
            session_max = start
            for e in all_events:
                if e.get("session_id") == session_id:
                    ts = e.get("timestamp") or 0
                    if ts > session_max:
                        session_max = ts
            end = session_max
        else:
            # No session_id — fall back to a 4-hour window.
            end = start + 4 * 3600

    result = []
    for e in all_events:
        ts = e.get("timestamp") or 0
        if ts < start or ts > end + 1:
            continue
        if session_id and e.get("session_id") and e["session_id"] != session_id:
            continue
        if source and e.get("source") and e["source"] != source:
            # Allow cross-source events (e.g. git commits linked to a coding task)
            # but prefer same-source. Keep all for now — drill_down can filter.
            pass
        result.append(e)
    return result


def _render_drill_down(result: dict, task: dict) -> str:
    """Render a stage-by-stage root-cause drill-down (Phase 10.2)."""
    from datetime import datetime as _dt
    from aggregate import render_context_text
    lines = []
    subj = task.get("subject") or "(no subject)"
    lines.append(f"# Drill-down: {subj}")
    lines.append("")
    act_h = (result.get("total_active_seconds") or 0) / 3600
    wall_h = (result.get("total_wall_seconds") or 0) / 3600
    from aggregate import _working_day_pct
    wd_pct = _working_day_pct(act_h)
    wd_str = f" ({wd_pct} of 8h)" if wd_pct else ""
    lines.append(f"Active: {act_h:.1f}h{wd_str} | Wall: {wall_h:.1f}h | "
                 f"Stages: {len(result.get('stages', []))}")
    lines.append("")

    # Lead-off: the key signals from task["context"], so the drill-down answers
    # "why did this take so long?" before the user reads the stage timeline.
    context_text = render_context_text(task)
    if context_text:
        lines.append("## Key signals")
        lines.append(context_text)
        lines.append("")

    # C6 fix: warn when the task has zero events or zero stages so that "no data"
    # is distinguishable from "no problems."
    event_count = len(task.get("events") or [])
    stage_count = len(result.get("stages") or [])
    if event_count == 0 or stage_count == 0:
        lines.append("WARNING: this task has unknown duration (zero-length background task).")
        lines.append("Event reconstruction may be incomplete — the analysis below is based on limited data.")
        lines.append("")

    # Narrative
    narrative = result.get("narrative")
    if narrative:
        lines.append(f"> {narrative}")
        lines.append("")

    # Stage-by-stage timeline
    markers = result.get("all_markers", [])
    lines.append("## Stages")
    lines.append(f"{'#':>2} {'Start':<17} {'Wall':>7} {'Active':>7} {'Events':>7}  "
                 f"{'Summary'}")
    lines.append("-" * 80)
    for stage in result.get("stages", []):
        idx = stage.get("stage_idx", 0)
        start_ts = stage.get("start", 0)
        start_str = _dt.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M") if start_ts else "?"
        wall = (stage.get("duration_seconds") or 0) / 60
        act = (stage.get("active_seconds") or 0) / 60
        ev = stage.get("event_count", 0)
        summary = stage.get("summary", "")[:50]
        lines.append(f"{idx:>2} {start_str:<17} {wall:>6.0f}m {act:>6.0f}m {ev:>7}  {summary}")
        # Inline markers for this stage
        for m in stage.get("markers", []):
            mtype = m.get("type", "")
            msg = m.get("message", "")
            lines.append(f"     ↳ [{mtype}] {msg}")

    # All markers summary
    if markers:
        lines.append("")
        lines.append(f"## Root-cause markers ({len(markers)} total)")
        for m in markers:
            lines.append(f"  - [{m.get('type')}] {m.get('message')}")

    return "\n".join(lines)


def _render_top_tasks(tasks: list[dict], n: int) -> str:
    """Render a ranked list of the top-N tasks by active time.

    This is the bridge between the aggregation layer (which kinds consumed the
    most time?) and the drill-down layer (what went wrong inside one task?).
    Each row gives the task ID so the user can immediately run
    ``--task <id> --drill`` on anything that looks like a time sink.
    """
    from datetime import datetime as _dt
    # Rank by HUMAN engaged time — the user's actual time cost, not machine time.
    def _human_engaged_h(t):
        return (t.get("human_data") or {}).get("human_engaged_seconds", 0) or 0
    ranked = sorted(tasks, key=_human_engaged_h, reverse=True)[:n]
    total_active = sum(t.get("active_seconds") or 0 for t in tasks) / 3600
    total_human = sum(_human_engaged_h(t) for t in tasks) / 3600

    lines = [f"# Top {len(ranked)} tasks by HUMAN engaged time"]
    from aggregate import _as_working_days, _working_day_pct, WORKING_DAY_HOURS
    wd_total = _as_working_days(total_human)
    total_str = f"{total_human:.1f}h human engaged"
    if wd_total:
        total_str += f" ({wd_total})"
    total_str += f" / {total_active:.1f}h total active"
    lines.append(f"(of {len(tasks)} tasks, {total_str})")
    lines.append("")
    lines.append(f"{'#':>3}  {'Human':>7}  {'%8h':>5}  {'Active':>7}  {'Involv':>7}  "
                 f"{'Kind':<11} {'Start':<12} {'Subject'}")
    lines.append("-" * 115)
    for i, t in enumerate(ranked, 1):
        eng = _human_engaged_h(t) / 3600
        act = (t.get("active_seconds") or 0) / 3600
        wd_pct = _working_day_pct(eng)
        hd = t.get("human_data") or {}
        inv = (hd.get("human_involvement") or "?")[:7]
        kind = (t.get("source_kind") or "?")[:11]
        start_str = _dt.fromtimestamp(t.get("start") or 0).strftime("%m-%d %H:%M")
        subj = (t.get("subject") or (t.get("text") or "")[:50] or "(no subject)")[:48]
        lines.append(f"{i:>3}  {eng:>6.1f}h  {wd_pct:>5}  {act:>6.1f}h  {inv:>7}  "
                     f"{kind:<11} {start_str:<12} {subj}")
        lines.append(f"       id: {t.get('id', '?')}")
    lines.append("")
    lines.append("Drill into any task:  python run.py --task <id> --drill")
    return "\n".join(lines)


def _export_session_records(tasks: list[dict], events: list[dict], output_dir: str) -> None:
    """Export detailed session records as evidence files (rubric 66).

    Writes a JSON file per task with: subject, time, human_data, narrative,
    user prompts (coding), message texts (chat), page titles (browser),
    commit subjects (git), file names (file-edit), and event timeline.

    Only exports tasks with is_genuine_time_sink=True (the ones that matter).
    Filenames are human-readable: source_kind_date_subject_taskid.json
    """
    import json as _json
    from datetime import datetime as _dt, timezone as _tz
    records_dir = os.path.join(output_dir, "session_records")
    os.makedirs(records_dir, exist_ok=True)
    try:
        os.chmod(records_dir, 0o700)
    except OSError:
        pass

    secret_patterns = (
        (re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|password|secret|cookie)\s*[:=]\s*)[^\s,;]+"), r"\1[REDACTED]"),
        (re.compile(r"(?i)(authorization\s*[:=]\s*(?:bearer\s+)?)[^\s,;]+"), r"\1[REDACTED]"),
        (re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"), "[REDACTED_JWT]"),
        (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "[REDACTED_EMAIL]"),
    )

    def _redact(value):
        if isinstance(value, str):
            for pattern, replacement in secret_patterns:
                value = pattern.sub(replacement, value)
            return value
        if isinstance(value, list):
            return [_redact(item) for item in value]
        if isinstance(value, dict):
            return {key: _redact(item) for key, item in value.items()}
        return value

    # Build a timestamp index once instead of rescanning every event per task.
    ordered_events = sorted(
        (e for e in events if isinstance(e.get("timestamp"), (int, float))),
        key=lambda e: e["timestamp"],
    )
    event_timestamps = [e["timestamp"] for e in ordered_events]

    def _events_for_task(t):
        start = t.get("start", 0)
        end = t.get("end", 0)
        sid = t.get("session_id")
        lo = bisect_left(event_timestamps, start)
        hi = bisect_right(event_timestamps, end)
        return [e for e in ordered_events[lo:hi]
                if e.get("session_id") == sid or not sid]

    exported = 0
    for t in tasks:
        hd = t.get("human_data") or {}
        if not hd.get("is_genuine_time_sink"):
            continue
        if (hd.get("human_engaged_seconds") or 0) < 600:  # < 10 min engaged
            continue

        tid = t.get("id", f"task-{exported}")
        # Filename: source_kind + date + full task_id (matches the report's
        # Task ID column so users can locate the source file directly).
        sk = t.get("source_kind", "unknown")
        start_dt = _dt.fromtimestamp(t.get("start") or 0, tz=_tz.utc)
        date_str = start_dt.strftime("%Y%m%d")
        safe_tid = re.sub(r'[^\w\-]', '_', tid)
        filename = f"{sk}_{date_str}_{safe_tid}.json"
        record = {
            "id": tid,
            "subject": t.get("subject"),
            "source_kind": t.get("source_kind"),
            "start": t.get("start"),
            "end": t.get("end"),
            "active_seconds": t.get("active_seconds"),
            "wall_clock_seconds": t.get("wall_clock_seconds"),
            "human_data": hd,
            "narrative": (t.get("context") or {}).get("narrative"),
            "context": {k: v for k, v in (t.get("context") or {}).items()
                        if k != "narrative"},
            "errors": t.get("errors"),
            "tool_calls": t.get("tool_calls"),
            "tool_names": t.get("tool_names"),
        }

        # Add event timeline (capped at 200 events).
        task_events = _events_for_task(t)
        timeline = []
        for ev in task_events[:200]:
            entry = {
                "timestamp": ev.get("timestamp"),
                "kind": ev.get("kind"),
                "text": (ev.get("text") or "")[:200],
                "tool_name": ev.get("tool_name"),
                "tool_is_error": ev.get("tool_is_error"),
            }
            # Enrich chat_message entries with comm-specific fields so the
            # timeline is self-describing: who sent it, in which conversation.
            if ev.get("kind") == "chat_message":
                ti = ev.get("tool_input") or {}
                entry["sender"] = ti.get("sender")
                entry["sender_name"] = ti.get("sender_name")
                entry["conversation_name"] = ti.get("conversation_name")
                entry["is_group"] = ti.get("is_group")
            timeline.append(entry)
        record["event_timeline"] = timeline
        record["event_count_total"] = len(task_events)
        record = _redact(record)

        filepath = os.path.join(records_dir, filename)
        fd, tmp_path = tempfile.mkstemp(prefix=".session-record-", dir=records_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                _json.dump(record, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            try:
                os.chmod(tmp_path, 0o600)
            except OSError:
                pass
            os.replace(tmp_path, filepath)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        exported += 1

    print(f"[session_records] exported {exported} genuine time sink records → {records_dir}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Multi-horizon mode
# ---------------------------------------------------------------------------

DEFAULT_HORIZONS = "90d,30d,7d,1d"


def _parse_horizon_spec(spec: str) -> list[tuple[int, str]]:
    """Parse a horizon spec like '90d,30d,7d,1d' into [(90, '90d'), (30, '30d'), ...].

    Each entry is (days, label). Validates the format; raises ValueError on bad input.
    """
    entries: list[tuple[int, str]] = []
    for part in spec.split(","):
        part = part.strip().lower()
        if not part:
            continue
        if not part.endswith("d") or not part[:-1].isdigit():
            raise ValueError(
                f"invalid horizon '{part}' — expected format like '90d' (number + 'd')"
            )
        days = int(part[:-1])
        if days < 1:
            raise ValueError(f"invalid horizon '{part}' — must be >= 1 day")
        entries.append((days, part))
    if not entries:
        raise ValueError("no horizons parsed from spec")
    return entries


def _granularity_for_horizon(days: int) -> str:
    """Pick an aggregation granularity appropriate for the horizon length.

    1-2 days → day, 3-30 days → week, 31+ days → month.
    """
    if days <= 2:
        return "day"
    if days <= 30:
        return "week"
    return "month"


def _run_multi_horizon(tasks: list[dict], events: list[dict],
                       horizons: list[tuple[int, str]],
                       end_ts: float, output_dir: str,
                       exclusive: dict | None, skipped: list[str]) -> str:
    """Generate one HTML report per horizon + a dashboard index page.

    Returns the path to the index page.
    """
    import html as html_mod
    from datetime import datetime as _dt, timezone as _tz
    from aggregate import aggregate, render_html, generate_insights

    os.makedirs(output_dir, exist_ok=True)
    end_date = _dt.fromtimestamp(end_ts, tz=_tz.utc)
    report_infos: list[dict] = []

    for days, label in horizons:
        since_ts = end_ts - days * 86400
        horizon_tasks = [t for t in tasks
                         if since_ts <= (t.get("start") or 0) <= end_ts]
        granularity = _granularity_for_horizon(days)
        agg = aggregate(horizon_tasks, granularity)

        since_date = _dt.fromtimestamp(since_ts, tz=_tz.utc).strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        filename = f"report_{label}.html"
        filepath = os.path.join(output_dir, filename)

        html_content = render_html(agg, granularity, tasks=horizon_tasks,
                                   since_ts=since_ts, until_ts=end_ts)

        # Recompute exclusive time for this horizon's task subset, so the
        # footer reflects the horizon, not the global total.
        if exclusive:
            try:
                from parallel_tasks import compute_exclusive_time
                horizon_exclusive = compute_exclusive_time(horizon_tasks)
                excl_h = horizon_exclusive["exclusive_seconds"] / 3600
                wall_h = horizon_exclusive["wall_span_seconds"] / 3600
                overlap_h = horizon_exclusive["overlap_seconds"] / 3600
                footer = (f"<p>exclusive time: {excl_h:.1f}h "
                          f"(wall span {wall_h:.1f}h, overlap {overlap_h:.1f}h, "
                          f"{horizon_exclusive['n_parallel_groups']} parallel group(s))</p>")
                if "</body>" in html_content:
                    html_content = html_content.replace("</body>", f"{footer}\n</body>")
                else:
                    html_content += footer
            except Exception:
                pass  # exclusive time is optional — don't fail the report

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
            if not html_content.endswith("\n"):
                f.write("\n")

        # Collect summary stats for the index page.
        total_active = sum(r.get("active_seconds", 0.0) for r in agg.values()) / 3600
        total_tasks = sum(r["task_count"] for r in agg.values())
        n_sources = len({t.get("source_kind") for t in horizon_tasks
                         if t.get("source_kind")})
        insights = generate_insights(horizon_tasks, agg)
        from aggregate import _as_working_days
        wd_str = _as_working_days(total_active)
        report_infos.append({
            "label": label, "days": days, "filename": filename,
            "since": since_date, "until": end_date_str,
            "active_h": total_active, "wd": wd_str,
            "task_count": total_tasks,
            "n_sources": n_sources,
            "top_insight": insights[0] if insights else "",
        })
        wd_display = f" ({wd_str})" if wd_str else ""
        print(f"  {label}: {total_active:.1f}h active{wd_display}, {total_tasks} tasks, "
              f"{n_sources} sources → {filepath}", file=sys.stderr)

    # Build the dashboard index page.
    index_path = os.path.join(output_dir, "index.html")
    cards = []
    for info in report_infos:
        label_esc = html_mod.escape(info["label"])
        since_esc = html_mod.escape(info["since"])
        until_esc = html_mod.escape(info["until"])
        insight_esc = html_mod.escape(info["top_insight"][:120])
        insight_html = (f'<p class="card-insight">{insight_esc}</p>'
                        if insight_esc else "")
        wd_html = ""
        if info.get("wd"):
            wd_html = f' <span class="card-wd">{html_mod.escape(info["wd"])}</span>'
        cards.append(
            f'  <a class="horizon-card" href="{html_mod.escape(info["filename"])}">'
            f'<div class="card-label">{label_esc}</div>'
            f'<div class="card-range">{since_esc} → {until_esc}</div>'
            f'<div class="card-stats"><strong>{info["active_h"]:.1f}h</strong> active{wd_html}, '
            f'{info["task_count"]} tasks, {info["n_sources"]} sources</div>'
            f'{insight_html}'
            f'</a>'
        )
    cards_html = "\n".join(cards)

    skipped_html = ""
    if skipped:
        # skipped is a list of dicts: {"name": ..., "reason": ...}
        skip_names = [s["name"] if isinstance(s, dict) else str(s) for s in skipped]
        skipped_html = (f'<p class="hint">Skipped sources: '
                        f'{html_mod.escape(", ".join(skip_names))}</p>')

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>retro-scope — multi-horizon dashboard</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; margin: 2em; color: #2c2c2c; max-width: 1000px; }}
  h1 {{ font-size: 1.6em; border-bottom: 3px solid #4e79a7; padding-bottom: 0.3em; }}
  .hint {{ font-size: 0.85em; color: #777; margin: 0.3em 0; }}
  .horizon-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin: 1.5em 0; }}
  .horizon-card {{ display: block; text-decoration: none; color: inherit; background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px 20px; transition: box-shadow 0.2s; }}
  .horizon-card:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.12); border-color: #4e79a7; }}
  .card-label {{ font-size: 1.4em; font-weight: 700; color: #4e79a7; }}
  .card-range {{ font-size: 0.85em; color: #888; margin: 0.2em 0; }}
  .card-stats {{ font-size: 0.95em; margin: 0.3em 0; }}
  .card-wd {{ font-size: 0.85em; color: #888; }}
  .card-insight {{ font-size: 0.82em; color: #555; margin-top: 0.5em; padding-top: 0.5em; border-top: 1px solid #eee; }}
</style>
</head>
<body>
<h1>Time analysis — multi-horizon</h1>
<p>Generated {_dt.fromtimestamp(end_ts, tz=_tz.utc).strftime("%Y-%m-%d %H:%M UTC")}.
Click any horizon for the full report.</p>
{skipped_html}
<div class="horizon-grid">
{cards_html}
</div>
</body>
</html>"""
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"\nDashboard: {index_path}", file=sys.stderr)
    return index_path


def main():
    ap = argparse.ArgumentParser(
        prog="run.py",
        description="retro-scope: retrospective task & time reconstruction.",
    )
    ap.add_argument("--horizons", default=DEFAULT_HORIZONS,
                    help=f"multi-horizon mode (DEFAULT): comma-separated horizon specs "
                         f"like '90d,30d,7d,1d'. Generates one HTML report per horizon "
                         f"ending at --until (or now), plus a dashboard index. "
                         f"Set to '' (empty) to disable and use single-range mode.")
    ap.add_argument("--output-dir", default=None,
                    help="directory for multi-horizon reports (default: output/)")
    ap.add_argument("--granularity", choices=["day", "week", "month", "year"],
                    default="week",
                    help="aggregation period (single-range mode only; ignored in "
                         "multi-horizon mode where granularity is auto-selected per horizon)")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of text report (equivalent to --format json)")
    ap.add_argument("--format", choices=["text", "table", "markdown", "html", "json"],
                    default=None, help="output format (default: text; --json overrides to json)")
    ap.add_argument("--output", default=None,
                    help="write report to this file instead of stdout (format inferred from extension if --format not given)")
    ap.add_argument("--since", help="single-range mode: only include tasks starting on/after this date (YYYY-MM-DD). "
                    "Setting --since disables multi-horizon mode.")
    ap.add_argument("--until", help="end date for both modes (YYYY-MM-DD, default: today). "
                    "In multi-horizon: horizons end at this date. In single-range: only tasks on/before this date.")
    ap.add_argument("--git-email", default=None,
                    help="with --provision: set git user.email to this value (skips prompt)")
    ap.add_argument("--git-name", default=None,
                    help="with --provision: set git user.name to this value (optional)")
    ap.add_argument("--only", choices=["welink", "git"], default=None,
                    help="with --provision: only provision the specified source")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --provision: print commands without executing")
    ap.add_argument("--rebuild", action="store_true",
                    help="ignore watermark, do full reparse (overrides incremental)")
    ap.add_argument("--enrich-pages", action="store_true",
                    help="fetch and analyze actual web page content for browser time sinks "
                         "(top pages per task). External pages only — Huawei internal pages "
                         "require SSO and are skipped. Uses proxy when configured.")
    ap.add_argument("--persist", action="store_true",
                    help="save reconstructed tasks to output/tasks.jsonl (merged with prior)")
    ap.add_argument("--task", help="show full detail for a single task by id (e.g. explicit-<session_id>-<timestamp>)")
    ap.add_argument("--drill", action="store_true",
                    help="with --task: stage-by-stage root-cause analysis (Phase 10.2)")
    ap.add_argument("--top", type=int, metavar="N", default=None,
                    help="list the top N tasks by active time (with task IDs, so you can "
                         "--task <id> --drill into any of them). Use with --since/--until to scope.")
    # Early-exit modes are mutually exclusive — only one can run per invocation.
    _exclusive = ap.add_mutually_exclusive_group()
    _exclusive.add_argument("--sources", action="store_true",
                            help="report which sources were found/used/skipped, then exit")
    _exclusive.add_argument("--check", action="store_true",
                            help="verify environment + adapters, then exit (no analysis)")
    _exclusive.add_argument("--provision", action="store_true",
                            help="auto-provision welink-cli (install + auth login) and git identity "
                                 "(user.email/user.name). Requires Node.js >= 18 for welink-cli. "
                                 "Use --git-email/--git-name to pre-supply git identity, "
                                 "--only welink/git to scope, --dry-run to preview.")
    _exclusive.add_argument("--eval", action="store_true",
                            help="run segmentation evaluation against the labeled benchmark (Phase 9.8)")
    args = ap.parse_args()

    # --check and --eval are detection/evaluation-only modes that must NOT
    # collect personal session data. Handle them before the two-pass AI
    # collection below, which parses real Claude session records.
    if args.check:
        from sources import default_registry as _reg
        from persistence import detect_legacy_output, format_legacy_report
        # session_cwds not needed — --check only calls detect(), not collect().
        reg = _reg(session_cwds=[])
        print(render_check_output(reg._adapters))
        # Surface legacy output migration status (read-only, no personal contents).
        legacy = detect_legacy_output()
        if legacy["status"] != "current_only" and legacy["status"] != "none":
            print()
            print(format_legacy_report(legacy))
        sys.exit(0)

    if args.eval:
        from eval_segmentation import run_eval, format_metrics_report
        metrics = run_eval()
        print(format_metrics_report(metrics))
        sys.exit(0)

    if args.provision:
        do_provision = cmd_provision
        rc = do_provision(
            git_email=args.git_email,
            git_name=args.git_name,
            only=args.only,
            dry_run=args.dry_run,
        )
        sys.exit(rc)

    # Two-pass collection: first collect AI-session events to discover project cwds,
    # then build the registry with those cwds so the git adapter finds the right repos.
    from claude_code_adapter import ClaudeCodeAdapter
    from git_adapter import GitAdapter, discover_git_roots

    ai_adapter = ClaudeCodeAdapter()
    session_cwds: list[str] = []
    if ai_adapter.detect():
        ai_events = list(ai_adapter.collect())
        session_cwds = sorted({e.get("cwd") for e in ai_events if e.get("cwd")})

    reg = default_registry(session_cwds=session_cwds)

    # Collect events — incremental if watermark exists and --rebuild not set.
    from persistence import read_watermark, persist_run

    collection_started_at = time.time()
    watermark = None if args.rebuild else read_watermark()
    if watermark:
        # Incremental: only events after the watermark.
        # For the two-pass git discovery, we still need session cwds — collect those
        # from the full AI history (cheap, just the cwd field) even in incremental mode.
        events, skipped = reg.collect_all(watermark=watermark)
        # Also include any git commits after the watermark.
        # (The registry already handles this via collect_since on each adapter.)
    else:
        events, skipped = reg.collect_all()

    # --sources: report found/used/skipped, then exit.
    if args.sources:
        detected = [a.name for a in reg.detected()]
        print("# Sources")
        print(f"  detected: {detected}")
        print(f"  skipped:  {skipped}")
        # IM-honesty: welink-cli is the only source of WeLink chat history; no local
        # store exists (verified: 52 WeLink Desktop .db files, zero message tables).
        # Surface this plainly rather than silently dropping the chat category.
        welink_detected = any(a.name == "welink_cli" for a in reg.detected())
        if not welink_detected:
            print("")
            print("  NOTE: welink-cli not detected.")
            print("    - IM/chat history is UNAVAILABLE. WeLink stores no messages locally;")
            print("      welink-cli is the only path to chat data. This category is skipped,")
            print("      not silently dropped.")
            print("    - Meetings/calendar/mail have backup routes (see SKILL.md")
            print("      'Data sources without welink-cli'). Recordings, .ics export, and")
            print("      Outlook OST provide partial-to-full coverage of those domains.")
        sys.exit(0)

    # Tag filesystem file_edit events that were likely agent-edited (rubric 68):
    # VSCode Local History records agent edits too — without tagging, files the
    # user never touched appear as "frequently edited by the user." Must run
    # BEFORE segmentation so the summarizer sees the tags during _make_task().
    try:
        from cross_source import tag_agent_file_edits
        events = tag_agent_file_edits(events)
    except Exception as e:
        print(f"[cross_source] agent-edit tagging failed: {e}", file=sys.stderr)

    # Segment into tasks.
    try:
        tasks = segment(events)
    except Exception as e:
        print(f"[segment] stage failed: {e}", file=sys.stderr)
        print("[segment] continuing with empty task list.", file=sys.stderr)
        tasks = []

    # C7 fix: assign stable task IDs that survive across incremental runs.
    # The segment() function generates ephemeral IDs (explicit-N/implicit-N) that
    # are re-numbered from 1 each run, causing merge collisions. Remap to stable
    # IDs based on session_id + start timestamp.
    tasks = _remap_task_ids(tasks)

    # C7 fix: in incremental mode, collect_since() now yields ALL events from
    # sessions with any post-watermark event. Filter out tasks that are entirely
    # before the watermark (already processed in a prior run).
    if watermark:
        tasks = _filter_tasks_by_watermark(tasks, watermark)

    # Cross-source linking: naive commit attachment (Phase 1.4) + entity resolution (Phase 4.4).
    from cross_source import link_commits_to_tasks
    commit_events = [e for e in events if e.get("kind") == "commit"]
    try:
        tasks = link_commits_to_tasks(tasks, commit_events)
    except Exception as e:
        print(f"[cross_source] stage failed: {e}", file=sys.stderr)
        print("[cross_source] continuing with unlinked tasks.", file=sys.stderr)
    # Phase 4.4: probabilistic cross-source identity via Leiden graph clustering.
    try:
        from entity_resolution import resolve_cross_source_tasks
        tasks = resolve_cross_source_tasks(tasks)
    except ImportError:
        pass  # igraph unavailable — skip, naive linking stands
    except Exception as e:
        print(f"[entity_resolution] stage failed: {e}", file=sys.stderr)
        print("[entity_resolution] continuing with pre-resolution tasks.", file=sys.stderr)

    # Phase 10.1: detect parallel tasks (background sub-agents, concurrent sessions,
    # browser-during-coding) and compute exclusive time (non-overlapping union).
    exclusive = None
    try:
        from parallel_tasks import detect_parallel_tasks, compute_exclusive_time
        tasks = detect_parallel_tasks(tasks, events)
        exclusive = compute_exclusive_time(tasks)
    except ImportError:
        exclusive = None
    except Exception as e:
        print(f"[parallel_tasks] stage failed: {e}", file=sys.stderr)
        print("[parallel_tasks] continuing with pre-parallel tasks.", file=sys.stderr)

    # Phase 10.3: refine three-valued success using cross-task context (commit landed,
    # research followed by artifact, meeting followed by action, etc.).
    # Runs AFTER detect_parallel_tasks so that new background/browser tasks (which
    # have success=None) also get refined. Normalize None -> SUCCESS_UNKNOWN first
    # so refine_success's guard processes them.
    from segment_tasks import refine_success, SUCCESS_UNKNOWN
    for t in tasks:
        if t.get("success") is None:
            t["success"] = SUCCESS_UNKNOWN
    try:
        tasks = refine_success(tasks)
    except Exception as e:
        print(f"[refine_success] stage failed: {e}", file=sys.stderr)
        print("[refine_success] continuing with pre-refined success values.", file=sys.stderr)

    # --- Optional LLM labeling (Phase 7.3) ---
    try:
        from llm_labeling import label_tasks, get_labeler
        labeler = get_labeler()
        if labeler.is_available:
            print(f"[llm_labeling] backend: {labeler.backend_name} — labeling tasks...", file=sys.stderr)
            tasks = label_tasks(tasks)
            labeled = sum(1 for t in tasks if t.get("llm_label"))
            print(f"[llm_labeling] labeled {labeled}/{len(tasks)} tasks.", file=sys.stderr)
    except Exception as e:
        print(f"[llm_labeling] stage skipped: {e}", file=sys.stderr)

    # --- Optional page content enrichment (Phase 11) ---
    # Fetches actual web page content for browser time sinks, enabling deeper
    # narratives: what each page was about, how pages relate, why time was spent.
    # External pages only — Huawei internal pages (CloudDevOps, CodeHub, W3, etc.)
    # require SSO and are skipped gracefully. Cached in output/page_cache/.
    _default_out = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "output")
    _output_dir = args.output_dir or os.environ.get("RETRO_SCOPE_OUTPUT_DIR", _default_out)

    if args.enrich_pages:
        try:
            from page_enricher import enrich_tasks
            # Resolve proxy: CLI flag > env > git config (same as webpage-to-markdown).
            proxy = _resolve_proxy()
            browser_tasks = [t for t in tasks if t.get("source_kind") == "browser"]
            if browser_tasks:
                print(f"[page_enricher] enriching top pages for {len(browser_tasks)} browser tasks...",
                      file=sys.stderr)
                enrichment = enrich_tasks(tasks, events, _output_dir, proxy=proxy)
                if enrichment:
                    # Attach enrichment data to task context, then re-generate
                    # narratives for enriched browser tasks so they use page content.
                    from summarize import summarize_root_cause
                    enriched_count = 0
                    for t in tasks:
                        tid = t.get("id") or ""
                        if tid in enrichment:
                            ctx = t.setdefault("context", {})
                            ctx["page_enrichment"] = enrichment[tid]
                            # Re-generate narrative with enrichment data.
                            task_events = _events_for_task(t, events)
                            new_narrative = summarize_root_cause(t, task_events)
                            if new_narrative:
                                ctx["narrative"] = new_narrative
                            enriched_count += 1
                    print(f"[page_enricher] enriched {enriched_count} tasks with page content.",
                          file=sys.stderr)
        except Exception as e:
            print(f"[page_enricher] stage failed: {e}", file=sys.stderr)
            print("[page_enricher] continuing with title-based narratives.", file=sys.stderr)

    # --- Export detailed session records as evidence (rubric 66) ---
    # Extracts detailed session records for later inspection.
    # Default: skills/huawei-auto-pal/output/ (shared with skill-forge).
    _default_out = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "output")
    _output_dir = args.output_dir or os.environ.get("RETRO_SCOPE_OUTPUT_DIR", _default_out)
    try:
        _export_session_records(tasks, events, _output_dir)
    except Exception as e:
        print(f"[session_records] export failed: {e}", file=sys.stderr)

    # Persist the complete, unfiltered task set before any reporting branch
    # exits. Use the collection start time so events created during processing
    # remain eligible for the next run.
    if args.persist:
        persist_run(tasks, collection_started_at)

    # --- Multi-horizon mode (default) vs single-range mode ---
    # Multi-horizon is the default (--horizons=90d,30d,7d,1d). It's disabled when:
    #   - --since is set (explicit single-range request)
    #   - --horizons is explicitly empty
    #   - --format/--json/--output is set (single-report request)
    #   - --task/--top/--sources/--check/--eval mode — already exited above
    use_multi_horizon = (
        bool(args.horizons)
        and not args.since
        and not args.json
        and not args.format
        and not args.output
        and args.top is None
        and not args.task
    )

    if use_multi_horizon:
        from datetime import datetime as _dt, timezone as _tz
        # Compute the end timestamp: --until (end of day) or now.
        if args.until:
            end_ts = _parse_date(args.until) + 86400  # end of day
        else:
            end_ts = _dt.now(tz=_tz.utc).timestamp()
        try:
            horizons = _parse_horizon_spec(args.horizons)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)
        output_dir = args.output_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "output")
        output_dir = os.path.normpath(output_dir)
        print("# Multi-horizon analysis", file=sys.stderr)
        print(f"  horizons: {args.horizons}", file=sys.stderr)
        print(f"  end date: {_dt.fromtimestamp(end_ts, tz=_tz.utc).strftime('%Y-%m-%d')}",
              file=sys.stderr)
        index_path = _run_multi_horizon(
            tasks, events, horizons, end_ts, output_dir,
            exclusive, skipped)
        print(f"\nOpen the dashboard: {index_path}")
        sys.exit(0)

    # Single-range mode: filter by --since / --until.
    if args.since:
        since_ts = _parse_date(args.since)
        tasks = [t for t in tasks if (t.get("start") or 0) >= since_ts]
    if args.until:
        until_ts = _parse_date(args.until) + 86400  # end of day
        tasks = [t for t in tasks if (t.get("start") or 0) <= until_ts]

    # --top: list the biggest time sinks by active time, then exit.
    # Bridges aggregation -> drill-down: shows task IDs so the user can
    # immediately --task <id> --drill into any sink that stands out.
    if args.top is not None:
        if args.top < 1:
            print("--top requires N >= 1", file=sys.stderr)
            sys.exit(2)
        print(_render_top_tasks(tasks, args.top))
        sys.exit(0)

    # --task: show single task detail, then exit.
    if args.task:
        from aggregate import render_task_detail
        match = [t for t in tasks if t.get("id") == args.task]
        if not match:
            # also try partial match
            match = [t for t in tasks if args.task in (t.get("id") or "")]
        if match:
            task = match[0]
            if args.drill:
                # Phase 10.2: stage-by-stage root-cause analysis.
                # segment() doesn't attach the events list to task dicts, so we
                # reconstruct it from the raw events by matching session + time range.
                from drill_down import drill_down
                task_events = _events_for_task(task, events)
                task_with_events = {**task, "events": task_events}
                result = drill_down(task_with_events)
                print(_render_drill_down(result, task_with_events))
            else:
                print(render_task_detail(task))
        else:
            print(f"No task found matching '{args.task}'. "
                  f"Try one of: {', '.join(t['id'] for t in tasks[:10])}...")
        sys.exit(0)

    # Aggregate.
    try:
        agg = aggregate(tasks, args.granularity)
    except Exception as e:
        print(f"[aggregate] stage failed: {e}", file=sys.stderr)
        print("[aggregate] falling back to trivial aggregate (task count by kind).", file=sys.stderr)
        from collections import Counter
        kind_counts = Counter(t.get("source_kind", "unknown") for t in tasks)
        agg = {"_fallback": True, "task_count": len(tasks),
               "kinds": dict(kind_counts)}

    # Report.
    # Determine format: --json takes precedence (backwards compat), then --format,
    # then default "text".
    if args.json:
        fmt = "json"
    elif args.format:
        fmt = args.format
    else:
        fmt = "text"

    # If --output is given without --format, infer from extension.
    if args.output and not args.format and not args.json:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".md":
            fmt = "markdown"
        elif ext == ".html" or ext == ".htm":
            fmt = "html"
        elif ext == ".json":
            fmt = "json"
        # else: fall through to "text"

    def _exclusive_footer() -> str:
        """Build a one-line footer summarising exclusive time, or '' if unavailable."""
        if not exclusive:
            return ""
        excl_h = exclusive["exclusive_seconds"] / 3600
        wall_h = exclusive["wall_span_seconds"] / 3600
        overlap_h = exclusive["overlap_seconds"] / 3600
        return (f"\n(exclusive time: {excl_h:.1f}h "
                f"(wall span {wall_h:.1f}h, overlap {overlap_h:.1f}h, "
                f"{exclusive['n_parallel_groups']} parallel group(s)))")

    # Compute the single-range since_ts/until_ts for the data-availability section.
    _single_since = _parse_date(args.since) if args.since else None
    _single_until = (_parse_date(args.until) + 86400) if args.until else None

    def _render() -> str:
        """Produce the report string for the chosen format."""
        if fmt == "json":
            out = {"granularity": args.granularity, "aggregation": agg,
                   "source_count": len(reg.detected()), "skipped": skipped,
                   "task_count": len(tasks)}
            if exclusive:
                out["exclusive_time"] = exclusive
            return json.dumps(out, ensure_ascii=False, indent=2)
        elif fmt == "table":
            return render_table(agg, args.granularity)
        elif fmt == "markdown":
            text = render_markdown(agg, args.granularity, tasks=tasks)
            return text + _exclusive_footer()
        elif fmt == "html":
            text = render_html(agg, args.granularity, tasks=tasks,
                               since_ts=_single_since, until_ts=_single_until)
            footer = _exclusive_footer().strip()
            if footer:
                # Insert before </body> if present, else append.
                if "</body>" in text:
                    text = text.replace("</body>", f"<p>{footer}</p>\n</body>")
                else:
                    text += f"\n<p>{footer}</p>"
            return text
        else:
            text = render_report(agg, args.granularity, tasks=tasks)
            if skipped:
                text += f"\n(skipped sources: {skipped})"
            text += _exclusive_footer()
            return text

    if args.output:
        try:
            content = _render()
        except Exception as e:
            print(f"[render] stage failed: {e}", file=sys.stderr)
            print("[render] falling back to raw JSON output.", file=sys.stderr)
            content = json.dumps(agg, ensure_ascii=False, indent=2)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
            if not content.endswith("\n"):
                f.write("\n")
    else:
        try:
            print(_render())
        except Exception as e:
            print(f"[render] stage failed: {e}", file=sys.stderr)
            print("[render] falling back to raw JSON output.", file=sys.stderr)
            print(json.dumps(agg, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
