#!/usr/bin/env python3
"""Verify that an OpenAI-compatible chat model endpoint works.

Most hosted model providers — DashScope (Bailian), DeepSeek, Moonshot/Kimi,
Zhipu/GLM, SiliconFlow, OpenRouter, OpenAI itself, local Ollama — expose an
OpenAI-compatible /chat/completions API. This script points the `openai` SDK
at any of them, fires a prompt, and prints the reply: a fast smoke test that
the key, base URL, and model name are all correct.

Configuration is per-provider, read from a .env file sitting next to this
script (skills/verify-model-endpoints/.env). Each provider is a trio of env
vars named `<PROVIDER>_API_KEY`, `<PROVIDER>_BASE_URL`, `<PROVIDER>_MODEL`
(PROVIDER uppercased). DashScope/Bailian also supports plan-specific defaults
with --dashscope-plan / DASHSCOPE_PLAN. CLI flags override env values; real env
vars win over .env (python-dotenv doesn't overwrite by default), so CI/prod
overrides just work.

Usage (run from the repo root so ./.venv resolves):
    # Test the default provider (dashscope, since .env has DASHSCOPE_*)
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py

    # Pick a different provider configured in .env
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --provider deepseek

    # List known providers + which ones have an API key set
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --list-providers

    # List DashScope/Bailian plans, base URLs, and model aliases
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --list-dashscope-plans

    # Test a specific DashScope/Bailian plan
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py \\
        --provider dashscope --dashscope-plan token-plan --model glm-5.2

    # Override anything ad hoc (no .env needed)
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py \\
        --base-url http://localhost:11434/v1 --api-key dummy --model qwen2.5:7b

    # Test streaming + sampling params
    ./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --stream --max-tokens 64 --temperature 0.9
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("The `python-dotenv` package is not installed. Install it with:\n  ./.venv/bin/pip install python-dotenv", file=sys.stderr)
    sys.exit(2)

try:
    from openai import OpenAI, OpenAIError
except ImportError:
    print("The `openai` package is not installed. Install it with:\n  ./.venv/bin/pip install openai", file=sys.stderr)
    sys.exit(2)

# .env lives next to this script (the skill folder), so the script works
# regardless of the caller's CWD.
SKILL_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_PATH = SKILL_DIR / ".env"

# Built-in defaults for well-known OpenAI-compatible providers. base_url is
# the OpenAI root (without /chat/completions — the SDK appends the path). A
# provider needs only <PROVIDER>_API_KEY in .env to be testable; base_url and
# model fall back to these. Add a row here, or just set the env vars, to
# support a new endpoint.
PROVIDER_DEFAULTS = {
    "dashscope": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "glm-5.2",
        "note": "Aliyun DashScope/Bailian OpenAI-compatible mode",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "note": "DeepSeek official",
    },
    "moonshot": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
        "note": "Moonshot / Kimi",
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-plus",
        "note": "Zhipu / GLM (bigmodel.cn)",
    },
    "siliconflow": {
        "base_url": "https://api.siliconflow.cn/v1",
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "note": "SiliconFlow — model name is owner/model",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-4o-mini",
        "note": "OpenRouter — model name is owner/model",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "note": "OpenAI official",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5:7b",
        "note": "Local Ollama (run `ollama serve`); API key is ignored — pass any dummy",
    },
}

DEFAULT_PROVIDER = "dashscope"
DEFAULT_PROMPT = "说喵"

DASHSCOPE_MODEL_ALIASES_COMMON = {
    "kimi-k2.6": "kimi-k2-6",
    "kimi-k2.5": "kimi-k2-5",
    "glm-5.2": "glm-5-2",
    "glm-5.1": "glm-5-1",
    "glm-5": "glm-5-0",
}

DASHSCOPE_MODEL_ALIASES_CODING = {
    "kimi-k2.5": "kimi-k2-5",
    "glm-4.7": "glm-4-7",
    "glm-5": "glm-5-0",
}

# Base URLs from the Bailian/Cursor integration docs. The plan key is stable
# CLI/env surface; aliases accept the names users tend to type.
DASHSCOPE_PLANS = {
    "payg-beijing": {
        "aliases": ("payg", "postpaid", "beijing", "cn-beijing"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "glm-5.2",
        "api_key_var": "DASHSCOPE_API_KEY",
        "note": "Pay-as-you-go, China North 2 (Beijing)",
        "model_aliases": DASHSCOPE_MODEL_ALIASES_COMMON,
    },
    "payg-singapore": {
        "aliases": ("singapore", "ap-southeast-1"),
        "base_url": "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
        "model": "glm-5.2",
        "api_key_var": "DASHSCOPE_API_KEY",
        "note": "Pay-as-you-go, Singapore; requires workspace ID",
        "model_aliases": DASHSCOPE_MODEL_ALIASES_COMMON,
        "requires_workspace_id": True,
    },
    "payg-us": {
        "aliases": ("us", "virginia", "us-east"),
        "base_url": "https://dashscope-us.aliyuncs.com/compatible-mode/v1",
        "model": "glm-5.2",
        "api_key_var": "DASHSCOPE_API_KEY",
        "note": "Pay-as-you-go, US (Virginia)",
        "model_aliases": DASHSCOPE_MODEL_ALIASES_COMMON,
    },
    "token-plan": {
        "aliases": ("token", "token-plan-team", "team"),
        "base_url": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        "model": "glm-5-0",
        "api_key_var": "DASHSCOPE_TOKEN_PLAN_API_KEY",
        "note": "Token Plan team subscription",
        "model_aliases": DASHSCOPE_MODEL_ALIASES_COMMON,
    },
    "coding-plan": {
        "aliases": ("coding", "codingplan"),
        "base_url": "https://coding.dashscope.aliyuncs.com/v1",
        "model": "glm-5-0",
        "api_key_var": "DASHSCOPE_CODING_PLAN_API_KEY",
        "note": "Coding Plan subscription",
        "model_aliases": DASHSCOPE_MODEL_ALIASES_CODING,
    },
}

DEFAULT_DASHSCOPE_PLAN = "payg-beijing"


def env_name(provider: str, suffix: str) -> str:
    return f"{provider.upper()}_{suffix}"


def resolve_dashscope_plan(plan: str):
    normalized = plan.lower().replace("_", "-")
    for name, info in DASHSCOPE_PLANS.items():
        aliases = (name, *info.get("aliases", ()))
        if normalized in aliases:
            return name, info
    return None, None


def dashscope_env_name(plan_name: str, suffix: str) -> str:
    return f"DASHSCOPE_{plan_name.upper().replace('-', '_')}_{suffix}"


def normalize_dashscope_model(model: str, plan_info: dict):
    aliases = plan_info.get("model_aliases", {})
    normalized = aliases.get(model, model)
    return normalized, model if normalized != model else None


def list_dashscope_plans(env_path: Path) -> int:
    print("DashScope/Bailian plans:")
    for name, info in DASHSCOPE_PLANS.items():
        key_var = info["api_key_var"]
        fallback_key_var = info.get("fallback_api_key_var")
        key_set = bool(os.environ.get(key_var))
        fallback_set = bool(fallback_key_var and os.environ.get(fallback_key_var))
        key_marker = "set" if key_set else ("fallback" if fallback_set else "—")
        aliases = ", ".join(info.get("aliases", ()))
        print(f"  {name:<14} key:{key_marker:<8} {info['note']}")
        print(f"                 base_url: {info['base_url']}")
        print(f"                 default model: {info['model']}")
        print(f"                 api key env: {key_var}" + (f" (fallback: {fallback_key_var})" if fallback_key_var else ""))
        if aliases:
            print(f"                 aliases: {aliases}")
        if info.get("requires_workspace_id"):
            print("                 needs: DASHSCOPE_WORKSPACE_ID or --workspace-id")
    print()
    print("DashScope model aliases:")
    for src, dst in DASHSCOPE_MODEL_ALIASES_COMMON.items():
        print(f"  {src} -> {dst}")
    print("Coding Plan aliases:")
    for src, dst in DASHSCOPE_MODEL_ALIASES_CODING.items():
        print(f"  {src} -> {dst}")
    print()
    print(f".env loaded from: {env_path}" if env_path.is_file() else f".env not found at {env_path}")
    return 0


def list_providers(env_path: Path) -> int:
    print(f"Known providers (defaults from script; env overrides .env):\n")
    found_any = False
    for name, info in PROVIDER_DEFAULTS.items():
        key_var = env_name(name, "API_KEY")
        key_set = bool(os.environ.get(key_var))
        marker = "set" if key_set else "—"
        print(f"  {name:<12} key:{marker:<3} {info['note']}")
        print(f"               {key_var} | {env_name(name,'BASE_URL')} | {env_name(name,'MODEL')}")
        print(f"               default base_url: {info['base_url']}")
        print(f"               default model:    {info['model']}")
        if key_set:
            found_any = True
    print()
    if env_path.is_file():
        print(f".env loaded from: {env_path}")
    else:
        print(f".env not found at {env_path} (only real env vars / CLI flags will apply)")
    if not found_any:
        print("No <PROVIDER>_API_KEY env vars set — set at least one in .env to test.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify an OpenAI-compatible chat endpoint.")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER,
                        help=f"Provider key prefix in .env (default: {DEFAULT_PROVIDER}). "
                             f"Known: {', '.join(PROVIDER_DEFAULTS)}.")
    parser.add_argument("--env", default=str(DEFAULT_ENV_PATH),
                        help=f"Path to .env (default: {DEFAULT_ENV_PATH})")
    parser.add_argument("--api-key", help=f"API key (defaults to .env {env_name('<provider>','API_KEY')} / env)")
    parser.add_argument("--base-url", help="API base URL, OpenAI root without /chat/completions "
                                           "(defaults to .env <PROVIDER>_BASE_URL / env / built-in default)")
    parser.add_argument("--model", help="Model name (defaults to .env <PROVIDER>_MODEL / env / built-in default)")
    parser.add_argument("--dashscope-plan", help=f"DashScope/Bailian plan or region (default: {DEFAULT_DASHSCOPE_PLAN}). "
                                                 "Examples: payg-beijing, payg-singapore, payg-us, token-plan, coding-plan.")
    parser.add_argument("--workspace-id", help="Workspace ID for DashScope Singapore pay-as-you-go URL.")
    parser.add_argument("--use-model-alias", action="store_true",
                        help="For DashScope/Bailian, apply documented Cursor/Bailian model aliases such as glm-5.2 -> glm-5-2.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help=f"Prompt text (default: {DEFAULT_PROMPT!r})")
    parser.add_argument("--max-tokens", type=int, help="Max tokens in the reply (optional cap)")
    parser.add_argument("--temperature", type=float, help="Sampling temperature 0..2 (optional)")
    parser.add_argument("--stream", action="store_true", help="Stream the reply token-by-token")
    parser.add_argument("--list-providers", action="store_true", help="List known providers and exit")
    parser.add_argument("--list-dashscope-plans", action="store_true", help="List DashScope/Bailian plan defaults and exit")
    args = parser.parse_args()

    env_path = Path(args.env)
    # Load .env into os.environ. Existing real env vars win over .env values
    # (load_dotenv does not overwrite by default), which is the right behavior
    # for CI / prod overrides.
    if env_path.is_file():
        load_dotenv(env_path)

    if args.list_providers:
        return list_providers(env_path)
    if args.list_dashscope_plans:
        return list_dashscope_plans(env_path)

    provider = args.provider.lower()
    defaults = PROVIDER_DEFAULTS.get(provider)

    dashscope_plan_name = None
    dashscope_plan_info = None
    explicit_dashscope_plan = False
    if provider == "dashscope":
        explicit_dashscope_plan = bool(args.dashscope_plan or os.environ.get("DASHSCOPE_PLAN"))
        requested_plan = args.dashscope_plan or os.environ.get("DASHSCOPE_PLAN") or DEFAULT_DASHSCOPE_PLAN
        dashscope_plan_name, dashscope_plan_info = resolve_dashscope_plan(requested_plan)
        if not dashscope_plan_info:
            print(f"ERROR: unknown DashScope plan '{requested_plan}'. Run --list-dashscope-plans.", file=sys.stderr)
            return 2

    if provider == "dashscope":
        plan_key_var = dashscope_plan_info["api_key_var"]
        api_key = args.api_key or os.environ.get(plan_key_var)
    else:
        api_key = args.api_key or os.environ.get(env_name(provider, "API_KEY"))
    if not api_key:
        if provider == "dashscope":
            names = [dashscope_plan_info["api_key_var"]]
            print(f"ERROR: no API key for DashScope plan '{dashscope_plan_name}'. "
                  f"Set one of {', '.join(dict.fromkeys(names))} in {env_path}, export it, or pass --api-key.",
                  file=sys.stderr)
        else:
            print(f"ERROR: no API key for provider '{provider}'. "
                  f"Put {env_name(provider,'API_KEY')} in {env_path}, export it, or pass --api-key.",
                  file=sys.stderr)
        return 2

    if provider == "dashscope":
        base_url = (args.base_url
                    or os.environ.get(dashscope_env_name(dashscope_plan_name, "BASE_URL"))
                    or (None if explicit_dashscope_plan else os.environ.get(env_name(provider, "BASE_URL")))
                    or dashscope_plan_info["base_url"])
        if "{WorkspaceId}" in base_url:
            workspace_id = args.workspace_id or os.environ.get("DASHSCOPE_WORKSPACE_ID")
            if not workspace_id:
                print("ERROR: DashScope Singapore URL needs --workspace-id or DASHSCOPE_WORKSPACE_ID.", file=sys.stderr)
                return 2
            base_url = base_url.replace("{WorkspaceId}", workspace_id)
    else:
        base_url = (args.base_url
                    or os.environ.get(env_name(provider, "BASE_URL"))
                    or (defaults["base_url"] if defaults else None))
    if not base_url:
        print(f"ERROR: no base URL for provider '{provider}'. "
              f"Set {env_name(provider,'BASE_URL')} in {env_path} or pass --base-url.", file=sys.stderr)
        return 2

    if provider == "dashscope":
        model = (args.model
                 or os.environ.get(dashscope_env_name(dashscope_plan_name, "MODEL"))
                 or os.environ.get(env_name(provider, "MODEL"))
                 or dashscope_plan_info["model"])
        model_alias_from = None
        if args.use_model_alias:
            model, model_alias_from = normalize_dashscope_model(model, dashscope_plan_info)
    else:
        model = (args.model
                 or os.environ.get(env_name(provider, "MODEL"))
                 or (defaults["model"] if defaults else None))
        model_alias_from = None
    if not model:
        print(f"ERROR: no model for provider '{provider}'. "
              f"Set {env_name(provider,'MODEL')} in {env_path} or pass --model.", file=sys.stderr)
        return 2

    # base_url is the OpenAI-compatible root (without /chat/completions);
    # the SDK appends the path itself.
    client = OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)

    print(f"provider: {provider}")
    if provider == "dashscope":
        print(f"dashscope_plan: {dashscope_plan_name}")
    print(f"Calling {base_url}/chat/completions")
    print(f"  model:  {model}")
    if model_alias_from:
        print(f"  alias:  {model_alias_from} -> {model}")
    print(f"  prompt: {args.prompt!r}")
    if args.max_tokens is not None:
        print(f"  max_tokens: {args.max_tokens}")
    if args.temperature is not None:
        print(f"  temperature: {args.temperature}")
    if args.stream:
        print("  stream: on")
    print()

    kwargs = dict(
        model=model,
        messages=[{"role": "user", "content": args.prompt}],
    )
    if args.max_tokens is not None:
        kwargs["max_tokens"] = args.max_tokens
    if args.temperature is not None:
        kwargs["temperature"] = args.temperature

    try:
        if args.stream:
            print("Reply (streamed):")
            collected = []
            for chunk in client.chat.completions.create(stream=True, **kwargs):
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    collected.append(delta)
                    print(delta, end="", flush=True)
            print()
            content = "".join(collected)
        else:
            resp = client.chat.completions.create(**kwargs)
            content = resp.choices[0].message.content
            print("Reply:")
            print(content)
    except OpenAIError as exc:
        # Covers auth errors, bad model, rate limits, network/timeout, etc.
        print(f"API ERROR: {exc}", file=sys.stderr)
        return 1

    print("\nOK — endpoint works.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
