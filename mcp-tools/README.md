# MCP tools

A collection of **remote MCP servers** packaged to work out of the box for any
agent/harness — with **no install step** and **no bundled credentials**.

This is the repo's third artifact category, alongside [skills](../skills/) and
[OpenCLI plugins](../opencli-plugins/). Each MCP tool is self-contained in its
own folder under `mcp-tools/`.

## Why this category exists

A remote MCP server is neither an instruction document (skill) nor a CLI
command (OpenCLI plugin). To make one "work out of the box for any agent," each
tool packages two things:

1. **Ready-to-load config** for each MCP-capable harness — Claude Code
   (`claude-code.mcp.json`) and opencode/ngAgent/cac (`opencode.mcp.json`). An
   agent loads the matching file and the MCP tool becomes available; no editing
   of the user's global config.
2. **A pure-stdlib wrapper script** that speaks the MCP protocol itself
   (urllib + json, no `pip install`). Any agent with Bash + Python 3 can call
   it directly — **no MCP support required at all**. This is the direct analog
   of an OpenCLI plugin committing its compiled `.js` so it "installs without a
   local esbuild."

## Layout

```
mcp-tools/
  <tool-name>/
    mcp-tool.json           # manifest — transport, url, headers, tool args (catalog source of truth)
    <wrapper>.py            # pure-stdlib MCP client; runs anywhere with Python 3
    claude-code.mcp.json    # ready-to-load config for Claude Code (.mcp.json format)
    opencode.mcp.json       # ready-to-load config for opencode/ngAgent/cac (mcp object format)
    README.md               # setup, network notes, usage per harness
```

## Activation

Pick one — see each tool's `README.md` for specifics:

- **Any agent with Bash + Python 3** (no MCP support needed):
  ```bash
  python3 mcp-tools/<tool>/<wrapper>.py "<query>"
  ```
- **Claude Code**: `cp mcp-tools/<tool>/claude-code.mcp.json .mcp.json` (auto-discovered).
- **opencode / ngAgent / cac**: `codeagent --mcp-config mcp-tools/<tool>/opencode.mcp.json`.

## Network note (Huawei intranet)

These tools hit intranet endpoints that **must bypass the corporate HTTP proxy**
(`proxyuk.huawei.com:8080`). The wrapper scripts handle this automatically (in
process). When loading the MCP config into an agent, set `NO_PROXY` to include
the tool's host in the shell that launches the agent. See each tool's
`mcp-tool.json` `network.no_proxy` field.

## Adding a new MCP tool

1. `mkdir mcp-tools/<kebab-case-name>`
2. Add `mcp-tool.json` (manifest: `name`, `transport`, `url`, `headers`,
   `auth`, `network.no_proxy`, and a `tools[]` array with `name`/`args`/
   `output_fields`). This is the catalog source of truth.
3. Write a pure-stdlib `<name>.py` wrapper (urllib + json only) that speaks the
   MCP Streamable HTTP protocol: `initialize` → `notifications/initialized` →
   `tools/call`. It must work with no `pip install` and set its own `NO_PROXY`
   / use a no-proxy opener for intranet hosts.
4. Add `claude-code.mcp.json` and `opencode.mcp.json` ready-to-load configs.
5. Add a `README.md` (model on `w3-search/README.md`).
6. Run `./scripts/generate-catalog.sh` to update `CATALOG.md`.

## Available tools

See [`../CATALOG.md`](../CATALOG.md) → "MCP tools" section (generated).
