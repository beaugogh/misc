# huawei-w3-search

Search Huawei's W3/3MS intranet (`w3.huawei.com`, `3ms.huawei.com` documents)
via the remote **`w3_search_tool`** MCP server. Returns documents — title,
source, url, text snippets, publish time — for any query (a person's name +
employee id, a product/topic, a technical term).

This is the first entry in the repo's `mcp-tools/` category: **remote MCP
servers packaged to work out of the box for any agent/harness**, with no
install step and no bundled credentials.

## Why it needs special packaging

The server is a *remote* MCP endpoint on the Huawei intranet — there is no
binary to install. Two things make it self-contained and runnable anywhere:

1. **Ready-to-load config** for each MCP-capable agent harness (Claude Code,
   opencode/ngAgent/cac). An agent loads the matching file and the
   `w3_web_search_tool` MCP tool becomes available — no editing of the user's
   global config.
2. **A pure-stdlib wrapper script** (`w3_search.py`) that speaks the MCP
   Streamable HTTP protocol itself. Any agent with Bash + Python 3 can call it
   directly — **no MCP support required at all**. This is the direct analog of
   an OpenCLI plugin committing its compiled `.js` so it "installs without a
   local esbuild."

No authentication is required — the server is an unauthenticated intranet
endpoint. The only credential-like concern is network reachability (below).

## Network requirement (the one piece of setup)

The endpoint is on the Huawei intranet and **must bypass the corporate HTTP
proxy** (`proxyuk.huawei.com:8080`), or the connection fails:

```
NO_PROXY=remote-mcp.rnd.huawei.com
```

- The **wrapper script sets this automatically** (in-process only).
- When loading the **MCP config** into an agent, set `NO_PROXY` in the shell
  that launches the agent, or in the agent's environment config, so the MCP
  client inside the agent honors it.

You must also be on the Huawei intranet/VPN — the host is not reachable from
the open internet.

## Tool

The server exposes one MCP tool:

### `w3_web_search_tool`

Search W3/3MS intranet content.

| Arg | Required | Default | Description |
|---|---|---|---|
| `query` | yes | — | search query (name, employee id, topic) |
| `page_index` | yes | `"1"` | page number, 1-based |
| `page_size` | yes | `"10"` | results per page |
| `engine` | yes | `"huawei"` | query engine |

Output fields per result: `title`, `source` (e.g. `hw3ms_doclib`, `w3_doc_w3`),
`url`, `texts` (snippets), `publish_time` (Unix timestamp).

## Usage — three ways, pick one

### A. Any agent with Bash + Python 3 (no MCP needed)

```bash
python3 mcp-tools/huawei-w3-search/w3_search.py "高博 b00563677"
python3 mcp-tools/huawei-w3-search/w3_search.py "盘古平台" --page 2 --size 5 --json
```

Prints human-readable results by default; `--json` emits the raw server JSON.
An agent with no MCP support at all can run this in a Bash tool call.

### B. Claude Code (via `.mcp.json`)

Copy or symlink the bundled config into your Claude Code project so it is
auto-discovered, or pass it explicitly:

```bash
# Auto-discovered: place at project root as .mcp.json
cp mcp-tools/huawei-w3-search/claude-code.mcp.json .mcp.json
# Ensure NO_PROXY is set in the shell that launches Claude Code, then:
claude
```

`w3_web_search_tool` appears as an available MCP tool.

### C. opencode / ngAgent / cac (via `--mcp-config`)

Load the bundled opencode config explicitly (no global edit):

```bash
NO_PROXY=remote-mcp.rnd.huawei.com codeagent --mcp-config mcp-tools/huawei-w3-search/opencode.mcp.json
# or strict (only this server): --strict-mcp-config
```

To install it into your global opencode config instead, merge the `mcp.w3_search_tool`
object from `opencode.mcp.json` into `~/.config/opencode/opencode.json`.

## Files

| File | Purpose |
|---|---|
| `mcp-tool.json` | Manifest — single source of truth (transport, url, headers, tool args). Catalog is generated from this. |
| `w3_search.py` | Pure-stdlib (urllib + json) MCP client. Runs anywhere with Python 3; no `pip install`. |
| `claude-code.mcp.json` | Ready-to-load config for Claude Code (`.mcp.json` format). |
| `opencode.mcp.json` | Ready-to-load config for opencode/ngAgent/cac (`mcp` object format). |
| `README.md` | This file. |

## Verification

```bash
python3 mcp-tools/huawei-w3-search/w3_search.py "b00563677" --size 3
```

Expect a few W3 document hits (titles + urls). If you see a connection error,
you're either off the intranet/VPN or `NO_PROXY` isn't set.
