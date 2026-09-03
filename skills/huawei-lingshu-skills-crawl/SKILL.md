---
name: huawei-lingshu-skills-crawl
description: Crawl all published and approved skills from the Huawei Lingshu Agent platform (灵枢Agent, cloudscope.ulanqab.huawei.com/lingshu-agent-alpha) onto the local machine for analysis. Discovers every skill via the agent-service REST API (using the authenticated browser session through opencli) and downloads each skill's complete source as a ZIP archive. Use when asked to harvest, archive, back up, or analyze Lingshu SRE agent skills — e.g. to study how existing SRE diagnostic skills are built, or to mine them for patterns.
---

# Huawei Lingshu Skills Crawl

Crawl the Lingshu Agent skill library (灵枢Agent Skill管理) into local
ZIP archives + extracted folders. Uses the user's authenticated Chrome
session via `opencli browser` — all REST calls are issued from page
context so cookies and the `Cftk` CSRF token are applied automatically.

## Quick Start

```bash
# Crawl everything (list all skills, download all zips, extract, index)
python3 skills/huawei-lingshu-skills-crawl/scripts/crawl_lingshu_skills.py

# Limit to published skills only
python3 skills/huawei-lingshu-skills-crawl/scripts/crawl_lingshu_skills.py --status published

# Fresh re-crawl (delete manifest, re-download everything)
python3 skills/huawei-lingshu-skills-crawl/scripts/crawl_lingshu_skills.py --refresh

# List only (no downloads)
python3 skills/huawei-lingshu-skills-crawl/scripts/crawl_lingshu_skills.py --list-only
```

No arguments needed in the common case — output goes to the skill's
`output/` directory (gitignored).

## Prerequisites

- **Chrome** with the opencli browser extension connected, logged into
  `cloudscope.ulanqab.huawei.com` (灵枢Agent). The page must be reachable
  without re-authentication.
- **opencli** on PATH (or in the usual npm global locations).

## How It Works

The Lingshu web app is a Vue SPA behind Huawei SSO. Its REST API lives
under `/lingshu-agent-alpha/copilot-rest/v1/agent-service/`. Direct
`requests`/`curl` calls fail because of the `Cftk` CSRF header
requirement; instead this skill runs `fetch()` **inside the page** via
`opencli browser eval`, which reuses the live session (cookies + token).

### API endpoints used

| Purpose | Method + Path |
|---|---|
| List skills (paginated) | `POST /skills/list?limit=10&offset=1&scope=ALL` with JSON body `{keyword,scene,status,...}` |
| Skill detail | `GET /skills/{uuid}/{versionUuid}` |
| File tree | `GET /skills/{uuid}/files?version_uuid={versionUuid}` |
| Download ZIP | `GET /skills/{uuid}/download?version_uuid={versionUuid}` → `application/octet-stream` (zip) |

All endpoints need header `Cftk: <cftk cookie value>` (read from the
`cftk` cookie on the page).

### Download strategy

For each skill the script downloads the **published version** when the
skill is `PUBLISHED` (`published_version_uuid`), otherwise the
**current version** (`current_version_uuid`) — so approved-but-unpublished
skills (已审批) are also captured. Skills with no downloadable version
(e.g. pending approval) are recorded in the manifest as skipped.

The ZIP is saved as `{output}/zips/{skill_name}-{version}.zip` and
extracted to `{output}/skills/{skill_name}/`.

## Output Structure

```
output/
├── manifest.json          # every discovered skill: metadata + download status
├── index.md               # human-readable index (name, 云服务, scene, versions, description)
├── zips/                  # raw ZIP archives, one per skill version
│   ├── modelarts-hardware-topology-1.0.7.zip
│   └── ...
└── skills/                # extracted skill folders
    ├── modelarts-hardware-topology/
    │   ├── SKILL.md
    │   ├── pipeline.graph.json
    │   ├── pipeline.py
    │   ├── scripts/ ...
    │   └── references/ ...
    └── ...
```

`index.md` includes a summary table by cloud service and scene, so you
can quickly answer "which DLI skills exist and what do they diagnose?".

## Resumability

- The manifest records `download_status` per skill (`downloaded` /
  `skipped` / `failed`) plus zip path and file count.
- Re-running skips skills already downloaded (zip exists on disk).
- `--refresh` deletes the manifest and re-crawls everything.
- A skill is marked failed only after the download endpoint itself
  fails; transient 502s are retried a few times.

## Limitations

- **Session-bound:** the crawl runs in the user's browser session; if
  the session expires mid-crawl, re-login in Chrome and re-run (resume
  picks up where it left off).
- **Rate:** a short delay between downloads (default 1.5 s) to be gentle
  on the backend; ~155 skills take a few minutes.
- **Version choice:** only one version per skill is downloaded (published
  if available, else current). Historical versions are not crawled
  (no list-versions endpoint was needed for this purpose).
- **Binary transfer through eval:** zips are base64-encoded in page
  context and decoded locally — fine for tens-of-KB skills, would need
  chunking for very large ones.
