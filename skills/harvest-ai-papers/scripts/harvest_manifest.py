#!/usr/bin/env python3
import argparse
import base64
import csv
import datetime as dt
import mimetypes
import re
import time
import urllib.parse
from pathlib import Path

from list_venue_papers import DEFAULT_YEAR, clean_text, configured_output_dir, fetch, fetch_bytes


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
        links.append((urllib.parse.urljoin(base_url, href), clean_text(re.sub(r"<[^>]+>", " ", text))))
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


def normalize_pdf_text(text):
    lines = []
    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def markdownize_pdf_text(text, allow_numbered_headings=False):
    section_re = re.compile(
        r"^(abstract|introduction|related work|background|method|methods|approach|experiments?|results?|discussion|limitations?|conclusion|acknowledg(e)?ments?|references|bibliography|appendix|supplementary material)$",
        re.I,
    )
    numbered_section_re = re.compile(r"^(\d+(\.\d+)*)\.?\s+[A-Z][A-Za-z0-9 ,:;()/-]{2,120}$")
    out = []
    current_paragraph = []
    saw_abstract = allow_numbered_headings
    for line in normalize_pdf_text(text).splitlines():
        explicit_section = section_re.match(line)
        if explicit_section and line.lower() == "abstract":
            saw_abstract = True
        numbered_match = numbered_section_re.match(line)
        plausible_numbered_heading = False
        if numbered_match:
            first_number = int(numbered_match.group(1).split(".")[0])
            plausible_numbered_heading = first_number <= 50
        is_heading = explicit_section or (saw_abstract and plausible_numbered_heading)
        if is_heading:
            if current_paragraph:
                out.append(" ".join(current_paragraph))
                current_paragraph = []
            out.extend(["", f"## {line}", ""])
        else:
            current_paragraph.append(line)
    if current_paragraph:
        out.append(" ".join(current_paragraph))
    return "\n".join(out).strip(), saw_abstract


def validate_whole_paper(markdown, min_words):
    word_count = len(re.findall(r"\b\w+\b", markdown))
    if word_count < min_words:
        raise RuntimeError(f"harvested paper is too short: {word_count} words, expected at least {min_words}")
    if not re.search(r"\b(references|bibliography)\b", markdown, flags=re.I):
        raise RuntimeError("harvested paper is missing a references/bibliography section")


def pdf_to_markdown(pdf_url, row, output_path, min_words, min_figure_pixels):
    fitz = require_fitz()
    pdf_bytes = fetch_bytes(pdf_url)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    figure_dir = output_path.with_suffix("")
    figure_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    allow_numbered_headings = False
    seen_xrefs = set()
    for page_index, page in enumerate(doc, start=1):
        text, allow_numbered_headings = markdownize_pdf_text(
            page.get_text("text", sort=True) or "",
            allow_numbered_headings=allow_numbered_headings,
        )
        if text:
            parts.append(f"\n\n<!-- Page {page_index} -->\n\n{text}")
        for image_index, image in enumerate(page.get_images(full=True), start=1):
            xref = image[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            extracted = doc.extract_image(xref)
            image_bytes = extracted.get("image", b"")
            extension = extracted.get("ext", "png")
            width = int(extracted.get("width", 0) or 0)
            height = int(extracted.get("height", 0) or 0)
            if not image_bytes or width * height < min_figure_pixels:
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
    markdown = "\n".join(frontmatter) + f"# {row.get('title') or 'Untitled paper'}\n\n" + "\n".join(parts).strip() + "\n"
    validate_whole_paper(markdown, min_words)
    return markdown


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
    parser.add_argument("--min-words", type=int, default=3000, help="Minimum words required before writing a harvested paper.")
    parser.add_argument(
        "--min-figure-pixels",
        type=int,
        default=40000,
        help="Minimum extracted image area to keep as an SVG figure asset.",
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
            source = fetch(row["paper_page_url"])
            pdf_url = row.get("pdf_url") or discover_paper_pdf(source, row["paper_page_url"])
            if not pdf_url:
                skipped += 1
                print(f"skipped-no-paper-pdf: {row['paper_page_url']}")
                continue
            markdown = pdf_to_markdown(pdf_url, row, path, args.min_words, args.min_figure_pixels)
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
