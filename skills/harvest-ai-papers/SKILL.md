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

The generated summary must reflect selective oral papers only. For NeurIPS, ICML, and ICLR, use the official virtual oral events pages. For AAAI, do not treat the Main Track Oral Talks schedule as a selective oral-paper tier; it appears to be a broad main-track presentation schedule. Audit it in the notes if useful, but exclude it from the oral-only total unless AAAI publishes a true selective oral category.

Practical oral-summary notes:

- Count NeurIPS/ICML/ICLR oral papers from `https://<venue-host>/virtual/<year>/events/oral`, preferring explicit `Oral` labels and falling back to the page's `N Events` count when needed.
- Audit AAAI Main Track oral schedules by extracting layout text with `pypdf` and counting unique `Paper ID` values, but report the result as a broad schedule count and leave the selective oral count blank.
- AAAI's site may challenge-gate or block CLI fetches for some schedule URLs. The script keeps validated official-PDF schedule-count fallbacks for known years: AAAI-25 Main Track Oral Talks = 457, AAAI-26 Main Track Oral Talks = 1051.
- If `pypdf` is missing, install it into a temporary directory, for example `python3 -m pip install --target /private/tmp/pypdf-extract pypdf`, then run with `PYTHONPATH=/private/tmp/pypdf-extract`.

## Page Conversion Workflow

1. Read `config.yaml` for target venues and the output directory.
2. Read `prompt.md` before converting a URL; it contains the preservation requirements.
3. Fetch or open the source URL using the best available tool for the environment.
4. Create a Markdown file in the configured output directory.
5. Preserve page content in original order, including metadata, text, links, tables, citations, code blocks, images, captions, and footnotes.
6. For meaningful images, include the original image URL and add a clearly labeled assistant-derived visual equivalent for text-only readers.
7. Verify the resulting file exists, includes the source URL, includes all discovered image URLs, and has correctly fenced added diagrams.

## Output

Derive the filename from the page title:

- lowercase
- hyphen-separated
- no special characters
- `.md` extension

Keep added interpretation separate from original content. Do not summarize the page unless the user explicitly asks for a summary.
