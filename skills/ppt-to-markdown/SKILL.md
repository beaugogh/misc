---
name: ppt-to-markdown
description: Use when asked to extract, convert, or transform a .pptx or .potx file into structured Markdown that preserves spatial layout, connector topology, group nesting, and shape-type semantics — not just flat text. Covers reading/parsing PowerPoint decks for analysis, archival, or downstream LLM consumption. Trigger whenever a .pptx needs to be read into Markdown and the structure matters (diagrams, flows, timelines, tables built from shapes).
---

# PPTX to Structured Markdown

Extract a `.pptx` deck into a structured Markdown file that preserves the
**spatial layout**, **connector topology**, **group nesting**, and
**shape-type semantics** that flat text extractions lose.

## Quick Start

```bash
python3 skills/ppt-to-markdown/scripts/extract_pptx_structured.py input.pptx
```

This writes `input_structured.md` next to the input file. Use `-o` for a
custom output path:

```bash
python3 skills/ppt-to-markdown/scripts/extract_pptx_structured.py input.pptx -o output.md
```

## Why not just `markitdown`?

`markitdown deck.pptx` produces a flat text dump — one block per slide,
all shape text in XML order. That's fine for prose-heavy slides, but it
**loses**:

| What's lost | Example impact |
|---|---|
| **Spatial layout** | A timeline's timestamps come out scrambled (07:11, 10:04, 07:22...) instead of left-to-right |
| **Connector topology** | "SRE → confirm → execute → verify" becomes four disconnected labels |
| **Group nesting** | A "recovery step" box (label + timestamp + icon) decomposes into separate items |
| **Shape semantics** | Diamonds, rectangles, arrows all become undifferentiated text |
| **Grid layouts** | Diagrams built from auto-shapes (not native tables) become label soup |

This skill preserves all five — plus a sixth: **slide image embedding**. Each
slide is exported as a PNG (via PowerPoint COM on Windows, or LibreOffice on
Linux) and embedded in the markdown as a base64 data URI. This faithfully
preserves complex tables, diagrams, and visual layouts that cannot be cleanly
rendered as markdown text.

## What the extraction captures per slide

1. **Slide title** (first text box near top, or core properties fallback)
2. **Slide image** — exported as PNG (via PowerPoint COM or LibreOffice) and
   embedded as a base64 data URI. This faithfully preserves complex tables,
   diagrams, swim lanes, timelines, and any visual layout that can't be
   rendered as markdown text. The image is the primary visual representation.
3. **Native tables** — rendered as Markdown tables (text-searchable supplement
   to the image)
4. **Content** — simple bullet list of all text shapes, sorted by reading
   order (top→bottom, left→right). Text-searchable supplement to the image.
5. **Speaker notes** — preserved

## Output format (example for a complex slide)

```markdown
## Slide 2

**Title:** 项目群任务书
**Shapes:** 32 | 1 tables | 0 connectors | 0 images

![Slide 2](data:image/png;base64,...)

### Tables

**Table 1:**

| 项目群名称 | 巫山云平台OBP项目 | 项目类型 | 平台项目 |
|---|---|---|---|
| 战略项目/战场 | 通过构建管理面容灾快恢平台... | | |
| 技术愿景 | 1、通过构建自动化改造... | | |

### Content

- 项目群任务书
- 管理面 | 容灾快恢平台
- 完成集群节点/AZ级切流能力集成到容灾管理平台...
- 10+云服务完成上车。覆盖10+Region...

**[Notes]** 1、技术生命周期中各个虚线框中补一下业务指标数据
```

## Config options (`config.yaml`)

```yaml
# Output
output_dir: ""                # empty = same dir as input
output_suffix: "_structured.md"
include_deck_summary: true
include_notes: true
truncate_text: 200            # max chars per content bullet
embed_slide_images: true      # export each slide as PNG and embed in markdown
image_embed_threshold: 10     # min shapes to trigger image embed (below = text only)
image_embed_max_kb: 500       # max image size to inline as base64 (larger = file ref)
```

## Visual QA

For verification, render the slides as images and compare against the
structured output:

**Option A — PowerPoint COM (Windows, if Office is installed):**

```python
import comtypes.client
ppt = comtypes.client.CreateObject("PowerPoint.Application")
pres = ppt.Presentations.Open(r"C:\path\to\deck.pptx", ReadOnly=True, WithWindow=False)
for i, slide_num in enumerate([5, 9, 17], 1):
    pres.Slides(slide_num).Export(f"slide-{slide_num:02d}.png", "PNG", 1920, 1080)
pres.Close()
ppt.Quit()
```

**Option B — LibreOffice (from the Anthropic pptx skill):**

```bash
python skills/anthropic-skills/skills/pptx/scripts/thumbnail.py deck.pptx thumbs
```

This requires LibreOffice (`soffice`) and `pdftoppm` (Poppler).

## Dependencies

- `python-pptx` — `.pptx` parsing (`pip install python-pptx`)
- `lxml` — XML parsing for OOXML internals (`pip install lxml`)
- `pyyaml` — config loading (`pip install pyyaml`)
- Optional: `comtypes` (Windows COM automation for PowerPoint slide image export)
- Optional: LibreOffice + `pdftoppm` (Linux/cross-platform slide image export fallback)

## Relationship to the Anthropic pptx skill

The [Anthropic pptx skill](../anthropic-skills/skills/pptx/) handles
**creating, editing, validating, and thumbnailing** decks. This skill
complements it by **reading** decks into structured Markdown — the one
task the Anthropic skill delegates to `markitdown` (flat text only).

Use together:
1. Use **this skill** to extract structured Markdown from an existing deck
2. Use the **Anthropic pptx skill**'s `thumbnail.py` for visual QA
3. Use the **Anthropic pptx skill**'s `validate.py` if you modify the deck
