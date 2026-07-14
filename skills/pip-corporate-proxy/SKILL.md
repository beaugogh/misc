---
name: pip-corporate-proxy
description: Installs Python pip packages behind a strict corporate proxy / VPN on Windows when pip hangs forever or fails with 407 Proxy Authentication Required. Use when `pip install` stalls on large wheels (numpy, onnxruntime, torch, av, imageio-ffmpeg, etc.) while small packages install fine, when pip's `--timeout` never fires, when `pip config global.proxy` returns 407 but env-var `HTTPS_PROXY` works, or when you need to install heavy ML wheels (faster-whisper, pytorch, transformers) on a locked-down network.
---

# Install Python packages behind a corporate proxy (Windows)

## Context — why pip stalls here
Behind the corporate proxy (e.g. Huawei `proxyuk.huawei.com:8080`), `pip install`
exhibits a specific, repeatable failure pattern that **looks like a hang but
isn't a timeout bug**:

- **Small wheels (<~3 MB) install fine.** Metadata, tiny pure-Python wheels,
  and dependency resolution all work.
- **Large wheels stall forever.** The proxy silently drops sustained transfers
  after a few MB but keeps the TCP connection open. curl/pip see an open socket
  with no data, so **pip's `--timeout` never fires** — the download just sits
  at e.g. "Downloading numpy-12.4 MB" until you kill it.
- **A transient `407 Proxy Authentication Required`** also appears on some
  requests, unrelated to the stall.

This is the same class of problem the [[git-corporate-proxy-lfs]] skill
documents for git/LFS — a TLS-intercepting, auth-challenging corporate proxy —
but pip's failure mode (silent stall on large transfers) needs a different fix
than git's.

## The two non-obvious traps
1. **`pip config set global.proxy` fails with 407, but `HTTPS_PROXY` env var works.**
   Same proxy URL, same moment. The env-var path forwards Windows integrated
   auth that pip's config-file path does not. **Always use the env var**, never
   `pip config global.proxy`, on this network. (Side effect: if you did set
   `global.proxy` in `%APPDATA%\pip\pip.ini`, unset it — it interferes.)
2. **Only a throughput-based abort kills the stall.** Absolute timeouts
   (`--timeout`, curl `-m`) don't fire because the socket stays open. curl's
   `--speed-limit 2000 --speed-time 15` (abort if <2 KB/s for 15s) is the
   only thing that reliably detects and kills a stalled transfer.

## The fix: download big wheels with curl, then pip-install locally
Resolve exact wheel URLs from PyPI's JSON API, download each with curl using
the stall-killing flags, then `pip install` from the local files. Small deps
flow through pip normally; only the big wheels need the curl detour.

### Option A — the bundled script (does it all)
```bash
# Download numpy + onnxruntime into ./wheels (PROXY read from registry by default)
python skills/pip-corporate-proxy/fetch_wheels.py numpy onnxruntime

# Download AND pip-install them in one go
python skills/pip-corporate-proxy/fetch_wheels.py --install faster-whisper pillow numpy

# Custom output dir
python skills/pip-corporate-proxy/fetch_wheels.py --dir /tmp/wheels av imageio-ffmpeg
```
The script reads the proxy from the Windows registry (`ProxyServer` value —
the same authoritative source as the browser / the git skill), picks the
right wheel for your interpreter (`cpXY-cpXY`, then `abi3`, then `py3-none`),
downloads with `--speed-limit`/`--retry-all-errors`, and on `--install` runs
pip with the env-var proxy. It's idempotent — cached wheels (matching size)
are skipped.

### Option B — manual (to understand each step)
```bash
PROXY="http://proxyuk.huawei.com:8080"
mkdir -p wheels

# 1. Resolve the wheel URL from the PyPI JSON API
URL=$(curl -sS -m 30 --ssl-no-revoke -x "$PROXY" https://pypi.org/pypi/numpy/json \
  | python -c "import sys,json; d=json.load(sys.stdin); v=d['info']['version']; \
    print(next(u['url'] for u in d['releases'][v] \
      if u['filename'].endswith('.whl') and 'cp312' in u['filename'] and 'win_amd64' in u['filename']))")

# 2. Download with stall-killing + 407 retry (--speed-limit is the key flag)
curl -sS -L -x "$PROXY" --ssl-no-revoke \
  --retry 5 --retry-all-errors --retry-delay 3 \
  --speed-limit 2000 --speed-time 15 \
  -o wheels/numpy.whl "$URL"

# 3. Install from the local file (small deps still come from PyPI via env-var proxy)
HTTP_PROXY="$PROXY" HTTPS_PROXY="$PROXY" \
  pip install wheels/numpy.whl faster-whisper
```

## curl flags, explained
| Flag | Why |
|---|---|
| `--speed-limit 2000 --speed-time 15` | **The fix.** Abort if throughput <2 KB/s for 15s. Kills the silent stall that `--timeout` can't. |
| `--retry 5 --retry-all-errors --retry-delay 3` | Ride out the transient `407 Proxy Authentication Required` windows; resume the download. |
| `--ssl-no-revoke` | The proxy does TLS interception (MITM); schannel's CRL/OCSP revocation check hangs otherwise (`CRYPT_E_NO_REVOCATION_CHECK`). Same flag as the git skill. |
| `-x "$PROXY"` | curl in Git Bash doesn't read the Windows registry proxy either — must pass it explicitly. |
| `-L` | Follow the redirect from `pypi.org` to `files.pythonhosted.org`. |

## How to tell which wheels will stall
Wheels that bundle native binaries (the ones that hurt) — roughly anything
>~3 MB. Examples seen stalling: `numpy` (12 MB), `onnxruntime` (13 MB),
`av`/PyAV (28 MB), `imageio-ffmpeg` (31 MB — bundles ffmpeg), `pytorch`
(hundreds of MB), `tokenizers`. Pure-Python wheels (`*-py3-none-any.whl`,
usually <1 MB) never stall.

## Verify
```bash
# Wheels downloaded complete (not truncated)?
python -c "import zipfile,glob; [print(w, 'OK' if zipfile.ZipFile(w).testzip() is None else 'CORRUPT') for w in glob.glob('wheels/*.whl')]"

# Imports work?
python -c "import numpy, faster_whisper, av, imageio_ffmpeg; print('all imports OK')"
```

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| pip stuck on "Downloading X (N MB)" for minutes | Silent stall on large wheel; `--timeout` won't fire | Use the curl detour above; `--speed-limit` kills the stall |
| `407 Proxy Authentication Required` from pip | Transient proxy auth challenge | `--retry-all-errors` on curl; or just re-run — usually clears in seconds |
| `pip config global.proxy` returns 407 but env var works | Config-file path doesn't forward integrated auth | `pip config unset global.proxy`; use `HTTP_PROXY`/`HTTPS_PROXY` env vars |
| `curl: (35) schannel: ... revocation` | TLS interception by the proxy | `--ssl-no-revoke` on every curl |
| `No matching distribution found` right after 407s | 407 swallowed as a resolution failure (misleading) | Re-run; it's the 407, not a real "no distribution" |
| Script: `no compatible wheel for cp312/win_amd64` | Package has no prebuilt wheel for your Python/OS | Check pypi.org for available files; you may need a different Python or to build from source (rare) |
| Script: `No proxy found` | Registry `ProxyServer` unset and no `PROXY` env var | `export PROXY="http://proxyuk.huawei.com:8080"` (or your network's proxy) |

## Notes
- The proxy from the Windows registry is authoritative:
  `reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer`
  — same value the browser uses. (`netsh winhttp show proxy` is a *separate*
  WinHTTP setting and often reads "direct access"; don't trust it — see
  [[git-corporate-proxy-lfs]].)
- These proxy settings are only needed **on** the corporate network. Off it
  (home, hotspot), unset `HTTP_PROXY`/`HTTPS_PROXY` or git/pip will try to
  route through a proxy that isn't there.
- `imageio-ffmpeg` is worth knowing about generally: it ships a full ffmpeg
  binary *inside* the package, so you get ffmpeg for frame extraction without
  a system install or admin rights — ideal on a locked-down box.
- A venv-scoped install keeps all this out of system Python. `.venv/` is
  gitignored; the wheels you download are a reusable local cache if you need
  to recreate the venv.
