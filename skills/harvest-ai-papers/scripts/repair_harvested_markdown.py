#!/usr/bin/env python3
import argparse
from pathlib import Path

from harvest_manifest import normalize_markdown_quality


def parse_args():
    parser = argparse.ArgumentParser(description="Normalize harvested whole-paper Markdown readability in place.")
    parser.add_argument("paths", nargs="+", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    changed = 0
    files = []
    for path in args.paths:
        files.extend(sorted(path.glob("**/*.md")) if path.is_dir() else [path])
    for path in files:
        original = path.read_text(encoding="utf-8")
        repaired = normalize_markdown_quality(original)
        if repaired != original:
            path.write_text(repaired, encoding="utf-8")
            changed += 1
            print(f"repaired: {path}")
    print(f"Checked {len(files)}; repaired {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
