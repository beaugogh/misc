"""Auto-categorization (Phase 7).

Replaces the crude `classify_task` in aggregate.py with:
  1. Domain detection from file paths + package manifests (Git Timeline MCP technique).
  2. PPMI embeddings + K-means clustering for unsupervised taxonomy discovery.
  3. RIPPER rules (wittgenstein) as an interpretable, user-auditable fallback.
  4. LLM labeling (optional, if a local LLM is available).

The taxonomy is hybrid: auto-derive a draft, let the user merge/rename.
"""

from __future__ import annotations

import os
import re
import logging
from collections import Counter, defaultdict
from typing import Iterator

log = logging.getLogger(__name__)

# Known package-config filenames that signal a project's domain.
PACKAGE_FILES = {"package.json", "requirements.txt", "pyproject.toml", "setup.py",
                 "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "docker-compose.yml",
                 "Dockerfile", ".eslintrc", "tsconfig.json"}

# Domain keywords detected from file paths.
DOMAIN_KEYWORDS = {
    "auth": ["auth", "login", "session", "token", "password", "oauth", "sso"],
    "api": ["api", "endpoint", "route", "handler", "controller", "middleware"],
    "ui": ["ui", "frontend", "component", "view", "page", "render", "css", "style"],
    "data": ["data", "model", "schema", "migration", "database", "db", "sql"],
    "test": ["test", "spec", "fixture", "mock", "assert"],
    "docs": ["doc", "readme", "guide", "tutorial", "help"],
    "config": ["config", "settings", "env", "deploy", "ci", "docker"],
    "ml": ["model", "train", "infer", "predict", "dataset", "embedding", "vector"],
    "skill": ["skill", "plugin", "adapter", "extension"],
    "meeting": ["meeting", "record", "transcribe", "agenda", "minutes"],
}


def detect_domain(file_paths: list[str], cwd: str | None = None) -> str | None:
    """Detect the business domain from file paths + package manifests.

    Uses the Git Timeline MCP technique: infer domain from which files/packages
    were touched, not from commit messages. File paths encode the business domain
    directly (auth, billing, onboarding) where commit messages describe the change.
    """
    # Collect all path components
    all_parts = []
    for fp in file_paths:
        fp_lower = (fp or "").lower().replace("\\", "/")
        all_parts.extend(fp_lower.split("/"))
        # check for package files
        basename = os.path.basename(fp_lower)
        if basename in PACKAGE_FILES:
            all_parts.append(basename)

    if cwd:
        cwd_lower = cwd.lower().replace("\\", "/")
        all_parts.extend(cwd_lower.split("/"))

    parts_text = " ".join(all_parts)

    # Score each domain by keyword matches
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in parts_text)
        if score > 0:
            scores[domain] = score

    if scores:
        return max(scores, key=scores.get)
    return None


def classify_task_advanced(task: dict) -> str:
    """Advanced task classifier using domain detection + source_kind + tools.

    Replaces aggregate.classify_task. Falls back to the crude rules if domain
    detection yields nothing.
    """
    source_kind = task.get("source_kind", "")
    tools = set(task.get("tool_names") or [])
    cwd = task.get("cwd") or ""

    # Browser-sourced tasks
    if source_kind == "browser":
        return "research"

    # VCS-sourced tasks
    if source_kind == "vcs":
        return "vcs"

    # Meeting-sourced tasks
    if source_kind == "meeting":
        return "meeting"

    # Filesystem-sourced tasks (VSCode history, Windows Recent)
    if source_kind == "filesystem":
        # Try domain detection on the file path
        file_paths = []
        ti = task.get("tool_input") or {}
        if ti.get("resource"):
            file_paths.append(ti["resource"])
        if ti.get("target_name"):
            file_paths.append(ti["target_name"])
        domain = detect_domain(file_paths, cwd)
        if domain:
            return domain
        return "other"

    # AI-session tasks: try domain detection from outputs (file paths) + cwd
    outputs = task.get("outputs", [])
    file_paths = [o for o in outputs if "/" in o or "\\" in o or o.endswith((".py", ".md", ".json"))]
    domain = detect_domain(file_paths, cwd)
    if domain:
        return domain

    # Fall back to tool-based classification
    if tools & {"Edit", "Write", "Read", "Bash"}:
        return "coding"
    if tools & {"WebSearch", "WebFetch"}:
        return "research"
    if any(k in (task.get("subject") or "").lower() for k in ("commit", "push", "rebase")):
        return "vcs"
    if not tools and task.get("event_count", 0) <= 3:
        return "conversation"
    return "other"


def cluster_tasks_ppmi(tasks: list[dict], n_clusters: int = 8) -> dict[str, str]:
    """Cluster tasks by PPMI embeddings of their signals (paths, tools, URLs, subjects).

    Returns a mapping {task_id: cluster_label}. Uses K-means on PPMI vectors.
    Falls back to per-task-unique labels if sklearn unavailable or too few tasks.
    """
    try:
        import numpy as np
        from sklearn.cluster import KMeans
    except ImportError:
        return {t["id"]: f"cluster-{i}" for i, t in enumerate(tasks)}

    if len(tasks) < n_clusters:
        return {t["id"]: f"cluster-{i}" for i, t in enumerate(tasks)}

    # Build vocabulary from task signals
    vocab: dict[str, int] = {}
    task_tokens: list[list[str]] = []

    for t in tasks:
        tokens = []
        # tool names
        tokens.extend(t.get("tool_names") or [])
        # cwd path components
        cwd = (t.get("cwd") or "").lower().replace("\\", "/")
        tokens.extend(cwd.split("/"))
        # output file extensions + path components
        for o in t.get("outputs", []):
            o_lower = o.lower()
            tokens.extend(o_lower.replace("\\", "/").split("/"))
            if "." in o:
                tokens.append(f"ext:{o.rsplit('.', 1)[-1]}")
        # subject words
        subj = (t.get("subject") or "").lower()
        tokens.extend(subj.split())
        task_tokens.append(tokens)
        for tok in set(tokens):
            vocab[tok] = vocab.get(tok, 0) + 1

    if not vocab:
        return {t["id"]: "cluster-0" for t in tasks}

    # Build PPMI matrix
    vocab_list = sorted(vocab.keys())
    vocab_idx = {w: i for i, w in enumerate(vocab_list)}
    n_tasks = len(tasks)
    n_vocab = len(vocab_list)

    # Co-occurrence: task x vocab
    cooc = np.zeros((n_tasks, n_vocab))
    for i, tokens in enumerate(task_tokens):
        for tok in set(tokens):
            if tok in vocab_idx:
                cooc[i, vocab_idx[tok]] += 1

    # PPMI: pmi = log(p(t,w) / (p(t) * p(w))); ppmi = max(pmi, 0)
    total = cooc.sum()
    if total == 0:
        return {t["id"]: "cluster-0" for t in tasks}
    p_t = cooc.sum(axis=1, keepdims=True) / total
    p_w = cooc.sum(axis=0, keepdims=True) / total
    p_tw = cooc / total
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(p_tw / (p_t * p_w + 1e-10) + 1e-10)
    ppmi = np.maximum(pmi, 0)

    # K-means
    k = min(n_clusters, n_tasks)
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(ppmi)

    return {tasks[i]["id"]: f"cluster-{labels[i]}" for i in range(n_tasks)}


def train_ripper_rules(tasks: list[dict], labels: dict[str, str]) -> list | None:
    """Train RIPPER rules on labeled tasks for an interpretable classifier.

    Returns the trained model, or None if wittgenstein unavailable.
    The rules let users audit/fix the categorization logic.
    """
    try:
        import wittgenstein as lw
        import pandas as pd
    except ImportError:
        return None

    # Build feature dataframe
    rows = []
    for t in tasks:
        label = labels.get(t["id"], "other")
        tools = ",".join(sorted(t.get("tool_names") or []))
        cwd = (t.get("cwd") or "").lower().replace("\\", "/")
        has_edit = "Edit" in (t.get("tool_names") or [])
        has_bash = "Bash" in (t.get("tool_names") or [])
        has_web = bool({"WebSearch", "WebFetch"} & set(t.get("tool_names") or []))
        n_outputs = len(t.get("outputs", []))
        n_events = t.get("event_count", 0)
        rows.append({
            "label": label,
            "has_edit": has_edit,
            "has_bash": has_bash,
            "has_web": has_web,
            "n_outputs": n_outputs,
            "n_events": n_events,
            "cwd_contains_workspace": "workspace" in cwd,
            "cwd_contains_skill": "skill" in cwd,
        })

    df = pd.DataFrame(rows)
    if df.empty or df["label"].nunique() < 2:
        return None

    ripper = lw.RIPPER()
    try:
        ripper.fit(df, class_feat="label")
        return ripper
    except Exception as e:
        log.debug(f"RIPPER training failed: {e}")
        return None


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from sources import default_registry
    from segment_tasks import segment

    reg = default_registry()
    events, _ = reg.collect_all()
    tasks = segment(events)

    # Classify with domain detection
    from collections import Counter
    kinds = Counter(classify_task_advanced(t) for t in tasks)
    print(f"# Advanced classification ({len(tasks)} tasks):")
    for k, n in kinds.most_common():
        print(f"  {k:15s} {n:4d} tasks")

    # Cluster
    labels = cluster_tasks_ppmi(tasks, n_clusters=8)
    cluster_sizes = Counter(labels.values())
    print(f"\n# PPMI clusters: {len(cluster_sizes)}")
    for c, n in cluster_sizes.most_common(8):
        print(f"  {c}: {n} tasks")

    # RIPPER rules
    rules = train_ripper_rules(tasks, labels)
    if rules:
        print(f"\n# RIPPER rules trained: {rules.ruleset_}")
    else:
        print("\n# RIPPER: unavailable or too few labels")
