#!/usr/bin/env python3
"""Verify that the Aliyun DashScope (OpenAI-compatible) chat API works.

The DashScope compatible-mode endpoint speaks the OpenAI Chat Completions
API, so we just point the `openai` SDK at it with a custom base_url.

Credentials are read from a .env file in the same directory (loaded with
python-dotenv), with CLI flags / real env vars as fallbacks.

Usage:
    python verify_dashscope_api.py

    # Use the raw HTTP path that mirrors the console's curl example
    python verify_dashscope_api.py --mode http

    # Override pieces on the command line if you like
    python verify_dashscope_api.py --model glm-5 --prompt "说喵"
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

try:
    from dotenv import load_dotenv
except ImportError:
    print("The `python-dotenv` package is not installed. Install it with:\n  pip install python-dotenv", file=sys.stderr)
    sys.exit(2)

DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "glm-5"
DEFAULT_PROMPT = "说喵"


def chat_url(base_url: str) -> str:
    return f"{base_url.rstrip('/')}/chat/completions"


def call_with_openai_sdk(api_key: str, base_url: str, model: str, prompt: str) -> str:
    try:
        from openai import OpenAI, OpenAIError
    except ImportError:
        print("The `openai` package is not installed. Install it with:\n  pip install openai", file=sys.stderr)
        raise SystemExit(2)

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
    except OpenAIError as exc:
        # Covers auth errors, bad model, rate limits, network/timeout, etc.
        print(f"API ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    return resp.choices[0].message.content or ""


def call_with_http(api_key: str, base_url: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        chat_url(base_url),
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        print(f"API ERROR: HTTP {exc.code} - {err_body}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as exc:
        print(f"API ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    return data["choices"][0]["message"]["content"]


def main() -> int:
    # Load variables from .env into os.environ. Existing real env vars win
    # over .env values (load_dotenv does not overwrite by default), which is
    # the right behavior for CI / prod overrides.
    load_dotenv()

    parser = argparse.ArgumentParser(description="Verify the DashScope chat API.")
    parser.add_argument("--api-key", help="API key (defaults to .env DASHSCOPE_API_KEY / env)")
    parser.add_argument(
        "--mode",
        choices=("sdk", "http"),
        default=os.environ.get("DASHSCOPE_CALL_MODE", "sdk"),
        help="Call mode: OpenAI SDK or raw HTTP like the curl example (default: sdk)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("DASHSCOPE_BASE_URL", DEFAULT_BASE_URL),
        help=f"OpenAI-compatible API root (default: env DASHSCOPE_BASE_URL or {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("DASHSCOPE_MODEL", DEFAULT_MODEL),
        help=f"Model name (default: env DASHSCOPE_MODEL or {DEFAULT_MODEL})",
    )
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help=f"Prompt text (default: {DEFAULT_PROMPT!r})")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("ERROR: no API key. Put DASHSCOPE_API_KEY in .env, export it, or pass --api-key.", file=sys.stderr)
        return 2

    print(f"Calling {chat_url(args.base_url)}")
    print(f"  mode:   {args.mode}")
    print(f"  model:  {args.model}")
    print(f"  prompt: {args.prompt!r}")
    print()

    if args.mode == "http":
        content = call_with_http(api_key, args.base_url, args.model, args.prompt)
    else:
        content = call_with_openai_sdk(api_key, args.base_url, args.model, args.prompt)

    print("Reply:")
    print(content)

    print("\nOK — API call works.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
