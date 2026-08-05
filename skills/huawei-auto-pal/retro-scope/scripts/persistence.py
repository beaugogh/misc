"""Task-log persistence + incremental/watermark (Phase 2).

Stores reconstructed tasks in a flat JSONL log (output/tasks.jsonl) — a deliberately
simple intermediate that's easy to migrate to OCEL 2.0 later (Phase 5). Append-only
across runs with dedup by task id.

The watermark (output/retro_scope_last_run.txt) holds an epoch-seconds timestamp, enabling two-axis
incremental collection: new sessions/files + new messages in old sessions. Adapters that
support `collect_since(watermark)` use it; others fall back to full collect.

`output/` is gitignored via the skill's local .gitignore — a personal time log is
sensitive performance data and must never be committed to the shared repo.
"""

from __future__ import annotations

import os
import json
import time
import tempfile

# Default output directory: skills/huawei-auto-pal/output/ (two levels up
# from scripts/ — retro-scope is a component of huawei-auto-pal, so its
# output lives at the parent skill level, shared with skill-forge).
# Can be overridden via RETRO_SCOPE_OUTPUT_DIR env var or --output-dir flag.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_RETRO_SCOPE_DIR = os.path.dirname(_SCRIPTS_DIR)
_DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(_RETRO_SCOPE_DIR), "output")
OUTPUT_DIR = os.environ.get("RETRO_SCOPE_OUTPUT_DIR", _DEFAULT_OUTPUT_DIR)
TASKS_LOG = os.path.join(OUTPUT_DIR, "tasks.jsonl")
WATERMARK_FILE = os.path.join(OUTPUT_DIR, "retro_scope_last_run.txt")
LEGACY_WATERMARK_FILE = os.path.join(OUTPUT_DIR, "last_run.txt")


def ensure_data_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        os.chmod(OUTPUT_DIR, 0o700)
    except OSError:
        pass


def _atomic_write(path: str, content: str) -> None:
    """Write a private file atomically in the destination directory."""
    ensure_data_dir()
    fd, tmp_path = tempfile.mkstemp(prefix=f".{os.path.basename(path)}.", dir=OUTPUT_DIR)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.chmod(tmp_path, 0o600)
        except OSError:
            pass
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def read_watermark() -> float | None:
    """Read the last-analysis timestamp (epoch seconds). Returns None if no prior run."""
    path = WATERMARK_FILE
    if not os.path.exists(path):
        # One-time compatibility with the former shared watermark. A legacy
        # millisecond value belongs to skill-forge and must not be interpreted
        # as seconds.
        path = LEGACY_WATERMARK_FILE
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            value = float(f.read().strip())
        if value < 0 or value >= 100_000_000_000:
            return None
        return value
    except (ValueError, OSError):
        return None


def write_watermark(ts: float | None = None):
    """Atomically write an epoch-seconds watermark. Defaults to current time."""
    if ts is None:
        ts = time.time()
    _atomic_write(WATERMARK_FILE, str(float(ts)))


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

    content = "".join(
        json.dumps(t, ensure_ascii=False, sort_keys=True) + "\n"
        for t in tasks
    )
    _atomic_write(TASKS_LOG, content)


def persist_run(tasks: list[dict], collection_started_at: float) -> None:
    """Persist tasks before advancing the watermark.

    Stable task IDs make a retry safe if the process stops between the two
    atomic replacements. Writing the watermark last prevents data loss.
    """
    save_tasks(tasks, mode="merge")
    write_watermark(collection_started_at)


def incremental_collect(registry, watermark: float | None):
    """Collect events incrementally using the watermark.

    Returns (events, skipped) — same shape as registry.collect_all(), but only
    events after the watermark are included (for adapters that support collect_since).
    """
    return registry.collect_all(watermark=watermark)
