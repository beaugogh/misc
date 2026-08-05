#!/usr/bin/env python3
"""Initialize a minimal, platform-neutral skill directory."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VALID_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_NAMES = {"scripts", "references", "assets"}

TEMPLATE = """---
name: {name}
description: >
  TODO: State what this skill does and the concrete requests or contexts in which it should be used.
---

# {title}

## Principles

- TODO: State the essential constraints and domain rules.

## Workflow

1. TODO: Inspect inputs and constraints.
2. TODO: Perform the task.
3. TODO: Verify the result.

## Completion criteria

- TODO: Define observable success and important failure conditions.
"""


def validate_name(name: str) -> str | None:
    if len(name) > 64:
        return "name exceeds 64 characters"
    if not VALID_NAME.fullmatch(name):
        return "name must use lowercase letters, digits, and single hyphens"
    return None


def parse_resources(value: str) -> list[str]:
    if not value:
        return []
    resources = [item.strip() for item in value.split(",") if item.strip()]
    unknown = sorted(set(resources) - RESOURCE_NAMES)
    if unknown:
        raise argparse.ArgumentTypeError(
            f"unknown resource type(s): {', '.join(unknown)}; choose scripts,references,assets"
        )
    return list(dict.fromkeys(resources))


def initialize(name: str, parent: Path, resources: list[str]) -> Path:
    error = validate_name(name)
    if error:
        raise ValueError(error)

    destination = parent.expanduser().resolve() / name
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")

    destination.mkdir(parents=True)
    try:
        title = " ".join(part.capitalize() for part in name.split("-"))
        (destination / "SKILL.md").write_text(
            TEMPLATE.format(name=name, title=title), encoding="utf-8"
        )
        for resource in resources:
            (destination / resource).mkdir()
    except Exception:
        # Remove only the empty/new files this invocation created.
        for child in sorted(destination.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        destination.rmdir()
        raise
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="kebab-case skill name, at most 64 characters")
    parser.add_argument("--path", required=True, type=Path, help="parent directory")
    parser.add_argument(
        "--resources",
        default=[],
        type=parse_resources,
        help="optional comma-separated list: scripts,references,assets",
    )
    args = parser.parse_args()

    try:
        destination = initialize(args.name, args.path, args.resources)
    except (ValueError, FileExistsError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
