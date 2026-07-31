#!/usr/bin/env python3
"""clouddevops — standalone client for the Huawei CloudDevOps (云捷) platform MCP server.

Runs with Python 3 only (stdlib urllib + json), no `pip install` required.
Any agent (or human) can call this directly to interact with CloudDevOps:

    python3 clouddevops.py search-domains --keyword "数字化"
    python3 clouddevops.py query-issues-detail --issue-number BUG2025032012345
    python3 clouddevops.py search-knowledge --search-key "盘古" --json
    python3 clouddevops.py query-workitems-by-code --code 1 --page 1 --size 20

This wrapper speaks the MCP Streamable HTTP protocol (initialize →
notifications/initialized → tools/call) over stdlib urllib. The server replies
with plain JSON (not SSE), which the wrapper parses directly.

Requires CLOUDDEVOPS_X_AUTH_TOKEN in the environment — the server returns 401
on every tools/call without it. The wrapper bypasses the corporate proxy via
an explicit no-proxy opener (does NOT rely on NO_PROXY env, unreliable on Windows).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

URL = "https://tool.clouddevops.huawei.com/clouddevops-mcpserver/mcp/streamable"
TIMEOUT = 30
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
# X-AUTH-TOKEN is required for all tool calls (handshake works without it,
# but every tools/call returns 401). Set CLOUDDEVOPS_X_AUTH_TOKEN in the env.
_xauth = os.environ.get("CLOUDDEVOPS_X_AUTH_TOKEN", "")
if _xauth:
    HEADERS["X-AUTH-TOKEN"] = _xauth
NO_PROXY_HOST = "tool.clouddevops.huawei.com"
PROTOCOL_VERSION = "2025-03-26"


class CloudDevOpsError(RuntimeError):
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
    # This server replies with plain JSON (not SSE data: lines).
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: try SSE parsing in case the server changes behavior.
        data_line = None
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                data_line = line[len("data:"):].strip()
                break
        if data_line is None:
            raise RuntimeError(f"no JSON or data line in response:\n{raw[:500]}")
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
            "clientInfo": {"name": "clouddevops.py", "version": "1.0"},
        },
    })
    if "error" in resp:
        raise RuntimeError(f"initialize failed: {resp['error']}")
    sid = resp.get("_session_id", "")
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"},
          session_id=sid, expect_response=False)
    return sid


def call_tool(name: str, arguments: dict) -> Any:
    sid = _initialize()
    resp = _post({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }, session_id=sid)
    if "error" in resp:
        raise CloudDevOpsError(f"tools/call failed: {resp['error']}")
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
        raise CloudDevOpsError(f"tool '{name}' error: {msg}")
    if not parts:
        return result
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
        # CloudDevOps often wraps: {code, message, data, path, timestamp}
        code = value.get("code")
        if code is not None and code != 200 and "data" in value:
            return f"server response: code={code} message={value.get('message','')}"
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
        description="Call the Huawei CloudDevOps (云捷) platform MCP server. "
                    "Requires CLOUDDEVOPS_X_AUTH_TOKEN in the environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  %(prog)s search-domains --keyword '数字化'\n"
               "  %(prog)s query-issues-detail --issue-number BUG2025032012345\n"
               "  %(prog)s search-knowledge --search-key '盘古' --json\n"
               "  %(prog)s query-workitems-by-code --code 1 --page 1 --size 20\n"
               "\nUse --list-tools to see all 65 tools. Pass --json for raw JSON.",
    )
    p.add_argument("tool", nargs="?", help="tool to call (kebab-case)")
    p.add_argument("--list-tools", action="store_true", help="list the server's tools and exit")
    p.add_argument("--json", action="store_true", help="emit raw JSON result instead of text")
    p.add_argument("tool_args", nargs=argparse.REMAINDER, help="tool arguments as --key value pairs")
    ns = p.parse_args(remaining)
    ns.json = as_json or ns.json
    ns.list_tools = list_tools or ns.list_tools
    return ns


def _collect_tool_args(remainder: list[str]) -> dict[str, Any]:
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
    # Token check before hitting the network (handshake works without it but
    # every tools/call returns 401 — fail fast with a clear message).
    if not _xauth and not args.list_tools:
        print("error: CLOUDDEVOPS_X_AUTH_TOKEN is not set in the environment.", file=sys.stderr)
        print("hint: obtain an X-AUTH-TOKEN from CloudDevOps and run:", file=sys.stderr)
        print("  export CLOUDDEVOPS_X_AUTH_TOKEN=<your-token>", file=sys.stderr)
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
        tool_name = args.tool.replace("-", "_")  # clouddevops tools already use snake_case
        tool_args = _collect_tool_args(args.tool_args)
        result = call_tool(tool_name, tool_args)
    except urllib.error.URLError as e:
        print(f"error: cannot reach {NO_PROXY_HOST} — {e}", file=sys.stderr)
        print("hint: ensure you are on the intranet/VPN.", file=sys.stderr)
        return 2
    except CloudDevOpsError as e:
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
