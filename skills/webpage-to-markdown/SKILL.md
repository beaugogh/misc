---
name: webpage-to-markdown
description: Use when asked to parse, extract, archive, preserve, clean up, or transform a given web page URL into a complete, human-readable and agent-friendly Markdown file for models that may or may not be multimodal, including page metadata, headings, links, tables, code blocks, images, visual fallbacks, and provenance.
---

# Webpage To Markdown

Use this skill to convert a web page URL into a faithful Markdown capture for humans and downstream agents/LLMs, including models that cannot inspect images.

## Quick Start

Read `config.yaml`, then run:

```bash
python3 skills/webpage-to-markdown/scripts/extract_url_markdown.py "<url>"
```

This writes to the configured output directory, defaulting to:

```text
skills/webpage-to-markdown/output
```

Useful options:

```bash
python3 skills/webpage-to-markdown/scripts/extract_url_markdown.py "<url>" --output-dir <dir> --name-chars 90
python3 skills/webpage-to-markdown/scripts/extract_url_markdown.py "<url>" --output <path/to/file.md>
python3 skills/webpage-to-markdown/scripts/extract_url_markdown.py "<url>" --html <already-downloaded.html>
python3 skills/webpage-to-markdown/scripts/extract_url_markdown.py "<url>" --no-assets
```

## Extraction Standards

The output must be useful both to humans and agents:

- Preserve source provenance: source URL, fetch time, canonical URL when available, page title, description, and extraction method.
- Keep one H1 title at the top, then use Markdown headings in source order.
- Preserve article/page order, not a keyword summary.
- Keep paragraphs readable: repair excessive whitespace, unwrap broken lines, and avoid giant wall-of-text paragraphs.
- Preserve links as Markdown links, resolving relative URLs against the source URL.
- Preserve images, figures, charts, and diagrams as local SVG assets when they can be fetched or are embedded inline. Raster images are wrapped in SVG with embedded data so the Markdown can reference a stable local asset.
- SVG preservation does not require a multimodal model. The extractor either saves inline SVG directly or wraps fetched raster image bytes in an SVG container.
- Add a machine-scannable visual note next to every preserved image with asset path, original source URL, type, extracted size, alt text, transcription status, multimodal status, and text-only fallback status.
- For non-multimodal readers, provide every visual's surrounding evidence in text: alt text, caption if available, source URL, dimensions, and a clear statement when the visual content itself has not been inspected or transcribed.
- For multimodal readers, preserve the local SVG asset so the visual can be opened and inspected directly.
- A multimodal or vision-capable model is only needed when converting image content into semantic text or Mermaid that cannot be derived from source HTML, alt text, captions, or nearby page text.
- Add Mermaid only when the visual can be honestly interpreted as a diagram, flowchart, graph, tree, timeline, or chart. Do not invent Mermaid for photos, screenshots, dense plots, or visuals that have not been inspected.
- Preserve tables as Markdown tables when the source has real table rows.
- Preserve preformatted code as fenced code blocks.
- Remove navigation, headers, footers, cookie banners, scripts, styles, forms, and other boilerplate when possible.
- Keep clearly labeled assistant-derived notes separate from original page content.

Do not summarize or omit sections unless the user explicitly asks for a summary or excerpt.

## Workflow

1. Use the script first for deterministic extraction.
2. Inspect the generated Markdown when quality matters.
3. If the page is JavaScript-rendered, challenge-gated, or the script output is too thin, use an available browser/fetch tool to render the page, save HTML, then rerun with `--html`.
4. If the source is a PDF or a paper page, use a specialized PDF/paper skill when available. This skill is for generic web pages.
5. Inspect any generated visual notes. If a visual is a clear process diagram, architecture diagram, timeline, tree, or simple chart and you can accurately infer it, add a fenced `mermaid` block immediately after the visual note. Otherwise leave the note's Mermaid status as not inferred.
6. Validate the output before calling it final:

```bash
python3 skills/webpage-to-markdown/scripts/extract_url_markdown.py "<url>" --check-only <path/to/file.md>
```

## Output Naming

Default filename:

```text
<YYYYMMDD>-<title-or-domain-slug>.md
```

The title slug is lowercase, hyphen-separated, ASCII-only, and capped by `--name-chars`.

## Quality Bar

A completed Markdown capture should let a reader reconstruct the source page's main text content without opening the URL. For visuals, the Markdown must support two readers:

- **Multimodal reader**: can inspect linked local SVG assets.
- **Text-only reader**: can still understand that a visual existed, where it came from, what alt/caption/source metadata says, and whether any textual transcription or Mermaid equivalent is available.

Validation should confirm that local visual asset links exist. Never imply a text-only visual transcription is complete unless an agent actually inspected the visual or the source provided the text directly.
