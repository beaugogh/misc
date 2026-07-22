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


def strip_pdf_control_chars(text):
    return "".join(
        char if char in "\n\t" or (ord(char) >= 32 and not 0x7F <= ord(char) <= 0x9F) else " "
        for char in text
    )


def normalize_pdf_line(text):
    text = strip_pdf_control_chars(text)
    return re.sub(r"[ \t]+", " ", text).strip()


def join_pdf_lines(lines):
    paragraph = ""
    for raw_line in lines:
        line = normalize_pdf_line(raw_line)
        if not line:
            continue
        if paragraph.endswith("-") and re.match(r"^[a-z]", line):
            paragraph = paragraph[:-1] + line
        elif paragraph:
            paragraph += " " + line
        else:
            paragraph = line
    paragraph = re.sub(r"\s+([,.;:!?])", r"\1", paragraph)
    paragraph = re.sub(r"\(\s+", "(", paragraph)
    paragraph = re.sub(r"\s+\)", ")", paragraph)
    return paragraph.strip()


def should_skip_block(text, page_index):
    compact = normalize_pdf_line(text)
    if not compact:
        return True
    if compact == str(page_index):
        return True
    if re.match(r"^(arXiv:\d{4}\.\d+v\d+|\[\w+\.[A-Z]{2}\])$", compact):
        return True
    if re.match(r"^\d{4}$", compact):
        return True
    return False


def append_readable_block(out, paragraph):
    if (
        out
        and paragraph[:1].islower()
        and not out[-1].startswith("## ")
        and not out[-1].startswith("**Figure ")
        and not out[-1].startswith("**Fig. ")
        and not out[-1].startswith("**Table ")
        and not re.search(r"[.!?:;)\]}]$", out[-1])
    ):
        out[-1] = f"{out[-1]} {paragraph}"
    else:
        out.append(paragraph)


SECTION_HEADINGS = [
    "Abstract",
    "Introduction",
    "Related Work",
    "Related Literature",
    "Background",
    "Preliminaries",
    "Problem Formulation",
    "Methodology",
    "Method",
    "Methods",
    "Approach",
    "Model",
    "Algorithm",
    "Experiments",
    "Experiment",
    "Experimental Setup",
    "Experimental Results and Analysis",
    "Results",
    "Equilibrium Existence",
    "Evaluation",
    "Analysis",
    "Discussion",
    "Limitations",
    "Conclusion",
    "Conclusion and Future Work",
    "Acknowledgements",
    "Acknowledgments",
    "References",
    "Bibliography",
    "Appendix",
    "Supplementary Material",
]


def split_inline_section_heading(paragraph):
    for heading in sorted(SECTION_HEADINGS, key=len, reverse=True):
        if paragraph == heading:
            return f"## {heading}"
        if paragraph.startswith(f"{heading} "):
            rest = paragraph[len(heading) + 1 :].strip()
            if rest:
                return f"## {heading}\n\n{rest}"
    numbered = re.match(r"^(\d+(?:\.\d+)*)\.?\s+([A-Z][A-Za-z0-9 ,:;()/-]{2,120})(?:\s{2,}|\s(?=[A-Z][a-z]))(.+)$", paragraph)
    if numbered:
        heading = f"{numbered.group(1)} {numbered.group(2).strip()}"
        rest = numbered.group(3).strip()
        return f"## {heading}\n\n{rest}" if rest else f"## {heading}"
    return paragraph


def normalize_markdown_quality(markdown):
    markdown = markdown.replace("```", "`\\`\\`\\`")
    normalized_lines = []
    seen_h1 = False
    in_frontmatter = False
    for index, line in enumerate(markdown.splitlines()):
        if index == 0 and line == "---":
            in_frontmatter = True
            normalized_lines.append(line)
            continue
        if in_frontmatter:
            normalized_lines.append(line)
            if line == "---":
                in_frontmatter = False
            continue
        if line.startswith("# "):
            if seen_h1:
                normalized_lines.append(f"## {line[2:].strip()}")
            else:
                seen_h1 = True
                normalized_lines.append(line)
        else:
            normalized_lines.append(line)

    paragraphs = re.split(r"\n{2,}", "\n".join(normalized_lines))
    repaired = []
    for paragraph in paragraphs:
        stripped = paragraph.strip()
        if not stripped:
            continue
        if stripped.startswith(("---", "#", "<!--", "![", "AI-readable visual equivalent")):
            repaired.append(stripped)
        else:
            repaired.append(split_inline_section_heading(stripped))
    return "\n\n".join(repaired).rstrip() + "\n"


def markdownize_pdf_blocks(page, page_index, allow_numbered_headings=False):
    section_re = re.compile(
        r"^(abstract|introduction|related work|background|method|methods|approach|experiments?|results?|discussion|limitations?|conclusion|acknowledg(e)?ments?|references|bibliography|appendix|supplementary material)$",
        re.I,
    )
    numbered_section_re = re.compile(r"^(\d+(\.\d+)*)\.?\s+[A-Z][A-Za-z0-9 ,:;()/-]{2,120}$")
    out = []
    saw_abstract = allow_numbered_headings
    blocks = page.get_text("blocks", sort=False) or []
    for block in blocks:
        if len(block) < 7 or block[6] != 0:
            continue
        raw_text = block[4]
        if should_skip_block(raw_text, page_index):
            continue
        lines = [normalize_pdf_line(line) for line in raw_text.splitlines()]
        lines = [line for line in lines if line and not should_skip_block(line, page_index)]
        if not lines:
            continue
        paragraph = join_pdf_lines(lines)
        if not paragraph:
            continue

        paragraph = split_inline_section_heading(paragraph)
        explicit_section = section_re.match(paragraph.removeprefix("## ").strip())
        if explicit_section and paragraph.lower() == "abstract":
            saw_abstract = True
        numbered_match = numbered_section_re.match(paragraph)
        plausible_numbered_heading = False
        if numbered_match:
            first_number = int(numbered_match.group(1).split(".")[0])
            plausible_numbered_heading = first_number <= 50
        is_heading = explicit_section or plausible_numbered_heading
        if is_heading:
            out.append(f"## {paragraph}")
        elif re.match(r"^(figure|fig\.|table)\s+\d+[:.]?\s+", paragraph, re.I):
            caption = re.sub(r"^(figure|fig\.|table)\s+(\d+)\s*[:.]?\s*", lambda m: f"**{m.group(1).title()} {m.group(2)}.** ", paragraph, flags=re.I)
            out.append(caption)
        else:
            append_readable_block(out, paragraph)
    return "\n\n".join(out).strip(), saw_abstract


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
        text, allow_numbered_headings = markdownize_pdf_blocks(
            page,
            page_index,
            allow_numbered_headings=allow_numbered_headings,
        )
        if text:
            parts.append(f"\n\n<!-- Page {page_index} -->\n\n{text}")
        for image_index, image in enumerate(page.get_images(full=True), start=1):
            xref = image[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            try:
                extracted = doc.extract_image(xref)
            except Exception as exc:
                print(f"skipped-figure: page {page_index} image {image_index} ({exc})")
                continue
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
    markdown = normalize_markdown_quality(markdown)
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
            pdf_url = row.get("pdf_url")
            if not pdf_url:
                source = fetch(row["paper_page_url"])
                pdf_url = discover_paper_pdf(source, row["paper_page_url"])
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
