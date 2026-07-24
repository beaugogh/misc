# opencli-plugin-huawei-jiaxian

Search Huawei's **稼先社区** ([jx.huawei.com](https://jx.huawei.com/)) — the internal
expert-and-engineer knowledge community — and get your questions answered from the
community's collective expertise.

Given an arbitrary question, `opencli huawei-jiaxian search` returns the **top N most relevant
documents**, each with title, type, author, date, views, replies, a **rich summary** (author +
abstract + expert viewpoints), and a URL. The rich summaries carry enough substance for a
downstream agent or reader to triage the question. To get one post's **full article body**, use
`opencli huawei-jiaxian read <postId>` with a postId from a detail URL you have.

稼先社区 is Huawei's high-density technical-discussion space (6,000+ chief experts, 100,000+ R&D
engineers), focused on deep technical exploration, architecture evolution, and cross-domain
problem-solving rather than routine business-process Q&A.

Requires a **logged-in Huawei session** via the OpenCLI Browser Bridge. The site is a Vue SPA with
no public search API, so the adapter is a `COOKIE`-strategy browser adapter: it drives your
logged-in Chrome tab, fills the search box the Vue-reactive way, clicks the search button, and
scrapes the rendered result cards.

## Prerequisites — human, one-time (an agent cannot do these)

This plugin drives your **logged-in Chrome** via the OpenCLI Browser Bridge, so three things must be
set up by a human before any agent (or `setup.sh`) can use it:

1. **Node.js ≥ 20** on the machine — https://nodejs.org
2. **OpenCLI + the Browser Bridge extension** — install opencli (`npm i -g @jackwener/opencli`),
   then add the **OpenCLI** extension to Chrome from the
   [Chrome Web Store](https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk)
   (or load it unpacked from the [GitHub Releases](https://github.com/jackwener/opencli/releases)
   zip). Keep Chrome running.
3. **Sign in to https://jx.huawei.com/** in Chrome with your Huawei account. The adapter reuses
   this session's cookies — if it's not signed in, every search fails with an auth error.

`opencli doctor` (run by `setup.sh`) verifies step 2; the smoke test at the end of `setup.sh`
verifies step 3.

## Setup (automatable)

From this directory, an agent (or you) runs:

```bash
./setup.sh
```

It verifies Node/opencli, checks `opencli doctor` is green, installs the plugin, ensures the
`@jackwener/opencli` peer-dep symlink at the **repo root** (not per-plugin — see
[`opencli-plugins/README.md`](../README.md)), and runs a smoke-test search. If a human prerequisite
is missing, it prints exactly what the human needs to do and exits. Safe to re-run.

<details>
<summary>Manual setup (what <code>setup.sh</code> does, if you'd rather run the steps by hand)</summary>

```bash
npm install -g @jackwener/opencli          # Node >= 20
opencli doctor                               # must be green — Browser Bridge connected
opencli plugin install D:/workspace/misc/opencli-plugins/huawei-jiaxian

# Ensure the peer-dep symlink. Hoist it to the REPO ROOT (not the plugin dir)
# so the plugin folder stays clean — Node's resolver walks up from search.js,
# so <repo>/node_modules/@jackwener/opencli resolves the import. Run from the
# repo root:
cd D:/workspace/misc
mkdir -p node_modules/@jackwener
ln -s "$(npm root -g)/@jackwener/opencli" node_modules/@jackwener/opencli

opencli huawei-jiaxian search "大模型" --limit 1   # smoke test
```

From GitHub (after pushing):
```bash
opencli plugin install github:<user>/misc/opencli-plugins/huawei-jiaxian
```

</details>

> **Note on TypeScript:** the command is written in `search.ts` and hand-mirrored to `search.js`
> (stripped type annotations, double quotes — no build step, no tsconfig). The committed
> `search.js` is what OpenCLI actually loads (it discovers `search.*` by convention and Node can't
> run `.ts` directly). If you edit `search.ts`, apply the same change to `search.js`. Keep the two
> in sync.

## Commands

| Command | Strategy | Description |
|---------|----------|-------------|
| `huawei-jiaxian search` | COOKIE | Search the 稼先社区 knowledge base; returns top N documents (rich summaries, not full bodies) |
| `huawei-jiaxian read` | COOKIE | Read one post's full body by postId (bare id or detail URL) |

## Usage

```bash
# Ask a question — returns the top 10 documents (rich summaries)
opencli huawei-jiaxian search "大模型推理优化"

# Limit to 3 documents
opencli huawei-jiaxian search "盘古2.0昇腾性能" --limit 3

# JSON output for agents
opencli huawei-jiaxian search "5G架构演进" -f json

# Read one post's full body — by bare postId
opencli huawei-jiaxian read da25639435334344912733f65c592a1b

# ...or by pasting the detail URL straight from the browser
opencli huawei-jiaxian read "https://jx.huawei.com/community/comgroup/postsDetails?postId=da25639435334344912733f65c592a1b&type=freePost"
```

`search` and `read` are complementary: `search` surveys many posts and returns
rich summaries (enough to triage); `read` fetches one post's complete article
body when you need the full text.

### `search` arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `query` (positional, required) | string | — | Your question or search term |
| `--limit` | int | 10 | Max number of documents to return (N) |
| `--language` | string | `cn` | Source language: `cn` \| `en` |

### `search` columns

`rank`, `title`, `type`, `author`, `date`, `views`, `replies`, `summary`, `url`

### `read` arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `post_id` (positional, required) | string | — | A bare 32-char hex postId, or a full `jx.huawei.com` detail URL |
| `--type` | string | `free_post` | Resource type: `free_post` \| `technical_report` \| `industry_report` (only `free_post` supported) |

### `read` columns

`title`, `author`, `author_id`, `dept`, `date`, `views`, `likes`, `replies`, `body`, `url`

## How it works (recon notes)

- `jx.huawei.com` is a Vue SPA (Vue + axios + echarts, hash-routed, login-gated behind Huawei SSO).
- `opencli analyze` classifies the homepage as **Pattern C** (no JSON XHR, HTML scrape). No public
  search API was observed.
- **Search results render inline on the homepage** (not on a separate route). After submitting,
  result cards replace/augment the homepage feed — the URL does not change.
- **The search trigger** is the subtle part. The input is `input.form-control` (placeholder
  "搜内容 搜话题"). The submit button is `.search-btn` (text "搜索"), which **only appears after
  typing**. Filling the input with `page.type` leaves its value `undefined` because Vue's `v-model`
  reactivity isn't triggered by synthetic typing. The adapter therefore sets the value via the
  native `HTMLInputElement.value` setter and dispatches `input` + `change` events (all inside one
  `page.evaluate`, to avoid stale element refs across separate opencli calls), then clicks
  `.search-btn`.
- **Result-card markup** (all confirmed against a live results render):
  - card root: `.recommended-page-list-item`
  - type: `.contention-page-content-type-item` (e.g. "思想简报")
  - title: `.contention-page-content-title`
  - **rich summary**: `.contention-page-content-summary` — its `title` attribute holds the
    **untruncated** author + abstract + expert-viewpoints text (the visible `textContent` is cut
    off by an `ellipsis-1` class). This is the field that makes the documents substantial enough
    to serve as answers.
  - author: `.author-name`  ·  date: `.create-time`
  - stats: `.stat-item` (1st = views, 2nd = replies)
- **Detail-page URLs** for `search` results are not obtainable from a homepage card: the cards
  carry no `postId` in their DOM/attributes, and clicking one fires only a telemetry XHR (no
  navigation, no content API). So `search`'s `url` is the community homepage where the card is
  surfaced, and the rich `summary` carries the content. To get a post's full body, use `read`
  with a postId obtained from a detail URL you already have (e.g. copied from the browser).

### How `read` works

- The detail route is `/community/comgroup/postsDetails?postId=<id>&type=freePost`, discovered from
  the app bundle's `resourceType → URL` mapping (`free_post` → `postsDetails?postId=${resourceId}`).
  `read` navigates the logged-in tab there and scrapes the rendered `.detail-content`.
- No clean JSON content API exists in the bundle — the body is server-rendered into the page HTML,
  so navigation + scrape is the reliable path (not an API call).
- The CSRF-gated `POST /ideaService/v2/lib2/ideas` general-search API (which would return postIds
  for all content types) was investigated but its request body schema could not be recovered (the
  bridge's network capture returned empty on this page, and synthetic clicks don't trigger the
  Vue app's handlers). Only `GET /ideaService/v2/innovation/ideas?searchKey=` was cracked, and it
  returns `ideaManager`-type results only (not `free_post`), so it is not wired in.
- `parsePostId` accepts a bare 32-char hex id or a full detail URL; for a URL it extracts `postId`
  + normalizes the `type` query param (`freePost` → `free_post`).

### Parts most likely to need adjustment

These are the fragile bits, called out honestly:

1. **`CARD_SELECTOR`** (in `search.ts`/`search.js`) — if the site's result-card markup changes,
   `.recommended-page-list-item` won't match and the adapter throws `EmptyResultError`. Inspect a
   real results page with `opencli browser huawei-jiaxian state` / `opencli browser huawei-jiaxian find --css ...`
   and update the selector.
2. **The input/button selectors** in `triggerSearch` — if the search UI changes (input class, button
   class), the adapter reports "Could not trigger a search". Run
   `opencli browser huawei-jiaxian state` after typing a query to find the new trigger elements and update
   the `input.form-control` / `.search-btn` selectors.
3. **`read`'s detail-page selectors** (in `read.ts`/`read.js`) — `.detail-content` (body),
   `.author-card__info-row` (author), `.author-card__stat-label`/`.nav-name` (stats),
   `.meta-icon-date` (date). If the detail page markup changes, `read` throws `EmptyResultError`.
   Inspect a real detail page with `opencli browser huawei-jiaxian state` and update the selectors.
4. **`read` only supports `free_post`** — `technical_report` / `industry_report` use different
   routes (`/TI/report/details/<id>`, `/TI/industry/details/<id>`) with different markup. Adding
   them means a new entry in `DETAIL_ROUTE` + a body extractor for that page's container.

## Development

```bash
# Each command has a typed source-of-truth (.ts) hand-mirrored to the .js entry
# OpenCLI loads. Keep both in sync after edits (no build step):
#   search.ts <-> search.js   ·   read.ts <-> read.js

# Verify the commands are registered:
opencli list | grep huawei-jiaxian

# Run them:
opencli huawei-jiaxian search "大模型" --limit 3
opencli huawei-jiaxian read da25639435334344912733f65c592a1b
```
