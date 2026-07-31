# huawei-wiki-mcp

Read and write Huawei **CloudDevOps Wiki** documents via the remote **`wiki-mcp`**
MCP server (`mcpgateway.his.huawei.com`). Exposes wiki content fetch/create/
overwrite, comments, document search/listing, and the full countersign (会签)
workflow — 13 tools total.

Like `w3-search`, this is a **remote** MCP endpoint: truly install-free,
pure-stdlib wrapper. **Most tools need no authentication** — content fetch,
search, list, and comment tools work without a token. However, **user-scoped
tools** (`list_my_initiated_wiki_countersigns`, `list_my_pending_wiki_countersigns`)
and **write tools** (create/overwrite/comment/countersign) require an
`X-Auth-Token` header to identify the user. The wrapper reads
`WIKI_X_AUTH_TOKEN` from the environment and includes it if set; without it,
user-scoped calls return a server message asking for the token.

## Network requirement

The endpoint is on the Huawei intranet and **must bypass the corporate HTTP
proxy** (`proxyuk.huawei.com:8080`):

```
NO_PROXY=mcpgateway.his.huawei.com
```

- The **wrapper script handles this automatically** (no-proxy opener, in-process).
- When loading the **MCP config** into an agent, set `NO_PROXY` in the shell
  that launches the agent.

You must be on the intranet/VPN.

## Tools (13)

| Tool | Read/Write | Purpose |
|---|---|---|
| `fetch_wiki_content` | read | fetch a wiki doc's metadata + body by URL |
| `search_wiki_documents` | read | keyword search within a knowledge base / category / subtree |
| `list_wiki_documents` | read | list docs in a category or subtree (no content) |
| `fetch_wiki_comment` | read | fetch all comments on a doc |
| `list_my_initiated_wiki_countersigns` | read | list countersigns I initiated (since a date) |
| `list_my_pending_wiki_countersigns` | read | list countersigns pending my action |
| `fetch_wiki_countersign_info` | read | fetch a doc's latest countersign info |
| `create_wiki_document` | **write** | create a new doc (sibling/child of a given URL) |
| `overwrite_wiki_content` | **write** | full-overwrite update of a doc's title + content |
| `add_wiki_comment` | **write** | add a comment (supports replies + notifications) |
| `initiate_wiki_countersign` | **write** | initiate a countersign on a doc |
| `submit_wiki_countersign_conclusion` | **write** | submit my countersign conclusion |
| `terminate_wiki_countersign` | **write** | terminate an in-progress countersign |

All wiki tools take a `url` argument — a CloudDevOps Wiki document URL whose
path or query params contain `WIKI` followed by consecutive digits (the wiki
serial number).

## Usage

### A. Any agent with Bash + Python 3

```bash
python3 mcp-tools/huawei-wiki-mcp/wiki_mcp.py fetch-wiki-content --url <wiki-url>
python3 mcp-tools/huawei-wiki-mcp/wiki_mcp.py search-wiki-documents --url <wiki-url> --search-range knowledge --search-key "盘古" --json
python3 mcp-tools/huawei-wiki-mcp/wiki_mcp.py list-my-pending-wiki-countersigns
python3 mcp-tools/huawei-wiki-mcp/wiki_mcp.py --list-tools
```

### B/C. Claude Code / opencode

`cp mcp-tools/huawei-wiki-mcp/claude-code.mcp.json .mcp.json` (Claude Code) or
`codeagent --mcp-config mcp-tools/huawei-wiki-mcp/opencode.mcp.json` (opencode).

## Files

| File | Purpose |
|---|---|
| `mcp-tool.json` | Manifest (source of truth for catalog). |
| `wiki_mcp.py` | Pure-stdlib MCP client (urllib + json). No `pip install`. |
| `claude-code.mcp.json` | Claude Code config (`.mcp.json`). |
| `opencode.mcp.json` | opencode/ngAgent/cac config. |
| `README.md` | This file. |
