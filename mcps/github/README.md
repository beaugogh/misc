# github

Interact with **GitHub** repositories, issues, PRs, actions, and more via the
official **GitHub MCP server** (`api.githubcopilot.com/mcp/`). Covers the full
GitHub platform: repos, commits, file contents, issues, pull requests, reviews,
workflow runs, notifications, code search.

## ⚠️ First EXTERNAL-host MCP server in this repo

Unlike the other four `mcps/` entries (`huawei-w3-search`,
`huawei-codehub`, `huawei-wiki`, `huawei-clouddevops`) which hit **Huawei
intranet** hosts and must **bypass** the corporate proxy, GitHub is an
**external** host that must go **through** the proxy:

| | Intranet tools (w3-search, codehub, etc.) | This tool (GitHub) |
|---|---|---|
| Host | `*.huawei.com` | `api.githubcopilot.com` |
| Proxy | **bypass** (`ProxyHandler({})`) | **route through** (`ProxyHandler({"https": "proxyuk...})`) |
| TLS | direct or `--allow-insecure-host` | `ssl.CERT_NONE` (proxy does TLS interception) |

The wrapper handles this automatically — it routes through
`proxyuk.huawei.com:8080` and disables cert verification (the urllib equivalent
of curl's `--ssl-no-revoke`, documented in the repo's
[`git-corporate-proxy-lfs`](../../skills/git-corporate-proxy-lfs/) skill).

## Prerequisites

1. **GitHub PAT** (Personal Access Token) — set `GITHUB_TOKEN` in the
   environment. Generate at github.com/settings/tokens (`repo` scope minimum).
   The server returns `401` without it.
2. **Corporate proxy** — the wrapper routes through `proxyuk.huawei.com:8080`
   automatically. Override with `GITHUB_MCP_PROXY` env var if needed.

## Tools

The server exposes 21 toolsets (repos, issues, pull_requests, actions,
code_security, notifications, etc.) with 100+ tools. The manifest documents the
key tools; `--list-tools` shows the full live list. Key tools:

| Tool | Read/Write | Purpose |
|---|---|---|
| `search_repositories` | read | search repos by query |
| `get_repository` | read | repo details |
| `list_commits` | read | commit history |
| `get_file_contents` | read | file/directory contents |
| `create_or_update_file` | **write** | create/update a file |
| `create_issue` / `get_issue` / `list_issues` | read/write | issue lifecycle |
| `add_issue_comment` | **write** | comment on issue |
| `create_pull_request` / `get_pull_request` / `list_pull_requests` | read/write | PR lifecycle |
| `get_pull_request_files` | read | PR changed files |
| `merge_pull_request` | **write** | merge a PR |
| `create_pull_request_review` / `get_pull_request_reviews` | read/write | PR reviews |
| `list_workflow_runs` / `get_workflow_run` | read | GitHub Actions |
| `list_notifications` | read | user notifications |
| `search_code` | read | search code across GitHub |

## Usage

### A. Any agent with Bash + Python 3

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
python3 mcps/github/github_mcp.py list-commits --owner beaugogh --repo misc --json
python3 mcps/github/github_mcp.py list-pull-requests --owner beaugogh --repo misc --state all
python3 mcps/github/github_mcp.py --list-tools
```

### B/C. Claude Code / opencode

Edit the config to put your real PAT in the `Authorization` header, then:
`cp mcps/github/claude-code.mcp.json .mcp.json` (Claude Code) or
`codeagent --mcp-config mcps/github/opencode.mcp.json` (opencode).

Note: the agent's MCP client must also route through the proxy. Set
`HTTPS_PROXY=http://proxyuk.huawei.com:8080` in the shell that launches the
agent.

## Relationship to huawei-codehub

`huawei-codehub` covers Huawei CodeHub (codehub-g.huawei.com) — MRs, reviews,
issues on Huawei's internal Git platform. This tool covers GitHub — the same
operations on GitHub. For repos hosted on GitHub (like this `misc` repo), use
this tool; for repos on CodeHub, use `huawei-codehub`.

## Files

| File | Purpose |
|---|---|
| `mcp-server.json` | Manifest (source of truth for catalog). |
| `github_mcp.py` | Pure-stdlib MCP client (urllib + json + ssl). No `pip install`. |
| `claude-code.mcp.json` | Claude Code config (`.mcp.json`). |
| `opencode.mcp.json` | opencode/ngAgent/cac config. |
| `README.md` | This file. |
