# opencli-plugin-huawei-terminology

Search the Huawei terminology database ([3ms.huawei.com/terminology](https://3ms.huawei.com/terminology)) — returns the English term, Chinese term, domain, confidence level, and definition for each match.

Requires a **logged-in Huawei session** via the OpenCLI Browser Bridge. The `searchWeb` endpoint is same-origin and authenticated by the browser's cookies, so the adapter issues the fetch from inside the page context (`page.evaluate`) rather than from Node.

## Prerequisites

One-time per machine:

```bash
npm install -g @jackwener/opencli     # Node >= 20
opencli doctor                          # Browser Bridge extension connected in Chrome
```

Then sign in to https://3ms.huawei.com/terminology in Chrome so the session cookies are present. `opencli doctor` must be green before this plugin will work.

## Install

```bash
# From this repo (local development — symlinked, edits reflect immediately)
opencli plugin install file://D:/workspace/misc/opencli-plugins/huawei-terminology

# From GitHub (after pushing)
opencli plugin install github:<user>/misc/opencli-plugins/huawei-terminology
```

> **Note on TypeScript:** the command is written in `search.ts` and transpiled to `search.js` with [esbuild](https://esbuild.github.io/). If `opencli plugin install` warns that no `.js` was compiled, install esbuild (`npm i -g esbuild`) and run, from this directory:
>
> ```bash
> esbuild search.ts --outfile=search.js --format=esm --platform=node
> ```

## Commands

| Command | Strategy | Description |
|---------|----------|-------------|
| `huawei-terminology search` | COOKIE | Search the terminology database |

## Usage

```bash
opencli huawei-terminology search "CloudDragon" --limit 5
opencli huawei-terminology search "5G"
opencli huawei-terminology search "云龙"                 # Chinese queries work too
opencli huawei-terminology search "5G" -f json           # JSON output for agents
```

### Arguments

| Arg | Type | Default | Description |
|---|---|---|---|
| `query` (positional, required) | string | — | Term or abbreviation to search |
| `--limit` | int | 10 | Max results (server caps at ~50) |
| `--language` | string | `en` | Source language: `en` \| `cn` |
| `--filter-language` | string | `` | Restrict to a result language, e.g. `cn`. Empty = all. |

### Columns

`rank`, `term_en`, `term_cn`, `domain`, `confidence`, `definition`, `url`

## How it works (recon notes)

- The site `3ms.huawei.com/terminology` is a Vue SPA; its search lives at `#/main/termSearch?searchValue=...`.
- Search fires `POST https://3ms.huawei.com/term-web/wiki/termSearch/searchWeb` with a JSON body:
  ```json
  { "page": 1, "numpage": 10, "language": "en", "query": "<q>",
    "filterLanguage": "", "filterDomain": "", "matchType": "match",
    "resourceType": "", "searchType": "RELATE",
    "userinfo": { "uid": "", "userName": "", "w3Account": "<from localStorage.userInfo>" } }
  ```
- The logged-in `w3Account` is read from `localStorage.userInfo` at runtime — it is **not** hardcoded.
- Response: `{ code: "0", list: [ { ftitleEn, ftitleCn, nodeNameZh, confidenceLevel, definitionContent, fid, ... } ] }`.
- Strategy is `COOKIE` (not `PUBLIC`): the endpoint has no public contract and requires the Huawei SSO session, but the request shape is stable and the data is the page's own.

## Development

```bash
# After editing search.ts, re-transpile:
esbuild search.ts --outfile=search.js --format=esm --platform=node

# Verify the command is registered:
opencli list | grep huawei-terminology

# Run it:
opencli huawei-terminology search "CloudDragon" --limit 3
```
