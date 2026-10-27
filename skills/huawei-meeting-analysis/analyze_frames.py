#!/usr/bin/env python3
"""Multi-modal mode: describe every extracted meeting frame with a vision model.

Sends each frame PNG from _analysis/frames/ to a vision-capable LLM via an
OpenAI-compatible /v1/chat/completions endpoint (default: the rnd gateway's
glm-5.3-flash) and writes per-frame text descriptions. The agent can then
read frames_analysis.md instead of loading PNGs into context.

Outputs (into --out, default <recording>/_analysis/):
  frames_analysis.json   [{file, timestamp, description}] — resumable cache
  frames_analysis.md     human-readable version, one section per frame

Notes:
  - Pure stdlib (urllib); the intranet gateway is unreachable through the
    corporate proxy, so all proxy handlers are stripped for this call.
  - Resumable: frames already present in frames_analysis.json are skipped;
    --force re-describes everything.
  - Run with PYTHONIOENCODING=utf-8 on zh-CN Windows consoles.
  - Do NOT send any thinking/reasoning params — the gateway rejects them for
    GLM models.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

API_BASE = "http://sk-1234.rnd.huawei.com:1234/v1/chat/completions"
API_KEY = "sk-1234"
MODEL = "glm-5.3-flash"

PROMPTS = {
    "zh": ("这是会议屏幕共享/幻灯片的一帧。直接输出中文描述（不要任何前言、不要解释"
           "你的思考过程）：版式与标题、可见的要点文字（按原样引用，不要翻译）、"
           "图表/表格/代码/架构图的内容。若信息量极少，也请如实说明。"),
    "en": ("This is one frame from a screen-shared meeting slide. Output the English "
           "description directly (no preamble, no meta commentary): layout and title, "
           "visible bullet text (quote verbatim), and the content of any "
           "charts/tables/code/architecture diagrams. If it is nearly empty, say so."),
}

# No-op proxy opener: proxyuk cannot reach intranet hosts.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

# Leading meta-commentary the model sometimes emits despite the prompt ("The
# user wants me to...", "Let me analyze...", "让我..."). Dropped line-by-line.
import re as _re
_META_LINE = _re.compile(
    r"^(the user|let me|i need|i'll|let's|i should|i can see that this|looking at|"
    r"okay|首先|让我|我需要|我来|我需要仔细|用户希望|好的|这张截图|接下来我)",
    _re.IGNORECASE)


def strip_meta(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines) and (_META_LINE.match(lines[i].strip())
                              or (lines[i].strip().endswith(":") and i + 1 < len(lines))):
        i += 1
    return "\n".join(lines[i:]).strip() or text.strip()


def find_analysis_dir(path):
    """Accept a recording dir, a video file, or the _analysis dir itself."""
    if os.path.isdir(path):
        if os.path.isfile(os.path.join(path, "manifest.json")):
            return path
        cand = os.path.join(path, "_analysis")
        if os.path.isdir(cand):
            return cand
        sys.exit(f"No _analysis/ (or manifest.json) under: {path}")
    sys.exit(f"Not a directory: {path}  (run extract.py first)")


def describe_frame(img_path, model, prompt, base_url, api_key):
    """One vision call. Returns the description text."""
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content":
                "你是会议帧描述助手。直接输出对图像的描述本身，"
                "禁止输出任何关于任务或思考过程的 meta 文本。"},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
                {"type": "text", "text": prompt},
            ]},
        ],
        "temperature": 0.0,
        "max_tokens": 800,
    }
    req = urllib.request.Request(
        base_url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + api_key})
    last_err = None
    for attempt in range(4):
        try:
            with OPENER.open(req, timeout=180) as resp:
                out = json.load(resp)
            msg = out["choices"][0]["message"]
            content = msg.get("content") or msg.get("reasoning_content") or ""
            if not content.strip():
                raise ValueError("empty content")
            return strip_meta(content.strip())
        except Exception as e:  # transient gateway errors: retry with backoff
            last_err = e
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"{os.path.basename(img_path)}: {last_err}")


def fmt_ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="recording dir or _analysis dir (manifest.json + frames/)")
    ap.add_argument("--out", help="output dir (default: the _analysis dir)")
    ap.add_argument("--model", default=MODEL, help=f"vision model id. default {MODEL}")
    ap.add_argument("--base-url", default=API_BASE, help="chat completions endpoint URL")
    ap.add_argument("--api-key", default=API_KEY, help="bearer token")
    ap.add_argument("--workers", type=int, default=4, help="parallel frame calls. default 4")
    ap.add_argument("--max-frames", type=int, default=0, help="cap frame count (0 = all)")
    ap.add_argument("--force", action="store_true", help="re-describe frames already cached")
    ap.add_argument("--language", choices=["zh", "en"], default="zh", help="prompt/output language")
    args = ap.parse_args()

    analysis_dir = find_analysis_dir(args.source)
    out_dir = args.out or analysis_dir
    frames_dir = os.path.join(analysis_dir, "frames")

    # Frame list: manifest.json if present, else scan frames/.
    manifest = os.path.join(analysis_dir, "manifest.json")
    if os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as f:
            frames = json.load(f)["frames"]
        items = [(fr["file"], float(fr["timestamp"])) for fr in frames]
    else:
        items = [(fn, 0.0) for fn in sorted(os.listdir(frames_dir))
                 if fn.lower().endswith(".png")]
    if args.max_frames:
        items = items[:args.max_frames]
    missing = [fn for fn, _ in items if not os.path.isfile(os.path.join(frames_dir, fn))]
    if missing:
        sys.exit(f"frames referenced but missing on disk: {missing}")

    # Resumable cache.
    cache_path = os.path.join(out_dir, "frames_analysis.json")
    results = {}
    if os.path.isfile(cache_path) and not args.force:
        with open(cache_path, encoding="utf-8") as f:
            for rec in json.load(f):
                results[rec["file"]] = rec
    todo = [(fn, t) for fn, t in items if fn not in results or "error" in results[fn]]
    print(f"{len(items)} frames, {len(items) - len(todo)} cached, {len(todo)} to describe "
          f"(model={args.model})")
    if not os.path.isdir(frames_dir):
        sys.exit(f"no frames dir: {frames_dir}  (run extract.py first)")

    prompt = PROMPTS[args.language]
    done = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futs = {pool.submit(describe_frame, os.path.join(frames_dir, fn),
                            args.model, prompt, args.base_url, args.api_key): (fn, t)
                for fn, t in todo}
        for fut in as_completed(futs):
            fn, t = futs[fut]
            try:
                results[fn] = {"file": fn, "timestamp": round(t, 1),
                               "description": fut.result()}
                done += 1
                print(f"  [{done}/{len(todo)}] {fn} ok")
            except Exception as e:
                results[fn] = {"file": fn, "timestamp": round(t, 1), "error": str(e)}
                print(f"  [{done}/{len(todo)}] {fn} FAILED: {e}")
            # incremental cache write so an interrupted run keeps everything
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump([results[fn] for fn, _ in items if fn in results], f,
                          indent=2, ensure_ascii=False)

    # Markdown report, timestamp order.
    md_path = os.path.join(out_dir, "frames_analysis.md")
    errs = sum(1 for fn, _ in items if "error" in results.get(fn, {}))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 帧描述（多模态模式）\n\n"
                f"- 来源：{os.path.basename(analysis_dir.rstrip('/\\'))} 的 frames/\n"
                f"- 模型：{args.model}　日期：{date.today().isoformat()}"
                f"　共 {len(items)} 帧（失败 {errs}）\n"
                f"- 提示：描述由视觉模型自动生成，文字引用可能有误，关键处对照 PNG 原图。\n")
        for fn, t in sorted(items, key=lambda x: x[1]):
            rec = results.get(fn, {})
            f.write(f"\n## {fn} @ {fmt_ts(t)}\n\n")
            f.write(rec.get("description") or f"(error: {rec.get('error', 'missing')})\n")
    print(f"\nwrote {cache_path}\nwrote {md_path}")
    if errs:
        print(f"warn: {errs} frame(s) failed — re-run to retry only those")


if __name__ == "__main__":
    main()
