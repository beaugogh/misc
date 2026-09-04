#!/usr/bin/env python3
"""codehub — standalone client for the Huawei CodeHub local MCP server.

Runs with Python 3 only (stdlib subprocess + json), no `pip install` required
for the wrapper itself. The wrapper launches `uvx`, which fetches and runs the
`mcp-server-codehub` Python package (a LOCAL stdio MCP server) from the Huawei
intranet artifactory. Any agent (or human) can call this directly:

    python3 codehub.py get-project-info --git-url ssh://git@codehub-dg-g.huawei.com:2222/g/p.git
    python3 codehub.py list-merge-requests --project-id 12345 --state all --json
    python3 codehub.py get-merge-request-reviews --project-id 12345 --mr-iid 7

This wrapper speaks the MCP stdio JSON-RPC protocol (initialize →
notifications/initialized → tools/list → tools/call) over the child process's
stdin/stdout, so it works even on agents with no MCP support at all — the same
self-contained-wrapper pattern as w3_search.py, but for a LOCAL server instead
of a remote one.

Two prerequisites (inherent to a local stdio server — NOT install-free):
  1. `uvx` (uv) on PATH, able to reach the intranet artifactory + PyPI mirror.
  2. A CodeHub token (CODEHUB_TOKEN env var) in the environment. The server
     exits at startup if neither is present.

Unlike w3_search.py, this wrapper CANNOT bypass the corporate proxy for uvx's
own fetches — uv reads the proxy from the Windows registry and has no
ProxyHandler escape hatch. If uvx fails to resolve/fetch the server, pre-download
the tarball with curl (which honors NO_PROXY) and pass --from <local-file> via
the CODEHUB_UVX_ARGS env var, or set NO_PROXY for the relevant intranet hosts
in the shell that runs this script. See README.md.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

# On Windows the default console encoding is often GBK (cp936), which can't
# encode some Unicode chars the server returns (Chinese review comments, etc.).
# Force UTF-8 so printing never crashes mid-result. Harmless on other platforms.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

# --- config (mirrors mcp-server.json) -----------------------------------------
# The uvx command that launches the local MCP server. The exact same args the
# harness configs use, so the wrapper and the MCP-client path launch the same
# server. Override the whole arg list with CODEHUB_UVX_ARGS (JSON array) if you
# need to point --from at a pre-downloaded local tarball to dodge proxy issues.
#
# Three flags here fix problems the upstream config doesn't anticipate (all
# diagnosed via the repo's git-corporate-proxy-lfs skill):
#   --allow-insecure-host cmc.centralrepo.rnd.huawei.com
#       The corporate proxy does TLS interception and re-signs the artifactory
#       cert; uv rejects it as "client error (Connect)" unless TLS verification
#       is relaxed for this host. (Same class of problem the skill documents as
#       http.schannelCheckRevoke=false for git.) NO_PROXY does NOT fix this.
#   --with python-dotenv
#       The server imports dotenv but omits it from pyproject.toml dependencies.
#   --with "mcp<2"
#       The server imports FastMCP from mcp.server; mcp 2.0 removed it, so pin 1.x.
DEFAULT_UVX_ARGS = [
    "uvx",
    "--index-url", "https://mirrors.tools.huawei.com/pypi/simple",
    "--allow-insecure-host", "mirrors.tools.huawei.com",
    "--allow-insecure-host", "cmc-nkg-artifactory.cmc.tools.huawei.com",
    "--allow-insecure-host", "cmc.centralrepo.rnd.huawei.com",
    "--with", "python-dotenv",
    "--with", "mcp<2",
    "--from", "https://cmc.centralrepo.rnd.huawei.com/artifactory/product_generic/mcp-server/python/gov-codehub/0.2.0/gov-codehub_0.2.0_1773145053.tar.gz",
    "mcp-server-codehub",
]
UVX_ARGS = json.loads(os.environ.get("CODEHUB_UVX_ARGS", "null")) or DEFAULT_UVX_ARGS

# How long to wait for the server to produce each JSON-RPC response line, and
# for the whole session. uvx's first run can be slow (fetching the tarball); the
# handshake + one tool call should still complete well under this.
TIMEOUT = 120

PROTOCOL_VERSION = "2025-03-26"
CLIENT_INFO = {"name": "huawei-codehub.py", "version": "1.0"}


class CodeHubError(RuntimeError):
    """Raised when the server returns an MCP-level error or a tool-level error."""


class ServerProcess:
    """A running CodeHub MCP server subprocess, spoken to over stdio JSON-RPC.

    MCP stdio transport: one JSON-RPC message per line, written to the child's
    stdin, responses read line-by-line from its stdout. The server may emit log
    lines on stderr (ignored) and may interleave notifications, so we read until
    we find a response matching our request id.
    """

    def __init__(self) -> None:
        env = dict(os.environ)
        # Translate user-facing env var names (CODEHUB_TOKEN, CODEHUB_HOST)
        # to the names the CodeHub MCP server expects (PRIVATE_TOKEN, WEB_HOST).
        codehub_token = env.get("CODEHUB_TOKEN", "")
        if codehub_token and not env.get("PRIVATE_TOKEN"):
            env["PRIVATE_TOKEN"] = codehub_token
        codehub_host = env.get("CODEHUB_HOST", "")
        if codehub_host and not env.get("WEB_HOST"):
            env["WEB_HOST"] = codehub_host
        # uvx must reach the intranet artifactory + PyPI mirror directly, not
        # through the corporate proxy. The TLS-interception problem is handled
        # by --allow-insecure-host in DEFAULT_UVX_ARGS (the proxy re-signs the
        # artifactory cert). Here we clear the proxy env vars so uv's HTTP
        # client (Rust reqwest) doesn't route through the proxy at all — on
        # Windows uv reads the registry proxy and NO_PROXY alone is unreliable.
        # Empty string (not unset) tells reqwest "no proxy".
        for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                  "http_proxy", "https_proxy", "all_proxy"):
            env[k] = ""
        intranet = "cmc.centralrepo.rnd.huawei.com,mirrors.tools.huawei.com,cmc-nkg-artifactory.cmc.tools.huawei.com,codehub-y.huawei.com,codehub-g.huawei.com,*.huawei.com,localhost,127.0.0.1"
        existing = env.get("NO_PROXY", "")
        env["NO_PROXY"] = intranet + ("," + existing if existing and existing != intranet else "")
        env["no_proxy"] = env["NO_PROXY"]
        try:
            self.proc = subprocess.Popen(
                UVX_ARGS,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,  # line-buffered
            )
        except FileNotFoundError:
            raise CodeHubError(
                "`uvx` not found on PATH. Install uv (https://github.com/astral-sh/uv) "
                "and ensure `uvx` is reachable, or set CODEHUB_UVX_ARGS to a command "
                "array that launches the server."
            )
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _send(self, payload: dict) -> None:
        assert self.proc.stdin is not None
        line = json.dumps(payload)
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()

    def _recv(self, expected_id: int | None = None) -> dict:
        """Read stdout lines until a JSON-RPC response matching expected_id.

        Skips notifications (messages without 'id') and log noise. Raises if the
        process exits before a response arrives.
        """
        assert self.proc.stdout is not None
        while True:
            line = self.proc.stdout.readline()
            if not line:
                # Process exited. Surface stderr for diagnosis.
                err = ""
                if self.proc.stderr is not None:
                    err = self.proc.stderr.read()
                raise CodeHubError(
                    f"server process exited before responding (code {self.proc.poll()})."
                    + (f"\nstderr:\n{err[:2000]}" if err else "")
                )
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                # Non-JSON line on stdout (log bleed-through); skip.
                continue
            if not isinstance(msg, dict):
                continue
            # Skip server->client notifications (no 'id').
            if expected_id is not None and msg.get("id") != expected_id:
                continue
            return msg

    def initialize(self) -> None:
        rid = self._next_id()
        self._send({
            "jsonrpc": "2.0", "id": rid, "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": CLIENT_INFO,
            },
        })
        resp = self._recv(rid)
        if "error" in resp:
            raise CodeHubError(f"initialize failed: {resp['error']}")
        # Complete the handshake (notification — no response expected).
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def list_tools(self) -> list[dict]:
        rid = self._next_id()
        self._send({"jsonrpc": "2.0", "id": rid, "method": "tools/list", "params": {}})
        resp = self._recv(rid)
        if "error" in resp:
            raise CodeHubError(f"tools/list failed: {resp['error']}")
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        rid = self._next_id()
        self._send({
            "jsonrpc": "2.0", "id": rid, "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })
        resp = self._recv(rid)
        if "error" in resp:
            raise CodeHubError(f"tools/call failed: {resp['error']}")
        result = resp.get("result", {})
        # MCP tool results come back as content[]. The server's
        # handle_tool_exceptions wrapper also returns {"isError": True, ...} on
        # server-side exceptions, delivered as a normal (non-error) result.
        content = result.get("content", [])
        # Tool-level error envelope (server wraps exceptions, not MCP errors).
        is_error = result.get("isError", False)
        parts = [c.get("text", "") for c in content if c.get("type") == "text"]
        parts = [p for p in parts if p]
        if is_error:
            # The error message is in the text content (JSON string).
            text = parts[0] if parts else ""
            try:
                err_obj = json.loads(text)
                msg = err_obj.get("error", text)
            except (json.JSONDecodeError, TypeError):
                msg = text
            raise CodeHubError(f"tool '{name}' error: {msg}")
        if not parts:
            return result
        # The server serializes return values as JSON text. For list-returning
        # tools (list_merge_requests, get_project_issues, get_merge_request_reviews,
        # ...) it emits ONE content item PER list element, each a JSON object —
        # not a single content item holding a JSON array. So: if every part
        # parses as JSON, return the list of parsed values; if there's exactly
        # one part, return it unwrapped (the common single-object case); else
        # fall back to the joined text.
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

    def close(self) -> None:
        try:
            if self.proc.stdin is not None:
                self.proc.stdin.close()
        except Exception:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


# --- tool name mapping (CLI kebab-case -> MCP tool name) --------------------
# Lets the CLI use ergonomic kebab-case subcommands while calling the exact MCP
# tool names the server expects.
TOOL_ALIASES = {
    "get-project-info": "get_project_info",
    "list-merge-requests": "list_merge_requests",
    "get-merge-request-info": "get_merge_request_info",
    "get-merge-request-changes": "get_merge_request_changes",
    "get-merge-request-mergeable-state": "get_merge_request_mergeable_state",
    "get-merge-request-reviews": "get_merge_request_reviews",
    "create-merge-request": "create_merge_request",
    "merge-merge-request": "merge_merge_request",
    "create-merge-request-review": "create_merge_request_review",
    "resolve-merge-request-reviews": "resolve_merge_request_reviews",
    "get-repo-file": "get_repo_file",
    "get-project-issues": "get_project_issues",
    "get-project-issue": "get_project_issue",
    "get-issue-discussions": "get_issue_discussions",
    "create-issue-discussion": "create_issue_discussion",
    "create-issue": "create_issue",
    "update-issue": "update_issue",
}


def _render(value: Any, indent: int = 0) -> str:
    """Render a tool result as compact human-readable text.

    CodeHub returns dicts/lists of varying shape (projects, MRs, reviews,
    issues). We render common fields when present and fall back to a JSON dump
    for anything unrecognized, so no result is ever silently lost.
    """
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
        # Tool-level error envelope already raised before render; but guard.
        if value.get("isError"):
            return f"ERROR: {value.get('error', value)}"
        # Detect a list nested under a common results key.
        for key in ("results", "merge_requests", "issues", "discussions", "reviews", "commits", "files", "content"):
            if key in value and isinstance(value[key], list):
                header = ", ".join(
                    f"{k}={v}" for k, v in value.items()
                    if k != key and not isinstance(v, (list, dict))
                )
                head = f"{pad}{header}\n" if header else ""
                return head + _render(value[key], indent)
        # Otherwise render each scalar field, and recurse into dict/list fields.
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
    # argparse.REMAINDER greedily swallows everything after the tool name,
    # including --json/--list-tools placed after the tool. Pre-extract those
    # global flags so they work in any position (before OR after the tool),
    # then let REMAINDER collect only genuine tool arguments.
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
        description="Call the Huawei CodeHub MCP server (local, via uvx). "
                    "Requires uvx on PATH and CODEHUB_TOKEN in the environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  %(prog)s list-merge-requests --project-id 12345 --state all\n"
               "  %(prog)s get-merge-request-reviews --project-id 12345 --mr-iid 7\n"
               "  %(prog)s get-project-info --git-url ssh://git@codehub-dg-g.huawei.com:2222/g/p.git\n"
               "\n"
               "Pass --json for the raw server JSON. Pass --list-tools to print the\n"
               "server's tool surface and exit (useful to verify the server starts).",
    )
    p.add_argument("tool", nargs="?", help="tool to call (kebab-case, e.g. list-merge-requests). "
                                           "Use --list-tools to see all.")
    p.add_argument("--list-tools", action="store_true", help="list the server's tools and exit")
    p.add_argument("--json", action="store_true", help="emit raw JSON result instead of text")
    # All tool arguments are accepted as free-form --key value pairs and passed
    # through to the MCP tool. This keeps the wrapper a thin transport: it does
    # not hardcode each tool's schema (the server validates), so it stays in
    # sync with whatever tools the installed server version exposes.
    p.add_argument("tool_args", nargs=argparse.REMAINDER,
                   help="tool arguments as --key value pairs (passed through to the MCP tool)")
    ns = p.parse_args(remaining)
    # Fold the pre-extracted globals back in (they win over any positional).
    ns.json = as_json or ns.json
    ns.list_tools = list_tools or ns.list_tools
    return ns


def _collect_tool_args(remainder: list[str]) -> dict[str, Any]:
    """Turn ['--project-id', '12345', '--state', 'all'] into a kwargs dict.

    Integers/bools are coerced so the server's typed pydantic fields accept them.
    Unknown flags are passed as strings; the server validates the full schema.
    """
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
                # Boolean flag (no value).
                val = "true"
                i += 1
            # Coerce common types: int, bool, else string.
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

    # Validate credentials early with a clear message, before spawning uvx
    # (which is slow on first run). The server exits at startup without a token;
    # failing fast here is friendlier than a subprocess crash after a long fetch.
    # The wrapper reads CODEHUB_TOKEN (user-facing) and translates it to
    # PRIVATE_TOKEN (server-facing) in ServerProcess.__init__.
    if not os.environ.get("CODEHUB_TOKEN") and not os.environ.get("PRIVATE_TOKEN") and not os.environ.get("X_AUTH_TOKEN"):
        print("error: CODEHUB_TOKEN is not set in the environment.", file=sys.stderr)
        print("hint: get a personal access token from CodeHub (codehub-g.huawei.com) and run:", file=sys.stderr)
        print("  export CODEHUB_TOKEN=<your-token>", file=sys.stderr)
        return 2
    if not os.environ.get("CODEHUB_HOST") and not os.environ.get("WEB_HOST"):
        os.environ["CODEHUB_HOST"] = "https://codehub-g.huawei.com/"

    try:
        server = ServerProcess()
    except CodeHubError as e:
        print(f"error: could not start the CodeHub MCP server — {e}", file=sys.stderr)
        return 2

    try:
        server.initialize()
        if args.list_tools:
            tools = server.list_tools()
            print(json.dumps(tools, ensure_ascii=False, indent=2) if args.json
                  else "\n".join(t.get("name", "?") for t in tools))
            return 0

        tool_name = TOOL_ALIASES.get(args.tool, args.tool.replace("-", "_"))
        tool_args = _collect_tool_args(args.tool_args)
        result = server.call_tool(tool_name, tool_args)
    except CodeHubError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    finally:
        server.close()

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
