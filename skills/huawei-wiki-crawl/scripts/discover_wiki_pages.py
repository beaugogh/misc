#!/usr/bin/env python3
"""Discover all wiki pages in a CloudDevOps wiki domain.

Uses the CloudDevOps REST API (/devops-knowledge-management/api/) with the
visionUserToken JWT as Authorization header. Falls back to opencli browser
DOM extraction if the API is unavailable.

Usage:
    python3 discover_wiki_pages.py "https://clouddevops.huawei.com/domains/44072/wiki" --output ./wiki
    python3 discover_wiki_pages.py "https://clouddevops.huawei.com/domains/44072/wiki" --token <jwt>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

API_BASE = "https://clouddevops.huawei.com/devops-knowledge-management/api"


def extract_domain_id(url: str) -> str | None:
    m = re.search(r"domains/(\d+)/wiki", url)
    return m.group(1) if m else None


def api_get(path: str, token: str, timeout: int = 15) -> dict | None:
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": token,
        "Accept": "application/json",
    })
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  API GET error ({path}): {e}", file=sys.stderr)
        return None


def api_post(path: str, token: str, body: dict, timeout: int = 15) -> dict | None:
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }, method="POST")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  API POST error ({path}): {e}", file=sys.stderr)
        return None


def discover_kanbans(domain_id: str, token: str) -> list[dict]:
    """List all wiki kanban boards in a domain."""
    d = api_get(f"/wiki/kanban?domain_id={domain_id}", token)
    if not d or d.get("code") != 200:
        return []
    return d.get("data", []) or []


def discover_articles(domain_id: str, kanban_id: int, token: str,
                      page_size: int = 100) -> list[dict]:
    """Search for all published wiki articles in a kanban."""
    all_records = []
    page = 1
    while True:
        body = {
            "status": ["published"],
            "searchKey": "",
            "pagination": {"current_page": page, "page_size": page_size},
            "sort": "lastUpdateTimeDESC",
            "condition": {},
            "select_field": ["assigned_domain_simple", "tags"],
            "kanbanId": kanban_id,
            "domainId": int(domain_id),
            "searchSreAttr": False,
        }
        d = api_post("/v2/search/wiki", token, body)
        if not d or d.get("code") != 200:
            break
        data = d.get("data", {})
        records = data.get("result") or data.get("listByPage") or []
        if not records:
            break
        for r in records:
            all_records.append({
                "id": r.get("id"),
                "title": r.get("title", ""),
                "wiki_sn": r.get("wikiSn") or r.get("sn") or "",
                "kanban_id": kanban_id,
                "kanban_title": r.get("kanbanTitle", ""),
                "category": r.get("category", ""),
                "status": r.get("status", ""),
                "created_by": r.get("created_by"),
                "url": f"https://clouddevops.huawei.com/domains/{domain_id}/wiki/{kanban_id}/{r.get('wikiSn') or r.get('sn', '')}",
                "harvest_status": "pending",
            })
        total = int(data.get("total_records", 0))
        total_pages = int(data.get("total_pages", 1))
        print(f"  Kanban {kanban_id}: page {page}/{total_pages} ({len(all_records)}/{total} articles)")
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.5)
    return all_records


def discover_via_opencli(domain_id: str, url: str) -> list[dict]:
    """Fallback: use opencli browser to discover wiki pages from DOM."""
    print(f"Fallback: discovering via opencli browser for domain {domain_id}...")
    pages = []
    try:
        # Navigate to the wiki domain page
        subprocess.run(["opencli", "browser", "default", "open", url],
                       capture_output=True, text=True, timeout=15)
        time.sleep(5)
        # Extract category/kanban info from the DOM
        result = subprocess.run(
            ["opencli", "browser", "default", "eval",
             "document.body.innerText.substring(0, 5000)"],
            capture_output=True, text=True, timeout=15)
        text = result.stdout.strip().strip('"')
        # Parse categories and article counts
        for m in re.finditer(r"([^\n]+)\n共(\d+)篇文章", text):
            title, count = m.group(1).strip(), int(m.group(2))
            pages.append({
                "id": None,
                "title": title,
                "wiki_sn": "",
                "kanban_title": title,
                "article_count": count,
                "url": f"{url}",
                "harvest_status": "pending",
                "source": "opencli_dom",
            })
            print(f"  Found category: {title} ({count} articles)")
    except Exception as e:
        print(f"  opencli error: {e}", file=sys.stderr)
    return pages


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Discover wiki pages in a CloudDevOps wiki domain.",
    )
    p.add_argument("url", help="Wiki domain URL")
    p.add_argument("--output", default="./wiki", help="Output directory")
    p.add_argument("--token", default=None, help="visionUserToken JWT (or set CLOUDDEVOPS_TOKEN env)")
    p.add_argument("--json", action="store_true", help="Print manifest as JSON")
    args = p.parse_args(argv)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    domain_id = extract_domain_id(args.url)
    if not domain_id:
        print(f"error: could not extract domainId from URL: {args.url}", file=sys.stderr)
        return 1

    token = args.token or os.environ.get("CLOUDDEVOPS_TOKEN") or os.environ.get("CLOUDDEVOPS_X_AUTH_TOKEN")

    pages = []
    method = "none"

    if token:
        print(f"Discovering via REST API (domainId={domain_id})...")
        method = "api"
        kanbans = discover_kanbans(domain_id, token)
        print(f"Found {len(kanbans)} kanban board(s)")
        for kb in kanbans:
            kb_id = kb.get("id")
            kb_title = kb.get("title", "")
            wiki_total = kb.get("wiki_total", "?")
            print(f"\nKanban: {kb_title} (id={kb_id}, ~{wiki_total} articles)")
            articles = discover_articles(domain_id, kb_id, token)
            pages.extend(articles)

    if not pages:
        pages = discover_via_opencli(domain_id, args.url)
        method = "opencli"

    if not pages:
        # Last resort: repo-code scan
        method = "repo_scan"
        print("No API token and opencli failed — falling back to repo-code scan (partial)")
        pages = discover_via_repo_scan(domain_id)

    # Deduplicate by wiki_sn
    seen = set()
    unique = []
    for p in pages:
        sn = p.get("wiki_sn", "")
        key = sn or p.get("title", "")
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        unique.append(p)

    manifest = {
        "domain_id": domain_id,
        "domain_url": args.url,
        "discovered_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "discovery_method": method,
        "page_count": len(unique),
        "pages": unique,
    }

    manifest_path = output_dir / f"{domain_id}-manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print(f"\nDomain: {domain_id}")
        print(f"Method: {method}")
        print(f"Pages: {len(unique)}")
        print(f"Manifest: {manifest_path}")
        for p in unique[:20]:
            print(f"  {p.get('wiki_sn','?')}: {p.get('title','')[:50]}")
        if len(unique) > 20:
            print(f"  ... and {len(unique) - 20} more")

    return 0


def discover_via_repo_scan(domain_id: str) -> list[dict]:
    """Last-resort fallback: scan repo code for wiki URLs."""
    pages = []
    pattern = re.compile(
        r"https?://[a-z0-9.-]+\.huawei\.com/domains/" + re.escape(domain_id) +
        r"/wiki/[^\s)\"'\]\\]*(WIKI\d+)", re.IGNORECASE)
    skip = {".git", "node_modules", "target", "build", "_book", ".idea"}
    repos_dir = Path("repos")
    if repos_dir.exists():
        for root, dirs, files in os.walk(repos_dir):
            dirs[:] = [d for d in dirs if d not in skip]
            for fn in files:
                if not fn.endswith((".md", ".yml", ".yaml", ".txt", ".html", ".json")):
                    continue
                fp = os.path.join(root, fn)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            for m in pattern.finditer(line):
                                url = m.group(0).rstrip(".,;)")
                                sn = m.group(1)
                                pages.append({
                                    "wiki_sn": sn, "title": "", "url": url,
                                    "kanban_id": None, "harvest_status": "pending",
                                    "source": "repo_code",
                                })
                except OSError:
                    pass
    return pages


if __name__ == "__main__":
    raise SystemExit(main())
