#!/usr/bin/env python3
"""Registration helper — list unregistered output skills and install them.

Usage:
  python register.py --list              # show unregistered skills + detected agents
  python register.py --install <name>    # install one skill (asks which agent)
  python register.py --install-memory    # install personal-context memory
  python register.py --archive           # zip output/ to Downloads (personal backup)
  python register.py --dist              # zip whole skill for distribution to colleagues
  python register.py --dry-run --install <name>  # preview without writing

This is the concrete entry point that skill-forge step 8 calls at the end
of a run to gently offer registration to the user.
"""

from __future__ import annotations

import os
import sys
import platform
import argparse
import zipfile
import datetime
from pathlib import Path

# Make sibling modules importable.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

# Output dir is two levels up: skill-forge/scripts/ → huawei-auto-pal/output/
_OUTPUT_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "output"))
# Can be overridden via env var (same convention as persistence.py).
_OUTPUT_DIR = os.environ.get("SKILL_FORGE_OUTPUT_DIR", _OUTPUT_DIR)

from agent_targets import discover_agents, format_agents_report, AgentTarget
from skill_installer import install_skill, install_memory, InstallResult


def _find_output_skills(output_dir: str) -> list[str]:
    """Return names of skills in output/ (directories containing SKILL.md)."""
    skills: list[str] = []
    base = Path(output_dir)
    if not base.is_dir():
        return skills
    for entry in sorted(base.iterdir()):
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            # Skip non-skill directories.
            name = entry.name
            if name in (".skill-forge-backups", "session_records", "personal-context"):
                continue
            skills.append(name)
    return skills


def _is_installed(skill_name: str, agent: AgentTarget) -> bool:
    """Check if a skill is already registered in an agent's skills dir."""
    if agent.skills_dir is None:
        return False
    return (Path(agent.skills_dir) / skill_name).exists()


def cmd_list(args, agents, output_skills):
    """Print unregistered skills and detected agents."""
    print("# Skill registration status")
    print()
    if not output_skills:
        print("No skills found in output/. Nothing to register.")
        print()
    else:
        print("Skills in output/:")
        for name in output_skills:
            source = os.path.join(_OUTPUT_DIR, name)
            print(f"  {name}")
            installed_somewhere = False
            for agent in agents:
                if _is_installed(name, agent):
                    print(f"    ✓ {agent.display_name}")
                    installed_somewhere = True
                elif agent.skills_dir is not None:
                    print(f"    ✗ {agent.display_name} — not installed")
            if not installed_somewhere:
                print(f"    (not registered in any agent)")
            print()
    # Personal context.
    pc_path = os.path.join(_OUTPUT_DIR, "personal-context", "SKILL.md")
    if os.path.isfile(pc_path):
        print("Personal context (memory, not a skill):")
        for agent in agents:
            if agent.memory_format != "none":
                print(f"  {agent.display_name}: {agent.memory_format}")
        print()

    print(format_agents_report(agents))
    print()
    if output_skills:
        print("To register: python register.py --install <skill-name>")
    if os.path.isfile(pc_path):
        print("To install memory: python register.py --install-memory")


def cmd_install(args, agents, output_skills):
    """Install one skill into detected agents."""
    name = args.install
    source = os.path.join(_OUTPUT_DIR, name)
    if not os.path.isdir(source) or not os.path.isfile(os.path.join(source, "SKILL.md")):
        print(f"Error: skill '{name}' not found in output/", file=sys.stderr)
        sys.exit(1)

    if args.all_agents:
        targets = [a for a in agents if a.skills_dir is not None]
    else:
        # Let user pick interactively — but since this is called by an agent,
        # just list and install into all that support skills.
        targets = [a for a in agents if a.skills_dir is not None]

    if not targets:
        print("No agents with skill directories detected.", file=sys.stderr)
        sys.exit(1)

    any_success = False
    for agent in targets:
        if _is_installed(name, agent):
            print(f"  {agent.display_name}: already installed, skipping")
            continue
        result = install_skill(source, agent, dry_run=args.dry_run)
        status = "✓" if result.success else "✗"
        print(f"  {agent.display_name}: {status} {result.action} — {result.detail}")
        if result.success:
            any_success = True

    if any_success and not args.dry_run:
        print()
        print("Registration complete. Restart your agent to load the new skill.")


def cmd_install_memory(args, agents, output_skills):
    """Install personal-context memory into detected agents."""
    pc_path = os.path.join(_OUTPUT_DIR, "personal-context", "SKILL.md")
    if not os.path.isfile(pc_path):
        print("Error: personal-context/SKILL.md not found in output/", file=sys.stderr)
        sys.exit(1)

    targets = [a for a in agents if a.memory_format != "none"]
    if not targets:
        print("No agents with supported memory mechanisms detected.", file=sys.stderr)
        sys.exit(1)

    for agent in targets:
        result = install_memory(pc_path, agent, dry_run=args.dry_run)
        status = "✓" if result.success else "✗"
        print(f"  {agent.display_name}: {status} {result.action} — {result.detail}")


def _downloads_dir() -> str:
    """Return the user's default Downloads directory across platforms."""
    home = os.path.expanduser("~")
    system = platform.system()
    if system == "Windows":
        # Windows: %USERPROFILE%\Downloads (standard since Win7)
        return os.path.join(home, "Downloads")
    elif system == "Darwin":
        # macOS: ~/Downloads
        return os.path.join(home, "Downloads")
    else:
        # Linux: $XDG_DOWNLOAD_DIR or ~/Downloads
        xdg = os.environ.get("XDG_DOWNLOAD_DIR")
        if xdg:
            return xdg
        return os.path.join(home, "Downloads")


def cmd_archive(args, agents, output_skills):
    """Zip the output/ folder and save it to the user's Downloads directory."""
    output_path = Path(_OUTPUT_DIR)
    if not output_path.is_dir():
        print(f"Error: output directory not found at {_OUTPUT_DIR}", file=sys.stderr)
        sys.exit(1)

    downloads = _downloads_dir()
    os.makedirs(downloads, exist_ok=True)

    # Build a timestamped filename: huawei-auto-pal-output-YYYYMMDD-HHMMSS.zip
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"huawei-auto-pal-output-{timestamp}.zip"
    zip_path = os.path.join(downloads, zip_name)

    # Count skills (directories with SKILL.md) for the summary.
    skill_count = len(output_skills)

    if args.dry_run:
        print(f"Would zip {_OUTPUT_DIR} → {zip_path}")
        print(f"  ({skill_count} skill(s), {len(agents)} agent(s) detected)")
        return

    # Create the zip, excluding __pycache__ and .skill-forge-backups.
    skip_dirs = {"__pycache__", ".skill-forge-backups"}
    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(_OUTPUT_DIR):
            # Filter out skip dirs in-place so os.walk doesn't descend into them.
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for fname in files:
                fpath = os.path.join(root, fname)
                arcname = os.path.relpath(fpath, _OUTPUT_DIR)
                zf.write(fpath, arcname)
                file_count += 1

    zip_size = os.path.getsize(zip_path)
    size_str = f"{zip_size / 1024:.0f} KB" if zip_size < 1024 * 1024 else f"{zip_size / 1024 / 1024:.1f} MB"
    print(f"✓ Output archived to: {zip_path}")
    print(f"  {file_count} files, {size_str}")
    if skill_count == 0:
        print(f"  ⚠ No skills found in output/ — only reports and session records were archived.")
        print(f"    Generated skills should be written to output/<skill-name>/ before archiving.")
    else:
        print(f"  {skill_count} skill(s) included: {', '.join(output_skills)}")


# --- Skill folder root for --dist. ---
# register.py lives at skill-forge/scripts/register.py.
# The distributable skill root is three levels up: scripts/ → skill-forge/ → huawei-auto-pal/.
_SKILL_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))


def cmd_dist(args, agents, output_skills):
    """Zip the whole huawei-auto-pal skill folder for distribution to colleagues.

    Excludes personal data (output/), all hidden files (anything starting with '.',
    per AgentCenter's HIDDEN_FILE rule — covers .env, .gitignore, etc.), and build
    artifacts (__pycache__/, *.pyc, .skill-forge-backups) so the archive contains
    only shareable skill code.
    """
    skill_root = Path(_SKILL_ROOT)
    if not skill_root.is_dir():
        print(f"Error: skill root not found at {_SKILL_ROOT}", file=sys.stderr)
        sys.exit(1)

    downloads = _downloads_dir()
    os.makedirs(downloads, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"huawei-auto-pal-{timestamp}.zip"
    zip_path = os.path.join(downloads, zip_name)

    if args.dry_run:
        print(f"Would zip {_SKILL_ROOT} → {zip_path}")
        return

    # AgentCenter rejects hidden files (anything starting with '.') and
    # bytecode caches. Exclude output/ (personal data) and .skill-forge-backups.
    skip_dirs = {"__pycache__", ".skill-forge-backups", "output"}
    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(_SKILL_ROOT):
            # Drop hidden and skip dirs in-place so os.walk doesn't descend.
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
            for fname in files:
                if fname.startswith(".") or fname.endswith((".pyc", ".pyo")):
                    continue
                fpath = os.path.join(root, fname)
                # Archive paths are relative to the skill root, so the zip
                # extracts as huawei-auto-pal/... on the colleague's machine.
                arcname = os.path.relpath(fpath, _SKILL_ROOT)
                # Prepend the skill folder name so it extracts into a single dir.
                arcname = os.path.join(skill_root.name, arcname)
                zf.write(fpath, arcname)
                file_count += 1

    zip_size = os.path.getsize(zip_path)
    size_str = f"{zip_size / 1024:.0f} KB" if zip_size < 1024 * 1024 else f"{zip_size / 1024 / 1024:.1f} MB"
    print(f"✓ Skill package saved to: {zip_path}")
    print(f"  {file_count} files, {size_str}")
    print(f"  Upload this zip to AgentCenter to share with colleagues.")


def main():
    ap = argparse.ArgumentParser(
        description="Register output skills and memory into installed agents."
    )
    ap.add_argument("--list", action="store_true",
                    help="list unregistered skills and detected agents")
    ap.add_argument("--install", metavar="NAME",
                    help="install a skill from output/ into detected agents")
    ap.add_argument("--install-memory", action="store_true",
                    help="install personal-context memory into detected agents")
    ap.add_argument("--archive", action="store_true",
                    help="zip output/ and save to the user's Downloads folder")
    ap.add_argument("--dist", action="store_true",
                    help="zip the whole skill folder (excl. personal data) for sharing with colleagues")
    ap.add_argument("--dry-run", action="store_true",
                    help="preview without writing anything")
    ap.add_argument("--all-agents", action="store_true",
                    help="install into all detected agents (default)")
    args = ap.parse_args()

    # --archive, --dist, --install, --install-memory are mutually exclusive
    # packaging/action modes. Passing more than one silently shadows the others.
    mode_count = sum(1 for m in (args.archive, args.dist, bool(args.install), args.install_memory) if m)
    if mode_count > 1:
        print("Error: --archive, --dist, --install, and --install-memory are mutually exclusive.",
              file=sys.stderr)
        sys.exit(1)

    agents = discover_agents()
    output_skills = _find_output_skills(_OUTPUT_DIR)

    if args.archive:
        cmd_archive(args, agents, output_skills)
    elif args.dist:
        cmd_dist(args, agents, output_skills)
    elif args.list or (not args.install and not args.install_memory):
        cmd_list(args, agents, output_skills)
    elif args.install:
        cmd_install(args, agents, output_skills)
    elif args.install_memory:
        cmd_install_memory(args, agents, output_skills)


if __name__ == "__main__":
    main()
