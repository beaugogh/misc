# opencli-plugin-huawei-terminology

Search the Huawei terminology database ([3ms.huawei.com/terminology](https://3ms.huawei.com/terminology)) — returns the English term, Chinese term, domain, confidence level, and definition for each match.

Requires a **logged-in Huawei session** via the OpenCLI Browser Bridge. The `searchWeb` endpoint is same-origin and authenticated by the browser's cookies, so the adapter issues the fetch from inside the page context (`page.evaluate`) rather than from Node.

## Prerequisites — human, one-time (an agent cannot do these)

This plugin drives your **logged-in Chrome** via the OpenCLI Browser Bridge, so two things must be set up by a human before any agent (or `setup.sh`) can use it:

1. **Node.js ≥ 20** on the machine — https://nodejs.org
2. **OpenCLI + the Browser Bridge extension** — install opencli (`npm i -g @jackwener/opencli`), then add the **OpenCLI** extension to Chrome from the [Chrome Web Store](https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk) (or load it unpacked from the [GitHub Releases](https://github.com/jackwener/opencli/releases) zip). Keep Chrome running.
3. **Sign in to https://3ms.huawei.com/terminology** in Chrome with your Huawei account. The adapter reuses this session's cookies — if it's not signed in, every search fails with an auth error.

`opencli doctor` (run by `setup.sh`) verifies step 2; the smoke test at the end of `setup.sh` verifies step 3.

## Setup (automatable)

From this directory, an agent (or you) runs:

```bash
./setup.sh
```

It verifies Node/opencli, checks `opencli doctor` is green, installs the plugin, ensures the `@jackwener/opencli` peer-dep symlink (the step `opencli plugin install` sometimes skips on a fresh checkout), and runs a smoke-test search. If a human prerequisite is missing, it prints exactly what the human needs to do and exits. Safe to re-run.

<details>
<summary>Manual setup (what <code>setup.sh</code> does, if you'd rather run the steps by hand)</summary>

```bash
npm install -g @jackwener/opencli          # Node >= 20
opencli doctor                               # must be green — Browser Bridge connected
opencli plugin install D:/workspace/misc/opencli-plugins/huawei-terminology

# Ensure the peer-dep symlink (opencli plugin install usually makes this, but
# not always on a fresh checkout — without it the plugin fails to load):
mkdir -p node_modules/@jackwener
ln -s "$(npm root -g)/@jackwener/opencli" node_modules/@jackwener/opencli

opencli huawei-terminology search "5G" --limit 1   # smoke test
```

From GitHub (after pushing):
```bash
opencli plugin install github:<user>/misc/opencli-plugins/huawei-terminology
```

</details>

> **Note on TypeScript:** the command is written in `search.ts` and transpiled to `search.js` with [esbuild](https://esbuild.github.io/). The compiled `search.js` is committed so the plugin installs without a local esbuild. If you edit `search.ts`, recompile:
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
