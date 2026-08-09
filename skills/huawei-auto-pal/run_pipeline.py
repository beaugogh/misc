#!/usr/bin/env python3
"""huawei-auto-pal pipeline runner — bakes the mechanical steps into one script.

Runs: check → provision → retro-scope, then prints a directive for the agent
to run skill-forge. After skill-forge, the agent runs `run_pipeline.py --archive`.

Usage:
    python run_pipeline.py                       # diagnose phase (check + provision + retro-scope)
    python run_pipeline.py --git-email <email>   # with git email for provision
    python run_pipeline.py --archive             # archive phase (zip output to Downloads)
    python run_pipeline.py --no-provision        # skip provision (re-runs)
    python run_pipeline.py --no-enrich-pages     # disable web page content extraction

This script handles the mechanical parts that don't need LLM reasoning.
The agent (Claude Code, codeagent, etc.) runs this script, reads the directive
at the end, then does skill-forge (which requires LLM analysis of findings).
"""

from __future__ import annotations

import sys
import os
import subprocess

# Python 3.9+ guard (same as run.py).
if sys.version_info < (3, 9):
    print(f"ERROR: Python 3.9+ required. You have {sys.version_info.major}."
          f"{sys.version_info.minor}.{sys.version_info.micro}.",
          file=sys.stderr)
    sys.exit(1)

# Resolve paths.
_HERE = os.path.dirname(os.path.abspath(__file__))
_RETRO_SCOPE = os.path.join(_HERE, "retro-scope", "scripts", "run.py")
_REGISTER = os.path.join(_HERE, "skill-forge", "scripts", "register.py")
_OUTPUT_DIR = os.path.join(_HERE, "output")

# Reconfigure stdout/stderr to UTF-8 (same as run.py and register.py).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass


def _run(cmd: list[str], timeout: int = 600) -> int:
    """Run a command, streaming output to the terminal. Returns exit code."""
    print(f"\n{'='*60}")
    print(f"$ {' '.join(cmd)}")
    print(f"{'='*60}\n")
    try:
        result = subprocess.run(cmd, timeout=timeout)
        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"\nERROR: command timed out after {timeout}s.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130


def _check_git_email() -> str | None:
    """Try to get git user.email from config."""
    try:
        result = subprocess.run(
            ["git", "config", "--global", "user.email"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


def phase_diagnose(git_email: str | None, skip_provision: bool,
                   skip_enrich: bool) -> int:
    """Run check → provision → retro-scope, then print skill-forge directive."""
    py = sys.executable

    # Step 1: Environment check
    print("\n# Step 1: Environment check")
    rc = _run([py, _RETRO_SCOPE, "--check"])
    if rc != 0:
        print(f"\nERROR: --check failed (exit {rc}).", file=sys.stderr)
        return rc

    # Step 2: Provision (if not skipped)
    if not skip_provision:
        print("\n# Step 2: Auto-provision welink-cli and git")
        # Determine git email: CLI arg > git config > None
        email = git_email or _check_git_email()
        provision_cmd = [py, _RETRO_SCOPE, "--provision"]
        if email:
            provision_cmd += ["--git-email", email]
        # --provision handles everything: install welink-cli, QR login, git config.
        # The QR code appears — user scans or lets it time out.
        rc = _run(provision_cmd, timeout=360)
        # Provision may return non-zero if auth timed out — that's OK, continue.
        if rc != 0:
            print(f"\nNOTE: provision did not fully complete (exit {rc}). "
                  f"Continuing with available sources.", file=sys.stderr)
    else:
        print("\n# Step 2: Provision skipped (--no-provision)")

    # Step 3: Retro-scope (multi-horizon, with page enrichment)
    print("\n# Step 3: Retro-scope multi-horizon analysis")
    retro_cmd = [py, _RETRO_SCOPE, "--horizons", "90d,30d,7d,1d"]
    if skip_enrich:
        retro_cmd.append("--no-enrich-pages")
    rc = _run(retro_cmd, timeout=900)
    if rc != 0:
        print(f"\nERROR: retro-scope failed (exit {rc}).", file=sys.stderr)
        return rc

    # Print the directive for the agent.
    index_path = os.path.join(_OUTPUT_DIR, "index.html")
    print(f"""
{'='*60}
DIAGNOSE PHASE COMPLETE.

Reports:      {index_path} (open in browser)
Session records: {os.path.join(_OUTPUT_DIR, 'session_records')}/
Tasks:        {os.path.join(_OUTPUT_DIR, 'tasks.jsonl')}
Top 10:       run `python retro-scope/scripts/run.py --top 10` for the ranked list

NEXT STEP (agent): Run skill-forge NOW. Do NOT ask the user whether to proceed.
  1. Read the top-10 time sinks and session records in output/session_records/
  2. Identify recurring patterns and validated problems
  3. Create skill/memory proposals in output/<skill-name>/PROPOSAL.md
  4. Run: python run_pipeline.py --archive
     (This zips the output — including proposals — to the user's Downloads.
     The zip is a diagnostic snapshot. It must be created BEFORE asking the
     user about installation, so the output is never blocked by that decision.
     A sentinel file (output/.archived) prevents double-archiving — if you
     run --archive again it will print "Already archived" and skip.
     Do NOT re-archive after the install step.)
  5. THEN present proposals to user (print PROPOSAL.md content as agent message)
  6. Ask which to install into which agents, run register.py --install
     (If the user declines all installs, the pipeline is DONE. Do NOT re-archive.)
{'='*60}
""")
    return 0


def phase_archive() -> int:
    """Run the archive phase (zip output to Downloads)."""
    py = sys.executable
    print("\n# Archive phase")
    rc = _run([py, _REGISTER, "--archive"], timeout=120)
    if rc != 0:
        print(f"\nERROR: archive failed (exit {rc}).", file=sys.stderr)
    return rc


def main():
    import argparse
    ap = argparse.ArgumentParser(
        prog="run_pipeline.py",
        description="huawei-auto-pal pipeline: check → provision → retro-scope → (skill-forge) → archive",
    )
    ap.add_argument("--git-email", default=None,
                    help="git user.email for provision (auto-detected from git config if omitted)")
    ap.add_argument("--archive", action="store_true",
                    help="run archive phase only (zip output to Downloads)")
    ap.add_argument("--no-provision", action="store_true",
                    help="skip the provision step")
    ap.add_argument("--no-enrich-pages", action="store_true",
                    help="disable web page content extraction in retro-scope")
    args = ap.parse_args()

    if args.archive:
        sys.exit(phase_archive())

    sys.exit(phase_diagnose(
        git_email=args.git_email,
        skip_provision=args.no_provision,
        skip_enrich=args.no_enrich_pages,
    ))


if __name__ == "__main__":
    main()
