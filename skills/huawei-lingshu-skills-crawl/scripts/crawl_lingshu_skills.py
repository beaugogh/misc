#!/usr/bin/env python3
"""Crawl the Lingshu Agent skill library (灵枢Agent) onto the local machine.

Discovers all skills via the agent-service REST API and downloads each
skill's source ZIP, using the authenticated browser session via opencli.

Usage:
    # Crawl everything
    python3 crawl_lingshu_skills.py

    # Only published skills
    python3 crawl_lingshu_skills.py --status published

    # List only, no downloads
    python3 crawl_lingshu_skills.py --list-only

    # Fresh re-crawl
    python3 crawl_lingshu_skills.py --refresh
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SKILL_DIR / "output"

LINGSHU_URL = "https://cloudscope.ulanqab.huawei.com/lingshu-agent-alpha/#/skill"
API_BASE = "/lingshu-agent-alpha/copilot-rest/v1/agent-service"

PAGE_SIZE = 10          # server-side max observed
DOWNLOAD_DELAY = 1.5    # seconds between downloads
MAX_RETRIES = 3
EVAL_TIMEOUT = 60       # per fetch; zips can take a while


def find_opencli() -> str:
    """Find the opencli executable (handles Windows npm global)."""
    for name in ("opencli", "opencli.cmd", "opencli.ps1"):
        path = shutil.which(name)
        if path:
            return path
    for base in (os.path.expandvars(r"%APPDATA%\npm"), os.path.expanduser("~/.npm-global/bin")):
        for ext in ("", ".cmd", ".ps1"):
            p = os.path.join(base, f"opencli{ext}")
            if os.path.isfile(p):
                return p
    return "opencli"


def _opencli_env() -> dict:
    # opencli talks to a local extension bridge; proxies break it.
    return {**os.environ, "NO_PROXY": "*", "ALL_PROXY": "",
            "HTTP_PROXY": "", "HTTPS_PROXY": ""}


def opencli_eval(js: str, timeout: int = EVAL_TIMEOUT, retries: int = 2) -> str | None:
    """Run JS in the bound browser page and return stdout.

    Retries on timeout/failure: evals can hang or hiccup when the SPA
    is busy re-rendering.
    """
    opencli = find_opencli()
    last_err = ""
    for attempt in range(retries + 1):
        try:
            result = subprocess.run(
                [opencli, "browser", "default", "eval", js],
                capture_output=True, text=True, timeout=timeout, encoding="utf-8",
                env=_opencli_env())
            if result.returncode == 0:
                return result.stdout
            last_err = (result.stderr or result.stdout or "").strip()[:300]
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {timeout}s"
        except Exception as e:
            last_err = str(e)
        if attempt < retries:
            time.sleep(1.5)
    if last_err:
        print(f"  opencli eval error: {last_err}", file=sys.stderr)
    return None


def ensure_page() -> bool:
    """Make sure the browser is on the Lingshu skill page and authenticated."""
    # Check current location first
    cur = opencli_eval("location.href", timeout=15)
    if cur and "lingshu-agent-alpha" in cur:
        # Verify session: cftk cookie present?
        has_tk = opencli_eval(
            "document.cookie.split('; ').some(function(c){return c.indexOf('cftk=')===0})",
            timeout=15)
        if has_tk and has_tk.strip() == "true":
            return True
    # Navigate (open also binds/creates the session tab)
    opencli = find_opencli()
    try:
        subprocess.run(
            [opencli, "browser", "default", "open", LINGSHU_URL],
            capture_output=True, text=True, timeout=30, encoding="utf-8",
            env=_opencli_env())
    except Exception as e:
        print(f"  opencli open error: {e}", file=sys.stderr)
        return False
    for _ in range(10):
        time.sleep(2)
        has_tk = opencli_eval(
            "document.cookie.split('; ').some(function(c){return c.indexOf('cftk=')===0})",
            timeout=15)
        if has_tk and has_tk.strip() == "true":
            return True
    print("error: Lingshu page did not come up with a session "
          "(cftk cookie missing). Log into cloudscope.ulanqab.huawei.com "
          "in Chrome and retry.", file=sys.stderr)
    return False


# ---------------------------------------------------------------------------
# Page-context fetch helper. All API calls run as fetch() inside the page so
# cookies + Cftk header are applied. Results are stashed on window and read
# back in a second eval (avoids huge return values / quoting issues).
# ---------------------------------------------------------------------------

_FETCH_JS_TEMPLATE = (
    "(function(){{"
    "var tk=(document.cookie.split('; ').find(function(c){{return c.indexOf('cftk=')===0}})||'=').split('=').slice(1).join('=');"
    "var url={url!r};"
    "var opts={{credentials:'include',headers:{{'Accept':'application/json, text/plain, */*','Cftk':tk}}}};"
    "{extra}"
    "return fetch(url,opts).then(function(r){{"
    "return r.text().then(function(t){{"
    "window.__crawlResult={{status:r.status,body:t}};"
    "return 'OK';"
    "}});"
    "}}).catch(function(e){{"
    "window.__crawlResult={{status:0,body:'ERR:'+e.message}};"
    "return 'ERR';"
    "}});"
    "}})()"
)


def page_fetch(path: str, method: str = "GET", body: dict | None = None,
               as_blob_b64: bool = False) -> tuple[int, str] | None:
    """Fetch an API path in page context. Returns (status, body-text).

    For binary (zip) responses set as_blob_b64=True — the body is returned
    base64-encoded so it survives the eval round-trip.
    """
    if as_blob_b64:
        # Blob chain: read the response as a data URL, keep the base64 part.
        tail = (
            "return fetch(url,opts).then(function(r){"
            "return r.blob().then(function(b){"
            "return new Promise(function(res){"
            "var fr=new FileReader();"
            "fr.onload=function(){"
            "window.__crawlResult={status:r.status,body:(fr.result.split(',')[1]||''),isB64:true};"
            "res('OK');"
            "};"
            "fr.readAsDataURL(b);"
            "});"
            "});"
            "}).catch(function(e){"
            "window.__crawlResult={status:0,body:'ERR:'+e.message};"
            "return 'ERR';"
            "});"
        )
        js = _FETCH_JS_TEMPLATE.format(
            url=API_BASE + path, extra="").replace(
            "return fetch(url,opts).then(function(r){return r.text().then(function(t){window.__crawlResult={status:r.status,body:t};return 'OK';});}).catch(function(e){window.__crawlResult={status:0,body:'ERR:'+e.message};return 'ERR';});",
            tail)
    else:
        extra = ""
        if method == "POST":
            extra = ("opts.method='POST';"
                     "opts.headers['Content-Type']='application/json';"
                     f"opts.body={json.dumps(json.dumps(body or {}))};")
        js = _FETCH_JS_TEMPLATE.format(url=API_BASE + path, extra=extra)

    # Clear any previous result
    opencli_eval("window.__crawlResult=null", timeout=15)

    # Kick off the fetch (returns immediately; result lands on window)
    res = opencli_eval(js)
    if res is None:
        return None
    if res.strip().startswith("ERR"):
        # fetch itself rejected; result already stashed
        got = opencli_eval(
            "window.__crawlResult?window.__crawlResult.body.slice(0,200):''",
            timeout=15)
        print(f"  fetch error: {got}", file=sys.stderr)
        return (0, got or "ERR")

    # Wait for the promise to stash the result (opencli awaits promises, so
    # the kick-off eval usually already resolved it — poll as fallback).
    for _ in range(60):
        got = opencli_eval(
            "window.__crawlResult?'S'+window.__crawlResult.status+'N'+window.__crawlResult.body.length:''",
            timeout=30)
        if got is not None:
            stripped = got.strip()
            if stripped and stripped not in ("SundefinedNundefined", "null"):
                m = re.match(r"S(\d+)N(\d+)", stripped)
                if m:
                    status = int(m.group(1))
                    total_len = int(m.group(2))
                    body = _read_result_body(total_len)
                    if body is None:
                        return None
                    return (status, body)
        time.sleep(1)
    return None


def _read_result_body(total_len: int) -> str | None:
    """Read window.__crawlResult.body in chunks (eval output size limits).

    The eval CLI appends a trailing newline to its output. The body is
    always compact JSON or base64 — neither contains actual newlines —
    so stripping newlines from each chunk is safe.
    """
    CHUNK = 100_000
    parts: list[str] = []
    for off in range(0, max(total_len, 1), CHUNK):
        got = opencli_eval(
            f"window.__crawlResult.body.substr({off},{CHUNK})", timeout=60)
        if got is None:
            return None
        chunk = got.strip("\n")
        if off == 0 and chunk == "" and total_len > 0:
            return None  # read failed / body gone
        parts.append(chunk)
    return "".join(parts)


def list_all_skills(status_filter: str | None) -> list[dict]:
    """Page through the skills list API and return all items."""
    items: list[dict] = []
    offset = 1
    total = None
    while True:
        body = {"keyword": "", "scene": "", "status": "",
                "query_start_time": "", "query_end_time": "",
                "cloudservice_id": "", "skill_level": ""}
        result = page_fetch(
            f"/skills/list?limit={PAGE_SIZE}&offset={offset}&scope=ALL",
            method="POST", body=body)
        if result is None:
            print(f"error: list fetch failed at offset {offset}", file=sys.stderr)
            break
        status, text = result
        if status != 200:
            print(f"error: list API status {status}: {text[:200]}", file=sys.stderr)
            break
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"error: list API returned non-JSON: {text[:200]}", file=sys.stderr)
            break
        payload = data.get("data") or {}
        if total is None:
            total = payload.get("total", 0)
            print(f"Total skills reported by server: {total}")
        page_items = payload.get("items") or []
        items.extend(page_items)
        print(f"  listed {len(items)}/{total} (offset {offset})", end="\r")
        if not page_items or (total and len(items) >= total):
            break
        offset += 1
        time.sleep(0.5)
    print()
    if status_filter:
        status_map = {"published": "PUBLISHED", "approved": "APPROVED"}
        want = status_map.get(status_filter.lower(), status_filter.upper())
        before = len(items)
        items = [i for i in items if i.get("status") == want]
        print(f"  status filter '{want}': {len(items)}/{before} skills kept")
    return items


def pick_version_uuid(item: dict) -> tuple[str | None, str]:
    """Pick the version to download: published first, else current."""
    pub = item.get("published_version_uuid")
    cur = item.get("current_version_uuid")
    if pub:
        return pub, f"{item.get('published_version') or '?'} (published)"
    if cur:
        return cur, f"{item.get('current_version') or '?'} (current)"
    return None, "none"


def download_skill(item: dict, zips_dir: Path) -> dict:
    """Download one skill's zip, save it, return a status record."""
    name = item.get("name") or "unknown"
    uuid = item.get("uuid")
    version_uuid, version_label = pick_version_uuid(item)
    record = {
        "name": name,
        "uuid": uuid,
        "status": item.get("status"),
        "version": version_label,
        "download_status": "skipped",
        "reason": "no downloadable version (pending approval?)",
    }
    if not uuid or not version_uuid:
        return record

    # File name: {name}-{version}.zip
    ver_no = (item.get("published_version") or item.get("current_version")
              or "0.0.0")
    safe_name = re.sub(r'[^\w.-]+', '_', name)
    zip_path = zips_dir / f"{safe_name}-{ver_no}.zip"

    # Skip if already downloaded
    if zip_path.exists() and zip_path.stat().st_size > 0:
        record.update(download_status="skipped",
                      reason="zip already on disk",
                      zip=str(zip_path))
        return record

    result = None
    for attempt in range(1, MAX_RETRIES + 1):
        result = page_fetch(
            f"/skills/{uuid}/download?version_uuid={version_uuid}",
            as_blob_b64=True)
        if result and result[0] == 200:
            break
        if result and result[0] == 404:
            record.update(download_status="failed", reason=f"404 not found",
                          zip=None)
            return record
        print(f"\n  retry {attempt}/{MAX_RETRIES} for {name} "
              f"(status={result[0] if result else 'no-result'})", file=sys.stderr)
        time.sleep(2 * attempt)

    if not result or result[0] != 200:
        record.update(download_status="failed",
                      reason=f"download status {result[0] if result else 'none'}",
                      zip=None)
        return record

    try:
        data = base64.b64decode(result[1])
    except Exception as e:
        record.update(download_status="failed", reason=f"b64 decode: {e}")
        return record

    if len(data) < 4 or data[:2] != b"PK":
        record.update(download_status="failed",
                      reason=f"not a zip ({len(data)} bytes, head={data[:8]!r})")
        return record

    zips_dir.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(data)
    record.update(download_status="downloaded",
                  reason=None,
                  zip=str(zip_path),
                  size=len(data))
    return record


def extract_all(zips_dir: Path, skills_dir: Path, manifest: dict) -> int:
    """Extract downloaded zips into skills_dir. Returns count extracted."""
    count = 0
    for entry in manifest.get("skills", []):
        zip_str = entry.get("zip")
        if entry.get("download_status") != "downloaded" or not zip_str:
            continue
        zip_path = Path(zip_str)
        if not zip_path.exists():
            continue
        try:
            with zipfile.ZipFile(zip_path) as zf:
                # Extract into a folder keyed by the SKILL NAME (from the zip
                # filename), not the zip's internal top-level folder. The
                # platform names some zips' root folder after a shared prefix
                # (e.g. every ldz-self-test-* skill's zip roots at
                # "ldz-self-test"), which silently overwrote one folder per
                # prefix. The zip filename is unique per skill.
                skill_name = re.sub(r"-[\d.]+\.zip$", "", zip_path.name)
                dest = skills_dir / skill_name
                names = zf.namelist()
                if dest.exists():
                    shutil.rmtree(dest)
                dest.mkdir(parents=True, exist_ok=True)
                top = {n.split("/")[0] for n in names if n and not n.endswith("/")}
                if len(top) == 1:
                    # single root folder inside the zip: move its contents up
                    zf.extractall(skills_dir)
                    inner = skills_dir / next(iter(top))
                    if inner != dest:
                        for e in os.listdir(inner):
                            shutil.move(str(inner / e), str(dest / e))
                        shutil.rmtree(inner)
                else:
                    zf.extractall(dest)
                entry["extracted_to"] = str(dest)
                entry["file_count"] = len([n for n in names if not n.endswith("/")])
                count += 1
        except zipfile.BadZipFile:
            entry["download_status"] = "failed"
            entry["reason"] = "bad zip on extraction"
    return count


def write_index(manifest: dict, index_path: Path) -> None:
    """Write a human-readable Markdown index of crawled skills."""
    skills = manifest.get("skills", [])
    by_service: dict[str, int] = {}
    by_scene: dict[str, int] = {}
    for s in skills:
        svc = s.get("cloudservice") or "(none)"
        scene = s.get("scene") or "(none)"
        by_service[svc] = by_service.get(svc, 0) + 1
        by_scene[scene] = by_scene.get(scene, 0) + 1

    lines = [
        "# Lingshu Agent Skills — Crawl Index",
        "",
        f"Crawled at: {manifest.get('crawled_at')}",
        f"Total skills: {len(skills)}",
        "",
        "## By cloud service",
        "",
        "| 云服务 | skills |",
        "|---|---|",
    ]
    for svc, n in sorted(by_service.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {svc} | {n} |")
    lines += ["", "## By scene", "", "| scene | skills |", "|---|---|"]
    for scene, n in sorted(by_scene.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {scene} | {n} |")

    lines += ["", "## All skills", "",
              "| name | 中文名 | 云服务 | scene | level | status | "
              "published | latest | downloaded |", "|---|---|---|---|---|---|---|---|---|"]
    for s in skills:
        lines.append(
            f"| {s.get('name')} | {s.get('name_cn') or ''} | "
            f"{s.get('cloudservice') or ''} | {s.get('scene') or ''} | "
            f"{s.get('skill_level') or ''} | {s.get('status') or ''} | "
            f"{s.get('published_version') or '--'} | "
            f"{s.get('current_version') or '--'} | "
            f"{s.get('download_status')} |")
    lines += [
        "",
        "## Skipped / failed downloads",
        "",
    ]
    skipped = [s for s in skills if s.get("download_status") != "downloaded"]
    if not skipped:
        lines.append("(none — everything downloaded)")
    for s in skipped:
        lines.append(f"- **{s.get('name')}** ({s.get('status')}): "
                     f"{s.get('reason')}")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Crawl Lingshu Agent skills into local zips + folders.")
    p.add_argument("--output", default=None, help="Output directory "
                   f"(default: {OUTPUT_DIR})")
    p.add_argument("--status", default=None,
                   help="Filter by status: published | approved | raw status value")
    p.add_argument("--list-only", action="store_true",
                   help="Only build the manifest + index, no downloads")
    p.add_argument("--refresh", action="store_true",
                   help="Delete manifest and re-crawl everything")
    p.add_argument("--limit", type=int, default=None,
                   help="Download at most N skills (debug)")
    args = p.parse_args(argv)

    out = Path(args.output or OUTPUT_DIR)
    out.mkdir(parents=True, exist_ok=True)
    zips_dir = out / "zips"
    skills_dir = out / "skills"
    manifest_path = out / "manifest.json"
    index_path = out / "index.md"

    if args.refresh and manifest_path.exists():
        manifest_path.unlink()
        print("Deleted manifest (refresh)")

    manifest: dict = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            print(f"Loaded existing manifest: "
                  f"{len(manifest.get('skills', []))} skills")
        except (json.JSONDecodeError, OSError):
            manifest = {}

    print("Checking browser session...")
    if not ensure_page():
        return 1

    print("Listing skills...")
    items = list_all_skills(args.status)
    if not items:
        print("error: no skills listed", file=sys.stderr)
        return 1

    # Merge list results into the manifest (keyed by uuid)
    prev = {s.get("uuid"): s for s in manifest.get("skills", [])}
    merged: list[dict] = []
    for item in items:
        rec = dict(item)  # fresh metadata from the list API
        rec["cloudservice"] = item.get("cloudservice_name")
        old = prev.get(item.get("uuid"))
        if old:
            # keep download bookkeeping
            for k in ("download_status", "reason", "zip", "size",
                      "extracted_to", "file_count"):
                if old.get(k) is not None:
                    rec[k] = old[k]
        merged.append(rec)

    # carry over skills from previous crawls no longer in the list
    seen = {s.get("uuid") for s in merged}
    for old in prev.values():
        if old.get("uuid") not in seen:
            merged.append(old)

    manifest = {
        "crawled_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "count": len(merged),
        "skills": merged,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Manifest saved: {manifest_path} ({len(merged)} skills)")

    if args.list_only:
        write_index(manifest, index_path)
        print(f"Index written: {index_path}")
        return 0

    # A skill is stale if never downloaded, or if the zip on disk predates the
    # version the manifest now reports (published/current changed since the
    # last crawl). The merge step above intentionally preserves bookkeeping,
    # so the version comparison happens here.
    def _is_stale(s: dict) -> bool:
        if s.get("download_status") != "downloaded":
            return True
        zip_path = s.get("zip")
        if not zip_path or not os.path.exists(zip_path):
            return True
        base = os.path.basename(zip_path)
        m = re.search(r"-([\d.]+)\.zip$", base)
        if not m:
            return True
        cur = str(s.get("published_version")
                  or s.get("current_version") or "")
        return bool(cur) and m.group(1) != cur

    todo = [s for s in merged if _is_stale(s)]
    if args.limit:
        todo = todo[:args.limit]
    print(f"\nDownloading {len(todo)} skill(s)...")
    done = failed = skipped = 0
    for i, s in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {s.get('name')} "
              f"({s.get('status')}, v{s.get('current_version')})")
        rec = download_skill(s, zips_dir)
        s.update(rec)
        if rec["download_status"] == "downloaded":
            done += 1
        elif rec["download_status"] == "failed":
            failed += 1
            print(f"  FAILED: {rec.get('reason')}", file=sys.stderr)
        else:
            skipped += 1
            print(f"  skipped: {rec.get('reason')}")
        # Persist after each skill so a crash/resume keeps progress
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8")
        if i < len(todo):
            time.sleep(DOWNLOAD_DELAY)

    print(f"\nExtracting zips...")
    extracted = extract_all(zips_dir, skills_dir, manifest)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    write_index(manifest, index_path)

    print(f"\n{'=' * 60}")
    print(f"Summary: {done} downloaded, {skipped} skipped, {failed} failed, "
          f"{extracted} extracted")
    print(f"Output:  {out}")
    print(f"Index:   {index_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
