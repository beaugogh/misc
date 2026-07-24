# opencli-plugin-huawei-jiaxian

Search Huawei's **稼先社区** ([jx.huawei.com](https://jx.huawei.com/)) — the internal
expert-and-engineer knowledge community — and get your questions answered from the
community's collective expertise.

Given an arbitrary question, `opencli huawei-jiaxian search` returns the **top N most relevant
documents**, each with title, type, author, date, views, replies, a **rich summary** (author +
abstract + expert viewpoints), and a URL. The rich summaries carry enough substance for a
downstream agent or reader to answer the question.

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
| `huawei-jiaxian search` | COOKIE | Search the 稼先社区 knowledge base; returns top N documents |

## Usage

```bash
# Ask a question — returns the top 10 documents
opencli huawei-jiaxian search "大模型推理优化"

# Limit to 3 documents
opencli huawei-jiaxian search "盘古2.0昇腾性能" --limit 3

# JSON output for agents
opencli huawei-jiaxian search "5G架构演进" -f json
```

### Arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `query` (positional, required) | string | — | Your question or search term |
| `--limit` | int | 10 | Max number of documents to return (N) |
| `--language` | string | `cn` | Source language: `cn` \| `en` |

### Columns

`rank`, `title`, `type`, `author`, `date`, `views`, `replies`, `summary`, `url`

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
- **Detail-page URLs** are not reliably obtainable from a card (navigation is Vue click-handler
  based and does not update `location.href`), so `url` is the community homepage where the card is
  surfaced. The rich `summary` carries the actual content.

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

## Development

```bash
# search.ts is the typed source-of-truth; search.js is the hand-mirrored entry
# OpenCLI loads. Keep both in sync after edits (no build step).

# Verify the command is registered:
opencli list | grep huawei-jiaxian

# Run it:
opencli huawei-jiaxian search "大模型" --limit 3
```
