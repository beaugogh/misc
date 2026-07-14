#!/usr/bin/env python3
"""Download Python wheels through a stall-prone corporate proxy.

PROBLEM
  pip hangs forever on large wheels (>~3 MB) behind the corporate proxy: the
  proxy silently drops sustained transfers but keeps the TCP connection open,
  so pip's --timeout never fires. Small wheels come through fine; only the big
  ones stall. A transient 407 Proxy Authentication Required also appears.

FIX
  Resolve exact wheel URLs from the PyPI JSON API and download each with curl
  --speed-limit / --speed-time (aborts on low throughput, which actually kills
  the stall) + --retry-all-errors (rides out 407 windows). Then pip-install
  from the local files. See SKILL.md for the full diagnosis.

USAGE
  python fetch_wheels.py <pkg> [<pkg> ...]              # download to ./wheels
  python fetch_wheels.py --install <pkg> [<pkg> ...]    # download + pip install
  python fetch_wheels.py --dir <path> <pkg> ...         # custom output dir

ENV
  PROXY   proxy URL, e.g. http://proxyuk.huawei.com:8080
          (default: Windows registry ProxyServer value)
  curl must be on PATH (Git Bash / Windows 10+ ship it).
"""
import json
import os
import platform
import re
import subprocess
import sys


def default_proxy():
    """Read the proxy from the Windows registry (authoritative — same value the browser uses)."""
    if platform.system() == "Windows":
        try:
            out = subprocess.check_output(
                ["reg", "query",
                 r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                 "/v", "ProxyServer"], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                if "ProxyServer" in line:
                    val = line.strip().split()[-1]
                    if val and not val.startswith("http"):
                        val = "http://" + val
                    return val
        except Exception:
            pass
    return os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY", "")


def best_wheel(release_files, cp, plat, running_minor):
    """Highest-priority wheel matching this interpreter; None if none compatible.

    Priority: exact cpXY-cpXY-plat > abi3-plat (minor <= running) > py3-none-plat
    > py3-none-any > py2.py3-none-any. abi3 wheels whose minimum minor is newer
    than the running Python are rejected (they won't import).
    """
    wheels = [f for f in release_files if f["filename"].endswith(".whl")]

    def score(f):
        n = f["filename"]
        has_plat = plat in n
        if f"{cp}-{cp}-" in n and has_plat:          # cp312-cp312-win_amd64
            return 5
        if "abi3" in n and has_plat:                 # cp311-abi3-win_amd64
            m = re.search(r"cp(\d+)-abi3", n)
            if m and int(m.group(1)) <= running_minor:
                return 4
            return -1                                # abi3 needs a newer Python
        if "py3-none-" in n and has_plat:            # py3-none-win_amd64
            return 3
        if "py3-none-any" in n:                      # py3-none-any
            return 2
        if "py2.py3-none-any" in n:                  # py2.py3-none-any
            return 1
        return 0

    scored = [(score(f), f) for f in wheels]
    scored = [(s, f) for s, f in scored if s > 0]
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def curl_json(url, proxy):
    """Fetch + parse JSON via curl (small payload; --ssl-no-revoke avoids the schannel hang)."""
    out = subprocess.check_output(
        ["curl", "-sS", "-L", "-m", "30", "-x", proxy, "--ssl-no-revoke", url],
        text=True)
    return json.loads(out)


def curl_download(url, dest, proxy):
    """Download a wheel with throughput-based stall killing + 407 retry."""
    subprocess.run(
        ["curl", "-sS", "-L", "-x", proxy, "--ssl-no-revoke",
         "--retry", "5", "--retry-all-errors", "--retry-delay", "3",
         "--speed-limit", "2000", "--speed-time", "15",   # <2 KB/s for 15s -> abort+retry
         "-o", dest, url], check=True)


def main():
    args = sys.argv[1:]
    do_install = False
    out_dir = os.path.join(os.getcwd(), "wheels")
    pkgs, i = [], 0
    while i < len(args):
        a = args[i]
        if a == "--install":
            do_install = True
        elif a == "--dir":
            out_dir = args[i + 1]
            i += 1
        else:
            pkgs.append(a)
        i += 1
    if not pkgs:
        print(__doc__)
        sys.exit(1)

    proxy = os.environ.get("PROXY") or default_proxy()
    if not proxy:
        sys.exit("No proxy found. Set PROXY env var or the ProxyServer registry value.")

    cp = f"cp{sys.version_info[0]}{sys.version_info[1]}"
    running_minor = sys.version_info[0] * 10 + sys.version_info[1]
    plat = "win_amd64" if platform.system() == "Windows" else "manylinux2014_x86_64"
    os.makedirs(out_dir, exist_ok=True)
    print(f"proxy={proxy}  python={cp}  platform={plat}  out={out_dir}")

    local = []
    for pkg in pkgs:
        try:
            data = curl_json(f"https://pypi.org/pypi/{pkg}/json", proxy)
        except subprocess.CalledProcessError as e:
            print(f"  {pkg}: FAILED to fetch metadata ({e})")
            continue
        ver = data["info"]["version"]
        wh = best_wheel(data["releases"].get(ver, []), cp, plat, running_minor)
        if not wh:
            print(f"  {pkg} {ver}: no compatible wheel for {cp}/{plat}")
            continue
        dest = os.path.join(out_dir, wh["filename"])
        print(f"  {pkg} {ver}: {wh['filename']} ({wh['size'] // 1024} KB)")
        if os.path.exists(dest) and os.path.getsize(dest) == wh["size"]:
            print("    cached")
        else:
            curl_download(wh["url"], dest, proxy)
            print("    downloaded")
        local.append(dest)

    if do_install:
        if not local:
            sys.exit("No wheels to install.")
        print("\npip install (local big wheels + small deps from PyPI)...")
        # env-var proxy (NOT pip config global.proxy) — see SKILL.md: env var forwards
        # auth reliably where pip config fails with 407 on this network.
        env = dict(os.environ, HTTP_PROXY=proxy, HTTPS_PROXY=proxy)
        subprocess.run(
            [sys.executable, "-m", "pip", "install",
             "--retries", "3", "--timeout", "60", *local],
            check=True, env=env)
        print("done.")


if __name__ == "__main__":
    main()
