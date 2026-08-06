#!/usr/bin/env python3
"""Registration helper — list unregistered output skills and install them.

Usage:
  python register.py --list                          # show skills, agents, problem summaries
  python register.py --present                       # show ALL bilingual proposals in one command
  python register.py --describe <name>               # show one skill's full bilingual PROPOSAL.md
  python register.py --install <name> --agent <ids>  # install into specific agents
  python register.py --install <name> --all-agents   # install into every detected agent
  python register.py --install-memory --agent <ids>  # install personal-context memory
  python register.py --archive                       # zip output/ to Downloads (personal backup)
  python register.py --dist                          # zip whole skill for distribution to colleagues
  python register.py --dry-run --install <name> --agent <id>  # preview without writing

Agent IDs: claude_code, codeagent, opencode, codex, openclaw, hermes.
Use --agent with a comma-separated list to choose which agents receive the
skill. Without --agent or --all-agents, --install lists agents and exits.

This is the concrete entry point that skill-forge step 8 calls at the end
of a run to present proposals and install skills into the user's agents.
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


def _safe_output_subpath(name: str) -> str:
    """Resolve name as a subdirectory of output/, rejecting path traversal.

    The name comes from CLI args (--describe, --install) which may carry
    untrusted text from AI-session traces. Ensure the resolved path stays
    inside output/ so '../' cannot escape to read or copy arbitrary files.
    """
    base = os.path.normpath(_OUTPUT_DIR)
    resolved = os.path.normpath(os.path.join(base, name))
    if not (resolved == base or resolved.startswith(base + os.sep)):
        print(f"Error: '{name}' resolves outside output/ — path traversal blocked.",
              file=sys.stderr)
        sys.exit(1)
    return resolved


def _read_frontmatter_description(skill_dir: str) -> str | None:
    """Read the `description` field from a skill's SKILL.md frontmatter.

    Tries PyYAML first (handles folded scalars >-, >, block scalars |, quoted
    values, multi-line). Falls back to a line-scrape for frontmatter that is
    not strictly valid YAML — skill authors often write plain-text
    descriptions containing unquoted colons, which PyYAML rejects but a
    line-scrape handles. Returns None if the file or field is missing.
    """
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    # Split on lines that are exactly "---" to avoid matching the substring
    # inside frontmatter values (e.g. description: "a---b").
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    fm_text = "\n".join(fm_lines)

    # Try strict YAML first (handles folded/block scalars, quoted values).
    import yaml
    try:
        fm = yaml.safe_load(fm_text)
        if isinstance(fm, dict):
            desc = fm.get("description")
            if isinstance(desc, str) and desc.strip():
                return desc.strip()
    except yaml.YAMLError:
        pass  # Fall through to line-scrape for loose plain-text values.

    # Fallback: line-scrape the description value. This handles plain-text
    # descriptions with unquoted colons (common in skill frontmatter).
    in_folded = False
    for i, line in enumerate(fm_lines):
        stripped = line.strip()
        if in_folded and stripped:
            return stripped
        if stripped.startswith("description:"):
            desc = stripped[len("description:"):].strip()
            if desc in (">-", ">", "|", "|-"):
                in_folded = True
                continue
            if desc:
                return desc
    return None


def _proposal_summary(skill_name: str) -> tuple[str, bool]:
    """Return a one-line problem summary for a skill in output/.

    Extracts the first non-empty non-heading line under '## Problem' from
    PROPOSAL.md. Falls back to the frontmatter `description` if no PROPOSAL.md
    exists. Returns (summary, has_proposal).
    """
    proposal_path = os.path.join(_OUTPUT_DIR, skill_name, "PROPOSAL.md")
    # _safe_output_subpath is not called here because skill_name flows from
    # _find_output_skills (trusted directory listing), not CLI input.
    if os.path.isfile(proposal_path):
        try:
            with open(proposal_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError:
            pass
        else:
            in_problem = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("## "):
                    in_problem = stripped.lower().startswith("## problem")
                    continue
                if in_problem and stripped and not stripped.startswith("#"):
                    # Skip [EN]/[ZH] language markers — they're structural
                    # labels, not content. The actual problem text follows.
                    if stripped in ("[EN]", "[ZH]"):
                        continue
                    return stripped, True
    # Fallback: frontmatter description.
    skill_dir = os.path.join(_OUTPUT_DIR, skill_name)
    desc = _read_frontmatter_description(skill_dir)
    if desc:
        return desc, False
    return "(no description available)", False


def _parse_agent_ids(value: str, agents: list[AgentTarget]) -> list[AgentTarget]:
    """Parse a comma-separated --agent value into a list of AgentTargets.

    Validates each ID against detected agents. Exits with an error listing
    valid IDs if any ID is unknown or not detected on this machine.
    """
    valid = {a.agent_id: a for a in agents}
    ids = list(dict.fromkeys(s.strip() for s in value.split(",") if s.strip()))
    if not ids:
        print("Error: --agent requires at least one agent ID.", file=sys.stderr)
        print(f"  Detected agents: {', '.join(valid) or '(none)'}", file=sys.stderr)
        sys.exit(1)
    unknown = [i for i in ids if i not in valid]
    if unknown:
        print(f"Error: unknown or undetected agent ID(s): {', '.join(unknown)}",
              file=sys.stderr)
        print(f"  Detected agents: {', '.join(valid) or '(none)'}", file=sys.stderr)
        sys.exit(1)
    return [valid[i] for i in ids]


def cmd_list(args, agents, output_skills):
    """Print unregistered skills, detected agents, and problem summaries."""
    print("# Skill registration status")
    print()
    if not output_skills:
        print("No skills found in output/. Nothing to register.")
        print()
    else:
        print("Skills in output/:")
        for name in output_skills:
            summary, has_proposal = _proposal_summary(name)
            tag = "" if has_proposal else "  (from description)"
            print(f"  {name}")
            print(f"    Problem: {summary}{tag}")
            installed_somewhere = False
            for agent in agents:
                if agent.skills_dir is None:
                    continue
                if _is_installed(name, agent):
                    print(f"    ✓ {agent.display_name} — installed")
                    installed_somewhere = True
                else:
                    print(f"    ✗ {agent.display_name} — not installed")
            if not installed_somewhere:
                print(f"    (not registered in any agent)")
            print()
    # Personal context.
    pc_path = os.path.join(_OUTPUT_DIR, "personal-context", "SKILL.md")
    if os.path.isfile(pc_path):
        print("Personal context (memory, not a skill):")
        summary, has_proposal = _proposal_summary("personal-context")
        tag = "" if has_proposal else "  (from description)"
        print(f"  Summary: {summary}{tag}")
        for agent in agents:
            if agent.memory_format != "none":
                print(f"  {agent.display_name}: {agent.memory_format}")
        print()

    print(format_agents_report(agents))
    print()
    if output_skills:
        print("To see full proposal:    python register.py --describe <skill-name>")
        print("To install into an agent: python register.py --install <name> --agent <agent-id>")
        print("  (agent IDs: %s)" % ", ".join(a.agent_id for a in agents if a.skills_dir is not None))
        print("  use --all-agents to install into every detected agent")
    if os.path.isfile(pc_path):
        print("To install memory:        python register.py --install-memory --agent <agent-id>")


def cmd_describe(args, agents, output_skills):
    """Print the full bilingual PROPOSAL.md for a skill or memory.

    Falls back to the frontmatter description if no PROPOSAL.md exists.
    """
    name = args.describe
    # Accept 'personal-context' for memory, or any skill name.
    skill_dir = _safe_output_subpath(name)
    proposal_path = os.path.join(skill_dir, "PROPOSAL.md")
    skill_md = os.path.join(skill_dir, "SKILL.md")

    # personal-context is memory, not a skill — it may have a PROPOSAL.md
    # without a SKILL.md, so skip the SKILL.md existence check for it.
    if not os.path.isfile(skill_md) and name != "personal-context":
        print(f"Error: '{name}' not found in output/", file=sys.stderr)
        sys.exit(1)

    if os.path.isfile(proposal_path):
        with open(proposal_path, "r", encoding="utf-8") as f:
            print(f.read(), end="")
    else:
        # Fallback: frontmatter description.
        desc = _read_frontmatter_description(os.path.join(_OUTPUT_DIR, name))
        if desc:
            print(f"# {name}")
            print()
            print("(No detailed PROPOSAL.md available. Showing frontmatter description.)")
            print()
            print(f"Description: {desc}")
        else:
            print(f"# {name}")
            print()
            print("(No PROPOSAL.md or description available for this skill.)")


def cmd_present(args, agents, output_skills):
    """Print the full bilingual proposals for ALL skills + memory in one command.

    Primarily for manual CLI debugging. The agent reads PROPOSAL.md files
    directly per step 8 (not via this command) because Bash tool output is
    collapsed in the terminal and the user won't see it. This command remains
    useful for checking proposals from the command line.

    Prints each skill's full PROPOSAL.md (or frontmatter description fallback)
    regardless of install status — the user should see the reasoning for
    everything in output/, not just uninstalled skills. Memory
    (personal-context) is included last.
    """
    if not output_skills and not os.path.isfile(
        os.path.join(_OUTPUT_DIR, "personal-context", "SKILL.md")
    ):
        print("No skills or memory found in output/. Nothing to present.")
        return

    print("=" * 70)
    print("# Skill Proposals — Bilingual (English / 中文)")
    print("# 技能提案 — 中英双语")
    print("=" * 70)
    print()

    for name in output_skills:
        print("-" * 70)
        _print_proposal(name)
        print()
        # Show install status for this skill.
        installed_in = [
            a.display_name for a in agents
            if a.skills_dir is not None and _is_installed(name, a)
        ]
        if installed_in:
            print(f"  [Already installed in: {', '.join(installed_in)}]")
        else:
            print(f"  [Not yet installed in any agent]")
        print()

    # Personal context memory.
    pc_path = os.path.join(_OUTPUT_DIR, "personal-context", "SKILL.md")
    if os.path.isfile(pc_path):
        print("-" * 70)
        _print_proposal("personal-context")
        print()
        print(f"  [Memory — not a skill. Install via: --install-memory --agent <id>]")
        print()

    print("=" * 70)
    print("# To install:")
    print("#   python register.py --install <skill-name> --agent <agent-id>")
    print("#   python register.py --install-memory --agent <agent-id>")
    print("#   (agent IDs: %s)" % ", ".join(a.agent_id for a in agents if a.skills_dir is not None))
    print("#   use --all-agents to install into every detected agent")
    print("=" * 70)


def _print_proposal(name: str):
    """Print the full PROPOSAL.md for a skill/memory, or the fallback."""
    skill_dir = _safe_output_subpath(name)
    proposal_path = os.path.join(skill_dir, "PROPOSAL.md")
    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(skill_md) and name != "personal-context":
        print(f"Error: '{name}' not found in output/", file=sys.stderr)
        return

    if os.path.isfile(proposal_path):
        with open(proposal_path, "r", encoding="utf-8") as f:
            print(f.read(), end="")
    else:
        desc = _read_frontmatter_description(skill_dir)
        if desc:
            print(f"# {name}")
            print()
            print("(No detailed PROPOSAL.md available. Showing frontmatter description.)")
            print()
            print(f"Description: {desc}")
        else:
            print(f"# {name}")
            print()
            print("(No PROPOSAL.md or description available for this skill.)")


def cmd_install(args, agents, output_skills):
    """Install one skill into selected agents.

    Agent selection:
    - --agent codeagent,claude_code : install into those specific agents
    - --all-agents                   : install into every detected agent with a skills dir
    - neither                        : list agents and exit without installing
    """
    name = args.install
    source = _safe_output_subpath(name)
    if not os.path.isdir(source) or not os.path.isfile(os.path.join(source, "SKILL.md")):
        print(f"Error: skill '{name}' not found in output/", file=sys.stderr)
        sys.exit(1)

    # Resolve which agents to install into.
    skill_agents = [a for a in agents if a.skills_dir is not None]
    if args.all_agents:
        targets = skill_agents
    elif args.agent:
        targets = _parse_agent_ids(args.agent, agents)
        # Filter to those that support skills.
        no_skill = [a.display_name for a in targets if a.skills_dir is None]
        if no_skill:
            print(f"Warning: {', '.join(no_skill)} do not support skill directories, skipping",
                  file=sys.stderr)
        targets = [a for a in targets if a.skills_dir is not None]
    else:
        # No selection made — list available agents and exit.
        print(f"Skill '{name}' is ready to install. Select an agent:")
        print()
        for a in skill_agents:
            status = "✓ installed" if _is_installed(name, a) else "✗ not installed"
            print(f"  {a.agent_id:15s}  {a.display_name}  ({status})")
        print()
        print("Run: python register.py --install %s --agent <agent-id>" % name)
        print("  (comma-separate multiple IDs, or use --all-agents)")
        return

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
    """Install personal-context memory into selected agents.

    Agent selection works the same as --install:
    - --agent codeagent,claude_code : install into those specific agents
    - --all-agents                   : install into every detected agent with memory support
    - neither                        : list agents and exit without installing
    """
    pc_path = os.path.join(_OUTPUT_DIR, "personal-context", "SKILL.md")
    if not os.path.isfile(pc_path):
        print("Error: personal-context/SKILL.md not found in output/", file=sys.stderr)
        sys.exit(1)

    memory_agents = [a for a in agents if a.memory_format != "none"]
    if args.all_agents:
        targets = memory_agents
    elif args.agent:
        targets = _parse_agent_ids(args.agent, agents)
        # Filter to those that support memory.
        no_mem = [a.display_name for a in targets if a.memory_format == "none"]
        if no_mem:
            print(f"Warning: {', '.join(no_mem)} do not support memory installation, skipping",
                  file=sys.stderr)
        targets = [a for a in targets if a.memory_format != "none"]
    else:
        # No selection made — list available agents and exit.
        print("Personal-context memory is ready to install. Select an agent:")
        print()
        for a in memory_agents:
            print(f"  {a.agent_id:15s}  {a.display_name}  ({a.memory_format})")
        print()
        print("Run: python register.py --install-memory --agent <agent-id>")
        print("  (comma-separate multiple IDs, or use --all-agents)")
        return

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
                    help="list unregistered skills, detected agents, and problem summaries")
    ap.add_argument("--present", action="store_true",
                    help="print full bilingual proposals for ALL skills + memory in one command")
    ap.add_argument("--describe", metavar="NAME",
                    help="print the full bilingual PROPOSAL.md for one skill or memory")
    ap.add_argument("--install", metavar="NAME",
                    help="install a skill from output/ into selected agents (use --agent)")
    ap.add_argument("--install-memory", action="store_true",
                    help="install personal-context memory into selected agents (use --agent)")
    ap.add_argument("--agent", metavar="IDS",
                    help="comma-separated agent IDs to install into (e.g. codeagent,claude_code)")
    ap.add_argument("--archive", action="store_true",
                    help="zip output/ and save to the user's Downloads folder")
    ap.add_argument("--dist", action="store_true",
                    help="zip the whole skill folder (excl. personal data) for sharing with colleagues")
    ap.add_argument("--dry-run", action="store_true",
                    help="preview without writing anything")
    ap.add_argument("--all-agents", action="store_true",
                    help="install into all detected agents")
    args = ap.parse_args()

    # --archive, --dist, --install, --install-memory, --describe, --present are
    # mutually exclusive action modes. Passing more than one silently shadows
    # the others.
    mode_count = sum(1 for m in (args.archive, args.dist, bool(args.install),
                                  args.install_memory, bool(args.describe),
                                  args.present) if m)
    if mode_count > 1:
        print("Error: --archive, --dist, --install, --install-memory, --describe, and --present are mutually exclusive.",
              file=sys.stderr)
        sys.exit(1)

    agents = discover_agents()
    output_skills = _find_output_skills(_OUTPUT_DIR)

    if args.archive:
        cmd_archive(args, agents, output_skills)
    elif args.dist:
        cmd_dist(args, agents, output_skills)
    elif args.present:
        cmd_present(args, agents, output_skills)
    elif args.describe:
        cmd_describe(args, agents, output_skills)
    elif args.install:
        cmd_install(args, agents, output_skills)
    elif args.install_memory:
        cmd_install_memory(args, agents, output_skills)
    else:
        cmd_list(args, agents, output_skills)


if __name__ == "__main__":
    main()
