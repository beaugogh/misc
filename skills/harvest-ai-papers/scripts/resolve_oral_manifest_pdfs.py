#!/usr/bin/env python3
import argparse
import csv
import json
import re
import subprocess
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

from list_venue_papers import DEFAULT_YEAR, USER_AGENT, clean_text, configured_output_dir, fetch
from harvest_manifest import discover_paper_pdf, links_from_html


FIELDS = [
    "year",
    "data_year",
    "venue",
    "presentation_type",
    "paper_id",
    "title",
    "authors",
    "paper_page_url",
    "pdf_url",
    "source_url",
    "status",
    "notes",
]


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def normalize_title(value):
    value = value or ""
    value = re.sub(r"([A-Z]{2,})([a-z])", r"\1 \2", value)
    value = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)
    value = re.sub(r"(?<=[0-9])(?=[A-Za-z])", " ", value)
    value = re.sub(r"(?<=[A-Za-z])(?=[0-9])", " ", value)
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def significant_tokens(value):
    stop = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "via",
        "with",
    }
    return {token for token in normalize_title(value).split() if len(token) > 2 and token not in stop}


def significant_tokens_ordered(value):
    seen = set()
    ordered = []
    for token in normalize_title(value).split():
        if token in significant_tokens(value) and token not in seen:
            seen.add(token)
            ordered.append(token)
    return ordered


def title_match_score(query, candidate):
    query_norm = normalize_title(query)
    candidate_norm = normalize_title(candidate)
    if query_norm and query_norm == candidate_norm:
        return 1.0
    query_tokens = significant_tokens(query)
    candidate_tokens = significant_tokens(candidate)
    if not query_tokens or not candidate_tokens:
        return 0.0
    return len(query_tokens & candidate_tokens) / len(query_tokens)


def verified_pdf(url):
    if not url:
        return False
    try:
        completed = subprocess.run(
            [
                "curl",
                "-fsSL",
                "--http1.1",
                "--compressed",
                "-A",
                USER_AGENT,
                "-r",
                "0-1023",
                url,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=25,
        )
    except Exception:
        return False
    return completed.stdout.startswith(b"%PDF")


def arxiv_pdf_from_abs(url):
    match = re.search(r"arxiv\.org/(abs|pdf)/([^?#]+)", url)
    if not match:
        return ""
    arxiv_id = match.group(2)
    arxiv_id = arxiv_id.removesuffix(".pdf")
    return f"https://arxiv.org/pdf/{arxiv_id}"


def arxiv_queries(title):
    title = (title or "").strip()
    queries = []
    if ":" in title:
        prefix = title.split(":", 1)[0].strip()
        if prefix:
            queries.append(f'ti:"{prefix}"')
    queries.append(f'ti:"{title[:160]}"')
    tokens = significant_tokens_ordered(title)
    if len(tokens) >= 3:
        queries.append(" AND ".join(f"ti:{urllib.parse.quote(token)}" for token in tokens[:6]))
    seen = set()
    for query in queries:
        if query and query not in seen:
            seen.add(query)
            yield query


def fetch_fast(url, timeout=12):
    completed = subprocess.run(
        ["curl", "-fsSL", "--http1.1", "--compressed", "-A", USER_AGENT, url],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return completed.stdout.decode("utf-8", errors="replace")


def arxiv_title_query(title, max_queries=2, cache=None, arxiv_delay=3.0):
    cache_key = normalize_title(title)
    if cache is not None and cache_key in cache:
        cached = cache[cache_key]
        return cached.get("pdf_url", ""), cached.get("reason", "")
    best = ("", "", 0.0)
    for index, query in enumerate(arxiv_queries(title)):
        if index >= max_queries:
            break
        quoted_title = urllib.parse.quote(query, safe=":")
        url = f"https://export.arxiv.org/api/query?search_query={quoted_title}&start=0&max_results=5"
        candidate = best_arxiv_match(url, title)
        if candidate[2] > best[2]:
            best = candidate
        if best[2] >= 0.98:
            break
        if arxiv_delay:
            time.sleep(arxiv_delay)
    if best[2] >= 0.86:
        result = {
            "pdf_url": best[0],
            "reason": f"arXiv title match score={best[2]:.2f}: {best[1]}",
        }
    else:
        result = {"pdf_url": "", "reason": ""}
    if cache is not None:
        cache[cache_key] = result
    return result["pdf_url"], result["reason"]


def best_arxiv_match(url, title):
    try:
        root = ET.fromstring(fetch_fast(url))
    except Exception:
        return "", "", 0.0
    best = ("", "", 0.0)
    for entry in root.findall("atom:entry", ATOM_NS):
        candidate_title = "".join(entry.findtext("atom:title", default="", namespaces=ATOM_NS).split())
        candidate_title = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", candidate_title)
        score = title_match_score(title, candidate_title)
        pdf_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
                break
        if score > best[2] and pdf_url:
            best = (pdf_url, candidate_title, score)
    return best


def aaai_ojs_issue_urls(year):
    marker = f"AAAI-{str(year)[-2:]} Technical Tracks"
    urls = []
    for page in range(1, 20):
        archive_url = "https://ojs.aaai.org/index.php/AAAI/issue/archive" if page == 1 else f"https://ojs.aaai.org/index.php/AAAI/issue/archive/{page}"
        source = fetch(archive_url)
        before = len(urls)
        for href, text in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', source, flags=re.I | re.S):
            label = clean_text(re.sub(r"<[^>]+>", " ", text))
            if marker in label and href not in urls:
                urls.append(href)
        if len(urls) == before:
            break
    return urls


def parse_aaai_ojs_issue(issue_url):
    source = fetch(issue_url)
    articles = []
    for block in re.findall(r'<div class="obj_article_summary">(.*?)</div>\s*</li>', source, flags=re.I | re.S):
        title_match = re.search(r'<h3 class="title">\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.I | re.S)
        pdf_match = re.search(r'<a class="obj_galley_link pdf" href="([^"]+)"', block, flags=re.I)
        authors_match = re.search(r'<div class="authors">\s*(.*?)\s*</div>', block, flags=re.I | re.S)
        if not title_match or not pdf_match:
            continue
        articles.append(
            {
                "title": clean_text(re.sub(r"<[^>]+>", " ", title_match.group(2))),
                "paper_page_url": title_match.group(1),
                "pdf_url": pdf_match.group(1),
                "authors": clean_text(re.sub(r"<[^>]+>", " ", authors_match.group(1))) if authors_match else "",
                "issue_url": issue_url,
            }
        )
    return articles


def aaai_ojs_index(year, cache_path=None):
    if cache_path and cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    articles = []
    for issue_url in aaai_ojs_issue_urls(year):
        articles.extend(parse_aaai_ojs_issue(issue_url))
        time.sleep(0.2)
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(articles, indent=2, sort_keys=True), encoding="utf-8")
    return articles


def resolve_aaai_ojs(row, ojs_articles, verify=True):
    if row.get("venue") != "AAAI" or not row.get("title"):
        return None
    best = None
    best_score = 0.0
    for article in ojs_articles:
        score = title_match_score(row["title"], article["title"])
        if score > best_score:
            best = article
            best_score = score
    if best and best_score >= 0.86 and (not verify or verified_pdf(best["pdf_url"])):
        row["title"] = best["title"]
        row["authors"] = best.get("authors", "")
        row["paper_page_url"] = best["paper_page_url"]
        row["pdf_url"] = best["pdf_url"]
        row["status"] = "ready"
        row["notes"] = append_note(row.get("notes", ""), f"Resolved paper PDF from official AAAI OJS proceedings title match score={best_score:.2f}.")
        return row
    return None


def candidate_pdfs_from_page(row):
    page_url = row.get("paper_page_url", "")
    if not page_url:
        return []
    try:
        source = fetch(page_url)
    except Exception:
        return []
    candidates = []
    direct_pdf = discover_paper_pdf(source, page_url)
    if direct_pdf and "openreview.net/pdf" not in direct_pdf:
        candidates.append((direct_pdf, "conference page direct PDF link"))
    for href, text in links_from_html(source, page_url):
        if "arxiv.org/" in href:
            arxiv_pdf = arxiv_pdf_from_abs(href)
            if arxiv_pdf:
                candidates.append((arxiv_pdf, f"conference page arXiv link: {text or href}"))
    return candidates


def resolve_row(row, use_arxiv, max_arxiv_queries, arxiv_cache, arxiv_delay, aaai_articles=None, trust_aaai_ojs=False):
    if row.get("venue") == "AAAI" and aaai_articles is not None:
        resolved = resolve_aaai_ojs(row, aaai_articles, verify=not trust_aaai_ojs)
        if resolved:
            return resolved

    if row.get("pdf_url") and verified_pdf(row["pdf_url"]):
        row["status"] = "ready"
        row["notes"] = append_note(row.get("notes", ""), "Verified existing paper PDF.")
        return row

    for pdf_url, reason in candidate_pdfs_from_page(row):
        if verified_pdf(pdf_url):
            row["pdf_url"] = pdf_url
            row["status"] = "ready"
            row["notes"] = append_note(row.get("notes", ""), f"Resolved paper PDF: {reason}.")
            return row

    if use_arxiv and row.get("title"):
        pdf_url, reason = arxiv_title_query(
            row["title"],
            max_queries=max_arxiv_queries,
            cache=arxiv_cache,
            arxiv_delay=arxiv_delay,
        )
        if pdf_url and verified_pdf(pdf_url):
            row["pdf_url"] = pdf_url
            row["status"] = "ready"
            row["notes"] = append_note(row.get("notes", ""), f"Resolved paper PDF from {reason}.")
            return row

    row["pdf_url"] = ""
    row["status"] = "needs_pdf_url"
    row["notes"] = append_note(
        row.get("notes", ""),
        "No reachable non-gated whole-paper PDF found; do not harvest this row yet.",
    )
    return row


def append_note(existing, addition):
    existing = (existing or "").strip()
    return f"{existing} {addition}".strip() if existing else addition


def parse_args():
    output_dir = configured_output_dir()
    parser = argparse.ArgumentParser(description="Resolve oral manifest rows to verified non-gated paper PDFs.")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--venue", action="append")
    parser.add_argument("--limit", type=int, help="Maximum matching rows to attempt.")
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--no-arxiv", action="store_true", help="Disable arXiv title-search fallback.")
    parser.add_argument("--max-arxiv-queries", type=int, default=2)
    parser.add_argument("--arxiv-delay", type=float, default=3.0)
    parser.add_argument("--arxiv-cache", type=Path, default=output_dir / "arxiv-resolution-cache.json")
    parser.add_argument("--aaai-ojs-cache", type=Path, default=output_dir / "aaai-ojs-index.json")
    parser.add_argument(
        "--trust-aaai-ojs",
        action="store_true",
        help="Trust official AAAI OJS proceedings PDF links during resolution; final harvesting still fetches and validates the PDF.",
    )
    parser.add_argument("--in-place", action="store_true", help="Overwrite the input manifest.")
    parser.set_defaults(
        manifest=output_dir / f"ai-venue-oral-papers-{DEFAULT_YEAR}.csv",
        output=output_dir / f"ai-venue-oral-papers-{DEFAULT_YEAR}-resolved.csv",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if "--year" in sys.argv and "--manifest" not in sys.argv:
        args.manifest = configured_output_dir() / f"ai-venue-oral-papers-{args.year}.csv"
    if "--year" in sys.argv and "--output" not in sys.argv:
        args.output = configured_output_dir() / f"ai-venue-oral-papers-{args.year}-resolved.csv"
    if args.in_place:
        args.output = args.manifest

    rows = list(csv.DictReader(args.manifest.open(encoding="utf-8")))
    if args.arxiv_cache.exists():
        arxiv_cache = json.loads(args.arxiv_cache.read_text(encoding="utf-8"))
    else:
        arxiv_cache = {}
    attempted = 0
    resolved = 0
    output_rows = []
    aaai_articles = None
    selected_venues = set(args.venue or [])
    if not selected_venues or "AAAI" in selected_venues:
        aaai_articles = aaai_ojs_index(args.year, args.aaai_ojs_cache)
    for row in rows:
        has_resolvable_target = bool(row.get("paper_page_url") or row.get("pdf_url") or row.get("venue") == "AAAI")
        should_attempt = has_resolvable_target and (not args.venue or row.get("venue") in args.venue)
        if should_attempt and (args.limit is None or attempted < args.limit):
            attempted += 1
            row = resolve_row(
                row,
                use_arxiv=not args.no_arxiv,
                max_arxiv_queries=args.max_arxiv_queries,
                arxiv_cache=arxiv_cache,
                arxiv_delay=args.arxiv_delay,
                aaai_articles=aaai_articles,
                trust_aaai_ojs=args.trust_aaai_ojs,
            )
            if row.get("status") == "ready":
                resolved += 1
            print(f"{row.get('venue')} {row.get('paper_id')}: {row.get('status')} {row.get('pdf_url')}", flush=True)
            args.arxiv_cache.parent.mkdir(parents=True, exist_ok=True)
            args.arxiv_cache.write_text(json.dumps(arxiv_cache, indent=2, sort_keys=True), encoding="utf-8")
            if args.sleep:
                time.sleep(args.sleep)
        output_rows.append(row)

    args.arxiv_cache.parent.mkdir(parents=True, exist_ok=True)
    args.arxiv_cache.write_text(json.dumps(arxiv_cache, indent=2, sort_keys=True), encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Attempted {attempted}; resolved {resolved}; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
