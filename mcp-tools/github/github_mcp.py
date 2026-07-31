#!/usr/bin/env python3
"""github_mcp — standalone client for the official GitHub MCP server.

Runs with Python 3 only (stdlib urllib + json + ssl), no `pip install`.
Any agent (or human) can call this directly to interact with GitHub:

    python3 github_mcp.py list-commits --owner beaugogh --repo misc --json
    python3 github_mcp.py list-pull-requests --owner beaugogh --repo misc --state all
    python3 github_mcp.py get-file-contents --owner beaugogh --repo misc --path README.md

This wrapper speaks the MCP Streamable HTTP protocol (initialize →
notifications/initialized → tools/call) over stdlib urllib.

**This is the first EXTERNAL-host MCP tool in this repo.** Unlike the Huawei
intranet tools (w3-search, codehub, wiki-mcp, clouddevops) which BYPASS the
corporate proxy, GitHub must go THROUGH it. The wrapper sets ProxyHandler to
route via proxyuk.huawei.com:8080. The proxy does TLS interception, so cert
verification is disabled (ssl.CERT_NONE) — the urllib equivalent of curl's
--ssl-no-revoke.

Requires GITHUB_TOKEN in the environment (GitHub Personal Access Token).
The server returns 401 without it.
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

URL = "https://api.githubcopilot.com/mcp/"
TIMEOUT = 30
PROXY = os.environ.get("GITHUB_MCP_PROXY", "http://proxyuk.huawei.com:8080")


PROTOCOL_VERSION = "2025-03-26"
NO_PROXY_HOST = "api.githubcopilot.com"


class GitHubError(RuntimeError):
    """Raised on MCP errors or server-side tool errors."""


def _get_pat() -> str:
    """Read the GitHub PAT from the environment."""
    pat = os.environ.get("GITHUB_TOKEN", "")
    if not pat:
        raise GitHubError(
            "GITHUB_TOKEN is not set. Generate a GitHub Personal Access Token "
            "at github.com/settings/tokens (repo scope minimum) and run:\n"
            "  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx"
        )
    return pat


def _build_opener() -> urllib.request.OpenerDirector:
    """Build a urllib opener that routes through the corporate proxy.

    Unlike the Huawei intranet tools (which use ProxyHandler({}) to bypass
    the proxy), GitHub is an external host that MUST go through the proxy.
    """
    proxy_handler = urllib.request.ProxyHandler({
        "http": PROXY,
        "https": PROXY,
    })
    # TLS interception workaround: corporate proxy re-signs certs.
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    https_handler = urllib.request.HTTPSHandler(context=ssl_ctx)
    return urllib.request.build_opener(proxy_handler, https_handler)


def _post(payload: dict, session_id: str | None = None,
          expect_response: bool = True) -> dict | None:
    pat = _get_pat()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {pat}",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    opener = _build_opener()
    with opener.open(req, timeout=TIMEOUT) as resp:
        new_sid = resp.headers.get("Mcp-Session-Id")
        raw = resp.read().decode("utf-8", errors="replace")
    if not expect_response:
        return None
    # The server may respond with plain JSON or SSE (data: lines).
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
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
            "clientInfo": {"name": "github-mcp.py", "version": "1.0"},
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
        raise GitHubError(f"tools/call failed: {resp['error']}")
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
        raise GitHubError(f"tool '{name}' error: {msg}")
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
        description="Call the GitHub MCP server (remote, via corporate proxy). "
                    "Requires GITHUB_TOKEN in the environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  %(prog)s list-commits --owner beaugogh --repo misc --json\n"
               "  %(prog)s list-pull-requests --owner beaugogh --repo misc --state all\n"
               "  %(prog)s get-file-contents --owner beaugogh --repo misc --path README.md\n"
               "\nUse --list-tools to see all tools. Pass --json for raw JSON.",
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
    # Token check before hitting the network.
    try:
        _get_pat()
    except GitHubError as e:
        print(f"error: {e}", file=sys.stderr)
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
        tool_name = args.tool.replace("-", "_")
        tool_args = _collect_tool_args(args.tool_args)
        result = call_tool(tool_name, tool_args)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        print(f"error: HTTP {e.code} from {NO_PROXY_HOST} — {e.reason}", file=sys.stderr)
        if body:
            print(f"  body: {body}", file=sys.stderr)
        if e.code == 401:
            print("hint: check that GITHUB_TOKEN is a valid GitHub PAT with sufficient scope.",
                  file=sys.stderr)
        return 2
    except urllib.error.URLError as e:
        print(f"error: cannot reach {NO_PROXY_HOST} — {e}", file=sys.stderr)
        print("hint: this is an external host — it must go through the corporate proxy "
              "(proxyuk.huawei.com:8080). The wrapper handles this automatically.", file=sys.stderr)
        return 2
    except GitHubError as e:
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
