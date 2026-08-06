"""Page content enrichment for browser time sinks.

Fetches and analyzes the actual content of web pages the user visited heavily,
to answer: what was this page about, how do pages relate, and why did the user
spend time on them.

This is an OPTIONAL post-segmentation enrichment phase. It is retrospective
(no live tracking), network-bound (fetches pages at analysis time), and
privacy-preserving (content stays in output/page_cache/, never committed, only
excerpts in session records).

Auth-required pages (Huawei internal: CloudDevOps Wiki, CodeHub, W3, etc.)
return a login redirect when fetched without session cookies. These are detected
and skipped gracefully — the summarizer falls back to title-based inference.

Usage from run.py::

    from page_enricher import enrich_tasks
    tasks = enrich_tasks(tasks, events, output_dir, proxy=proxy)
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Iterator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Only enrich tasks with at least this much active time (seconds).
_MIN_ACTIVE_SECONDS = 1800  # 0.5h

# Only enrich the top N pages per task (by visit count).
_MAX_PAGES_PER_TASK = 5

# Cache TTL in days. Pages fetched more than this ago are re-fetched.
_CACHE_TTL_DAYS = 7

# Delay between fetches (seconds) — be polite, don't hammer servers.
_FETCH_DELAY_SECONDS = 1.0

# Fetch timeout (seconds).
_FETCH_TIMEOUT = 15

# Maximum text excerpt length (characters).
_TEXT_EXCERPT_MAX = 1000

# URLs matching these patterns are never fetched (login redirects, internal IPs,
# non-page resources).
_SKIP_PATTERNS = [
    re.compile(r"^https?://login\.huawei\.com", re.I),
    re.compile(r"^https?://login\.microsoftonline\.com", re.I),
    re.compile(r"^https?://\d+\.\d+\.\d+\.\d+", re.I),  # internal IPs
    re.compile(r"^https?://localhost", re.I),
    re.compile(r"^https?://127\.", re.I),
    re.compile(r"\.(pdf|zip|rar|tar\.gz|exe|msi|dmg|deb|rpm)$", re.I),
    re.compile(r"^javascript:", re.I),
    re.compile(r"^mailto:", re.I),
    re.compile(r"^data:", re.I),
]

# Huawei internal domains that require SSO — we can't fetch these without
# the user's session cookies. Skip them and note in the report.
_AUTH_REQUIRED_DOMAINS = {
    "clouddevops.huawei.com",
    "codehub-g.huawei.com",
    "codehub-y.huawei.com",
    "w3.huawei.com",
    "agent.huawei.com",
    "agentcenter.huawei.com",
    "pandora.ai.huawei.com",
    "3ms.huawei.com",
    "e3.huawei.com",
    "welink.huawei.com",
    "onebox.huawei.com",
    "cloudscope.ulanqab.huawei.com",
    "jiaxian.huawei.com",
}

# Entity patterns for relationship detection.
_US_TICKET_RE = re.compile(r"US\d{10,}", re.I)
_MR_NUMBER_RE = re.compile(r"[#!](\d{2,})", re.I)
_PROJECT_RE = re.compile(r"([A-Z][a-z]+[A-Z][a-z]+(?:Service|API|Tool|Engine|Platform))", re.I)
_WIKI_ID_RE = re.compile(r"WIKI\d{8,}", re.I)


# ---------------------------------------------------------------------------
# Page selection
# ---------------------------------------------------------------------------

def select_pages_to_enrich(tasks: list[dict], events: list[dict]) -> dict[str, list[dict]]:
    """Select which pages to fetch for which tasks.

    Returns a mapping: task_id → list of {url, title, visit_count} for the top
    pages that are worth enriching.

    Only tasks with active_seconds >= _MIN_ACTIVE_SECONDS are considered.
    Only the top _MAX_PAGES_PER_TASK pages by visit count are selected.
    Pages matching _SKIP_PATTERNS or _AUTH_REQUIRED_DOMAINS are excluded.
    """
    from collections import Counter

    # Build a timeline index for finding events per task.
    task_pages: dict[str, Counter] = {}
    task_titles: dict[str, dict[str, str]] = {}  # task_id → {url: title}

    # Index events by timestamp for efficient lookup.
    ordered_events = sorted(
        (e for e in events if isinstance(e.get("timestamp"), (int, float))
         and e.get("kind") == "visit"),
        key=lambda e: e["timestamp"],
    )
    event_timestamps = [e["timestamp"] for e in ordered_events]

    from bisect import bisect_left, bisect_right

    for task in tasks:
        task_id = task.get("id") or task.get("session_id") or ""
        if not task_id:
            continue
        # Only enrich browser tasks — other source kinds don't have visit events.
        if task.get("source_kind") != "browser":
            continue
        active_s = task.get("active_seconds") or 0
        if active_s < _MIN_ACTIVE_SECONDS:
            continue

        start = task.get("start", 0)
        end = task.get("end", 0)

        lo = bisect_left(event_timestamps, start)
        hi = bisect_right(event_timestamps, end)

        page_counts: Counter = Counter()
        page_title_map: dict[str, str] = {}

        for ev in ordered_events[lo:hi]:
            ti = ev.get("tool_input") or {}
            url = (ti.get("url") or "").strip()
            title = (ti.get("title") or ev.get("text") or "").strip()
            if not url:
                continue
            page_counts[url] += 1
            if title and url not in page_title_map:
                page_title_map[url] = title

        if page_counts:
            task_pages[task_id] = page_counts
            task_titles[task_id] = page_title_map

    result: dict[str, list[dict]] = {}
    for task_id, counts in task_pages.items():
        titles = task_titles.get(task_id, {})
        top_urls = counts.most_common(_MAX_PAGES_PER_TASK)
        pages = []
        for url, visit_count in top_urls:
            if _should_skip_url(url):
                continue
            pages.append({
                "url": url,
                "title": titles.get(url, ""),
                "visit_count": visit_count,
            })
        if pages:
            result[task_id] = pages

    return result


def _should_skip_url(url: str) -> bool:
    """True if this URL should not be fetched."""
    for pattern in _SKIP_PATTERNS:
        if pattern.search(url):
            return True
    parsed = urllib.parse.urlparse(url)
    domain = parsed.hostname or ""
    # Skip auth-required Huawei internal domains.
    if domain in _AUTH_REQUIRED_DOMAINS or any(domain.endswith("." + d) for d in _AUTH_REQUIRED_DOMAINS):
        return True
    return False


def is_auth_required_domain(url: str) -> bool:
    """True if this URL is on a Huawei internal domain requiring SSO."""
    parsed = urllib.parse.urlparse(url)
    domain = parsed.hostname or ""
    return (domain in _AUTH_REQUIRED_DOMAINS
            or any(domain.endswith("." + d) for d in _AUTH_REQUIRED_DOMAINS))


# ---------------------------------------------------------------------------
# Page fetching + content extraction
# ---------------------------------------------------------------------------

class _TextExtractor(HTMLParser):
    """Minimal HTML-to-text extractor. Collects visible text and headings."""

    def __init__(self):
        super().__init__()
        self._skip_depth = 0  # inside script/style/noscript
        self._heading_depth = 0  # inside h1-h6
        self._text_parts: list[str] = []
        self._headings: list[str] = []
        self._links: list[tuple[str, str]] = []  # (text, href)
        self._current_link_href: str | None = None
        self._current_link_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg", "form", "nav", "footer"):
            self._skip_depth += 1
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading_depth += 1
        if tag == "a":
            href = None
            for k, v in attrs:
                if k == "href":
                    href = v
                    break
            self._current_link_href = href

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg", "form", "nav", "footer"):
            if self._skip_depth > 0:
                self._skip_depth -= 1
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self._heading_depth > 0:
                self._heading_depth -= 1
        if tag == "a" and self._current_link_href is not None:
            link_text = " ".join(self._current_link_text).strip()
            if link_text and self._current_link_href:
                self._links.append((link_text[:100], self._current_link_href[:200]))
            self._current_link_href = None
            self._current_link_text = []

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        text = data.strip()
        if not text:
            return
        self._text_parts.append(text)
        if self._heading_depth > 0:
            self._heading_text_parts = getattr(self, "_heading_text_parts", [])
            self._heading_text_parts.append(text)
        if self._current_link_href is not None:
            self._current_link_text.append(text)

    def handle_startendtag(self, tag, attrs):
        # self-closing tags like <br/>
        pass

    def get_text(self) -> str:
        return " ".join(self._text_parts)

    def get_headings(self) -> list[str]:
        # Re-parse for headings — simpler approach: collect h1-h6 text
        return self._headings

    def get_links(self) -> list[tuple[str, str]]:
        return self._links[:20]  # cap at 20 links


def _extract_heading_texts(html_source: str) -> list[str]:
    """Extract h1-h6 text from HTML using regex (simpler than parser tracking)."""
    headings = []
    for match in re.finditer(
        r"<(h[1-6])[^>]*>(.*?)</\1>", html_source, re.I | re.S
    ):
        text = re.sub(r"<[^>]+>", " ", match.group(2))
        text = html.unescape(text).strip()
        if text and len(text) <= 200:
            headings.append(text)
    return headings[:10]  # cap at 10


def _is_login_redirect(html_source: str, final_url: str, original_url: str) -> bool:
    """Detect if the fetched page is a login/SSO redirect rather than content."""
    # URL changed to a login domain
    if "login" in final_url.lower():
        return True
    # HTML contains login form indicators
    lower = html_source[:2000].lower()
    if "please sign in" in lower or "please log in" in lower:
        return True
    if '<form' in lower and ('password' in lower or 'passwd' in lower) and 'login' in lower:
        return True
    # SSO redirect pages
    if "samlrequest" in lower or "saml response" in lower:
        return True
    # Very short HTML with redirect meta tag
    if len(html_source) < 500 and "redirect" in lower:
        return True
    return False


def fetch_page_content(url: str, proxy: str | None = None,
                       timeout: int = _FETCH_TIMEOUT) -> dict:
    """Fetch a URL and extract a content summary.

    Returns a dict with:
        url, fetched_at (epoch), status, title, text_excerpt, headings, links

    status is one of: "ok", "login_redirect", "fetch_error", "not_html"
    """
    result = {
        "url": url,
        "fetched_at": time.time(),
        "status": "fetch_error",
        "title": "",
        "text_excerpt": "",
        "headings": [],
        "links": [],
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; huawei-auto-pal/1.0; +retrospective-analysis)",
        }
        req = urllib.request.Request(url, headers=headers)

        if proxy:
            proxy_handler = urllib.request.ProxyHandler({
                "http": proxy,
                "https": proxy,
            })
            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener()

        with opener.open(req, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type not in ("text/html", "application/xhtml+xml"):
                result["status"] = "not_html"
                return result
            charset = response.headers.get_content_charset() or "utf-8"
            data = response.read()
            final_url = str(response.geturl())

        html_source = data.decode(charset, errors="replace")

        # Check for login redirect
        if _is_login_redirect(html_source, final_url, url):
            result["status"] = "login_redirect"
            return result

        # Extract title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_source, re.I | re.S)
        if title_match:
            result["title"] = html.unescape(title_match.group(1).strip())[:200]

        # Strip boilerplate
        clean = re.sub(r"(?is)<(script|style|noscript|canvas|iframe|form|nav|footer)\b.*?</\1>", " ", html_source)
        clean = re.sub(r"(?is)<!--.*?-->", " ", clean)

        # Extract text
        extractor = _TextExtractor()
        extractor.feed(clean)
        text = extractor.get_text()
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()
        result["text_excerpt"] = text[:_TEXT_EXCERPT_MAX]

        # Extract headings
        result["headings"] = _extract_heading_texts(clean)

        # Extract links
        result["links"] = [{"text": t, "href": h} for t, h in extractor.get_links()]

        result["status"] = "ok"
        return result

    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as e:
        result["status"] = "fetch_error"
        result["text_excerpt"] = str(e)[:200]
        return result


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------

def _cache_path(url: str, cache_dir: str) -> str:
    """Generate a cache file path for a URL."""
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return os.path.join(cache_dir, f"{url_hash}.json")


def _load_cache(url: str, cache_dir: str) -> dict | None:
    """Load a cached page result. Returns None if not cached or expired."""
    path = _cache_path(url, cache_dir)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    # Check TTL
    fetched_at = data.get("fetched_at", 0)
    age_days = (time.time() - fetched_at) / 86400
    if age_days > _CACHE_TTL_DAYS:
        return None
    return data


def _save_cache(url: str, data: dict, cache_dir: str) -> None:
    """Save a page result to cache."""
    os.makedirs(cache_dir, exist_ok=True)
    path = _cache_path(url, cache_dir)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass  # cache write failure is non-fatal


# ---------------------------------------------------------------------------
# Entity extraction + relationship detection
# ---------------------------------------------------------------------------

def extract_entities(text: str) -> dict[str, list[str]]:
    """Extract entities from text (page title + content).

    Returns a dict with keys: us_tickets, mr_numbers, wiki_ids, projects.
    """
    us_tickets = sorted(set(m.group(0) for m in _US_TICKET_RE.finditer(text)))
    mr_numbers = sorted(set(m.group(1) for m in _MR_NUMBER_RE.finditer(text) if m.group(1).isdigit()))
    wiki_ids = sorted(set(m.group(0) for m in _WIKI_ID_RE.finditer(text)))
    projects = sorted(set(m.group(1) for m in _PROJECT_RE.finditer(text)))

    return {
        "us_tickets": us_tickets,
        "mr_numbers": mr_numbers,
        "wiki_ids": wiki_ids,
        "projects": projects,
    }


def detect_relationships(pages: list[dict]) -> list[dict]:
    """Detect relationships between pages based on shared entities.

    Each page is a dict with at least: url, title, text_excerpt (or enriched data).

    Returns a list of relationship clusters:
        [{"entities": {"us_tickets": ["US2026071700209"]}, "pages": [url1, url2]}]
    """
    # Extract entities per page
    page_entities: list[tuple[str, dict]] = []
    for page in pages:
        url = page.get("url", "")
        title = page.get("title", "")
        text = page.get("text_excerpt", "")
        combined = f"{title} {text}"
        entities = extract_entities(combined)
        if any(entities.values()):
            page_entities.append((url, entities))

    # Find shared entities
    clusters: dict[str, set[str]] = {}  # entity_key → set of urls

    for url, entities in page_entities:
        for entity_type, values in entities.items():
            for value in values:
                key = f"{entity_type}:{value}"
                clusters.setdefault(key, set()).add(url)

    # Only keep clusters with 2+ pages
    relationships = []
    for key, urls in clusters.items():
        if len(urls) >= 2:
            entity_type, value = key.split(":", 1)
            relationships.append({
                "entity_type": entity_type,
                "entity_value": value,
                "pages": sorted(urls),
            })

    return relationships


# ---------------------------------------------------------------------------
# Top-level enrichment
# ---------------------------------------------------------------------------

def enrich_tasks(tasks: list[dict], events: list[dict],
                 output_dir: str, proxy: str | None = None,
                 dry_run: bool = False) -> dict[str, dict]:
    """Enrich browser tasks with page content.

    For each task that is a genuine time sink (active_seconds >= threshold),
    fetches the top visited pages and extracts content summaries.

    Args:
        tasks: List of task dicts from segmentation.
        events: List of all events.
        output_dir: Path to output/ directory (for cache).
        proxy: Optional proxy URL for external pages.
        dry_run: If True, select pages but don't fetch.

    Returns:
        Mapping: task_id → {
            "pages": [{url, title, visit_count, status, text_excerpt, ...}],
            "relationships": [{entity_type, entity_value, pages}],
            "auth_skipped": [url, ...],  # pages skipped because they need auth
        }
    """
    cache_dir = os.path.join(output_dir, "page_cache")
    pages_by_task = select_pages_to_enrich(tasks, events)

    if not pages_by_task:
        return {}

    # Collect all unique URLs to fetch (across tasks).
    all_urls: set[str] = set()
    for pages in pages_by_task.values():
        for p in pages:
            all_urls.add(p["url"])

    # Fetch each URL once (with caching), then distribute results to tasks.
    fetched: dict[str, dict] = {}
    auth_skipped: set[str] = set()

    for url in sorted(all_urls):
        # Check cache first
        cached = _load_cache(url, cache_dir)
        if cached is not None:
            fetched[url] = cached
            continue

        if is_auth_required_domain(url):
            auth_skipped.add(url)
            result = {
                "url": url,
                "fetched_at": time.time(),
                "status": "auth_required",
                "title": "",
                "text_excerpt": "",
                "headings": [],
                "links": [],
            }
            fetched[url] = result
            _save_cache(url, result, cache_dir)
            continue

        if dry_run:
            result = {
                "url": url,
                "fetched_at": time.time(),
                "status": "dry_run",
                "title": "",
                "text_excerpt": "",
                "headings": [],
                "links": [],
            }
        else:
            result = fetch_page_content(url, proxy=proxy)
            _save_cache(url, result, cache_dir)
            time.sleep(_FETCH_DELAY_SECONDS)  # rate limit

        fetched[url] = result

    # Build enrichment result per task.
    enrichment: dict[str, dict] = {}
    for task_id, pages in pages_by_task.items():
        task_pages = []
        task_auth_skipped = []
        for p in pages:
            url = p["url"]
            page_data = fetched.get(url, {})
            task_pages.append({
                "url": url,
                "title": p["title"] or page_data.get("title", ""),
                "visit_count": p["visit_count"],
                "status": page_data.get("status", "not_fetched"),
                "text_excerpt": page_data.get("text_excerpt", ""),
                "headings": page_data.get("headings", []),
            })
            if page_data.get("status") == "auth_required":
                task_auth_skipped.append(url)

        relationships = detect_relationships(task_pages)

        enrichment[task_id] = {
            "pages": task_pages,
            "relationships": relationships,
            "auth_skipped": task_auth_skipped,
        }

    return enrichment
