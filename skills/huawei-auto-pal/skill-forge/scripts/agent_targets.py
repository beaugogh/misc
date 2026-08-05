"""Agent target discovery for skill registration.

Detects which AI agents are installed on the current machine and reports each
agent's skill directory and memory mechanism. All detection is read-only —
no personal data is read, no files are opened beyond existence checks.

Supported agents:
  - Claude Code  (~/.claude/)
  - CodeAgent    (~/.cac/)        — Huawei's Claude Code fork
  - OpenCode     (~/.config/opencode/)
  - Codex        (~/.codex/)
  - OpenClaw     (~/.openclaw/ or ~/.open-claw/)
  - Hermes       (~/.hermes-agent/ or ~/.hermes/)
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from pathlib import Path


HOME = Path(os.path.expanduser("~"))


@dataclass
class AgentTarget:
    """One installed agent and where it stores skills + memory."""

    agent_id: str           # "claude_code", "codeagent", etc.
    display_name: str       # "Claude Code", "CodeAgent", etc.
    skills_dir: str | None  # absolute path to skills/ dir, or None if unsupported
    memory_dir: str | None  # absolute path to memory/ dir for current project, or None
    memory_format: str      # "claude_memory" | "instructions_md" | "none"
    detect_path: str        # the path whose existence proves the agent is installed


def derive_project_slug(cwd: str | None = None) -> str:
    """Derive the project slug an agent uses for the given directory.

    Claude Code and CodeAgent use the same algorithm: replace : \\ / with -.
    Consecutive dashes are NOT collapsed — a Windows drive colon plus the
    following separator produce a double dash that Claude Code preserves
    (e.g. D:\\workspace\\misc → D--workspace-misc).

    Only leading/trailing dashes are stripped.
    """
    if cwd is None:
        cwd = os.getcwd()
    # Replace drive colon, backslashes, forward slashes with dashes.
    slug = cwd.replace(":", "-").replace("\\", "-").replace("/", "-")
    # Strip leading/trailing dashes only — preserve internal double dashes.
    slug = slug.strip("-")
    return slug


def _claude_memory_dir(base: Path, slug: str) -> str | None:
    """Return the memory dir for a Claude-style agent if it exists."""
    mem = base / "projects" / slug / "memory"
    # The memory dir may not exist yet on a fresh project. That's fine —
    # we return the path so the installer can create it. But the projects/
    # dir itself must exist (proving the agent is used for this project).
    projects_dir = base / "projects"
    if projects_dir.is_dir():
        return str(mem)
    return None


def discover_agents(cwd: str | None = None) -> list[AgentTarget]:
    """Detect installed agents. Returns only agents that are actually present.

    No personal file contents are read — only directory existence checks.
    """
    slug = derive_project_slug(cwd)
    agents: list[AgentTarget] = []

    # Claude Code
    claude_base = HOME / ".claude"
    if claude_base.is_dir():
        # skills/ may not exist yet — that's fine, installer creates it.
        skills_dir = str(claude_base / "skills")
        memory_dir = _claude_memory_dir(claude_base, slug)
        agents.append(AgentTarget(
            agent_id="claude_code",
            display_name="Claude Code",
            skills_dir=skills_dir,
            memory_dir=memory_dir,
            memory_format="claude_memory" if memory_dir else "none",
            detect_path=str(claude_base),
        ))

    # CodeAgent (.cac) — Huawei's Claude Code fork
    cac_base = HOME / ".cac"
    if cac_base.is_dir():
        skills_dir = str(cac_base / "skills")
        memory_dir = _claude_memory_dir(cac_base, slug)
        agents.append(AgentTarget(
            agent_id="codeagent",
            display_name="CodeAgent",
            skills_dir=skills_dir,
            memory_dir=memory_dir,
            memory_format="claude_memory" if memory_dir else "none",
            detect_path=str(cac_base),
        ))

    # OpenCode — skills confirmed at ~/.config/opencode/skills/.
    # Memory: legacy opencode-ai used OpenCode.md in the project root; modern
    # opencode uses MCP/LSP for live context. We support the legacy OpenCode.md
    # convention since it's a simple markdown file in the project dir.
    opencode_base = HOME / ".config" / "opencode"
    if opencode_base.is_dir():
        skills_dir = str(opencode_base / "skills")
        agents.append(AgentTarget(
            agent_id="opencode",
            display_name="OpenCode",
            skills_dir=skills_dir,
            memory_dir=None,
            memory_format="none",
            detect_path=str(opencode_base),
        ))

    # Codex — skills in $CODEX_HOME/skills/ (default ~/.codex/skills/).
    # Memory via AGENTS.md in the project root (emerging standard).
    codex_base = HOME / ".codex"
    if codex_base.is_dir():
        skills_dir = str(codex_base / "skills")
        agents.append(AgentTarget(
            agent_id="codex",
            display_name="Codex",
            skills_dir=skills_dir,
            memory_dir=None,
            memory_format="agents_md",
            detect_path=str(codex_base),
        ))

    # OpenClaw — skills in ~/.openclaw/workspace/skills/ or ~/.openclaw/skills/.
    # Memory via USER.md and MEMORY.md in the workspace.
    for claw_dir_name in (".openclaw", ".open-claw"):
        claw_base = HOME / claw_dir_name
        if claw_base.is_dir():
            # Prefer workspace/skills/ (agent-specific), fall back to skills/ (shared).
            workspace_skills = claw_base / "workspace" / "skills"
            shared_skills = claw_base / "skills"
            skills_dir = str(workspace_skills if workspace_skills.is_dir() or not shared_skills.is_dir()
                             else shared_skills)
            # Memory: USER.md in the workspace dir.
            workspace_dir = claw_base / "workspace"
            memory_dir = str(workspace_dir) if workspace_dir.is_dir() else None
            agents.append(AgentTarget(
                agent_id="openclaw",
                display_name="OpenClaw",
                skills_dir=skills_dir,
                memory_dir=memory_dir,
                memory_format="user_md" if memory_dir else "none",
                detect_path=str(claw_base),
            ))
            break

    # Hermes — skills in ~/.hermes/ (automated skill creation, SKILL.md format).
    # Persistent memory is native but the exact file layout is not documented;
    # treat as none until confirmed.
    for hermes_dir_name in (".hermes-agent", ".hermes"):
        hermes_base = HOME / hermes_dir_name
        if hermes_base.is_dir():
            skills_dir = str(hermes_base / "skills")
            agents.append(AgentTarget(
                agent_id="hermes",
                display_name="Hermes",
                skills_dir=skills_dir,
                memory_dir=None,
                memory_format="none",
                detect_path=str(hermes_base),
            ))
            break

    return agents


def format_agents_report(agents: list[AgentTarget]) -> str:
    """Format a human-readable summary of detected agents."""
    if not agents:
        return "No AI agents detected on this machine."
    lines = ["Detected agents:"]
    for a in agents:
        skill_status = a.skills_dir if a.skills_dir else "not supported"
        mem_status = "none"
        if a.memory_format == "claude_memory" and a.memory_dir:
            mem_status = f"memory/ ({a.memory_dir})"
        elif a.memory_format == "instructions_md" and a.memory_dir:
            mem_status = f"instructions.md ({a.memory_dir})"
        lines.append(f"  {a.display_name:15s}  skills: {skill_status}")
        lines.append(f"  {'':15s}  memory: {mem_status}")
    return "\n".join(lines)
