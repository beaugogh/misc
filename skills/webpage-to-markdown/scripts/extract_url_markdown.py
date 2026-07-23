#!/usr/bin/env python3
"""Convert a web page URL or saved HTML file into readable Markdown."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import html
import mimetypes
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_CONFIG = SKILL_DIR / "config.yaml"


@dataclass
class Config:
    output: str = "output"
    name_chars: int = 90
    user_agent: str = "Mozilla/5.0 (compatible; CodexWebpageToMarkdown/1.0)"
    timeout_seconds: int = 30
    min_words: int = 80
    include_frontmatter: bool = True
    preserve_images: bool = True
    preserve_links: bool = True
    extract_visual_assets: bool = True
    visual_asset_dir_suffix: str = "_assets"
    max_image_bytes: int = 50_000_000


@dataclass
class PageMetadata:
    source_url: str
    fetched_at: str
    title: str = ""
    canonical_url: str = ""
    description: str = ""
    language: str = ""
    extraction_method: str = "stdlib-html-parser"


@dataclass
class Chunk:
    kind: str
    text: str = ""
    level: int = 0
    rows: list[list[str]] = field(default_factory=list)
    ordered: bool = False
    lang: str = ""
    url: str = ""


def parse_simple_yaml(path: Path) -> Config:
    config = Config()
    if not path.exists():
        return config
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().replace("-", "_")
        value = value.strip().strip('"').strip("'")
        if not hasattr(config, key):
            continue
        current = getattr(config, key)
        if isinstance(current, bool):
            value = value.lower() in {"1", "true", "yes", "on"}
        elif isinstance(current, int):
            value = int(value)
        setattr(config, key, value)
    return config


def fetch_url(url: str, config: Config) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": config.user_agent})
    with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
        content_type = response.headers.get_content_type()
        charset = response.headers.get_content_charset() or "utf-8"
        data = response.read()
    if content_type not in {"text/html", "application/xhtml+xml"}:
        raise SystemExit(f"unsupported content type: {content_type}; expected an HTML web page")
    return data.decode(charset, errors="replace"), str(response.geturl())


def strip_hidden_boilerplate(source: str) -> str:
    source = re.sub(r"(?is)<!--.*?-->", " ", source)
    source = re.sub(r"(?is)<(script|style|noscript|canvas|iframe|form)\b.*?</\1>", " ", source)
    return source


def attr_value(attrs: list[tuple[str, str | None]], name: str) -> str:
    for key, value in attrs:
        if key.lower() == name:
            return value or ""
    return ""


def has_attr_value(attrs: list[tuple[str, str | None]], name: str, expected: str) -> bool:
    return attr_value(attrs, name).lower() == expected.lower()


def format_start_tag(tag: str, attrs: list[tuple[str, str | None]], close: bool = False) -> str:
    svg_attr_names = {
        "viewbox": "viewBox",
        "preserveaspectratio": "preserveAspectRatio",
        "gradientunits": "gradientUnits",
        "gradienttransform": "gradientTransform",
        "markerwidth": "markerWidth",
        "markerheight": "markerHeight",
        "refx": "refX",
        "refy": "refY",
    }
    rendered = []
    for key, value in attrs:
        key = svg_attr_names.get(key, key)
        if value is None:
            rendered.append(html.escape(key, quote=True))
        else:
            rendered.append(f'{html.escape(key, quote=True)}="{html.escape(value, quote=True)}"')
    suffix = " /" if close else ""
    return f"<{tag}{(' ' + ' '.join(rendered)) if rendered else ''}{suffix}>"


class MarkdownHTMLParser(HTMLParser):
    SKIP_TAGS = {"nav", "header", "footer", "aside", "button", "select", "option"}
    BLOCK_TAGS = {"p", "div", "section", "article", "main", "blockquote"}
    HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self, base_url: str, preserve_links: bool = True, preserve_images: bool = True) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.preserve_links = preserve_links
        self.preserve_images = preserve_images
        self.meta = PageMetadata(source_url=base_url, fetched_at=utc_now())
        self.chunks: list[Chunk] = []
        self.skip_depth = 0
        self.current_parts: list[str] = []
        self.current_kind = "paragraph"
        self.current_heading_level = 0
        self.link_stack: list[str] = []
        self.list_stack: list[dict[str, object]] = []
        self.in_li = False
        self.li_parts: list[str] = []
        self.in_pre = False
        self.pre_parts: list[str] = []
        self.table_stack: list[list[list[str]]] = []
        self.current_row: list[str] | None = None
        self.current_cell_parts: list[str] | None = None
        self.in_svg = False
        self.svg_depth = 0
        self.svg_parts: list[str] = []
        self.svg_title_parts: list[str] = []
        self.in_svg_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self.in_svg:
            self.svg_depth += 1
            self.svg_parts.append(format_start_tag(tag, attrs))
            if tag == "title":
                self.in_svg_title = True
                self.svg_title_parts = []
            return
        if self.skip_depth:
            self.skip_depth += 1
            return
        if tag in self.SKIP_TAGS or has_attr_value(attrs, "aria-hidden", "true"):
            self.flush_text()
            self.skip_depth = 1
            return
        # Capture images embedded as inline CSS background-image (e.g. x.com article
        # section images on <div style="background-image:url(...)">). Applies to any
        # element; the chunk is emitted before normal tag handling so it sits in source
        # order. JS-applied background-image (absent from static HTML) is not reachable
        # here — see SKILL.md for the browser-bridge render path.
        if self.preserve_images:
            bg_url = background_image_url(attr_value(attrs, "style"))
            if bg_url and not bg_url.startswith("data:image/svg"):
                alt = clean_inline(attr_value(attrs, "aria-label") or attr_value(attrs, "title") or "image")
                self.flush_text()
                self.chunks.append(Chunk("image", text=alt, url=resolve_url(self.base_url, bg_url)))
        if tag == "html":
            self.meta.language = attr_value(attrs, "lang")
        elif tag == "title":
            self.flush_text()
            self.current_kind = "title"
            self.current_parts = []
        elif tag == "meta":
            name = attr_value(attrs, "name").lower() or attr_value(attrs, "property").lower()
            content = attr_value(attrs, "content")
            if name in {"description", "og:description"} and content and not self.meta.description:
                self.meta.description = clean_inline(content)
            elif name in {"og:title", "twitter:title"} and content and not self.meta.title:
                self.meta.title = clean_inline(content)
        elif tag == "link" and attr_value(attrs, "rel").lower() == "canonical":
            href = attr_value(attrs, "href")
            if href:
                self.meta.canonical_url = resolve_url(self.base_url, href)
        elif tag in self.HEADING_TAGS:
            self.flush_text()
            self.current_kind = "heading"
            self.current_heading_level = int(tag[1])
            self.current_parts = []
        elif tag in self.BLOCK_TAGS:
            self.flush_text()
        elif tag == "br":
            self.add_text("\n")
        elif tag == "a":
            self.link_stack.append(resolve_url(self.base_url, attr_value(attrs, "href")))
        elif tag == "img" and self.preserve_images:
            alt = clean_inline(attr_value(attrs, "alt") or attr_value(attrs, "title") or "image")
            src = attr_value(attrs, "src") or attr_value(attrs, "data-src") or first_srcset_url(attr_value(attrs, "srcset"))
            if src:
                self.flush_text()
                self.chunks.append(Chunk("image", text=alt, url=resolve_url(self.base_url, src)))
        elif tag == "svg" and self.preserve_images:
            self.flush_text()
            self.in_svg = True
            self.svg_depth = 1
            self.svg_parts = [format_start_tag(tag, attrs)]
            self.svg_title_parts = []
            self.in_svg_title = False
        elif tag in {"ul", "ol"}:
            self.flush_text()
            self.list_stack.append({"ordered": tag == "ol", "index": 1})
        elif tag == "li":
            self.flush_text()
            self.in_li = True
            self.li_parts = []
        elif tag == "pre":
            self.flush_text()
            self.in_pre = True
            self.pre_parts = []
        elif tag == "table":
            self.flush_text()
            self.table_stack.append([])
        elif tag == "tr" and self.table_stack:
            self.current_row = []
        elif tag in {"td", "th"} and self.current_row is not None:
            self.current_cell_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.in_svg:
            self.svg_parts.append(f"</{tag}>")
            if tag == "title":
                self.in_svg_title = False
            self.svg_depth -= 1
            if self.svg_depth <= 0:
                svg_text = "".join(self.svg_parts)
                alt = clean_inline("".join(self.svg_title_parts)) or "inline svg"
                data_url = "data:image/svg+xml," + urllib.parse.quote(svg_text)
                self.chunks.append(Chunk("image", text=alt, url=data_url))
                self.in_svg = False
                self.svg_parts = []
                self.svg_title_parts = []
            return
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag == "title":
            title = clean_inline("".join(self.current_parts))
            if title and not self.meta.title:
                self.meta.title = title
            self.current_parts = []
            self.current_kind = "paragraph"
        elif tag in self.HEADING_TAGS:
            text = clean_inline("".join(self.current_parts))
            if text:
                self.chunks.append(Chunk("heading", text=text, level=self.current_heading_level))
                if not self.meta.title and self.current_heading_level == 1:
                    self.meta.title = text
            self.current_parts = []
            self.current_kind = "paragraph"
        elif tag in self.BLOCK_TAGS:
            self.flush_text()
        elif tag == "a":
            if self.link_stack:
                self.link_stack.pop()
        elif tag == "li" and self.in_li:
            text = clean_inline("".join(self.li_parts))
            if text:
                ordered = bool(self.list_stack[-1]["ordered"]) if self.list_stack else False
                if ordered and self.list_stack:
                    idx = int(self.list_stack[-1]["index"])
                    self.list_stack[-1]["index"] = idx + 1
                self.chunks.append(Chunk("list_item", text=text, ordered=ordered))
            self.in_li = False
            self.li_parts = []
        elif tag in {"ul", "ol"}:
            self.flush_text()
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "pre" and self.in_pre:
            code = "\n".join(line.rstrip() for line in "".join(self.pre_parts).splitlines()).strip("\n")
            if code:
                self.chunks.append(Chunk("code", text=code))
            self.in_pre = False
            self.pre_parts = []
        elif tag in {"td", "th"} and self.current_cell_parts is not None and self.current_row is not None:
            self.current_row.append(clean_inline("".join(self.current_cell_parts)))
            self.current_cell_parts = None
        elif tag == "tr" and self.current_row is not None and self.table_stack:
            if any(cell for cell in self.current_row):
                self.table_stack[-1].append(self.current_row)
            self.current_row = None
        elif tag == "table" and self.table_stack:
            rows = self.table_stack.pop()
            if rows:
                self.chunks.append(Chunk("table", rows=rows))

    def handle_data(self, data: str) -> None:
        if self.in_svg:
            self.svg_parts.append(html.escape(data, quote=False))
            if self.in_svg_title:
                self.svg_title_parts.append(data)
            return
        if self.skip_depth:
            return
        self.add_text(data)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self.in_svg:
            self.svg_parts.append(format_start_tag(tag, attrs, close=True))
            return
        if tag == "img" and self.preserve_images:
            self.handle_starttag(tag, attrs)
            return
        # Self-closing element carrying an inline background-image style.
        if self.preserve_images and background_image_url(attr_value(attrs, "style")):
            self.handle_starttag(tag, attrs)

    def add_text(self, text: str) -> None:
        if not text:
            return
        if self.in_pre:
            self.pre_parts.append(text)
            return
        if self.current_cell_parts is not None:
            self.current_cell_parts.append(text)
            return
        if self.in_li:
            self.li_parts.append(self.format_link_text(text))
            return
        self.current_parts.append(self.format_link_text(text))

    def format_link_text(self, text: str) -> str:
        if not self.preserve_links or not self.link_stack or not self.link_stack[-1]:
            return text
        cleaned = clean_inline(text)
        if not cleaned:
            return text
        return f"[{escape_markdown(cleaned)}]({self.link_stack[-1]})"

    def flush_text(self) -> None:
        if self.current_kind != "paragraph":
            return
        text = clean_block("".join(self.current_parts))
        if text:
            self.chunks.append(Chunk("paragraph", text=text))
        self.current_parts = []


def clean_inline(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean_block(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n\s*\n+", "\n\n", value)
    value = re.sub(r"\s+\n", "\n", value)
    value = re.sub(r"\n\s+", "\n", value)
    return value.strip()


def escape_markdown(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]")


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def resolve_url(base_url: str, maybe_url: str) -> str:
    if not maybe_url:
        return ""
    return urllib.parse.urljoin(base_url, maybe_url)


def slugify(value: str, fallback: str, max_chars: int) -> str:
    value = value or fallback
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    if not value:
        value = fallback
    return value[:max_chars].strip("-") or fallback


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def word_count(markdown: str) -> int:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\w'-]+\b", text))


def looks_like_boilerplate(text: str) -> bool:
    lowered = text.lower()
    if len(text) < 3:
        return True
    markers = [
        "accept cookies",
        "cookie policy",
        "privacy policy",
        "all rights reserved",
        "subscribe to our newsletter",
        "sign in",
        "log in",
        "skip to content",
    ]
    return any(marker in lowered for marker in markers)


def dedupe_chunks(chunks: Iterable[Chunk]) -> list[Chunk]:
    result: list[Chunk] = []
    seen_short: set[str] = set()
    for chunk in chunks:
        if chunk.kind in {"paragraph", "heading", "list_item"}:
            key = re.sub(r"\W+", "", chunk.text.lower())
            if looks_like_boilerplate(chunk.text):
                continue
            if len(key) < 120 and key in seen_short:
                continue
            if len(key) < 120:
                seen_short.add(key)
        result.append(chunk)
    return result


def render_markdown(
    meta: PageMetadata,
    chunks: list[Chunk],
    config: Config,
    output_path: Path | None = None,
) -> str:
    title = meta.title or urllib.parse.urlparse(meta.source_url).netloc or "Untitled page"
    lines: list[str] = []
    if config.include_frontmatter:
        lines.extend(
            [
                "---",
                f'title: "{yaml_quote(title)}"',
                f'source_url: "{yaml_quote(meta.source_url)}"',
                f'fetched_at: "{meta.fetched_at}"',
                f'extraction_method: "{meta.extraction_method}"',
            ]
        )
        if meta.canonical_url:
            lines.append(f'canonical_url: "{yaml_quote(meta.canonical_url)}"')
        if meta.description:
            lines.append(f'description: "{yaml_quote(meta.description)}"')
        if meta.language:
            lines.append(f'language: "{yaml_quote(meta.language)}"')
        lines.append("---")
        lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    if meta.description:
        lines.append(f"> {meta.description}")
        lines.append("")
    lines.append("## Source Metadata")
    lines.append("")
    lines.append(f"- Source URL: {meta.source_url}")
    if meta.canonical_url:
        lines.append(f"- Canonical URL: {meta.canonical_url}")
    lines.append(f"- Fetched at: {meta.fetched_at}")
    lines.append(f"- Extraction method: {meta.extraction_method}")
    lines.append("")
    lines.append("## Page Content")
    lines.append("")

    previous_kind = ""
    skipped_title_heading = False
    for chunk in chunks:
        if chunk.kind == "heading":
            if not skipped_title_heading and chunk.level == 1 and clean_inline(chunk.text).lower() == title.lower():
                skipped_title_heading = True
                continue
            level = max(2, min(chunk.level + 1, 6))
            lines.append(f"{'#' * level} {chunk.text}")
            lines.append("")
        elif chunk.kind == "paragraph":
            lines.append(wrap_markdown_text(chunk.text))
            lines.append("")
        elif chunk.kind == "list_item":
            prefix = "1." if chunk.ordered else "-"
            lines.append(f"{prefix} {chunk.text}")
            previous_kind = "list_item"
            continue
        elif chunk.kind == "code":
            lines.append("```")
            lines.append(chunk.text.replace("```", "`\\`\\`"))
            lines.append("```")
            lines.append("")
        elif chunk.kind == "table":
            lines.extend(render_table(chunk.rows))
            lines.append("")
        elif chunk.kind == "image":
            lines.extend(render_image_chunk(chunk, config, output_path))
            lines.append("")
        if previous_kind == "list_item":
            lines.append("")
        previous_kind = chunk.kind
    return "\n".join(lines).rstrip() + "\n"


def yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def wrap_markdown_text(text: str) -> str:
    if re.search(r"!\[.*?\]\(.*?\)|\[[^\]]+\]\([^)]+\)", text):
        return text
    return "\n".join(textwrap.wrap(text, width=100, break_long_words=False, break_on_hyphens=False))


def render_table(rows: list[list[str]]) -> list[str]:
    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    header = normalized[0]
    lines = [
        "| " + " | ".join(escape_table_cell(cell) for cell in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in normalized[1:]:
        lines.append("| " + " | ".join(escape_table_cell(cell) for cell in row) + " |")
    return lines


def render_image_chunk(chunk: Chunk, config: Config, output_path: Path | None) -> list[str]:
    alt = chunk.text or "image"
    source_url = chunk.url
    asset_ref = source_url
    status = "remote reference preserved; local SVG asset not requested"
    asset_type = "image"
    size_text = "unknown"

    if config.extract_visual_assets and output_path is not None and source_url:
        asset_dir = output_path.with_suffix("").parent / f"{output_path.stem}{config.visual_asset_dir_suffix}"
        asset_dir.mkdir(parents=True, exist_ok=True)
        try:
            asset_path, asset_type, size_text = save_image_as_svg(source_url, alt, asset_dir, config)
            asset_ref = asset_path.relative_to(output_path.parent).as_posix()
            status = "preserved as local SVG asset"
        except Exception as exc:  # noqa: BLE001 - preserve page conversion even when one image fails.
            status = f"local SVG asset unavailable: {exc}"

    lines = [f"![{escape_markdown(alt)}]({asset_ref})", "", "<!-- visual-asset"]
    lines.append(f"Asset: {asset_ref}")
    lines.append(f"Source: {source_url}")
    lines.append(f"Type: {asset_type}")
    lines.append(f"Extracted size: {size_text}")
    lines.append(f"Alt text: {alt}")
    lines.append(f"Transcription status: {status}")
    lines.append("Multimodal status: local SVG asset is available when Asset is a relative path; inspect it directly for visual details.")
    lines.append("Text-only fallback: use alt text, source URL, dimensions, nearby page text, and any explicit caption; visual content is not fully transcribed unless Mermaid or a human/agent note is added.")
    lines.append("Mermaid: not inferred automatically; add only after visual inspection confirms a diagram, flowchart, graph, or timeline.")
    lines.append("-->")
    return lines


def save_image_as_svg(source_url: str, alt: str, asset_dir: Path, config: Config) -> tuple[Path, str, str]:
    data, content_type = fetch_binary(source_url, config)
    if len(data) > config.max_image_bytes:
        raise ValueError(f"image is {len(data)} bytes, above max_image_bytes={config.max_image_bytes}")
    parsed = urllib.parse.urlparse(source_url)
    fallback_name = "" if parsed.scheme == "data" else Path(parsed.path).name
    stem = slugify(Path(fallback_name).stem or alt, "image", 80)
    digest = hashlib.sha256(source_url.encode("utf-8")).hexdigest()[:12]
    content_type = content_type or mimetypes.guess_type(fallback_name)[0] or "application/octet-stream"
    if content_type == "image/svg+xml" or data.lstrip().startswith(b"<svg"):
        asset_path = unique_path(asset_dir / f"{stem}-{digest}.svg")
        asset_path.write_bytes(data)
        dimensions = svg_dimensions(data.decode("utf-8", errors="ignore"))
        return asset_path, "svg", dimensions

    width, height = image_dimensions(data, content_type)
    encoded = base64.b64encode(data).decode("ascii")
    escaped_alt = html.escape(alt or "image", quote=True)
    width_attr = str(width or 1)
    height_attr = str(height or 1)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_attr}" height="{height_attr}" '
        f'viewBox="0 0 {width_attr} {height_attr}" role="img" aria-label="{escaped_alt}">\n'
        f"  <title>{escaped_alt}</title>\n"
        f'  <image href="data:{content_type};base64,{encoded}" width="{width_attr}" height="{height_attr}" '
        'preserveAspectRatio="xMidYMid meet"/>\n'
        "</svg>\n"
    )
    asset_path = unique_path(asset_dir / f"{stem}-{digest}.svg")
    asset_path.write_text(svg, encoding="utf-8")
    return asset_path, f"{content_type} wrapped in svg", f"{width_attr}x{height_attr}; {len(data)} bytes"


def fetch_binary(url: str, config: Config) -> tuple[bytes, str]:
    if url.startswith("data:"):
        header, _, payload = url.partition(",")
        content_type = header[5:].split(";", 1)[0] or "application/octet-stream"
        if ";base64" in header:
            return base64.b64decode(payload), content_type
        return urllib.parse.unquote_to_bytes(payload), content_type
    request = urllib.request.Request(url, headers={"User-Agent": config.user_agent})
    with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
        content_type = response.headers.get_content_type()
        return response.read(config.max_image_bytes + 1), content_type


def image_dimensions(data: bytes, content_type: str) -> tuple[int | None, int | None]:
    if content_type == "image/png" and data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if content_type in {"image/jpeg", "image/jpg"}:
        return jpeg_dimensions(data)
    if content_type == "image/gif" and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    return None, None


def jpeg_dimensions(data: bytes) -> tuple[int | None, int | None]:
    idx = 2
    while idx + 9 < len(data):
        if data[idx] != 0xFF:
            idx += 1
            continue
        marker = data[idx + 1]
        idx += 2
        if marker in {0xD8, 0xD9}:
            continue
        length = int.from_bytes(data[idx : idx + 2], "big")
        if marker in range(0xC0, 0xC4):
            height = int.from_bytes(data[idx + 3 : idx + 5], "big")
            width = int.from_bytes(data[idx + 5 : idx + 7], "big")
            return width, height
        idx += length
    return None, None


def svg_dimensions(svg_text: str) -> str:
    width = re.search(r'\bwidth=["\']([^"\']+)["\']', svg_text)
    height = re.search(r'\bheight=["\']([^"\']+)["\']', svg_text)
    if width and height:
        return f"{width.group(1)}x{height.group(1)}"
    view_box = re.search(r'\bviewBox=["\']([^"\']+)["\']', svg_text)
    return f"viewBox {view_box.group(1)}" if view_box else "unknown"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(2, 10_000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise ValueError(f"could not create unique path for {path}")


def first_srcset_url(srcset: str) -> str:
    if not srcset:
        return ""
    return srcset.split(",", 1)[0].strip().split(" ", 1)[0]


def background_image_url(style: str) -> str:
    """Extract the first url(...) from a CSS ``background``/``background-image`` declaration.

    Many sites (notably x.com article pages, and various SPA image galleries) embed
    section images as ``style="background-image:url(...)"`` on a ``<div>`` rather than
    via ``<img>``. The static-HTML parser only sees inline ``style`` attributes, so this
    covers that case. Returns "" when no usable url() is present.

    Note: this only captures URLs that are present in the serialized HTML. Sites that
    apply ``background-image`` imperatively via JavaScript at runtime (x.com does this)
    leave no trace in ``outerHTML``; for those, render the page in a browser and capture
    computed styles, then pass the HTML or a pre-resolved image list — see SKILL.md.
    """
    if not style:
        return ""
    match = re.search(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)", style, re.I)
    if not match:
        return ""
    url = match.group(2).strip()
    # Skip data: URIs that are not images and obviously non-image schemes; the caller
    # resolves and fetches. Keep http(s) and protocol-relative and data: image URIs.
    return url



def output_path_for(url: str, title: str, output_dir: Path, name_chars: int) -> Path:
    parsed = urllib.parse.urlparse(url)
    fallback = parsed.netloc.replace(".", "-") or "webpage"
    slug = slugify(title, fallback, name_chars)
    prefix = dt.datetime.now().strftime("%Y%m%d")
    return output_dir / f"{prefix}-{slug}.md"


def extract_chunks(source_html: str, source_url: str, config: Config) -> tuple[list[Chunk], PageMetadata]:
    parser = MarkdownHTMLParser(source_url, config.preserve_links, config.preserve_images)
    parser.feed(strip_hidden_boilerplate(source_html))
    parser.flush_text()
    chunks = dedupe_chunks(parser.chunks)
    return chunks, parser.meta


def validate_markdown(path: Path, min_words: int) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("missing YAML frontmatter")
    if len(re.findall(r"^# ", text, flags=re.M)) != 1:
        errors.append("expected exactly one H1 heading")
    if "Source URL:" not in text:
        errors.append("missing source URL metadata")
    count = word_count(text)
    if count < min_words:
        errors.append(f"word count {count} is below minimum {min_words}")
    if "## Page Content" not in text:
        errors.append("missing Page Content section")
    for ref in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        parsed = urllib.parse.urlparse(ref)
        if not parsed.scheme and not (path.parent / ref).exists():
            errors.append(f"missing local image asset: {ref}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?", help="URL to fetch and convert")
    parser.add_argument("--html", type=Path, help="Use an already-downloaded HTML file")
    parser.add_argument("--output-dir", type=Path, help="Directory for generated Markdown")
    parser.add_argument("--output", type=Path, help="Exact Markdown output path")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--name-chars", type=int)
    parser.add_argument("--min-words", type=int)
    parser.add_argument("--check-only", type=Path, help="Validate an existing Markdown file and exit")
    parser.add_argument("--no-assets", action="store_true", help="Preserve remote image links without creating local SVG assets")
    args = parser.parse_args(argv)

    config = parse_simple_yaml(args.config)
    if args.name_chars is not None:
        config.name_chars = args.name_chars
    if args.min_words is not None:
        config.min_words = args.min_words
    if args.no_assets:
        config.extract_visual_assets = False

    if args.check_only:
        errors = validate_markdown(args.check_only, config.min_words)
        if errors:
            for error in errors:
                print(f"FAIL: {error}", file=sys.stderr)
            return 1
        print(f"OK: {args.check_only}")
        return 0

    if not args.url:
        parser.error("url is required unless --check-only is used")
    url = args.url
    if args.html:
        source_html = args.html.read_text(encoding="utf-8", errors="replace")
        final_url = url
    else:
        try:
            source_html, final_url = fetch_url(url, config)
        except urllib.error.URLError as exc:
            raise SystemExit(f"failed to fetch {url}: {exc}") from exc

    chunks, meta = extract_chunks(source_html, final_url, config)
    output_dir = args.output_dir or (SKILL_DIR / config.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output or output_path_for(final_url, meta.title, output_dir, config.name_chars)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = render_markdown(meta, chunks, config, output_path)
    output_path.write_text(markdown, encoding="utf-8")

    errors = validate_markdown(output_path, config.min_words)
    status = "OK" if not errors else "WARN"
    print(f"{status}: wrote {output_path}")
    print(f"words={word_count(markdown)}")
    for error in errors:
        print(f"WARN: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
