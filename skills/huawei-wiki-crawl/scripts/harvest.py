#!/usr/bin/env python3
"""Harvest wiki pages using opencli browser + webpage-to-markdown skill.

For each wiki page:
1. Navigate via opencli browser (authenticated SPA session)
2. Extract the article HTML from the DOM (.content-article-body-warp)
3. Save HTML to temp file
4. Run webpage-to-markdown with --html to convert to clean Markdown
5. Save to wiki/<domain_id>/<wiki_sn>.md

Usage:
    python3 harvest.py --manifest wiki/manifest/39602-manifest.json --output wiki
    python3 harvest.py --manifest wiki/manifest/39602-manifest.json --output wiki --limit 10
    python3 harvest.py --url "https://clouddevops.huawei.com/domains/39602/wiki/2/WIKI2023122800744" --output wiki
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

WTM_SCRIPT = Path.home() / ".claude" / "skills" / "webpage-to-markdown" / "scripts" / "extract_url_markdown.py"
if not WTM_SCRIPT.exists():
    # Fallback to the misc/skills location
    WTM_SCRIPT = Path("D:/workspace/misc/skills/webpage-to-markdown/scripts/extract_url_markdown.py")


def find_opencli() -> str:
    for name in ("opencli.cmd", "opencli", "opencli.ps1"):
        p = shutil.which(name)
        if p:
            return p
    p = os.path.join(os.path.expandvars(r"%APPDATA%\npm"), "opencli.cmd")
    if os.path.isfile(p):
        return p
    return "opencli"


def opencli_eval(js: str, timeout: int = 30) -> str | None:
    opencli = find_opencli()
    env = {**os.environ, "NO_PROXY": "*", "ALL_PROXY": "", "HTTP_PROXY": "", "HTTPS_PROXY": ""}
    try:
        r = subprocess.run([opencli, "browser", "default", "eval", js],
                           capture_output=True, text=True, timeout=timeout, encoding="utf-8", env=env)
        if r.returncode == 0:
            return r.stdout.strip()
        return None
    except Exception as e:
        print(f"  opencli error: {e}", file=sys.stderr)
        return None


def opencli_open(url: str, wait: int = 6) -> bool:
    opencli = find_opencli()
    env = {**os.environ, "NO_PROXY": "*", "ALL_PROXY": "", "HTTP_PROXY": "", "HTTPS_PROXY": ""}
    try:
        subprocess.run([opencli, "browser", "default", "open", url],
                       capture_output=True, text=True, timeout=15, encoding="utf-8", env=env)
        time.sleep(wait)
        return True
    except Exception:
        return False


def extract_wiki_html(url: str) -> dict | None:
    """Navigate to a wiki page and extract the article HTML + metadata."""
    if not opencli_open(url, wait=6):
        return None

    # Extract content from the rendered SPA DOM
    js = (
        "(function(){"
        "var el=document.querySelector('.content-article-body-warp')||"
        "document.querySelector('.wiki-content-wrapper')||"
        "document.querySelector('.right-content');"
        "if(!el)return JSON.stringify({error:'no-content',title:document.title,url:window.location.href});"
        "var bc=document.querySelector('.breadcrumb,.wiki-path,[class*=path]');"
        "return JSON.stringify({"
        "title:document.title.replace(/^Wiki:\\s*/,''),"
        "breadcrumb:bc?bc.innerText.trim():'',"
        "html:el.innerHTML,"
        "text:el.innerText,"
        "textLength:el.innerText.length});})()"
    )
    result = opencli_eval(js, timeout=15)
    if not result:
        return None
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return None


def convert_to_markdown(html: str, source_url: str, title: str,
                        output_path: Path, domain_id: str) -> bool:
    """Run webpage-to-markdown with --html to convert HTML to clean Markdown."""
    if not WTM_SCRIPT.exists():
        print(f"  ERROR: webpage-to-markdown not found at {WTM_SCRIPT}", file=sys.stderr)
        return False

    # Write HTML to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False,
                                     encoding="utf-8", dir=tempfile.gettempdir()) as f:
        # Wrap in a basic HTML document with title
        f.write(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{title}</title></head><body><h1>{title}</h1>{html}</body></html>""")
        html_path = f.name

    try:
        cmd = [sys.executable, str(WTM_SCRIPT), source_url,
               "--html", html_path,
               "--output", str(output_path),
               "--name-chars", "90"]
        env = {**os.environ, "NO_PROXY": "*", "ALL_PROXY": "", "HTTP_PROXY": "", "HTTPS_PROXY": ""}
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           encoding="utf-8", env=env)
        if r.returncode == 0:
            return True
        else:
            print(f"  webpage-to-markdown failed: {r.stderr.strip()[:200]}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("  webpage-to-markdown timeout", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  webpage-to-markdown error: {e}", file=sys.stderr)
        return False
    finally:
        os.unlink(html_path)


def harvest_page(page: dict, domain_id: str, output_dir: Path) -> str:
    """Harvest a single wiki page. Returns status."""
    url = page.get("url", "")
    wiki_sn = page.get("wiki_sn") or ""
    title = page.get("title", "")

    if not wiki_sn or not url:
        return "skipped"

    domain_dir = output_dir / domain_id
    domain_dir.mkdir(parents=True, exist_ok=True)
    filepath = domain_dir / f"{wiki_sn}.md"

    # Skip if already harvested
    if filepath.exists():
        return "skipped"

    print(f"  Harvesting: {wiki_sn} — {title[:50] if title else url[:50]}")

    # Step 1: Extract HTML from the rendered SPA
    data = extract_wiki_html(url)
    if not data or data.get("error"):
        err = data.get("error", "unknown") if data else "no response"
        print(f"  FAILED: {err}", file=sys.stderr)
        return "failed"

    html = data.get("html", "")
    text = data.get("text", "")
    page_title = data.get("title", title)
    breadcrumb = data.get("breadcrumb", "")

    if not html or len(text) < 50:
        print(f"  FAILED: content too short ({len(text)} chars)", file=sys.stderr)
        return "failed"

    # Step 2: Convert to Markdown via webpage-to-markdown skill
    if convert_to_markdown(html, url, page_title, filepath, domain_id):
        # The script names files with date prefix — find the output and rename
        actual_file = None
        if filepath.exists():
            actual_file = filepath
        else:
            # The script might have created a differently-named file
            files = list(domain_dir.glob("*.md"))
            if files:
                # Find the newest file
                actual_file = max(files, key=os.path.getmtime)
                if actual_file != filepath:
                    actual_file.rename(filepath)

        if filepath.exists():
            # Add frontmatter with wiki metadata
            add_frontmatter(filepath, wiki_sn, page_title, url, domain_id, breadcrumb)
            size = filepath.stat().st_size
            print(f"  OK: {wiki_sn} — {page_title[:40]} ({size:,} bytes)")
            return "harvested"

    # Fallback: save the raw text if webpage-to-markdown fails
    print("  Fallback: saving raw text", file=sys.stderr)
    save_raw_text(filepath, text, wiki_sn, page_title, url, domain_id, breadcrumb)
    return "harvested_raw"


def add_frontmatter(filepath: Path, wiki_sn: str, title: str, url: str,
                    domain_id: str, breadcrumb: str):
    """Prepend YAML frontmatter to the harvested Markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if frontmatter already exists (webpage-to-markdown adds its own)
    if content.startswith("---"):
        # Insert wiki metadata into existing frontmatter
        end = content.find("\n---", 3)
        if end > 0:
            wiki_meta = f"\nwiki_sn: {wiki_sn}\ndomain_id: {domain_id}\nbreadcrumb: {breadcrumb}\nharvested_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\nharvest_method: opencli+webpage-to-markdown\n"
            content = content[:end] + wiki_meta + content[end:]
        else:
            frontmatter = f"---\nwiki_sn: {wiki_sn}\ntitle: {title}\nsource_url: {url}\ndomain_id: {domain_id}\nbreadcrumb: {breadcrumb}\nharvested_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\nharvest_method: opencli+webpage-to-markdown\n---\n\n"
            content = frontmatter + content
    else:
        frontmatter = f"---\nwiki_sn: {wiki_sn}\ntitle: {title}\nsource_url: {url}\ndomain_id: {domain_id}\nbreadcrumb: {breadcrumb}\nharvested_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\nharvest_method: opencli+webpage-to-markdown\n---\n\n"
        content = frontmatter + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def save_raw_text(filepath: Path, text: str, wiki_sn: str, title: str,
                  url: str, domain_id: str, breadcrumb: str):
    """Save raw text as fallback when webpage-to-markdown fails."""
    frontmatter = (
        f"---\n"
        f"wiki_sn: {wiki_sn}\n"
        f"title: {title}\n"
        f"source_url: {url}\n"
        f"domain_id: {domain_id}\n"
        f"breadcrumb: {breadcrumb}\n"
        f"harvested_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\n"
        f"harvest_method: opencli-raw-text\n"
        f"---\n\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + text)


def extract_domain_id(url: str) -> str | None:
    m = re.search(r"domains/(\d+)/wiki", url)
    return m.group(1) if m else None


def extract_wiki_sn(url: str) -> str | None:
    m = re.search(r"(WIKI\d+)", url, re.IGNORECASE)
    return m.group(1) if m else None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Harvest wiki pages to Markdown.")
    p.add_argument("--manifest", default=None, help="Path to manifest JSON")
    p.add_argument("--url", default=None, help="Harvest a single wiki page URL")
    p.add_argument("--output", default="wiki", help="Output directory")
    p.add_argument("--limit", type=int, default=None, help="Max pages to harvest")
    p.add_argument("--delay", type=float, default=2.0, help="Delay between pages (seconds)")
    args = p.parse_args(argv)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Single-page mode
    if args.url:
        domain_id = extract_domain_id(args.url) or "unknown"
        wiki_sn = extract_wiki_sn(args.url) or "UNKNOWN"
        page = {"url": args.url, "wiki_sn": wiki_sn, "title": ""}
        status = harvest_page(page, domain_id, output_dir)
        print(f"\nResult: {status}")
        return 0 if "harvested" in status else 1

    if not args.manifest:
        print("error: provide --manifest or --url", file=sys.stderr)
        return 1

    # Load manifest
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)

    domain_id = str(manifest.get("domain_id", "unknown"))
    pages = manifest.get("pages", [])

    # Filter to pending pages only
    pending = [p for p in pages if p.get("harvest_status", "pending") == "pending"]
    if args.limit:
        pending = pending[:args.limit]

    print(f"Domain: {domain_id}")
    print(f"Total pages: {len(pages)}, pending: {len(pending)}")
    print(f"Output: {output_dir / domain_id}/")
    print(f"webpage-to-markdown: {WTM_SCRIPT}")
    print()

    harvested = skipped = failed = 0

    for i, page in enumerate(pending, 1):
        print(f"[{i}/{len(pending)}]")
        status = harvest_page(page, domain_id, output_dir)
        page["harvest_status"] = status

        if "harvested" in status:
            harvested += 1
        elif status == "skipped":
            skipped += 1
        else:
            failed += 1

        if args.delay and i < len(pending):
            time.sleep(args.delay)

    # Update manifest with harvest status
    manifest["harvest_summary"] = {
        "total": len(pending), "harvested": harvested,
        "skipped": skipped, "failed": failed,
        "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Summary: {harvested} harvested, {skipped} skipped, {failed} failed")
    print(f"Manifest updated: {args.manifest}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
