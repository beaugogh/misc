#!/usr/bin/env python3
import argparse
import base64
import csv
import datetime as dt
import html
import mimetypes
import re
import time
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

from list_venue_papers import DEFAULT_YEAR, clean_text, configured_output_dir, fetch, fetch_bytes


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


def slugify(value, max_chars=80):
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-")[:max_chars].strip("-") or "paper"


def prefixed_filename(row, name_chars):
    year = row.get("data_year") or row.get("year")
    venue = (row.get("venue") or "venue").upper()
    title = slugify(row.get("title") or row.get("paper_id") or "paper", name_chars)
    return f"{year}-{venue}-{title}.md"


def links_from_html(source, base_url):
    links = []
    for href, text in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', source, flags=re.I | re.S):
        links.append((urllib.parse.urljoin(base_url, html.unescape(href)), clean_text(re.sub(r"<[^>]+>", " ", text))))
    return links


def openreview_pdf_url(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "openreview.net":
        return ""
    params = urllib.parse.parse_qs(parsed.query)
    paper_id = (params.get("id") or [""])[0]
    return f"https://openreview.net/pdf?id={paper_id}" if paper_id else ""


def discover_paper_pdf(source, base_url):
    links = links_from_html(source, base_url)
    for href, text in links:
        label = text.lower()
        href_lower = href.lower()
        if "slide" not in label and href_lower.endswith(".pdf") and any(word in label for word in ("paper", "pdf", "proceedings")):
            return href
    for href, _text in links:
        if "openreview.net/forum" in href:
            pdf_url = openreview_pdf_url(href)
            if pdf_url:
                return pdf_url
    for href, text in links:
        label = text.lower()
        if "slide" not in label and "presentation" not in label and href.lower().endswith(".pdf"):
            return href
    return ""


def require_fitz():
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required to harvest whole-paper PDFs and SVG figure assets. "
            "Install it with: python3 -m pip install --target /private/tmp/pymupdf pymupdf "
            "and run with PYTHONPATH=/private/tmp/pymupdf."
        ) from exc
    return fitz


def svg_wrap_image(image_bytes, extension, output_path):
    mime = mimetypes.types_map.get(f".{extension.lower()}", "image/png")
    encoded = base64.b64encode(image_bytes).decode("ascii")
    output_path.write_text(
        "\n".join(
            [
                '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 1 1">',
                f'  <image href="data:{mime};base64,{encoded}" width="1" height="1" preserveAspectRatio="xMidYMid meet"/>',
                "</svg>",
                "",
            ]
        ),
        encoding="utf-8",
    )


def pdf_to_markdown(pdf_url, row, output_path):
    fitz = require_fitz()
    pdf_bytes = fetch_bytes(pdf_url)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    figure_dir = output_path.with_suffix("")
    figure_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for page_index, page in enumerate(doc, start=1):
        text = clean_text(page.get_text("text") or "")
        if text:
            parts.append(f"\n\n## Page {page_index}\n\n{text}")
        for image_index, image in enumerate(page.get_images(full=True), start=1):
            xref = image[0]
            extracted = doc.extract_image(xref)
            image_bytes = extracted.get("image", b"")
            extension = extracted.get("ext", "png")
            if not image_bytes:
                continue
            figure_path = figure_dir / f"page-{page_index:03d}-figure-{image_index:02d}.svg"
            svg_wrap_image(image_bytes, extension, figure_path)
            relative = figure_path.relative_to(output_path.parent)
            parts.append(
                "\n\n"
                f"![Figure extracted from page {page_index}]({relative})\n\n"
                "AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. "
                "Use the surrounding page text and caption for interpretation."
            )
    frontmatter = [
        "---",
        f'title: "{(row.get("title") or "").replace(chr(34), chr(92) + chr(34))}"',
        f"source_url: {row.get('paper_page_url')}",
        f"paper_pdf_url: {pdf_url}",
        f"venue: {row.get('venue')}",
        f"year: {row.get('data_year') or row.get('year')}",
        f"retrieved_date: {dt.date.today().isoformat()}",
        "content_scope: whole paper PDF text with extracted SVG figure assets",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + "\n".join(parts).strip() + "\n"


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
    parser.add_argument("--limit", type=int, help="Maximum number of ready manifest rows to attempt.")
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--name-chars",
        type=int,
        default=80,
        help="Maximum characters from the paper title to include after YEAR-VENUE- in filenames.",
    )
    parser.add_argument(
        "--page-only",
        action="store_true",
        help="Harvest the conference page only. Default is whole-paper PDF harvesting.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    manifest = args.manifest or configured_output_dir() / f"ai-venue-oral-papers-{args.year}.csv"
    rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
    harvested = 0
    skipped = 0
    attempted = 0
    for row in rows:
        if args.venue and row["venue"] not in args.venue:
            continue
        if row.get("status") != "ready" or not row.get("paper_page_url"):
            skipped += 1
            continue
        if args.limit is not None and attempted >= args.limit:
            break
        attempted += 1
        venue_dir = args.output_dir / str(args.year) / row["venue"].lower()
        venue_dir.mkdir(parents=True, exist_ok=True)
        path = venue_dir / prefixed_filename(row, args.name_chars)
        if path.exists() and not args.overwrite:
            skipped += 1
            continue
        try:
            if args.page_only:
                markdown = page_to_markdown(row["paper_page_url"], row["title"], row["venue"], row["data_year"])
            else:
                source = fetch(row["paper_page_url"])
                pdf_url = row.get("pdf_url") or discover_paper_pdf(source, row["paper_page_url"])
                if not pdf_url:
                    skipped += 1
                    print(f"skipped-no-paper-pdf: {row['paper_page_url']}")
                    continue
                markdown = pdf_to_markdown(pdf_url, row, path)
        except Exception as exc:
            skipped += 1
            print(f"skipped-error: {row['paper_page_url']} ({exc})")
            continue
        path.write_text(markdown, encoding="utf-8")
        harvested += 1
        print(f"harvested: {path}")
        if args.sleep:
            time.sleep(args.sleep)
    print(f"Attempted {attempted}; harvested {harvested}; skipped {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
