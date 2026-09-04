# cloudscope

The **CloudScope 运维大脑 (ops brain) MCP server** — the ops/diagnosis tool
surface for Huawei Cloud services behind one intranet endpoint. One server,
**~248 callable tools**: alarms, topology, metrics, DWS/RDS/ModelArts
diagnosis, remediation diagnosis trees, CMDB, tickets, CDN ops, and more.

> **Server vs tools:** this folder packages **one MCP server**. Its ~248
> callable tools are NOT listed in this README or embedded in the manifest
> (the server adds tools continuously, so an embedded list rots). Discover
> them via the dated snapshot or the live wrapper — see [Discovering
> tools](#discovering-tools).

## Endpoint

- URL: `http://100.93.18.106:18080/cloudscope/mcp`
- Server: `CloudScope MCP Server` v3.4.0 (as of 2026-09-03), Streamable HTTP,
  protocol 2025-03-26 / 2024-11-05
- **Auth: none** — the `cloudscope` route on the proxy at `100.93.18.106:18080`
  is auth-free. (The same proxy also fronts a `tsc` route at `/mcp`, but that
  one is 404/auth-gated — not usable here.)
- Source of this setup recipe: the AgentRun Develop-Kit wiki (CloudDevOps,
  AgentRun/架构设计) — the relay agent's `cloudscope.json` config points at
  this same endpoint with `use_proxy: false`.

## Network requirement (the one piece of setup)

The endpoint is on the Huawei intranet and **must bypass the corporate HTTP
proxy** (`proxyuk.huawei.com:8080`), or the connection fails:

```
NO_PROXY=100.93.18.106
```

- The **wrapper script handles this automatically** (explicit no-proxy opener,
  in-process only — does not rely on `NO_PROXY` env, which Windows urllib
  reads unreliably).
- When loading the **MCP config** into an agent, set `NO_PROXY` in the shell
  that launches the agent so the agent's MCP client honors it.

You must also be on the Huawei intranet/VPN — the host is not reachable from
the open internet.

## Discovering tools

Two complementary ways:

1. **Dated snapshot (offline)** — [`tools/inventory-2026-09-03.json`](tools/inventory-2026-09-03.json):
   all 248 tools with descriptions, captured 2026-09-03. Grep it, diff it
   against a newer snapshot, or browse it without touching the network.

2. **Live (authoritative)** — the wrapper's discovery subcommands:

```bash
python3 mcps/cloudscope/cloudscope_mcp.py list                 # all tools: name — one-line description
python3 mcps/cloudscope/cloudscope_mcp.py list --group monitor # tools starting with a prefix
python3 mcps/cloudscope/cloudscope_mcp.py search dws           # grep names + descriptions
python3 mcps/cloudscope/cloudscope_mcp.py schema <tool-name>   # full input schema (required args starred)
```

Useful groups (prefixes): `monitor_*` (alarms/topology/metrics),
`tros_*` (TROS diagnosis + MRS SSH inspection), `opstools_tros_dws_*` (DWS
diagnosis), `rds_*`, `modelarts_*`/`model_arts_*`, `obs_*`,
`resources_*` (CMDB), `cloud_auto_remediation_*` (diagnosis trees),
`decision_x_copilot_*`, `ommgmt_*`/`gom_*`/`cor_*` (tickets/warroom),
`c_cdn_*` (CDN). The manifest's `tools_summary` maps each group to what it
does.

## Usage — three ways, pick one

### A. Any agent with Bash + Python 3 (no MCP needed)

```bash
# discover
python3 mcps/cloudscope/cloudscope_mcp.py search "alarm"

# call a tool (args are the tool's inputSchema properties as JSON)
python3 mcps/cloudscope/cloudscope_mcp.py call monitor_cma_get_active_alarms \
  --args '{"service_name":"DWS","start_time":"1756857600000","end_time":"1756943999000"}' --json

# bigger payloads via file
python3 mcps/cloudscope/cloudscope_mcp.py call <tool> --args-file payload.json
```

Exit codes: `0` ok, `2` usage error, `3` connection/protocol error, `4` the
tool itself returned an error result. Tool output is the text content of the
MCP result (usually JSON from the backend); `--json` pretty-prints it when it
parses as JSON.

### B. Claude Code (via `.mcp.json`)

```bash
cp mcps/cloudscope/claude-code.mcp.json .mcp.json
# ensure NO_PROXY includes 100.93.18.106 in the launching shell, then:
claude
```

All ~248 tools appear namespaced as `mcp__cloudscope__<tool_name>`.

### C. opencode / ngAgent / cac (via `--mcp-config`)

```bash
NO_PROXY=100.93.18.106 codeagent --mcp-config mcps/cloudscope/opencode.mcp.json
# or strict (only this server): --strict-mcp-config
```

## Files

| File | Purpose |
|---|---|
| `mcp-server.json` | Manifest — connection facts + `tools_summary` group map. Deliberately does not embed the 248-tool list (see `tools_note`). |
| `cloudscope_mcp.py` | Pure-stdlib (urllib + json) generic MCP client: `list` / `search` / `schema` / `call`. Runs anywhere with Python 3. |
| `claude-code.mcp.json` | Ready-to-load config for Claude Code (`.mcp.json` format). |
| `opencode.mcp.json` | Ready-to-load config for opencode/ngAgent/cac (`mcp` object format). |
| `tools/inventory-2026-09-03.json` | Dated snapshot of the live `tools/list` (name + description each). Reference, not source of truth. |
| `README.md` | This file. |

## Verification

```bash
python3 mcps/cloudscope/cloudscope_mcp.py search dws        # expect ~7 hits
python3 mcps/cloudscope/cloudscope_mcp.py schema monitor_cma_get_active_alarms
python3 mcps/cloudscope/cloudscope_mcp.py call monitor_cma_get_active_alarms \
  --args '{"service_name":"DWS","start_time":"1756857600000","end_time":"1756943999000"}' --json
```

Expect `{"count": 0, ...}` or alarm records. If you see `cannot reach …`, you
are either off the intranet/VPN or the endpoint is down (the wrapper already
bypasses the proxy). Note: some tools' *backends* are only reachable from
certain networks (e.g. `dws_service_autopilot_*` needs the DWS internal
network) — a tool may list fine but fail at call time with a backend connect
error; that is the backend, not this wrapper.
