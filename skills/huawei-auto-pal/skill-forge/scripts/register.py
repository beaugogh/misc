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
import tempfile
from pathlib import Path

# Windows console defaults to the system codepage (e.g. cp936/GBK on Chinese
# Windows), which cannot encode the ✓/✗/⚠ characters used in status output —
# causing UnicodeEncodeError that crashes --list and --archive even when the
# underlying operation succeeded. Reconfigure stdout/stderr to UTF-8 so the
# skill just works on Windows without requiring PYTHONUTF8=1. This matches
# the pattern in retro-scope/scripts/run.py.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass  # stream doesn't support reconfigure (e.g. redirected/closed)

# Make sibling modules importable.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

# Output dir is two levels up: skill-forge/scripts/ → huawei-auto-pal/output/
_OUTPUT_DIR = os.path.normpath(os.path.join(_HERE, "..", "..", "output"))
# Can be overridden via env var (same convention as persistence.py).
_OUTPUT_DIR = os.environ.get("SKILL_FORGE_OUTPUT_DIR", _OUTPUT_DIR)

from agent_targets import discover_agents, format_agents_report, AgentTarget
from skill_installer import install_skill, install_memory, update_skill, InstallResult


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


def scan_installed_skills(agents: list[AgentTarget]) -> dict[str, list[dict]]:
    """Scan each detected agent's skills/ directory for installed skills.

    Returns a dict: {agent_id: [{name, description, path}, ...]}.
    Read-only — only reads SKILL.md frontmatter, never modifies anything.

    This gives skill-forge visibility into what's already installed so it can:
    - Skip creating a redundant skill that overlaps with an installed one
    - Propose an update to an existing skill instead of creating a new one
    - Note the overlap in PROPOSAL.md
    """
    result: dict[str, list[dict]] = {}
    for agent in agents:
        if agent.skills_dir is None:
            continue
        skills_path = Path(agent.skills_dir)
        if not skills_path.is_dir():
            continue
        installed: list[dict] = []
        try:
            for entry in sorted(skills_path.iterdir()):
                if not entry.is_dir():
                    continue
                skill_md = entry / "SKILL.md"
                if not skill_md.is_file():
                    continue
                desc = _read_frontmatter_description(str(entry)) or ""
                installed.append({
                    "name": entry.name,
                    "description": desc[:200],  # truncate for display
                    "path": str(entry),
                })
        except OSError:
            pass
        if installed:
            result[agent.agent_id] = installed
    return result


def cmd_installed(args, agents, output_skills):
    """Print all skills installed across all detected agents.

    Used by skill-forge before creating proposals — gives the LLM visibility
    into existing skills so it can avoid redundancy and propose updates
    instead of duplicates.
    """
    installed = scan_installed_skills(agents)
    if not installed:
        print("# No skills installed in any detected agent.")
        print()
        print(format_agents_report(agents))
        return

    print("# Installed skills (across all detected agents)")
    print()
    for agent in agents:
        skills = installed.get(agent.agent_id, [])
        if not skills:
            if agent.skills_dir is None:
                print(f"## {agent.display_name} — no skills directory")
            else:
                print(f"## {agent.display_name} — no skills installed")
            print()
            continue
        print(f"## {agent.display_name} ({len(skills)} skill{'s' if len(skills) != 1 else ''})")
        print()
        for s in skills:
            desc = s["description"]
            if desc:
                # Truncate description to one line for readability.
                first_line = desc.split("\n")[0][:120]
                print(f"  {s['name']:40s}  {first_line}")
            else:
                print(f"  {s['name']:40s}  (no description)")
        print()
    # Summary of unique skill names across all agents.
    all_names: dict[str, list[str]] = {}
    for agent_id, skills in installed.items():
        for s in skills:
            all_names.setdefault(s["name"], []).append(agent_id)
    if len(all_names) > 1:
        print(f"## Summary: {len(all_names)} unique skill{'s' if len(all_names) != 1 else ''}")
        print()
        for name, agent_ids in sorted(all_names.items()):
            count = len(agent_ids)
            if count > 1:
                print(f"  {name:40s}  (in {count} agents: {', '.join(agent_ids)})")
            else:
                print(f"  {name:40s}  (in {agent_ids[0]})")
        print()


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


def _read_skill_version() -> str:
    """Read the `version` field from the root SKILL.md frontmatter.

    Returns the version string (e.g. '1.0.11') for use in dist zip naming.
    Falls back to 'unknown' if the file or field is missing.
    """
    skill_md = os.path.join(_SKILL_ROOT, "SKILL.md")
    if not os.path.isfile(skill_md):
        return "unknown"
    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return "unknown"
    if not text.startswith("---"):
        return "unknown"
    lines = text.split("\n")
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    # Try PyYAML first (handles folded scalars, quoted values).
    try:
        import yaml
        fm = yaml.safe_load("\n".join(fm_lines))
        if isinstance(fm, dict):
            ver = fm.get("version")
            if isinstance(ver, str) and ver.strip():
                return ver.strip()
    except ImportError:
        pass  # PyYAML not installed — fall through to line-scrape.
    except Exception:
        pass  # YAML parse error — fall through to line-scrape.
    # Fallback: line-scrape the version value (handles simple "version: X.Y.Z").
    for line in fm_lines:
        stripped = line.strip()
        if stripped.startswith("version:"):
            ver = stripped[len("version:"):].strip()
            if ver:
                return ver
    return "unknown"


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
    try:
        import yaml
        fm = yaml.safe_load(fm_text)
        if isinstance(fm, dict):
            desc = fm.get("description")
            if isinstance(desc, str) and desc.strip():
                return desc.strip()
    except ImportError:
        pass  # PyYAML not installed — fall through to line-scrape.
    except Exception:
        pass  # YAML parse error — fall through to line-scrape.

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
            if getattr(args, 'update', False):
                # --update: back up existing, overwrite with new version.
                result = update_skill(source, agent, dry_run=args.dry_run)
                status = "✓" if result.success else "✗"
                print(f"  {agent.display_name}: {status} {result.action} — {result.detail}")
                if result.success:
                    any_success = True
            else:
                print(f"  {agent.display_name}: already installed, skipping "
                      f"(use --update to overwrite)")
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


def _user_id() -> str | None:
    """Return the user's employee ID or username for zip file naming.

    Tries, in order: $USERNAME (Windows), $USER (Linux/macOS), whoami.
    Returns None if nothing is available — the caller falls back to omitting it.
    """
    for var in ("USERNAME", "USER"):
        val = os.environ.get(var, "").strip()
        if val:
            return val
    try:
        import subprocess
        result = subprocess.run(["whoami"], capture_output=True, text=True, timeout=3)
        val = result.stdout.strip()
        if val:
            return val
    except Exception:
        pass
    return None


# --- Session trace capture for diagnosis ---

# Known session-store directories for each supported agent.
# Each entry: (agent_name, projects_dir_path, env_var_for_session_id)
# The env var is optional — if set, we search for a file matching that ID.
# If not set, we fall back to the most recently modified .jsonl.
_JSONL_SESSION_SOURCES = [
    ("claude_code", os.path.expanduser("~/.claude/projects"), "CLAUDE_CODE_SESSION_ID"),
    ("codeagent",   os.path.expanduser("~/.cac/projects"),    None),
]

# Legacy codeagent SQLite DB paths (checked in order).
_LEGACY_DB_PATHS = [
    os.path.expanduser("~/.local/share/opencode/db/ngagent.db"),
    os.path.expanduser("~/.cac/ngagent.db"),
    os.path.expanduser("~/.ngagent/ngagent.db"),
    os.path.join(os.path.expanduser("~"), "AppData", "Local", "ngagent", "ngagent.db"),
    os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "ngagent", "ngagent.db"),
]


def _find_jsonl_session() -> tuple[str, str] | None:
    """Find the current session's JSONL file across all JSONL-based agents.

    Returns (agent_name, file_path) or None.
    """
    import glob as _glob
    import time as _time
    cutoff = _time.time() - 6 * 3600  # last 6 hours

    for agent_name, projects_dir, env_var in _JSONL_SESSION_SOURCES:
        if not os.path.isdir(projects_dir):
            continue

        # 1. Try env var if available (exact match).
        session_id = os.environ.get(env_var, "").strip() if env_var else ""
        if session_id:
            pattern = os.path.join(projects_dir, "*", f"{session_id}.jsonl")
            matches = _glob.glob(pattern)
            if matches and os.path.isfile(matches[0]):
                return (agent_name, matches[0])

        # 2. Fallback: most recently modified .jsonl in this agent's dir.
        best_path = None
        best_mtime = 0.0
        for path in _glob.glob(os.path.join(projects_dir, "*", "*.jsonl")):
            if not os.path.isfile(path):
                continue
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime > cutoff and mtime > best_mtime:
                best_mtime = mtime
                best_path = path
        if best_path:
            return (agent_name, best_path)

    return None


def _find_legacy_codeagent_session() -> tuple[str, str] | None:
    """Find the most recent session in the legacy codeagent SQLite DB.

    Returns (db_path, session_id) or None.
    """
    import sqlite3
    import shutil as _shutil
    db_path = None
    for p in _LEGACY_DB_PATHS:
        if os.path.isfile(p):
            db_path = p
            break
    if not db_path:
        return None

    # Copy to temp (DB may be locked by the running codeagent).
    try:
        fd, tmp = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        _shutil.copy2(db_path, tmp)
    except OSError:
        return None

    try:
        conn = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        c = conn.cursor()
        # Get the most recently updated session.
        c.execute(
            "SELECT id FROM session ORDER BY time_updated DESC LIMIT 1"
        )
        row = c.fetchone()
        conn.close()
    except Exception:
        os.unlink(tmp)
        return None
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass

    if row and row[0]:
        return (db_path, row[0])
    return None


def _export_legacy_codeagent_session(db_path: str, session_id: str) -> list[str]:
    """Export a legacy codeagent session from SQLite as JSONL lines.

    Queries the message and part tables for the given session_id and
    reconstructs a JSONL stream similar to the Claude Code format so the
    same truncation logic can process it.
    """
    import sqlite3
    import json as _json
    import shutil as _shutil

    # Copy to temp (DB may be locked).
    try:
        fd, tmp = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        _shutil.copy2(db_path, tmp)
    except OSError:
        return []

    lines = []
    try:
        conn = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        c = conn.cursor()

        # Fetch messages for this session, ordered by time.
        c.execute(
            "SELECT message_id, session_id, time_created, data "
            "FROM message WHERE session_id = ? ORDER BY time_created",
            (session_id,)
        )
        messages = c.fetchall()

        # Fetch all parts for this session, ordered by time.
        c.execute(
            "SELECT id, message_id, session_id, time_created, data "
            "FROM part WHERE session_id = ? ORDER BY time_created",
            (session_id,)
        )
        parts = c.fetchall()
        conn.close()

        # Build a lookup: message_id -> list of parts
        parts_by_msg = {}
        for pid, mid, sid, ts, data_json in parts:
            parts_by_msg.setdefault(mid, []).append((pid, ts, data_json))

        # Emit one JSONL line per message, with parts embedded.
        for mid, sid, ts_ms, data_json in messages:
            try:
                data = _json.loads(data_json) if data_json else {}
            except _json.JSONDecodeError:
                data = {}

            role = data.get("role", "unknown")
            obj = {
                "type": role,
                "session_id": sid,
                "message_id": mid,
                "timestamp": ts_ms,
                "data": data,
                "parts": [],
            }
            for pid, pts, pdata_json in parts_by_msg.get(mid, []):
                try:
                    pdata = _json.loads(pdata_json) if pdata_json else {}
                except _json.JSONDecodeError:
                    pdata = {}
                obj["parts"].append({
                    "id": pid,
                    "time_created": pts,
                    "data": pdata,
                })
            lines.append(_json.dumps(obj, ensure_ascii=False))

    except Exception:
        pass
    finally:
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass

    return lines


def _write_session_trace(output_dir: str) -> str | None:
    """Write a truncated copy of the current session transcript to output/.

    Supports multiple agent session formats:
    - Claude Code / codeagent: JSONL files in ~/.claude/projects/ or ~/.cac/projects/
    - Legacy codeagent: ngagent.db SQLite (exported as JSONL)

    Large content blocks are truncated to keep the archive manageable.
    Secrets (API keys, tokens, JWTs, passwords) are redacted to match the
    privacy model in run.py's _export_session_records.
    Returns the path to the written file, or None if no session was found.
    """
    import json as _json
    import re as _re

    # Try JSONL-based agents first (Claude Code, codeagent).
    jsonl_result = _find_jsonl_session()
    # Also try legacy codeagent SQLite.
    legacy_result = _find_legacy_codeagent_session()

    if not jsonl_result and not legacy_result:
        return None

    dest = os.path.join(output_dir, "session_trace.jsonl")
    lines_written = 0

    # Secret redaction patterns — same as run.py _export_session_records.
    # Applied to the full JSON string after truncation so secrets anywhere
    # (user messages, tool inputs, tool results, thinking) are caught.
    _secret_patterns = (
        (_re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|password|passwd|secret|cookie|token)\s*[:=]\s*)[^\s,;]+"), r"\1[REDACTED]"),
        (_re.compile(r"(?i)(authorization\s*[:=]\s*(?:bearer\s+)?)[^\s,;]+"), r"\1[REDACTED]"),
        (_re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"), "[REDACTED_JWT]"),
        (_re.compile(r"(?i)(?:--strict-ssl\s+false|--strict-ssl=false)"), "[REDACTED_SSL_FLAG]"),
        (_re.compile(r"(?i)(https?://[^:/@\s]+:)[^@/\s]+(@)"), r"\1[REDACTED]\2"),
    )

    def _redact_str(s: str) -> str:
        for pattern, replacement in _secret_patterns:
            s = pattern.sub(replacement, s)
        return s

    def _truncate(text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[:limit] + f"\n[...truncated {len(text) - limit} chars...]"

    def _process_obj(obj: dict) -> dict | None:
        """Process one JSON object: skip metadata, truncate large fields.
        Returns the modified object, or None to skip the line entirely."""
        # Skip entries with no diagnostic value.
        if obj.get("type") in (
            "file-history-snapshot",
            "file-history-delta",
            "attachment",
            "queue-operation",
            "ai-title",
            "custom-title",
            "agent-name",
            "mode",
            "permission-mode",
        ):
            return None

        # --- Claude Code / codeagent JSONL format ---
        # (message.content is a list of blocks with type/text/tool_use/etc.)
        msg = obj.get("message")
        if isinstance(msg, dict):
            content = msg.get("content")
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    btype = block.get("type")
                    if btype == "tool_result":
                        c = block.get("content")
                        if isinstance(c, str):
                            block["content"] = _truncate(c, 500)
                        elif isinstance(c, list):
                            for sub in c:
                                if not isinstance(sub, dict):
                                    continue
                                stype = sub.get("type")
                                if stype == "text":
                                    sub["text"] = _truncate(sub.get("text", ""), 500)
                                elif stype == "image":
                                    src = sub.get("source", {})
                                    if isinstance(src, dict) and \
                                       isinstance(src.get("data"), str) and \
                                       len(src["data"]) > 200:
                                        src["data"] = f"[base64 image data: {len(src['data'])} chars, truncated]"
                    elif btype == "text":
                        block["text"] = _truncate(block.get("text", ""), 1000)
                    elif btype == "thinking":
                        block["thinking"] = _truncate(block.get("thinking", ""), 1000)
                    elif btype == "image":
                        src = block.get("source", {})
                        if isinstance(src, dict) and \
                           isinstance(src.get("data"), str) and \
                           len(src["data"]) > 200:
                            src["data"] = f"[base64 image data: {len(src['data'])} chars, truncated]"

        # Truncate top-level toolUseResult (Claude Code duplicate).
        tur = obj.get("toolUseResult")
        if isinstance(tur, str) and len(tur) > 500:
            obj["toolUseResult"] = _truncate(tur, 500)
        elif isinstance(tur, dict):
            for tur_key in ("content", "stdout", "stderr", "output", "result"):
                val = tur.get(tur_key)
                if isinstance(val, str) and len(val) > 500:
                    tur[tur_key] = _truncate(val, 500)
            tur_file = tur.get("file")
            if isinstance(tur_file, dict):
                b64 = tur_file.get("base64")
                if isinstance(b64, str) and len(b64) > 200:
                    tur_file["base64"] = f"[base64 image data: {len(b64)} chars, truncated]"

        # --- Legacy codeagent format ---
        # (data JSON has role/model/path; parts[] have type/text/tool/etc.)
        data = obj.get("data")
        if isinstance(data, dict):
            # Truncate large string fields in data.
            for dk in ("content", "output", "error"):
                dv = data.get(dk)
                if isinstance(dv, str) and len(dv) > 500:
                    data[dk] = _truncate(dv, 500)

        parts = obj.get("parts")
        if isinstance(parts, list):
            for part in parts:
                if not isinstance(part, dict):
                    continue
                pdata = part.get("data")
                if isinstance(pdata, dict):
                    # Truncate tool state.output and text content.
                    state = pdata.get("state")
                    if isinstance(state, dict):
                        so = state.get("output")
                        if isinstance(so, str) and len(so) > 500:
                            state["output"] = _truncate(so, 500)
                        si = state.get("input")
                        if isinstance(si, str) and len(si) > 1000:
                            state["input"] = _truncate(si, 1000)
                    # Truncate text content in parts.
                    text = pdata.get("text")
                    if isinstance(text, str) and len(text) > 1000:
                        pdata["text"] = _truncate(text, 1000)
                    # Truncate reasoning.
                    reasoning = pdata.get("reasoning")
                    if isinstance(reasoning, str) and len(reasoning) > 1000:
                        pdata["reasoning"] = _truncate(reasoning, 1000)

        return obj

    try:
        with open(dest, "w", encoding="utf-8") as fout:
            if jsonl_result:
                agent_name, src = jsonl_result
                with open(src, encoding="utf-8") as fin:
                    for line in fin:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = _json.loads(line)
                        except _json.JSONDecodeError:
                            fout.write(line + "\n")
                            lines_written += 1
                            continue
                        result = _process_obj(obj)
                        if result is None:
                            continue
                        raw = _json.dumps(result, ensure_ascii=False)
                        fout.write(_redact_str(raw) + "\n")
                        lines_written += 1
            elif legacy_result:
                db_path, session_id = legacy_result
                lines = _export_legacy_codeagent_session(db_path, session_id)
                for line in lines:
                    try:
                        obj = _json.loads(line)
                    except _json.JSONDecodeError:
                        fout.write(line + "\n")
                        lines_written += 1
                        continue
                    result = _process_obj(obj)
                    if result is None:
                        continue
                    raw = _json.dumps(result, ensure_ascii=False)
                    fout.write(_redact_str(raw) + "\n")
                    lines_written += 1
    except OSError as e:
        print(f"  ⚠ Could not write session trace: {e}", file=sys.stderr)
        return None

    return dest if lines_written > 0 else None


def _update_index_skills_section(output_dir: str) -> None:
    """Inject the proposed-skills section into index.html after skill-forge.

    During retro-scope, index.html is written before any skills exist.
    After skill-forge creates PROPOSAL.md files, this function regenerates
    the skills section and injects it into the existing index.html so the
    dashboard shows the proposals.
    """
    import html as html_mod
    index_path = os.path.join(output_dir, "index.html")
    if not os.path.isfile(index_path):
        return

    # Generate the skills section HTML.
    # Import the function from retro-scope's run.py via sys.path.
    retro_scripts = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "retro-scope", "scripts")
    if retro_scripts not in sys.path:
        sys.path.insert(0, retro_scripts)
    try:
        from run import _build_skills_section
        skills_html = _build_skills_section(output_dir, html_mod)
    except Exception:
        return

    if not skills_html:
        return

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
    except OSError:
        return

    # Replace the skills section using marker comments (robust against
    # nested HTML — regex on nested divs is unreliable).
    START = '<!-- SKILLS_SECTION_START -->'
    END = '<!-- SKILLS_SECTION_END -->'
    if START in html and END in html:
        import re as _re
        pattern = _re.compile(_re.escape(START) + r'.*?' + _re.escape(END), _re.DOTALL)
        html = pattern.sub(skills_html, html)
    elif "</body>" in html:
        html = html.replace("</body>", f"{skills_html}\n</body>")
    else:
        html += "\n" + skills_html

    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Updated index.html with skills section")
    except OSError:
        pass


def _redact_pii_in_output(output_dir: str) -> None:
    """Scan all SKILL.md and PROPOSAL.md files in output/ for PII and redact it.

    This is a mechanical enforcement layer — the LLM is told not to hardcode
    PII but may do so anyway. This catches and fixes it before zipping.

    Redacts:
    - Employee IDs matching b\\d{8} (Huawei convention)
    - Email addresses (user@huawei.com, user@example.com)
    - Internal Huawei URLs (https://*.huawei.com/...)
    - GitHub usernames in URLs (github.com/<user>)

    Uses placeholder replacements. Prints a warning for each redaction.
    """
    import re as _re

    # PII patterns with replacements.
    # Note: employee ID pattern (b + 8 digits) is Huawei-specific.
    pii_patterns = [
        # Employee ID: b00563677, b12345678, etc.
        (_re.compile(r'\bb\d{8}\b'), '<employee-id>'),
        # Email addresses.
        (_re.compile(r'\b[\w.+-]+@[\w.-]+\.\w{2,}\b'), '<email>'),
        # Internal Huawei URLs — match the full URL including query strings
        # and fragments, so names in ?q=bo+gao or #frag don't leak.
        (_re.compile(r'https?://[a-z0-9-]+\.huawei\.com\S*'), '<internal-url>'),
        # GitHub profile URLs (github.com/username).
        (_re.compile(r'https?://github\.com/[\w-]+'), '<github-url>'),
    ]

    redacted_count = 0
    for name in sorted(os.listdir(output_dir)):
        skill_dir = os.path.join(output_dir, name)
        if not os.path.isdir(skill_dir):
            continue
        if name in ("session_records", "page_cache", "__pycache__",
                    ".skill-forge-backups", "reports"):
            continue
        for fname in ("SKILL.md", "PROPOSAL.md"):
            fpath = os.path.join(skill_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except OSError:
                continue

            original = content
            for pattern, replacement in pii_patterns:
                content = pattern.sub(replacement, content)

            if content != original:
                try:
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(content)
                    redacted_count += 1
                    print(f"  Redacted PII in {name}/{fname}")
                except OSError:
                    pass

    if redacted_count > 0:
        print(f"  PII redaction: {redacted_count} file(s) cleaned")


def cmd_archive(args, agents, output_skills):
    """Zip the output/ folder and save it to the user's Downloads directory."""
    output_path = Path(_OUTPUT_DIR)
    if not output_path.is_dir():
        print(f"Error: output directory not found at {_OUTPUT_DIR}", file=sys.stderr)
        sys.exit(1)

    # Guard against double-archive. The agent sometimes runs --archive twice
    # in the same turn (e.g. re-running with 2>&1). A sentinel file prevents
    # the second call from creating a duplicate zip. The sentinel records the
    # timestamp of the first archive; the user sees which zip to use.
    # --dry-run does not set the sentinel (it doesn't actually archive).
    sentinel = output_path / ".archived"
    if not args.dry_run and sentinel.exists():
        sentinel_mtime = datetime.datetime.fromtimestamp(
            sentinel.stat().st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S")
        print(f"✓ Already archived at {sentinel_mtime}.")
        print(f"  Re-running --archive is unnecessary — the zip was already created.")
        print(f"  To force a new archive, delete output/.archived first.")
        return

    if not args.dry_run:
        sentinel.touch()

    # Capture the current agent session transcript for diagnosis.
    # Written to output/session_trace.jsonl before zipping so it's included
    # in the archive automatically.
    trace_path = _write_session_trace(_OUTPUT_DIR)
    if trace_path:
        import os as _os
        trace_size = _os.path.getsize(trace_path)
        trace_kb = trace_size / 1024
        if trace_kb < 1024:
            size_str = f"{trace_kb:.0f} KB"
        else:
            size_str = f"{trace_kb / 1024:.1f} MB"
        print(f"  Session trace: {os.path.basename(trace_path)} ({size_str})")
    else:
        print(f"  ⚠ No session trace found (agent session JSONL not detected).")

    # Regenerate the skills section in index.html now that skill-forge has
    # created PROPOSAL.md files. During retro-scope, index.html was written
    # before any skills existed. This adds the skills section post-hoc.
    _update_index_skills_section(_OUTPUT_DIR)

    # Check for proposals missing SKILL.md — the agent sometimes creates
    # PROPOSAL.md but forgets the actual SKILL.md. Warn so the user knows.
    proposals_without_skill = []
    try:
        for name in sorted(os.listdir(_OUTPUT_DIR)):
            full = os.path.join(_OUTPUT_DIR, name)
            if not os.path.isdir(full):
                continue
            if name in ("session_records", "page_cache", "__pycache__",
                        ".skill-forge-backups", "reports"):
                continue
            has_proposal = os.path.isfile(os.path.join(full, "PROPOSAL.md"))
            has_skill = os.path.isfile(os.path.join(full, "SKILL.md"))
            if has_proposal and not has_skill:
                proposals_without_skill.append(name)
    except OSError:
        pass
    if proposals_without_skill:
        print(f"  ⚠ {len(proposals_without_skill)} proposal(s) missing SKILL.md: "
              f"{', '.join(proposals_without_skill)}")
        print(f"    The agent created PROPOSAL.md but not the actual skill file. "
              f"Re-run skill-forge to generate SKILL.md for these.")

    # Mechanically scan generated SKILL.md and PROPOSAL.md files for PII
    # and redact it. Wording-based rules are insufficient — the LLM reads
    # unredacted session data and may write PII into output files despite
    # instructions not to. This is the enforcement layer.
    _redact_pii_in_output(_OUTPUT_DIR)

    downloads = _downloads_dir()
    os.makedirs(downloads, exist_ok=True)

    # Build a timestamped filename: huawei-auto-pal-output-<user>-YYYYMMDD-HHMMSS.zip
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    user = _user_id()
    user_part = f"{user}-" if user else ""
    zip_name = f"huawei-auto-pal-output-{user_part}{timestamp}.zip"
    zip_path = os.path.join(downloads, zip_name)

    # Count skills (directories with SKILL.md) for the summary.
    skill_count = len(output_skills)

    if args.dry_run:
        print(f"Would zip {_OUTPUT_DIR} → {zip_path}")
        print(f"  ({skill_count} skill(s), {len(agents)} agent(s) detected)")
        return

    # Create the zip, excluding __pycache__, .skill-forge-backups, and
    # agent-created scratch scripts (.py files at the output/ root level
    # that the agent created to help read tasks/session records — not skill
    # artifacts and should not be in the archive).
    skip_dirs = {"__pycache__", ".skill-forge-backups"}
    skip_files = {".archived"}  # sentinel — not an artifact
    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(_OUTPUT_DIR):
            # Filter out skip dirs in-place so os.walk doesn't descend into them.
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for fname in files:
                # Skip agent-created scratch .py scripts at the output/ root.
                # These are temp files the agent creates to read tasks/sessions
                # (e.g. extract_top10.py, read_sessions.py). They are not skill
                # artifacts. Only exclude .py at the root level — .py files
                # inside skill directories (e.g. <skill>/scripts/foo.py) are
                # legitimate skill code and must be included.
                rel = os.path.relpath(root, _OUTPUT_DIR)
                is_root_level = (rel == ".")
                if is_root_level and fname.endswith(".py"):
                    continue
                if fname in skip_files:
                    continue
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

    version = _read_skill_version()
    zip_name = f"huawei-auto-pal-{version}.zip"
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
    ap.add_argument("--installed", action="store_true",
                    help="list all skills already installed across all detected agents")
    ap.add_argument("--update", action="store_true",
                    help="with --install: back up and overwrite an existing skill instead of skipping")
    args = ap.parse_args()

    # --archive, --dist, --install, --install-memory, --describe, --present,
    # --installed are mutually exclusive action modes.
    mode_count = sum(1 for m in (args.archive, args.dist, bool(args.install),
                                  args.install_memory, bool(args.describe),
                                  args.present, args.installed) if m)
    if mode_count > 1:
        print("Error: --archive, --dist, --install, --install-memory, --describe, --present, and --installed are mutually exclusive.",
              file=sys.stderr)
        sys.exit(1)

    # --update is a modifier for --install only.
    if args.update and not args.install:
        print("Error: --update requires --install.", file=sys.stderr)
        sys.exit(2)

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
    elif args.installed:
        cmd_installed(args, agents, output_skills)
    else:
        cmd_list(args, agents, output_skills)


if __name__ == "__main__":
    main()
