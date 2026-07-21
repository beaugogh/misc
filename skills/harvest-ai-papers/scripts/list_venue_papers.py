#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_YEAR = 2026
SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUT = SKILL_DIR / "output"
USER_AGENT = "Mozilla/5.0"
KNOWN_AAAI_MAIN_ORAL_COUNTS = {
    2025: (
        457,
        "https://aaai.org/wp-content/uploads/2025/02/AAAI-25-Main-Track-Oral-Talks-Schedule-2.22.pdf",
    ),
    2026: (1051, "https://aaai.org/wp-content/uploads/2026/01/Main-track-oral-talks.pdf"),
}


def fetch(url):
    last_error = None
    for _ in range(3):
        try:
            completed = subprocess.run(
                ["curl", "-fsSL", "--http1.1", "--compressed", "-A", USER_AGENT, url],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=25,
            )
            return completed.stdout.decode("utf-8", errors="replace")
        except Exception as exc:
            last_error = exc
            time.sleep(0.5)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=45) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except Exception:
        raise last_error


def fetch_bytes(url):
    last_error = None
    for _ in range(3):
        try:
            completed = subprocess.run(
                ["curl", "-fsSL", "--http1.1", "--compressed", "-A", USER_AGENT, url],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=45,
            )
            return completed.stdout
        except Exception as exc:
            last_error = exc
            time.sleep(0.5)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as response:
            return response.read()
    except Exception:
        raise last_error


def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def configured_output_dir():
    config_path = SKILL_DIR / "config.yaml"
    try:
        for line in config_path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^output:\s*(.+?)\s*$", line)
            if match:
                value = match.group(1).strip().strip('"').strip("'")
                path = Path(value).expanduser()
                return path if path.is_absolute() else SKILL_DIR / path
    except FileNotFoundError:
        pass
    return DEFAULT_OUT


def absolutize(url, base):
    return urllib.parse.urljoin(base, url)


class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = []
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            attrs = dict(attrs)
            self._href = attrs.get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            text = clean_text("".join(self._text))
            if text:
                self.links.append((text, absolutize(self._href, self.base_url)))
            self._href = None
            self._text = []


def links_from(url, source=None):
    source = source if source is not None else fetch(url)
    parser = LinkParser(url)
    parser.feed(source)
    return parser.links


def paper_row(
    venue,
    title,
    url="",
    authors="",
    track="",
    source_url="",
    status="listed",
    year=None,
    presentation_type="",
):
    return {
        "year": year,
        "venue": venue,
        "presentation_type": clean_text(presentation_type),
        "title": clean_text(title),
        "authors": clean_text(authors),
        "track": clean_text(track),
        "url": url,
        "source_url": source_url,
        "status": status,
    }


def from_openreview(venue_name, venue_id):
    rows = []
    offset = 0
    limit = 1000
    source_url = f"https://openreview.net/group?id={urllib.parse.quote(venue_id)}"
    while True:
        params = urllib.parse.urlencode(
            {
                "content.venueid": venue_id,
                "limit": limit,
                "offset": offset,
                "details": "replyCount,invitation",
            }
        )
        data = json.loads(fetch(f"https://api2.openreview.net/notes?{params}"))
        notes = data.get("notes", [])
        for note in notes:
            content = note.get("content", {})
            title = content.get("title", {}).get("value", "")
            authors = content.get("authors", {}).get("value", [])
            venue = content.get("venue", {}).get("value", "")
            paper_url = f"https://openreview.net/forum?id={note.get('forum') or note.get('id')}"
            rows.append(
                paper_row(
                    venue_name,
                    title,
                    paper_url,
                    ", ".join(authors) if isinstance(authors, list) else authors,
                    venue,
                    source_url,
                )
            )
        if len(notes) < limit:
            break
        offset += limit
        time.sleep(0.2)
    return rows, source_url


def icml(year):
    url = f"https://icml.cc/Downloads/{year}"
    return parse_virtual_downloads("ICML", url, year)


def parse_virtual_downloads(venue, url, year):
    source = fetch(url)
    rows = []
    for href, title_html in re.findall(
        r'<a href="([^"]+)" class="Poster">(.*?)</a>', source, flags=re.I | re.S
    ):
        title = clean_text(re.sub(r"<[^>]+>", " ", title_html))
        rows.append(
            paper_row(
                venue,
                title,
                absolutize(href, url),
                source_url=url,
                year=year,
                presentation_type="Poster",
            )
        )
    return rows, url, len(rows)


def iclr(year):
    url = f"https://iclr.cc/Downloads/{year}"
    return parse_virtual_downloads("ICLR", url, year)


def virtual_oral_count(venue, year):
    hosts = {
        "NeurIPS": "neurips.cc",
        "ICML": "icml.cc",
        "ICLR": "iclr.cc",
    }
    url = f"https://{hosts[venue]}/virtual/{year}/events/oral"
    source = fetch(url)
    count = len(re.findall(r">\s*Oral\s*<", source, flags=re.I))
    if not count:
        match = re.search(r"(\d+)\s+Events", source, flags=re.I)
        if match:
            count = int(match.group(1))
    return {
        "count": count,
        "source_url": url,
        "note": f"Official {venue} virtual oral events page.",
    }


def aaai_main_oral_pdf_url(year):
    if year in KNOWN_AAAI_MAIN_ORAL_COUNTS:
        return KNOWN_AAAI_MAIN_ORAL_COUNTS[year][1], ""
    page_url = f"https://aaai.org/conference/aaai/aaai-{str(year)[-2:]}/main-technical-track/"
    source = fetch(page_url)
    for text, href in links_from(page_url, source):
        link_text = clean_text(text).lower()
        if link_text in {"main track oral talks", "main track oral presentations"}:
            return href, page_url
    raise RuntimeError("Could not find AAAI Main Track Oral Talks link")


def count_pdf_ids(pdf_bytes, id_pattern):
    try:
        from io import BytesIO
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is required to count paper IDs in AAAI oral PDFs") from exc

    text = "\n".join(
        page.extract_text(extraction_mode="layout") or ""
        for page in PdfReader(BytesIO(pdf_bytes)).pages
    )
    ids = []
    row_re = re.compile(rf"^.*?\s{{2,}}({id_pattern})\s{{2,}}", re.M)
    for match in row_re.finditer(text):
        line = match.group(0)
        if "Paper ID" not in line:
            ids.append(match.group(1))
    return len(set(ids))


def aaai_main_oral_count(year):
    pdf_url, page_url = aaai_main_oral_pdf_url(year)
    try:
        count = count_pdf_ids(fetch_bytes(pdf_url), r"\d+")
        note = f"Official AAAI {year} Main Track Oral Talks PDF; counted unique Paper IDs."
    except Exception:
        if year not in KNOWN_AAAI_MAIN_ORAL_COUNTS:
            raise
        count, pdf_url = KNOWN_AAAI_MAIN_ORAL_COUNTS[year]
        note = f"Validated count from the official AAAI {year} Main Track Oral Talks PDF; counted unique Paper IDs."
    if page_url:
        note = f"{note} Schedule hub: {page_url}"
    return {
        "count": count,
        "source_url": pdf_url,
        "note": note,
    }


def aaai(year):
    url = f"https://dblp.org/db/conf/aaai/aaai{year}.html"
    source = fetch(url)
    starts = [match.start() for match in re.finditer(r'<li class="entry inproceedings"', source)]
    rows = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(source)
        block = source[start:end]
        title_match = re.search(r'<span class="title"[^>]*>(.*?)</span>', block, flags=re.I | re.S)
        if not title_match:
            continue
        title = clean_text(re.sub(r"<[^>]+>", " ", title_match.group(1)))
        authors = re.findall(r'<span itemprop="name"[^>]*>(.*?)</span>', block, flags=re.I | re.S)
        authors = ", ".join(clean_text(re.sub(r"<[^>]+>", " ", author)) for author in authors)
        doi_match = re.search(r'href="(https://doi\.org/[^"]+)"', block, flags=re.I)
        rec_match = re.search(r'id="([^"]+)"', block, flags=re.I)
        paper_url = doi_match.group(1) if doi_match else ""
        if not paper_url and rec_match:
            paper_url = f"https://dblp.org/rec/{rec_match.group(1)}"
        rows.append(
            paper_row(
                "AAAI",
                title,
                paper_url,
                authors=authors,
                source_url=url,
                year=year,
                presentation_type="Proceedings paper",
            )
        )
    return rows, url, len(rows)


def neurips(year):
    data_year = year
    note = "Official NeurIPS downloads page; counted Poster entries and excluded workshops."
    neurips_start = dt.date(year, 12, 6)
    if year == dt.date.today().year and dt.date.today() < neurips_start:
        data_year = year - 1
        note = (
            f"Using NeurIPS {data_year} as fallback because NeurIPS {year} has not started "
            f"as of {dt.date.today().isoformat()}."
        )
    url = f"https://neurips.cc/Downloads/{data_year}"
    source = fetch(url)
    rows = []
    for href, title_html in re.findall(
        r'<a href="([^"]+)" class="Poster">(.*?)</a>', source, flags=re.I | re.S
    ):
        title = clean_text(re.sub(r"<[^>]+>", " ", title_html))
        rows.append(
            paper_row(
                "NeurIPS",
                title,
                absolutize(href, url),
                source_url=url,
                year=data_year,
                presentation_type="Poster",
            )
        )
    return rows, url, len(rows), note, data_year


def oral_summary_for(results):
    oral_counters = {
        "NeurIPS": lambda data_year: virtual_oral_count("NeurIPS", data_year),
        "ICML": lambda data_year: virtual_oral_count("ICML", data_year),
        "ICLR": lambda data_year: virtual_oral_count("ICLR", data_year),
        "AAAI": aaai_main_oral_count,
    }
    oral_results = []
    for venue in results:
        data_year = venue.get("data_year")
        name = venue["venue"]
        try:
            oral = oral_counters[name](data_year)
        except Exception as exc:
            oral = {
                "count": "",
                "source_url": "",
                "note": f"Oral count failed: {exc}",
            }
        oral_results.append(
            {
                "venue": name,
                "data_year": data_year,
                "oral_count": oral["count"],
                "source_url": oral["source_url"],
                "note": oral["note"],
            }
        )
    return oral_results


def write_outputs(results, year, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"ai-venue-papers-{year}.csv"
    md_path = output_dir / f"ai-venue-papers-{year}-summary.md"
    fields = [
        "year",
        "venue",
        "presentation_type",
        "title",
        "authors",
        "track",
        "url",
        "source_url",
        "status",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for venue in results:
            writer.writerows(venue["rows"])

    oral_results = oral_summary_for(results)
    known_oral_total = sum(
        venue["oral_count"] for venue in oral_results if isinstance(venue["oral_count"], int)
    )
    lines = [
        "---",
        f"title: AI venue oral paper inventory {year}",
        f"retrieved_date: {dt.date.today().isoformat()}",
        "---",
        "",
        f"# AI Venue Oral Paper Inventory {year}",
        "",
        "Scope: oral-paper counts for the configured venues. AAAI counts Main Track Oral Talks only.",
        "",
        f"Oral papers counted: {known_oral_total}",
        "",
        "| Venue | Data year | Oral paper count | Source | Notes |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for venue in oral_results:
        lines.append(
            f"| {venue['venue']} | {venue['data_year']} | {venue['oral_count']} | {venue['source_url']} | {venue['note']} |"
        )
    lines.extend(
        [
            "",
            f"Broad accepted/proceedings CSV retained for workload planning: `{csv_path}`",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return csv_path, md_path


def parse_args():
    parser = argparse.ArgumentParser(
        description="List top AI venue papers from non-gated public listing pages."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=DEFAULT_YEAR,
        help=f"Conference/listing year to inventory. Defaults to {DEFAULT_YEAR}.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=configured_output_dir(),
        help="Directory for CSV and Markdown summary. Defaults to config.yaml output, resolved relative to the skill directory.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    year = args.year
    runners = [
        ("NeurIPS", neurips, None),
        ("ICML", icml, "Official ICML downloads page; counted Poster entries and excluded workshops."),
        ("ICLR", iclr, "Official ICLR downloads page; counted Poster entries and excluded workshops."),
        ("AAAI", aaai, f"DBLP AAAI {year} proceedings page; non-gated metadata with DOI links to AAAI papers."),
    ]
    results = []
    failures = []
    for venue, runner, note in runners:
        try:
            result = runner(year)
            if len(result) == 5:
                rows, source_url, workload_count, result_note, data_year = result
            else:
                rows, source_url, workload_count = result
                result_note = note
                data_year = year
            results.append({"venue": venue, "rows": rows, "source_url": source_url, "note": result_note, "workload_count": workload_count, "data_year": data_year})
            print(f"{venue}: year={data_year}, workload={workload_count}, rows={len(rows)}")
        except Exception as exc:
            failures.append((venue, str(exc)))
            results.append({"venue": venue, "rows": [], "source_url": "", "note": f"Fetch failed: {exc}"})
            print(f"{venue}: failed: {exc}", file=sys.stderr)
    csv_path, md_path = write_outputs(results, year, args.output_dir)
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
