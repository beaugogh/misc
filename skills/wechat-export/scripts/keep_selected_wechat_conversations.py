#!/usr/bin/env python3
"""Destructively retain only selected conversations in a generated WeChat export."""

from __future__ import annotations

import csv
import html
import json
import os
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote


PORTRAIT_RE = re.compile(r'["\'](?:\.\./)?Portrait/([^"\']+)["\']')


def rebuild_account_index(account_dir: Path, targets: list[str]) -> None:
    links = "\n".join(
        f'      <li><a href="{quote(name + ".html")}">{html.escape(name)}</a></li>'
        for name in targets
    )
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Selected WeChat conversations</title>
  <style>
    body {{ max-width: 760px; margin: 40px auto; padding: 0 20px; font: 17px -apple-system, sans-serif; }}
    li {{ margin: 14px 0; }}
  </style>
</head>
<body>
  <h1>Selected WeChat conversations</h1>
  <ul>
{links}
  </ul>
</body>
</html>
"""
    temp = account_dir / "index.html.tmp"
    temp.write_text(page, encoding="utf-8")
    os.replace(temp, account_dir / "index.html")


def prune_html(account_dir: Path, targets: set[str]) -> tuple[int, int]:
    removed_pages = 0
    removed_dirs = 0
    for html_path in account_dir.glob("*.html"):
        if html_path.name == "index.html" or html_path.stem in targets:
            continue
        paired_dir = html_path.with_name(f"{html_path.stem}_files")
        html_path.unlink()
        removed_pages += 1
        if paired_dir.is_dir():
            shutil.rmtree(paired_dir)
            removed_dirs += 1
    return removed_pages, removed_dirs


def referenced_portraits(account_dir: Path, targets: set[str]) -> set[str]:
    keep: set[str] = set()
    for name in targets:
        paths = [account_dir / f"{name}.html"]
        data_dir = account_dir / f"{name}_files" / "Data"
        if data_dir.is_dir():
            paths.extend(data_dir.glob("msg-*.js"))
        for path in paths:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            keep.update(unquote(match) for match in PORTRAIT_RE.findall(text))
    return keep


def prune_portraits(account_dir: Path, keep: set[str]) -> int:
    portrait_dir = account_dir / "Portrait"
    if not portrait_dir.is_dir():
        return 0
    removed = 0
    for path in portrait_dir.iterdir():
        if path.is_file() and path.name not in keep:
            path.unlink()
            removed += 1
    return removed


def filter_structured(structured_dir: Path, targets: set[str]) -> dict:
    source_json = structured_dir / "messages.json"
    source_csv = structured_dir / "messages.csv"
    summary_path = structured_dir / "export_summary.json"
    temp_json = structured_dir / "messages.json.tmp"
    temp_csv = structured_dir / "messages.csv.tmp"

    with source_json.open(encoding="utf-8") as handle:
        messages = json.load(handle)
    kept = [record for record in messages if record.get("conversation") in targets]

    with temp_json.open("w", encoding="utf-8") as handle:
        json.dump(kept, handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")

    with source_csv.open(encoding="utf-8-sig", newline="") as src, temp_csv.open(
        "w", encoding="utf-8-sig", newline=""
    ) as dst:
        reader = csv.DictReader(src)
        assert reader.fieldnames is not None
        writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row.get("conversation") in targets:
                writer.writerow(row)

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["conversations"] = [
        item for item in summary.get("conversations", []) if item.get("conversation") in targets
    ]
    summary["conversation_count"] = len(summary["conversations"])
    summary["message_count"] = len(kept)
    summary["message_type_counts"] = dict(
        Counter(str(record.get("message_type", "")) for record in kept).most_common()
    )
    summary["direction_counts"] = dict(
        Counter(record.get("direction", "unknown") for record in kept)
    )
    temp_summary = structured_dir / "export_summary.json.tmp"
    temp_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    os.replace(temp_json, source_json)
    os.replace(temp_csv, source_csv)
    os.replace(temp_summary, summary_path)
    return {"messages": len(kept), "conversations": len(summary["conversations"])}


def main() -> int:
    if len(sys.argv) < 4:
        raise SystemExit("usage: script ACCOUNT_DIR STRUCTURED_DIR CONVERSATION...")
    account_dir = Path(sys.argv[1]).resolve()
    structured_dir = Path(sys.argv[2]).resolve()
    ordered_targets = sys.argv[3:]
    targets = set(ordered_targets)

    missing = [name for name in ordered_targets if not (account_dir / f"{name}.html").is_file()]
    if missing:
        raise SystemExit(f"missing exact conversation pages: {missing}")

    stats = filter_structured(structured_dir, targets)
    removed_pages, removed_dirs = prune_html(account_dir, targets)
    keep_portraits = referenced_portraits(account_dir, targets)
    removed_portraits = prune_portraits(account_dir, keep_portraits)
    rebuild_account_index(account_dir, ordered_targets)

    stats.update(
        {
            "removed_conversation_pages": removed_pages,
            "removed_conversation_media_dirs": removed_dirs,
            "kept_portraits": len(keep_portraits),
            "removed_portraits": removed_portraits,
        }
    )
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
