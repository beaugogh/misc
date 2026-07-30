"""Advanced segmentation methods (Phase 4).

Replaces the naive gap+cwd heuristics in segment_tasks.segment_implicit with:
  - PELT change-point detection (ruptures) on multivariate activity features
  - GMM (sklearn) on log inter-arrival times to learn a personalized gap threshold

These are the research-informed methods (see research-findings.md §2). Each falls back to
the naive heuristic if there are too few events or the library is unavailable.

This module is optional — segment_tasks works without it (stdlib-only). When available,
`segment_implicit_advanced()` is used in place of `segment_implicit()`.
"""

from __future__ import annotations

import math
import logging
from typing import Iterator

log = logging.getLogger(__name__)

# Minimum events for PELT/GMM to be meaningful.
MIN_EVENTS_FOR_PELT = 20
MIN_EVENTS_FOR_GMM = 30
# Maximum events for PELT — beyond this it's too slow (O(n) but with a large constant
# on high-dimensional signals). Fall back to naive for very large sessions.
MAX_EVENTS_FOR_PELT = 5000


def _try_imports():
    """Return (ruptures, sklearn_mixture) or (None, None) if unavailable."""
    try:
        import ruptures
    except ImportError:
        ruptures = None
    try:
        from sklearn import mixture as gmm_module
    except ImportError:
        gmm_module = None
    return ruptures, gmm_module


def learn_gap_threshold(events: list[dict], default: float = 30 * 60) -> float:
    """Learn a personalized gap threshold from inter-arrival times via a 2-component GMM.

    Fits a 2-component GMM to log-transformed inter-arrival times. The component with the
    lower mean = intra-task gaps; the higher mean = inter-task boundaries. The threshold is
    set at the boundary between the two components.

    Falls back to `default` (30 min) if too few events or sklearn unavailable.
    """
    _, gmm_mod = _try_imports()
    if gmm_mod is None:
        return default

    ts_list = sorted(e["timestamp"] for e in events if e.get("timestamp"))
    if len(ts_list) < MIN_EVENTS_FOR_GMM:
        return default

    # Compute log inter-arrival times
    gaps = [ts_list[i + 1] - ts_list[i] for i in range(len(ts_list) - 1)]
    gaps = [g for g in gaps if g > 0]  # exclude zero-gaps (same-timestamp bursts)
    if len(gaps) < MIN_EVENTS_FOR_GMM:
        return default

    log_gaps = [[math.log(g + 1)] for g in gaps]  # +1 to avoid log(0)

    try:
        gmm = gmm_mod.GaussianMixture(n_components=2, random_state=42)
        gmm.fit(log_gaps)
        means = gmm.means_.flatten()
        # The threshold is between the two component means (in log space)
        lower_mean = min(means)
        higher_mean = max(means)
        threshold_log = (lower_mean + higher_mean) / 2
        threshold = math.exp(threshold_log) - 1
        # Sanity: threshold should be between 1 min and 4 hours
        threshold = max(60, min(threshold, 4 * 3600))
        log.debug(f"GMM gap threshold: {threshold:.0f}s ({threshold/60:.1f} min)")
        return threshold
    except Exception as e:
        log.debug(f"GMM fitting failed: {e}, using default threshold")
        return default


def detect_boundaries_pelt(events: list[dict], gap_threshold: float = 30 * 60) -> list[int]:
    """Detect task-boundary change points using PELT on multivariate features.

    Features per event: timestamp, one-hot of kind, cwd hash. Returns a list of event
    indices where boundaries occur (the START of a new task).

    Falls back to the naive gap heuristic if ruptures unavailable or too few events.
    """
    ruptures, _ = _try_imports()
    if ruptures is None or len(events) < MIN_EVENTS_FOR_PELT:
        return _naive_gap_boundaries(events, gap_threshold)

    # Build feature matrix: for each event, a feature vector.
    # We use: [timestamp (normalized), kind_onehot..., cwd_hash]
    kinds = sorted({e.get("kind") or "?" for e in events})
    kind_idx = {k: i for i, k in enumerate(kinds)}
    cwds = sorted({e.get("cwd") or "" for e in events})
    cwd_idx = {c: i for i, c in enumerate(cwds)}

    import numpy as np
    n_features = 1 + len(kinds) + len(cwds)
    signals = np.zeros((len(events), n_features))
    ts_list = [e.get("timestamp", 0) for e in events]
    if not ts_list or max(ts_list) == min(ts_list):
        return _naive_gap_boundaries(events, gap_threshold)
    ts_min, ts_max = min(ts_list), max(ts_list)
    ts_range = ts_max - ts_min or 1

    for i, e in enumerate(events):
        signals[i, 0] = (e.get("timestamp", 0) - ts_min) / ts_range  # normalized timestamp
        k = kind_idx.get(e.get("kind", "?"), 0)
        if k < len(kinds):
            signals[i, 1 + k] = 1
        c = cwd_idx.get(e.get("cwd", ""), 0)
        if c < len(cwds):
            signals[i, 1 + len(kinds) + c] = 1

    # PELT with L2 cost. The penalty beta controls sensitivity — higher = fewer boundaries.
    # We scale beta by the number of features to keep it reasonable.
    try:
        algo = ruptures.Pelt(model="l2", min_size=3).fit(signals)
        # Penalty: tune by the signal variance. A higher penalty = fewer boundaries.
        penalty = 10 * n_features  # heuristic; tune against a labeled benchmark (Phase 4.5)
        change_points = algo.predict(pen=penalty)
        # ruptures returns the END of each segment; convert to start-of-new-task indices
        boundaries = [cp for cp in change_points if cp < len(events)]
        return boundaries
    except Exception as e:
        log.debug(f"PELT failed: {e}, falling back to naive")
        return _naive_gap_boundaries(events, gap_threshold)


def _naive_gap_boundaries(events: list[dict], gap_threshold: float) -> list[int]:
    """The naive gap heuristic — used as a fallback. Returns indices where a new task starts."""
    boundaries = []
    last_ts = None
    for i, ev in enumerate(events):
        ts = ev.get("timestamp")
        if last_ts is not None and ts is not None and (ts - last_ts) > gap_threshold:
            boundaries.append(i)
        if ts:
            last_ts = ts
    return boundaries


def segment_implicit_advanced(events: list[dict], counter: list[int],
                              use_pelt: bool = True) -> list[dict]:
    """Advanced implicit segmentation using PELT + GMM.

    Drop-in replacement for segment_tasks.segment_implicit when the libraries are available.
    Falls back to the full naive segment_implicit (gap+cwd+correction) per-session if PELT
    can't be applied (too few events or library unavailable).
    """
    from segment_tasks import (
        GAP_THRESHOLD_SECONDS, _summarize_message, _is_correction, _make_task,
        segment_implicit,
    )

    if not events:
        return []

    # If too few events for PELT, use the full naive heuristic (which handles cwd-shift
    # and corrections, not just gaps). This preserves test behavior for small fixtures.
    ruptures, _ = _try_imports()
    if (not use_pelt or ruptures is None
            or len(events) < MIN_EVENTS_FOR_PELT
            or len(events) > MAX_EVENTS_FOR_PELT):
        return segment_implicit(events, counter)

    # Learn the gap threshold from this user's data
    gap_threshold = learn_gap_threshold(events, default=GAP_THRESHOLD_SECONDS)

    # Detect boundaries via PELT
    boundary_indices = detect_boundaries_pelt(events, gap_threshold)

    # Build tasks by splitting at boundaries
    tasks: list[dict] = []
    boundary_set = set(boundary_indices)
    current: list[dict] = []
    current_subject: str | None = None

    def flush():
        nonlocal current, current_subject
        if current:
            counter[0] += 1
            tasks.append(_make_task(f"implicit-{counter[0]}", "implicit", current, current_subject))
            current = []
            current_subject = None

    for i, ev in enumerate(events):
        if i in boundary_set and current:
            flush()
        if ev.get("kind") == "user_message":
            if not current or current_subject is None:
                current_subject = _summarize_message(ev.get("text"))
        current.append(ev)
    flush()
    return tasks
