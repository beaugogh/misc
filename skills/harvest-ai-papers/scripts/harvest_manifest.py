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


def svg_wrap_image(image_bytes, extension, output_path, width=1, height=1):
    mime = mimetypes.types_map.get(f".{extension.lower()}", "image/png")
    encoded = base64.b64encode(image_bytes).decode("ascii")
    width = max(int(width or 1), 1)
    height = max(int(height or 1), 1)
    output_path.write_text(
        "\n".join(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                f'  <image href="data:{mime};base64,{encoded}" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet"/>',
                "</svg>",
                "",
            ]
        ),
        encoding="utf-8",
    )


def svg_wrap_pixmap(pixmap, output_path):
    svg_wrap_image(pixmap.tobytes("png"), "png", output_path, pixmap.width, pixmap.height)


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


def truncate_text(text, max_chars=900):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "..."


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
        and "```" not in out[-1]
        and not re.search(r"[.!?:;)\]}]$", out[-1])
    ):
        out[-1] = f"{out[-1]} {paragraph}"
    else:
        out.append(paragraph)


GENERIC_VISUAL_NOTE = (
    "AI-readable visual equivalent, added: Figure extracted from the paper PDF and converted to an SVG wrapper asset. "
    "Use the surrounding page text and caption for interpretation."
)


MATH_CHARS_RE = re.compile(r"[=≈≃≅≤≥<>+\-*/×÷∑∏∫√∞∂∇∆∈∉∋⊂⊆⊃⊇∪∩∀∃¬∧∨→←↔⇒⇔±λθΘαβγδϵεημνξπρσΣτφΦψΨωΩ𝛼-𝜔𝐀-𝛀𝑨-𝝎𝟎-𝟗]")
MATH_LAYOUT_RE = re.compile(r"(\b[TKMN]\s+X\s+[a-z]=\d+\b|\$\$|\\frac|\\sum|\\begin\{|[A-Za-z]\s*[=≈]\s*[^.]+|[!\"#$%&]{3,})")
MATH_LEAD_IN_RE = re.compile(r"\b(as|by|objective|regularization|loss|defined as|given by|computed as):$", re.I)


def looks_like_equation_text(lines, paragraph):
    compact = paragraph.strip()
    if not compact:
        return False
    lower = compact.lower()
    if lower.startswith(("figure ", "fig. ", "table ")):
        return False
    if re.search(r"\b(et al\.|proceedings|conference|university|abstract|introduction|references)\b", lower):
        return False
    if re.match(r"^\[\d+\]", compact):
        return False
    if "$$" in compact:
        return True

    math_chars = len(MATH_CHARS_RE.findall(compact))
    ascii_letters = len(re.findall(r"[A-Za-z]", compact))
    words = re.findall(r"[A-Za-z]{3,}", compact)
    if len(words) > 30 and not re.search(r"[!\"#$%&]{3,}", compact):
        return False
    if len(words) > 8 and compact.endswith((".", ":", ";")):
        return False
    short_lines = sum(1 for line in lines if len(line) <= 90)
    has_layout_signal = bool(MATH_LAYOUT_RE.search(compact))
    has_unicode_math = any(0x1D400 <= ord(char) <= 0x1D7FF for char in compact)
    has_operator_line = any(re.search(r"(^|[^A-Za-z])(=|≈|≤|≥|∑|∫|\\frac|\\sum|\\begin\{)", line) for line in lines)
    punctuation_noise = bool(re.search(r"[!\"#$%&]{3,}", compact))

    if punctuation_noise and has_unicode_math:
        return True
    if has_layout_signal and (len(lines) > 1 or has_unicode_math or math_chars >= 4):
        return True
    if has_operator_line and short_lines >= max(1, len(lines) - 1) and math_chars >= 3 and len(words) <= 18:
        return True
    if has_unicode_math and math_chars >= 4 and ascii_letters <= 40 and len(words) <= 12:
        return True
    return False


def looks_like_equation_fragment(lines, paragraph):
    compact = paragraph.strip()
    if not compact or len(compact) > 180:
        return False
    words = re.findall(r"[A-Za-z]{3,}", compact)
    if len(words) > 8:
        return False
    if compact in {'"', "#"}:
        return True
    if compact.startswith(("=", "≈", "≤", "≥", "+", "-", "−")):
        return True
    if re.match(r"^\d+\s*[A-Z]{1,3}$", compact):
        return True
    if re.match(r"^[`$]?[A-Za-z][A-Za-z0-9`_$.,()✓ −+\-]*$", compact) and any(char in compact for char in "(),=✓$`"):
        return True
    if re.match(r"^[A-Z] X$", compact):
        return True
    if re.match(r"^[a-zA-Z],[a-zA-Z]|^[a-zA-Z]=\d+$|^,?\s*\(\d+\)$", compact):
        return True
    return looks_like_equation_text(lines, paragraph)


def expand_rect(fitz, rect, page_rect, margin=4):
    expanded = fitz.Rect(rect)
    expanded.x0 = max(page_rect.x0, expanded.x0 - margin)
    expanded.y0 = max(page_rect.y0, expanded.y0 - margin)
    expanded.x1 = min(page_rect.x1, expanded.x1 + margin)
    expanded.y1 = min(page_rect.y1, expanded.y1 + margin)
    return expanded


def write_equation_asset(fitz, page, rect, equation_dir, output_path, page_index, equation_index):
    rect = expand_rect(fitz, rect, page.rect)
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect, alpha=False)
    equation_path = equation_dir / f"page-{page_index:03d}-equation-{equation_index:02d}.svg"
    svg_wrap_pixmap(pixmap, equation_path)
    return equation_path.relative_to(output_path.parent)


def markdown_equation_block(relative_asset, extracted_text):
    extracted_text = extracted_text.replace("```", "`\\`\\`\\`")
    lines = [
        f"![Equation rendered from PDF]({relative_asset})",
        "",
        "AI-readable equation transcription, added from PDF text extraction; may be lossy:",
        "",
        "```text",
        extracted_text.strip(),
        "```",
    ]
    return "\n".join(lines)


def merge_block_rects(fitz, blocks):
    rect = fitz.Rect(blocks[0][:4])
    for block in blocks[1:]:
        rect.include_rect(fitz.Rect(block[:4]))
    return rect


def plain_text_blocks(page):
    blocks = []
    for block in page.get_text("blocks", sort=False) or []:
        if len(block) < 7 or block[6] != 0:
            continue
        lines = [normalize_pdf_line(line) for line in block[4].splitlines()]
        lines = [line for line in lines if line]
        if not lines:
            continue
        blocks.append({"rect": block[:4], "text": join_pdf_lines(lines)})
    return blocks


def nearest_caption_for_rect(fitz, text_blocks, rect):
    caption_re = re.compile(r"^(figure|fig\.|table)\s+\d+[:.]?\s+", re.I)
    candidates = []
    for block in text_blocks:
        text = block["text"]
        if not caption_re.match(text):
            continue
        block_rect = fitz.Rect(block["rect"])
        vertical_gap = min(abs(block_rect.y0 - rect.y1), abs(rect.y0 - block_rect.y1))
        horizontal_overlap = max(0, min(rect.x1, block_rect.x1) - max(rect.x0, block_rect.x0))
        if horizontal_overlap <= 0 and vertical_gap > 80:
            continue
        candidates.append((vertical_gap, text))
    if candidates:
        return truncate_text(sorted(candidates, key=lambda item: item[0])[0][1], 1200)
    return ""


def nearby_text_for_rect(fitz, text_blocks, rect, caption):
    snippets = []
    for block in text_blocks:
        text = block["text"]
        if text == caption or should_skip_block(text, 0):
            continue
        block_rect = fitz.Rect(block["rect"])
        vertical_gap = min(abs(block_rect.y0 - rect.y1), abs(rect.y0 - block_rect.y1))
        horizontal_overlap = max(0, min(rect.x1, block_rect.x1) - max(rect.x0, block_rect.x0))
        if vertical_gap <= 120 or horizontal_overlap > 0:
            snippets.append((vertical_gap, text))
    joined = " ".join(text for _gap, text in sorted(snippets, key=lambda item: item[0])[:3])
    return truncate_text(joined, 1200)


def visual_equivalent_note(kind, relative_asset, width, height, caption="", nearby_text=""):
    lines = [
        "AI-readable visual equivalent, added:",
        "",
        f"- Asset: `{relative_asset}`",
        f"- Type: {kind}",
        f"- Extracted size: {width} x {height} px",
    ]
    if caption:
        lines.append(f"- Caption/context: {caption}")
    if nearby_text and nearby_text != caption:
        lines.append(f"- Nearby paper text: {nearby_text}")
    if not caption and not nearby_text:
        lines.append("- Nearby paper text: none extracted from the PDF page for this asset.")
    lines.append(
        "- Transcription status: visual content is preserved in the linked SVG; the text above is extracted from the paper's caption and nearby page text."
    )
    return "\n".join(lines)


def clean_visual_context(text):
    text = text.replace(GENERIC_VISUAL_NOTE, " ")
    text = re.sub(r"---.*?---", " ", text, flags=re.S)
    text = re.sub(r"<!--\s*Page\s+\d+\s*-->", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"AI-readable visual equivalent, added:\s*", " ", text)
    text = re.sub(r"- (Asset|Type|Extracted size|Transcription status):[^\n]*", " ", text)
    text = re.sub(r"- (Caption/context|Nearby paper text):", " ", text)
    return truncate_text(text)


def split_markdown_blocks_preserving_fences(text):
    blocks = []
    current = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            current.append(line)
            continue
        if not in_fence and not line.strip():
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return blocks


def escape_untrusted_code_fences(markdown):
    escaped_lines = []
    in_added_text_fence = False
    previous_nonempty = ""
    for line in markdown.splitlines():
        stripped = line.strip()
        starts_added_fence = (
            stripped == "```text"
            and previous_nonempty.startswith("AI-readable equation transcription")
        )
        if starts_added_fence:
            in_added_text_fence = True
            escaped_lines.append(line)
        elif in_added_text_fence and stripped == "```":
            in_added_text_fence = False
            escaped_lines.append(line)
        elif in_added_text_fence:
            escaped_lines.append(line)
        else:
            escaped_lines.append(line.replace("```", "\\`\\`\\`"))
        if stripped:
            previous_nonempty = stripped
    return "\n".join(escaped_lines)


def find_recent_caption(text):
    caption_re = re.compile(r"^\*\*(Figure|Fig\.|Table) \d+\.?\*\*\s+(.+)$", re.I | re.M)
    matches = list(caption_re.finditer(text))
    if not matches:
        return ""
    return truncate_text(matches[-1].group(0), 1200)


def enhance_generic_visual_notes(markdown):
    pattern = re.compile(r"(!\[[^\]]*\]\(([^)]+)\))\n\n" + re.escape(GENERIC_VISUAL_NOTE))

    def replace(match):
        before = markdown[: match.start()]
        clean_before = clean_visual_context(before)
        caption = find_recent_caption(clean_before[-3000:])
        note = visual_equivalent_note(
            "PDF figure/image asset",
            match.group(2),
            "unknown",
            "unknown",
            caption=caption,
            nearby_text=clean_visual_context(clean_before[-1400:]),
        )
        return f"{match.group(1)}\n\n{note}"

    return pattern.sub(replace, markdown)


def ensure_visual_note_context(markdown):
    pattern = re.compile(
        r"(AI-readable visual equivalent, added:\n\n(?:- [^\n]*\n)+?)(- Transcription status:[^\n]*)",
        re.M,
    )

    def replace(match):
        note = match.group(1)
        if "- Caption/context:" in note or "- Nearby paper text:" in note:
            return match.group(0)
        fallback = "- Nearby paper text: none extracted from the PDF page for this asset.\n"
        return f"{note}{fallback}{match.group(2)}"

    return pattern.sub(replace, markdown)


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
    markdown = escape_untrusted_code_fences(markdown)
    markdown = enhance_generic_visual_notes(markdown)
    markdown = ensure_visual_note_context(markdown)
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

    paragraphs = split_markdown_blocks_preserving_fences("\n".join(normalized_lines))
    repaired = []
    for paragraph in paragraphs:
        stripped = paragraph.strip()
        if not stripped:
            continue
        if stripped.startswith(("---", "#", "<!--", "![", "AI-readable visual equivalent", "```")):
            repaired.append(stripped)
        else:
            repaired.append(split_inline_section_heading(stripped))
    return "\n\n".join(repaired).rstrip() + "\n"


def markdownize_pdf_blocks(page, page_index, output_path, equation_dir, allow_numbered_headings=False):
    fitz = require_fitz()
    section_re = re.compile(
        r"^(abstract|introduction|related work|background|method|methods|approach|experiments?|results?|discussion|limitations?|conclusion|acknowledg(e)?ments?|references|bibliography|appendix|supplementary material)$",
        re.I,
    )
    numbered_section_re = re.compile(r"^(\d+(\.\d+)*)\.?\s+[A-Z][A-Za-z0-9 ,:;()/-]{2,120}$")
    out = []
    saw_abstract = allow_numbered_headings
    equation_index = 0
    blocks = page.get_text("blocks", sort=False) or []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if len(block) < 7 or block[6] != 0:
            index += 1
            continue
        raw_text = block[4]
        if should_skip_block(raw_text, page_index):
            index += 1
            continue
        lines = [normalize_pdf_line(line) for line in raw_text.splitlines()]
        lines = [line for line in lines if line and not should_skip_block(line, page_index)]
        if not lines:
            index += 1
            continue
        paragraph = join_pdf_lines(lines)
        if not paragraph:
            index += 1
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
            heading = paragraph[3:].strip() if paragraph.startswith("## ") else paragraph
            out.append(f"## {heading}")
        elif re.match(r"^(figure|fig\.|table)\s+\d+[:.]?\s+", paragraph, re.I):
            caption = re.sub(r"^(figure|fig\.|table)\s+(\d+)\s*[:.]?\s*", lambda m: f"**{m.group(1).title()} {m.group(2)}.** ", paragraph, flags=re.I)
            out.append(caption)
        elif looks_like_equation_text(lines, paragraph):
            equation_index += 1
            relative = write_equation_asset(fitz, page, fitz.Rect(block[:4]), equation_dir, output_path, page_index, equation_index)
            out.append(markdown_equation_block(relative, "\n".join(lines)))
        elif out and MATH_LEAD_IN_RE.search(out[-1]) and looks_like_equation_fragment(lines, paragraph):
            equation_blocks = [block]
            equation_lines = list(lines)
            index += 1
            while index < len(blocks):
                next_block = blocks[index]
                if len(next_block) < 7 or next_block[6] != 0:
                    index += 1
                    continue
                next_lines = [normalize_pdf_line(line) for line in next_block[4].splitlines()]
                next_lines = [line for line in next_lines if line and not should_skip_block(line, page_index)]
                next_paragraph = join_pdf_lines(next_lines)
                if not looks_like_equation_fragment(next_lines, next_paragraph):
                    break
                equation_blocks.append(next_block)
                equation_lines.extend(next_lines)
                index += 1
            equation_index += 1
            relative = write_equation_asset(
                fitz,
                page,
                merge_block_rects(fitz, equation_blocks),
                equation_dir,
                output_path,
                page_index,
                equation_index,
            )
            out.append(markdown_equation_block(relative, "\n".join(equation_lines)))
            continue
        else:
            append_readable_block(out, paragraph)
        index += 1
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
    equation_dir = figure_dir / "equations"
    equation_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    allow_numbered_headings = False
    seen_xrefs = set()
    for page_index, page in enumerate(doc, start=1):
        text_blocks = plain_text_blocks(page)
        text, allow_numbered_headings = markdownize_pdf_blocks(
            page,
            page_index,
            output_path,
            equation_dir,
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
                try:
                    pixmap = fitz.Pixmap(doc, xref)
                    if pixmap.alpha:
                        pixmap = fitz.Pixmap(fitz.csRGB, pixmap)
                    if pixmap.width * pixmap.height >= min_figure_pixels:
                        figure_path = figure_dir / f"page-{page_index:03d}-figure-{image_index:02d}.svg"
                        svg_wrap_pixmap(pixmap, figure_path)
                        relative = figure_path.relative_to(output_path.parent)
                        rects = page.get_image_rects(xref)
                        image_rect = rects[0] if rects else fitz.Rect(0, 0, 0, 0)
                        caption = nearest_caption_for_rect(fitz, text_blocks, image_rect) if rects else ""
                        nearby_text = nearby_text_for_rect(fitz, text_blocks, image_rect, caption) if rects else ""
                        parts.append(
                            "\n\n"
                            f"![Figure extracted from page {page_index}]({relative})\n\n"
                            + visual_equivalent_note("PDF figure/image xref pixmap", relative, pixmap.width, pixmap.height, caption, nearby_text)
                        )
                        continue
                    continue
                except Exception as pixmap_exc:
                    print(f"skipped-figure-pixmap: page {page_index} image {image_index} ({pixmap_exc})")
                rects = page.get_image_rects(xref)
                if rects:
                    try:
                        image_rect = expand_rect(fitz, rects[0], page.rect)
                        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=image_rect, alpha=False)
                        if pixmap.width * pixmap.height >= min_figure_pixels:
                            figure_path = figure_dir / f"page-{page_index:03d}-figure-{image_index:02d}.svg"
                            svg_wrap_pixmap(pixmap, figure_path)
                            relative = figure_path.relative_to(output_path.parent)
                            caption = nearest_caption_for_rect(fitz, text_blocks, image_rect)
                            nearby_text = nearby_text_for_rect(fitz, text_blocks, image_rect, caption)
                            parts.append(
                                "\n\n"
                                f"![Figure extracted from page {page_index}]({relative})\n\n"
                                + visual_equivalent_note("PDF figure/image rendered crop", relative, pixmap.width, pixmap.height, caption, nearby_text)
                            )
                            continue
                        continue
                    except Exception as fallback_exc:
                        print(f"skipped-figure-fallback: page {page_index} image {image_index} ({fallback_exc})")
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
            rects = page.get_image_rects(xref)
            image_rect = rects[0] if rects else fitz.Rect(0, 0, 0, 0)
            caption = nearest_caption_for_rect(fitz, text_blocks, image_rect) if rects else ""
            nearby_text = nearby_text_for_rect(fitz, text_blocks, image_rect, caption) if rects else ""
            parts.append(
                "\n\n"
                f"![Figure extracted from page {page_index}]({relative})\n\n"
                + visual_equivalent_note("PDF figure/image asset", relative, width, height, caption, nearby_text)
            )
    frontmatter = [
        "---",
        f'title: "{(row.get("title") or "").replace(chr(34), chr(92) + chr(34))}"',
        f"source_url: {row.get('paper_page_url')}",
        f"paper_pdf_url: {pdf_url}",
        f"venue: {row.get('venue')}",
        f"year: {row.get('data_year') or row.get('year')}",
        f"retrieved_date: {dt.date.today().isoformat()}",
        "content_scope: whole paper PDF text with extracted SVG figure and equation assets",
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
    parser.add_argument("--row-offset", type=int, default=0, help="Skip this many eligible ready rows after venue filtering.")
    parser.add_argument("--row-count", type=int, help="Attempt at most this many eligible ready rows after --row-offset.")
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
    eligible_seen = 0
    for row in rows:
        if args.venue and row["venue"] not in args.venue:
            continue
        if row.get("status") != "ready" or not row.get("paper_page_url"):
            skipped += 1
            continue
        if eligible_seen < args.row_offset:
            eligible_seen += 1
            skipped += 1
            continue
        if args.row_count is not None and attempted >= args.row_count:
            break
        eligible_seen += 1
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
