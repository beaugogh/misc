#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import html
import re
import time
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

from list_venue_papers import DEFAULT_YEAR, clean_text, configured_output_dir, fetch


class MarkdownHTMLParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.parts = []
        self.images = []
        self._skip = 0
        self._link = None
        self._heading = None
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self._skip += 1
            return
        if self._skip:
            return
        if tag in {"h1", "h2", "h3"}:
            self._heading = tag
            self._buffer = []
        elif tag == "a":
            self._link = attrs.get("href")
            self._buffer = []
        elif tag == "img":
            src = attrs.get("src")
            if src:
                src = urllib.parse.urljoin(self.base_url, src)
                alt = clean_text(attrs.get("alt", "Image"))
                self.images.append(src)
                self.parts.append(f"![{alt}]({src})\n\nAI-readable visual equivalent, added: Image from the original page. Detailed visual content was not available from HTML alone.")
        elif tag in {"p", "div", "section", "article", "li", "br"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        data = clean_text(data)
        if not data:
            return
        if self._heading or self._link:
            self._buffer.append(data)
        else:
            self.parts.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"script", "style", "noscript"} and self._skip:
            self._skip -= 1
            return
        if self._skip:
            return
        if self._heading == tag:
            level = {"h1": "#", "h2": "##", "h3": "###"}[tag]
            text = clean_text(" ".join(self._buffer))
            if text:
                self.parts.append(f"\n\n{level} {text}\n")
            self._heading = None
            self._buffer = []
        elif tag == "a" and self._link is not None:
            text = clean_text(" ".join(self._buffer))
            href = urllib.parse.urljoin(self.base_url, self._link)
            if text:
                self.parts.append(f"[{text}]({href})")
            self._link = None
            self._buffer = []


def slugify(value):
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-")[:120] or "paper"


def page_to_markdown(url, title, venue, year):
    source = fetch(url)
    parser = MarkdownHTMLParser(url)
    parser.feed(source)
    body = clean_text("\n".join(parser.parts))
    body = re.sub(r"\n{3,}", "\n\n", body)
    escaped_title = title.replace('"', '\\"')
    frontmatter = [
        "---",
        f'title: "{escaped_title}"',
        f"source_url: {url}",
        f"venue: {venue}",
        f"year: {year}",
        f"retrieved_date: {dt.date.today().isoformat()}",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + body + "\n"


def parse_args():
    default_output = configured_output_dir()
    parser = argparse.ArgumentParser(description="Harvest oral paper pages from an oral-only manifest.")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, default=default_output / "harvested")
    parser.add_argument("--venue", action="append", help="Limit to one or more venues.")
    parser.add_argument("--limit", type=int, help="Maximum number of ready rows to harvest.")
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    manifest = args.manifest or configured_output_dir() / f"ai-venue-oral-papers-{args.year}.csv"
    rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
    harvested = 0
    skipped = 0
    for row in rows:
        if args.venue and row["venue"] not in args.venue:
            continue
        if row.get("status") != "ready" or not row.get("paper_page_url"):
            skipped += 1
            continue
        if args.limit is not None and harvested >= args.limit:
            break
        venue_dir = args.output_dir / str(args.year) / row["venue"].lower()
        venue_dir.mkdir(parents=True, exist_ok=True)
        path = venue_dir / f"{slugify(row['title'])}.md"
        if path.exists() and not args.overwrite:
            skipped += 1
            continue
        markdown = page_to_markdown(row["paper_page_url"], row["title"], row["venue"], row["data_year"])
        path.write_text(markdown, encoding="utf-8")
        harvested += 1
        print(f"harvested: {path}")
        if args.sleep:
            time.sleep(args.sleep)
    print(f"Harvested {harvested}; skipped {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
