---
name: git-corporate-proxy-lfs
description: Diagnoses and fixes `git clone`/`git pull` failures behind a strict corporate proxy on Windows — the "Failed to connect to github.com:443" timeout, the schannel revocation-check hang (CRYPT_E_NO_REVOCATION_CHECK / 0x80092012), and Git LFS pulling at single-digit KB/s. Use when git over HTTPS stalls or times out on a corporate/VPN network, when regular git works but LFS crawls, when a clone dies mid-checkout leaving files as LFS pointers, or when the proxy injects a 407 Proxy Authentication Required partway through a transfer.
---

# Git behind a corporate proxy, with LFS (Windows / Git Bash Edition)

## Context
Locked-down corporate networks (e.g. Huawei `proxyuk.huawei.com:8080`) break git
in a stack of compounding layers. Each layer has a different symptom and a
different fix — you usually hit several at once:

- **Direct outbound HTTPS is blocked.** Every external host times out on port
  443 (and SSH port 22): `github.com`, `google.com`, `bing.com`, `ssh.github.com`.
  The browser works only because Windows has the proxy set in the IE/registry
  settings — but `git`/`curl` in Git Bash **do not read that registry value**.
  They need the proxy told to them explicitly. **Fix:** set `http.proxy` /
  `https.proxy` in git config (or `HTTP_PROXY`/`HTTPS_PROXY` env vars).

- **The proxy does TLS interception (man-in-the-middle).** It re-signs traffic,
  so Windows schannel's certificate-revocation check tries to fetch CRL/OCSP
  endpoints that the interceptor mangles — the check **hangs for the full
  timeout** (the 20s / 2min stall). curl reports
  `CRYPT_E_NO_REVOCATION_CHECK (0x80092012)`. **Fix:** set
  `http.sslBackend=schannel` + `http.schannelCheckRevoke=false`.

- **LFS uses its own HTTP client** that does **not** read git's `http.proxy`.
  If you fix git's proxy but not LFS's, regular `git clone` works yet
  `git lfs pull` still can't reach GitHub's LFS storage. **Fix:** set
  `lfs.proxy` (and the per-host `lfs.https://github.com.proxy`).

- **LFS defaults to only 3 concurrent transfers.** Through a high-latency
  proxy each small file pays the full round-trip cost serially, giving
  ~5 KB/s. **Fix:** `lfs.concurrenttransfers=20` (or higher). This alone took
  a real pull from 5 KB/s to ~100 KB/s — a 20x speedup.

- **Killing a clone mid-LFS leaves files as pointers.** An interrupted clone
  downloads the packed git objects (so `git fsck` passes and history is
  complete) but never materializes the LFS files — they stay as tiny
  `version https://git-lfs.github.com/spec/v1` text pointers, and
  `git status` shows every one as `D` (deleted). **Fix:** clear any stale
  `.git/index.lock`, then `git lfs pull` to finish.

- **The proxy may inject `407 Proxy Authentication Required` mid-transfer.**
  Often transient (a quota/credential window rotating). The in-flight pull
  dies with `Failed to fetch some objects`. **Fix:** just re-run
  `git lfs pull` — it resumes from the LFS cache and usually clears.

## Prerequisites
- **Git for Windows** (provides Git Bash, `git`, and schannel). Check `git --version`.
- **Git LFS** installed. Check `git lfs version`; install with
  `winget install GitHub.GitLFS` if missing.
- **Git Credential Manager (GCM)** for private-repo auth without pasting tokens
  into config. Git for Windows bundles it; check `git credential-manager --version`.
- A working **proxy URL** for your corporate network (host:port), e.g.
  `http://proxy.example.com:8080`.

## Required inputs — confirm or ask the user before running
1. **Proxy URL** — host:port of the corporate HTTP proxy, e.g.
   `http://proxyuk.huawei.com:8080`. If unknown, check Windows:
   `reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" //v ProxyServer`.
2. Whether the target repo is **private** (needs auth) and whether it uses
   **Git LFS** (look for `filter=lfs` lines in its `.gitattributes`).

The bundled script has `http://proxyuk.huawei.com:8080` as a placeholder —
replace it before running.

## How to run

### Option A — run the bundled script (fastest)
1. Read `setup.sh` in this skill directory.
2. Edit the **CONFIG** block at the top with the user's proxy URL. Use the
   Edit tool — don't hand-type the whole script.
3. Run it in Git Bash:
   ```bash
   bash setup.sh
   ```
   It applies the global git config (proxy + schannel revocation off),
   configures LFS for the proxy, sets a high transfer concurrency, and enables
   Git Credential Manager. It is idempotent and safe to re-run.

### Option B — run the steps manually
In Git Bash, replace `PROXY` with the corporate proxy URL:

```bash
PROXY="http://proxyuk.huawei.com:8080"

# 1. Route git through the proxy (git/curl in Bash ignore the Windows registry proxy)
git config --global http.proxy  "$PROXY"
git config --global https.proxy "$PROXY"

# 2. Disable schannel's revocation check — it hangs on the TLS-intercepting proxy
git config --global http.sslBackend schannel
git config --global http.schannelCheckRevoke false

# 3. Point LFS at the proxy too (LFS has its own HTTP client, ignores git's http.proxy)
git config --global lfs.proxy "$PROXY"
git config --global lfs.https://github.com.proxy "$PROXY"

# 4. Raise LFS concurrency from the default 3 -> 20 (kills the single-digit-KB/s crawl)
git config --global lfs.concurrenttransfers 20

# 5. Private repos: use Git Credential Manager (encrypted in Windows Credential Manager,
#    browser-based OAuth) instead of pasting tokens into config files
git config --global credential.helper manager
git config --global credential.https://github.com.helper "!git-credential-manager"
git config --global credential.github.com.oauthmethod web
```

Then clone normally — GCM pops a browser window for GitHub login on the first
private-repo operation:
```bash
git clone https://github.com/owner/repo.git
```

## Verify
```bash
# Proxy + revocation settings applied
git config --global --get http.proxy            # -> http://proxy...:8080
git config --global --get http.schannelCheckRevoke  # -> false
git config --global --get lfs.concurrenttransfers   # -> 20

# Can git reach GitHub through the proxy? (--ssl-no-revoke mirrors the git setting)
curl -sS -m 20 -x "$PROXY" --ssl-no-revoke -o /dev/null \
  -w "github -> HTTP %{http_code}\n" https://github.com

# Clone a tiny public repo as a smoke test
git clone --depth 1 https://github.com/git-fixtures/basic.git /tmp/smoke && echo OK
```

## Recovering an interrupted clone (files stuck as LFS pointers)
If a clone was killed mid-LFS, the working tree is incomplete but salvageable —
**don't delete and re-clone** (the big objects are already on disk):

```bash
cd repo
rm -f .git/index.lock                       # stale lock from the killed process (0 bytes = safe)
git reset --mixed HEAD                       # resync the index with the working tree
git status --porcelain | grep -c '^ D'       # count files still missing (LFS pointers)
git lfs pull                                 # finish materializing the LFS files
git fsck --connectivity-only                 # confirm object integrity (empty output = clean)
```
A file is a real asset (not a pointer) if its first bytes are binary, e.g. a
`.wav` starts with `RIFF...WAVE`. A pointer starts with the text
`version https://git-lfs.github.com/spec/v1`.

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `Failed to connect to github.com:443 after Ns` | Direct outbound blocked; git not told the proxy | `git config --global http.proxy "$PROXY"` (+ `https.proxy`) |
| Connects but hangs ~20s/2min, then times out | schannel revocation check stalled on TLS-intercepting proxy | `git config --global http.sslBackend schannel` + `http.schannelCheckRevoke false` |
| `CRYPT_E_NO_REVOCATION_CHECK (0x80092012)` (curl) | Same TLS interception | `curl --ssl-no-revoke` / set schannel revocation off in git |
| Regular git works, `git lfs pull` can't reach host | LFS ignores git's `http.proxy` | `git config --global lfs.proxy "$PROXY"` (+ per-host) |
| LFS pulling at ~5 KB/s | Default 3 concurrent transfers through a latent proxy | `git config --global lfs.concurrenttransfers 20` |
| `destination path already exists and is not empty` | A prior (interrupted) clone left a partial dir | Inspect it first — likely salvageable; see "Recovering" above. Only `rm -rf` if it's a true empty stub |
| `git status` shows every file as `D` (deleted) | Clone killed mid-checkout; index out of sync | `rm -f .git/index.lock; git reset --mixed HEAD; git lfs pull` |
| `401 Unauthorized` on clone | Repo is private, no creds yet | GCM prompts in-browser on first op; or use a PAT at github.com/settings/tokens (`repo` scope) |
| `407 Proxy Authentication Required` mid-LFS | Transient proxy auth challenge (quota/credential rotation) | Re-run `git lfs pull` — resumes from LFS cache, usually clears |
| `index.lock: File exists` | A git/LFS process was killed mid-write | Confirm no `git`/`git-lfs` process is running (`tasklist \| grep -i git`), then `rm -f .git/index.lock` |
| `403`/block page from `Invoke-WebRequest`/installers | Proxy returns HTML block page for some clients | Use NPM/git (honor proxy) rather than PowerShell web cmdlets |

## Notes
- These are **global** settings (`--global`); they apply to all repos. That's
  correct on a corporate network, but **off that network** (home, hotspot,
  other office) the proxy config will break git. Toggle it:
  ```bash
  # Going OFF the corporate network:
  git config --global --unset http.proxy
  git config --global --unset https.proxy
  # Coming back ON:
  git config --global http.proxy  "$PROXY"
  git config --global https.proxy "$PROXY"
  ```
- GCM stores credentials in **Windows Credential Manager** (encrypted, tied to
  the Windows account) — never in plaintext config. Browser-based OAuth is the
  most reliable flow through a corporate proxy; GCM falls back to device-code
  if the browser can't reach github.com.
- LFS caches downloaded objects under `.git/lfs/`. A killed `git lfs pull`
  loses nothing already cached — re-running resumes from there.
- The proxy URL in the registry is the authoritative one the browser uses:
  `reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" //v ProxyServer`.
  `netsh winhttp show proxy` is a *separate* WinHTTP setting and often reads
  "direct access" even when the IE/registry proxy is set — don't trust it as
  the source of truth.
