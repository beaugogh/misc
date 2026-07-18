#!/usr/bin/env python3
"""Generate images via the chatgpt.com web interface using OpenCLI.

Drives your logged-in chatgpt.com Chrome session through OpenCLI's
`chatgpt image` command, which sends each prompt as a conversation and
scrapes the rendered image from the DOM. The conversation path streams
immediately, so it is NOT subject to the ~190s response-start cap that the
codex /images/generations API endpoint imposes — long/multi-human prompts
that time out via the API succeed here.

When a prompt is blocked by ChatGPT's third-party-content-similarity
moderation, this script detects the placeholder image ChatGPT leaves behind,
retries by asking ChatGPT (in a fresh chat) to rephrase-and-generate, and
tries again — up to N retries.

Input: one or more textual prompts. NOT bound to any file format — accept:
  --prompt "..."            a single prompt
  --prompts-file FILE       one prompt per line; blank lines and lines
                            starting with '#' are ignored; multi-line prompts
                            can be given as blocks separated by a blank line
  --prompts-json '["...", "..."]'  or a path to a JSON file holding an array
  (or pass a file path as the single positional arg = alias for --prompts-file)

Output: PNGs in --out (default ./out), named <prefix>_<n>.<ext> where <n> is
the 1-based index and <prefix> defaults to "image". Existing files with the
generated index are skipped unless --force is passed.

Prerequisites (one-time, interactive — see SKILL.md):
  - opencli installed and on PATH (npm install -g @jackwener/opencli)
  - OpenCLI Browser Bridge extension connected in Chrome (opencli doctor)
  - logged into chatgpt.com in that Chrome profile

Usage:
    python3 generate.py --prompt "Generate an image of a red cube on white."
    python3 generate.py --prompts-file prompts.txt --out ./out --retries 3
    python3 generate.py --prompts-json '["prompt A", "prompt B"]'
    python3 generate.py prompts.txt            # positional = prompts-file
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time

OPENCLI = "opencli"

# Fresh-chat rephrase-and-generate wrapper. Each retry sends this as the image
# prompt to a NEW chat: ChatGPT rephrases to dodge third-party-content-
# similarity and generates the image in one turn. The original prompt is
# embedded so the rephrase stays faithful to scene/characters/style.
# (The real block signal is the placeholder image detected by is_real_image();
# we don't parse the assistant's refusal text — a placeholder image is a
# more reliable signal than its wording, which varies by locale and model.)
REPHRASE_PROMPT = (
    "The following image-generation prompt was blocked by ChatGPT's "
    "third-party-content-similarity moderation:\n\n"
    "{prompt}\n\n"
    "Please rephrase this prompt to avoid any third-party-content-similarity "
    "issues (remove character names, franchise terms, and distinctive "
    "trademarked features) while preserving the scene composition, the "
    "characters' general appearance and roles, and the original illustration "
    "style. Then generate the image from the rephrased prompt."
)


def find_opencli() -> str:
    path = shutil.which(OPENCLI)
    if not path:
        raise SystemExit(
            "`opencli` not found on PATH. Install with "
            "`sudo npm install -g @jackwener/opencli`, install the Browser "
            "Bridge extension in Chrome, and run `opencli doctor`. See SKILL.md."
        )
    return path


def is_real_image(path: str) -> bool:
    """True if the saved PNG is a genuine generated image, not ChatGPT's
    'generating…' placeholder or a blank.

    ChatGPT real outputs: color_type 2 (RGB, no alpha), >=1254x1254, >2MB.
    Placeholder seen: color_type 6 (RGBA), 960x960, ~40KB.
    Discriminate on structural PNG-header fields, not pixel content, so it
    survives changes to the placeholder's exact bytes.
    """
    try:
        data = open(path, "rb").read(33)
    except OSError:
        return False
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    if len(data) < 33 or data[12:16] != b"IHDR":
        return False
    width, height, _bd, color_type = struct.unpack(">IIBB", data[16:26])
    size = os.path.getsize(path)
    return (color_type == 2           # RGB, no alpha (placeholder is RGBA=6)
            and width >= 1024
            and height >= 1024
            and size > 500_000)


def load_prompts(args) -> list[str]:
    """Collect prompts from the CLI sources, in order. Errors out if none."""
    prompts: list[str] = []

    if args.prompt:
        prompts.append(args.prompt.strip())

    if args.prompts_json:
        prompts.extend(_load_json_prompts(args.prompts_json))

    if args.prompts_file:
        prompts.extend(_load_text_prompts(args.prompts_file))

    # positional alias for --prompts-file
    if args.file:
        prompts.extend(_load_text_prompts(args.file))

    prompts = [p for p in prompts if p and p.strip()]
    if not prompts:
        raise SystemExit(
            "No prompts provided. Pass --prompt, --prompts-file, "
            "--prompts-json, or a positional file path. See --help."
        )
    return prompts


def _load_json_prompts(spec: str) -> list[str]:
    """spec is either a JSON array literal or a path to a .json file."""
    if os.path.exists(spec):
        arr = json.loads(open(spec, encoding="utf-8").read())
    else:
        arr = json.loads(spec)
    if not isinstance(arr, list):
        raise SystemExit(f"--prompts-json must be a JSON array, got {type(arr).__name__}")
    return [str(p).strip() for p in arr if str(p).strip()]


def _load_text_prompts(path: str) -> list[str]:
    """One prompt per line; '#' comments ignored; multi-line prompts as
    blank-line-separated blocks."""
    raw = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n\s*\n", raw)
    out: list[str] = []
    for block in blocks:
        lines = [ln for ln in block.splitlines()
                 if ln.strip() and not ln.strip().startswith("#")]
        if lines:
            out.append("\n".join(ln.strip() for ln in lines).strip())
    return out


def run(cmd: list[str], timeout: int) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout + 60)
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def latest_file(d: str) -> str | None:
    entries = [os.path.join(d, f) for f in os.listdir(d)
               if os.path.isfile(os.path.join(d, f))]
    return max(entries, key=os.path.getmtime) if entries else None


def extract_json_field(blob: str, field: str) -> str | None:
    """Pull a field value from opencli -f json output."""
    for chunk in _json_objects(blob):
        try:
            obj = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, list):
            for row in obj:
                if isinstance(row, dict) and row.get(field):
                    return str(row[field])
        elif isinstance(obj, dict) and obj.get(field):
            return str(obj[field])
    # Fallback: plain `field: value`
    m = re.search(rf"^\s*{re.escape(field)}\s*:\s*(.+?)(?=\n\s*\w+:|\Z)",
                  blob, re.S | re.M)
    return m.group(1).strip() if m else None


def _json_objects(blob: str):
    depth = 0
    start = None
    for i, ch in enumerate(blob):
        if ch in "{[":
            if depth == 0:
                start = i
            depth += 1
        elif ch in "}]":
            depth -= 1
            if depth == 0 and start is not None:
                yield blob[start:i + 1]
                start = None


def opencli_image(opencli: str, prompt: str, out_dir: str,
                  timeout: int) -> tuple[bool, str | None, str]:
    """Run `opencli chatgpt image`. Returns (real_image_saved, path, conv_url)."""
    cmd = [opencli, "chatgpt", "image", prompt,
           "--op", out_dir, "--timeout", str(timeout),
           "-f", "json", "--window", "background"]
    code, out, err = run(cmd, timeout)
    saved = latest_file(out_dir)
    conv = extract_json_field((out or "") + (err or ""), "link") or ""
    if code == 0 and saved and is_real_image(saved):
        return True, saved, conv
    return False, saved, conv


# JS used by capture_from_conversation: find the large generated <img> and
# fetch it as a data URL. Matches chatgpt.com's estuary/content image src.
CAPTURE_JS = r"""
(async () => {
  const large = Array.from(document.querySelectorAll('img')).filter(i => {
    const r = i.getBoundingClientRect();
    return r.width > 32 && r.height > 32 && (i.naturalWidth || i.width || 0) >= 1024;
  });
  if (!large.length) return { error: 'no_large_img' };
  const img = large[0];
  const src = img.currentSrc || img.src;
  try {
    const res = await fetch(src, { credentials: 'include' });
    if (!res.ok) return { error: 'fetch_' + res.status };
    const blob = await res.blob();
    return await new Promise(resolve => {
      const r = new FileReader();
      r.onloadend = () => resolve({ dataUrl: String(r.result || ''),
                                    mime: blob.type,
                                    w: img.naturalWidth, h: img.naturalHeight });
      r.readAsDataURL(blob);
    });
  } catch (e) { return { error: String(e) }; }
})()
"""


def _normalize_link(link: str) -> str:
    """Strip opencli's emoji prefix from a 'link' field value."""
    return (link or "").replace("\U0001f517", "").strip()


def _parse_json_from_blob(blob: str):
    """Find and parse the first JSON object/array in a blob of text."""
    for i, ch in enumerate(blob):
        if ch in "{[":
            depth = 0
            for j in range(i, len(blob)):
                if blob[j] in "{[":
                    depth += 1
                elif blob[j] in "}]":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(blob[i:j + 1])
                        except json.JSONDecodeError:
                            return None
            break
    return None


def capture_from_conversation(opencli: str, conv_url: str, out_path: str,
                               timeout: int = 240) -> tuple[str, str | None]:
    """Capture the generated image from a chatgpt.com/c/<id> conversation,
    waiting out ChatGPT's "generating…" grey-dots placeholder.

    ChatGPT shows an animated grey-dots placeholder while the image generates
    — which can persist arbitrarily long, AND (a website quirk) can stay
    animating even after the backend has finished, until the page is refreshed.
    So this polls the conversation state and refreshes periodically to unstick
    the placeholder. Only once the real <img> replaces the placeholder does it
    fetch+save the image.

    Returns (status, saved_path) where status is one of:
      - "image"   : a real image was captured and saved to out_path.
      - "refused" : the assistant's turn is a moderation-refusal text (no
                    image will ever appear here) — caller should rephrase.
      - "timeout" : neither resolved within the budget — unknown state.
    """
    conv_url = _normalize_link(conv_url)
    if not conv_url or "/c/" not in conv_url:
        return "timeout", None
    run([opencli, "browser", "chatgpt", "open", conv_url,
         "--window", "background"], 60)

    deadline = time.time() + timeout
    last_refresh = time.time()
    refresh_every = 45   # defeat the stuck-placeholder quirk
    while time.time() < deadline:
        code, out, err = run([opencli, "browser", "chatgpt", "eval",
                              STATE_JS, "--window", "background"], 30)
        res = _parse_json_from_blob((out or "") + (err or ""))
        if not isinstance(res, dict):
            time.sleep(5)
            continue
        if res.get("largeImgs", 0) >= 1:
            code, out, err = run([opencli, "browser", "chatgpt", "eval",
                                  CAPTURE_JS, "--window", "background"], 30)
            fres = _parse_json_from_blob((out or "") + (err or ""))
            if isinstance(fres, dict) and fres.get("dataUrl"):
                b64 = fres["dataUrl"].split(",", 1)[1]
                data = base64.b64decode(b64)
                with open(out_path, "wb") as fh:
                    fh.write(data)
                return "image", out_path
            # fetch failed; keep polling
        elif res.get("refused"):
            return "refused", None
        # else: still generating (grey-dots) OR page not hydrated. Wait, and
        # periodically refresh to unstick the stuck-placeholder quirk.
        if time.time() - last_refresh >= refresh_every:
            run([opencli, "browser", "chatgpt", "open", conv_url,
                 "--window", "background"], 60)
            last_refresh = time.time()
        time.sleep(5)
    return "timeout", None


# State probe: classifies the conversation DOM into image-present / refused /
# still-generating. (No fetch — cheap to poll.)
STATE_JS = r"""
(() => {
  const turns = document.querySelectorAll('[data-message-author-role], article[data-testid*="conversation-turn"]').length;
  const large = Array.from(document.querySelectorAll('img')).filter(i => (i.naturalWidth || i.width || 0) >= 1024);
  const asst = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
  const asstText = asst.map(n => (n.innerText||'')).join('\n').slice(0, 400);
  const refused = /违反|限制|moderation|violate|may have|抱歉|无法|policy|sorry, i can|content policy/i.test(asstText);
  return { turns, largeImgs: large.length, refused, asstText: asstText.slice(0,80) };
})()
"""


def generate_one(opencli: str, prompt: str, retries: int,
                 timeout: int, log) -> tuple[bool, str | None, str | None]:
    """Generate one real image, with delayed-capture + moderation rephrase.

    Per attempt (fresh chat each time):
      1. `opencli chatgpt image` — if it saves a real image, done.
      2. If opencli returns no/placeholder image BUT captured a real
         `/c/<id>` conversation link → the generation likely finished after
         opencli's internal poll gave up (EMPTY_RESULT). Delayed-capture:
         navigate to that conversation and fetch the large <img> via
         `opencli browser eval`. Rescues slow generations without re-running.
      3. If delayed-capture finds no <img> → genuine moderation refusal →
         rephrase on the next attempt (up to `retries` rephrasings).

    Attempt 1 uses the original prompt; attempts 2..retries+1 wrap the
    original in REPHRASE_PROMPT (ChatGPT rephrases to dodge IP signals and
    generates in one turn).

    Returns (success, temp_png_path, conv_url) — caller copies then unlinks
    the temp; conv_url is the chatgpt.com/c/<id> for the successful attempt
    (None if not captured), so the caller can write a .url sidecar for
    recovery.
    """
    scratch_root = tempfile.mkdtemp(prefix="opencli_out_")
    try:
        current_prompt = prompt
        phase = "original"
        for attempt in range(1, retries + 2):
            scratch = os.path.join(scratch_root, f"a{attempt}")
            os.makedirs(scratch, exist_ok=True)
            log(f"  attempt {attempt}/{retries+1} ({phase}): image gen "
                f"({len(current_prompt)} chars)")
            ok, saved, conv = opencli_image(opencli, current_prompt,
                                           scratch, timeout)
            if ok and saved:
                final = tempfile.NamedTemporaryFile(
                    prefix="realimg_", suffix=".png", delete=False).name
                shutil.move(saved, final)
                return True, final, conv

            # opencli didn't save a real image. If it captured a real
            # /c/<id> conversation link, the generation is likely still
            # running (or finished-but-placeholder-stuck). Wait it out:
            # poll the conversation, refreshing to unstick the placeholder,
            # until the real image appears or the assistant refuses.
            conv_norm = _normalize_link(conv)
            if conv_norm and "/c/" in conv_norm:
                log(f"  attempt {attempt}: opencli returned no image — "
                    f"waiting out the generation at {conv_norm}")
                cap_path = os.path.join(scratch_root, f"cap_{attempt}.png")
                status, cap_saved = capture_from_conversation(
                    opencli, conv_norm, cap_path)
                if status == "image" and cap_saved and is_real_image(cap_saved):
                    final = tempfile.NamedTemporaryFile(
                        prefix="realimg_", suffix=".png", delete=False).name
                    shutil.move(cap_saved, final)
                    return True, final, conv_norm
                log(f"  attempt {attempt}: capture → {status}; "
                    f"{'rephrasing' if attempt <= retries else 'giving up'}")
            else:
                log(f"  attempt {attempt}: no image and no conversation "
                    f"link (cold-session/early-exit) → "
                    f"{'rephrase' if attempt <= retries else 'give up'}")

            if attempt > retries:
                log(f"  attempt {attempt}: no real image after "
                    f"{retries+1} attempts; giving up")
                return False, None, None
            phase = "rephrase"
            current_prompt = REPHRASE_PROMPT.format(prompt=prompt)
            time.sleep(5)
        return False, None, None
    finally:
        shutil.rmtree(scratch_root, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", default=None,
                    help="path to a prompts file (alias for --prompts-file)")
    ap.add_argument("--prompt", default=None,
                    help="a single prompt (repeatable? no — use the file/json "
                         "sources for multiple)")
    ap.add_argument("--prompts-file", default=None,
                    help="file with one prompt per line (blank-line-separated "
                         "blocks = multi-line prompts); '#' lines ignored")
    ap.add_argument("--prompts-json", default=None,
                    help="JSON array literal, or path to a .json array file")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "out"),
                    help="output directory (default: ./out next to this script)")
    ap.add_argument("--prefix", default="image",
                    help="output filename prefix (default: image → image_1.png)")
    ap.add_argument("--timeout", type=int, default=300,
                    help="per-image wall seconds passed to opencli (default 300)")
    ap.add_argument("--retries", type=int, default=3,
                    help="moderation rephrase attempts (total attempts = +1)")
    ap.add_argument("--force", action="store_true",
                    help="regenerate even if the output PNG already exists")
    args = ap.parse_args()

    opencli = find_opencli()
    prompts = load_prompts(args)
    os.makedirs(args.out, exist_ok=True)

    def log(msg: str) -> None:
        print(msg, flush=True)

    print(f"{len(prompts)} prompt(s) → {args.out}")
    print(f"via: {opencli} chatgpt image (timeout {args.timeout}s, "
          f"retries {args.retries}, prefix '{args.prefix}_<n>.png')")
    print()

    ok = fail = skipped = 0
    failed_idx: list[int] = []
    for idx, prompt in enumerate(prompts, 1):
        target = os.path.join(args.out, f"{args.prefix}_{idx}.png")
        prefix = f"[{idx}/{len(prompts)}] {os.path.basename(target)[:-4]}"
        if not args.force and os.path.exists(target):
            print(f"{prefix}: already exists, skipping")
            skipped += 1
            continue

        print(f"{prefix}: generating ({len(prompt)} chars)…")
        t0 = time.time()
        success, saved, conv = generate_one(opencli, prompt, args.retries,
                                            args.timeout, log)
        if success and saved:
            shutil.copy(saved, target)
            try:
                os.unlink(saved)
            except OSError:
                pass
            size = os.path.getsize(target)
            print(f"{prefix}: ok {size // 1024}KB in {time.time()-t0:.1f}s\n")
            ok += 1
        else:
            print(f"{prefix}: FAILED in {time.time()-t0:.1f}s "
                  f"(moderation-blocked after retries, or generation error)\n")
            fail += 1
            failed_idx.append(idx)

    print(f"done: {ok} ok, {fail} failed, {skipped} skipped")
    if failed_idx:
        print(f"failed prompt indices (1-based): {failed_idx}")
        print("(moderation-blocked; review the corresponding prompts manually "
              "in chatgpt.com, or reword them and rerun)")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    main()
