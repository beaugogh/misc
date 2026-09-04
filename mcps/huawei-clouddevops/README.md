# huawei-clouddevops

Interact with the full Huawei **CloudDevOps (云捷)** platform via the remote
**`clouddevops-mcpserver`** MCP server (`tool.clouddevops.huawei.com`). **65
tools** spanning:

- **Issues / bugs** — full lifecycle (query, save, submit, accept, close, fix,
  online, test, reject, drawback, tags, comments, export)
- **Requirements** — list, detail, accept, comments, FE→mks mapping,
  relationships, release plans
- **Workitems** — list (my todo / my created), detail, batch create, update,
  comments, export
- **Wiki** — search knowledge, get by SN, create, update, query kanban
- **Design articles** — create, edit, query template, query by FE number
- **Vulnerabilities** — full lifecycle (query, detail, confirm, distribute,
  close, argue, uninvolved, validate, changed, published)
- **Labels / COE / notes / MR-by-e2e / download records**

Like `w3-search`, this is a **remote** MCP endpoint: install-free, pure-stdlib
wrapper. **But not credential-free** — requires an `X-AUTH-TOKEN` for all tool
calls (the handshake + `tools/list` work without it, but every `tools/call`
returns `401 Auth info is invalid!`).

## Prerequisites

1. **`X-AUTH-TOKEN`** — set `CLOUDDEVOPS_X_AUTH_TOKEN` in the environment. The
   wrapper reads it and includes it as the `X-AUTH-TOKEN` header. Obtain a token
   from the CloudDevOps platform.
2. **Intranet/VPN** — `tool.clouddevops.huawei.com` must be reachable.

## Network / proxy

```
NO_PROXY=tool.clouddevops.huawei.com
```

- The **wrapper handles this automatically** (no-proxy opener).
- When loading the **MCP config** into an agent, set `NO_PROXY` in the shell
  that launches the agent.

## Usage

### A. Any agent with Bash + Python 3

```bash
export CLOUDDEVOPS_X_AUTH_TOKEN=<your-token>
python3 mcps/huawei-clouddevops/clouddevops.py search-domains --keyword "数字化"
python3 mcps/huawei-clouddevops/clouddevops.py query-issues-detail --issue-number BUG2025032012345
python3 mcps/huawei-clouddevops/clouddevops.py search-knowledge --search-key "盘古" --json
python3 mcps/huawei-clouddevops/clouddevops.py query-workitems-by-code --code 1 --page 1 --size 20
python3 mcps/huawei-clouddevops/clouddevops.py --list-tools
```

### B/C. Claude Code / opencode

Edit the config to put your real `X-AUTH-TOKEN` in the headers, then:
`cp mcps/huawei-clouddevops/claude-code.mcp.json .mcp.json` (Claude Code) or
`codeagent --mcp-config mcps/huawei-clouddevops/opencode.mcp.json` (opencode).

## Relationship to wiki-mcp

This server's Wiki tools (`searchKnowledge`, `getDescription`, `createWiki`,
`updateWiki`) overlap with [`wiki-mcp`](../wiki-mcp/)'s 13 Wiki tools. The
difference:

- **wiki-mcp** is Wiki-only, needs no auth for read tools, and uses the
  `mcpgateway.his.huawei.com` endpoint (different gateway).
- **clouddevops** covers the *entire* CloudDevOps platform (65 tools) but
  requires `X-AUTH-TOKEN` for every call.

For auto-evolve's Wiki data source, `wiki-mcp` is the lighter choice. This
server is for skills that need issues, requirements, workitems, or
vulnerabilities — not just Wiki.

## Files

| File | Purpose |
|---|---|
| `mcp-server.json` | Manifest (source of truth for catalog). |
| `clouddevops.py` | Pure-stdlib MCP client (urllib + json). No `pip install`. |
| `claude-code.mcp.json` | Claude Code config (`.mcp.json`). |
| `opencode.mcp.json` | opencode/ngAgent/cac config. |
| `README.md` | This file. |
