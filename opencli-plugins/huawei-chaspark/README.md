# opencli-plugin-huawei-chaspark

Search Huawei's **黄大年茶思屋** academic community ([chaspark.com](https://www.chaspark.com/#/home))
— Huawei's academic/paper community (papers, videos, patents, conferences) — and
read an item's full content.

Given an arbitrary question, `opencli huawei-chaspark search` returns the
**top N most relevant items**, each with title, type, date, views, summary, an
**item_id**, and a detail URL. To get one item's **full content**, use
`opencli huawei-chaspark read <detail_url>` with the `detail_url` from a `search`
result.

黄大年茶思屋 (ChASPark — Chaspark Academic Spark) is Huawei's academic
knowledge community: papers (论文分享), academic hotspots (学术热点), patents
(查思专利), conferences (学术会议), and domain channels (数学/材料科学/难题揭榜/
科技赛事/开源/数据集/视频/专题/圈子).

Requires a **logged-in Huawei session** via the OpenCLI Browser Bridge. The site
is a Vue SPA behind Huawei SSO, so the adapter is a `COOKIE`-strategy browser
adapter: `search` calls the chaspark search JSON API directly
(`/chasiwu/v1/content/search`, with the CSRF token from the `X-CSRF-TOKEN`
cookie) — the SPA's card rendering doesn't reliably fire under `page.goto`, but
the API returns clean JSON; `read` drives the tab to an item's detail page and
scrapes the content.

## Prerequisites — human, one-time (an agent cannot do these)

This plugin drives your **logged-in Chrome** via the OpenCLI Browser Bridge, so
three things must be true before it works:

1. **OpenCLI + the Browser Bridge are installed** — see
   [`opencli-plugins/README.md`](../README.md). `opencli doctor` must be green.
2. **Chrome is running** with the Browser Bridge extension active.
3. **You are signed into `chaspark.com` in that Chrome** — the adapter reuses
   this session's cookies; if it's not signed in, every call fails with an auth
   error.

Then run [`setup.sh`](#setup-automatable) to install + verify.

## Setup (automatable)

```bash
./setup.sh
```

Verifies opencli + the Browser Bridge, installs the plugin, ensures the
`@jackwener/opencli` peer-dep symlink (hoisted to the repo root — see
[`opencli-plugins/README.md`](../README.md)), and runs a smoke-test search.

> **Note on TypeScript:** the commands are written in `search.ts`/`read.ts` and
> hand-mirrored to `search.js`/`read.js` (no build step). `package.json` is
> `"type":"module"`, so the `.js` files use ES `import`. If you edit a `.ts`,
> apply the same change to its `.js`. Keep the two in sync.

## Commands

| Command | Strategy | Description |
|---------|----------|-------------|
| `huawei-chaspark search` | COOKIE | Search chaspark; returns top N items (summary + item_id + detail_url) |
| `huawei-chaspark read` | COOKIE | Read one item's full content by detail_url (paper body or video summary + transcript) |

## Usage

```bash
# Ask a question — returns the top 10 items
opencli huawei-chaspark search "大模型"

# Limit to 3 items
opencli huawei-chaspark search "光通信" --limit 3

# JSON output for agents
opencli huawei-chaspark search "AI安全" -f json

# Read one item's full content — pass the detail_url from a search result
opencli huawei-chaspark read "https://www.chaspark.com/#/research/paper/1298427126325977088"

# ...or a video
opencli huawei-chaspark read "https://www.chaspark.com/#/stw/media/1298064463498584064"

# search → read pipeline: search returns a detail_url per result, pass it to read
opencli huawei-chaspark search "大模型" --limit 5 -f json   # → detail_url per result
opencli huawei-chaspark read "<detail_url>"
```

`search` and `read` are complementary: `search` surveys many items and returns
summaries **plus a `detail_url` per result**; `read` fetches one item's full
content. Take `detail_url` from any search result and pass it to `read`.

### `search` arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `query` (positional, required) | string | — | Your question or search term |
| `--limit` | int | 10 | Max number of items to return (N) |

### `search` columns

`rank`, `title`, `type`, `author`, `date`, `views`, `summary`, `item_id`,
`detail_url`

`type` is the chaspark `columnType` (e.g. `subjectUniversal`). `detail_url` is
the item's route (e.g. `https://www.chaspark.com/#/s/<id>`) — pass it to `read`.

### `read` arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `detail_url` (positional, required) | string | — | A full `chaspark.com` detail URL from a search result's `detail_url` (paper `#/research/paper/<id>` or video `#/stw/media/<id>`) |

### `read` columns

`title`, `author`, `author_id`, `date`, `views`, `likes`, `comments`, `body`,
`url`

`body` is the article text for papers (`.style_m_text__hMFtq`); for videos it's
the AI video summary + transcript. `likes`/`comments` are not rendered on the
detail page and left empty.

## How it works (recon notes)

- `chaspark.com` is a Vue SPA (Ant Design) behind Huawei SSO. The homepage
  (`#/home`) is a recommendation feed (茶思头条荟萃 / 综合推荐).
- **`search` calls the JSON API directly**: `GET /chasiwu/v1/content/search?searchTxt=<q>&size=<N>&...`
  with the `X-CSRF-TOKEN` header (value from the `X-CSRF-TOKEN` cookie) and
  `Column-Type: searchDoc`. Returns `{ data: { records: [...] } }` with fields
  `id`, `title`, `columnType`, `creatorName`, `publishTime` (Unix seconds),
  `views`/`likes`/`comments`, `subjectIntroduction`, `route` (the detail URL).
  The API path was chosen over scraping cards because the SPA's card rendering
  doesn't reliably fire under the plugin's `page.goto` (CDP `Page.navigate`
  leaves the page's JS in a state where the search XHR doesn't fire), while the
  API returns clean JSON with just the session cookies + CSRF token.
- **`read`** navigates to the detail URL and branches on type:
  - **paper** (`#/research/paper/<id>`): title in `h2`, body in
    `.style_m_text__hMFtq` (the full article).
  - **video/live** (`#/stw/media/<id>`, `#/live/<id>`): title in `h2`, body =
    the "AI视频摘要：" summary + the transcript segments (`trackItem__` time +
    content). The video player chrome (vjs-*) is not scraped.
  - **subject** (`#/s/<id>`): topic-landing pages with little readable text;
    returns title + metadata, no article body.

### Known limitation

`read` uses `page.goto` to load the detail page, which (like the search cards)
can land title-only under the plugin's CDP navigation. Paper/video/subject pages
may return empty bodies when this happens. The search command (API-based) is
reliable; `read` is best-effort. Re-running often helps when the page load
settles.

### Parts most likely to need adjustment

1. **The search API** (`/chasiwu/v1/content/search`) — if the endpoint, its
   `searchTxt` param, or the CSRF token cookie name (`X-CSRF-TOKEN`) changes,
   search breaks. Inspect a manual search's network tab in Chrome.
2. **`read`'s body selectors** — paper `.style_m_text__hMFtq` / video
   `trackItem__` + `AI视频摘要：`. If the detail page markup changes, `read`
   may return the raw container text or throw `EmptyResultError`.
4. **Tabs** — the `--tab` options map to Chinese tab labels (综合/视频/文章/…)
   clicked in-page; if the labels change, the tab filter no-ops (search still
   returns 综合 results).

## Development

```bash
# Each command has a typed source-of-truth (.ts) hand-mirrored to the .js entry
# OpenCLI loads. Keep both in sync after edits (no build step):
#   search.ts <-> search.js   ·   read.ts <-> read.js

# Verify the commands are registered:
opencli list | grep huawei-chaspark

# Run them:
opencli huawei-chaspark search "大模型" --limit 3
opencli huawei-chaspark read "https://www.chaspark.com/#/research/paper/1298427126325977088"
```
