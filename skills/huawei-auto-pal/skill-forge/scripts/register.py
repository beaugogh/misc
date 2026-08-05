#!/usr/bin/env python3
"""Registration helper — list unregistered output skills and install them.

Usage:
  python register.py --list              # show unregistered skills + detected agents
  python register.py --install <name>    # install one skill (asks which agent)
  python register.py --install-memory    # install personal-context memory
  python register.py --dry-run --install <name>  # preview without writing

This is the concrete entry point that skill-forge step 8 calls at the end
of a run to gently offer registration to the user.
"""

from __future__ import annotations

import os
import sys
import argparse
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
    ap.add_argument("--dry-run", action="store_true",
                    help="preview without writing anything")
    ap.add_argument("--all-agents", action="store_true",
                    help="install into all detected agents (default)")
    args = ap.parse_args()

    agents = discover_agents()
    output_skills = _find_output_skills(_OUTPUT_DIR)

    if args.list or (not args.install and not args.install_memory):
        cmd_list(args, agents, output_skills)
    elif args.install:
        cmd_install(args, agents, output_skills)
    elif args.install_memory:
        cmd_install_memory(args, agents, output_skills)


if __name__ == "__main__":
    main()
