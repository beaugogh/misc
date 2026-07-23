---
name: analyze-paper-corpus
description: >
  Analyzes a corpus of harvested academic papers (markdown files from top AI venues or
  arXiv) against a reference/context document (e.g., a design brainstorm, project
  proposal, or system architecture doc). Extracts abstracts from all papers, screens
  each against the reference context, flags only papers with genuinely novel and
  relevant ideas, and composes a structured findings document organized by topic.
  Use when the user has a harvested paper corpus and a design/planning document, and
  wants to mine the corpus for ideas that expand their thinking — not to summarize
  every paper, but to ruthlessly filter to what matters. Handles corpora of 500-2000+
  papers via parallel abstract screening followed by selective deep-read of the most
  promising hits.
---

# Analyze Paper Corpus Against a Reference Document

## What this skill does

Given:
- A **reference document** (any `.md` file — a design brainstorm, project proposal,
  system architecture, etc.) that defines the context, goals, and known patterns of
  a project.
- A **paper corpus** (a directory of `.md` files, each a harvested paper with
  frontmatter + title + abstract + body). Typically produced by the
  `harvest-ai-papers` skill, but any directory of paper markdown files works.

Produces:
- A **findings document** (`paper_findings.md`) where each flagged paper has:
  - Paper info (title, venue, year)
  - TL;DR (why relevant to the reference project — 1-3 sentences)
  - Methodology & novelty (concise but specific — bullet points with concrete
    mechanisms, numbers, and project connections)
- Papers are **organized by topic** (not by reading order), with a category overview
  table showing each topic's paper count and weight percentage.

## When to use

- "Read these 1000+ papers and find what's relevant to my project design."
- "Screen this paper corpus against our architecture doc and flag novel ideas."
- "Mine the harvested papers for anything that expands our thinking beyond what we
  already know."

## Prerequisites

- A reference document (`.md`) defining the project context, goals, and already-known
  patterns/technologies. This is the "lens" through which papers are screened.
- A paper corpus directory containing `.md` files with extractable abstracts (papers
  should have frontmatter with `title:` and an `Abstract` or `## Abstract` section
  near the top).

## The pipeline — run these in order

### Step 1 — Extract abstracts

Extract title + abstract from every `.md` paper in the corpus into a single
compact file. Each paper gets ~500 chars of abstract — enough to judge relevance
without reading the full paper.

```python
# extract_abstracts.py — see bundled script
# Reads all .md files in the corpus dir, extracts title + abstract, writes to a
# single output file. Capped at 8KB per paper (abstract is always near top).
```

Or inline:
```python
import os, re
papers_dir = "<corpus_dir>"
output_file = "all_abstracts.txt"
papers = []
for root, dirs, files in os.walk(papers_dir):
    for f in sorted(files):
        if not f.endswith(".md"):
            continue
        # ... extract title from frontmatter, extract abstract section
        # ... cap abstract at 500 chars
papers.append(f"### {title}\n{abstract}\n")
# write all to output_file
```

### Step 2 — Split into chunks for parallel screening

Split the abstracts file into ~8-10 chunks (130-150 abstracts each). This allows
parallel agent screening — each agent reads ~130 abstracts and flags only papers with
genuinely novel ideas.

```bash
# Split by line count (each paper = ~3 lines: ### title, abstract, blank)
split -l 440 -d all_abstracts.txt chunk_
```

### Step 3 — Parallel abstract screening

Launch one agent per chunk. Each agent receives:
1. The chunk file to read.
2. A **context summary** of the reference document — distilled to: project name, what
   it does, key architecture, known patterns (so the agent doesn't re-flag what's
   already known).
3. Instructions to flag only papers with **genuinely novel** ideas that **expand
   thinking** — not duplicates of known patterns, not irrelevant domains.
4. Output format: per flagged paper, return title + 1-2 sentence novel insight + which
   project design aspect it informs.

**Critical instruction for agents:** "Be ruthless — only flag papers that genuinely add
something new. Skip silently if irrelevant or duplicating known patterns."

### Step 4 — Consolidate and deduplicate

Collect all flagged papers from all agents. Deduplicate by normalized title (some papers
may appear in multiple chunks). Remove any entries marked "已列出" or "already listed."

### Step 5 — Optional: Deep-read the most promising hits

For the top ~20-30 flagged papers (those rated highest relevance), read the full paper
(not just abstract) to extract detailed methodology and actionable insights. This is
optional — the abstract-level findings may be sufficient for a phase-1 brainstorm.

### Step 6 — Categorize by topic

Assign each paper to a topic category based on which aspect of the reference project
it informs. Categories should be derived from the reference document's structure (e.g.,
if the reference doc has sections on "evaluation," "memory," "safety," those become
categories). Common categories for agent/AI projects:

- 评估工程与遥测 (Evaluation engineering & telemetry)
- 记忆、检索与上下文管理 (Memory, retrieval & context management)
- 多 Agent 协调与拓扑 (Multi-agent coordination & topology)
- 安全、护栏与合规 (Safety, guardrails & compliance)
- 成本、预算与效率 (Cost, budget & efficiency)
- 规划、推理与验证 (Planning, reasoning & verification)
- Agent 训练与自改进 (Agent training & self-improvement)
- 知识图谱与 RAG (Knowledge graph & RAG)
- 运维特定 (Ops-specific: event-driven, anomaly detection, RCA)
- Agent 架构与工具系统 (Agent architecture & tool system)

### Step 7 — Compose the findings document

Write `paper_findings.md` with:

1. **Header**: source corpus description, paper count, usage note.
2. **Big-picture insight** (see Step 8) — placed before the category table so the reader
   sees the forest before the trees.
3. **Category overview table**: category name, paper count, weight percentage.
4. **Papers organized by category** (not by reading order). Each paper:
   - `### Title` (no A/B batch prefixes)
   - `- **论文：** Full title (Venue Year)`
   - `- **TL;DR：** Why relevant (1-3 sentences)`
   - `- **方法与新颖性：**` with bullet points (concrete mechanisms, numbers, project connections)
5. **Cross-cutting themes** at the end: 5-10 convergence patterns observed across
   multiple papers.

### Step 8 — Identify trends, frontiers, and the next step

After consolidating all paper findings, step back and analyze the corpus as a whole to
identify where the field is heading. This is the most valuable output for strategic
planning — it turns a paper list into actionable foresight.

Produce a **big-picture insight section** with:

1. **Evolution trajectory**: a simple timeline showing how the field got here and where
   it's going (e.g., "LLM training → Agent loops → Harness infrastructure → [current
   bottleneck] → [predicted next frontier]"). Ground each transition in evidence from
   the corpus (e.g., "41% of papers are about evaluation → evaluation is the current
   bottleneck").

2. **Top signals (3-7)**: the strongest patterns emerging across multiple papers. For
   each signal:
   - **What the signal is** (one sentence)
   - **Evidence from the corpus** (which papers, what numbers — e.g., "41% of flagged
     papers are about evaluation; SAP's two-dimensional taxonomy; The Obfuscation Atlas
     on benchmark gaming")
   - **Prediction**: what this means for the next 1-2 years (concrete, falsifiable)

3. **The convergence point**: if you see one, identify the meta-pattern that connects
   everything — the "holy grail" the field is converging toward. Frame it as a set of
   capabilities that no system achieves simultaneously today, where each paper contributes
   a piece of the puzzle.

4. **Implication for the reference project**: connect the trends back to the user's
   specific project (the reference document). Which architecture choices are validated?
   Which should be reconsidered? Where can the project get ahead of the curve?

5. **Honest caveats**: acknowledge that these are inferences from a limited corpus, not
   predictions you're certain about. Note what could invalidate each prediction. Note
   what's missing from the corpus (industry labs, open-source projects, other fields).

**Key principles for this step:**

- **Ground every claim in corpus evidence.** Don't say "the field is moving toward X"
  without citing which papers show X. "41% of papers are about evaluation" is evidence;
  "evaluation is important" is not.
- **Be honest about uncertainty.** Distinguish "strong signal across many papers" from
  "interesting idea from one paper." Acknowledge that predictions could be wrong.
- **Distinguish signal from fad.** A real frontier has concrete mechanisms across
  multiple independent papers (evaluation engineering, self-improvement loops). A fad
  has many papers but no convergence on mechanisms (or mechanisms that don't survive
  production deployment).
- **Connect to the reference project.** This isn't a generic trend report — it's
  strategic foresight for the user's specific design. Every trend should answer "so
  what should we do differently in our project?"
- **The category distribution itself is a signal.** If 41% of relevant papers are about
  evaluation, that's the strongest signal about where the field's bottleneck is. The
  distribution table is not just an index — it's data.

## Key design principles

- **No pre-fixed selection count.** Don't say "select the top 100 papers." Read every
  abstract and flag however many (or few) are genuinely novel. The count emerges from
  the screening, not from a quota.
- **Ruthless filtering.** The agent should skip >90% of papers silently. Only flag
  papers that would change how you think about the reference project.
- **Topic organization, not reading-order.** The reader wants to find papers by
  "what design aspect does this inform," not by "which batch was this read in."
- **Reference document is the lens.** Every paper is judged against the reference
  doc's context, goals, and known patterns. A paper about "multi-agent reinforcement
  learning" is irrelevant if the reference doc is about a text-based devops agent —
  unless it has a transferable architectural pattern.
- **Already-known patterns must be listed in the screening prompt.** Otherwise agents
  will re-flag papers that duplicate what the reference doc already covers. Extract the
  known-patterns list from the reference doc before launching screening agents.
- **Abstracts are sufficient for screening.** Full-paper deep reads are a separate
  optional step for the top hits only. Don't deep-read every paper — that's
  infeasible for 1000+ paper corpora.

## Scaling

- **500 papers**: 4 chunks × ~125 abstracts each. ~5 minutes wall-clock with 4 agents.
- **1,000 papers**: 8 chunks × ~125 each. ~8 minutes.
- **2,000+ papers**: 12-16 chunks. ~12 minutes. Agent concurrency cap may queue some
  chunks — they complete as slots free up.

## Output file structure

```
paper_findings.md
├── # Title + usage note
├── ## 分类概览 (category overview table with counts + percentages)
├── ## Category 1 (N 篇)
│   ├── ### Paper 1
│   │   ├── 论文 info
│   │   ├── TL;DR
│   │   └── 方法与新颖性
│   ├── ### Paper 2
│   └── ...
├── ## Category 2 (N 篇)
│   └── ...
└── ## Cross-cutting themes (5-10 convergence patterns)
```

## Relationship to harvest-ai-papers

This skill is the **downstream consumer** of `harvest-ai-papers`. The harvest skill
collects papers from top AI venues into markdown files. This skill reads those files,
screens them against a reference document, and produces a findings report. They compose:

```
harvest-ai-papers → [paper .md files] → analyze-paper-corpus → [paper_findings.md]
```

## Scripts

| Script | What it does |
|---|---|
| `extract_abstracts.py` | Reads all `.md` papers in a directory, extracts title + abstract, writes to a single compact file. |
