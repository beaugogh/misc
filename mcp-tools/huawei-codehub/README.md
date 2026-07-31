# huawei-codehub

Interact with Huawei **CodeHub** Git repositories (`codehub-y.huawei.com` /
`codehub-g.huawei.com`) via the local **`Codehub-Mcp-Server`** MCP server.
Exposes project lookup, the full merge-request lifecycle (list / detail /
changes / mergeable state / reviews / create / merge), issues (list / detail /
discussions / create / update), and repo file reading.

This is the **second** entry in the repo's `mcp-tools/` category. Unlike the
first entry (`w3-search`, a *remote* MCP endpoint), this is a **local stdio
server** launched by `uvx`. That difference changes what "self-contained" means
here — read the prerequisites carefully.

## ⚠️ This tool is NOT install-free

`w3-search` is self-contained because its server is a remote URL and the
wrapper is pure stdlib — nothing to install. CodeHub's server is a Python
package that must be fetched and launched on your machine. A fresh `git clone`
of this repo **cannot** run it without:

1. **`uvx` (uv) installed** and on PATH — [github.com/astral-sh/uv](https://github.com/astral-sh/uv).
   The wrapper and the harness configs all invoke `uvx`, which on first run
   downloads the server tarball from the Huawei intranet artifactory.
2. **Intranet/VPN reachability** to:
   - `cmc.centralrepo.rnd.huawei.com` (the tarball artifactory)
   - `mirrors.tools.huawei.com` (the PyPI mirror, for dependency resolution)
3. **A CodeHub `PRIVATE_TOKEN`** (personal access token) in the environment.
   Get one from CodeHub → Settings → Access Tokens. The server exits at
   startup if neither `PRIVATE_TOKEN` nor `X_AUTH_TOKEN` is set.

If `uvx` fails with `Failed to resolve --with requirement / client error (Connect)`
— common on Windows, where uv reads the proxy from the registry and may ignore
`NO_PROXY` — see [Troubleshooting](#troubleshooting) below.

## Network / proxy (the corporate TLS-interception trap)

`uvx` must reach the intranet artifactory (`cmc.centralrepo.rnd.huawei.com`)
and PyPI mirror (`mirrors.tools.huawei.com`). The corporate proxy
(`proxyuk.huawei.com:8080`) does **TLS interception** — it re-signs the
artifactory's certificate. uv rejects the re-signed cert with
`client error (Connect)`, which looks like a network failure but is really a
TLS verification failure.

This is the **same class of problem** the repo's
[`git-corporate-proxy-lfs`](../skills/git-corporate-proxy-lfs/) skill documents
for git (`http.schannelCheckRevoke=false`): the proxy is a MITM, so certificate
revocation/verification must be relaxed for intranet hosts.

**The fix is already baked into this tool's uvx args:**
`--allow-insecure-host cmc.centralrepo.rnd.huawei.com` tells uv to skip TLS
verification for the artifactory host. The wrapper and both harness configs
include it. You do **not** need to set `NO_PROXY` for the wrapper — it clears
the proxy env vars itself so uv's HTTP client routes directly.

Two additional uvx flags fix packaging gaps in the server itself (also baked in):
- `--with python-dotenv` — the server imports `dotenv` but omits it from its
  `pyproject.toml` dependencies.
- `--with "mcp<2"` — the server imports `FastMCP` from `mcp.server`, which
  `mcp` 2.0 removed; pinning to 1.x matches the server's expected API.

When loading the **MCP config** into an agent harness, the harness launches uvx
directly (not through the wrapper), so the `--allow-insecure-host` flag in the
config's `args` array handles TLS. No `NO_PROXY` needed.

## Tools (17)

The server exposes 17 tools. Key ones for analysis/automation:

| Tool | Read/Write | Purpose |
|---|---|---|
| `get_project_info` | read | git_url → integer `project_id` (required by most other tools) |
| `list_merge_requests` | read | list MRs in a project (by state) |
| `get_merge_request_info` | read | MR detail (title/desc, no diff) |
| `get_merge_request_changes` | read | MR diff; `filters=commits` returns MR's commits |
| `get_merge_request_mergeable_state` | read | gate state (conflict/CI/approvers/E2E) |
| `get_merge_request_reviews` | read | all review comments on an MR |
| `create_merge_request` | **write** | create an MR |
| `merge_merge_request` | **write** | merge an MR |
| `create_merge_request_review` | **write** | post a review comment |
| `resolve_merge_request_reviews` | **write** | mark review resolved/unresolved |
| `get_repo_file` | read | file content at a ref |
| `get_project_issues` | read | issue list (filter by author/assignee/state) |
| `get_project_issue` | read | single issue detail |
| `get_issue_discussions` | read | issue discussion list |
| `create_issue_discussion` | **write** | comment on an issue |
| `create_issue` | **write** | create an issue |
| `update_issue` | **write** | update / close / reopen an issue |

> **No "list commits by author" tool.** The server is MR/Issue-centric, not
> commit-centric. It does not replace local `git log --author` for enumerating a
> user's raw commit history; it complements it with the collaboration layer
> (MRs, reviews, issues) that local git cannot see. The closest is
> `get_merge_request_changes` with `filters=commits`, which returns commits
> *within one MR*.

## Usage — three ways, pick one

### A. Any agent with Bash + Python 3 (no MCP needed)

```bash
export PRIVATE_TOKEN=<your-token>
python3 mcp-tools/huawei-codehub/codehub.py get-project-info \
  --git-url ssh://git@codehub-dg-g.huawei.com:2222/group/project.git

python3 mcp-tools/huawei-codehub/codehub.py list-merge-requests --project-id 12345 --state all
python3 mcp-tools/huawei-codehub/codehub.py get-merge-request-reviews --project-id 12345 --mr-iid 7 --json

# Verify the server starts and see its full tool surface:
python3 mcp-tools/huawei-codehub/codehub.py --list-tools
```

Tool names on the CLI use **kebab-case** (`list-merge-requests`); the wrapper
maps them to the server's snake_case names automatically. Pass tool arguments as
`--key value` pairs — the wrapper coerces ints/bools and passes them through;
the server validates the full schema.

Prints human-readable text by default; `--json` emits the raw server JSON.

### B. Claude Code (via `.mcp.json`)

```bash
# Edit mcp-tools/huawei-codehub/claude-code.mcp.json to put your real PRIVATE_TOKEN
# in the environment block, then:
cp mcp-tools/huawei-codehub/claude-code.mcp.json .mcp.json
# Ensure NO_PROXY is set in the shell that launches Claude Code, then:
claude
```

The 17 tools appear as available MCP tools (`get_project_info`,
`list_merge_requests`, …).

### C. opencode / ngAgent / cac (via `--mcp-config`)

```bash
# Edit mcp-tools/huawei-codehub/opencode.mcp.json to put your real PRIVATE_TOKEN in
# the environment block, then:
NO_PROXY=cmc.centralrepo.rnd.huawei.com,mirrors.tools.huawei.com codeagent \
  --mcp-config mcp-tools/huawei-codehub/opencode.mcp.json
```

To install it into your global opencode config instead, merge the
`mcp.Codehub-Mcp-Server` object from `opencode.mcp.json` into
`~/.config/opencode/opencode.json`.

## Files

| File | Purpose |
|---|---|
| `mcp-tool.json` | Manifest — single source of truth (transport, command, env, tool args). Catalog is generated from this. |
| `codehub.py` | Pure-stdlib (subprocess + json) MCP stdio client. Launches `uvx`, speaks JSON-RPC, returns text. No `pip install` for the wrapper itself (but `uvx` fetches the server). |
| `claude-code.mcp.json` | Ready-to-load config for Claude Code (local/stdio `.mcp.json` format). |
| `opencode.mcp.json` | Ready-to-load config for opencode/ngAgent/cac (`mcp` object, `type: local`). |
| `README.md` | This file. |

## Troubleshooting

**`uvx` fails: "Failed to resolve `--with` requirement / client error (Connect)"**

This is the TLS-interception problem described above. The fix
(`--allow-insecure-host cmc.centralrepo.rnd.huawei.com`) is already in the
wrapper's default args and the harness configs, so if you see this you're
likely running a stale `CODEHUB_UVX_ARGS` override or an old config. Check that
the host is in `--allow-insecure-host`. If uvx *still* can't connect after
that, pre-download the tarball with curl (which honors `NO_PROXY`) and point
`--from` at the local file as a fallback:

```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com \
  curl -L -o /tmp/gov-codehub.tar.gz \
  https://cmc.centralrepo.rnd.huawei.com/artifactory/product_generic/mcp-server/python/gov-codehub/0.2.0/gov-codehub_0.2.0_1773145053.tar.gz

CODEHUB_UVX_ARGS='["uvx","--index-url","https://mirrors.tools.huawei.com/pypi/simple","--allow-insecure-host","mirrors.tools.huawei.com","--allow-insecure-host","cmc.centralrepo.rnd.huawei.com","--with","python-dotenv","--with","mcp<2","--from","/tmp/gov-codehub.tar.gz","mcp-server-codehub"]' \
  python3 mcp-tools/huawei-codehub/codehub.py --list-tools
```

`CODEHUB_UVX_ARGS` is a JSON array that replaces the default uvx command line.

**`ModuleNotFoundError: No module named 'dotenv'`**

The server's `pyproject.toml` omits `python-dotenv` from its dependencies.
The default args include `--with python-dotenv` to fix this; if you've
overridden `CODEHUB_UVX_ARGS`, make sure you keep that flag.

**`ImportError: cannot import name 'FastMCP' from 'mcp.server'`**

The PyPI mirror serves `mcp` 2.0, which removed `FastMCP` from `mcp.server`.
The default args pin `--with "mcp<2"` to fix this; keep it in any override.

**`server process exited before responding`**

Usually a missing token. Ensure `PRIVATE_TOKEN` (or `X_AUTH_TOKEN`) is exported
in the environment before running the wrapper or launching the agent. The
wrapper checks this up front; the harness-config path does not, so the server
crashes at startup — check the agent's MCP server logs.

**Server starts but every tool returns an auth error**

The token is invalid or expired, or `WEB_HOST` points at a CodeHub instance
where the token isn't valid. Regenerate the token and confirm `WEB_HOST`
matches (default `https://codehub-y.huawei.com/`).
