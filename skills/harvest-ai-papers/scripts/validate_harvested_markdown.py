#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

from harvest_manifest import fetch_bytes


def has_control_chars(text):
    return any(char not in "\n\t" and (ord(char) < 32 or 0x7F <= ord(char) <= 0x9F) for char in text)


def frontmatter_value(text, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.M)
    return match.group(1).strip() if match else ""


def pdf_page_count(pdf_url):
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required for --check-pdf-pages") from exc
    pdf_bytes = fetch_bytes(pdf_url)
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        return doc.page_count


def validate_file(path, min_words, check_pdf_pages):
    errors = []
    text = path.read_text(encoding="utf-8")
    if "\x00" in text or has_control_chars(text):
        errors.append("contains NUL or non-Markdown control characters")
    if not text.startswith("---\n"):
        errors.append("missing YAML frontmatter")
    if len(re.findall(r"^# ", text, flags=re.M)) != 1:
        errors.append("expected exactly one H1 title")
    if "source_url:" not in text or "paper_pdf_url:" not in text:
        errors.append("missing source_url or paper_pdf_url metadata")
    if "content_scope: whole paper PDF text" not in text:
        errors.append("missing whole-paper content_scope metadata")
    if text.count("```") % 2:
        errors.append("has unbalanced fenced code blocks")
    word_count = len(re.findall(r"\b\w+\b", text))
    if word_count < min_words:
        errors.append(f"too short: {word_count} words, expected at least {min_words}")
    if not re.search(r"^## .*?(References|Bibliography)\b", text, flags=re.I | re.M):
        errors.append("missing Markdown references/bibliography heading")
    heading_count = len(re.findall(r"^## ", text, flags=re.M))
    if heading_count < 4:
        errors.append(f"too few Markdown section headings: {heading_count}")
    page_markers = [int(value) for value in re.findall(r"<!-- Page (\d+) -->", text)]
    if not page_markers:
        errors.append("missing page markers")
    elif page_markers != list(range(1, max(page_markers) + 1)):
        errors.append("page markers are missing or out of order")
    if text.count("\n\n") < 40:
        errors.append("too few paragraph breaks for readable long-form Markdown")
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1)
        if "://" in target:
            continue
        if not (path.parent / target).exists():
            errors.append(f"missing local figure asset: {target}")
    if check_pdf_pages:
        pdf_url = frontmatter_value(text, "paper_pdf_url")
        if not pdf_url:
            errors.append("cannot check PDF pages without paper_pdf_url")
        else:
            source_pages = pdf_page_count(pdf_url)
            extracted_pages = max(page_markers) if page_markers else 0
            if extracted_pages != source_pages:
                errors.append(f"page coverage mismatch: Markdown has {extracted_pages}, PDF has {source_pages}")
    return errors


def parse_args():
    parser = argparse.ArgumentParser(description="Validate harvested whole-paper Markdown outputs.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--min-words", type=int, default=3000)
    parser.add_argument("--check-pdf-pages", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    failed = False
    files = []
    for path in args.paths:
        files.extend(sorted(path.glob("**/*.md")) if path.is_dir() else [path])
    for path in files:
        errors = validate_file(path, args.min_words, args.check_pdf_pages)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
