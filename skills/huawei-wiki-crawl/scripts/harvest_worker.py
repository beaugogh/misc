#!/usr/bin/env python3
"""Parallel harvest worker — one instance per browser tab.

Each worker takes a session name and a list of manifest paths, then harvests
them sequentially using that browser session. Multiple workers run in parallel,
each with its own tab.

Usage (as sub-agent):
    python3 scripts/harvest_worker.py --session h1 --manifests wiki/manifest/44072-manifest.json
    python3 scripts/harvest_worker.py --session h2 --manifests wiki/manifest/39599-manifest.json,wiki/manifest/43979-manifest.json
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
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

WIKI_DIR = Path("wiki")

# File locking for concurrent manifest access
import msvcrt

def load_manifest_locked(path: str, retries: int = 10) -> dict | None:
    """Load manifest with exclusive file lock."""
    for attempt in range(retries):
        try:
            f = open(path, "rb")
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            content = f.read()
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            f.close()
            if not content:
                time.sleep(0.3)
                continue
            return json.loads(content.decode("utf-8", errors="replace"))
        except (json.JSONDecodeError, UnicodeDecodeError, IOError, OSError) as e:
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                f.close()
            except:
                pass
            time.sleep(0.3 + attempt * 0.2)
            continue
    return None

def save_manifest_locked(path: str, data: dict, retries: int = 10) -> bool:
    """Save manifest with exclusive file lock (atomic write via temp file)."""
    tmp_path = path + ".tmp"
    for attempt in range(retries):
        try:
            content = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            # Lock the file, write temp, close (releases lock), then replace
            f = open(path, "rb")
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            with open(tmp_path, "wb") as tf:
                tf.write(content)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            f.close()
            os.replace(tmp_path, path)
            return True
        except (IOError, OSError):
            try:
                f.close()
            except:
                pass
            time.sleep(0.3 + attempt * 0.2)
            continue
    return False
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
        print(f"  [{session}] opencli eval error: {e}", file=sys.stderr)
        return None


def opencli_open(session: str, url: str, wait: int = 12) -> bool:
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


def harvest_page(page: dict, local_dir: str, session: str) -> str:
    url = page.get("url", "")
    wiki_sn = page.get("wiki_sn", "")
    if not wiki_sn or not url:
        return "skipped"

    domain_dir = WIKI_DIR / local_dir
    domain_dir.mkdir(parents=True, exist_ok=True)
    filepath = domain_dir / f"{wiki_sn}.md"
    if filepath.exists():
        return "skipped"

    # Navigate with short wait — access-denied pages show message almost instantly
    if not opencli_open(session, url, wait=4):
        return "failed"

    # FAST access-denied check — 5s timeout, no retry
    ad_check = opencli_eval(session, "document.body.innerText.includes('您没有查看') ? 'AD' : 'NO'", timeout=5)
    if ad_check == "AD":
        return "access_denied"

    # Not access-denied — now wait longer for SPA to fully render the article
    time.sleep(8)

    # Extract article content
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
        time.sleep(3)
        result = opencli_eval(session, js, timeout=15)
    if not result:
        return "failed"
    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        return "failed"

    if data.get("error"):
        # Content not found — check access-denied one more time with longer timeout
        ad_check2 = opencli_eval(session, "document.body.textContent.includes('开通权限') ? 'AD' : 'NO'", timeout=10)
        if ad_check2 == "AD":
            return "access_denied"
        return "failed"

    html = data.get("html", "")
    text = data.get("text", "")
    title = data.get("title", page.get("title", ""))
    breadcrumb = data.get("breadcrumb", "")

    # Check for access-denied message in content
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
    p = argparse.ArgumentParser(description="Parallel harvest worker.")
    p.add_argument("--session", required=True, help="opencli browser session name (e.g. h1)")
    p.add_argument("--manifests", required=True, help="Comma-separated manifest paths")
    p.add_argument("--delay", type=float, default=1.0, help="Delay between pages")
    args = p.parse_args()

    manifest_paths = [m.strip() for m in args.manifests.split(",")]
    session = args.session

    print(f"[{session}] Starting harvest — {len(manifest_paths)} manifest(s)")

    total_harvested = 0
    total_skipped = 0
    total_failed = 0

    for manifest_path in manifest_paths:
        # Load manifest to get domain_id
        manifest = load_manifest_locked(manifest_path)
        if manifest is None:
            print(f"[{session}] Could not load manifest {manifest_path}, skipping")
            continue
        domain_id = str(manifest["domain_id"])
        local_dir = manifest.get("local_dir", str(domain_id))

        pending_count = sum(1 for p in manifest.get("pages", []) if p.get("harvest_status", "pending") == "pending")
        if pending_count == 0:
            print(f"[{session}] Domain {domain_id}: all pages done, skipping")
            continue

        print(f"[{session}] Domain {domain_id}: {pending_count} pending pages")

        dh = ds = df = 0
        processed = 0
        while True:
            # Reload manifest with lock to get latest state
            manifest = load_manifest_locked(manifest_path)
            if manifest is None:
                time.sleep(0.5)
                continue

            pages = manifest.get("pages", [])

            # Find next truly-pending page
            page = None
            page_idx = -1
            for idx, p in enumerate(pages):
                if p.get("harvest_status", "pending") == "pending":
                    page = p
                    page_idx = idx
                    break

            if page is None:
                break  # No more pending pages

            # Claim the page
            wiki_sn = page.get("wiki_sn", "")
            manifest["pages"][page_idx]["harvest_status"] = "in_progress"
            manifest["pages"][page_idx]["claimed_by"] = session
            if not save_manifest_locked(manifest_path, manifest):
                time.sleep(0.5)
                continue

            processed += 1

            # Harvest the page
            status = harvest_page(page, local_dir, session)

            # Reload manifest and update the page status
            manifest = load_manifest_locked(manifest_path)
            if manifest is None:
                # Save a minimal update
                for _ in range(5):
                    time.sleep(0.5)
                    manifest = load_manifest_locked(manifest_path)
                    if manifest:
                        break

            if manifest:
                for idx, p in enumerate(manifest["pages"]):
                    if p.get("wiki_sn") == wiki_sn:
                        manifest["pages"][idx]["harvest_status"] = status
                        break
                save_manifest_locked(manifest_path, manifest)

            if status == "harvested":
                dh += 1
                total_harvested += 1
            elif status == "skipped":
                ds += 1
                total_skipped += 1
            else:
                df += 1
                total_failed += 1

            if processed % 10 == 0:
                remaining = sum(1 for p in manifest.get("pages", []) if p.get("harvest_status", "pending") == "pending") if manifest else -1
                print(f"[{session}]   processed={processed} h={dh} s={ds} f={df} remaining={remaining}")

            time.sleep(args.delay)

        # Save final manifest
        manifest = load_manifest_locked(manifest_path)
        if manifest:
            manifest["harvest_summary"] = {
                "harvested": dh, "skipped": ds, "failed": df,
                "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            save_manifest_locked(manifest_path, manifest)

        print(f"[{session}] Domain {domain_id} done: h={dh} s={ds} f={df}")

    print(f"\n[{session}] COMPLETE: harvested={total_harvested} skipped={total_skipped} failed={total_failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
