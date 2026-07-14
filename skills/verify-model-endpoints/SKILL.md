---
name: verify-model-endpoints
description: Smoke-tests any OpenAI-compatible chat model endpoint — DashScope/Bailian plans and regions, DeepSeek, Moonshot/Kimi, Zhipu/GLM, SiliconFlow, OpenRouter, OpenAI, local Ollama — by firing a prompt and printing the reply. Use when you want to confirm a new API key / base URL / model name actually works end-to-end, debug "why does my model call 401/404/hang", or quickly compare a prompt across providers before wiring it into an app. The openai SDK pointed at a custom base_url does the work; .env holds per-provider credentials.
---

# Verify a model endpoint works (OpenAI-compatible)

## What this skill does
Most hosted model providers expose an OpenAI-compatible `/chat/completions`
API. That means one client — the `openai` SDK pointed at a custom `base_url`
— can smoke-test all of them. This skill is that one client:

1. Read a **provider** (`--provider dashscope`, `deepseek`, …) whose
   credentials live in this skill's `.env`.
2. For DashScope/Bailian, optionally select a plan/region
   (`--dashscope-plan token-plan`, `coding-plan`, `payg-us`, …).
3. Fire a prompt, print the reply.
4. Done — the key, base URL, and model name are all correct.

If you got a model endpoint from somewhere (a vendor dashboard, a teammate,
`install-claude-code-windows`'s internal endpoint) and want to confirm it
actually answers before wiring it into anything, use this.

## Providers supported
Each is a trio `<PROVIDER>_API_KEY` / `<PROVIDER>_BASE_URL` / `<PROVIDER>_MODEL`
in `.env`. `base_url` and `model` have built-in defaults, so for a known
provider you usually only need the API key.

| Provider | Base URL default | Note |
|---|---|---|
| `dashscope` | plan-specific, default `https://dashscope.aliyuncs.com/compatible-mode/v1` | Aliyun DashScope/Bailian OpenAI-compatible mode |
| `deepseek` | `https://api.deepseek.com/v1` | DeepSeek official |
| `moonshot` | `https://api.moonshot.cn/v1` | Moonshot / Kimi |
| `zhipu` | `https://open.bigmodel.cn/api/paas/v4` | Zhipu / GLM (bigmodel.cn) |
| `siliconflow` | `https://api.siliconflow.cn/v1` | SiliconFlow — model name is `owner/model` |
| `openrouter` | `https://openrouter.ai/api/v1` | OpenRouter — model name is `owner/model` |
| `openai` | `https://api.openai.com/v1` | OpenAI official |
| `ollama` | `http://localhost:11434/v1` | Local `ollama serve`; API key ignored — pass `--api-key dummy` |

Add a row to `PROVIDER_DEFAULTS` in `verify_endpoint.py` (or just set the
three env vars) to support a new endpoint.

## DashScope/Bailian plans
DashScope has multiple billing plans, and their credentials are not
interchangeable. Use `--list-dashscope-plans` to see the built-in matrix.

| Plan | Base URL default | API key env | Notes |
|---|---|---|---|
| `payg-beijing` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | Pay-as-you-go, China North 2 Beijing |
| `payg-singapore` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | Needs `--workspace-id` or `DASHSCOPE_WORKSPACE_ID` |
| `payg-us` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_API_KEY` | Pay-as-you-go, US Virginia |
| `token-plan` | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `DASHSCOPE_TOKEN_PLAN_API_KEY` | Token Plan team key only |
| `coding-plan` | `https://coding.dashscope.aliyuncs.com/v1` | `DASHSCOPE_CODING_PLAN_API_KEY` | Coding Plan key only |

Select a plan with `--dashscope-plan` or `DASHSCOPE_PLAN`. You can also set
plan-specific overrides like `DASHSCOPE_TOKEN_PLAN_MODEL` or
`DASHSCOPE_CODING_PLAN_BASE_URL`; CLI flags still win.

DashScope model aliases are available for Cursor-plan compatibility, but the
skill preserves the model name exactly by default. Pass `--use-model-alias`
when you want the documented alias rewrite:

| Written as | Sent as |
|---|---|
| `kimi-k2.6` | `kimi-k2-6` |
| `kimi-k2.5` | `kimi-k2-5` |
| `glm-5.2` | `glm-5-2` |
| `glm-5.1` | `glm-5-1` |
| `glm-5` | `glm-5-0` |

Coding Plan only documents these aliases: `kimi-k2.5 -> kimi-k2-5`,
`glm-4.7 -> glm-4-7`, and `glm-5 -> glm-5-0`.

## Setup — one-time
The Python deps (`openai`, `python-dotenv`) live in the repo's `./.venv`.
Always run the script with the venv interpreter — never bare `python3` (which
hits a global env that doesn't have these packages).

```bash
# If not already installed in the venv:
./.venv/bin/pip install openai python-dotenv
```

Credentials go in this skill's **`.env`** (next to `SKILL.md`):
```bash
# Copy the template, then edit with real keys
cp skills/verify-model-endpoints/.env.example skills/verify-model-endpoints/.env
```
`.env` is gitignored (the repo's `.env` rule ignores it at any depth); only
`.env.example` is committed.

## How to run (from the repo root)
```bash
# Default provider is dashscope (the one with keys in .env)
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py

# Pick a different configured provider
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --provider deepseek

# See which providers have an API key set, + their default base_url/model
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --list-providers

# See DashScope/Bailian plans, base URLs, API key vars, and aliases
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --list-dashscope-plans

# Test a specific DashScope/Bailian plan or region
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py \
    --provider dashscope --dashscope-plan token-plan --model glm-5.2

./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py \
    --provider dashscope --dashscope-plan payg-singapore --workspace-id YOUR_WORKSPACE_ID --model glm-5.2

# Override anything ad hoc — no .env entry needed (e.g. a local server)
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py \
    --base-url http://localhost:11434/v1 --api-key dummy --model qwen2.5:7b

# Test streaming + sampling params
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --stream --max-tokens 64 --temperature 0.9

# Custom prompt
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --prompt "Reply with just 'pong'"
```

Each flag overrides the `.env`/env value for that run — nothing is written.

## The one non-obvious thing: base_url is the *root*, not the path
`base_url` must be the OpenAI root **without** `/chat/completions`:
- ✅ `https://dashscope.aliyuncs.com/compatible-mode/v1`
- ❌ `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

The SDK appends `/chat/completions` itself. If you point it at the full path,
every request 404s. The built-in defaults are already correct; only watch
this if you set a `*_BASE_URL` yourself or pass `--base-url`.

## Verify (quick smoke test)
```bash
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --list-providers
./.venv/bin/python skills/verify-model-endpoints/verify_endpoint.py --provider dashscope
```
Exit 0 = endpoint answered; exit 1 = API error (auth/bad model/rate limit/
network, printed to stderr); exit 2 = config missing (no API key etc.).

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `The 'openai' package is not installed` | Ran with bare `python3` (global env) | Use `./.venv/bin/python …` (deps live in the venv) |
| `404 Not Found` on every request | `base_url` includes `/chat/completions` | Drop the path suffix — `base_url` is the root; SDK appends the path |
| `401 Unauthorized` | Wrong/stale API key | Check `<PROVIDER>_API_KEY` in `.env`; real env var wins over `.env` |
| `404 model not found` | Model name wrong for that provider | `--list-providers` shows defaults; vendor dashboards list available names |
| DashScope plan rejects a valid-looking key | API key does not match the selected plan | Use the plan-specific key env var shown by `--list-dashscope-plans` |
| DashScope Singapore says config missing | Workspace ID missing | Pass `--workspace-id` or set `DASHSCOPE_WORKSPACE_ID` |
| DashScope docs require a model alias | Cursor/Bailian plan docs say e.g. `glm-5.2` should be `glm-5-2` | Pass `--use-model-alias` |
| `model name is owner/model` style wrong | SiliconFlow/OpenRouter want `owner/model` | e.g. `Qwen/Qwen2.5-7B-Instruct`, `openai/gpt-4o-mini` |
| Connection refused / timeout | Endpoint unreachable, or wrong region URL | `curl <base_url>/models` to confirm reachability; for Ollama run `ollama serve` first |
| Ollama: auth error despite local server | `OpenAI(api_key='')` rejects empty | Pass `--api-key dummy` (value is ignored by Ollama) |
| `.env` values seem ignored | A real env var with the same name is set | `load_dotenv` doesn't overwrite env vars; `unset <VAR>` or override with the CLI flag |

## Notes
- The script resolves the `.env` path next to itself (`skills/verify-model-endpoints/.env`),
  so it works regardless of CWD. Override with `--env /path/to/.env`.
- `load_dotenv` does **not** overwrite existing real env vars — so a key set
  in your shell/CI takes precedence over `.env`. That's intentional for
  prod/CI overrides; unset the env var if you want the `.env` value instead.
- This is a **chat** smoke test. It doesn't cover embeddings, images,
  function-calling, or provider-specific extensions — just "does the model
  answer a prompt".
- Provider endpoints and model names drift; if a built-in default stops
  working, check the vendor's docs and update `PROVIDER_DEFAULTS` in
  `verify_endpoint.py`.
