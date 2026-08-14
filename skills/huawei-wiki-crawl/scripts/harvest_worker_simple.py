#!/usr/bin/env python3
"""Simple harvest worker — processes a pre-assigned slice of pages.
No manifest locking needed because each worker has its own page range.

Usage:
    python3 harvest_worker_simple.py --session w1 --manifest wiki/manifest/28786-manifest.json --worker 0 --total 6
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

WIKI_DIR = Path("wiki")


def find_opencli() -> str:
    for name in ("opencli.cmd", "opencli", "opencli.ps1"):
        p = shutil.which(name)
        if p:
            return p
    p = os.path.join(os.path.expandvars(r"%APPDATA%\npm"), "opencli.cmd")
    if os.path.isfile(p):
        return p
    return "opencli"


def opencli_eval(session: str, js: str, timeout: int = 30) -> str | None:
    opencli = find_opencli()
    env = {**os.environ, "NO_PROXY": "*", "ALL_PROXY": "", "HTTP_PROXY": "", "HTTPS_PROXY": ""}
    try:
        r = subprocess.run(
            [opencli, "browser", session, "eval", js],
            capture_output=True, text=True, timeout=timeout, encoding="utf-8", env=env,
        )
        if r.returncode == 0:
            return r.stdout.strip()
        return None
    except Exception as e:
        print(f"  [{session}] eval error: {e}", file=sys.stderr)
        return None


def opencli_open(session: str, url: str, wait: int = 8) -> bool:
    opencli = find_opencli()
    env = {**os.environ, "NO_PROXY": "*", "ALL_PROXY": "", "HTTP_PROXY": "", "HTTPS_PROXY": ""}
    try:
        subprocess.run(
            [opencli, "browser", session, "open", url],
            capture_output=True, text=True, timeout=15, encoding="utf-8", env=env,
        )
        time.sleep(wait)
        return True
    except Exception:
        return False


def harvest_page(page: dict, domain_id: str, session: str) -> str:
    url = page.get("url", "")
    wiki_sn = page.get("wiki_sn", "")
    if not wiki_sn or not url:
        return "skipped"

    domain_dir = WIKI_DIR / str(domain_id)
    domain_dir.mkdir(parents=True, exist_ok=True)
    filepath = domain_dir / f"{wiki_sn}.md"
    if filepath.exists():
        return "skipped"

    if not opencli_open(session, url, wait=8):
        return "failed"

    js = (
        "(function(){"
        "var el=document.querySelector('.content-article-body-warp')||"
        "document.querySelector('.wiki-content-wrapper')||"
        "document.querySelector('.right-content');"
        "if(!el)return JSON.stringify({error:'no-content'});"
        "var bc=document.querySelector('.breadcrumb,.wiki-path,[class*=path]');"
        "return JSON.stringify({"
        "title:document.title.replace(/^Wiki:\\s*/,''),"
        "breadcrumb:bc?bc.innerText.trim():'',"
        "html:el.innerHTML,text:el.innerText,textLength:el.innerText.length});})()"
    )
    result = opencli_eval(session, js, timeout=15)
    if not result:
        # Retry after additional wait
        time.sleep(5)
        result = opencli_eval(session, js, timeout=15)
    if not result:
        return "failed"
    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        return "failed"

    if data.get("error"):
        return "failed"

    text = data.get("text", "")
    title = data.get("title", page.get("title", ""))
    breadcrumb = data.get("breadcrumb", "")

    # Check for access-denied
    if text and ("您没有查看这篇WIKI的权限" in text or "开通权限" in text):
        return "access_denied"

    if not text or len(text) < 50:
        return "failed"

    frontmatter = (
        f"---\n"
        f"wiki_sn: {wiki_sn}\n"
        f"title: {title}\n"
        f"source_url: {url}\n"
        f"domain_id: {domain_id}\n"
        f"breadcrumb: {breadcrumb}\n"
        f"harvested_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\n"
        f"harvest_method: opencli-{session}\n"
        f"---\n\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + text)

    return "harvested"


def main():
    p = argparse.ArgumentParser(description="Simple harvest worker with page slicing.")
    p.add_argument("--session", required=True, help="opencli browser session name")
    p.add_argument("--manifest", required=True, help="Manifest path")
    p.add_argument("--worker", type=int, required=True, help="Worker index (0-based)")
    p.add_argument("--total", type=int, required=True, help="Total number of workers")
    p.add_argument("--delay", type=float, default=1.0, help="Delay between pages")
    args = p.parse_args()

    session = args.session

    # Load manifest
    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    domain_id = str(manifest["domain_id"])
    pages = manifest.get("pages", [])

    # Assign strided slice: worker N gets pages[N], pages[N+total], pages[N+2*total], ...
    my_pages = [(i, pages[i]) for i in range(args.worker, len(pages), args.total)
                if pages[i].get("harvest_status", "pending") == "pending"
                and not (WIKI_DIR / domain_id / f"{pages[i].get('wiki_sn','')}.md").exists()]

    if not my_pages:
        print(f"[{session}] Worker {args.worker}/{args.total}: no pending pages, done")
        return 0

    print(f"[{session}] Worker {args.worker}/{args.total}: {len(my_pages)} pending pages")

    dh = ds = df = 0
    for i, (orig_idx, page) in enumerate(my_pages, 1):
        status = harvest_page(page, domain_id, session)

        # Update manifest (single worker per stride, so no contention on these specific pages)
        try:
            with open(args.manifest, encoding="utf-8") as f:
                manifest = json.load(f)
            manifest["pages"][orig_idx]["harvest_status"] = status
            with open(args.manifest, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
        except (json.JSONDecodeError, IOError, OSError):
            pass  # Non-critical

        if status == "harvested":
            dh += 1
        elif status == "skipped":
            ds += 1
        else:
            df += 1

        if i % 10 == 0 or i == len(my_pages):
            print(f"[{session}]   [{i}/{len(my_pages)}] h={dh} s={ds} f={df}")

        time.sleep(args.delay)

    print(f"[{session}] Worker {args.worker}/{args.total} done: h={dh} s={ds} f={df}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
