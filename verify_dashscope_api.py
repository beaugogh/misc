#!/usr/bin/env python3
"""Verify that the Aliyun DashScope (OpenAI-compatible) chat API works.

The DashScope compatible-mode endpoint speaks the OpenAI Chat Completions
API, so we just point the `openai` SDK at it with a custom base_url.

Credentials are read from a .env file in the same directory (loaded with
python-dotenv), with CLI flags / real env vars as fallbacks.

Usage:
    python verify_dashscope_api.py

    # Override pieces on the command line if you like
    python verify_dashscope_api.py --model glm-5 --prompt "说喵"
"""

import argparse
import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("The `python-dotenv` package is not installed. Install it with:\n  pip install python-dotenv", file=sys.stderr)
    sys.exit(2)

try:
    from openai import OpenAI, OpenAIError
except ImportError:
    print("The `openai` package is not installed. Install it with:\n  pip install openai", file=sys.stderr)
    sys.exit(2)

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "glm-5"
DEFAULT_PROMPT = "说喵"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the DashScope chat API.")
    parser.add_argument("--api-key", help="API key (defaults to .env DASHSCOPE_API_KEY / env)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help=f"Prompt text (default: {DEFAULT_PROMPT!r})")
    args = parser.parse_args()

    # Load variables from .env into os.environ. Existing real env vars win
    # over .env values (load_dotenv does not overwrite by default), which is
    # the right behavior for CI / prod overrides.
    load_dotenv()

    api_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("ERROR: no API key. Put DASHSCOPE_API_KEY in .env, export it, or pass --api-key.", file=sys.stderr)
        return 2

    # base_url is the OpenAI-compatible root (without /chat/completions);
    # the SDK appends the path itself.
    client = OpenAI(api_key=api_key, base_url=BASE_URL, timeout=60.0)

    print(f"Calling {BASE_URL}/chat/completions")
    print(f"  model:  {args.model}")
    print(f"  prompt: {args.prompt!r}")
    print()

    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": args.prompt}],
        )
    except OpenAIError as exc:
        # Covers auth errors, bad model, rate limits, network/timeout, etc.
        print(f"API ERROR: {exc}", file=sys.stderr)
        return 1

    content = resp.choices[0].message.content
    print("Reply:")
    print(content)

    print("\nOK — API call works.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
