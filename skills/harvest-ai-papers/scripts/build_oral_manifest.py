#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import re
import sys
import urllib.parse
from io import BytesIO
from pathlib import Path

from list_venue_papers import (
    DEFAULT_YEAR,
    SKILL_DIR,
    aaai_main_oral_pdf_url,
    absolutize,
    clean_text,
    configured_output_dir,
    fetch,
    fetch_bytes,
)


HOSTS = {
    "NeurIPS": "neurips.cc",
    "ICML": "icml.cc",
    "ICLR": "iclr.cc",
}


FIELDS = [
    "year",
    "data_year",
    "venue",
    "presentation_type",
    "paper_id",
    "title",
    "authors",
    "paper_page_url",
    "pdf_url",
    "source_url",
    "status",
    "notes",
]


def current_neurips_data_year(year):
    neurips_start = dt.date(year, 12, 6)
    if year == dt.date.today().year and dt.date.today() < neurips_start:
        return year - 1
    return year


def strip_tags(value):
    return clean_text(re.sub(r"<[^>]+>", " ", value or ""))


def virtual_oral_rows(venue, year):
    data_year = current_neurips_data_year(year) if venue == "NeurIPS" else year
    source_url = f"https://{HOSTS[venue]}/virtual/{data_year}/events/oral"
    source = fetch(source_url)
    rows = []
    seen = set()
    pattern = rf'href="([^"]*/virtual/{data_year}/oral/[^"]+)">(.*?)</a>'
    for href, title_html in re.findall(pattern, source, flags=re.I | re.S):
        url = absolutize(href, source_url)
        if url in seen:
            continue
        seen.add(url)
        title = strip_tags(title_html)
        if not title:
            continue
        paper_id = urllib.parse.urlparse(url).path.rstrip("/").split("/")[-1]
        rows.append(
            {
                "year": year,
                "data_year": data_year,
                "venue": venue,
                "presentation_type": "Oral",
                "paper_id": paper_id,
                "title": title,
                "authors": "",
                "paper_page_url": url,
                "pdf_url": "",
                "source_url": source_url,
                "status": "needs_pdf_url",
                "notes": "Official virtual oral event page; paper PDF must be resolved before harvesting.",
            }
        )
    return rows


def aaai_pdf_text(pdf_bytes):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "pypdf is required for AAAI oral manifests; install it or set PYTHONPATH to a target install."
        ) from exc

    return "\n".join(
        page.extract_text(extraction_mode="layout") or ""
        for page in PdfReader(BytesIO(pdf_bytes)).pages
    )


def join_words_by_line(words):
    lines = []
    for word in sorted(words, key=lambda item: (round(item[1] / 3) * 3, item[0])):
        if not lines or abs(lines[-1][0] - word[1]) > 3:
            lines.append([word[1], [word[4]]])
        else:
            lines[-1][1].append(word[4])
    return clean_text(" ".join(" ".join(line_words) for _y, line_words in lines))


def aaai_oral_rows_from_coordinates(year, pdf_url, page_url, pdf_bytes):
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required for accurate AAAI oral schedule extraction; "
            "install it or set PYTHONPATH to a target install."
        ) from exc

    rows = []
    seen = set()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        words = page.get_text("words") or []
        ids = []
        for word in words:
            x0, y0, x1, _y1, text = word[:5]
            if 135 <= x0 <= 185 and re.fullmatch(r"\d{2,6}", text):
                ids.append((y0, x0, text))
        ids = sorted(ids)
        for index, (y0, _x0, paper_id) in enumerate(ids):
            if paper_id in seen:
                continue
            seen.add(paper_id)
            next_y = ids[index + 1][0] if index + 1 < len(ids) else page.rect.height
            title_words = [word for word in words if 188 <= word[0] < 378 and y0 - 1 <= word[1] < next_y - 1]
            author_words = [word for word in words if word[0] >= 378 and y0 - 1 <= word[1] < next_y - 1]
            title = join_words_by_line(title_words)
            authors = join_words_by_line(author_words)
            if not title:
                continue
            rows.append(
                {
                    "year": year,
                    "data_year": year,
                    "venue": "AAAI",
                    "presentation_type": "Oral",
                    "paper_id": paper_id,
                    "title": title,
                    "authors": authors,
                    "paper_page_url": "",
                    "pdf_url": "",
                    "source_url": page_url or pdf_url,
                    "status": "needs_paper_url",
                    "notes": "Official AAAI Main Track Oral Talks PDF; schedule row captured, paper URL still needs mapping.",
                }
            )
    return rows


def aaai_oral_rows(year):
    pdf_url, page_url = aaai_main_oral_pdf_url(year)
    pdf_bytes = fetch_bytes(pdf_url)
    try:
        rows = aaai_oral_rows_from_coordinates(year, pdf_url, page_url, pdf_bytes)
        if rows:
            return rows
    except Exception:
        pass
    text = aaai_pdf_text(pdf_bytes)
    rows = []
    seen = set()
    row_re = re.compile(r"^.*?\s{2,}(?P<paper_id>\d{2,6})\s{2,}", re.M)
    for match in row_re.finditer(text):
        line = match.group(0)
        if "Paper ID" in line:
            continue
        paper_id = match.group("paper_id")
        if paper_id in seen:
            continue
        seen.add(paper_id)
        full_line = text[match.start() : text.find("\n", match.start())]
        title = clean_text(full_line[match.end() - match.start() : 125])
        rows.append(
            {
                "year": year,
                "data_year": year,
                "venue": "AAAI",
                "presentation_type": "Oral",
                "paper_id": paper_id,
                "title": title,
                "authors": "",
                "paper_page_url": "",
                "pdf_url": "",
                "source_url": page_url or pdf_url,
                "status": "needs_paper_url",
                "notes": "Official AAAI Main Track Oral Talks PDF; schedule row captured, paper URL still needs mapping.",
            }
        )
    return rows


def write_manifest(rows, output_dir, year):
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"ai-venue-oral-papers-{year}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def parse_args():
    parser = argparse.ArgumentParser(description="Build an oral-only paper manifest for harvesting.")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=configured_output_dir(),
        help="Output directory, defaulting to config.yaml output relative to the skill directory.",
    )
    parser.add_argument(
        "--venue",
        choices=["NeurIPS", "ICML", "ICLR", "AAAI"],
        action="append",
        help="Limit to one or more venues. Defaults to all configured oral venues.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    venues = args.venue or ["NeurIPS", "ICML", "ICLR", "AAAI"]
    rows = []
    failures = []
    for venue in venues:
        try:
            venue_rows = aaai_oral_rows(args.year) if venue == "AAAI" else virtual_oral_rows(venue, args.year)
            rows.extend(venue_rows)
            ready = sum(1 for row in venue_rows if row["status"] == "ready")
            print(f"{venue}: oral={len(venue_rows)}, ready_for_harvest={ready}")
        except Exception as exc:
            failures.append((venue, str(exc)))
            print(f"{venue}: failed: {exc}", file=sys.stderr)
    path = write_manifest(rows, args.output_dir, args.year)
    print(f"Wrote {path}")
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
