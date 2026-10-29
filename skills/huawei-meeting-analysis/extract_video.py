#!/usr/bin/env python3
"""Extract (download) a Huawei eMeeting recording video from its w3.huawei.com URL.

Usage (run from inside an `opencli browser <name> open "<emeeting-url>"` session —
session cookies are required, this script shells out to opencli):

    opencli browser emeeting open "<url>" --window background
    python extract_video.py <browser-name> <emeeting-url> "<out-dir>" [--quality Extreme]

Pipeline (validated 2026-10-28 on the 3-hour 变更观摩 recording):
  1. getCloudRecord API  → record metadata: quality tiers, videoId, fileSize.
     Tiers seen: Extreme(40) > High(22) > Medium(28) > Low(34) > Audio.
  2. Fetch chosen tier's .m3u8 playlist (AES-128 tagged, absolute segment URLs).
  3. Download every .ts segment through `opencli eval` fetch(base64) — the
     segments/key live on imss-video.huawei.com and need the browser session.
  4. Fetch the AES-128 key (16 bytes) the same way.
  5. openssl enc -aes-128-cbc -d -nopad each segment (IV from playlist tag,
     media-sequence fallback; TS sync 0x47 check).
  6. ffmpeg concat → single mp4 (faststart).

Outputs into <out-dir>:
  record_meta.json     quality tiers + metadata
  playlist_<tier>.m3u8 the playlist text
  segs/NNNNN.ts        raw encrypted segments (resumable: kept on re-run)
  segs_dec/NNNNN.ts    decrypted segments
  <basename>.mp4       the final video

Notes:
  - AES key URL comes from the playlist tag; IV likewise (all-zero observed,
    media-sequence fallback per RFC 8216 when absent).
  - Decryption uses Git-for-Windows openssl (C:\\Program Files\\Git\\usr\\bin\\openssl.exe).
  - ffmpeg: Gyan full build via winget, or any ffmpeg on PATH.
  - opencli eval returns base64 via chunked String.fromCharCode (32 KB chunks).
  - Measured pace: ~10 s/segment via opencli — a 3 h meeting ≈ 3.5-4 h at best
    tier. Run in background and report ETA, or --quality High for ~2-3x faster
    download. Batch-fetching multiple segments per eval call is the future
    4-5x speedup.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import time
from pathlib import Path

OPENSSL = r"C:\Program Files\Git\usr\bin\openssl.exe"


def opencli(browser: str, *args: str, timeout: int = 180) -> str:
    exe = _which_opencli()
    p = subprocess.run([exe, "browser", browser, *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(f"opencli {' '.join(args)} failed: {p.stderr[:300]}")
    return p.stdout


def _which_opencli() -> str:
    exe = "opencli"
    for cand in (r"C:\Users\b00563677\AppData\Roaming\npm\opencli.cmd",):
        if Path(cand).exists():
            return cand
    return exe


def find_ffmpeg() -> str:
    winget = (r"C:\Users\b00563677\AppData\Local\Microsoft\WinGet\Packages"
              r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
              r"\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe")
    if Path(winget).exists():
        return winget
    return "ffmpeg"  # hope PATH has it


def browser_fetch_b64(browser: str, url: str, retries: int = 4) -> bytes:
    """fetch(url) inside the opencli page context; returns response body bytes."""
    js = ("(async()=>{const r=await fetch(%r,{credentials:'include'});"
          "if(!r.ok)return 'ERR '+r.status;"
          "const b=await r.arrayBuffer();"
          "let s='';const u=new Uint8Array(b);"
          "for(let i=0;i<u.length;i+=32768){s+=String.fromCharCode.apply(null,u.subarray(i,i+32768));}"
          "return btoa(s)})()") % url
    for attempt in range(retries):
        out = opencli(browser, "eval", js, timeout=180).strip()
        if out.startswith("ERR 40"):
            raise RuntimeError(
                f"session rejected ({out}) — re-open: opencli browser {browser} "
                f'open "<meeting-url>"')
        if out and not out.startswith("ERR"):
            try:
                return base64.b64decode(out)
            except Exception:
                pass
        time.sleep(2 + attempt * 3)
    raise RuntimeError(f"fetch failed after {retries} tries: {url[:120]}")


def get_record_meta(browser: str, emeeting_url: str) -> dict:
    """Record id = the 32-hex id in the AI-summary URL."""
    m = re.search(r"/aiSummary/([0-9A-Fa-f]{32})", emeeting_url)
    if not m:
        sys.exit(f"Cannot find record id in URL: {emeeting_url}")
    rid = m.group(1)
    api = (f"https://w3.huawei.com/emeeting/server/api/weteam/meeting/v1/"
           f"getCloudRecord/{rid}?_t={int(time.time()*1000)}")
    raw = browser_fetch_b64(browser, api)
    meta = json.loads(raw.decode("utf-8"))
    if meta.get("code") != 200 or not meta.get("response"):
        sys.exit(f"getCloudRecord failed: {str(meta)[:300]}")
    return meta["response"]


def pick_record(records: list, index: int) -> dict:
    if index >= len(records):
        sys.exit(f"record index {index} >= {len(records)} records")
    return records[index]


def tier_url(rec: dict, quality: str) -> tuple[str, str]:
    """Return (tier, m3u8 url) for the requested quality (highest available
    at/under the request: Extreme > High > Medium > Low)."""
    order = ["Extreme", "High", "Medium", "Low"]
    tiers = {v.get("type"): v.get("url") for v in rec.get("videoRes", [])}
    if quality == "best":
        for t in order:
            if tiers.get(t):
                return t, tiers[t]
        sys.exit(f"No video tier found. Available: {list(tiers)}")
    if not tiers.get(quality):
        sys.exit(f"Tier {quality} not available. Have: {list(tiers)}")
    return quality, tiers[quality]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("browser", help="opencli browser session name")
    ap.add_argument("url", help="emeeting AI-summary URL")
    ap.add_argument("out", help="output directory")
    ap.add_argument("--quality", default="best",
                    help="Extreme/High/Medium/Low or 'best' (default)")
    ap.add_argument("--record-index", type=int, default=0,
                    help="which recording when a meeting has several (default 0)")
    ap.add_argument("--skip-decrypt", action="store_true",
                    help="stop after downloading segments")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    segs = out / "segs"
    segs.mkdir(exist_ok=True)

    # Resume cache is keyed to this recording — refuse a reused out-dir for a
    # different meeting (stale playlist/key/segments would silently mix).
    rm = re.search(r"/aiSummary/([0-9A-Fa-f]{32})", args.url)
    if not rm:
        sys.exit(f"Cannot find record id in URL: {args.url}")
    rid = rm.group(1)
    marker = out / "record_id.txt"
    if marker.exists() and marker.read_text(encoding="utf-8").strip() != rid:
        sys.exit(f"out-dir holds a different recording "
                 f"({marker.read_text(encoding='utf-8').strip()} != {rid}); "
                 f"use a fresh --out")
    marker.write_text(rid, encoding="utf-8")

    # 1. metadata
    meta_path = out / "record_meta.json"
    if meta_path.exists():
        records = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        records = get_record_meta(args.browser, args.url)
        meta_path.write_text(json.dumps(records, ensure_ascii=False, indent=1),
                             encoding="utf-8")
    rec = pick_record(records, args.record_index)
    print(f"record: {rec.get('fileName')} | {rec.get('duration', 0)//60} min | "
          f"{rec.get('fileSize')} | {rec.get('recordType')}")

    # 2. playlist
    tier, m3u8 = tier_url(rec, args.quality)
    pl_path = out / f"playlist_{tier}.m3u8"
    if not pl_path.exists():
        pl_path.write_bytes(browser_fetch_b64(args.browser, m3u8))
    playlist = pl_path.read_text(encoding="utf-8")
    urls = [l.strip() for l in playlist.splitlines()
            if ".ts" in l and not l.startswith("#")]
    print(f"tier={tier} segments={len(urls)}")

    # key
    km = re.search(r'URI="([^"]+)"', playlist)
    if not km:
        sys.exit("No AES key URI in playlist (maybe unencrypted?)")
    key_path = out / "key_b64.txt"
    if not key_path.exists():
        key_path.write_text(base64.b64encode(
            browser_fetch_b64(args.browser, km.group(1))).decode())
    key_hex = base64.b64decode(key_path.read_text().strip()).hex()
    print(f"key {key_hex[:8]}… fetched")

    # 3. segments (resumable)
    t0 = time.time()
    miss = []
    for i, u in enumerate(urls):
        dst = segs / f"{i:05d}.ts"
        if dst.exists() and dst.stat().st_size > 0:
            continue
        try:
            data = browser_fetch_b64(args.browser, u)
        except RuntimeError as e:
            miss.append(i)
            print(f"[{i+1}/{len(urls)}] MISS: {e}", flush=True)
            continue
        if len(data) < 100:  # tiny final segment is valid; 0x47 check validates
            miss.append(i)
            continue
        dst.write_bytes(data)
        if (i + 1) % 25 == 0:
            el = time.time() - t0
            print(f"[{i+1}/{len(urls)}] ({el/60:.1f} min)", flush=True)
    have = sum(1 for u2 in segs.glob("*.ts"))
    print(f"segments on disk: {have}/{len(urls)} missing={len(miss)}")
    if miss:
        (out / "missing_segments.txt").write_text(
            "\n".join(map(str, miss)), encoding="utf-8")
        sys.exit(f"{len(miss)} segments missing — re-run to resume")
    if args.skip_decrypt:
        return

    # 4. decrypt (AES-128-CBC; IV from playlist, else per-segment media-sequence
    #    IV per RFC 8216; TS sync byte check)
    dec = out / "segs_dec"
    dec.mkdir(exist_ok=True)
    ivm = re.search(r'IV=0x([0-9a-fA-F]+)', playlist)
    iv_hex = ivm.group(1).lower().zfill(32) if ivm else None
    bad = 0
    for i in range(len(urls)):
        src = segs / f"{i:05d}.ts"
        dst = dec / f"{i:05d}.ts"
        if dst.exists() and dst.stat().st_size > 0:
            continue
        data = src.read_bytes()
        n = len(data) - (len(data) % 16)
        p = subprocess.run([OPENSSL, "enc", "-aes-128-cbc", "-d", "-nopad",
                            "-K", key_hex, "-iv", iv_hex or f"{i:032x}"],
                           input=data[:n], capture_output=True)
        if not p.stdout or p.stdout[0] != 0x47:
            bad += 1
            if bad <= 3:
                print(f"DEC-BAD {src.name}", flush=True)
            continue
        dst.write_bytes(p.stdout)
    print(f"decrypted {sum(1 for _ in dec.glob('*.ts'))}/{len(urls)} bad={bad}")

    # 5. concat + remux (gate: every segment must have decrypted)
    for i in range(len(urls)):
        if not (dec / f"{i:05d}.ts").exists():
            sys.exit(f"decrypted segment {i:05d}.ts missing — re-run to resume")
    ff = find_ffmpeg()
    concat = dec / "concat.txt"
    with open(concat, "w", encoding="utf-8") as f:
        for i in range(len(urls)):
            f.write(f"file '{i:05d}.ts'\n")  # relative: cwd=dec avoids
            # non-ASCII absolute-path issues in ffmpeg concat on Windows
    merged = dec / "merged.ts"
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c", "copy", str(merged)],
                   cwd=str(dec), check=True)
    base = re.sub(r'[\\/:*?"<>|]', "_", str(rec.get("fileName") or "meeting"))
    final = out / f"{base}.mp4"
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(merged),
                    "-c", "copy", "-movflags", "+faststart", str(final)],
                   check=True)

    # 6. verify duration against record metadata, then drop the intermediate
    probe = ff.replace("ffmpeg.exe", "ffprobe.exe")
    q = subprocess.run([probe, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(final)],
                       capture_output=True, text=True)
    try:
        dur = float(q.stdout.strip())
    except ValueError:
        sys.exit(f"ffprobe could not read duration (output {q.stdout!r}) — "
                 f"the mp4 may be corrupt")
    expected = rec.get("duration")
    if expected and abs(dur - expected) > 120:
        sys.exit(f"duration mismatch: got {dur:.0f}s, expected {expected}s — "
                 f"merge incomplete?")
    merged.unlink()
    print(f"DONE: {final} ({final.stat().st_size // (1024*1024)} MB, "
          f"{dur/60:.0f} min)")


if __name__ == "__main__":
    main()
