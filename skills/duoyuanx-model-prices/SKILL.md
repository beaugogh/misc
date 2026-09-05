---
name: duoyuanx-model-prices
description: Fetches and lists the DuoyuanX (duoyuanx.com) model catalog with live prices — chat models (Claude, GPT, Gemini, Grok, GLM, Kimi, DeepSeek…) plus image and video generation models — from its /api/pricing endpoint, normalizing the three billing schemes (per-1M-token ratios, per-request USD, per-second video pricing) into one sortable table. Use when you want to know what a model costs on DuoyuanX, whether a model is listed there at all, which endpoint style (openai/anthropic/gemini) a model speaks, or to compare DuoyuanX prices before routing traffic there. Python 3 stdlib only, caches an offline JSON+Markdown snapshot.
---

# DuoyuanX model prices

## What this skill does

DuoyuanX is a Chinese model **reseller**: one account, one balance, many
vendors' models — Claude, GPT, Gemini, Grok, GLM, Kimi, DeepSeek, Qwen on the
chat side; Nano Banana / GPT-Image / Seedream / Midjourney on images;
Seedance / Veo / Kling / Vidu on video. It exposes
`https://duoyuanx.com/api/pricing` (no auth) with the whole catalog and price
list as JSON.

The raw payload is annoying to read directly because it mixes three billing
schemes in one flat list (the mapping is DuoyuanX's own — it ships in their
frontend bundle as `quota_type` 0/1/2 → 按量/按次/按秒计费):

| `quota_type` | Billing | Price fields |
|---|---|---|
| `0` | **按量 (per-token)** — USD per 1M tokens | `model_ratio` = input, `completion_ratio` = output, `cache_ratio` = cache hit |
| `1` | **按次 (per-request)** — USD per call | `model_price` |
| `2` | **按秒 (per-second)** — per generated second | `model_price` |

> **Currency caveat (q2):** q0/q1 prices reconcile as USD (q0 ratios match
> official vendor USD pricing 1:1), but q2 `model_price` matches vendor CNY
> rates 1:1 in the one description that states a currency (wan3.0:
> "CNY/秒 ¥0.30000/s" = model_price 0.3). Until verified with a billed call,
> per-second prices are rendered **without a currency symbol**.

`quota_type 2` covers the video task models (MiniMax-H3, kling-3.0-omni,
wan3.0-video…) — their "price" is per second of generated video, so a
10-second clip at 0.5/s costs 10× that, not 1×. A few models also embed
resolution-tier price tables in their `description` (e.g. wan3.0-video:
480P/720P/1080P at different ¥/s); `model_price` carries the cheapest tier.

This skill fetches that endpoint, normalizes all three schemes into one
per-category table sorted cheapest-first, optionally enriches it with
`/v1/models` (needs your API key; adds `owned_by`, endpoint compatibility,
and marks which models your key can actually call), and caches a JSON +
Markdown snapshot you can filter offline.

Ported from transcribe-and-align's `src/taa/pipeline/model_prices.py` (the
duoyuanx half) so it runs **standalone: Python 3.9+ stdlib only** — no venv,
no `requests`, no third-party packages. The cached JSON shape matches the
original tool's, so either can read the other's cache.

## Quick start

```bash
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh   # fetch + cache
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list      # offline read
```

## Commands

```bash
# refresh — fetch live pricing, print it, and write output/duoyuanx.{json,md}
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh --dry-run    # fetch + print, write nothing
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh --type image # filter the printed table too
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh --api-key sk-xxx   # enrich via /v1/models

# list — read the cached snapshot without any network access
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --type video
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --model gpt        # substring on model id or org
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --format markdown  # or json / table (default)
python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --compare-models gpt-image-2,grok-4,veo_3_1-4K
```

Filters (`--type`, `--model`, `--format`) apply to both commands;
`--compare-models` checks listed/MISSING against the **whole** snapshot,
ignoring filters.

Output lands in `skills/duoyuanx-model-prices/output/` (gitignored). Use
`--cache-dir <path>` to redirect — e.g. point it at transcribe-and-align's
`data/model_prices/` to reuse that pipeline's cache and vice versa.

## Reading the output

Table example (trimmed):

```
Org        Model ID              Type   Inputs    Unit         Input Price  Output Price
---------- --------------------  -----  --------  -----------  -----------  -----------
Google     gemini-2.5-flash-lite  chat  text      token ratio  0.05         4
xAI        grok-4                chat  text      per request  0.04         N/A
ByteDance  doubao-seedance...    video text,...  per video    0.75         N/A
```

- **token ratio** rows: input/cache/output are USD per 1M tokens (按量计费).
- **per request / per image / per video** rows: one USD price per call (按次计费).
- **per second** rows: price per generated second of video (按秒计费),
  rendered currency-neutral — multiply
  by the clip length for the real cost.
- `免费` means free; `N/A` means the field is absent or zero.
- Markdown format renders the Chinese labels from DuoyuanX's own pricing page
  (`按量计费: 输入价格 $0.05 / 1M Tokens; …`, `按次计费: 模型价格 $0.04 / 次`).
- The **Org** column is inferred from model-name patterns and `vendor_id`
  (vendor→org map in `_duoyuanx_vendor_org`); unknown vendors show `N/A`.
- **Context** and endpoint columns: `context_length` is present for only ~15
  of ~90 models; endpoint compatibility (`openai` / `anthropic` / `gemini`)
  comes from `supported_endpoint_types` in the pricing payload itself.
- Tiered/conditional billing (a few models use `billing_mode: tiered_expr`
  with an expression like `len < 200000 ? …`) is kept verbatim in the JSON
  `extra.billing_expr` — the table shows the base price only.

## API key (optional enrichment)

`refresh` works with no credentials. With a key, it also calls
`/v1/models` and marks `available: true` for models your key can call, adds
`owned_by`, and merges endpoint types — useful to catch models that are
*priced* but not *routable* on your account (e.g. grok-4 has appeared in
`/v1/models` while missing from pricing, and vice versa).

Key resolution order: `--api-key` flag → `DUOYUANX_API_KEY` real env var →
`skills/duoyuanx-model-prices/.env` → misc-repo-root `.env` (never commit
either file). The same key the transcribe-and-align `duoyuanx` image backend
uses works.

## Network notes

- `urllib` honors `HTTP(S)_PROXY` env vars; with **no** proxy env vars set,
  macOS falls back to the system (scutil) proxy automatically. **Gotcha:** any
  proxy env var — even a bare `no_proxy` — suppresses that fallback entirely.
  If the direct route is broken, pass the local proxy explicitly:
  `--proxy http://127.0.0.1:15236`. `--no-proxy` bypasses every proxy,
  including env vars.
- Windows consoles use legacy code pages (cp1252/GBK) that can't render the
  Chinese pricing labels. Run with `PYTHONUTF8=1` for correct output; without
  it, unencodable characters are replaced with `?` instead of crashing.
- A trailing `/v1` in `--base-url` (OpenAI-style) is stripped automatically.

## Porting notes / provenance

Behavior-identical port of the duoyuanx half of
`transcribe-and-align/src/taa/pipeline/model_prices.py` (same normalization,
same JSON cache shape, same table semantics minus the `provider` column,
which is constant here). Differences worth knowing:

- `requests` replaced by `urllib.request` (stdlib-only constraint of this
  repo — no venv needed; run with system `python3`).
- SiliconFlow support dropped (that provider scrapes a Next.js-embedded
  pricing page — irrelevant outside transcribe-and-align).
- `--compare-config` (diff cache against `config.yaml` `model_providers`)
  replaced by `--compare-models` (explicit list — no config file to read here).
- Vendor→org map extended with vendors 3/10/11/40 (DeepSeek, Zhipu, Moonshot,
  Midjourney) observed in the live payload.
- `_load_dotenv` is a minimal stdlib reimplementation of python-dotenv's
  default behavior (real env wins; only missing keys are set; `export `
  prefixes and trailing comments supported).
- **Empty-fetch guard**: if the API returns zero models (outage or payload
  shape change), `refresh` keeps the existing cache and warns instead of
  overwriting it with an empty snapshot.
- **Windows-safe output**: stdout/stderr are reconfigured with
  `errors="replace"` so CJK pricing labels degrade to `?` on cp1252/GBK
  consoles rather than crashing before the cache is written. `PYTHONUTF8=1`
  still gives correct rendering.
- Cached JSON rows carry a constant `"provider": "duoyuanx"` key for exact
  cache-shape parity with taa (rendered tables still omit that constant
  column). A trailing `/v1` in `--base-url` is stripped.

If the two implementations drift, prefer fixing them in lockstep — the JSON
cache must stay readable by both.
