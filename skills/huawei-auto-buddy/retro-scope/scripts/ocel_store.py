"""OCEL 2.0 storage layer (Phase 5).

Migrates the flat JSONL task log to an Object-Centric Event Log (OCEL 2.0) via pm4py.

OCEL 2.0 models many-to-many relationships between events and objects — a flat timeline
can't represent "a task touches multiple files, and a file is touched by multiple tasks"
without duplication. OCEL's E2O (event-to-object) and O2O (object-to-object) relations
handle this natively.

Object types:
  - task: a reconstructed task (from segmentation)
  - file: a file touched by a task (from Write/Edit/Read tool calls)
  - commit: a git commit linked to a task
  - url: a browser URL visited during a task
  - session: an AI-agent session

Event types:
  - task_started, task_ended: task lifecycle
  - file_edited, file_read: file interactions within a task
  - committed: a commit was made
  - visited: a URL was visited

Relational queries this enables (that a flat log can't):
  - "Which files were touched by >1 task this week?"
  - "Which task produced this commit?"
  - "Which sessions contributed to this file's history?"
"""

from __future__ import annotations

import os
import json
import logging
from datetime import datetime, timezone

log = logging.getLogger(__name__)

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_RETRO_SCOPE_DIR = os.path.dirname(_SCRIPTS_DIR)
_DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(_RETRO_SCOPE_DIR), "output")
OUTPUT_DIR = os.environ.get("RETRO_SCOPE_OUTPUT_DIR", _DEFAULT_OUTPUT_DIR)
OCEL_DB_PATH = os.path.join(OUTPUT_DIR, "ocel.sqlite")


def _ts_to_iso(ts: float) -> str:
    """Convert epoch seconds to ISO 8601 string for OCEL."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def build_ocel(tasks: list[dict]):
    """Build an OCEL 2.0 object from a list of tasks, using pm4py.

    Returns an OCEL object that can be inspected, queried, or exported to SQLite.
    Falls back to None if pm4py unavailable.
    """
    try:
        from pm4py.objects.ocel.obj import OCEL
        import pandas as pd
    except ImportError:
        log.warning("pm4py unavailable — cannot build OCEL. Using JSONL fallback.")
        return None

    events_list = []
    relations_list = []
    objects_list = []

    seen_objects: set[tuple[str, str]] = set()

    def add_object(otype: str, oid: str):
        key = (otype, oid)
        if key not in seen_objects:
            seen_objects.add(key)
            objects_list.append({"ocel:type": otype, "ocel:oid": oid})

    eid_counter = 0
    for task in tasks:
        tid = task.get("id", "?")
        start = task.get("start", 0)
        end = task.get("end", start)
        subject = task.get("subject") or "(no subject)"
        cwd = task.get("cwd")
        session_id = task.get("session_id")

        # Task object
        add_object("task", tid)

        # Session object (if present)
        if session_id:
            add_object("session", session_id)

        # task_started event
        eid = f"e{eid_counter}"; eid_counter += 1
        events_list.append({"ocel:eid": eid, "ocel:activity": "task_started",
                            "ocel:timestamp": _ts_to_iso(start), "ocel:type": "task"})
        relations_list.append({"ocel:eid": eid, "ocel:type": "task", "ocel:oid": tid})
        if session_id:
            relations_list.append({"ocel:eid": eid, "ocel:type": "session", "ocel:oid": session_id})

        # task_ended event
        if end > start:
            eid = f"e{eid_counter}"; eid_counter += 1
            events_list.append({"ocel:eid": eid, "ocel:activity": "task_ended",
                                "ocel:timestamp": _ts_to_iso(end), "ocel:type": "task"})
            relations_list.append({"ocel:eid": eid, "ocel:type": "task", "ocel:oid": tid})

        # File objects (from outputs + inputs)
        for out in task.get("outputs", []):
            if out.startswith(("read: ", "url: ", "search: ", "grep: ", "prompt: ")):
                continue
            fid = out.replace("git commit: ", "").replace("bash: ", "")
            if "/" in fid or "\\" in fid or fid.endswith((".py", ".md", ".json", ".yaml", ".txt")):
                add_object("file", fid)
                eid = f"e{eid_counter}"; eid_counter += 1
                events_list.append({"ocel:eid": eid, "ocel:activity": "file_edited",
                                    "ocel:timestamp": _ts_to_iso(start), "ocel:type": "file"})
                relations_list.append({"ocel:eid": eid, "ocel:type": "file", "ocel:oid": fid})
                relations_list.append({"ocel:eid": eid, "ocel:type": "task", "ocel:oid": tid})

        # Commit objects (from git_commits)
        for c in task.get("git_commits", []):
            chash = c.get("hash", "?")
            add_object("commit", chash)
            eid = f"e{eid_counter}"; eid_counter += 1
            events_list.append({"ocel:eid": eid, "ocel:activity": "committed",
                                "ocel:timestamp": _ts_to_iso(c.get("timestamp", start)),
                                "ocel:type": "commit"})
            relations_list.append({"ocel:eid": eid, "ocel:type": "commit", "ocel:oid": chash})
            relations_list.append({"ocel:eid": eid, "ocel:type": "task", "ocel:oid": tid})

    # Build the OCEL object with pandas DataFrames
    events_df = pd.DataFrame(events_list)
    objects_df = pd.DataFrame(objects_list)
    relations_df = pd.DataFrame(relations_list)

    if events_df.empty:
        log.warning("No events to build OCEL from")
        return None

    ocel = OCEL(
        events=events_df,
        objects=objects_df,
        relations=relations_df,
    )
    return ocel


def save_ocel_sqlite(ocel, path: str = OCEL_DB_PATH):
    """Save an OCEL object to a SQLite database via pm4py."""
    try:
        import pm4py
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pm4py.write_ocel2_sqlite(ocel, path)
        return path
    except Exception as e:
        log.error(f"Failed to save OCEL SQLite: {e}")
        return None


def relational_query_files_multi_task(ocel) -> list[dict]:
    """Query: which files were touched by >1 task?

    This is the relational query a flat timeline can't answer. Returns a list of
    {file, task_count, tasks: [...]}.
    """
    try:
        import pandas as pd
    except ImportError:
        return []

    df = ocel.relations
    if not hasattr(df, "columns"):
        df = pd.DataFrame(df)

    # Get file oids and task oids per event
    file_rels = df[df["ocel:type"] == "file"][["ocel:eid", "ocel:oid"]].rename(
        columns={"ocel:oid": "file_id"})
    task_rels = df[df["ocel:type"] == "task"][["ocel:eid", "ocel:oid"]].rename(
        columns={"ocel:oid": "task_id"})

    # Join: events that involve both a file and a task
    merged = file_rels.merge(task_rels, on="ocel:eid", how="inner")

    # Count distinct tasks per file
    file_task_counts = merged.groupby("file_id")["task_id"].nunique().reset_index()
    file_task_counts.columns = ["file_id", "task_count"]
    multi = file_task_counts[file_task_counts["task_count"] > 1]

    result = []
    for _, row in multi.iterrows():
        fid = row["file_id"]
        tasks = merged[merged["file_id"] == fid]["task_id"].unique().tolist()
        result.append({"file": fid, "task_count": int(row["task_count"]), "tasks": tasks})
    return sorted(result, key=lambda x: -x["task_count"])


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from sources import default_registry
    from segment_tasks import segment
    from cross_source import link_commits_to_tasks

    reg = default_registry()
    events, _ = reg.collect_all()
    tasks = segment(events)
    commits = [e for e in events if e.get("kind") == "commit"]
    tasks = link_commits_to_tasks(tasks, commits)

    print(f"Building OCEL from {len(tasks)} tasks...", file=sys.stderr)
    ocel = build_ocel(tasks)
    if ocel is None:
        print("pm4py unavailable", file=sys.stderr)
        sys.exit(1)

    path = save_ocel_sqlite(ocel)
    print(f"OCEL saved to: {path}", file=sys.stderr)

    # Relational query
    multi = relational_query_files_multi_task(ocel)
    print(f"\n# Files touched by >1 task: {len(multi)}", file=sys.stderr)
    for m in multi[:10]:
        print(f"  {m['file'][:60]} — {m['task_count']} tasks")
