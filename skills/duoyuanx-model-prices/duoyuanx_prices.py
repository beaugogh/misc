#!/usr/bin/env python3
"""Fetch, cache, and list DuoyuanX (duoyuanx.com) model prices.

DuoyuanX is a Chinese model reseller exposing Claude / GPT / Gemini / Grok
chat models plus image- and video-generation models over OpenAI-, Anthropic-,
and Gemini-compatible endpoints. Its catalog and prices change often, and the
pricing API mixes two billing schemes in one payload:

  quota_type 0     per-token billing — model_ratio / completion_ratio /
                   cache_ratio are USD prices per 1M tokens
  quota_type 1     per-request billing — model_price is USD per call
  quota_type 2     per-second billing — model_price is per generated second
                   (video task models; the site labels these 按秒计费; the
                   currency is ambiguous — CNY per wan3.0's description,
                   USD per the site's default display — so rendered bare)

This script pulls https://duoyuanx.com/api/pricing (no auth), optionally
enriches it with https://duoyuanx.com/v1/models (needs an API key; adds
owned_by / endpoint types / availability), normalizes both schemes into one
table, and caches a JSON + Markdown snapshot you can list and filter offline.

Ported from transcribe-and-align's src/taa/pipeline/model_prices.py (the
duoyuanx half) so it runs standalone: Python 3.9+ stdlib only — no venv, no
third-party packages.

USAGE (run from the misc repo root, or anywhere — paths resolve from __file__)
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh --dry-run
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py refresh --api-key sk-...
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --type image
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --model gpt --format markdown
  python3 skills/duoyuanx-model-prices/duoyuanx_prices.py list --compare-models gpt-image-2,grok-4

ENV
  DUOYUANX_API_KEY  optional; enables /v1/models enrichment (the same key the
                    image backend uses). Resolution order: --api-key flag >
                    real environment > skills/duoyuanx-model-prices/.env >
                    misc-repo-root .env (never committed). .env lines may use
                    `export KEY=value` shell syntax.
  HTTP(S)_PROXY     honored by default (urllib behavior); with no proxy env
                    vars set, macOS falls back to the system (scutil) proxy.
                    Gotcha: ANY proxy env var — even a bare no_proxy —
                    suppresses that fallback. --proxy URL forces one;
                    --no-proxy goes direct.
  PYTHONUTF8=1      recommended on Windows: consoles use legacy code pages
                    (cp1252/GBK) that can't render the Chinese pricing labels;
                    without it unencodable characters become `?` (never crash).

CACHE
  <skill dir>/output/duoyuanx.json   machine-readable snapshot (gitignored)
  <skill dir>/output/duoyuanx.md     human-readable snapshot (gitignored)
  --cache-dir redirects both. The JSON shape matches transcribe-and-align's
  data/model_prices/duoyuanx.json, so either tool can read the other's cache.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping

PROVIDER = "duoyuanx"
DUOYUANX_BASE_URL = "https://duoyuanx.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
)
DEFAULT_TIMEOUT = 20
DEFAULT_CACHE_DIR = Path(__file__).resolve().parent / "output"

LIST_KEYS = ("data", "models", "items", "list", "records", "result")
MODEL_ID_KEYS = ("model_name", "modelName", "model_id", "modelId", "model", "id", "name")
CONTEXT_KEYS = (
    "context_length",
    "contextLength",
    "context_window",
    "contextWindow",
    "max_context",
    "maxContext",
    "max_tokens",
)
CACHE_PRICE_KEYS = (
    "cache_price",
    "cachePrice",
    "cache_hit_price",
    "cacheHitPrice",
    "cached_input_price",
    "cachedInputPrice",
)
INPUT_PRICE_KEYS = (
    "input_price",
    "inputPrice",
    "prompt_price",
    "promptPrice",
    "input",
    "prompt",
)
OUTPUT_PRICE_KEYS = (
    "output_price",
    "outputPrice",
    "completion_price",
    "completionPrice",
    "output",
    "completion",
)
FLAT_PRICE_KEYS = (
    "price",
    "image_price",
    "imagePrice",
    "video_price",
    "videoPrice",
    "audio_price",
    "audioPrice",
    "realTimePrice",
    "real_time_price",
)

TYPE_ORDER = {
    "chat": 0,
    "text": 0,
    "image": 1,
    "text-to-image": 1,
    "video": 2,
    "text-to-video": 2,
    "image-to-video": 3,
    "audio": 4,
    "text-to-speech": 4,
    "speech-to-text": 5,
    "embedding": 6,
    "reranker": 7,
}


@dataclass(frozen=True)
class ModelPrice:
    model_id: str
    category: str = ""
    org: str = ""
    context: str = "N/A"
    pricing_unit: str = "N/A"
    cache_hit: str = "N/A"
    input_price: str = "N/A"
    output_price: str = "N/A"
    input_modalities: tuple[str, ...] = ()
    output_modalities: tuple[str, ...] = ()
    source: str = ""
    endpoint_types: tuple[str, ...] = ()
    available: bool | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelPriceSnapshot:
    provider: str
    fetched_at: str
    source: str
    rows: list[ModelPrice]
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def _build_opener(proxy: str | None, no_proxy: bool) -> urllib.request.OpenerDirector:
    if no_proxy:
        handler = urllib.request.ProxyHandler({})  # bypass every proxy, even env vars
    elif proxy:
        handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
    else:
        handler = urllib.request.ProxyHandler()  # default: honor HTTP(S)_PROXY env vars
    return urllib.request.build_opener(handler)


def _get_json(
    opener: urllib.request.OpenerDirector,
    url: str,
    headers: Mapping[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Any:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json", **(headers or {})},
    )
    with opener.open(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_duoyuanx(
    timeout: int = DEFAULT_TIMEOUT,
    base_url: str = DUOYUANX_BASE_URL,
    api_key: str = "",
    proxy: str | None = None,
    no_proxy: bool = False,
) -> ModelPriceSnapshot:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/v1"):  # tolerate OpenAI-style base URLs
        base_url = base_url[: -len("/v1")]
    opener = _build_opener(proxy, no_proxy)
    pricing_url = f"{base_url}/api/pricing"
    pricing_payload = _get_json(opener, pricing_url, timeout=timeout)

    model_payload: Any = None
    if api_key:
        try:
            model_payload = _get_json(
                opener,
                _duoyuanx_url(base_url, "/v1/models"),
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=timeout,
            )
        except (urllib.error.URLError, ValueError, TimeoutError) as exc:
            print(
                f"Note: /v1/models enrichment failed ({exc}); continuing with pricing data only.",
                file=sys.stderr,
            )
    else:
        print(
            "Note: no API key set; skipped /v1/models enrichment "
            "(set DUOYUANX_API_KEY or --api-key).",
            file=sys.stderr,
        )

    rows = normalize_duoyuanx_payload(
        pricing_payload,
        models_payload=model_payload,
        source=pricing_url,
    )
    return ModelPriceSnapshot(
        provider=PROVIDER,
        fetched_at=_now_iso(),
        source=pricing_url,
        rows=rows,
        metadata={
            "source_type": "api_pricing",
            "models_enriched": model_payload is not None,
        },
    )


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def normalize_duoyuanx_payload(
    pricing_payload: Mapping[str, Any] | list[Any],
    models_payload: Mapping[str, Any] | None = None,
    source: str = "",
) -> list[ModelPrice]:
    pricing_rows = _find_model_list(pricing_payload)
    model_rows = _find_model_list(models_payload or {})
    model_metadata = {
        str(row.get("id") or row.get("model") or row.get("model_name") or ""): row
        for row in model_rows
        if isinstance(row, Mapping)
    }
    rows: list[ModelPrice] = []
    for item in pricing_rows:
        if not isinstance(item, Mapping):
            continue
        model_id = str(_pick(item, MODEL_ID_KEYS) or "")
        if not model_id:
            continue
        metadata = model_metadata.get(model_id, {})
        category = _canonical_category(str(item.get("model_type") or item.get("type") or metadata.get("type") or ""))
        pricing_unit, cache_hit, input_price, output_price = _duoyuanx_price_fields(item, category)
        input_modalities = _string_tuple(
            item.get("input_modalities") or metadata.get("input_modalities") or ()
        )
        output_modalities = _string_tuple(
            item.get("output_modalities") or metadata.get("output_modalities") or ()
        )
        input_modalities, output_modalities = _duoyuanx_effective_modalities(
            category,
            model_id,
            input_modalities,
            output_modalities,
        )
        endpoint_types = tuple(str(v) for v in (
            metadata.get("supported_endpoint_types")
            or item.get("supported_endpoint_types")
            or item.get("endpoints")
            or []
        ))
        rows.append(
            ModelPrice(
                org=str(metadata.get("owned_by") or item.get("owned_by") or item.get("vendor_id") or ""),
                model_id=model_id,
                category=category,
                context=_format_context(_pick(item, CONTEXT_KEYS) or _pick(metadata, CONTEXT_KEYS)),
                pricing_unit=pricing_unit,
                cache_hit=cache_hit,
                input_price=input_price,
                output_price=output_price,
                input_modalities=input_modalities,
                output_modalities=output_modalities,
                source=source,
                endpoint_types=endpoint_types,
                available=True if metadata else None,
                extra=_compact_extra(item, metadata),
            )
        )
    return sort_rows(rows)


def _find_model_list(payload: Mapping[str, Any] | list[Any]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, Mapping):
        return []
    for key in LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, Mapping):
            nested = _find_model_list(value)
            if nested:
                return nested
    best: list[dict[str, Any]] = []
    stack = list(payload.values())
    while stack:
        value = stack.pop()
        if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            if len(value) > len(best):
                best = list(value)
        elif isinstance(value, Mapping):
            stack.extend(value.values())
    return best


def _duoyuanx_price_fields(item: Mapping[str, Any], category: str) -> tuple[str, str, str, str]:
    quota_type = item.get("quota_type")
    model_ratio = item.get("model_ratio")
    completion_ratio = item.get("completion_ratio")
    cache_ratio = item.get("cache_ratio")
    # quota_type is the authoritative billing enum (the frontend maps 0/1/2 to
    # 按量/按次/按秒计费). Ratio sniffing only classifies when the enum is
    # absent — a stray nonzero ratio on a per-request row (e.g. grok-4.5's
    # cache_ratio=0.25 with model_price=$0.01) must NOT flip it to token
    # pricing, and must not leak into the cache-hit field.
    if quota_type in (0, "0"):
        return (
            "token ratio",
            _format_duoyuanx_price(cache_ratio),
            _format_duoyuanx_price(model_ratio),
            _format_duoyuanx_price(completion_ratio),
        )
    if quota_type in (1, "1", 2, "2"):
        model_price = item.get("model_price")
        if model_price not in (None, ""):
            return (
                _duoyuanx_pricing_unit(category, item),
                "N/A",
                _format_duoyuanx_price(model_price),
                "N/A",
            )
        # q1/q2 without model_price: fall through to generic price keys below
        # rather than misreading stray ratios as token pricing.
    elif any(_has_nonzero_price(value) for value in (model_ratio, completion_ratio, cache_ratio)):
        return (
            "token ratio",
            _format_duoyuanx_price(cache_ratio),
            _format_duoyuanx_price(model_ratio),
            _format_duoyuanx_price(completion_ratio),
        )
    model_price = item.get("model_price")
    if model_price not in (None, ""):
        return (
            _duoyuanx_pricing_unit(category, item),
            "N/A",
            _format_duoyuanx_price(model_price),
            "N/A",
        )
    input_price = _format_duoyuanx_price(_pick_exact(item, INPUT_PRICE_KEYS))
    output_price = _format_duoyuanx_price(_pick_exact(item, OUTPUT_PRICE_KEYS))
    flat_price = _duoyuanx_flat_price(item)
    if input_price == "N/A" and flat_price != "N/A":
        input_price = flat_price
    return (
        _duoyuanx_pricing_unit(category, item),
        _format_duoyuanx_price(_pick(item, CACHE_PRICE_KEYS)),
        input_price,
        output_price,
    )


def _duoyuanx_pricing_unit(category: str, item: Mapping[str, Any]) -> str:
    unit = item.get("unit") or item.get("pricing_unit") or item.get("unitZhCnName")
    if unit:
        return str(unit)
    if item.get("quota_type") in (2, "2"):
        # 按秒计费: billed per generated second (video task models)
        return "per second"
    if item.get("quota_type") in (1, "1"):
        if category == "image":
            return "per image"
        if category == "video":
            return "per video"
        return "per request"
    if category == "image":
        return "per image"
    if category == "video":
        return "per video"
    if category == "audio":
        return "1K chars"
    return "1M tokens"


def _duoyuanx_flat_price(item: Mapping[str, Any]) -> str:
    for key in FLAT_PRICE_KEYS:
        value = item.get(key)
        if value not in (None, ""):
            return _format_duoyuanx_price(value)
    pricing = item.get("pricing")
    if isinstance(pricing, list):
        values = [
            _format_duoyuanx_price(row.get("price"))
            for row in pricing
            if isinstance(row, Mapping) and row.get("price") not in (None, "")
        ]
        values = [value for value in values if value != "N/A"]
        if values:
            return "<br>".join(values)
    return "N/A"


def _format_duoyuanx_price(value: Any) -> str:
    if value in (None, ""):
        return "N/A"
    if isinstance(value, str) and ("¥" in value or "$" in value or "免费" in value):
        return value.strip()
    try:
        price = Decimal(str(value))
    except InvalidOperation:
        return str(value)
    if price == 0:
        return "免费"
    return str(price.normalize())


def _has_nonzero_price(value: Any) -> bool:
    if value in (None, ""):
        return False
    try:
        return Decimal(str(value)) != 0
    except InvalidOperation:
        return True


def _duoyuanx_effective_modalities(
    category: str,
    model_id: str,
    input_modalities: tuple[str, ...],
    output_modalities: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Apply documented DuoyuanX family input modes over coarse provider metadata."""
    model = model_id.lower()
    if category == "image":
        return _merge_modalities(input_modalities, ("text", "image")), ("image",)
    if category != "video":
        return input_modalities, output_modalities
    if model.startswith("doubao-seedance-1-5-pro"):
        return ("text", "image"), ("video",)
    if model.startswith("doubao-seedance-2-0"):
        return ("text", "image", "video", "audio"), ("video",)
    if model.startswith("grok-video") or model.startswith("grok-1.5-video"):
        return ("text", "image"), ("video",)
    if model.startswith("veo"):
        return ("text", "image"), ("video",)
    if model == "omni-fast-v2v":
        return ("text", "image", "video"), ("video",)
    if model == "omni-fast":
        return ("text", "image"), ("video",)
    if model.startswith(("kling", "vidu")) or model.startswith(("viduq", "jimeng", "hailuo")):
        return ("text", "image", "video"), ("video",)
    if input_modalities == ("video",):
        return ("text", "image", "video"), ("video",)
    return input_modalities, output_modalities or ("video",)


def _merge_modalities(
    current: tuple[str, ...],
    additions: tuple[str, ...],
) -> tuple[str, ...]:
    values = []
    for item in (*current, *additions):
        if item and item not in values:
            values.append(item)
    return tuple(values)


def _compact_extra(item: Mapping[str, Any], metadata: Mapping[str, Any]) -> dict[str, Any]:
    extra: dict[str, Any] = {}
    for key in (
        "description",
        "vendor_id",
        "input_modalities",
        "output_modalities",
        "group",
        "groups",
        "quota_type",
        "model_ratio",
        "model_price",
        "completion_ratio",
        "cache_ratio",
        "create_cache_ratio",
        "enable_groups",
        # Tiered/conditional billing (billing_mode "tiered_expr" carries the
        # real pricing rule in billing_expr — rendered only here, not in tables).
        "billing_mode",
        "billing_expr",
        "max_output_tokens",
    ):
        if key in item:
            extra[key] = item[key]
    for key in ("owned_by", "created", "supported_endpoint_types"):
        if key in metadata:
            extra[key] = metadata[key]
    return extra


def _known_model_org(model_id: str) -> str:
    model = model_id.lower()
    rules = [
        (("claude",), "Anthropic"),
        (("gemini", "veo",), "Google"),
        (("gpt-", "openai",), "OpenAI"),
        (("grok",), "xAI"),
        (("doubao", "seedance", "seedream",), "ByteDance"),
        (("deepseek",), "DeepSeek"),
        (("qwen",), "Alibaba"),
        (("glm",), "Zhipu AI"),
        (("kimi",), "Moonshot AI"),
        (("minimax",), "MiniMax"),
        (("kling",), "Kuaishou"),
        (("vidu", "viduq",), "Vidu"),
        (("midjourney",), "Midjourney"),
        (("mimo",), "Xiaomi"),
        (("hunyuan",), "Tencent"),
        (("ernie",), "Baidu"),
    ]
    for needles, org in rules:
        if any(needle in model for needle in needles):
            return org
    return ""


def _duoyuanx_vendor_org(vendor_id: Any) -> str:
    mapping = {
        "1": "Anthropic",
        "2": "OpenAI",
        "3": "DeepSeek",
        "4": "Google",
        "8": "Vidu",
        "10": "Zhipu AI",
        "11": "Moonshot AI",
        "12": "Alibaba",
        "18": "Kuaishou",
        "21": "ByteDance",
        "23": "MiniMax",
        "40": "Midjourney",
        "41": "xAI",
    }
    return mapping.get(str(vendor_id or ""))


def _display_org(row: ModelPrice) -> str:
    org = _known_model_org(row.model_id)
    if org:
        return org
    org = (row.org or "").strip()
    mapped = _duoyuanx_vendor_org(row.extra.get("vendor_id"))
    if mapped:
        return mapped
    if org in {"", "custom"} or org.isdigit():
        return "N/A"
    return org or "N/A"


def _canonical_category(value: str) -> str:
    text = (value or "").lower().replace("_", "-")
    if text in {"", "llm", "text"}:
        return "chat"
    if text in {"chat", "embedding", "reranker", "image", "video", "audio"}:
        return text
    if "image" in text:
        return "image"
    if "video" in text:
        return "video"
    if "audio" in text or "speech" in text:
        return "audio"
    if "embed" in text:
        return "embedding"
    if "rank" in text:
        return "reranker"
    return text


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------


def sort_rows(rows: Iterable[ModelPrice]) -> list[ModelPrice]:
    """Sort by category, then cheapest input→output price.

    Within a category group — the unit each rendered table covers — rows run
    from cheapest to most costly, using the cheapest tier in each price field
    so any free tier sorts first. Org/model IDs break ties for equal prices;
    models with no parseable price sort last.
    """
    return sorted(
        rows,
        key=lambda row: (
            TYPE_ORDER.get(row.category, 99),
            _numeric_price(row.input_price),
            _numeric_price(row.output_price),
            row.org.lower(),
            row.model_id.lower(),
        ),
    )


_PRICE_NUMBER_RE = re.compile(r"[¥$]\s*(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)")
_PRICE_SPLIT_RE = re.compile(r"<br>|;")

# Unbounded sentinel: models with no parseable price sort last, free models first.
_PRICE_UNKNOWN = Decimal("Infinity")


def _numeric_price(value: Any) -> Decimal:
    """Cheapest numeric price embedded in a price string, for sorting.

    Each ``<br>``/``;``-separated tier is parsed independently and the minimum
    tier wins, so a model with any free tier sorts as free. Currency-prefixed
    numbers are extracted directly; bare numbers (DuoyuanX ratios /
    per-request USD) are parsed directly. ``免费`` maps to 0; ``N/A`` or
    anything unparseable sorts last.
    """
    if value is None:
        return _PRICE_UNKNOWN
    text = str(value).strip()
    if not text or text.lower() in {"n/a", "none", "null"}:
        return _PRICE_UNKNOWN
    prices: list[Decimal] = []
    for part in _PRICE_SPLIT_RE.split(text):
        segment = part.strip()
        if not segment:
            continue
        if "免费" in segment:
            prices.append(Decimal(0))
            continue
        prefixed = _PRICE_NUMBER_RE.findall(segment)
        if prefixed:
            prices.extend(d for d in (_safe_decimal(match) for match in prefixed) if d is not None)
            continue
        bare = _safe_decimal(segment)
        if bare is not None:
            prices.append(bare)
    if prices:
        return min(prices)
    return _PRICE_UNKNOWN


def _safe_decimal(text: str) -> Decimal | None:
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def filter_rows(
    rows: Iterable[ModelPrice],
    category: str | None = None,
    model_substring: str | None = None,
) -> list[ModelPrice]:
    result = list(rows)
    if category:
        wanted = category.lower()
        result = [row for row in result if row.category.lower() == wanted]
    if model_substring:
        needle = model_substring.lower()
        result = [
            row for row in result
            if needle in row.model_id.lower() or needle in _display_org(row).lower()
        ]
    return sort_rows(result)


def render_table(rows: Iterable[ModelPrice], source: str = "") -> str:
    lines = []
    if source:
        lines.append(f"Source: {source}")
        lines.append("")
    lines.extend(_table_lines(rows))
    return "\n".join(lines)


def render_markdown(rows: Iterable[ModelPrice], source: str = "") -> str:
    sorted_rows = sort_rows(rows)
    lines = []
    if source:
        lines.append(f"Source: {source}")
        lines.append("")
    for category, category_rows in _group_rows_by_category(sorted_rows):
        lines.append(f"## {_category_heading(category)}")
        lines.append("")
        lines.extend(_markdown_table_lines(category_rows))
        lines.append("")
    return "\n".join(lines) + "\n"


def render_json(rows: Iterable[ModelPrice]) -> str:
    return json.dumps([model_price_to_dict(row) for row in rows], ensure_ascii=False, indent=2)


def _group_rows_by_category(rows: Iterable[ModelPrice]) -> list[tuple[str, list[ModelPrice]]]:
    grouped: dict[str, list[ModelPrice]] = {}
    for row in rows:
        grouped.setdefault(row.category or "uncategorized", []).append(row)
    return sorted(
        grouped.items(),
        key=lambda item: (TYPE_ORDER.get(item[0], 99), item[0]),
    )


def _category_heading(category: str) -> str:
    labels = {
        "chat": "Chat Models",
        "image": "Image Models",
        "video": "Video Models",
        "audio": "Audio Models",
        "embedding": "Embedding Models",
        "reranker": "Reranker Models",
    }
    return labels.get(category, f"{category.title()} Models" if category else "Uncategorized Models")


def _table_lines(rows: Iterable[ModelPrice]) -> list[str]:
    sorted_rows = sort_rows(rows)
    include_context = any(row.category != "image" for row in sorted_rows)
    headers = [
        "Org",
        "Model ID",
        "Type",
        "Inputs",
        "Outputs",
        "Unit",
        "Cache",
        "Input Price",
        "Output Price",
    ]
    if include_context:
        headers.insert(5, "Context")
    body = [_row_cells(row, include_context) for row in sorted_rows]
    widths = [
        max(len(str(row[i])) for row in [headers, *body]) if body else len(header)
        for i, header in enumerate(headers)
    ]
    lines = ["  ".join(header.ljust(widths[i]) for i, header in enumerate(headers))]
    lines.append("  ".join("-" * width for width in widths))
    lines.extend("  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)) for row in body)
    return lines


def _row_cells(row: ModelPrice, include_context: bool) -> list[str]:
    cells = [
        _display_org(row),
        row.model_id,
        row.category,
        ", ".join(row.input_modalities) or "N/A",
        ", ".join(row.output_modalities) or "N/A",
        row.pricing_unit,
        row.cache_hit,
        row.input_price,
        row.output_price,
    ]
    if include_context:
        cells.insert(5, row.context)
    return cells


def _markdown_table_lines(rows: Iterable[ModelPrice]) -> list[str]:
    sorted_rows = sort_rows(rows)
    include_context = any(row.category != "image" for row in sorted_rows)
    candidates = [
        ("Org", _display_org, True),
        ("Model", lambda row: row.model_id, True),
        ("Inputs", lambda row: _modalities_text(row.input_modalities), True),
        ("Outputs", lambda row: _modalities_text(row.output_modalities), True),
        ("Context", lambda row: row.context, include_context),
        ("Pricing", _pricing_text, True),
    ]
    rendered_rows = [
        [(header, _blank_na(renderer(row)), enabled) for header, renderer, enabled in candidates]
        for row in sorted_rows
    ]
    keep_indexes = []
    for index, (header, _renderer, enabled) in enumerate(candidates):
        if not enabled:
            continue
        values = [row[index][1] for row in rendered_rows]
        if header in {"Org", "Model", "Pricing"} or any(_useful(value) for value in values):
            keep_indexes.append(index)
    headers = [candidates[index][0] for index in keep_indexes]
    lines = [
        "| " + " | ".join(_escape_md(header) for header in headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for rendered in rendered_rows:
        lines.append("| " + " | ".join(_escape_md(rendered[index][1]) for index in keep_indexes) + " |")
    return lines


def _pricing_text(row: ModelPrice) -> str:
    return _duoyuanx_pricing_text(row, (row.pricing_unit or "").strip())


def _duoyuanx_pricing_text(row: ModelPrice, normalized_unit: str) -> str:
    cache = _price_or_empty(row.cache_hit)
    input_price = _price_or_empty(row.input_price)
    output_price = _price_or_empty(row.output_price)
    if normalized_unit == "per second" and input_price:
        # q2 model_price currency is ambiguous (wan3.0's own description says
        # CNY/秒 1:1 with model_price; q0 ratios are demonstrably USD) — render
        # without a currency symbol rather than guess.
        return f"按秒计费: 模型价格 {input_price} / 秒"
    if normalized_unit in {"per image", "per video", "per request"} and input_price:
        return f"按次计费: 模型价格 {_format_usd(input_price)} / 次"
    if normalized_unit == "token ratio":
        parts = []
        if input_price:
            parts.append(f"输入价格 {_format_usd(input_price)} / 1M Tokens")
        if cache:
            parts.append(f"缓存价格 {_format_usd(cache)} / 1M Tokens")
        if output_price:
            parts.append(f"补全价格 {_format_usd(output_price)} / 1M Tokens")
        return "按量计费: " + "; ".join(parts) if parts else "按量计费"
    unit = _pricing_basis(normalized_unit)
    if input_price and not cache and not output_price:
        return f"{unit}: price {_format_usd(input_price)}"
    return _generic_pricing_text(unit, cache, input_price, output_price)


def _generic_pricing_text(unit: str, cache: str, input_price: str, output_price: str) -> str:
    parts = []
    if input_price:
        parts.append(f"input {input_price}")
    if cache:
        parts.append(f"cache {cache}")
    if output_price:
        parts.append(f"output {output_price}")
    if not parts:
        return unit
    return f"{unit}: " + "; ".join(parts)


def _pricing_basis(unit: str) -> str:
    normalized = (unit or "").strip()
    if not normalized or normalized == "N/A":
        return "pricing unavailable"
    if normalized == "per image":
        return "per image request"
    if normalized == "per video":
        return "per video request"
    if normalized == "per request":
        return "per request"
    if normalized == "1K chars":
        return "per 1K chars"
    if normalized == "token ratio":
        return "token pricing"
    return f"per {normalized}" if normalized[0].isdigit() else normalized


def _modalities_text(modalities: tuple[str, ...]) -> str:
    return ", ".join(modalities) if modalities else "N/A"


def _price_or_empty(value: str) -> str:
    return "" if not _useful(value) else value


def _format_usd(value: Any) -> str:
    if value in (None, ""):
        return "N/A"
    text = str(value).strip()
    if not text or text in {"N/A", "免费"}:
        return text or "N/A"
    if text.startswith("$"):
        return text
    try:
        price = Decimal(text.replace(",", ""))
    except InvalidOperation:
        return text
    return f"${price:.4f}"


def _format_context(value: Any) -> str:
    if value in (None, ""):
        return "N/A"
    try:
        context = Decimal(str(value))
    except InvalidOperation:
        return str(value)
    if context <= 0:
        return "N/A"
    if context >= 1_000_000:
        return f"{float(context / Decimal(1_000_000)):.1f}M"
    if context >= 1_000:
        return f"{float(context / Decimal(1_000)):.1f}K"
    return f"{context:g}"


def _useful(value: str) -> bool:
    return str(value).strip() not in {"", "N/A", "none", "None", "null"}


def _blank_na(value: str) -> str:
    return "" if not _useful(value) else value


def _escape_md(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def compare_models(rows: Iterable[ModelPrice], wanted: Iterable[str]) -> str:
    listed = {row.model_id for row in rows if row.model_id}
    lines = ["Model availability for duoyuanx (from the whole snapshot, unfiltered):"]
    for model in wanted:
        status = "listed " if model in listed else "MISSING"
        lines.append(f"  {status}  {model}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Snapshot cache
# ---------------------------------------------------------------------------


def cache_json_path(cache_dir: str | Path) -> Path:
    return Path(cache_dir) / f"{PROVIDER}.json"


def cache_markdown_path(cache_dir: str | Path) -> Path:
    return Path(cache_dir) / f"{PROVIDER}.md"


def write_snapshot(snapshot: ModelPriceSnapshot, cache_dir: str | Path) -> tuple[Path, Path]:
    directory = Path(cache_dir)
    directory.mkdir(parents=True, exist_ok=True)
    json_path = cache_json_path(directory)
    md_path = cache_markdown_path(directory)
    _write_json_atomic(json_path, snapshot_to_dict(snapshot))
    md_path.write_text(render_markdown(snapshot.rows, snapshot.source), encoding="utf-8")
    return json_path, md_path


def read_snapshot(cache_dir: str | Path) -> ModelPriceSnapshot:
    path = cache_json_path(cache_dir)
    if not path.exists():
        raise FileNotFoundError(
            f"Model price cache not found: {path}. Run `duoyuanx_prices.py refresh` first."
        )
    return snapshot_from_dict(json.loads(path.read_text(encoding="utf-8")))


def _write_json_atomic(path: str | Path, data: Mapping[str, Any]) -> None:
    """Write ``data`` as JSON to ``path`` atomically (temp file + os.replace),
    so a crash mid-write never leaves a truncated or empty snapshot."""
    target = Path(path)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, target)


def snapshot_to_dict(snapshot: ModelPriceSnapshot) -> dict[str, Any]:
    return {
        "provider": snapshot.provider,
        "fetched_at": snapshot.fetched_at,
        "source": snapshot.source,
        "metadata": snapshot.metadata,
        "models": [model_price_to_dict(row) for row in snapshot.rows],
    }


def snapshot_from_dict(data: Mapping[str, Any]) -> ModelPriceSnapshot:
    rows = data.get("models") or data.get("rows") or []
    return ModelPriceSnapshot(
        provider=str(data.get("provider", "")),
        fetched_at=str(data.get("fetched_at", "")),
        source=str(data.get("source", "")),
        metadata=dict(data.get("metadata", {})) if isinstance(data.get("metadata"), Mapping) else {},
        rows=[model_price_from_dict(row) for row in rows if isinstance(row, Mapping)],
    )


def model_price_to_dict(row: ModelPrice) -> dict[str, Any]:
    # provider key kept for cache-shape parity with taa's model_prices
    data = {"provider": PROVIDER, **asdict(row)}
    data["endpoint_types"] = list(row.endpoint_types)
    data["input_modalities"] = list(row.input_modalities)
    data["output_modalities"] = list(row.output_modalities)
    return data


def model_price_from_dict(data: Mapping[str, Any]) -> ModelPrice:
    extra = dict(data.get("extra", {})) if isinstance(data.get("extra"), Mapping) else {}
    endpoints = data.get("endpoint_types") or ()
    input_modalities = data.get("input_modalities")
    if input_modalities is None:
        input_modalities = extra.get("input_modalities") or ()
    output_modalities = data.get("output_modalities")
    if output_modalities is None:
        output_modalities = extra.get("output_modalities") or ()
    input_price = str(data.get("input_price", "N/A"))
    output_price = str(data.get("output_price", "N/A"))
    if _looks_like_modality_value(input_price):
        input_price = "N/A"
    if _looks_like_modality_value(output_price):
        output_price = "N/A"
    pricing_unit = str(data.get("pricing_unit", "N/A"))
    if pricing_unit == "1M tokens" and extra.get("quota_type") in (0, "0"):
        pricing_unit = "token ratio"
    elif extra.get("quota_type") in (2, "2") and pricing_unit in (
        "1M tokens", "per video", "per request",
    ):
        # pre-fix caches lumped q2 into per video/request (or 1M tokens)
        pricing_unit = "per second"
    elif pricing_unit == "1M tokens" and extra.get("quota_type") in (1, "1"):
        pricing_unit = "per request"
    input_modalities, output_modalities = _duoyuanx_effective_modalities(
        str(data.get("category", "")),
        str(data.get("model_id", "")),
        _string_tuple(input_modalities),
        _string_tuple(output_modalities),
    )
    return ModelPrice(
        model_id=str(data.get("model_id", "")),
        category=str(data.get("category", "")),
        org=str(data.get("org", "")),
        context=str(data.get("context", "N/A")),
        pricing_unit=pricing_unit,
        cache_hit=str(data.get("cache_hit", "N/A")),
        input_price=input_price,
        output_price=output_price,
        input_modalities=_string_tuple(input_modalities),
        output_modalities=_string_tuple(output_modalities),
        source=str(data.get("source", "")),
        endpoint_types=tuple(str(item) for item in endpoints),
        available=data.get("available") if isinstance(data.get("available"), bool) else None,
        extra=extra,
    )


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _pick(flat: Mapping[str, Any], keys: Iterable[str]) -> Any:
    normalized = {key.lower().replace("_", ""): key for key in flat}
    for wanted in keys:
        direct = normalized.get(wanted.lower().replace("_", ""))
        if direct is not None:
            return flat[direct]
    wanted_fragments = [key.lower().replace("_", "") for key in keys]
    for key, value in flat.items():
        compact = key.lower().replace("_", "")
        if any(fragment in compact for fragment in wanted_fragments):
            return value
    return None


def _pick_exact(flat: Mapping[str, Any], keys: Iterable[str]) -> Any:
    normalized = {key.lower().replace("_", ""): key for key in flat}
    for wanted in keys:
        direct = normalized.get(wanted.lower().replace("_", ""))
        if direct is not None:
            return flat[direct]
    return None


def _string_tuple(value: Any) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable) and not isinstance(value, Mapping):
        return tuple(str(item) for item in value if item not in (None, ""))
    return (str(value),)


def _looks_like_modality_value(value: str) -> bool:
    text = value.strip()
    if text in {"[]", "()"}:
        return True
    if not (text.startswith("[") and text.endswith("]")):
        return False
    return any(token in text for token in ("text", "image", "video", "audio", "file"))


def _duoyuanx_url(base_url: str, path: str) -> str:
    if base_url.endswith("/v1") and path.startswith("/v1/"):
        return base_url + path[len("/v1"):]
    return base_url + path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _load_dotenv() -> None:
    """Populate missing env vars from .env files, without python-dotenv.

    Real environment wins (values are only set when absent), matching
    python-dotenv's default. Checked: the skill dir's .env first, then the
    repo root's .env (misc repo convention for per-provider credentials).
    """
    skill_dir = Path(__file__).resolve().parent
    for candidate in (skill_dir / ".env", skill_dir.parent.parent / ".env"):
        try:
            text = candidate.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            if key.startswith("export "):  # python-dotenv / shell-style lines
                key = key[len("export "):].strip()
            value = value.strip()
            if value[:1] in {"'", '"'}:  # quoted: strip quotes, ignore trailing junk
                value = value[1 : value.find(value[0], 1)] if value[0] in value[1:] else value
            else:
                value = value.split(" #", 1)[0].rstrip()  # trailing comment
            if key and key not in os.environ:
                os.environ[key] = value


def _resolve_api_key(args: argparse.Namespace) -> str:
    if args.api_key:
        return args.api_key.strip()
    return os.environ.get("DUOYUANX_API_KEY", "").strip()


def _configure_streams() -> None:
    """Make printing CJK pricing labels safe on non-UTF-8 consoles (Windows
    cp1252/GBK): replace unencodable characters instead of crashing with
    UnicodeEncodeError before the cache is written."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(errors="replace")
        except (ValueError, OSError):
            pass


def _render(rows: list[ModelPrice], source: str, output_format: str) -> str:
    if output_format == "json":
        return render_json(rows)
    if output_format == "markdown":
        return render_markdown(rows, source).rstrip()
    return render_table(rows, source)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--type",
        dest="model_type_filter",
        choices=["chat", "image", "video", "embedding", "audio", "reranker"],
        default=None,
        help="Only show models of this normalized type.",
    )
    parser.add_argument(
        "--model",
        dest="model_filter",
        default=None,
        help="Only show models whose ID or org contains this substring.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json", "markdown"],
        default="table",
        help="Output format. Defaults to table.",
    )
    parser.add_argument(
        "--compare-models",
        default=None,
        help="Comma-separated model IDs to check against the snapshot (listed vs MISSING).",
    )
    parser.add_argument(
        "--cache-dir",
        default=None,
        help=f"Snapshot directory. Defaults to {DEFAULT_CACHE_DIR}",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch, cache, and list DuoyuanX (duoyuanx.com) model prices.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list",
        help="Read the cached pricing snapshot without contacting the network.",
    )
    _add_common_args(list_parser)

    refresh_parser = subparsers.add_parser(
        "refresh",
        help="Fetch live pricing and write the cached JSON/Markdown snapshots.",
    )
    _add_common_args(refresh_parser)
    refresh_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and render pricing without writing cache files.",
    )
    refresh_parser.add_argument(
        "--api-key",
        default=None,
        help="DuoyuanX API key for /v1/models enrichment (default: DUOYUANX_API_KEY env/.env).",
    )
    refresh_parser.add_argument(
        "--base-url",
        default=DUOYUANX_BASE_URL,
        help=f"DuoyuanX base URL; a trailing /v1 is stripped (default: {DUOYUANX_BASE_URL}).",
    )
    refresh_parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT}).",
    )
    refresh_parser.add_argument(
        "--proxy",
        default=None,
        help="Proxy URL, e.g. http://127.0.0.1:15236 (default: HTTP(S)_PROXY env vars, if set).",
    )
    refresh_parser.add_argument(
        "--no-proxy",
        action="store_true",
        help="Bypass all proxies, including HTTP(S)_PROXY environment variables.",
    )

    return parser.parse_args(argv)


def _print_snapshot(args: argparse.Namespace, snapshot: ModelPriceSnapshot) -> None:
    """Print the (possibly filtered) snapshot + compare check, shared by both
    subcommands. Filters affect display only — the full snapshot is cached."""
    rows = filter_rows(
        snapshot.rows,
        category=args.model_type_filter,
        model_substring=args.model_filter,
    )
    print(_render(rows, snapshot.source, args.format))
    if args.compare_models:
        wanted = [m.strip() for m in args.compare_models.split(",") if m.strip()]
        print()
        print(compare_models(snapshot.rows, wanted))


def main(argv: list[str] | None = None) -> int:
    _configure_streams()
    args = parse_args(argv)
    _load_dotenv()
    cache_dir = Path(args.cache_dir) if args.cache_dir else DEFAULT_CACHE_DIR

    if args.command == "list":
        try:
            snapshot = read_snapshot(cache_dir)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        _print_snapshot(args, snapshot)
        return 0

    # refresh
    try:
        print(f"Refreshing model prices for {PROVIDER}...")
        snapshot = fetch_duoyuanx(
            timeout=args.timeout,
            base_url=args.base_url,
            api_key=_resolve_api_key(args),
            proxy=args.proxy,
            no_proxy=args.no_proxy,
        )
    except (urllib.error.URLError, ValueError, OSError) as exc:
        print(f"Error refreshing {PROVIDER}: {exc}", file=sys.stderr)
        return 1
    _print_snapshot(args, snapshot)
    if args.dry_run:
        print("\nDry run: cache files were not written.")
    elif not snapshot.rows:
        print(
            "\nWarning: fetched an empty model list; kept the existing cache. "
            "Delete the cache file manually if you really want it emptied.",
            file=sys.stderr,
        )
    else:
        json_path, md_path = write_snapshot(snapshot, cache_dir)
        print(f"\nWrote JSON: {json_path}")
        print(f"Wrote Markdown: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
