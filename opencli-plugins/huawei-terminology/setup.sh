#!/usr/bin/env bash
# Set up the huawei-terminology OpenCLI plugin on this machine.
#
# Handles the AUTOMATABLE parts: verifies opencli + the Browser Bridge, installs
# the plugin, ensures the @jackwener/opencli peer-dep symlink, and verifies with
# a real search.
#
# The NON-automatable parts (installing the Chrome Browser Bridge extension and
# signing into 3ms.huawei.com) must be done by a human first — see the
# "Prerequisites (human, one-time)" section in README.md. `opencli doctor` below
# gates on the extension, and the final search gates on the Huawei login.
#
# Usage:
#   ./setup.sh                 # from this directory
#   bash setup.sh              # if not executable
#
# Safe to re-run.

set -euo pipefail

# Colors for the human-step callout.
RED=$'\033[31m'; YELLOW=$'\033[33m'; GREEN=$'\033[32m'; BOLD=$'\033[1m'; RESET=$'\033[0m'

# Resolve the plugin directory (this script lives next to search.ts).
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_NAME="huawei-terminology"

say() { printf '%s\n' "$*"; }
ok()  { printf "${GREEN}✓${RESET} %s\n" "$*"; }
warn(){ printf "${YELLOW}!${RESET} %s\n" "$*"; }
die() { printf "${RED}✗${RESET} %s\n" "$*" >&2; exit 1; }

# --- 1. Node + opencli -----------------------------------------------------
command -v node >/dev/null 2>&1 || die "Node.js not found. Install Node >= 20 first: https://nodejs.org"
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
[ "$NODE_MAJOR" -ge 20 ] || die "Node $NODE_MAJOR found; OpenCLI needs >= 20."

if ! command -v opencli >/dev/null 2>&1; then
  say "Installing @jackwener/opencli globally…"
  npm install -g @jackwener/opencli || die "npm install -g @jackwener/opencli failed"
fi
ok "opencli $(opencli --version) on PATH"

# --- 2. Browser Bridge (HUMAN gate) ---------------------------------------
# `opencli doctor` exits non-zero if the Chrome extension / daemon / profile
# aren't connected. The extension install + Chrome sign-in are the parts a
# human must do — an agent can't.
if ! opencli doctor >/dev/null 2>&1; then
  printf '\n%s%s%sAction needed — a human must do this (an agent cannot):%s\n\n' "$BOLD" "$YELLOW" "" "$RESET"
  printf '  %s1. Install the OpenCLI Browser Bridge extension in Chrome%s\n' "$BOLD" "$RESET"
  printf '     Chrome Web Store: https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk\n'
  printf '     (or load it unpacked from the GitHub Releases zip — see opencli-plugins/README.md)\n\n'
  printf '  %s2. Open Chrome and keep it running%s (OpenCLI drives your logged-in Chrome tab).\n\n' "$BOLD" "$RESET"
  printf 'Then re-run:  ./setup.sh\n\n'
  die "opencli doctor is not green — Browser Bridge not connected."
fi
ok "opencli doctor is green (Browser Bridge connected)"

# --- 3. Install the plugin -------------------------------------------------
say "Installing plugin from $PLUGIN_DIR …"
# Pass the bare absolute path — `file://` with a Unix-style path is rejected
# on Windows. Re-running install on an already-installed plugin is a no-op
# (it prints "already installed" and exits 0), so this is safe to re-run.
install_out="$(opencli plugin install "$PLUGIN_DIR" 2>&1)" || {
  # "already installed" exits 1 but is fine — treat it as success.
  case "$install_out" in
    *"already installed"*) : ;;
    *) printf '%s\n' "$install_out" | sed 's/^/    /' >&2
       die "opencli plugin install failed" ;;
  esac
}
ok "plugin installed"

# --- 4. Ensure the @jackwener/opencli peer-dep resolves --------------------
# The plugin imports @jackwener/opencli/registry. Node's ESM resolver walks UP
# from the importing file, so the peer-dep does NOT need to live inside the
# plugin dir — it resolves from any ancestor node_modules. We hoist it to the
# REPO ROOT so the plugin dir stays clean (no per-plugin node_modules, which is
# an anti-pattern when several plugins could share one resolution).
#
# `opencli plugin install` symlinks the plugin into ~/.opencli/plugins/, which
# points back here, so the root node_modules is still on the upward walk.
# (node_modules/ is gitignored, so it is never committed.)
REPO_ROOT="$(cd "$PLUGIN_DIR/../.." && pwd)"
GLOBAL_OPENCLI="$(npm root -g 2>/dev/null)/@jackwener/opencli"
LINK_TARGET="$REPO_ROOT/node_modules/@jackwener/opencli"
if [ ! -e "$LINK_TARGET" ]; then
  mkdir -p "$REPO_ROOT/node_modules/@jackwener"
  if [ -e "$GLOBAL_OPENCLI" ]; then
    ln -s "$GLOBAL_OPENCLI" "$LINK_TARGET"
    ok "linked @jackwener/opencli -> $GLOBAL_OPENCLI (at repo root)"
  else
    die "global @jackwener/opencli not found at $GLOBAL_OPENCLI — run 'npm install -g @jackwener/opencli' and re-run setup."
  fi
else
  ok "peer-dep symlink already present (at repo root)"
fi
# Remove any stale per-plugin node_modules from older setup.sh runs — keeping
# it would shadow the root symlink and recreate the anti-pattern we just fixed.
if [ -e "$PLUGIN_DIR/node_modules/@jackwener" ]; then
  rm -rf "$PLUGIN_DIR/node_modules"
  ok "removed stale per-plugin node_modules (now resolved from repo root)"
fi

# --- 5. Verify the command is registered ----------------------------------
# `opencli list` prints the plugin name on one line and the command on the next
# ("  huawei-terminology\n    search [cookie] — …"), so match the pair.
if ! opencli list 2>&1 | grep -A1 -qE "^\s*$PLUGIN_NAME\s*$"; then
  die "plugin not listed in 'opencli list' — run 'opencli list' to inspect."
fi
ok "'$PLUGIN_NAME search' registered"

# --- 6. Smoke test (also gates on Huawei login) ----------------------------
# A real search needs a logged-in Huawei session. If this fails with an auth
# error, the human must sign into 3ms.huawei.com in Chrome first.
say "Smoke test: searching '5G' --limit 1 …"
if out="$(opencli huawei-terminology search "5G" --limit 1 2>&1)"; then
  printf '%s\n' "$out" | sed 's/^/    /'
  ok "smoke test passed — plugin is ready"
  printf '\n%sDone.%s  Try:  opencli huawei-terminology search "CloudDragon"\n' "$GREEN" "$RESET"
else
  rc=$?
  printf '\n%sSmoke test failed — likely the Huawei session:%s\n' "$YELLOW" "$RESET"
  printf '%s\n' "$out" | sed 's/^/    /'
  printf '\n%s%sAction needed — a human must do this (an agent cannot):%s\n\n' "$BOLD" "$YELLOW" "$RESET"
  printf '  Open https://3ms.huawei.com/terminology in Chrome and sign in with your Huawei account,\n'
  printf '  then re-run:  ./setup.sh\n\n'
  die "smoke test failed (exit $rc) — Huawei session may be missing or expired."
fi
