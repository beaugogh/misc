#!/usr/bin/env python3
"""Aggregate platform-neutral grading.json records below an evaluation workspace."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def mean_std(values: list[float]) -> dict[str, float | int | None]:
    return {
        "count": len(values),
        "mean": statistics.fmean(values) if values else None,
        "sample_stddev": statistics.stdev(values) if len(values) > 1 else None,
    }


def load_records(workspace: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(workspace.rglob("grading.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError(f"cannot parse {path}: {error}") from error
        if not isinstance(record, dict):
            raise ValueError(f"record must be an object: {path}")
        configuration = record.get("configuration")
        expectations = record.get("expectations")
        if not isinstance(configuration, str) or not configuration:
            raise ValueError(f"missing configuration: {path}")
        if not isinstance(expectations, list):
            raise ValueError(f"missing expectations list: {path}")
        record["_source"] = str(path.relative_to(workspace))
        records.append(record)
    if not records:
        raise ValueError(f"no grading.json records found below {workspace}")
    return records


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[record["configuration"]].append(record)

    configurations: dict[str, Any] = {}
    for name, group in sorted(groups.items()):
        statuses: list[str] = []
        critical_failures = 0
        for record in group:
            for expectation in record["expectations"]:
                if not isinstance(expectation, dict):
                    continue
                status = expectation.get("status", "unverified")
                statuses.append(status)
                if expectation.get("critical") and status != "pass":
                    critical_failures += 1
        durations = [float(r["duration_seconds"]) for r in group if isinstance(r.get("duration_seconds"), (int, float))]
        input_units = [float(r["input_units"]) for r in group if isinstance(r.get("input_units"), (int, float))]
        output_units = [float(r["output_units"]) for r in group if isinstance(r.get("output_units"), (int, float))]
        graded = sum(status in {"pass", "fail"} for status in statuses)
        passed = statuses.count("pass")
        configurations[name] = {
            "runs": len(group),
            "expectations": {status: statuses.count(status) for status in ("pass", "fail", "unverified")},
            "pass_rate": passed / graded if graded else None,
            "critical_failures": critical_failures,
            "duration_seconds": mean_std(durations),
            "input_units": mean_std(input_units),
            "output_units": mean_std(output_units),
            "sources": [record["_source"] for record in group],
        }
    comparisons: dict[str, Any] = {}
    baseline = configurations.get("baseline")
    if baseline:
        for name, configuration in configurations.items():
            if name == "baseline":
                continue
            comparison: dict[str, float | None] = {}
            for metric in ("pass_rate",):
                left = configuration.get(metric)
                right = baseline.get(metric)
                comparison[f"{metric}_delta"] = left - right if left is not None and right is not None else None
            for metric in ("duration_seconds", "input_units", "output_units"):
                left = configuration[metric]["mean"]
                right = baseline[metric]["mean"]
                comparison[f"{metric}_mean_delta"] = left - right if left is not None and right is not None else None
            comparisons[f"{name}_vs_baseline"] = comparison
    return {
        "schema_version": 1,
        "record_count": len(records),
        "configurations": configurations,
        "comparisons": comparisons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = aggregate(load_records(args.workspace.resolve()))
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
