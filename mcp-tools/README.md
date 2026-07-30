# MCP tools

A collection of **MCP servers** packaged to work for any agent/harness. Each
tool is self-contained in its own folder under `mcp-tools/`.

This is the repo's third artifact category, alongside [skills](../skills/) and
[OpenCLI plugins](../opencli-plugins/).

## Two transport types

Not all MCP tools here are equal — the transport decides what "self-contained"
means:

- **Remote** (`transport: remote`) — the server is an HTTP endpoint on the
  intranet. **Truly install-free**: the wrapper is pure stdlib (urllib + json),
  nothing to `pip install`, no bundled credentials. Example: `w3-search`.
- **Local** (`transport: local`) — the server is a process launched by `uvx`
  (a Python package fetched from the intranet artifactory). **NOT install-free**:
  requires `uv`/`uvx` on PATH, intranet reachability for the first-run fetch,
  and a user credential (`PRIVATE_TOKEN`). Example: `codehub`.

Both share the same packaging shape (manifest + wrapper + harness configs +
README) so an agent discovers and activates them uniformly; the local variant
just carries extra runtime prerequisites that its README states up front.

## Why this category exists

An MCP server is neither an instruction document (skill) nor a CLI command
(OpenCLI plugin). To make one "work for any agent," each tool packages:

1. **Ready-to-load config** for each MCP-capable harness — Claude Code
   (`claude-code.mcp.json`) and opencode/ngAgent/cac (`opencode.mcp.json`). An
   agent loads the matching file and the MCP tool becomes available; no editing
   of the user's global config.
2. **A pure-stdlib wrapper script** that speaks the MCP protocol itself
   (no `pip install` for the wrapper). Any agent with Bash + Python 3 can call
   it directly — **no MCP support required at all**. For remote tools this is
   the direct analog of an OpenCLI plugin committing its compiled `.js` so it
   "installs without a local esbuild"; for local tools the wrapper shells out
   to `uvx` and speaks stdio JSON-RPC, so it still needs no MCP support in the
   harness but does depend on `uvx` + credentials on the host.

## Layout

```
mcp-tools/
  <tool-name>/
    mcp-tool.json           # manifest — transport, url/command, env, tool args (catalog source of truth)
    <wrapper>.py            # pure-stdlib MCP client; runs anywhere with Python 3
    claude-code.mcp.json    # ready-to-load config for Claude Code (.mcp.json format)
    opencode.mcp.json       # ready-to-load config for opencode/ngAgent/cac (mcp object format)
    README.md               # setup, network notes, usage per harness
```

## Activation

Pick one — see each tool's `README.md` for specifics:

- **Any agent with Bash + Python 3** (no MCP support needed):
  ```bash
  python3 mcp-tools/<tool>/<wrapper>.py <args>
  ```
- **Claude Code**: `cp mcp-tools/<tool>/claude-code.mcp.json .mcp.json` (auto-discovered).
- **opencode / ngAgent / cac**: `codeagent --mcp-config mcp-tools/<tool>/opencode.mcp.json`.

## Network note (Huawei intranet)

These tools hit intranet endpoints that **must bypass the corporate HTTP proxy**
(`proxyuk.huawei.com:8080`). The wrapper scripts handle this automatically (in
process, for their own connections). When loading the MCP config into an agent,
set `NO_PROXY` to include the tool's hosts in the shell that launches the agent.
See each tool's `mcp-tool.json` `network.no_proxy` field.

> ⚠️ **Local tools on Windows**: `uvx` reads the proxy from the Windows registry
> and may ignore `NO_PROXY`. If `uvx` fails to fetch the server, pre-download the
> tarball with `curl` (which honors `NO_PROXY`) and point `--from` at the local
> file — see `codehub/README.md` → Troubleshooting.

## Adding a new MCP tool

1. `mkdir mcp-tools/<kebab-case-name>`
2. Add `mcp-tool.json` (manifest: `name`, `transport` (`remote` or `local`),
   and for remote `url`/`headers` or for local `command`/`environment`;
   `auth`, `network.no_proxy`, and a `tools[]` array with `name`/`args`/
   `output_fields`). This is the catalog source of truth. For local tools also
   add a `runtime` block stating the `requires`/`install`/`note` prerequisites.
3. Write a pure-stdlib `<name>.py` wrapper (stdlib only) that speaks the MCP
   protocol — Streamable HTTP for remote, stdio JSON-RPC for local. It must
   work with no `pip install` (for the wrapper itself) and set its own
   `NO_PROXY` / use a no-proxy opener for intranet hosts where applicable.
4. Add `claude-code.mcp.json` and `opencode.mcp.json` ready-to-load configs.
5. Add a `README.md` (model on `w3-search/README.md` for remote,
   `codehub/README.md` for local — the local variant must state its runtime
   prerequisites up front).
6. Run `./scripts/generate-catalog.sh` to update `CATALOG.md`.

## Available tools

See [`../CATALOG.md`](../CATALOG.md) → "MCP tools" section (generated).
