#!/usr/bin/env python3
"""Run the bundled WeChat exporter against an authorized Finder/iTunes backup."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--account")
    parser.add_argument("--session", action="append", default=[])
    parser.add_argument("--format", choices=("html", "text"), default="html")
    parser.add_argument(
        "--asyncloading", choices=("sync", "onscroll", "oninit"), default="onscroll"
    )
    parser.add_argument("--filter", choices=("no", "yes"), default="no")
    args = parser.parse_args()

    backup = args.backup.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not backup.is_dir():
        parser.error(f"backup directory does not exist: {backup}")
    if not (backup / "Manifest.db").is_file():
        parser.error(f"not a Finder/iTunes backup (Manifest.db missing): {backup}")
    output.mkdir(parents=True, exist_ok=True)

    runtime = (
        Path(__file__).resolve().parent.parent
        / "vendor"
        / "wechat-exporter-1.9.5.13"
    )
    binary = runtime / "WechatExporterCmd"
    if not binary.is_file():
        parser.error(f"bundled exporter is missing: {binary}")

    command = [
        str(binary),
        f"--backup={backup}",
        f"--output={output}",
        f"--format={args.format}",
        f"--asyncloading={args.asyncloading}",
        f"--filter={args.filter}",
    ]
    if args.account:
        command.append(f"--account={args.account}")
    command.extend(f"--session={name}" for name in args.session)

    env = os.environ.copy()
    env.update({"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"})
    return subprocess.run(command, cwd=runtime, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
