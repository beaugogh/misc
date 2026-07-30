"""Task-log persistence + incremental/watermark (Phase 2).

Stores reconstructed tasks in a flat JSONL log (output/tasks.jsonl) — a deliberately
simple intermediate that's easy to migrate to OCEL 2.0 later (Phase 5). Append-only
across runs with dedup by task id.

The watermark (output/last_run.txt) holds the last-analysis timestamp, enabling two-axis
incremental collection: new sessions/files + new messages in old sessions. Adapters that
support `collect_since(watermark)` use it; others fall back to full collect.

`output/` is gitignored via the skill's local .gitignore — a personal time log is
sensitive performance data and must never be committed to the shared repo.
"""

from __future__ import annotations

import os
import json
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
TASKS_LOG = os.path.join(OUTPUT_DIR, "tasks.jsonl")
WATERMARK_FILE = os.path.join(OUTPUT_DIR, "last_run.txt")


def ensure_data_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_watermark() -> float | None:
    """Read the last-analysis timestamp (epoch seconds). Returns None if no prior run."""
    if not os.path.exists(WATERMARK_FILE):
        return None
    try:
        with open(WATERMARK_FILE, encoding="utf-8") as f:
            return float(f.read().strip())
    except (ValueError, OSError):
        return None


def write_watermark(ts: float | None = None):
    """Write the watermark. Defaults to current time."""
    ensure_data_dir()
    if ts is None:
        ts = time.time()
    with open(WATERMARK_FILE, "w", encoding="utf-8") as f:
        f.write(str(ts))


def load_existing_tasks() -> list[dict]:
    """Load all tasks from the persistent log. Returns empty list if none."""
    if not os.path.exists(TASKS_LOG):
        return []
    tasks = []
    with open(TASKS_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                tasks.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return tasks


def save_tasks(tasks: list[dict], mode: str = "replace"):
    """Save tasks to the persistent log.

    `mode="replace"` — overwrite the log with the given tasks (full rebuild).
    `mode="merge"` — merge with existing tasks, dedup by task id (new/updated win).

    C7 fix: stable task IDs (format: ``{flavor}-{session_id}-{start_timestamp}``)
    ensure the same task gets the same ID across runs. When the same task appears
    in a new run (updated with new events), its stable ID matches the old entry
    and the merge correctly updates it rather than creating a duplicate.

    Old-format IDs (``explicit-N``, ``implicit-N``) are structurally different
    from new-format IDs — the old format has only two dash-separated parts while
    the new format has three or more (session_id itself may contain dashes).
    This prevents accidental collisions between old and new entries.
    """
    ensure_data_dir()
    if mode == "merge":
        existing = load_existing_tasks()
        by_id = {t["id"]: t for t in existing if "id" in t}
        for t in tasks:
            by_id[t["id"]] = t  # new/updated overwrites
        tasks = list(by_id.values())

    with open(TASKS_LOG, "w", encoding="utf-8") as f:
        for t in tasks:
            # Sort keys for stable diffs; ensure_ascii=False for CJK subjects.
            f.write(json.dumps(t, ensure_ascii=False, sort_keys=True) + "\n")


def incremental_collect(registry, watermark: float | None):
    """Collect events incrementally using the watermark.

    Returns (events, skipped) — same shape as registry.collect_all(), but only
    events after the watermark are included (for adapters that support collect_since).
    """
    return registry.collect_all(watermark=watermark)
