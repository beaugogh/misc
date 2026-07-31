#!/usr/bin/env python3
"""wiki_mcp — standalone client for the Huawei CloudDevOps Wiki remote MCP server.

Runs with Python 3 only (stdlib urllib + json), no `pip install` required.
Any agent (or human) can call this directly to read/write CloudDevOps Wiki:

    python3 wiki_mcp.py fetch-wiki-content --url <wiki-url>
    python3 wiki_mcp.py search-wiki-documents --url <wiki-url> --search-range knowledge --search-key "盘古"
    python3 wiki_mcp.py list-my-pending-wiki-countersigns --json

This wrapper speaks the MCP Streamable HTTP protocol (initialize →
notifications/initialized → tools/call) over stdlib urllib, so it works even
on agents with no MCP support at all. The server requires no authentication;
it only needs to reach the intranet host. The wrapper bypasses any corporate
HTTP proxy via an explicit no-proxy opener (it does NOT rely on the NO_PROXY
env var, which on Windows is unreliable for urllib).

The server replies as text/event-stream (SSE); this script parses the first
`data:` line. Tool results are JSON; this script prints them as text (human-ish)
by default, or raw JSON with --json. A non-zero exit code is returned on failure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

URL = "http://mcpgateway.his.huawei.com/mcp/69e5c49fc1218e60a80b1740/2038867975988133890"
TIMEOUT = 15
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
# Most tools (fetch/search/list content) need no auth. User-scoped tools
# (list_my_*) and write tools (create/overwrite/comment/countersign) require
# X-Auth-Token to identify the user. Set WIKI_X_AUTH_TOKEN in the environment.
_xauth = os.environ.get("WIKI_X_AUTH_TOKEN", "")
if _xauth:
    HEADERS["X-Auth-Token"] = _xauth
NO_PROXY_HOST = "mcpgateway.his.huawei.com"
PROTOCOL_VERSION = "2025-03-26"

TOOL_ALIASES = {
    "fetch-wiki-content": "fetch_wiki_content",
    "create-wiki-document": "create_wiki_document",
    "overwrite-wiki-content": "overwrite_wiki_content",
    "add-wiki-comment": "add_wiki_comment",
    "fetch-wiki-comment": "fetch_wiki_comment",
    "list-wiki-documents": "list_wiki_documents",
    "search-wiki-documents": "search_wiki_documents",
    "initiate-wiki-countersign": "initiate_wiki_countersign",
    "fetch-wiki-countersign-info": "fetch_wiki_countersign_info",
    "submit-wiki-countersign-conclusion": "submit_wiki_countersign_conclusion",
    "terminate-wiki-countersign": "terminate_wiki_countersign",
    "list-my-initiated-wiki-countersigns": "list_my_initiated_wiki_countersigns",
    "list-my-pending-wiki-countersigns": "list_my_pending_wiki_countersigns",
}


class WikiError(RuntimeError):
    """Raised on MCP errors or server-side tool errors."""


def _post(payload: dict, session_id: str | None = None,
          expect_response: bool = True) -> dict | None:
    headers = dict(HEADERS)
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=TIMEOUT) as resp:
        new_sid = resp.headers.get("Mcp-Session-Id")
        raw = resp.read().decode("utf-8", errors="replace")
    if not expect_response:
        return None
    data_line = None
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            data_line = line[len("data:"):].strip()
            break
    if data_line is None:
        raise RuntimeError(f"no data line in response:\n{raw[:500]}")
    result = json.loads(data_line)
    if new_sid:
        result["_session_id"] = new_sid
    return result


def _initialize() -> str:
    resp = _post({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "wiki_mcp.py", "version": "1.0"},
        },
    })
    if "error" in resp:
        raise RuntimeError(f"initialize failed: {resp['error']}")
    sid = resp.get("_session_id", "")
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"},
          session_id=sid, expect_response=False)
    return sid


def call_tool(name: str, arguments: dict) -> Any:  # type: ignore[name-defined]
    """Call an MCP tool and return the parsed result."""
    sid = _initialize()
    resp = _post({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }, session_id=sid)
    if "error" in resp:
        raise WikiError(f"tools/call failed: {resp['error']}")
    result = resp.get("result", {})
    is_error = result.get("isError", False)
    content = result.get("content", [])
    parts = [c.get("text", "") for c in content if c.get("type") == "text"]
    parts = [p for p in parts if p]
    if is_error:
        text = parts[0] if parts else ""
        try:
            err_obj = json.loads(text)
            msg = err_obj.get("message", err_obj.get("error", text))
        except (json.JSONDecodeError, TypeError):
            msg = text
        raise WikiError(f"tool '{name}' error: {msg}")
    if not parts:
        return result
    # Each part is a JSON string; return single unwrapped or a list.
    parsed = []
    all_json = True
    for p in parts:
        try:
            parsed.append(json.loads(p))
        except json.JSONDecodeError:
            all_json = False
            break
    if all_json:
        return parsed[0] if len(parsed) == 1 else parsed
    return "\n".join(parts)


def _render(value: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if value is None:
        return "(none)"
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        if not value:
            return "(empty list)"
        out = []
        for i, item in enumerate(value, 1):
            out.append(f"{pad}[{i}]")
            out.append(_render(item, indent + 1))
        return "\n".join(out)
    if isinstance(value, dict):
        if value.get("isError"):
            return f"ERROR: {value.get('error', value)}"
        out = []
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                out.append(f"{pad}{k}:")
                out.append(_render(v, indent + 1))
            else:
                out.append(f"{pad}{k}: {v}")
        return "\n".join(out)
    return str(value)


GLOBAL_FLAGS = {"--json", "--list-tools"}


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    if argv is None:
        argv = sys.argv[1:]
    as_json = False
    list_tools = False
    remaining: list[str] = []
    for tok in argv:
        if tok == "--json":
            as_json = True
        elif tok == "--list-tools":
            list_tools = True
        else:
            remaining.append(tok)
    p = argparse.ArgumentParser(
        description="Call the Huawei CloudDevOps Wiki MCP server (remote, no auth).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  %(prog)s fetch-wiki-content --url <wiki-url>\n"
               "  %(prog)s search-wiki-documents --url <wiki-url> --search-range knowledge --search-key '盘古'\n"
               "  %(prog)s list-my-pending-wiki-countersigns --json\n"
               "\nUse --list-tools to see all 13 tools. Pass --json for raw JSON output.",
    )
    p.add_argument("tool", nargs="?", help="tool to call (kebab-case, e.g. fetch-wiki-content)")
    p.add_argument("--list-tools", action="store_true", help="list the server's tools and exit")
    p.add_argument("--json", action="store_true", help="emit raw JSON result instead of text")
    p.add_argument("tool_args", nargs=argparse.REMAINDER, help="tool arguments as --key value pairs")
    ns = p.parse_args(remaining)
    ns.json = as_json or ns.json
    ns.list_tools = list_tools or ns.list_tools
    return ns


def _collect_tool_args(remainder: list[str]) -> dict[str, Any]:  # type: ignore[name-defined]
    out: dict[str, Any] = {}
    i = 0
    while i < len(remainder):
        tok = remainder[i]
        if tok.startswith("--"):
            key = tok[2:].replace("-", "_")
            if i + 1 < len(remainder) and not remainder[i + 1].startswith("--"):
                val = remainder[i + 1]
                i += 2
            else:
                val = "true"
                i += 1
            if val.lower() in ("true", "false"):
                out[key] = val.lower() == "true"
            else:
                try:
                    out[key] = int(val)
                except ValueError:
                    out[key] = val
        else:
            i += 1
    return out


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if not args.tool and not args.list_tools:
        print("error: specify a tool to call, or use --list-tools. See --help.", file=sys.stderr)
        return 2
    try:
        if args.list_tools:
            sid = _initialize()
            resp = _post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, session_id=sid)
            tools = resp.get("result", {}).get("tools", [])
            if args.json:
                print(json.dumps(tools, ensure_ascii=False, indent=2))
            else:
                print("\n".join(t.get("name", "?") for t in tools))
            return 0
        tool_name = TOOL_ALIASES.get(args.tool, args.tool.replace("-", "_"))
        tool_args = _collect_tool_args(args.tool_args)
        result = call_tool(tool_name, tool_args)
    except urllib.error.URLError as e:
        print(f"error: cannot reach {NO_PROXY_HOST} — {e}", file=sys.stderr)
        print("hint: ensure you are on the intranet/VPN; the wrapper bypasses "
              "the corporate proxy automatically, but the host must be reachable.",
              file=sys.stderr)
        return 2
    except WikiError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            print(_render(result))
    except Exception as e:
        print(f"error: failed to render result — {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
