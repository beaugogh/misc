---
name: huawei-wiki-crawl
description: Crawl and harvest Huawei CloudDevOps Wiki pages from a given wiki domain URL into Markdown files. Discovers all wiki pages in a domain via REST API or opencli browser DOM extraction, then harvests each page's content. Use when asked to scrape, harvest, archive, or bulk-download CloudDevOps wiki content for analysis, documentation preservation, or AI-agent reading.
---

# Huawei Wiki Crawl

Crawl a CloudDevOps wiki domain, discover all pages, and harvest each into
Markdown. Uses the CloudDevOps REST API for discovery and `opencli browser`
for content extraction (the wiki is a SPA requiring authenticated session).

## Quick Start

```bash
# Discover + harvest all pages in a wiki domain
python3 skills/huawei-wiki-crawl/scripts/crawl_wiki_domain.py \
  "https://clouddevops.huawei.com/domains/44072/wiki" \
  --output ./wiki --token <visionUserToken>

# Discovery only (build manifest, no harvesting)
python3 skills/huawei-wiki-crawl/scripts/discover_wiki_pages.py \
  "https://clouddevops.huawei.com/domains/44072/wiki" \
  --output ./wiki --token <visionUserToken>

# Harvest from existing manifest
python3 skills/huawei-wiki-crawl/scripts/crawl_wiki_domain.py \
  --manifest ./wiki/44072-manifest.json --output ./wiki

# Harvest a single page
python3 skills/huawei-wiki-crawl/scripts/crawl_wiki_domain.py \
  --url "https://clouddevops.huawei.com/domains/28786/wiki/2/WIKI2026030401189" \
  --output ./wiki
```

## Auth

The CloudDevOps wiki is a SPA requiring a `visionUserToken` JWT. Obtain it
via `opencli browser eval "localStorage.getItem('visionUserToken')"` when
the user is logged into CloudDevOps in Chrome (with the opencli browser
extension connected).

The token is used in two ways:
1. **REST API** (`Authorization` header) for discovery — listing kanbans
   and searching articles via `/devops-knowledge-management/api/`.
2. **opencli browser** — the browser session is already authenticated, so
   DOM extraction works without explicitly passing the token.

If no token is available, discovery falls back to:
1. `opencli browser` DOM extraction (navigate to the wiki page, parse
   categories from the rendered page).
2. Repo-code scan (scan `repos/` for `domains/<id>/wiki` URL references —
   partial, not the full wiki tree).

## Two-Phase Workflow

### Phase 1: Discovery (`discover_wiki_pages.py`)

1. Extract `domainId` from the input URL.
2. If token available:
   - `GET /wiki/kanban?domain_id=<id>` → list all wiki boards (kanbans).
   - For each kanban: `POST /v2/search/wiki` with `{kanbanId, domainId,
     pagination}` → paginated article list with `id`, `title`, `wikiSn`.
3. If no token: `opencli browser` DOM extraction, or repo-code scan.
4. Write `<output>/<domainId>-manifest.json`.

### Phase 2: Harvest (`crawl_wiki_domain.py`)

For each page in the manifest:

1. Navigate to the wiki page URL via `opencli browser default open <url>`.
2. Wait for the SPA to render (default 6 seconds).
3. Extract article content from the DOM via `opencli browser default eval`:
   - Content element: `.content-article-body-warp` (Angular component)
   - Fallbacks: `.wiki-content-wrapper`, `.right-content`
   - Extracts: title, breadcrumb path, innerText, innerHTML
4. Save as `<output>/<domainId>/<wikiSn>.md` with YAML frontmatter.
5. Skip already-harvested pages (resumable).
6. Update manifest with `harvest_status` per page.

## Output Structure

```
wiki/
├── 28786/
│   ├── WIKI2026030401189.md
│   ├── WIKI2021120200478.md
│   └── ...
├── 28786-manifest.json
├── 44072/
│   └── ...
└── 44072-manifest.json
```

## Resumability

The harvest is resumable — it skips pages whose output file already exists.
To re-harvest a page, delete its `.md` file or set `harvest_status: pending`
in the manifest.

## Limitations

- **SPA rendering:** CloudDevOps is a Single Page Application. Content
  extraction depends on `opencli browser` rendering the page. If the page
  is very large or slow to load, increase the wait time.
- **Rate limiting:** Default 2-second delay between pages. Adjust with
  `--delay`.
- **Token expiry:** The `visionUserToken` JWT expires (typically ~24h).
  Re-extract if harvesting spans multiple sessions.
- **Redirects:** Some wiki pages have been moved (redirect notice in the
  content). The harvester captures the redirect text but does not
  auto-follow.
