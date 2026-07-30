"""
CloudDevOps Wiki API Script

Read, update, convert, and publish CloudDevOps Wiki documents via REST API.
Supports Markdown input with Mermaid diagrams (rendered to PNG and uploaded to file storage).

Usage:
    python wiki_api.py get --sn WIKIxxxxxxxx [--output file.json] [--format html|text]
    python wiki_api.py update --sn WIKIxxxxxxxx --payload payload.json
    python wiki_api.py structure --sn WIKIxxxxxxxx
    python wiki_api.py convert --input doc.md [--output doc.html] [--title "Doc Title"]
    python wiki_api.py publish --sn WIKIxxxxxxxx --input doc.md [--section "3 方案设计"]
    python wiki_api.py sections --sn WIKIxxxxxxxx

Environment Variables:
    CLOUDDEVOPS_AUTH       Authorization token (overrides built-in auth)
    W3_USERNAME            W3 account username (for built-in auth)
    W3_PASSWORD            W3 account password (for built-in auth)
    W3_CID                 W3 client ID (for built-in auth)
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://clouddevops.huawei.com"
API_PREFIX = "/devops-knowledge-management/api"


class HTMLTextExtractor(HTMLParser):
    """Extract plain text from HTML content, preserving structure."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.skip_tags = {"script", "style"}

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.result.append("\n\n")
        elif tag in ("p", "div"):
            self.result.append("\n")
        elif tag == "li":
            self.result.append("\n- ")
        elif tag == "tr":
            self.result.append("\n")
        elif tag in ("td", "th"):
            self.result.append(" | ")
        elif tag == "br":
            self.result.append("\n")

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.result.append("\n")
        elif tag == "table":
            self.result.append("\n")

    def handle_data(self, data):
        self.result.append(data)

    def handle_entityref(self, name):
        entities = {"nbsp": " ", "lt": "<", "gt": ">", "amp": "&", "quot": '"'}
        self.result.append(entities.get(name, f"&{name};"))

    def get_text(self):
        text = "".join(self.result)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


# --- Built-in authentication (no MCP dependency) ---

_cached_token: str | None = None
_cached_token_time: float = 0
_TOKEN_TTL = 300  # seconds, token is cached for 5 minutes


def _login_w3(username: str, password: str, cid: str = "") -> str:
    """Login via W3 IDP and get CloudDevOps JWT token. Returns the JWT string."""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Step 1: Login to get Cookie
    login_url = "https://login.huawei.com/login1/rest/hwidcenter/login"
    login_headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    login_body = {
        "loginAccount": username,
        "password": password,
        "uid": username,
    }
    if cid:
        login_body["fingerPrint"] = {"cid": cid}

    req = Request(login_url, data=json.dumps(login_body).encode("utf-8"),
                  headers=login_headers, method="POST")
    try:
        with urlopen(req, timeout=15, context=_ssl_no_verify()) as resp:
            login_resp = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        raise APIError(f"W3 login failed: HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}")
    except URLError as e:
        raise APIError(f"W3 login failed: {e.reason}")

    # Extract all Set-Cookie headers (urllib may return multiple)
    # urllib's HTTPResponse.headers is an http.client.HTTPMessage, which
    # supports get_all() for duplicate header names.
    cookie_parts = []
    try:
        all_cookies = resp.headers.get_all("Set-Cookie") or []
    except AttributeError:
        all_cookies = resp.headers.get("Set-Cookie", "").split(", ")

    for cookie_header in all_cookies:
        # Each Set-Cookie header is like "name=value; Path=/; ..."
        name_value = cookie_header.split(";")[0].strip()
        if name_value:
            cookie_parts.append(name_value)

    cookie_str = "; ".join(cookie_parts)

    if not cookie_str:
        raise APIError("W3 login succeeded but no cookies returned")

    # Step 2: Use Cookie to get JWT Token
    token_url = "https://clouddevops.huawei.com/auth/api/v1/token"
    token_headers = {
        "Content-Type": "application/json",
        "cookie": cookie_str,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    token_body = {"deviceid": uuid.uuid4().hex}

    req = Request(token_url, data=json.dumps(token_body).encode("utf-8"),
                  headers=token_headers, method="POST")
    try:
        with urlopen(req, timeout=15, context=_ssl_no_verify()) as resp:
            token_resp = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        raise APIError(f"Get JWT token failed: HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}")

    jwt_token = token_resp.get("data", {}).get("jwt")
    if not jwt_token:
        raise APIError(f"JWT token not found in response: {json.dumps(token_resp, ensure_ascii=False)[:300]}")
    return jwt_token


def _ssl_no_verify():
    """Create an SSL context that skips verification (for Huawei internal HTTPS)."""
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def get_auth_token(args, force_refresh: bool = False) -> str:
    """Get authorization token.

    Priority:
      1. --auth flag (explicit token)
      2. CLOUDDEVOPS_AUTH env var
      3. Built-in W3 login (from --w3-username or W3_USERNAME env)
      4. Cached token (if still fresh)

    Token is cached for 5 minutes and auto-refreshed on expiry.
    """
    global _cached_token, _cached_token_time

    # 1. Explicit token from --auth
    if getattr(args, 'auth', None):
        return args.auth

    # 2. Environment variable
    env_token = os.environ.get("CLOUDDEVOPS_AUTH", "")
    if env_token:
        return env_token

    # 3. Cached token (still fresh)
    if not force_refresh and _cached_token and (time.time() - _cached_token_time < _TOKEN_TTL):
        return _cached_token

    # 4. Built-in W3 login
    username = getattr(args, 'w3_username', '') or os.environ.get("W3_USERNAME", "")
    password = getattr(args, 'w3_password', '') or os.environ.get("W3_PASSWORD", "")
    cid = getattr(args, 'w3_cid', '') or os.environ.get("W3_CID", "")

    if not username or not password:
        print("ERROR: No authorization token provided.", file=sys.stderr)
        print("Use one of:", file=sys.stderr)
        print("  --auth TOKEN              (explicit JWT token)", file=sys.stderr)
        print("  --w3-username + --w3-password  (built-in W3 login)", file=sys.stderr)
        print("  CLOUDDEVOPS_AUTH env var  (JWT token)", file=sys.stderr)
        print("  W3_USERNAME + W3_PASSWORD env vars  (built-in W3 login)", file=sys.stderr)
        sys.exit(1)

    try:
        token = _login_w3(username, password, cid)
        _cached_token = token
        _cached_token_time = time.time()
        print("  Auth: logged in via W3", file=sys.stderr)
        return token
    except APIError as e:
        print(f"ERROR: Built-in auth failed: {e}", file=sys.stderr)
        sys.exit(1)


class APIError(Exception):
    """Raised when a CloudDevOps API call fails."""
    pass


def make_request(url: str, auth: str, method: str = "GET", data: bytes | None = None) -> dict:
    """Make HTTP request to CloudDevOps API. Raises APIError on failure."""
    headers = {
        "Authorization": auth,
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
    }
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            if not body.strip():
                return {"code": resp.status, "data": None}
            return json.loads(body)
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise APIError(f"HTTP {e.code} {e.reason}: {error_body[:500]}")
    except URLError as e:
        raise APIError(f"Network error: {e.reason}")


def html_to_text(html: str) -> str:
    """Convert HTML to plain text."""
    extractor = HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()


def read_wiki_document(auth: str, sn: str) -> dict:
    """Read a wiki document and return parsed data with paragraphs.

    Returns dict with: sn, id, title, status, paragraphs (list of dicts).
    Raises APIError on failure.
    """
    request_tag = str(int(time.time() * 1000))
    url = f"{BASE_URL}{API_PREFIX}/wiki?sn={sn}&request_tag={request_tag}&type=UI&filterClassify=FEATURE_API_DESIGN"
    result = make_request(url, auth)

    if result.get("code") != 200:
        raise APIError(f"API error: {result.get('message', 'Unknown error')}")

    data = result["data"]
    paragraphs = []
    for p in data.get("paragraphs", []):
        paragraphs.append({
            "content_id": p.get("content_id"),
            "content_category": p.get("content_category", ""),
            "content_sort": p.get("content_sort", 0),
            "ui_source": str(p.get("ui_source", "1")),
            "content": p["content"],
        })

    return {
        "sn": data["sn"],
        "id": data["id"],
        "title": data["title"],
        "status": data.get("status", ""),
        "paragraphs": paragraphs,
    }


def build_update_payload(doc: dict, modified_paragraphs: dict | None = None) -> dict:
    """Build an update payload from a read document.

    If modified_paragraphs is provided (dict mapping content_id -> new HTML content),
    only those paragraphs will have their content replaced; all others are preserved as-is.
    """
    paragraphs = []
    for p in doc["paragraphs"]:
        para = {
            "documentClassify": "DEFAULT_VALUE",
            "category": p["content_category"],
            "content": p["content"],
            "uiSource": p["ui_source"],
            "order": p["content_sort"],
        }
        if p["content_id"] is not None:
            para["contentId"] = str(p["content_id"])

        # Apply modifications
        if modified_paragraphs and str(p["content_id"]) in modified_paragraphs:
            para["content"] = modified_paragraphs[str(p["content_id"])]

        paragraphs.append(para)

    return {
        "wikiSn": doc["sn"],
        "wikiTitle": doc["title"],
        "sourceSystem": "cloudDevops",
        "addActivity": True,
        "paragraphs": paragraphs,
        "wordCount": 0,
        "characterCount": 0,
    }


def submit_update(auth: str, payload: dict) -> dict:
    """Submit an update payload to the Wiki API. Returns the API response dict."""
    request_tag = str(int(time.time() * 1000))
    url = f"{BASE_URL}{API_PREFIX}/wiki/structured?requestTag={request_tag}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    result = make_request(url, auth, method="PUT", data=data)

    if result.get("code") != 200:
        raise APIError(f"Update failed: {result.get('message', 'Unknown error')}")

    return result


def upload_image(image_path: str | Path, auth: str, username: str = "") -> str:
    """Upload an image file to CloudDevOps file storage.

    Returns the full image URL that can be used in <img src="...">.
    """
    import mimetypes
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type = mimetypes.guess_type(str(image_path))[0] or "image/png"
    filename = image_path.name

    boundary = f"----PythonFormBoundary{uuid.uuid4().hex[:16]}"
    with open(image_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="avatar"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    request_tag = str(int(time.time() * 1000))
    url = f"{BASE_URL}/vision-file-storage/api/file/upload?file_type=image&username={username}&domain_id=&requestTag={request_tag}"

    headers = {
        "Authorization": auth,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json, text/plain, */*",
    }

    req = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Image upload failed: HTTP {e.code}: {error_body[:300]}")
    except URLError as e:
        raise RuntimeError(f"Image upload failed: {e.reason}")

    if result.get("code") != 200:
        raise RuntimeError(f"Image upload API error: {result.get('message')}")

    image_url = result["data"]["image_url"]
    return f"{BASE_URL}{image_url}"


_MMDC_CMD = "mmdc.cmd" if sys.platform == "win32" else "mmdc"
_MMDC_CHECKED = False
_MMDC_RESULT: str | None = None


def _find_mmdc() -> str | None:
    """Find mmdc executable, returns None if not available. Result is cached."""
    global _MMDC_CHECKED, _MMDC_RESULT
    if _MMDC_CHECKED:
        return _MMDC_RESULT
    _MMDC_CHECKED = True
    try:
        subprocess.run([_MMDC_CMD, "--version"], capture_output=True, timeout=10)
        _MMDC_RESULT = _MMDC_CMD
    except (FileNotFoundError, subprocess.TimeoutExpired):
        _MMDC_RESULT = None
    return _MMDC_RESULT


def _render_mermaid_to_file(mermaid_code: str, work_dir: Path, output_ext: str, scale: int = 1) -> Path | None:
    mmdc = _find_mmdc()
    if not mmdc:
        return None

    mid = uuid.uuid4().hex[:8]
    mmd_file = work_dir / f"mermaid_{mid}.mmd"
    out_file = work_dir / f"mermaid_{mid}.{output_ext}"

    mmd_file.write_text(mermaid_code, encoding="utf-8")

    cmd = [mmdc, "-i", str(mmd_file), "-o", str(out_file), "-b", "white"]
    if output_ext == "png" and scale > 1:
        cmd.extend(["-s", str(scale)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  mmdc warning: {result.stderr.strip()}", file=sys.stderr)
            return None
        if not out_file.exists():
            return None
        return out_file
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    finally:
        mmd_file.unlink(missing_ok=True)


def render_mermaid_to_svg(mermaid_code: str, work_dir: Path) -> str:
    """Render a Mermaid diagram to inline SVG. Falls back to <pre> if mmdc fails."""
    out_file = _render_mermaid_to_file(mermaid_code, work_dir, "svg")
    if out_file is None:
        return f'<pre class="mermaid">{_html_escape(mermaid_code)}</pre>'
    try:
        return out_file.read_text(encoding="utf-8")
    finally:
        out_file.unlink(missing_ok=True)


def _html_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_mermaid_to_base64_img(mermaid_code: str, work_dir: Path) -> str:
    """Render Mermaid to base64-encoded PNG <img>. Falls back to SVG if mmdc fails."""
    out_file = _render_mermaid_to_file(mermaid_code, work_dir, "png", scale=2)
    if out_file is None:
        return render_mermaid_to_svg(mermaid_code, work_dir)
    try:
        b64 = base64.b64encode(out_file.read_bytes()).decode("ascii")
        return f'<img src="data:image/png;base64,{b64}" alt="Mermaid diagram" style="max-width:100%;" />'
    finally:
        out_file.unlink(missing_ok=True)


def render_mermaid_to_uploaded_img(mermaid_code: str, work_dir: Path, auth: str, username: str = "") -> str:
    """Render Mermaid to PNG, upload to CloudDevOps file storage, return <img> tag.

    Recommended mode for CloudDevOps Wiki (inline SVG not supported).
    Falls back to base64 <img> if upload fails.
    """
    out_file = _render_mermaid_to_file(mermaid_code, work_dir, "png", scale=2)
    if out_file is None:
        return render_mermaid_to_base64_img(mermaid_code, work_dir)
    try:
        image_url = upload_image(out_file, auth, username)
        print(f"  Mermaid diagram uploaded: {image_url}", file=sys.stderr)
        return f'<img src="{image_url}" alt="Mermaid diagram" style="max-width:100%;" />'
    except Exception as e:
        print(f"  Image upload failed ({e}), falling back to base64 <img>", file=sys.stderr)
        return render_mermaid_to_base64_img(mermaid_code, work_dir)
    finally:
        out_file.unlink(missing_ok=True)


def _preprocess_obsidian_images(md_text: str) -> str:
    """Convert Obsidian ![[image.png]] syntax to standard Markdown ![image.png](image.png).

    Obsidian uses ![[filename]] for embedding images, which is not standard Markdown.
    This converts them so markdown-it can parse them correctly.
    """
    pattern = re.compile(r"!\[\[([^\]]+)\]\]")
    def replacer(match):
        filename = match.group(1)
        return f"![{filename}]({filename})"
    return pattern.sub(replacer, md_text)


def _resolve_local_images(md_text: str, base_dir: Path, auth: str = "", username: str = "") -> str:
    """Find local image references in Markdown, upload them to CloudDevOps file storage,
    and replace paths with the uploaded URLs.

    Handles two cases that markdown-it cannot parse:
    1. Image paths containing spaces (CommonMark treats spaces as delimiters)
    2. Local relative paths that need uploading before the Wiki can display them

    When auth and username are provided, images are uploaded. Otherwise, paths are
    URL-encoded so markdown-it can parse them.
    """
    # Match ![alt](path) — capture alt and path separately
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def replacer(match):
        alt_text = match.group(1)
        image_path_str = match.group(2).strip()

        # Skip URLs (already remote)
        if image_path_str.startswith(("http://", "https://", "data:")):
            return match.group(0)

        # Resolve relative path against the Markdown file's directory
        image_path = base_dir / image_path_str

        if image_path.exists() and auth and username:
            try:
                uploaded_url = upload_image(image_path, auth, username)
                print(f"  Uploaded image: {image_path_str} -> {uploaded_url}", file=sys.stderr)
                return f'![{alt_text}]({uploaded_url})'
            except Exception as e:
                print(f"  Warning: Failed to upload {image_path_str}: {e}", file=sys.stderr)

        # URL-encode spaces so markdown-it can parse the path correctly.
        # CommonMark treats unencoded spaces as delimiters, breaking the image syntax.
        if " " in image_path_str:
            encoded = image_path_str.replace(" ", "%20")
            return f"![{alt_text}]({encoded})"

        return match.group(0)

    return pattern.sub(replacer, md_text)


def markdown_to_html(md_text: str, mermaid_mode: str = "svg", auth: str = "", username: str = "",
                     base_dir: Path | None = None) -> str:
    """Convert Markdown text to HTML, rendering Mermaid code blocks.

    Args:
        md_text: Markdown source text
        mermaid_mode: How to render Mermaid diagrams - "svg" (inline SVG),
                      "img" (base64 PNG <img>), "upload" (PNG upload to file storage),
                      or "pre" (raw <pre> block)
        auth: Authorization token (required for "upload" mode and local image upload)
        username: Username for file upload (used in "upload" mode and local image upload)
        base_dir: Base directory for resolving relative image paths (defaults to cwd)
    """
    import markdown_it

    if base_dir is None:
        base_dir = Path.cwd()

    # Pre-process Obsidian ![[image.png]] -> standard ![image.png](image.png)
    md_text = _preprocess_obsidian_images(md_text)

    # Upload local images and fix paths with spaces
    md_text = _resolve_local_images(md_text, base_dir, auth, username)

    mdit = markdown_it.MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")

    mermaid_blocks = []
    protected_md = _extract_mermaid_blocks(md_text, mermaid_blocks)

    html_parts = mdit.render(protected_md)

    html_parts = _restore_mermaid_blocks(html_parts, mermaid_blocks, mermaid_mode, auth, username)

    return html_parts


def _extract_mermaid_blocks(md_text: str, mermaid_blocks: list) -> str:
    """Replace ```mermaid ... ``` blocks with placeholders to prevent markdown-it from mangling them."""
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)

    def replacer(match):
        idx = len(mermaid_blocks)
        mermaid_blocks.append(match.group(1).strip())
        return f"MERMAID_PLACEHOLDER_{idx}_END"

    return pattern.sub(replacer, md_text)


def _restore_mermaid_blocks(html: str, mermaid_blocks: list, mermaid_mode: str, auth: str = "", username: str = "") -> str:
    """Replace Mermaid placeholders with rendered diagrams."""
    work_dir = Path(tempfile.mkdtemp(prefix="mermaid_"))
    try:
        for idx, mermaid_code in enumerate(mermaid_blocks):
            placeholder = f"MERMAID_PLACEHOLDER_{idx}_END"

            if mermaid_mode == "pre":
                rendered = f'<pre class="mermaid">{_html_escape(mermaid_code)}</pre>'
            elif mermaid_mode == "img":
                rendered = render_mermaid_to_base64_img(mermaid_code, work_dir)
            elif mermaid_mode == "upload":
                rendered = render_mermaid_to_uploaded_img(mermaid_code, work_dir, auth, username)
            else:
                rendered = render_mermaid_to_svg(mermaid_code, work_dir)

            html = html.replace(f"<p>{placeholder}</p>", rendered)
            html = html.replace(placeholder, rendered)
    finally:
        for f in work_dir.iterdir():
            f.unlink(missing_ok=True)
        work_dir.rmdir()

    return html


def cmd_get(args):
    """Read a wiki document."""
    auth = get_auth_token(args)

    try:
        doc = read_wiki_document(auth, args.sn)
    except APIError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    output = {
        "sn": doc["sn"],
        "id": doc["id"],
        "title": doc["title"],
        "status": doc["status"],
        "paragraphs": [],
    }

    for p in doc["paragraphs"]:
        para = {
            "content_id": p["content_id"],
            "content_category": p["content_category"],
            "category": p["content_category"],
            "content_sort": p["content_sort"],
            "ui_source": p["ui_source"],
            "content": p["content"],
        }
        if args.format == "text":
            para["content_text"] = html_to_text(p["content"])
        output["paragraphs"].append(para)

    output_str = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")
        print(f"Document saved to: {args.output}")
        print(f"Title: {output['title']}")
        print(f"Paragraphs: {len(output['paragraphs'])}")
    else:
        print(output_str)


def cmd_update(args):
    """Update a wiki document."""
    auth = get_auth_token(args)

    payload_path = Path(args.payload)
    if not payload_path.exists():
        print(f"ERROR: Payload file not found: {args.payload}", file=sys.stderr)
        sys.exit(1)

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload["wikiSn"] = args.sn

    try:
        result = submit_update(auth, payload)
    except APIError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    _print_update_result(result)


def cmd_structure(args):
    """Get wiki document structure — clean paragraph listing."""
    auth = get_auth_token(args)

    try:
        doc = read_wiki_document(auth, args.sn)
    except APIError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Title: {doc['title']}")
    print(f"SN: {doc['sn']}")
    print(f"Paragraphs: {len(doc['paragraphs'])}")
    print()

    for p in doc["paragraphs"]:
        preview = html_to_text(p["content"])[:80].replace("\n", " ")
        print(f"  [{p['content_category']}] content_id={p['content_id']} sort={p['content_sort']}")
        print(f"    Preview: {preview}")
        print()


def cmd_convert(args):
    """Convert a Markdown file to HTML, rendering Mermaid diagrams."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    auth = ""
    username = ""
    if args.mermaid == "upload":
        auth = get_auth_token(args)
        username = getattr(args, "username", "") or ""

    md_text = input_path.read_text(encoding="utf-8")
    html = markdown_to_html(md_text, mermaid_mode=args.mermaid, auth=auth, username=username,
                            base_dir=input_path.parent)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(html, encoding="utf-8")
        print(f"HTML saved to: {args.output}")
        print(f"Size: {len(html)} chars")
    else:
        print(html)


def cmd_publish(args):
    """Convert Markdown to HTML and publish to CloudDevOps Wiki.

    Two modes:
      - Full publish (default): replaces the first paragraph with new content.
      - Section publish (--section): reads the document, replaces only the
        matching paragraph, and writes back all paragraphs unchanged except
        the target section.
    """
    auth = get_auth_token(args)
    username = getattr(args, "username", "") or ""

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    md_text = input_path.read_text(encoding="utf-8")
    html = markdown_to_html(md_text, mermaid_mode=args.mermaid, auth=auth, username=username,
                            base_dir=input_path.parent)

    # --- Section-level publish ---
    if args.section:
        try:
            doc = read_wiki_document(auth, args.sn)
        except APIError as e:
            print(f"ERROR: Could not read document for section update: {e}", file=sys.stderr)
            sys.exit(1)

        # Find the matching paragraph
        section = args.section
        target_para = None
        for p in doc["paragraphs"]:
            cat = p["content_category"]
            # Match by exact category, or by category starting with the section string
            if cat == section or cat.startswith(section.split()[0] if section.split() else section):
                target_para = p
                break

        if target_para is None:
            # List available sections to help the user
            print(f"ERROR: Section '{section}' not found.", file=sys.stderr)
            print("Available sections:", file=sys.stderr)
            for p in doc["paragraphs"]:
                print(f"  - {p['content_category']}", file=sys.stderr)
            sys.exit(1)

        print(f"  Updating section: [{target_para['content_category']}] (content_id={target_para['content_id']})")

        modified = {str(target_para["content_id"]): html}
        payload = build_update_payload(doc, modified_paragraphs=modified)

        if args.dry_run:
            _save_dry_run(args.dry_run, payload, html)
            return

        try:
            result = submit_update(auth, payload)
        except APIError as e:
            print(f"Publish failed: {e}", file=sys.stderr)
            sys.exit(1)

        _print_update_result(result, title=doc["title"], section=target_para["content_category"])
        return

    # --- Full publish (original behavior, first paragraph only) ---
    try:
        doc = read_wiki_document(auth, args.sn)
    except APIError as e:
        print(f"Note: Could not read current document ({e}), will create new.", file=sys.stderr)
        doc = None

    if doc and doc["paragraphs"]:
        title = args.title or doc["title"]
        first_para = doc["paragraphs"][0]

        paragraph = {
            "documentClassify": "DEFAULT_VALUE",
            "category": first_para["content_category"],
            "content": html,
            "uiSource": first_para["ui_source"],
            "order": first_para["content_sort"],
        }
        if first_para["content_id"] is not None:
            paragraph["contentId"] = str(first_para["content_id"])
    else:
        title = args.title or "Untitled"
        paragraph = {
            "documentClassify": "DEFAULT_VALUE",
            "category": "",
            "content": html,
            "uiSource": "1",
            "order": 99,
        }

    paragraphs = [paragraph]

    payload = {
        "wikiSn": args.sn,
        "wikiTitle": title,
        "sourceSystem": "cloudDevops",
        "addActivity": True,
        "paragraphs": paragraphs,
        "wordCount": 0,
        "characterCount": 0,
    }

    if args.dry_run:
        _save_dry_run(args.dry_run, payload, html)
        return

    try:
        result = submit_update(auth, payload)
    except APIError as e:
        print(f"Publish failed: {e}", file=sys.stderr)
        sys.exit(1)

    _print_update_result(result, title=title)


def _print_update_result(result: dict, title: str = "", section: str = ""):
    """Print a formatted update result."""
    success_items = (result.get("data") or {}).get("success", [])
    failed_items = (result.get("data") or {}).get("failed", [])

    print("Published successfully!")
    if title:
        print(f"  Title: {title}")
    if section:
        print(f"  Section: {section}")
    print(f"  Paragraphs updated: {len(success_items)}")
    for item in success_items:
        print(f"    - {item.get('field')}: {item.get('status')}")

    if failed_items:
        print(f"  Failed paragraphs: {len(failed_items)}", file=sys.stderr)
        for item in failed_items:
            print(f"    - {item}", file=sys.stderr)


def _save_dry_run(path: str, payload: dict, html: str):
    """Save payload to file for dry-run inspection."""
    payload_path = Path(path)
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Dry run: payload saved to {path}")
    print(f"  HTML size: {len(html)} chars")
    print(f"  Paragraphs: {len(payload['paragraphs'])}")


def cmd_sections(args):
    """List document sections (alias for structure with cleaner output)."""
    cmd_structure(args)


def parse_wiki_url(url: str) -> dict:
    """Extract domain_id and wiki_sn from a CloudDevOps Wiki URL.

    Example:
        https://clouddevops.huawei.com/domains/34152/wiki/3/WIKI2026060200471
        -> {"domain_id": "34152", "wiki_sn": "WIKI2026060200471"}
    """
    pattern = r"clouddevops\.huawei\.com/domains/(\d+)/wiki/\d+/(WIKI\d+)"
    match = re.search(pattern, url)
    if match:
        return {"domain_id": match.group(1), "wiki_sn": match.group(2)}
    return {}


def main():
    parser = argparse.ArgumentParser(
        description="CloudDevOps Wiki API Tool - Read, update, convert and publish Wiki documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Read document
  python wiki_api.py --w3-username w00511258 --w3-password PASS get --sn WIKI2026060200471

  # Read and save to file as plain text
  python wiki_api.py get --sn WIKI2026060200471 --output doc.json --format text

  # List document sections
  python wiki_api.py structure --sn WIKI2026060200471

  # Convert Markdown to HTML (with Mermaid rendering)
  python wiki_api.py convert --input design.md --output design.html

  # Publish Markdown directly to Wiki (full document)
  python wiki_api.py publish --sn WIKI2026060200471 --input design.md

  # Publish Markdown to a specific section only
  python wiki_api.py publish --sn WIKI2026060200471 --input design.md --section "3 方案设计"

  # Dry-run publish (save payload without sending)
  python wiki_api.py publish --sn WIKI2026060200471 --input design.md --dry-run payload.json

  # Update document from JSON payload
  python wiki_api.py update --sn WIKI2026060200471 --payload update.json
        """,
    )

    # Global auth options (must come before subcommand)
    parser.add_argument("--auth", help="Authorization JWT token (or set CLOUDDEVOPS_AUTH env)")
    parser.add_argument("--username", default="", help="Username for image upload (used with --mermaid upload)")
    parser.add_argument("--w3-username", default="", help="W3 account username for built-in auth (or set W3_USERNAME env)")
    parser.add_argument("--w3-password", default="", help="W3 account password for built-in auth (or set W3_PASSWORD env)")
    parser.add_argument("--w3-cid", default="", help="W3 client ID for built-in auth (or set W3_CID env)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # get
    get_parser = subparsers.add_parser("get", help="Read a wiki document")
    get_parser.add_argument("--sn", required=True, help="Wiki document SN (e.g. WIKI2026060200471)")
    get_parser.add_argument("--output", help="Output file path (default: stdout)")
    get_parser.add_argument("--format", choices=["html", "text"], default="html",
                            help="Output format (default: html)")

    # update
    update_parser = subparsers.add_parser("update", help="Update a wiki document from JSON payload")
    update_parser.add_argument("--sn", required=True, help="Wiki document SN")
    update_parser.add_argument("--payload", required=True, help="JSON file with update payload")

    # structure
    struct_parser = subparsers.add_parser("structure", help="List document sections (paragraph categories)")
    struct_parser.add_argument("--sn", required=True, help="Wiki document SN")

    # sections (alias)
    sections_parser = subparsers.add_parser("sections", help="Alias for 'structure'")

    sections_parser.add_argument("--sn", required=True, help="Wiki document SN")

    # convert
    convert_parser = subparsers.add_parser("convert", help="Convert Markdown to HTML (with Mermaid support)")
    convert_parser.add_argument("--input", required=True, help="Input Markdown file path")
    convert_parser.add_argument("--output", help="Output HTML file path (default: stdout)")
    convert_parser.add_argument("--mermaid", choices=["svg", "img", "upload", "pre"], default="svg",
                                help="Mermaid render mode (default: svg)")
    convert_parser.add_argument("--title", help="Document title (used in publish mode)")

    # publish
    publish_parser = subparsers.add_parser("publish",
                                           help="Convert Markdown to HTML and publish to CloudDevOps Wiki")
    publish_parser.add_argument("--sn", required=True, help="Wiki document SN")
    publish_parser.add_argument("--input", required=True, help="Input Markdown file path")
    publish_parser.add_argument("--section", default="",
                                help="Only update the matching section/paragraph (e.g. '3 方案设计'). "
                                     "Other paragraphs are preserved unchanged.")
    publish_parser.add_argument("--title", help="Document title (default: keep current title)")
    publish_parser.add_argument("--mermaid", choices=["svg", "img", "upload", "pre"], default="upload",
                                help="Mermaid render mode (default: upload)")
    publish_parser.add_argument("--dry-run", metavar="FILE",
                                help="Save payload to FILE without sending to API")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "get": cmd_get,
        "update": cmd_update,
        "structure": cmd_structure,
        "sections": cmd_sections,
        "convert": cmd_convert,
        "publish": cmd_publish,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
