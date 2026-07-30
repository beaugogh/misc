#!/usr/bin/env python3
"""w3_search — standalone client for the Huawei W3 search remote MCP server.

Runs with Python 3 only (stdlib urllib + json), no `pip install` required.
Any agent (or human) can call this directly to search the W3/3MS intranet:

    python3 w3_search.py "高博 b00563677"
    python3 w3_search.py "盘古平台" --page 2 --size 5
    python3 w3_search.py "LLM conversion" --engine huawei --json

This wrapper speaks the MCP Streamable HTTP protocol (initialize →
notifications/initialized → tools/call) over stdlib urllib, so it works even
on agents with no MCP support at all. The server requires no authentication;
it only needs to reach the intranet host. The wrapper bypasses any corporate
HTTP proxy via an explicit no-proxy opener (it does NOT rely on the NO_PROXY
env var, which on Windows is unreliable for urllib).

The server returns JSON; this script prints it as text (human-ish) by default,
or raw JSON with --json. A non-zero exit code is returned on any failure,
including server-side search errors (inner status != 200).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from http.client import HTTPResponse  # noqa: F401  (typing only)

# On Windows the default console encoding is often GBK (cp936), which can't
# encode some Unicode chars the server returns (en-space, etc.). Force UTF-8
# so printing never crashes mid-result. Harmless on other platforms.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

# --- config (mirrors mcp-tool.json) -----------------------------------------
URL = "http://remote-mcp.rnd.huawei.com/remote-mcp/mcp/w3_search_tool"
# HTTP timeout for the wrapper's own requests, in seconds. The manifest
# (mcp-tool.json) and the harness configs use 8000ms = 8s for the MCP-client
# timeout; the wrapper adds headroom (15s) for slow VPN links. Keep these
# aligned in intent: if you change one, change the other.
TIMEOUT = 15
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "OpenCode-MCP-Client/1.0",
    "Accept": "application/json, text/event-stream",  # server replies SSE
}
# The intranet endpoint must bypass the corporate proxy.
NO_PROXY_HOST = "remote-mcp.rnd.huawei.com"

PROTOCOL_VERSION = "2025-03-26"
TOOL_NAME = "w3_web_search_tool"


class SearchError(RuntimeError):
    """Raised when the server returns a search-level error (inner status != 200)."""


def _post(payload: dict, session_id: str | None = None,
          expect_response: bool = True) -> dict | None:
    """POST a JSON-RPC message and parse the SSE `data:` line back to JSON.

    The w3 server replies as `text/event-stream` with one
    `event: message\\ndata: {...}` block per response. We pull the first
    non-empty data line and json-decode it.

    If `expect_response` is False (notifications, which carry no `id`), the
    server returns an empty body and we return None instead of raising.
    """
    headers = dict(HEADERS)
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    # Force NO proxy: on Windows, urllib reads the proxy from the registry
    # (system Internet settings), not just NO_PROXY env vars, so the corporate
    # proxy (proxyuk.huawei.com:8080) would otherwise intercept and fail the
    # intranet request. An empty ProxyHandler disables all proxying.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=TIMEOUT) as resp:  # noqa: S310 — intranet http
        # Capture the session id from the first response (initialize).
        new_sid = resp.headers.get("Mcp-Session-Id")
        raw = resp.read().decode("utf-8", errors="replace")
    if not expect_response:
        return None
    # Parse SSE: find first 'data: ' line.
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
            "clientInfo": {"name": "w3_search.py", "version": "1.0"},
        },
    })
    if "error" in resp:
        raise RuntimeError(f"initialize failed: {resp['error']}")
    sid = resp.get("_session_id", "")
    # Complete the handshake (notification — no response expected).
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"},
          session_id=sid, expect_response=False)
    return sid


def search(query: str, page_index: str = "1", page_size: str = "10",
           engine: str = "huawei") -> dict:
    """Call the w3_web_search_tool and return the parsed result dict."""
    # No NO_PROXY env handling here: _post() uses an explicit no-proxy opener
    # (ProxyHandler({})) which bypasses the corporate proxy regardless of env
    # vars — more reliable on Windows than setting NO_PROXY, which urllib's
    # default opener may misinterpret. MCP clients loaded from the bundled
    # configs still need NO_PROXY set in their shell (see README).
    sid = _initialize()
    resp = _post({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {
            "name": TOOL_NAME,
            "arguments": {
                "query": query,
                "page_index": str(page_index),
                "page_size": str(page_size),
                "engine": engine,
            },
        },
    }, session_id=sid)
    if "error" in resp:
        raise RuntimeError(f"tools/call failed: {resp['error']}")
    # The tool result is content[0].text (a JSON string) per MCP spec.
    content = resp.get("result", {}).get("content", [])
    if not content:
        raise RuntimeError(f"empty content in result: {resp}")
    text = content[0].get("text", "")
    if not text:
        raise RuntimeError(f"empty text in content: {resp}")
    result = json.loads(text)
    # The server wraps results: {status, data: {status, message, data: {results}}}.
    # An inner status != 200 (e.g. -8 "搜索失败") means the search itself failed.
    outer = result.get("data", {}) or {}
    inner_status = outer.get("status")
    if inner_status is not None and inner_status != 200:
        raise SearchError(f"search failed (status {inner_status}): {outer.get('message', '?')}")
    return result


def _render(result: dict) -> str:
    """Render the search result as compact human-readable text."""
    data = (result or {}).get("data", {}) or {}
    data = data.get("data", data)  # one level of nesting in the server's shape
    if not isinstance(data, dict):
        return "(no results)"
    results = data.get("results", [])
    if not results:
        return "(no results)"
    lines = []
    for i, r in enumerate(results, 1):
        title = r.get("title", "(untitled)")
        url = r.get("url", "")
        source = r.get("source", "")
        texts = r.get("texts", [])
        pt = r.get("publish_time")
        lines.append(f"[{i}] {title}")
        meta = []
        if source:
            meta.append(source)
        if pt:
            import datetime
            try:
                meta.append(datetime.datetime.fromtimestamp(pt).strftime("%Y-%m-%d"))
            except Exception:
                meta.append(str(pt))
        if meta:
            lines.append("    " + " · ".join(meta))
        if url:
            lines.append(f"    {url}")
        if texts:
            snippet = " ".join(texts)[:300]
            lines.append(f"    {snippet}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Search Huawei W3/3MS intranet via the w3_search_tool remote MCP server.",
    )
    p.add_argument("query", help="search query (name, employee id, or topic)")
    p.add_argument("--page", default="1", help="page number, 1-based (default: 1)")
    p.add_argument("--size", default="10", help="results per page (default: 10)")
    p.add_argument("--engine", default="huawei", help="query engine (default: huawei)")
    p.add_argument("--json", action="store_true", help="emit raw JSON result instead of text")
    args = p.parse_args(argv)

    try:
        result = search(args.query, args.page, args.size, args.engine)
    except urllib.error.URLError as e:
        print(f"error: cannot reach {NO_PROXY_HOST} — {e}", file=sys.stderr)
        print("hint: ensure you are on the intranet/VPN; the wrapper bypasses "
              "the corporate proxy automatically, but the host must be reachable.",
              file=sys.stderr)
        return 2
    except SearchError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    try:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(_render(result))
    except Exception as e:
        print(f"error: failed to render result — {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
