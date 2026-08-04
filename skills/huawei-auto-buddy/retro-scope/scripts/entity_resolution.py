"""Cross-source entity resolution via temporal-decay graph + Leiden (Phase 4.4).

Replaces the naive cwd+time linker (Phase 1.4 scaffolding) with a probabilistic graph-
based approach:

  1. Each reconstructed task (from segmentation) becomes a node.
  2. Edges between tasks are weighted by a fusion of temporal proximity and semantic
     similarity, with exponential time decay: w_ij = sim(i,j) * exp(-lambda * dt).
  3. The Leiden algorithm (igraph) partitions nodes into communities — each community
     is a unified cross-source task identity.

This handles the case where an AI coding session, a git commit, and a browser visit all
belong to one task but were segmented as separate tasks by the per-source segmenter.

Research reference: research-findings.md §3.2 (Temporal Graph Clustering).

Falls back to the naive linker (cross_source.link_commits_to_tasks) if igraph unavailable.
"""

from __future__ import annotations

import math
import logging
from typing import Iterator

log = logging.getLogger(__name__)

# Exponential decay lambda: how fast temporal relevance drops.
# With lambda=1/3600, a 1-hour gap reduces the weight by e^-1 ≈ 0.37.
DEFAULT_LAMBDA = 1.0 / 3600.0  # per second

# Minimum edge weight to include (below this, no meaningful link).
MIN_EDGE_WEIGHT = 0.05

# Maximum temporal window for considering links (beyond this, decay makes weight ~0).
MAX_LINK_WINDOW = 6 * 3600  # 6 hours


def _semantic_similarity(task_a: dict, task_b: dict) -> float:
    """Compute a crude semantic similarity between two tasks (Jaccard on token sets).

    Compares subject text, cwd, and tool names. Returns [0, 1].
    """
    def tokens(t: dict) -> set[str]:
        s = set()
        subj = (t.get("subject") or "").lower()
        s.update(subj.split())
        cwd = (t.get("cwd") or "").lower()
        s.update(cwd.replace("\\", "/").split("/"))
        s.update(t.get("tool_names") or [])
        s.discard("")
        return s

    ta = tokens(task_a)
    tb = tokens(task_b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def resolve_cross_source_tasks(tasks: list[dict], lambda_decay: float = DEFAULT_LAMBDA) -> list[dict]:
    """Link tasks across sources using a temporal-decay graph + Leiden clustering.

    Returns the tasks list with an added `cluster_id` field — tasks sharing a cluster_id
    belong to the same cross-source task identity. Also merges git_commits from linked tasks.

    Falls back to no-op (each task its own cluster) if igraph is unavailable or too few tasks.
    """
    try:
        import igraph as ig
    except ImportError:
        log.debug("igraph unavailable, skipping cross-source resolution")
        for i, t in enumerate(tasks):
            t["cluster_id"] = i
        return tasks

    if len(tasks) < 2:
        for i, t in enumerate(tasks):
            t["cluster_id"] = i
        return tasks

    # Build the graph: nodes are tasks, edges weighted by temporal-decay * semantic sim.
    n = len(tasks)
    edges: list[tuple[int, int, float]] = []

    # Sort tasks by start time for efficient windowed comparison
    indexed = sorted(enumerate(tasks), key=lambda x: x[1].get("start") or 0.0)

    for i in range(len(indexed)):
        idx_i, t_i = indexed[i]
        ts_i = t_i.get("start") or 0.0
        for j in range(i + 1, len(indexed)):
            idx_j, t_j = indexed[j]
            ts_j = t_j.get("start") or 0.0
            dt = ts_j - ts_i
            if dt > MAX_LINK_WINDOW:
                break  # sorted by time; no further links possible
            if dt < 0:
                dt = 0
            sim = _semantic_similarity(t_i, t_j)
            if sim < 0.01:
                continue
            weight = sim * math.exp(-lambda_decay * dt)
            if weight >= MIN_EDGE_WEIGHT:
                edges.append((idx_i, idx_j, weight))

    if not edges:
        for i, t in enumerate(tasks):
            t["cluster_id"] = i
        return tasks

    # Build igraph and run Leiden
    g = ig.Graph(n=n, edges=[(e[0], e[1]) for e in edges], directed=False)
    g.es["weight"] = [e[2] for e in edges]

    try:
        clusters = g.community_leiden(
            objective_function="modularity",
            weights="weight",
            resolution=1.0,
            n_iterations=-1,
        )
        membership = clusters.membership
    except Exception as e:
        log.debug(f"Leiden failed: {e}, each task its own cluster")
        membership = list(range(n))

    # Assign cluster ids and merge git_commits within clusters
    for i, t in enumerate(tasks):
        t["cluster_id"] = membership[i]

    # Merge commits across tasks in the same cluster
    cluster_commits: dict[int, list[dict]] = {}
    for i, t in enumerate(tasks):
        cid = membership[i]
        for c in t.get("git_commits", []):
            cluster_commits.setdefault(cid, []).append(c)
    for i, t in enumerate(tasks):
        cid = membership[i]
        if cid in cluster_commits:
            existing = set(c.get("hash") for c in t.get("git_commits", []))
            for c in cluster_commits[cid]:
                if c.get("hash") not in existing:
                    t.setdefault("git_commits", []).append(c)

    return tasks


if __name__ == "__main__":
    # Smoke test against real data
    import sys, os, json
    sys.path.insert(0, os.path.dirname(__file__))
    from sources import default_registry
    from segment_tasks import segment
    from cross_source import link_commits_to_tasks

    reg = default_registry()
    events, _ = reg.collect_all()
    tasks = segment(events)
    commits = [e for e in events if e.get("kind") == "commit"]
    tasks = link_commits_to_tasks(tasks, commits)
    tasks = resolve_cross_source_tasks(tasks)

    cluster_sizes = {}
    for t in tasks:
        cid = t.get("cluster_id", 0)
        cluster_sizes[cid] = cluster_sizes.get(cid, 0) + 1
    multi = {k: v for k, v in cluster_sizes.items() if v > 1}
    print(f"# {len(tasks)} tasks, {len(cluster_sizes)} clusters, {len(multi)} multi-task clusters", file=sys.stderr)
    for cid, size in sorted(multi.items(), key=lambda x: -x[1])[:5]:
        members = [t for t in tasks if t.get("cluster_id") == cid]
        print(f"  cluster {cid} ({size} tasks):")
        for m in members[:3]:
            print(f"    {m['id']} {(m.get('subject') or '')[:50]} [{m.get('source_kind','?')}]")
