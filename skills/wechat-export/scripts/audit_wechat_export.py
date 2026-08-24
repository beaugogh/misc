#!/usr/bin/env python3
"""Audit a WechatExporter account directory and optional JSON/CSV conversion."""

from __future__ import annotations

import argparse
import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from convert_wechat_export import iter_conversation_messages


RESOURCE_ATTRS = {"src", "poster", "data-src"}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value and key in RESOURCE_ATTRS | {"href"}:
                self.references.append((key, value))


def local_path(base: Path, reference: str) -> Path | None:
    if reference.startswith(("data:", "javascript:", "mailto:", "tel:", "#")):
        return None
    parsed = urlparse(reference)
    if parsed.scheme or reference.startswith("/"):
        return None
    return base / unquote(parsed.path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("account_dir", type=Path)
    parser.add_argument("--structured", type=Path)
    args = parser.parse_args()

    account = args.account_dir.expanduser().resolve()
    html_files = sorted(p for p in account.glob("*.html") if p.name != "index.html")
    if not html_files:
        parser.error(f"no conversation HTML files found in {account}")

    missing_html: list[str] = []
    remote_resources: list[str] = []
    message_count = 0
    missing_media: list[str] = []

    for html_file in html_files:
        ref_parser = ReferenceParser()
        ref_parser.feed(html_file.read_text(encoding="utf-8", errors="replace"))
        for attr, reference in ref_parser.references:
            if reference.startswith(("http://", "https://")):
                if attr in RESOURCE_ATTRS:
                    remote_resources.append(f"{html_file.name}: {reference}")
                continue
            path = local_path(html_file.parent, reference)
            if path is not None and not path.exists():
                missing_html.append(f"{html_file.name}: {reference}")

        for message in iter_conversation_messages(html_file):
            message_count += 1
            for reference in message.get("media_paths", []):
                path = local_path(account, reference)
                if path is not None and not path.exists():
                    missing_media.append(f"{html_file.stem}/{message['message_id']}: {reference}")

    result: dict[str, object] = {
        "conversations": len(html_files),
        "messages": message_count,
        "missing_html_references": len(missing_html),
        "missing_media_references": len(missing_media),
        "remote_resource_references": len(remote_resources),
    }
    failed = bool(missing_html or missing_media or remote_resources)

    if args.structured:
        structured = args.structured.expanduser().resolve()
        messages = json.loads((structured / "messages.json").read_text(encoding="utf-8"))
        summary = json.loads(
            (structured / "export_summary.json").read_text(encoding="utf-8")
        )
        with (structured / "messages.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            csv_count = sum(1 for _ in csv.DictReader(handle))
        result.update(
            {
                "json_messages": len(messages),
                "csv_messages": csv_count,
                "summary_messages": summary.get("message_count"),
                "summary_conversations": summary.get("conversation_count"),
            }
        )
        failed |= not (
            len(messages)
            == csv_count
            == summary.get("message_count")
            == message_count
            and summary.get("conversation_count") == len(html_files)
        )

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    for label, entries in (
        ("missing HTML", missing_html),
        ("missing media", missing_media),
        ("remote resources", remote_resources),
    ):
        for entry in entries[:20]:
            print(f"{label}: {entry}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
