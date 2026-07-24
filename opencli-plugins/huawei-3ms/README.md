# opencli-plugin-huawei-3ms

Search Huawei's **3MS 知识管理社区** ([3ms.huawei.com](https://3ms.huawei.com/)) — Huawei's
knowledge-management community (blogs, docs, forums, experts, courses) — and read a
document's full content.

Given an arbitrary question, `opencli huawei-3ms search` returns the **top N most
relevant documents**, each with title, type, author, source, date, summary, a
**docId**, and a detail URL. To get one document's **full body**, use
`opencli huawei-3ms read <detail_url>` with the `detail_url` from a `search` result.

3MS (Knowledge Online) is Huawei's broad knowledge-sharing platform — blogs,
documents, forums, expert profiles, and courses across every business unit
(运营商/企业/ICT BG/GTS/数字能源/华为云计算/半导体/终端/IAS/2012实验室…).

Requires a **logged-in Huawei session** via the OpenCLI Browser Bridge. The site is
a Vue SPA (Ant Design) behind Huawei SSO, so the adapter is a `COOKIE`-strategy
browser adapter: `search` drives your logged-in Chrome tab to the 3MS搜索 app
(`/doc3ms/index.html?...&text=<query>#/`) and scrapes the rendered result cards;
`read` drives it to a document's detail page and scrapes the full body.

## Prerequisites — human, one-time (an agent cannot do these)

This plugin drives your **logged-in Chrome** via the OpenCLI Browser Bridge, so
three things must be true before it works:

1. **OpenCLI + the Browser Bridge are installed** — see
   [`opencli-plugins/README.md`](../README.md). `opencli doctor` must be green.
2. **Chrome is running** with the Browser Bridge extension active.
3. **You are signed into `3ms.huawei.com` in that Chrome** — the adapter reuses
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
| `huawei-3ms search` | COOKIE | Search the 3MS knowledge base; returns top N documents (summary + docId + detail URL) |
| `huawei-3ms read` | COOKIE | Read one document's full body by docId (bare id or detail URL) |

## Usage

```bash
# Ask a question — returns the top 10 documents
opencli huawei-3ms search "大模型推理优化"

# Limit to 3 documents
opencli huawei-3ms search "盘古平台" --limit 3

# JSON output for agents
opencli huawei-3ms search "5G架构演进" -f json

# Search a specific tab/scope (default: community)
opencli huawei-3ms search "编码规范" --tab doc

# Read one document's full body — pass the detail_url from a search result
opencli huawei-3ms read "https://3ms.huawei.com/km/groups/3059465/blogs/details/22436113"

# ...or paste a detail URL straight from the browser
opencli huawei-3ms read "https://3ms.huawei.com/km/groups/3947070/blogs/details/22403734"

# search → read pipeline: search returns a detail_url per result, pass it to read
opencli huawei-3ms search "大模型" --limit 5 -f json   # → detail_url per result
opencli huawei-3ms read "<detail_url>"
```

`search` and `read` are complementary: `search` surveys many documents and
returns summaries **plus a `detail_url` per result**; `read` fetches one
document's full body. Take `detail_url` from any search result and pass it to
`read`. (A bare numeric docId is **not** accepted — 3MS detail URLs require the
group id, which a bare id doesn't carry.)

### `search` arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `query` (positional, required) | string | — | Your question or search term |
| `--limit` | int | 10 | Max number of documents to return (N) |
| `--tab` | string | `community` | Search scope: `community` \| `doc` \| `blog` \| `expert` \| `know` \| `external` |

### `search` columns

`rank`, `title`, `type`, `author`, `author_id`, `source`, `date`, `views`,
`likes`, `comments`, `summary`, `doc_id`, `detail_url`

`views`/`likes`/`comments` are enriched via the 3MS stats API
(`/api/projectspace/1-2-4/v1/statistics`); best-effort (empty if the API is
unreachable).

### `read` arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `doc_id` (positional, required) | string | — | A full `3ms.huawei.com` detail URL (take it from a search result's `detail_url`). A bare numeric id is not accepted — 3MS detail URLs require the group id. |

### `read` columns

`title`, `author`, `author_id`, `date`, `views`, `likes`, `comments`, `body`,
`comments_thread`, `url`

`body` is the document text. `comments_thread` is best-effort and often empty —
3MS blog detail pages lazy-load the comment thread via a widget/iframe that only
renders on interaction, so it is not reliably scrapable on a cold navigation. The
body is the primary content on 3MS.

## How it works (recon notes)

- `3ms.huawei.com` is a Vue SPA (Ant Design Vue) behind Huawei SSO. The homepage
  (`/next/map/index.html#/`) is a category-portal "Knowledge Online" page; its
  search box opens a **new tab** to a dedicated search app.
- **`search` drives the search app** at `/doc3ms/index.html?type=<tab>&l=zh&text=<urlencoded>#/`
  (title "3MS搜索"). The query goes in the `text` param, so the app runs the
  search on load — no input-filling needed for the initial query. Result cards
  are `.ant-list-item` (e.g. `.ant-list-item.blog`).
- **The docId is in the card's `<a href>`** (`/km/groups/<gid>/blogs/details/<docId>`)
  — directly available, no `window.open` intercept needed (unlike 稼先社区).
  The title lives in the `<a title="...">` attribute (with `<em>` highlight tags
  stripped). Author id comes from the `/Ufield/<id>` profile link.
- **Stats** (views/likes/comments): the search cards don't render counts inline,
  but the stats API `GET /api/projectspace/1-2-4/v1/statistics?moduleType=blog&resourceIds=<csv>`
  returns them per docId — called for the visible results to enrich the cards.
- **`read`** takes a full detail URL (`/km/groups/<gid>/blogs/details/<docId>` — the
  `detail_url` from `search`) and scrapes `#content-body` (fallback `.content`).
  The container mixes breadcrumb + meta (作者/日期/浏览/回复) + article body; the meta
  is parsed out and the body is the text after the "最近编辑时间" marker. A bare
  docId is rejected — 3MS detail URLs require the group id, and the group-less
  form (`/km/blogs/details/<id>`) redirects to the user profile, not the doc.

### Parts most likely to need adjustment

1. **`CARD_SELECTOR` + field selectors** (in `search.ts`/`search.js`) —
   `.ant-list-item` / `.ant-list-item-meta-title a[href]` / `a[href^="/Ufield/"]`.
   If the search-app markup changes, the adapter throws `EmptyResultError`.
   Inspect a real `/doc3ms/index.html?...` page with
   `opencli browser huawei-3ms state` / `opencli browser huawei-3ms find --css ...`.
2. **The search-app route + `text` param** — `search` depends on
   `/doc3ms/index.html?type=<tab>&l=zh&text=<urlencoded>#/` rendering cards. If the
   route or param name changes, inspect the URL a manual search produces.
3. **The stats API** (`/api/projectspace/1-2-4/v1/statistics`) — if the endpoint
   or its `resourceIds` param changes, stats go empty (search still works).
4. **`read`'s body selectors** — `#content-body` / `.content` and the meta-parsing
   regexes (`楼主…等级`, `日期：`, `浏览：`, `回复：`). If the detail page markup
   changes, `read` may return the raw container text or throw `EmptyResultError`.
5. **Comments are not extracted** — 3MS lazy-loads the comment thread (widget/
   iframe, interaction-gated). `comments_thread` is left empty. If you need
   comments, recon the comment widget's load trigger first.

## Development

```bash
# Each command has a typed source-of-truth (.ts) hand-mirrored to the .js entry
# OpenCLI loads. Keep both in sync after edits (no build step):
#   search.ts <-> search.js   ·   read.ts <-> read.js

# Verify the commands are registered:
opencli list | grep huawei-3ms

# Run them:
opencli huawei-3ms search "大模型" --limit 3
opencli huawei-3ms read 22436113
```
