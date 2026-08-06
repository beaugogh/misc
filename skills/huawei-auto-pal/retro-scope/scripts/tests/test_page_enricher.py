"""Tests for page_enricher: page content extraction and relationship detection."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import page_enricher
from page_enricher import (
    select_pages_to_enrich,
    _should_skip_url,
    is_auth_required_domain,
    fetch_page_content,
    extract_entities,
    detect_relationships,
    enrich_tasks,
    _TextExtractor,
    _is_login_redirect,
    _cache_path,
    _load_cache,
    _save_cache,
)


def _make_visit_event(ts: float, url: str, title: str = "", visit_count: int = 1) -> dict:
    return {
        "timestamp": ts,
        "kind": "visit",
        "source": "chrome",
        "source_kind": "browser",
        "text": title,
        "tool_input": {"url": url, "title": title, "visit_count": visit_count},
    }


def _make_task(task_id: str, start: float, end: float, active_seconds: float = 3600) -> dict:
    return {
        "id": task_id,
        "source_kind": "browser",
        "start": start,
        "end": end,
        "active_seconds": active_seconds,
        "wall_clock_seconds": active_seconds,
    }


# ---------------------------------------------------------------------------
# Page selection
# ---------------------------------------------------------------------------

class TestSelectPagesToEnrich(unittest.TestCase):

    def test_selects_top_pages_for_time_sinks(self):
        """Tasks with enough active time get their top pages selected."""
        events = [
            _make_visit_event(1000, "https://example.com/a", "Page A", 3),
            _make_visit_event(1001, "https://example.com/a", "Page A", 3),
            _make_visit_event(1002, "https://example.com/a", "Page A", 3),
            _make_visit_event(1003, "https://example.com/b", "Page B", 1),
        ]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = select_pages_to_enrich(tasks, events)
        self.assertIn("t1", result)
        self.assertEqual(len(result["t1"]), 2)
        # Page A (3 visits) should be first
        self.assertEqual(result["t1"][0]["url"], "https://example.com/a")
        self.assertEqual(result["t1"][0]["visit_count"], 3)

    def test_skips_short_tasks(self):
        """Tasks under the active time threshold are not enriched."""
        events = [_make_visit_event(1000, "https://example.com/a", "A")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=60)]
        result = select_pages_to_enrich(tasks, events)
        self.assertNotIn("t1", result)

    def test_skips_auth_required_domains(self):
        """Huawei internal domains are skipped."""
        events = [
            _make_visit_event(1000, "https://codehub-g.huawei.com/repo", "CodeHub"),
            _make_visit_event(1001, "https://example.com/page", "External"),
        ]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = select_pages_to_enrich(tasks, events)
        self.assertIn("t1", result)
        urls = [p["url"] for p in result["t1"]]
        self.assertNotIn("https://codehub-g.huawei.com/repo", urls)
        self.assertIn("https://example.com/page", urls)

    def test_caps_at_max_pages(self):
        """Only top N pages per task are selected."""
        events = []
        for i in range(10):
            events.append(_make_visit_event(1000 + i, f"https://example.com/p{i}", f"Page {i}"))
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = select_pages_to_enrich(tasks, events)
        self.assertLessEqual(len(result["t1"]), 5)

    def test_no_browser_tasks(self):
        """Non-browser tasks are ignored."""
        events = [_make_visit_event(1000, "https://example.com/a", "A")]
        tasks = [{"id": "t1", "source_kind": "ai_session", "start": 1000, "end": 2000, "active_seconds": 3600}]
        result = select_pages_to_enrich(tasks, events)
        self.assertEqual(result, {})

    def test_no_visit_events(self):
        """Tasks with no visit events produce no pages."""
        events = [{"timestamp": 1000, "kind": "search", "text": "query", "tool_input": {}}]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = select_pages_to_enrich(tasks, events)
        self.assertEqual(result, {})


# ---------------------------------------------------------------------------
# URL filtering
# ---------------------------------------------------------------------------

class TestShouldSkipUrl(unittest.TestCase):

    def test_skips_login_urls(self):
        self.assertTrue(_should_skip_url("https://login.huawei.com/redirect"))
        self.assertTrue(_should_skip_url("https://login.microsoftonline.com/"))

    def test_skips_internal_ips(self):
        self.assertTrue(_should_skip_url("http://100.95.190.165:8520/ui"))
        self.assertTrue(_should_skip_url("http://127.0.0.1:8080"))

    def test_skips_non_page_resources(self):
        self.assertTrue(_should_skip_url("https://example.com/doc.pdf"))
        self.assertTrue(_should_skip_url("https://example.com/archive.zip"))

    def test_skips_auth_required_huawei_domains(self):
        self.assertTrue(_should_skip_url("https://codehub-g.huawei.com/repo"))
        self.assertTrue(_should_skip_url("https://clouddevops.huawei.com/wiki/1"))
        self.assertTrue(_should_skip_url("https://w3.huawei.com/next"))

    def test_allows_external_pages(self):
        self.assertFalse(_should_skip_url("https://google.com/search?q=python"))
        self.assertFalse(_should_skip_url("https://blog.example.com/article"))

    def test_allows_subdomain_of_huawei(self):
        # subdomain of a known internal domain should also be skipped
        self.assertTrue(_should_skip_url("https://sub.codehub-g.huawei.com/page"))


class TestIsAuthRequiredDomain(unittest.TestCase):

    def test_huawei_internal(self):
        self.assertTrue(is_auth_required_domain("https://codehub-g.huawei.com/repo"))
        self.assertTrue(is_auth_required_domain("https://w3.huawei.com/next"))

    def test_external(self):
        self.assertFalse(is_auth_required_domain("https://google.com/search"))
        self.assertFalse(is_auth_required_domain("https://example.com"))


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------

class TestTextExtractor(unittest.TestCase):

    def test_extracts_visible_text(self):
        html = "<html><body><h1>Title</h1><p>Hello world</p></body></html>"
        ext = _TextExtractor()
        ext.feed(html)
        text = ext.get_text()
        self.assertIn("Title", text)
        self.assertIn("Hello world", text)

    def test_skips_script_style(self):
        html = "<html><body><p>visible</p><script>hidden()</script><style>.x{}</style></body></html>"
        ext = _TextExtractor()
        ext.feed(html)
        text = ext.get_text()
        self.assertIn("visible", text)
        self.assertNotIn("hidden", text)
        self.assertNotIn(".x", text)

    def test_extracts_links(self):
        html = '<html><body><a href="/page1">Link 1</a><a href="https://example.com">Link 2</a></body></html>'
        ext = _TextExtractor()
        ext.feed(html)
        links = ext.get_links()
        self.assertEqual(len(links), 2)


class TestIsLoginRedirect(unittest.TestCase):

    def test_login_in_url(self):
        self.assertTrue(_is_login_redirect("some html", "https://login.huawei.com/auth", "https://app.huawei.com"))

    def test_login_form(self):
        html = '<html><body><form action="/login"><input type="password" name="passwd"></form>Please sign in</body></html>'
        self.assertTrue(_is_login_redirect(html, "https://app.huawei.com", "https://app.huawei.com"))

    def test_normal_page(self):
        html = "<html><body><h1>Welcome to my page</h1><p>Content here</p></body></html>"
        self.assertFalse(_is_login_redirect(html, "https://example.com", "https://example.com"))

    def test_saml_redirect(self):
        html = "<html><body>SAMLRequest=...</body></html>"

    def test_login_in_path_not_false_positive(self):
        """URLs with 'login' in the path but not a login domain should NOT be flagged."""
        html = "<html><body><h1>Login Best Practices</h1><p>Guide for secure logins</p></body></html>"
        self.assertFalse(_is_login_redirect(html, "https://blog.example.com/login-tips", "https://blog.example.com/login-tips"))
        self.assertFalse(_is_login_redirect(html, "https://example.com/docs/user-login-guide", "https://example.com/docs/user-login-guide"))


class TestFetchPageContent(unittest.TestCase):

    @patch("page_enricher.urllib.request.build_opener")
    def test_successful_fetch(self, mock_build):
        mock_resp = MagicMock()
        mock_resp.headers.get_content_type.return_value = "text/html"
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.read.return_value = b"<html><head><title>Test Page</title></head><body><h1>Hello</h1><p>Content</p></body></html>"
        mock_resp.geturl.return_value = "https://example.com"
        mock_opener = MagicMock()
        mock_opener.open.return_value.__enter__.return_value = mock_resp
        mock_build.return_value = mock_opener

        result = fetch_page_content("https://example.com")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["title"], "Test Page")
        self.assertIn("Hello", result["text_excerpt"])
        self.assertIn("Content", result["text_excerpt"])

    @patch("page_enricher.urllib.request.build_opener")
    def test_login_redirect_detected(self, mock_build):
        mock_resp = MagicMock()
        mock_resp.headers.get_content_type.return_value = "text/html"
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.read.return_value = b"<html><body>Please sign in<form><input type='password'></form></body></html>"
        mock_resp.geturl.return_value = "https://login.huawei.com/auth"
        mock_opener = MagicMock()
        mock_opener.open.return_value.__enter__.return_value = mock_resp
        mock_build.return_value = mock_opener

        result = fetch_page_content("https://app.huawei.com")
        self.assertEqual(result["status"], "login_redirect")

    @patch("page_enricher.urllib.request.build_opener")
    def test_non_html_content(self, mock_build):
        mock_resp = MagicMock()
        mock_resp.headers.get_content_type.return_value = "application/pdf"
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.read.return_value = b"PDF content"
        mock_resp.geturl.return_value = "https://example.com/doc.pdf"
        mock_opener = MagicMock()
        mock_opener.open.return_value.__enter__.return_value = mock_resp
        mock_build.return_value = mock_opener

        result = fetch_page_content("https://example.com/doc.pdf")
        self.assertEqual(result["status"], "not_html")

    @patch("page_enricher.urllib.request.build_opener")
    def test_fetch_error_on_exception(self, mock_build):
        import urllib.error
        mock_build.side_effect = urllib.error.URLError("timeout")

        result = fetch_page_content("https://example.com")
        self.assertEqual(result["status"], "fetch_error")

    @patch("page_enricher.urllib.request.build_opener")
    def test_uses_proxy_when_provided(self, mock_build):
        mock_resp = MagicMock()
        mock_resp.headers.get_content_type.return_value = "text/html"
        mock_resp.headers.get_content_charset.return_value = "utf-8"
        mock_resp.read.return_value = b"<html><body><p>Hi</p></body></html>"
        mock_resp.geturl.return_value = "https://example.com"
        mock_opener = MagicMock()
        mock_opener.open.return_value.__enter__.return_value = mock_resp
        mock_build.return_value = mock_opener

        fetch_page_content("https://example.com", proxy="http://proxy:8080")
        # Verify ProxyHandler was used (build_opener was called, not just urlopen)
        mock_build.assert_called_once()


# ---------------------------------------------------------------------------
# Entity extraction + relationship detection
# ---------------------------------------------------------------------------

class TestExtractEntities(unittest.TestCase):

    def test_us_tickets(self):
        entities = extract_entities("Working on US2026071700209 and US2026071700210")
        self.assertEqual(entities["us_tickets"], ["US2026071700209", "US2026071700210"])

    def test_mr_numbers(self):
        entities = extract_entities("See MR #89 and #4457 for details")
        self.assertIn("89", entities["mr_numbers"])
        self.assertIn("4457", entities["mr_numbers"])

    def test_wiki_ids(self):
        entities = extract_entities("Wiki WIKI2026080500102 and WIKI2026041700179")
        self.assertEqual(len(entities["wiki_ids"]), 2)

    def test_projects(self):
        entities = extract_entities("The ComplianceAssessmentToolService needs an update")
        self.assertIn("ComplianceAssessmentToolService", entities["projects"])

    def test_no_entities(self):
        entities = extract_entities("Just some random text without entities")
        self.assertEqual(entities["us_tickets"], [])
        self.assertEqual(entities["mr_numbers"], [])

    def test_case_insensitive_us(self):
        entities = extract_entities("working on us2026071700209")
        self.assertEqual(len(entities["us_tickets"]), 1)


class TestDetectRelationships(unittest.TestCase):

    def test_shared_us_ticket(self):
        pages = [
            {"url": "https://example.com/a", "title": "Sprint page US2026071700209", "text_excerpt": ""},
            {"url": "https://example.com/b", "title": "MR for US2026071700209", "text_excerpt": ""},
            {"url": "https://example.com/c", "title": "Unrelated page", "text_excerpt": ""},
        ]
        rels = detect_relationships(pages)
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["entity_type"], "us_tickets")
        self.assertEqual(rels[0]["entity_value"], "US2026071700209")
        self.assertEqual(len(rels[0]["pages"]), 2)

    def test_no_relationships(self):
        pages = [
            {"url": "https://example.com/a", "title": "Page A", "text_excerpt": "about cats"},
            {"url": "https://example.com/b", "title": "Page B", "text_excerpt": "about dogs"},
        ]
        rels = detect_relationships(pages)
        self.assertEqual(rels, [])

    def test_multiple_shared_entities(self):
        pages = [
            {"url": "https://example.com/a", "title": "US2026071700209 #89", "text_excerpt": ""},
            {"url": "https://example.com/b", "title": "US2026071700209 #89", "text_excerpt": ""},
            {"url": "https://example.com/c", "title": "US2026071700210 #89", "text_excerpt": ""},
        ]
        rels = detect_relationships(pages)
        # Two entities shared: US2026071700209 (pages a,b) and #89 (pages a,b,c)
        entity_values = [r["entity_value"] for r in rels]
        self.assertIn("US2026071700209", entity_values)
        self.assertIn("89", entity_values)

    def test_uses_text_excerpt(self):
        """Relationships are detected from text content, not just titles."""
        pages = [
            {"url": "https://example.com/a", "title": "Page A", "text_excerpt": "Reference US2026071700209 for details"},
            {"url": "https://example.com/b", "title": "Page B", "text_excerpt": "See US2026071700209"},
        ]
        rels = detect_relationships(pages)
        self.assertEqual(len(rels), 1)


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------

class TestCaching(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_cache_path_deterministic(self):
        path1 = _cache_path("https://example.com/a", self.tmpdir)
        path2 = _cache_path("https://example.com/a", self.tmpdir)
        self.assertEqual(path1, path2)

    def test_cache_path_different_urls(self):
        path1 = _cache_path("https://example.com/a", self.tmpdir)
        path2 = _cache_path("https://example.com/b", self.tmpdir)
        self.assertNotEqual(path1, path2)

    def test_save_and_load_cache(self):
        data = {"url": "https://example.com", "status": "ok", "text_excerpt": "hello",
                "fetched_at": 999999999999.0}  # far future → never expires
        _save_cache("https://example.com", data, self.tmpdir)
        loaded = _load_cache("https://example.com", self.tmpdir)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["status"], "ok")
        self.assertEqual(loaded["text_excerpt"], "hello")

    def test_load_cache_expired(self):
        data = {"url": "https://example.com", "status": "ok", "text_excerpt": "old",
                "fetched_at": 0}  # epoch → expired
        _save_cache("https://example.com", data, self.tmpdir)
        loaded = _load_cache("https://example.com", self.tmpdir)
        self.assertIsNone(loaded)

    def test_load_cache_missing(self):
        loaded = _load_cache("https://nonexistent.com", self.tmpdir)
        self.assertIsNone(loaded)

    def test_save_cache_creates_dir(self):
        new_dir = os.path.join(self.tmpdir, "subdir", "cache")
        data = {"url": "https://example.com", "status": "ok", "fetched_at": 999999999999.0}
        _save_cache("https://example.com", data, new_dir)
        self.assertTrue(os.path.exists(new_dir))


# ---------------------------------------------------------------------------
# enrich_tasks integration
# ---------------------------------------------------------------------------

class TestEnrichTasks(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_dry_run_selects_but_doesnt_fetch(self):
        events = [_make_visit_event(1000, "https://example.com/a", "Page A")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=True)
        self.assertIn("t1", result)
        self.assertEqual(result["t1"]["pages"][0]["status"], "dry_run")

    def test_auth_required_pages_marked(self):
        events = [_make_visit_event(1000, "https://codehub-g.huawei.com/repo", "CodeHub")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=True)
        # Auth-required pages are filtered out by select_pages_to_enrich,
        # so no pages should be selected.
        self.assertNotIn("t1", result)

    def test_uses_cache(self):
        # First, cache a result.
        cache_data = {"url": "https://example.com/a", "status": "ok",
                      "text_excerpt": "cached content", "fetched_at": 999999999999.0,
                      "title": "Cached", "headings": [], "links": []}
        _save_cache("https://example.com/a", cache_data, os.path.join(self.tmpdir, "page_cache"))

        events = [_make_visit_event(1000, "https://example.com/a", "Page A")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=False)
        self.assertIn("t1", result)
        self.assertEqual(result["t1"]["pages"][0]["status"], "ok")
        self.assertEqual(result["t1"]["pages"][0]["text_excerpt"], "cached content")

    def test_empty_tasks(self):
        result = enrich_tasks([], [], self.tmpdir)
        self.assertEqual(result, {})

    def test_no_time_sink_tasks(self):
        events = [_make_visit_event(1000, "https://example.com/a", "A")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=60)]
        result = enrich_tasks(tasks, events, self.tmpdir)
        self.assertEqual(result, {})

    def test_relationships_detected_in_result(self):
        # Cache two pages that share a US ticket.
        for url, title in [
            ("https://example.com/a", "Sprint US2026071700209"),
            ("https://example.com/b", "MR US2026071700209"),
        ]:
            cache_data = {"url": url, "status": "ok", "text_excerpt": "",
                          "fetched_at": 999999999999.0, "title": title,
                          "headings": [], "links": []}
            _save_cache(url, cache_data, os.path.join(self.tmpdir, "page_cache"))

        events = [
            _make_visit_event(1000, "https://example.com/a", "Sprint US2026071700209"),
            _make_visit_event(1001, "https://example.com/b", "MR US2026071700209"),
        ]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=False)
        self.assertIn("t1", result)
        rels = result["t1"]["relationships"]
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["entity_value"], "US2026071700209")

    @patch("page_enricher.fetch_page_content")
    def test_fetches_non_cached_pages(self, mock_fetch):
        mock_fetch.return_value = {
            "url": "https://example.com/a", "fetched_at": 999999999999.0,
            "status": "ok", "title": "Fetched", "text_excerpt": "real content",
            "headings": ["H1"], "links": [],
        }
        events = [_make_visit_event(1000, "https://example.com/a", "Page A")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=False)
        self.assertIn("t1", result)
        self.assertEqual(result["t1"]["pages"][0]["status"], "ok")
        self.assertEqual(result["t1"]["pages"][0]["text_excerpt"], "real content")
        mock_fetch.assert_called_once()

    @patch("page_enricher.fetch_page_content")
    @patch("page_enricher.time.sleep")
    def test_rate_limited(self, mock_sleep, mock_fetch):
        mock_fetch.return_value = {
            "url": "", "fetched_at": 999999999999.0, "status": "ok",
            "title": "", "text_excerpt": "", "headings": [], "links": [],
        }
        events = [
            _make_visit_event(1000, "https://example.com/a", "A"),
            _make_visit_event(1001, "https://example.com/b", "B"),
        ]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        enrich_tasks(tasks, events, self.tmpdir, dry_run=False)
        # Should have slept between fetches.
        mock_sleep.assert_called()

    @patch("page_enricher.fetch_page_content")
    def test_fetch_error_handled_gracefully(self, mock_fetch):
        mock_fetch.return_value = {
            "url": "https://example.com/a", "fetched_at": 999999999999.0,
            "status": "fetch_error", "title": "", "text_excerpt": "timeout",
            "headings": [], "links": [],
        }
        events = [_make_visit_event(1000, "https://example.com/a", "Page A")]
        tasks = [_make_task("t1", 1000, 2000, active_seconds=3600)]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=False)
        self.assertIn("t1", result)
        self.assertEqual(result["t1"]["pages"][0]["status"], "fetch_error")

    def test_deduplicates_urls_across_tasks(self):
        """If two tasks share a URL, it's only fetched once."""
        cache_data = {"url": "https://example.com/a", "status": "ok",
                      "text_excerpt": "shared", "fetched_at": 999999999999.0,
                      "title": "Shared", "headings": [], "links": []}
        _save_cache("https://example.com/a", cache_data, os.path.join(self.tmpdir, "page_cache"))

        events = [
            _make_visit_event(1000, "https://example.com/a", "Shared"),
            _make_visit_event(2000, "https://example.com/a", "Shared"),
        ]
        tasks = [
            _make_task("t1", 1000, 1500, active_seconds=3600),
            _make_task("t2", 2000, 2500, active_seconds=3600),
        ]
        result = enrich_tasks(tasks, events, self.tmpdir, dry_run=False)
        # Both tasks should get the cached content.
        self.assertIn("t1", result)
        self.assertIn("t2", result)
        self.assertEqual(result["t1"]["pages"][0]["text_excerpt"], "shared")
        self.assertEqual(result["t2"]["pages"][0]["text_excerpt"], "shared")


if __name__ == "__main__":
    unittest.main()
