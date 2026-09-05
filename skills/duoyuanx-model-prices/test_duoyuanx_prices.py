#!/usr/bin/env python3
"""Self-contained regression tests for duoyuanx_prices.py (stdlib unittest).

Run from anywhere:
    python3 skills/duoyuanx-model-prices/test_duoyuanx_prices.py

Covers the fixes from the 2026-09-05 adversarial review: cp1252-safe output,
empty-fetch cache guard, sort tie-break parity with taa, provider key in
cached rows, /v1 base-URL tolerance, and dotenv export/comment parsing.
"""
from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duoyuanx_prices as dp  # noqa: E402


FIXTURE_PRICING = {
    "data": [
        {
            "model_name": "gpt-image-2-all",
            "model_type": "image",
            "quota_type": 1,
            "model_price": "0.08",
            "vendor_id": 7,
        },
        {
            "model_name": "doubao-seedance-1-5-pro_480p",
            "model_type": "video",
            "quota_type": 1,
            "model_price": "0.10",
        },
        {
            "model_name": "claude-sonnet-4",
            "model_type": "text",
            "quota_type": 0,
            "model_ratio": "37.5",
            "completion_ratio": "5",
            "cache_ratio": "0.1",
        },
    ]
}

# Two chat models with identical prices but different orgs — exercises the
# org tie-break that once drifted from taa's sort.
TIE_BREAK_PRICING = {
    "data": [
        {
            "model_name": "model-b",
            "model_type": "text",
            "quota_type": 0,
            "model_ratio": "1",
            "completion_ratio": "2",
            "owner_by": "vendor-zzz",
        },
        {
            "model_name": "model-a",
            "model_type": "text",
            "quota_type": 0,
            "model_ratio": "1",
            "completion_ratio": "2",
            "owner_by": "vendor-aaa",
        },
    ]
}


def _normalize(payload):
    return dp.normalize_duoyuanx_payload(payload, source="fixture")


class NormalizeTests(unittest.TestCase):
    # taa fixture semantics (minus the constant provider field on the row)
    def test_normalize_merges_models_metadata(self):
        rows = dp.normalize_duoyuanx_payload(
            FIXTURE_PRICING,
            models_payload={
                "data": [
                    {
                        "id": "gpt-image-2-all",
                        "owned_by": "duoyuanx",
                        "supported_endpoint_types": ["image-generation"],
                    }
                ]
            },
            source="fixture",
        )
        image = next(r for r in rows if r.model_id == "gpt-image-2-all")
        video = next(r for r in rows if r.model_id == "doubao-seedance-1-5-pro_480p")
        chat = next(r for r in rows if r.model_id == "claude-sonnet-4")
        self.assertEqual(image.category, "image")
        self.assertEqual(image.input_price, "0.08")
        self.assertEqual(image.endpoint_types, ("image-generation",))
        self.assertTrue(image.available)
        self.assertEqual(image.extra["vendor_id"], 7)
        self.assertEqual(video.category, "video")
        self.assertEqual(video.pricing_unit, "per video")
        self.assertEqual(video.input_price, "0.1")
        self.assertEqual(chat.pricing_unit, "token ratio")
        self.assertEqual(chat.input_price, "37.5")
        self.assertEqual(chat.output_price, "5")
        self.assertEqual(chat.cache_hit, "0.1")

    def test_quota_type_2_is_per_second_not_per_request(self):
        # DuoyuanX's frontend maps quota_type 0/1/2 to 按量/按次/按秒计费.
        # MiniMax-H3 & kling-3.0-omni style rows: quota_type=2, model_price = $/sec.
        rows = dp.normalize_duoyuanx_payload(
            {
                "data": [
                    {
                        "model_name": "MiniMax-H3",
                        "model_type": "video",
                        "quota_type": 2,
                        "model_price": 0.5,
                        "description": "按秒！！！",
                    },
                    {
                        "model_name": "grok-1.5-video-10s",
                        "model_type": "video",
                        "quota_type": 1,
                        "model_price": 0.6,
                    },
                ]
            },
            source="fixture",
        )
        per_second = next(r for r in rows if r.model_id == "MiniMax-H3")
        per_request = next(r for r in rows if r.model_id == "grok-1.5-video-10s")
        self.assertEqual(per_second.pricing_unit, "per second")
        self.assertEqual(per_second.input_price, "0.5")
        self.assertEqual(per_request.pricing_unit, "per video")
        # markdown rendering uses the per-second label
        md = dp.render_markdown([per_second], "fixture")
        # currency-neutral: no $ prefix on per-second prices (q2 currency is
        # ambiguous — CNY per wan3.0's description, USD per the site default)
        self.assertIn("按秒计费: 模型价格 0.5 / 秒", md)
        self.assertIn("按次计费", dp.render_markdown([per_request], "fixture"))

    def test_cache_roundtrip_restores_per_second_unit(self):
        # Legacy caches written by pre-fix code lumped quota_type 2 into
        # "per video" (video rows) / "per request" — the read-back must
        # recover "per second" from extra.quota_type.
        row = dp.normalize_duoyuanx_payload(
            {
                "data": [
                    {
                        "model_name": "MiniMax-H3",
                        "model_type": "video",
                        "quota_type": 2,
                        "model_price": 0.5,
                    }
                ]
            },
            source="fixture",
        )[0]
        for legacy_unit in ("per video", "per request", "1M tokens"):
            legacy = dp.model_price_to_dict(row)
            legacy["pricing_unit"] = legacy_unit
            restored = dp.model_price_from_dict(legacy)
            self.assertEqual(restored.pricing_unit, "per second", legacy_unit)

    def test_quota_type_1_with_stray_cache_ratio_stays_per_request(self):
        # Live shape: grok-4.5 — quota_type=1, model_price=$0.01, cache_ratio=0.25.
        # quota_type is authoritative; the stray ratio must neither flip the
        # unit to token pricing nor leak into the cache-hit field.
        rows = dp.normalize_duoyuanx_payload(
            {
                "data": [
                    {
                        "model_name": "grok-4.5",
                        "model_type": "text",
                        "quota_type": 1,
                        "model_price": 0.01,
                        "model_ratio": 0,
                        "completion_ratio": 0,
                        "cache_ratio": 0.25,
                    }
                ]
            },
            source="fixture",
        )
        row = rows[0]
        self.assertEqual(row.pricing_unit, "per request")
        self.assertEqual(row.input_price, "0.01")
        self.assertEqual(row.cache_hit, "N/A")

    def test_missing_quota_type_falls_back_to_ratio_sniffing(self):
        # No enum -> ratio sniffing still classifies (back-compat for payloads
        # that omit quota_type).
        rows = dp.normalize_duoyuanx_payload(
            {
                "data": [
                    {
                        "model_name": "mystery",
                        "model_type": "text",
                        "model_ratio": 2,
                        "completion_ratio": 6,
                        "cache_ratio": 0.1,
                    }
                ]
            },
            source="fixture",
        )
        self.assertEqual(rows[0].pricing_unit, "token ratio")
        self.assertEqual(rows[0].input_price, "2")
        self.assertEqual(rows[0].output_price, "6")

    def test_normalize_keeps_modalities_out_of_price_fields(self):
        rows = dp.normalize_duoyuanx_payload(
            {
                "data": [
                    {
                        "model_name": "gemini-2.5-flash-image",
                        "model_type": "image",
                        "input_modalities": ["text", "image"],
                        "output_modalities": ["image"],
                    }
                ]
            },
            source="fixture",
        )
        row = rows[0]
        self.assertEqual(row.input_price, "N/A")
        self.assertEqual(row.output_price, "N/A")
        self.assertEqual(row.input_modalities, ("text", "image"))
        self.assertEqual(row.output_modalities, ("image",))

    def test_sort_tie_break_uses_org_before_model_id(self):
        rows = _normalize(TIE_BREAK_PRICING)
        self.assertEqual([r.model_id for r in rows], ["model-a", "model-b"])


class CacheShapeTests(unittest.TestCase):
    def test_cached_rows_carry_provider_key(self):
        row = _normalize(FIXTURE_PRICING)[0]
        data = dp.model_price_to_dict(row)
        self.assertEqual(data["provider"], "duoyuanx")
        # and the round-trip reader still works
        restored = dp.model_price_from_dict(data)
        self.assertEqual(restored.model_id, row.model_id)
        self.assertEqual(restored.pricing_unit, row.pricing_unit)


class EmptyFetchGuardTests(unittest.TestCase):
    def test_refresh_empty_snapshot_keeps_existing_cache(self):
        empty = dp.ModelPriceSnapshot(
            provider="duoyuanx", fetched_at="now", source="x", rows=[]
        )
        good = dp.ModelPriceSnapshot(
            provider="duoyuanx",
            fetched_at="now",
            source="x",
            rows=_normalize(FIXTURE_PRICING),
        )
        with tempfile.TemporaryDirectory() as tmp:
            dp.write_snapshot(good, tmp)
            before = dp.read_snapshot(tmp)
            orig = dp.fetch_duoyuanx
            dp.fetch_duoyuanx = lambda **kw: empty
            try:
                buf_out, buf_err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                    rc = dp.main(["refresh", "--cache-dir", tmp])
            finally:
                dp.fetch_duoyuanx = orig
            self.assertEqual(rc, 0)
            self.assertIn("kept the existing cache", buf_err.getvalue())
            after = dp.read_snapshot(tmp)
            self.assertEqual(len(after.rows), len(before.rows))

    def test_refresh_good_snapshot_still_writes(self):
        good = dp.ModelPriceSnapshot(
            provider="duoyuanx",
            fetched_at="now",
            source="x",
            rows=_normalize(FIXTURE_PRICING),
        )
        with tempfile.TemporaryDirectory() as tmp:
            orig = dp.fetch_duoyuanx
            dp.fetch_duoyuanx = lambda **kw: good
            try:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = dp.main(["refresh", "--cache-dir", tmp])
            finally:
                dp.fetch_duoyuanx = orig
            self.assertEqual(rc, 0)
            self.assertIn("Wrote JSON", buf.getvalue())
            self.assertEqual(len(dp.read_snapshot(tmp).rows), 3)


class DotenvTests(unittest.TestCase):
    def _load(self, content):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, ".env").write_text(content, encoding="utf-8")
            key = "DUOYUANX_API_KEY"
            saved = os.environ.pop(key, None)
            try:
                orig_file = dp.__file__
                dp.__file__ = str(Path(tmp, "duoyuanx_prices.py"))
                dp._load_dotenv()
                return os.environ.get(key)
            finally:
                dp.__file__ = orig_file
                if saved is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = saved

    def test_plain_value_with_equals(self):
        self.assertEqual(self._load("DUOYUANX_API_KEY=sk-abc=def==\n"), "sk-abc=def==")

    def test_export_prefix_and_quotes(self):
        self.assertEqual(
            self._load('export DUOYUANX_API_KEY="sk-quoted"\n'), "sk-quoted"
        )

    def test_trailing_comment(self):
        self.assertEqual(
            self._load("DUOYUANX_API_KEY=sk-x # my key\n"), "sk-x"
        )

    def test_quoted_value_with_trailing_comment(self):
        self.assertEqual(
            self._load('export DUOYUANX_API_KEY="sk-q" # trailing\n'), "sk-q"
        )

    def test_single_quoted_value(self):
        self.assertEqual(
            self._load("export DUOYUANX_API_KEY='sk-single'\n"), "sk-single"
        )


class UrlTests(unittest.TestCase):
    def test_base_url_trailing_v1_stripped(self):
        # Exercise the real fetch path with a stubbed opener so the /v1 strip
        # in fetch_duoyuanx is covered, not just the URL helper.
        import urllib.request

        calls = []

        def fake_open(request, timeout=None):
            calls.append(request.full_url)
            return contextlib.nullcontext(_FakeResponse({"data": []}))

        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        opener.open = fake_open
        orig_build = dp._build_opener
        dp._build_opener = lambda proxy, no_proxy: opener
        try:
            snapshot = dp.fetch_duoyuanx(base_url="https://example.com/v1")
        finally:
            dp._build_opener = orig_build
        self.assertEqual(calls, ["https://example.com/api/pricing"])
        self.assertEqual(snapshot.rows, [])


class _FakeResponse:
    def __init__(self, payload):
        import json as _json

        self._data = _json.dumps(payload).encode("utf-8")

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class StreamEncodingTests(unittest.TestCase):
    def test_configure_streams_does_not_crash_on_cjk(self):
        # Simulate a cp1252 console: after reconfigure(errors="replace"),
        # printing pricing labels must not raise.
        buf = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
        try:
            buf.reconfigure(errors="replace")
            buf.write("按量计费: 免费\n")
            buf.flush()
        finally:
            buf.close()


if __name__ == "__main__":
    unittest.main()
