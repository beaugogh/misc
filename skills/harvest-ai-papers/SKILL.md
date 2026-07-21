---
name: harvest-ai-papers
description: Use when asked to list, inventory, harvest, preserve, or convert top AI venue paper pages, conference paper pages, proceedings pages, or AI research URLs into Markdown for downstream AI-agent reading, including NeurIPS, ICML, ICLR, AAAI, images, metadata, citations, and AI-readable visual equivalents.
---

# Harvest AI Papers

Use this skill to inventory top AI venue papers and turn AI paper, proceedings, conference, or research webpage URLs into faithful Markdown captures suitable for another AI agent.

## Venue Paper Inventory

When the user asks to list or size the papers for the configured venues, run:

```bash
python3 skills/harvest-ai-papers/scripts/list_venue_papers.py --year <year>
```

If the user does not provide a year, use the script default.

This writes:

- `skills/harvest-ai-papers/output/ai-venue-papers-<year>.csv`
- `skills/harvest-ai-papers/output/ai-venue-papers-<year>-summary.md`

The CSV is a broad accepted/proceedings workload inventory. The Markdown summary is oral-only.

The inventory script uses non-gated listing sources:

- NeurIPS: official downloads page, falling back to the previous year when the current conference has not started
- ICML: official downloads page
- ICLR: official downloads page
- AAAI: DBLP proceedings page with DOI links

The generated CSV is a broad accepted/proceedings workload estimate, not an oral-only list. Count only links with paper/poster semantics where the listing source includes workshops or other events, and preserve the presentation type when the source exposes it.

The generated summary must reflect oral papers only. For NeurIPS, ICML, and ICLR, use the official virtual oral events pages. For AAAI, count **Main Track Oral Talks only** from the official Main Track Oral Talks PDF. Exclude AISI, AIA, ETA, workshops, and other special-track oral schedules unless the user explicitly asks for them.

Practical oral-summary notes:

- Count NeurIPS/ICML/ICLR oral papers from `https://<venue-host>/virtual/<year>/events/oral`, preferring explicit `Oral` labels and falling back to the page's `N Events` count when needed.
- Count AAAI Main Track oral schedules by extracting layout text with `pypdf` and counting unique `Paper ID` values.
- AAAI's site may challenge-gate or block CLI fetches for some schedule URLs. The script keeps validated official-PDF fallbacks for known years: AAAI-25 Main Track Oral Talks = 457, AAAI-26 Main Track Oral Talks = 1051. Prefer the direct AAAI-26 PDF URL `https://aaai.org/wp-content/uploads/2026/01/Main-track-oral-talks.pdf`.
- If `pypdf` is missing, install it into a temporary directory, for example `python3 -m pip install --target /private/tmp/pypdf-extract pypdf`, then run with `PYTHONPATH=/private/tmp/pypdf-extract`.

## Oral Harvesting Workflow

Harvesting must focus on oral papers only unless the user explicitly changes scope.

First build the oral-only manifest:

```bash
python3 skills/harvest-ai-papers/scripts/build_oral_manifest.py --year <year>
```

This writes:

- `skills/harvest-ai-papers/output/ai-venue-oral-papers-<year>.csv`

Manifest sources:

- NeurIPS, ICML, and ICLR: official virtual oral event pages, one row per oral event URL.
- AAAI: official Main Track Oral Talks PDF, one row per unique Paper ID. These rows may be marked `needs_paper_url` when the PDF does not expose a stable paper page URL directly.

Then harvest only rows marked `ready`:

```bash
python3 skills/harvest-ai-papers/scripts/harvest_manifest.py --year <year>
```

Useful pilot command:

```bash
python3 skills/harvest-ai-papers/scripts/harvest_manifest.py --year <year> --venue ICLR --limit 10
```

Do not harvest broad proceedings CSV rows for this workflow. Use the broad CSV only for workload planning or URL reconciliation.

Harvested filenames must use this pattern:

```text
<YEAR>-<VENUE>-<paper-title-slug-capped>.md
```

The default cap for the paper-title slug is 80 characters; change it with `--name-chars` when needed.

Harvesting must capture the whole paper, not just the conference detail page. Use the conference page to discover the actual paper PDF or canonical paper URL, then preserve the full paper from title, authors, abstract, all body sections, references, and appendices/supplemental material when available. Do not write a completed harvest file from a conference landing page, abstract page, schedule page, slide deck, or short metadata page.

The harvester enforces a minimum word count before writing each file. The default is 3000 words; change it with `--min-words` only for unusually short papers after manual inspection. A completed harvest must include a references or bibliography section.

For figures, images, and charts, include an AI-readable representation:

- Prefer Mermaid when the figure is a reconstructible workflow, architecture, tree, timeline, or chart.
- Otherwise convert extracted PDF images/figures into SVG assets and reference those SVGs from the Markdown.
- Keep captions and nearby explanatory text with the figure whenever the source exposes them.

The default harvester expects PyMuPDF for whole-paper PDF extraction and SVG figure assets. If it is missing, install it into a temporary directory, for example `python3 -m pip install --target /private/tmp/pymupdf pymupdf`, then run with `PYTHONPATH=/private/tmp/pymupdf`.

## Page Conversion Workflow

1. Read `config.yaml` for target venues and the output directory.
2. Build or read the oral-only manifest and select only rows whose `presentation_type` is `Oral`.
3. Read `prompt.md` before converting a URL; it contains the preservation requirements.
4. Fetch or open the source URL using the best available tool for the environment.
5. Create a Markdown file in the configured output directory using the `<YEAR>-<VENUE>-<paper-title-slug-capped>.md` filename pattern.
6. Preserve the whole paper in original order: title, authors, abstract, every section, references, appendices, citations, equations, tables, code blocks, figures, captions, and footnotes.
7. For meaningful images, figures, and charts, include SVG assets or Mermaid equivalents and add a clearly labeled assistant-derived visual equivalent for text-only readers.
8. Verify the resulting file exists, includes the source URL and paper PDF URL when applicable, includes all extracted figure asset links, and has correctly fenced added diagrams.

## Output

Derive the filename from the data year, venue, and paper title:

- prefix with `<YEAR>-<VENUE>-`
- lowercase hyphen-separated title slug
- cap the title slug length, default 80 characters
- no special characters
- `.md` extension

Keep added interpretation separate from original content. Do not summarize the page unless the user explicitly asks for a summary.
