#!/usr/bin/env bash
# =====================================================================
# Git + corporate proxy + Git LFS setup — Corporate Firewall Edition
#
# Edit the CONFIG block below, then run in Git Bash:
#     bash setup.sh
#
# Why this script exists (see SKILL.md for full context):
#   - Direct HTTPS blocked by firewall          -> route git through the proxy
#   - Proxy does TLS interception               -> disable schannel revocation check
#   - LFS ignores git's http.proxy              -> set lfs.proxy explicitly
#   - LFS defaults to 3 parallel transfers      -> raise to 20 (20x speedup)
#   - Private repos need auth                   -> Git Credential Manager (encrypted)
#
# Idempotent: safe to re-run. All settings are --global.
# =====================================================================

set -euo pipefail

# ---------------------------------------------------------------------
# CONFIG — replace with your corporate proxy URL
# ---------------------------------------------------------------------
PROXY="http://proxyuk.huawei.com:8080"
# Per-host LFS proxy (same as PROXY for github.com in most cases)
LFS_GITHUB_PROXY="$PROXY"
# LFS parallel transfers (default is 3; 20 is a good balance through a latent proxy)
LFS_CONCURRENCY=20
# ---------------------------------------------------------------------

step() { printf '\n==> %s\n' "$1"; }

# 0. Preflight
command -v git >/dev/null || { echo "git not found. Install Git for Windows." >&2; exit 1; }
if ! git lfs version >/dev/null 2>&1; then
  echo "Git LFS not found. Install it:" >&2
  echo "  winget install GitHub.GitLFS" >&2
  exit 1
fi

# 1. Route git through the proxy.
#    git/curl in Git Bash do NOT read the Windows registry proxy that the
#    browser uses — they need it set explicitly.
step "Setting git http(s).proxy = $PROXY"
git config --global http.proxy  "$PROXY"
git config --global https.proxy "$PROXY"

# 2. Disable schannel's certificate-revocation check.
#    The proxy intercepts TLS, so CRL/OCSP fetches hang for the full timeout
#    (CRYPT_E_NO_REVOCATION_CHECK / 0x80092012). schannel is the Windows-native
#    SSL backend and the right choice behind a corporate MITM proxy.
step "Disabling schannel revocation check (TLS-interception workaround)"
git config --global http.sslBackend schannel
git config --global http.schannelCheckRevoke false

# 3. Point LFS at the proxy.
#    LFS has its OWN HTTP client and ignores git's http.proxy — without this,
#    regular git works but `git lfs pull` can't reach GitHub's LFS storage.
step "Setting lfs.proxy = $PROXY"
git config --global lfs.proxy "$PROXY"
git config --global lfs.https://github.com.proxy "$LFS_GITHUB_PROXY"

# 4. Raise LFS concurrency.
#    Default is 3 parallel transfers; through a high-latency proxy that yields
#    ~5 KB/s. Raising it spreads the per-request round-trip cost across many
#    in-flight downloads — measured 5 KB/s -> ~100 KB/s.
step "Setting lfs.concurrenttransfers = $LFS_CONCURRENCY"
git config --global lfs.concurrenttransfers "$LFS_CONCURRENCY"

# 5. Private-repo auth via Git Credential Manager.
#    Stores credentials encrypted in Windows Credential Manager (tied to the
#    Windows account), browser-based OAuth — no tokens pasted into config files.
#    Git for Windows bundles GCM; check with: git credential-manager --version
if git credential-manager --version >/dev/null 2>&1; then
  step "Enabling Git Credential Manager"
  git config --global credential.helper manager
  git config --global credential.https://github.com.helper "!git-credential-manager"
  git config --global credential.github.com.oauthmethod web
else
  echo "Git Credential Manager not found — skipping (private-repo auth will prompt for user/PAT)." >&2
fi

# 6. Verify
step "Verify"
printf '  http.proxy                 = %s\n' "$(git config --global --get http.proxy)"
printf '  http.sslBackend            = %s\n' "$(git config --global --get http.sslBackend)"
printf '  http.schannelCheckRevoke   = %s\n' "$(git config --global --get http.schannelCheckRevoke)"
printf '  lfs.proxy                  = %s\n' "$(git config --global --get lfs.proxy)"
printf '  lfs.concurrenttransfers    = %s\n' "$(git config --global --get lfs.concurrenttransfers)"
printf '  credential.helper          = %s\n' "$(git config --global --get credential.helper || echo '(unset)')"

echo
echo "Smoke test — can git reach GitHub through the proxy?"
if curl -sS -m 20 -x "$PROXY" --ssl-no-revoke -o /dev/null -w '  github.com -> HTTP %{http_code} in %{time_total}s\n' https://github.com; then
  echo
  echo "Done. Clone normally — e.g.:"
  echo "  git clone https://github.com/owner/repo.git"
  echo "  (GCM opens a browser for GitHub login on the first private-repo op)"
else
  echo "  curl could not reach github.com via the proxy — check PROXY=$PROXY and your VPN." >&2
fi

echo
echo "NOTE: these are GLOBAL settings. Off this corporate network (home/other office)"
echo "they will break git. Clear them with:"
echo "  git config --global --unset http.proxy && git config --global --unset https.proxy"
echo "(re-set them when you're back on the corporate network.)"
