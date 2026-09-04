#!/usr/bin/env python3
"""cloudscope_mcp — generic client for the CloudScope ops MCP server.

One server, many tools (~248): alarms, topology, metrics, DWS/RDS/ModelArts
diagnosis, remediation trees, CMDB, tickets, and more. Runs with Python 3 only
(stdlib urllib + json), no `pip install` required. Any agent (or human) can
drive the full tool surface directly:

    python3 cloudscope_mcp.py list                        # all tools: name + one-line description
    python3 cloudscope_mcp.py list --group monitor        # tools whose name starts with a prefix
    python3 cloudscope_mcp.py search dws                  # grep name+description for a keyword
    python3 cloudscope_mcp.py schema opstools_tros_dws_execute_diagnose
    python3 cloudscope_mcp.py call monitor_cma_get_current_alarms --args '{"csns":["870379428"]}'
    python3 cloudscope_mcp.py call <tool> --args-file payload.json

This wrapper speaks the MCP Streamable HTTP protocol (initialize →
notifications/initialized → tools/list | tools/call) over stdlib urllib, so it
works even on agents with no MCP support at all. The server requires no
authentication; it only needs to reach the intranet host. The wrapper bypasses
any corporate HTTP proxy via an explicit no-proxy opener (it does NOT rely on
the NO_PROXY env var, which on Windows is unreliable for urllib).

Exit codes: 0 success; 2 usage error; 3 connection/protocol error; 4 the tool
itself returned an error (isError result).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

# On Windows the default console encoding is often GBK (cp936), which can't
# encode some Unicode chars the server returns (Chinese descriptions, etc.).
# Force UTF-8 so printing never crashes mid-result. Harmless elsewhere.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

# --- config (mirrors mcp-server.json) -----------------------------------------
URL = "http://100.93.18.106:18080/cloudscope/mcp"
# HTTP timeout for the wrapper's own requests, in seconds. The manifest
# (mcp-server.json) and the harness configs use 30000ms = 30s for the
# MCP-client timeout; the wrapper adds headroom (45s) for slow VPN links and
# slow backend tools. Keep these aligned in intent: if you change one, change
# the other.
TIMEOUT = 45
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",  # server replies SSE
    "User-Agent": "cloudscope_mcp.py/1.0",
}
# The intranet endpoint must bypass the corporate proxy.
NO_PROXY_HOST = "100.93.18.106"

PROTOCOL_VERSION = "2025-03-26"

# Group prefixes commonly useful for diagnosis/ops work (see README for the
# full table). `list --group X` matches tools whose name starts with X.
KNOWN_GROUPS = [
    "monitor", "tros", "opstools", "rds", "dws", "modelarts", "model_arts",
    "obs", "resources", "cloud_auto_remediation", "decision_x_copilot",
    "ommgmt", "gom", "cor", "c_cdn", "cloudservice", "ecs", "change", "cmw",
    "dlc", "cob", "knowledge_base", "cloud", "query",
]


class McpError(RuntimeError):
    """Protocol/connection-level failure (initialize, transport, SSE parse)."""


class ToolError(RuntimeError):
    """The tool executed but returned an error result (isError=true)."""


def _post(payload: dict, session_id: str | None = None,
          expect_response: bool = True) -> dict | None:
    """POST a JSON-RPC message and parse the SSE `data:` line back to JSON.

    The server replies as `text/event-stream` with one
    `event: message\ndata: {...}` block per response. We pull the first
    non-empty data line and json-decode it. Some responses (notifications)
    carry no data line — return None in that case rather than failing.

    Uses an explicit no-proxy opener (ProxyHandler({})): on Windows, urllib
    reads the proxy from the registry (system Internet settings), not just
    NO_PROXY env vars, so the corporate proxy (proxyuk.huawei.com:8080) would
    otherwise intercept and fail the intranet request.
    """
    headers = dict(HEADERS)
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:  # noqa: S310 — intranet http
            new_sid = resp.headers.get("Mcp-Session-Id")
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise McpError(f"HTTP {e.code} from {URL}: {e.read()[:300]!r}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise McpError(
            f"cannot reach {URL} ({e}). Are you on the intranet/VPN, and is "
            f"the endpoint up? (the wrapper bypasses the proxy itself)") from e
    if not expect_response:
        return None
    data_line = None
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            data_line = line[len("data:"):].strip()
            break
    if data_line is None:
        raise McpError(f"no data line in response:\n{raw[:500]}")
    result = json.loads(data_line)
    if new_sid:
        result["_session_id"] = new_sid
    return result


def _initialize() -> str:
    """MCP handshake; returns the session id for subsequent calls."""
    resp = _post({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "cloudscope_mcp.py", "version": "1.0"},
        },
    })
    if resp and "error" in resp:
        raise McpError(f"initialize failed: {resp['error']}")
    sid = (resp or {}).get("_session_id", "")
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"},
          session_id=sid, expect_response=False)
    return sid


def _unwrap_call(resp: dict) -> str:
    """Extract text content from a tools/call result; raise on isError."""
    result = resp.get("result") or {}
    if "error" in resp:
        raise McpError(f"tools/call failed: {resp['error']}")
    if result.get("isError"):
        parts = result.get("content") or []
        msg = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict))
        raise ToolError(msg or "tool returned isError without details")
    parts = result.get("content") or []
    texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
    return "\n".join(t for t in texts if t)


def list_tools(prefix: str | None = None) -> list[dict]:
    """Fetch tools/list; optionally filter by name prefix (e.g. 'monitor_')."""
    sid = _initialize()
    resp = _post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                 session_id=sid)
    if resp and "error" in resp:
        raise McpError(f"tools/list failed: {resp['error']}")
    tools = (resp or {}).get("result", {}).get("tools", [])
    if prefix:
        tools = [t for t in tools if t["name"].startswith(prefix)]
    return tools


def print_tool_brief(t: dict) -> None:
    """One line per tool: name — first sentence of the description."""
    desc = (t.get("description") or "").strip().replace("\n", " ")
    # Truncate to the first sentence-ish boundary for a scannable list.
    for sep in ("。", ". ", "\n"):
        idx = desc.find(sep)
        if 0 < idx <= 120:
            desc = desc[: idx + (1 if sep == "。" else 0)]
            break
    print(f"{t['name']} — {desc}")


def print_tool_detail(t: dict) -> None:
    """Full detail: description + input schema rendered as an args table."""
    print(f"## {t['name']}")
    desc = (t.get("description") or "").strip()
    if desc:
        print(f"\n{desc}")
    schema = t.get("inputSchema") or {}
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    if props:
        print("\nArguments:")
        for name, p in props.items():
            star = "*" if name in required else ""
            typ = p.get("type", "?")
            help_ = (p.get("description") or "").strip().replace("\n", " ")
            print(f"  {name}{star} ({typ}) — {help_}" if help_ else
                  f"  {name}{star} ({typ})")
        if required:
            print(f"  (* = required: {', '.join(sorted(required))})")


def cmd_list(args: argparse.Namespace) -> int:
    tools = list_tools(args.group)
    if args.json:
        slim = [{"name": t["name"], "description": t.get("description") or "",
                 "inputSchema": t.get("inputSchema") or {}} for t in tools]
        print(json.dumps(slim, ensure_ascii=False, indent=1))
    else:
        for t in tools:
            print_tool_brief(t)
    print(f"\n({len(tools)} tools)", file=sys.stderr)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    kw = args.keyword.lower()
    tools = list_tools()
    hits = [t for t in tools
            if kw in t["name"].lower()
            or kw in (t.get("description") or "").lower()]
    if args.json:
        slim = [{"name": t["name"], "description": t.get("description") or ""}
                for t in hits]
        print(json.dumps(slim, ensure_ascii=False, indent=1))
    else:
        for t in hits:
            print_tool_brief(t)
    print(f"\n({len(hits)} of {len(tools)} tools match '{args.keyword}')",
          file=sys.stderr)
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    tools = list_tools()
    matches = [t for t in tools if t["name"] == args.tool]
    if not matches:
        near = [t["name"] for t in tools if args.tool.lower() in t["name"].lower()]
        raise McpError(f"tool not found: {args.tool}"
                       + (f" (similar: {', '.join(near[:5])})" if near else ""))
    t = matches[0]
    if args.json:
        print(json.dumps(t, ensure_ascii=False, indent=1))
    else:
        print_tool_detail(t)
    return 0


def cmd_call(args: argparse.Namespace) -> int:
    call_args: dict = {}
    if args.args:
        call_args = json.loads(args.args)
    elif args.args_file:
        call_args = json.load(open(args.args_file, encoding="utf-8"))
    sid = _initialize()
    resp = _post({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": args.tool, "arguments": call_args},
    }, session_id=sid)
    out = _unwrap_call(resp or {})
    if args.json:
        # Re-encode whatever text came back; if it parses as JSON, pretty-print.
        try:
            print(json.dumps(json.loads(out), ensure_ascii=False, indent=1))
        except (json.JSONDecodeError, TypeError):
            print(out)
    else:
        print(out)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="cloudscope_mcp.py",
        description="Generic client for the CloudScope ops MCP server "
                    f"({URL}). List/search/schema/call any of its ~248 tools.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="list tools (name + one-line description)")
    p.add_argument("--group", help="filter by name prefix, e.g. monitor_")
    p.add_argument("--json", action="store_true", help="emit JSON")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("search", help="grep tool names + descriptions")
    p.add_argument("keyword")
    p.add_argument("--json", action="store_true", help="emit JSON")
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("schema", help="show one tool's full input schema")
    p.add_argument("tool")
    p.add_argument("--json", action="store_true", help="emit raw JSON")
    p.set_defaults(fn=cmd_schema)

    p = sub.add_parser("call", help="invoke a tool")
    p.add_argument("tool")
    p.add_argument("--args", help="arguments as a JSON object string")
    p.add_argument("--args-file", help="read arguments from a JSON file")
    p.add_argument("--json", action="store_true",
                   help="pretty-print the result if it parses as JSON")
    p.set_defaults(fn=cmd_call)

    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except (McpError, ToolError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 4 if isinstance(e, ToolError) else 3
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"usage error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
