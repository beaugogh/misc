---
name: git-corporate-proxy-lfs
description: Diagnoses and fixes `git clone`/`git pull` failures behind a strict corporate proxy on Windows — the "Failed to connect to github.com:443" timeout, the schannel revocation-check hang (CRYPT_E_NO_REVOCATION_CHECK / 0x80092012), and Git LFS pulling at single-digit KB/s. Use when git over HTTPS stalls or times out on a corporate/VPN network, when regular git works but LFS crawls, when a clone dies mid-checkout leaving files as LFS pointers, or when the proxy injects a 407 Proxy Authentication Required partway through a transfer. Also covers partial (`blob:none`/promisor) clones that can't finish a checkout (`could not fetch ... from promisor remote`) and phantom `git status` deletions caused by the LFS smudge filter.
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

- **Partial clones (`--filter=blob:none`) defer blob downloads.** A
  `blob:none` clone fetches commits and trees but fetches file blobs *lazily,
  on demand*. Any `git reset --hard` / `git checkout` then tries to fetch
  every missing blob at once, and the proxy kills the transfer
  (`could not fetch <oid> from promisor remote`). Worse, a promisor remote
  **lies about presence**: `git cat-file -e <oid>` (and `git fsck`) will
  report a blob as present when it isn't, because the promisor answers "yes,
  I can get that" rather than "yes, I have that." **Fix:** fetch the missing
  blobs explicitly in chunks via `git fetch origin <oid1> <oid2> ...` (GitHub
  honors `uploadpack.allowAnySHA1InWant`), with a retry loop per chunk — see
  **Partial / promisor clones** below.

- **The LFS smudge filter can fake tens of thousands of phantom deletions.**
  When a repo's `.gitattributes` marks patterns as `filter=lfs` but the
  working-tree files hold *real content* (not LFS pointers), the clean/smudge
  filter re-hashes them and the hash mismatches what the index expects — so
  `git status` reports **every** such file as `D` (deleted) even though the
  bytes are on disk. This is not a real deletion. **Fix:** disable the smudge
  and rebuild the index — `git lfs install --skip-smudge` then
  `git read-tree HEAD`; the phantom deletions collapse to the genuine set of
  missing files. Re-enable smudge with `git lfs install --force` before
  checking out LFS-tracked files.

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
git config --global --get lfs.proxy             # -> http://proxy...:8080  (MUST be set; LFS ignores http.proxy)
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

## Partial / promisor clones (`--filter=blob:none`)
A `blob:none` clone fetches history (commits + trees) but **not** file blobs —
they're fetched lazily on first access. Behind a flaky proxy this makes any
bulk checkout (`reset --hard`, `checkout`, `merge`) die mid-way with
`could not fetch <oid> from promisor remote`, because it tries to lazy-fetch
thousands of blobs in one shot. Work through it in three steps:

**1. Get an *accurate* count of missing blobs.** Do **not** trust `git fsck`
or `git cat-file -e` under a promisor remote — they report blobs as present
that aren't. Enumerate what's actually in the local object store and diff it
against the HEAD tree (blobs only — exclude `160000` gitlink/submodule entries):

```bash
cd repo
# Blobs actually present locally (from packs + loose):
git cat-file --batch-all-objects --batch-check --unordered \
  | awk '$2=="blob"{print $1}' | sort -u > /tmp/local_blobs.txt
# Blobs the HEAD tree needs (blob entries only, NOT mode-160000 submodule gitlinks):
git ls-tree -r HEAD | awk '$2=="blob"{print $3}' | sort -u > /tmp/head_blobs.txt
comm -23 /tmp/head_blobs.txt /tmp/local_blobs.txt > /tmp/missing_blobs.txt
wc -l < /tmp/missing_blobs.txt        # the true missing count
```

**2. Fetch the missing blobs in chunks.** GitHub honors
`uploadpack.allowAnySHA1InWant`, so `git fetch origin <oid> <oid> ...` batches
many blobs into one pack request — far more proxy-resilient than per-blob
lazy fetches. Loop in chunks (~200), recompute the missing set each round
(failed chunks get retried automatically), and kill stale `.git/index.lock`
between rounds:

```bash
CHUNK=200
while :; do
  head -n "$CHUNK" /tmp/missing_blobs.txt > /tmp/chunk_oids.txt
  [ -s /tmp/chunk_oids.txt ] || break
  git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=45 fetch --no-tags \
    --no-write-fetch-head origin $(cat /tmp/chunk_oids.txt) || sleep 2   # retry on 407/truncation
  rm -f .git/index.lock
  git cat-file --batch-all-objects --batch-check --unordered \
    | awk '$2=="blob"{print $1}' | sort -u > /tmp/local_blobs.txt
  comm -23 /tmp/head_blobs.txt /tmp/local_blobs.txt > /tmp/missing_blobs.txt
done
```

**Gotcha — submodule gitlinks poison OID chunks.** `git ls-tree -r HEAD`
lists submodule pointers as `160000 commit <sha> <path>`. If one of those
commit SHAs lands in your blob list, GitHub rejects the **entire** chunk with
`upload-pack: not our ref <sha>` (the parent repo doesn't host the
submodule's commit). The fix is the `awk '$2=="blob"'` filter in step 1 —
it excludes the `160000`/commit entries. If you still see `not our ref`,
check whether the named SHA is a gitlink: `git ls-tree -r HEAD | grep <sha>`
shows mode `160000`.

**3. Once missing = 0, materialize the tree.** With every blob local, a hard
reset needs no network. If it still triggers LFS smudge filtering (large files),
run `git lfs pull` separately afterward (it resumes from the `.git/lfs/` cache)
rather than letting the reset's smudge stage fight the proxy.

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
| `could not fetch <oid> from promisor remote` on `reset`/`checkout` | Partial (`blob:none`) clone; checkout lazy-fetches thousands of blobs at once and the proxy kills it | Fetch missing blobs in chunks: `git fetch origin <oid>...`; see **Partial / promisor clones** above. Don't trust `cat-file -e` for presence under a promisor remote |
| `upload-pack: not our ref <sha>` rejects an entire OID chunk | A submodule gitlink (mode `160000 commit`) SHA got into the blob list | Rebuild the list filtering to blobs only: `git ls-tree -r HEAD \| awk '$2=="blob"{print $3}'`; see **Partial / promisor clones** above |
| `git status` shows every LFS-pattern file as `D` (deleted) but the files are on disk | LFS clean/smudge filter re-hashing real content matched by `filter=lfs` — hash mismatch, not a real deletion | `git lfs install --skip-smudge; git read-tree HEAD` to collapse to the true missing set, then `git lfs install --force` before checking out LFS files |
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
