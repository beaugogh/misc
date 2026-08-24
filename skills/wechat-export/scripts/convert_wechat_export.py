#!/usr/bin/env python3
"""Convert WechatExporter HTML output into structured JSON and CSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\b")
PAGE_RE = re.compile(r"msg-(\d+)\.js$")
ARRAY_RE = re.compile(r"\bvar\s+msgArray\s*=\s*(\[.*?\]);\s*for\s*\(", re.S)


class MessageHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.messages: list[dict] = []
        self.in_message = False
        self.div_depth = 0
        self.nt_depth: int | None = None
        self.content_depth: int | None = None
        self.in_sender = False
        self.in_message_text = False
        self.current: dict | None = None
        self._nt_text: list[str] = []
        self._sender_text: list[str] = []
        self._message_text: list[str] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k: (v or "") for k, v in attrs}

    @staticmethod
    def _classes(attrs: dict[str, str]) -> set[str]:
        return set(attrs.get("class", "").split())

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = self._attrs(attrs_list)
        classes = self._classes(attrs)

        if tag == "div" and not self.in_message and "msg" in classes:
            self.in_message = True
            self.div_depth = 1
            direction = "outgoing" if "right" in classes else "incoming" if "left" in classes else "unknown"
            self.current = {
                "message_id": attrs.get("msgid", ""),
                "message_type": attrs.get("msgtype", ""),
                "direction": direction,
                "sender_display": "",
                "sender_id": "",
                "timestamp": "",
                "text": "",
                "media_paths": [],
                "links": [],
            }
            self._nt_text = []
            self._sender_text = []
            self._message_text = []
            return

        if not self.in_message:
            return

        if tag == "div":
            self.div_depth += 1
            if "nt-box" in classes:
                self.nt_depth = self.div_depth
            if "content-box" in classes:
                self.content_depth = self.div_depth

        if tag == "span" and "dspname" in classes:
            self.in_sender = True
            assert self.current is not None
            self.current["sender_id"] = attrs.get("wxid", attrs.get("wxId", ""))

        if tag == "span" and "msg-text" in classes:
            self.in_message_text = True

        if tag == "br" and self.in_message_text:
            self._message_text.append("\n")

        if tag in {"img", "audio", "video", "source"} and self.content_depth is not None:
            path = attrs.get("src", "")
            if path:
                assert self.current is not None
                self.current["media_paths"].append(unquote(path))
            if tag == "img" and "wxemoji" in classes and self.in_message_text:
                emoji = attrs.get("rawemoji") or attrs.get("title") or attrs.get("alt")
                if emoji:
                    self._message_text.append(emoji)

        if tag == "a" and self.content_depth is not None:
            href = attrs.get("href", "")
            if href:
                assert self.current is not None
                self.current["links"].append(unquote(href))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if not self.in_message:
            return

        if tag == "span" and self.in_sender:
            self.in_sender = False
        elif tag == "span" and self.in_message_text:
            self.in_message_text = False

        if tag != "div":
            return

        if self.nt_depth == self.div_depth:
            self.nt_depth = None
        if self.content_depth == self.div_depth:
            self.content_depth = None

        self.div_depth -= 1
        if self.div_depth == 0:
            self._finish_message()

    def handle_data(self, data: str) -> None:
        if not self.in_message:
            return
        if self.nt_depth is not None:
            self._nt_text.append(data)
        if self.in_sender:
            self._sender_text.append(data)
        if self.in_message_text:
            self._message_text.append(data)

    def _finish_message(self) -> None:
        assert self.current is not None
        nt_text = " ".join("".join(self._nt_text).split())
        match = DATE_RE.search(nt_text)
        self.current["timestamp"] = match.group(1) if match else ""
        self.current["sender_display"] = " ".join("".join(self._sender_text).split())
        self.current["text"] = "".join(self._message_text).strip()
        self.current["media_paths"] = list(dict.fromkeys(self.current["media_paths"]))
        self.current["links"] = list(dict.fromkeys(self.current["links"]))
        self.messages.append(self.current)
        self.in_message = False
        self.current = None
        self.nt_depth = None
        self.content_depth = None
        self.in_sender = False
        self.in_message_text = False


def parse_fragments(fragments: Iterable[str]) -> list[dict]:
    parser = MessageHTMLParser()
    for fragment in fragments:
        parser.feed(fragment)
    parser.close()
    return parser.messages


def js_page_number(path: Path) -> int:
    match = PAGE_RE.search(path.name)
    return int(match.group(1)) if match else 0


def iter_conversation_messages(html_path: Path) -> Iterable[dict]:
    seen: set[tuple[str, str, str]] = set()
    main_messages = parse_fragments([html_path.read_text(encoding="utf-8", errors="replace")])
    for message in main_messages:
        key = (message["message_id"], message["timestamp"], message["text"])
        if key not in seen:
            seen.add(key)
            yield message

    data_dir = html_path.with_name(f"{html_path.stem}_files") / "Data"
    if not data_dir.is_dir():
        return
    for js_path in sorted(data_dir.glob("msg-*.js"), key=js_page_number):
        source = js_path.read_text(encoding="utf-8", errors="replace")
        match = ARRAY_RE.search(source)
        if not match:
            continue
        try:
            fragments = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        for message in parse_fragments(fragments):
            key = (message["message_id"], message["timestamp"], message["text"])
            if key not in seen:
                seen.add(key)
                yield message


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="WechatExporter account directory")
    parser.add_argument("output", type=Path, help="Structured export directory")
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    account = source.name

    html_files = sorted(
        (p for p in source.glob("*.html") if p.name != "index.html"),
        key=lambda p: p.name.casefold(),
    )

    fields = [
        "account",
        "conversation",
        "message_id",
        "timestamp",
        "direction",
        "sender_display",
        "sender_id",
        "message_type",
        "text",
        "media_paths",
        "links",
        "source_html",
    ]

    total = 0
    type_counts: Counter[str] = Counter()
    direction_counts: Counter[str] = Counter()
    conversations: list[dict] = []

    json_path = output / "messages.json"
    csv_path = output / "messages.csv"
    with json_path.open("w", encoding="utf-8") as json_file, csv_path.open(
        "w", encoding="utf-8-sig", newline=""
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        json_file.write("[\n")
        first_json = True

        for html_path in html_files:
            conversation = html_path.stem
            count = 0
            first_timestamp = ""
            last_timestamp = ""
            for message in iter_conversation_messages(html_path):
                record = {
                    "account": account,
                    "conversation": conversation,
                    **message,
                    "source_html": html_path.name,
                }
                if not first_json:
                    json_file.write(",\n")
                json.dump(record, json_file, ensure_ascii=False, separators=(",", ":"))
                first_json = False

                csv_record = dict(record)
                csv_record["media_paths"] = json.dumps(record["media_paths"], ensure_ascii=False)
                csv_record["links"] = json.dumps(record["links"], ensure_ascii=False)
                writer.writerow(csv_record)

                timestamp = record["timestamp"]
                if timestamp:
                    first_timestamp = first_timestamp or timestamp
                    last_timestamp = timestamp
                count += 1
                total += 1
                type_counts[str(record["message_type"])] += 1
                direction_counts[record["direction"]] += 1

            conversations.append(
                {
                    "conversation": conversation,
                    "message_count": count,
                    "first_timestamp": first_timestamp,
                    "last_timestamp": last_timestamp,
                    "html_file": html_path.name,
                }
            )

        json_file.write("\n]\n")

    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "account": account,
        "source": str(source),
        "conversation_count": len(html_files),
        "message_count": total,
        "message_type_counts": dict(type_counts.most_common()),
        "direction_counts": dict(direction_counts),
        "files": {
            "html_index": str(source.parent / "index.html"),
            "account_index": str(source / "index.html"),
            "json": str(json_path),
            "csv": str(csv_path),
        },
        "conversations": conversations,
    }
    (output / "export_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"conversations": len(html_files), "messages": total}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
