#!/usr/bin/env python3
"""Crawl a CloudDevOps wiki domain: discover pages, then harvest each to Markdown.

Orchestrates two phases:
1. Discovery: run discover_wiki_pages.py to build a manifest of wiki pages.
2. Harvest: for each page, extract content via opencli browser DOM extraction,
   then convert to Markdown using webpage-to-markdown.

Usage:
    # Full crawl (discover + harvest)
    python3 crawl_wiki_domain.py "https://clouddevops.huawei.com/domains/44072/wiki" --output ./wiki --token <jwt>

    # Harvest from existing manifest
    python3 crawl_wiki_domain.py --manifest ./wiki/44072-manifest.json --output ./wiki --token <jwt>

    # Harvest a single page
    python3 crawl_wiki_domain.py --url "https://clouddevops.huawei.com/domains/28786/wiki/2/WIKI2026030401189" --output ./wiki --token <jwt>
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

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SKILL_DIR / "config.yaml"
DISCOVER_SCRIPT = SCRIPT_DIR / "discover_wiki_pages.py"

DEFAULTS = {
    "output": "./wiki",
    "delay_seconds": 2,
    "timeout_seconds": 30,
    "webpage_to_markdown_path": "../webpage-to-markdown/scripts/extract_url_markdown.py",
}


def load_config() -> dict:
    cfg = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            import yaml  # type: ignore
            with open(CONFIG_PATH, encoding="utf-8") as f:
                cfg.update(yaml.safe_load(f) or {})
        except ImportError:
            pass
    for key in ("webpage_to_markdown_path",):
        if key in cfg and not os.path.isabs(cfg[key]):
            cfg[key] = str((SKILL_DIR / cfg[key]).resolve())
    return cfg


def extract_domain_id(url: str) -> str | None:
    m = re.search(r"domains/(\d+)/wiki", url)
    return m.group(1) if m else None


def extract_wiki_sn(url: str) -> str | None:
    m = re.search(r"(WIKI\d+)", url, re.IGNORECASE)
    return m.group(1) if m else None


def find_opencli() -> str:
    """Find the opencli executable (handles Windows npm global)."""
    for name in ("opencli", "opencli.cmd", "opencli.ps1"):
        path = shutil.which(name)
        if path:
            return path
    # Check common npm global locations
    for base in (os.path.expandvars(r"%APPDATA%\npm"), os.path.expanduser("~/.npm-global/bin")):
        for ext in ("", ".cmd", ".ps1"):
            p = os.path.join(base, f"opencli{ext}")
            if os.path.isfile(p):
                return p
    return "opencli"  # fallback, may fail


def opencli_eval(js: str, timeout: int = 30) -> str | None:
    """Run opencli browser eval and return the result."""
    opencli = find_opencli()
    try:
        result = subprocess.run(
            [opencli, "browser", "default", "eval", js],
            capture_output=True, text=True, timeout=timeout, encoding="utf-8",
            env={**os.environ, "NO_PROXY": "*", "ALL_PROXY": "",
                 "HTTP_PROXY": "", "HTTPS_PROXY": ""})
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"  opencli error: {e}", file=sys.stderr)
        return None


def opencli_navigate(url: str, wait: int = 5) -> bool:
    """Navigate the browser to a URL and wait for it to load."""
    opencli = find_opencli()
    try:
        subprocess.run(
            [opencli, "browser", "default", "open", url],
            capture_output=True, text=True, timeout=15, encoding="utf-8",
            env={**os.environ, "NO_PROXY": "*", "ALL_PROXY": "",
                 "HTTP_PROXY": "", "HTTPS_PROXY": ""})
        time.sleep(wait)
        return True
    except Exception:
        return False


def resolve_local_dir(domain_id: str, output_dir: Path, override: str | None = None) -> str:
    """Resolve the output folder name for a domain.

    Naming convention: {general_domain}-{sub_domain}-{domain_id}
    e.g. data-CloudDB-44072, cloudnative-KKEI-47138, middleware-GEMAS-28877

    Lookup order:
    1. Explicit override (--local-dir argument)
    2. local_dir field in existing manifest (wiki/manifest/{domain_id}-manifest.json)
    3. Existing folder in wiki/ that ends with the domain_id
    4. Fallback to bare domain_id (with a warning)
    """
    if override:
        return override

    # Check manifest for local_dir
    manifest_path = output_dir / "manifest" / f"{domain_id}-manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            local_dir = manifest.get("local_dir")
            if local_dir:
                return local_dir
        except (json.JSONDecodeError, OSError):
            pass

    # Check if a folder matching *-{domain_id} already exists in output_dir
    if output_dir.exists():
        for entry in output_dir.iterdir():
            if entry.is_dir() and entry.name.endswith(f"-{domain_id}"):
                return entry.name

    # Fallback: bare domain_id
    print(f"  WARNING: no local_dir found for domain {domain_id}. "
          f"Using bare ID '{domain_id}'. "
          f"Pass --local-dir to specify the conventional name "
          f"(e.g. data-CloudDB-{domain_id}).", file=sys.stderr)
    return domain_id


def harvest_via_opencli(url: str, wiki_sn: str, domain_id: str,
                        output_dir: Path, cfg: dict,
                        local_dir: str | None = None) -> str:
    """Harvest a wiki page by navigating to it and extracting DOM content via opencli.

    This is the primary harvest method — it uses the user's authenticated
    browser session (via opencli) to render the SPA page and extract content.
    """
    folder_name = resolve_local_dir(domain_id, output_dir, local_dir)
    domain_dir = output_dir / folder_name
    domain_dir.mkdir(parents=True, exist_ok=True)
    filepath = domain_dir / f"{wiki_sn}.md"

    # Check if already harvested
    if filepath.exists():
        return "skipped"

    # Navigate to the wiki page
    if not opencli_navigate(url, wait=6):
        return "failed"

    # Extract the article content from the DOM
    # The wiki content is in .content-article-body-warp (Angular component)
    js = ("(function(){var el=document.querySelector('.content-article-body-warp')||"
          "document.querySelector('.wiki-content-wrapper')||"
          "document.querySelector('.right-content');"
          "if(!el)return JSON.stringify({error:'not found',title:document.title});"
          "var bc=document.querySelector('.breadcrumb,.wiki-path,[class*=path]');"
          "return JSON.stringify({"
          "title:document.title.replace(/^Wiki:\\s*/,''),"
          "breadcrumb:bc?bc.innerText.trim():'',"
          "text:el.innerText,"
          "html:el.innerHTML,"
          "textLength:el.innerText.length});})()")
    result = opencli_eval(js, timeout=15)
    if not result:
        return "failed"

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        # Try removing outer quotes
        try:
            data = json.loads(result.strip('"').replace('\\"', '"'))
        except json.JSONDecodeError:
            print(f"  Failed to parse opencli result for {wiki_sn}", file=sys.stderr)
            return "failed"

    if data.get("error"):
        print(f"  {data['error']} for {wiki_sn}", file=sys.stderr)
        return "failed"

    title = data.get("title", "")
    text = data.get("text", "")
    html = data.get("html", "")
    breadcrumb = data.get("breadcrumb", "")

    if not text or len(text) < 50:
        print(f"  Content too short ({len(text)} chars) for {wiki_sn}", file=sys.stderr)
        return "failed"

    # Write as Markdown with frontmatter
    frontmatter = f"""---
wiki_sn: {wiki_sn}
title: {title}
source_url: {url}
domain_id: {domain_id}
breadcrumb: {breadcrumb}
harvested_at: {time.strftime("%Y-%m-%dT%H:%M:%S")}
harvest_method: opencli_dom
---

"""
    # Convert HTML to simple Markdown (basic conversion)
    # For rich conversion, the webpage-to-markdown skill can be used
    markdown = html_to_markdown(html, text)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + markdown)

    print(f"  Harvested: {wiki_sn} — {title[:50]} ({len(text)} chars)")
    return "harvested"


def html_to_markdown(html: str, fallback_text: str) -> str:
    """Basic HTML-to-Markdown conversion. Falls back to plain text."""
    # If webpage-to-markdown script is available, use it for better conversion
    # For now, use the innerText as the Markdown body
    # (the DOM innerText is already structured with line breaks)
    return fallback_text


def run_discovery(url: str, output_dir: Path, token: str | None) -> str | None:
    """Run the discovery script and return the manifest path."""
    cmd = [sys.executable, str(DISCOVER_SCRIPT), url, "--output", str(output_dir)]
    if token:
        cmd.extend(["--token", token])
    try:
        subprocess.run(cmd, timeout=120)
    except Exception:
        return None
    domain_id = extract_domain_id(url)
    if not domain_id:
        return None
    manifest_path = output_dir / f"{domain_id}-manifest.json"
    return str(manifest_path) if manifest_path.exists() else None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Crawl and harvest a CloudDevOps wiki domain into Markdown.")
    p.add_argument("url", nargs="?", help="Wiki domain URL to crawl")
    p.add_argument("--manifest", default=None, help="Existing manifest JSON (skip discovery)")
    p.add_argument("--url-single", "--url", dest="single_url", default=None,
                   help="Harvest a single wiki page URL")
    p.add_argument("--output", default=None, help="Output directory")
    p.add_argument("--token", default=None, help="visionUserToken JWT")
    p.add_argument("--delay", type=float, default=None, help="Delay between fetches (seconds)")
    p.add_argument("--local-dir", default=None,
                   help="Override folder name (e.g. data-CloudDB-49870). "
                        "Default: look up from manifest or fallback to domain ID.")
    args = p.parse_args(argv)

    cfg = load_config()
    output_dir = Path(args.output or cfg["output"])
    output_dir.mkdir(parents=True, exist_ok=True)
    delay = args.delay or cfg.get("delay_seconds", 2)
    token = args.token or os.environ.get("CLOUDDEVOPS_TOKEN") or os.environ.get("CLOUDDEVOPS_X_AUTH_TOKEN")

    # Single-page mode
    if args.single_url:
        wiki_sn = extract_wiki_sn(args.single_url) or "UNKNOWN"
        domain_id = extract_domain_id(args.single_url) or "unknown"
        status = harvest_via_opencli(args.single_url, wiki_sn, domain_id,
                                     output_dir, cfg, local_dir=args.local_dir)
        print(f"\nResult: {status}")
        return 0 if status != "failed" else 1

    # Discovery phase
    manifest_path = args.manifest
    if not manifest_path:
        if not args.url:
            print("error: provide a wiki domain URL or --manifest", file=sys.stderr)
            return 1
        print(f"Phase 1: Discovery for {args.url}")
        manifest_path = run_discovery(args.url, output_dir, token)
        if not manifest_path or not os.path.exists(manifest_path):
            print("error: discovery failed", file=sys.stderr)
            return 1

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    domain_id = manifest.get("domain_id", "unknown")
    pages = manifest.get("pages", [])
    # Use manifest's local_dir if present, fall back to resolve_local_dir
    local_dir = manifest.get("local_dir") or resolve_local_dir(
        str(domain_id), output_dir, args.local_dir)
    manifest.setdefault("local_dir", local_dir)  # persist if not already set
    print(f"\nPhase 2: Harvesting {len(pages)} page(s) for domain {domain_id}")
    print(f"Output: {output_dir / local_dir}/")
    print(f"Method: opencli browser DOM extraction")
    print()

    harvested = skipped = failed = 0

    for i, page in enumerate(pages, 1):
        url = page.get("url", "")
        wiki_sn = page.get("wiki_sn") or extract_wiki_sn(url) or "UNKNOWN"
        title = page.get("title", "")
        print(f"[{i}/{len(pages)}] {wiki_sn} — {title[:40]}")

        status = harvest_via_opencli(url, wiki_sn, domain_id,
                                     output_dir, cfg, local_dir=local_dir)
        page["harvest_status"] = status

        if status == "harvested":
            harvested += 1
        elif status == "skipped":
            skipped += 1
        else:
            failed += 1

        if delay and i < len(pages):
            time.sleep(delay)

    manifest["harvest_summary"] = {
        "total": len(pages), "harvested": harvested,
        "skipped": skipped, "failed": failed,
        "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Summary: {harvested} harvested, {skipped} skipped, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
