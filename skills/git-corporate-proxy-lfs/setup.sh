#!/usr/bin/env bash
# =====================================================================
# Git + corporate proxy + Git LFS setup — Corporate Firewall Edition
# Supports Windows (Git Bash) AND macOS.
#
# Run:
#     bash setup.sh                          # auto-detect OS + proxy
#     PROXY=http://host:port bash setup.sh   # override proxy detection
#
# Why this script exists (see SKILL.md for full context):
#   - Direct HTTPS blocked/mangled by firewall  -> route git through the proxy
#   - Proxy does TLS interception (Windows)     -> disable schannel revocation check
#   - LFS ignores git's http.proxy              -> set lfs.proxy explicitly
#   - LFS defaults to 3 parallel transfers      -> raise to 20 (20x speedup)
#   - Private repos need auth                   -> GCM (Windows) / gh (macOS)
#
# Idempotent: safe to re-run. All settings are --global.
# =====================================================================

set -euo pipefail

# ---------------------------------------------------------------------
# CONFIG — optional; leave PROXY empty to auto-detect from system settings
# ---------------------------------------------------------------------
PROXY="${PROXY:-}"
# LFS parallel transfers (default is 3; 20 is a good balance through a latent proxy)
LFS_CONCURRENCY=20
# ---------------------------------------------------------------------

step() { printf '\n==> %s\n' "$1"; }

# ---- Platform detection ------------------------------------------------
OS="$(uname -s)"
case "$OS" in
  Darwin)               PLATFORM="macOS" ;;
  MINGW*|MSYS*|CYGWIN*) PLATFORM="Windows" ;;
  *)
    echo "Unsupported platform: $OS (this skill covers Windows + macOS)." >&2
    echo "The 'both platforms' steps in SKILL.md Option B may still apply." >&2
    exit 1 ;;
esac
echo "Platform: $PLATFORM"

# ---- Proxy auto-detection ----------------------------------------------
# The browser reads the OS proxy setting; git does not. Pull the same value
# the browser uses so git can be pointed at it.
detect_proxy() {
  if [ "$PLATFORM" = "macOS" ]; then
    # scutil --proxy is the authoritative source (System Settings -> Proxies).
    # Prefer the HTTP proxy; fall back to SOCKS if that's all that's enabled
    # (git accepts socks5:// URLs in http.proxy).
    scutil --proxy | awk '
      $1 == "HTTPEnable"  && $3 == 1 { enabled = 1 }
      enabled && $1 == "HTTPProxy"   { host = $3 }
      enabled && $1 == "HTTPPort"    { port = $3 }
      $1 == "SOCKSEnable" && $3 == 1 { socks = 1 }
      socks   && $1 == "SOCKSProxy"  { shost = $3 }
      socks   && $1 == "SOCKSPort"   { sport = $3 }
      END {
        if (enabled && host != "" && port != "")
          printf "http://%s:%s\n", host, port
        else if (socks && shost != "" && sport != "")
          printf "socks5://%s:%s\n", shost, sport
      }'
  else
    # Windows: the IE/registry proxy is the one the browser uses.
    local out val
    out="$(reg query 'HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings' 2>/dev/null || true)"
    if printf '%s\n' "$out" | grep -Eq 'ProxyEnable[[:space:]]+REG_DWORD[[:space:]]+0x1'; then
      val="$(printf '%s\n' "$out" | awk '/ProxyServer/ { print $3 }' | head -n 1)"
      case "$val" in
        "")                  ;;
        *=*|*\;*)            # multi-protocol form like "http=h:80;https=h:80"
          echo "Registry proxy '$val' is in multi-protocol form — pass PROXY explicitly." >&2 ;;
        http://*|https://*)  printf '%s\n' "$val" ;;
        *)                   printf 'http://%s\n' "$val" ;;
      esac
    fi
  fi
}

if [ -z "$PROXY" ]; then
  step "Auto-detecting proxy from system settings"
  PROXY="$(detect_proxy || true)"
fi
if [ -z "$PROXY" ]; then
  echo "Could not auto-detect the proxy. Pass it explicitly:" >&2
  echo "  PROXY=http://proxy.example.com:8080 bash setup.sh" >&2
  exit 1
fi

# 0. Preflight
command -v git >/dev/null || { echo "git not found." >&2; exit 1; }
if ! git lfs version >/dev/null 2>&1; then
  echo "Git LFS not found. Install it:" >&2
  if [ "$PLATFORM" = "macOS" ]; then
    echo "  brew install git-lfs" >&2
  else
    echo "  winget install GitHub.GitLFS" >&2
  fi
  exit 1
fi

# 1. Route git through the proxy (both platforms).
#    git/curl do NOT read the OS proxy settings the browser uses — they need
#    it set explicitly.
step "Setting git http(s).proxy = $PROXY"
git config --global http.proxy  "$PROXY"
git config --global https.proxy "$PROXY"

# 2. Disable schannel's certificate-revocation check — Windows ONLY.
#    The proxy intercepts TLS, so CRL/OCSP fetches hang for the full timeout
#    (CRYPT_E_NO_REVOCATION_CHECK / 0x80092012). macOS git uses
#    OpenSSL/LibreSSL: no revocation-check hang, nothing to do.
if [ "$PLATFORM" = "Windows" ]; then
  step "Disabling schannel revocation check (TLS-interception workaround)"
  git config --global http.sslBackend schannel
  git config --global http.schannelCheckRevoke false
fi

# 3. Point LFS at the proxy (both platforms).
#    LFS has its OWN HTTP client and ignores git's http.proxy — without this,
#    regular git works but `git lfs pull` can't reach GitHub's LFS storage.
step "Setting lfs.proxy = $PROXY"
git config --global lfs.proxy "$PROXY"
git config --global lfs.https://github.com.proxy "$PROXY"

# 4. Raise LFS concurrency (both platforms).
#    Default is 3 parallel transfers; through a high-latency proxy that yields
#    ~5 KB/s. Raising it spreads the per-request round-trip cost across many
#    in-flight downloads — measured 5 KB/s -> ~100 KB/s.
step "Setting lfs.concurrenttransfers = $LFS_CONCURRENCY"
git config --global lfs.concurrenttransfers "$LFS_CONCURRENCY"

# 5. Private-repo auth.
#    Windows: Git Credential Manager — encrypted in Windows Credential
#    Manager, browser-based OAuth, bundled with Git for Windows.
#    macOS: gh CLI (token in Keychain) if present, else GCM if installed.
if [ "$PLATFORM" = "Windows" ]; then
  if git credential-manager --version >/dev/null 2>&1; then
    step "Enabling Git Credential Manager"
    git config --global credential.helper manager
    git config --global credential.https://github.com.helper "!git-credential-manager"
    git config --global credential.github.com.oauthmethod web
  else
    echo "Git Credential Manager not found — skipping (private-repo auth will prompt for user/PAT)." >&2
  fi
else
  if command -v gh >/dev/null 2>&1; then
    step "Wiring gh CLI into git's credential helper"
    if gh auth setup-git; then
      gh auth status >/dev/null 2>&1 \
        || echo "gh is installed but not logged in — run: gh auth login" >&2
    else
      echo "gh auth setup-git failed — run 'gh auth login', then re-run this script." >&2
    fi
  elif git credential-manager --version >/dev/null 2>&1; then
    step "Enabling Git Credential Manager (macOS build)"
    git config --global credential.helper manager
    git config --global credential.https://github.com.helper "!git-credential-manager"
  else
    echo "Neither gh nor GCM found — install one for private-repo auth:" >&2
    echo "  brew install gh && gh auth login" >&2
  fi
fi

# 6. Verify
step "Verify"
printf '  http.proxy                 = %s\n' "$(git config --global --get http.proxy)"
if [ "$PLATFORM" = "Windows" ]; then
  printf '  http.sslBackend            = %s\n' "$(git config --global --get http.sslBackend)"
  printf '  http.schannelCheckRevoke   = %s\n' "$(git config --global --get http.schannelCheckRevoke)"
fi
printf '  lfs.proxy                  = %s\n' "$(git config --global --get lfs.proxy)"
printf '  lfs.concurrenttransfers    = %s\n' "$(git config --global --get lfs.concurrenttransfers)"
printf '  credential.helper          = %s\n' "$(git config --global --get credential.helper || echo '(unset)')"

echo
echo "Smoke test — can git reach GitHub through the proxy?"
# Windows curl needs --ssl-no-revoke behind the TLS-intercepting proxy;
# stock macOS curl has no such flag and doesn't need it.
CURL_FLAGS=(-sS -m 20 -x "$PROXY")
if [ "$PLATFORM" = "Windows" ]; then
  CURL_FLAGS+=(--ssl-no-revoke)
fi
if curl "${CURL_FLAGS[@]}" -o /dev/null -w '  curl github.com -> HTTP %{http_code} in %{time_total}s\n' https://github.com; then
  :
else
  echo "  curl could not reach github.com via the proxy — check PROXY=$PROXY and your VPN." >&2
  if [ "$PLATFORM" = "macOS" ]; then
    echo "  (is the local proxy client running? did its port change? see: scutil --proxy)" >&2
  fi
fi
if git ls-remote https://github.com/git-fixtures/basic.git >/dev/null 2>&1; then
  echo "  git ls-remote github.com -> OK"
  echo
  echo "Done. Clone normally — e.g.:"
  echo "  git clone https://github.com/owner/repo.git"
else
  echo "  git ls-remote FAILED — git cannot reach GitHub through the proxy." >&2
fi

echo
echo "NOTE: these are GLOBAL settings. Off this network (home/other office, or"
echo "the local proxy app has quit) they will break git. Clear them with:"
echo "  git config --global --unset http.proxy && git config --global --unset https.proxy"
echo "(re-run this script when you're back on the corporate network.)"
