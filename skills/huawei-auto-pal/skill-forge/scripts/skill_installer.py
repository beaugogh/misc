"""Skill and memory installer — copies output skills into agent directories.

After skill-forge creates a skill in output/<name>/, this module copies it into
the target agent's skills/ directory. For personal-context memory, it routes
facts into the agent's memory system (MEMORY.md + per-fact .md for Claude-style
agents, or instructions.md for Codex).

All writes require explicit user approval. dry_run=True reports what would
happen without writing anything.
"""

from __future__ import annotations

import os
import re
import shutil
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agent_targets import AgentTarget


@dataclass
class InstallResult:
    """Result of an install attempt."""
    success: bool
    action: str               # "copied" | "updated" | "skipped" | "conflict" | "error" | "unsupported" | "dry_run"
    target_path: str          # where it went (or would go)
    detail: str = ""          # human-readable detail
    files_copied: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Skill installation
# ---------------------------------------------------------------------------

def install_skill(
    source_dir: str,
    agent: AgentTarget,
    dry_run: bool = False,
) -> InstallResult:
    """Copy a skill folder into an agent's skills/ directory.

    source_dir must contain a SKILL.md file. The copy is independent —
    edits to the source afterwards won't propagate.

    Returns InstallResult. Does NOT auto-overwrite existing skills.
    """
    source = Path(source_dir)
    if not source.is_dir():
        return InstallResult(False, "error", source_dir, "source directory does not exist")
    if not (source / "SKILL.md").is_file():
        return InstallResult(False, "error", source_dir, "source has no SKILL.md")

    skill_name = source.name

    # Validate skill_name — reject path traversal and invalid characters.
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', skill_name):
        return InstallResult(
            False, "error", source_dir,
            f"invalid skill directory name: {skill_name!r} — must match [a-zA-Z0-9][a-zA-Z0-9._-]*"
        )

    if agent.skills_dir is None:
        return InstallResult(
            False, "unsupported", "",
            f"{agent.display_name} does not support skill directories"
        )

    target = Path(agent.skills_dir) / skill_name

    if target.exists():
        return InstallResult(
            False, "conflict", str(target),
            f"skill already exists at {target} — remove it first or update it manually"
        )

    if dry_run:
        return InstallResult(
            True, "dry_run", str(target),
            f"would copy {skill_name}/ into {agent.skills_dir}"
        )

    # Create parent if needed.
    target.parent.mkdir(parents=True, exist_ok=True)

    # Copy the skill folder. We copy SKILL.md + scripts/ + references/ + assets/
    # (same structure quick_validate checks). Exclude PROPOSAL.md (bilingual
    # proposal metadata for the user's review — not part of the installed skill),
    # __pycache__, and bytecode files. symlinks=True copies symlinks as-is
    # rather than following them — a symlink in output/<skill>/ pointing to
    # ~/.ssh/id_rsa or .env must not leak into the agent's skills dir.
    copied: list[str] = []
    try:
        shutil.copytree(source, target,
                        symlinks=True,
                        ignore=shutil.ignore_patterns("PROPOSAL.md", "__pycache__", "*.pyc", "*.pyo"))
        # Verify the copy.
        if not (target / "SKILL.md").is_file():
            shutil.rmtree(target, ignore_errors=True)
            return InstallResult(False, "error", str(target), "copy failed — SKILL.md missing after copy")
        copied.append("SKILL.md")
        for subdir in ("scripts", "references", "assets"):
            sub = target / subdir
            if sub.is_dir():
                count = sum(1 for _ in sub.rglob("*") if _.is_file())
                if count:
                    copied.append(f"{subdir}/ ({count} files)")
    except Exception as e:
        # Clean up partial copy.
        if target.exists():
            shutil.rmtree(target, ignore_errors=True)
        return InstallResult(False, "error", str(target), f"copy failed: {e}")

    return InstallResult(
        True, "copied", str(target),
        f"installed {skill_name} into {agent.display_name}",
        files_copied=copied,
    )


def update_skill(
    source_dir: str,
    agent: AgentTarget,
    backup_dir: str | None = None,
    dry_run: bool = False,
) -> InstallResult:
    """Update an existing skill in an agent's skills/ directory.

    Backs up the existing skill, then overwrites with the new version.
    The backup is placed at ``backup_dir/<skill_name>/<timestamp>/`` if
    ``backup_dir`` is provided, otherwise at
    ``output/.skill-forge-backups/<skill_name>/<timestamp>/`` relative to
    the source skill's parent's parent (the output/ directory).

    Returns InstallResult with action="updated" or "error".
    """
    source = Path(source_dir)
    if not source.is_dir():
        return InstallResult(False, "error", source_dir, "source directory does not exist")
    if not (source / "SKILL.md").is_file():
        return InstallResult(False, "error", source_dir, "source has no SKILL.md")

    skill_name = source.name

    # Validate skill_name — reject path traversal and invalid characters
    # (same guard as install_skill, for defense-in-depth).
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', skill_name):
        return InstallResult(
            False, "error", source_dir,
            f"invalid skill directory name: {skill_name!r} — must match [a-zA-Z0-9][a-zA-Z0-9._-]*"
        )

    if agent.skills_dir is None:
        return InstallResult(
            False, "unsupported", "",
            f"{agent.display_name} does not support skill directories"
        )

    target = Path(agent.skills_dir) / skill_name

    if not target.exists():
        # Nothing to update — fall back to install.
        return install_skill(source_dir, agent, dry_run=dry_run)

    # Determine backup location.
    if backup_dir is None:
        # Default: output/.skill-forge-backups/<name>/<timestamp>/
        # source is output/<name>/ → output/ is source.parent
        output_root = source.parent
        backup_base = output_root / ".skill-forge-backups"
    else:
        backup_base = Path(backup_dir)

    import time as _time
    timestamp = _time.strftime("%Y%m%d-%H%M%S")
    backup_path = backup_base / skill_name / timestamp

    if dry_run:
        return InstallResult(
            True, "dry_run", str(target),
            f"would back up {target} → {backup_path}, then overwrite with {skill_name}/",
        )

    # 1. Back up the existing skill.
    try:
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup_path,
                        symlinks=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
    except Exception as e:
        return InstallResult(
            False, "error", str(target),
            f"backup failed ({e}) — existing skill left untouched at {target}",
        )

    # 2. Copy new version to a temp dir, then swap atomically.
    #    On Windows, os.rename is atomic for dirs on the same volume.
    #    If the agent process has files locked, the rename fails but
    #    the original skill is left untouched.
    target_new = target.parent / f"{skill_name}.new"
    target_old = target.parent / f"{skill_name}.old"
    try:
        # Clean up any stale temp dirs from a previous failed run.
        if target_new.exists():
            shutil.rmtree(target_new, ignore_errors=True)
        if target_old.exists():
            shutil.rmtree(target_old, ignore_errors=True)

        # Copy new version to <name>.new/
        shutil.copytree(source, target_new,
                        symlinks=True,
                        ignore=shutil.ignore_patterns("PROPOSAL.md", "__pycache__", "*.pyc", "*.pyo"))
        if not (target_new / "SKILL.md").is_file():
            shutil.rmtree(target_new, ignore_errors=True)
            return InstallResult(False, "error", str(target),
                                 "copy failed — SKILL.md missing after copy, original left untouched")

        # Swap: target → target.old, target_new → target
        try:
            os.rename(str(target), str(target_old))
        except PermissionError:
            # Agent process has files locked — can't rename target.
            shutil.rmtree(target_new, ignore_errors=True)
            return InstallResult(
                False, "error", str(target),
                f"cannot replace skill (agent may be running) — "
                f"original left untouched at {target}. Close the agent and retry.",
            )
        os.rename(str(target_new), str(target))
        # Clean up the old version.
        shutil.rmtree(target_old, ignore_errors=True)
    except Exception as e:
        # Clean up any temp dirs.
        shutil.rmtree(target_new, ignore_errors=True)
        shutil.rmtree(target_old, ignore_errors=True)
        return InstallResult(
            False, "error", str(target),
            f"update failed ({e}) — original skill untouched at {target}, backup at {backup_path}",
        )

    return InstallResult(
        True, "updated", str(target),
        f"updated {skill_name} in {agent.display_name} (backup: {backup_path})",
        files_copied=["SKILL.md"],
    )


# ---------------------------------------------------------------------------
# Memory installation (personal-context → agent memory system)
# ---------------------------------------------------------------------------

def _parse_personal_context(content: str) -> list[dict]:
    """Parse personal-context/SKILL.md body into individual memory facts.

    Extracts sections marked by ## headings. Each becomes one memory file.
    Returns a list of {name, description, body} dicts.
    """
    facts: list[dict] = []
    # Split on ## headings at line start, but not inside fenced code blocks.
    in_fence = False
    current_title = None
    current_body: list[str] = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_fence = not in_fence
            current_body.append(line)
            continue
        if not in_fence and line.startswith('## '):
            # Flush previous section.
            if current_title is not None:
                facts.append(_make_fact(current_title, '\n'.join(current_body).strip()))
            current_title = line[3:].strip()
            current_body = []
        elif current_title is not None:
            current_body.append(line)
    # Flush last section.
    if current_title is not None:
        facts.append(_make_fact(current_title, '\n'.join(current_body).strip()))
    return facts


def _make_fact(title: str, body: str) -> dict:
    """Build a memory fact dict from a title and body text."""
    # Derive a slug from the title — lowercase, allow Unicode word chars so
    # non-ASCII titles (Chinese, Japanese, etc.) produce a meaningful slug.
    slug = re.sub(r'[^\w]+', '-', title.lower(), flags=re.UNICODE).strip('-')
    if not slug:
        slug = "unnamed-fact"
    # Description: first sentence of body, truncated.
    first_sentence = body.split('.')[0][:100] if body else title
    return {
        "name": slug,
        "title": title,
        "description": first_sentence,
        "body": body,
    }


def install_memory(
    personal_context_path: str,
    agent: AgentTarget,
    dry_run: bool = False,
) -> InstallResult:
    """Route personal-context memory into the agent's memory system.

    For claude_memory agents: creates per-fact .md files + updates MEMORY.md index.
    For instructions_md agents: appends a section to instructions.md.
    For none: reports unsupported.
    """
    pc_path = Path(personal_context_path)
    if not pc_path.is_file():
        return InstallResult(
            False, "error", personal_context_path,
            "personal-context/SKILL.md not found"
        )

    content = pc_path.read_text(encoding="utf-8")
    facts = _parse_personal_context(content)

    if not facts:
        return InstallResult(
            False, "skipped", personal_context_path,
            "no memory facts found in personal-context"
        )

    if agent.memory_format == "none":
        return InstallResult(
            False, "unsupported", "",
            f"{agent.display_name} has no supported memory mechanism"
        )

    # agents_md uses the project root (cwd), not a fixed memory_dir.
    if agent.memory_format == "agents_md":
        return _install_agents_md(facts, agent, dry_run)

    if agent.memory_format == "claude_memory":
        return _install_claude_memory(facts, agent, dry_run)
    elif agent.memory_format == "instructions_md":
        return _install_instructions_md(facts, agent, dry_run)
    elif agent.memory_format == "user_md":
        return _install_user_md(facts, agent, dry_run)
    else:
        return InstallResult(
            False, "unsupported", "",
            f"unknown memory format: {agent.memory_format}"
        )


def _install_claude_memory(
    facts: list[dict],
    agent: AgentTarget,
    dry_run: bool,
) -> InstallResult:
    """Install facts as .md files + MEMORY.md index in a Claude-style memory dir."""
    memory_dir = Path(agent.memory_dir)
    files_written: list[str] = []

    if dry_run:
        names = [f["name"] for f in facts]
        return InstallResult(
            True, "dry_run", str(memory_dir),
            f"would write {len(facts)} memory files: {', '.join(names)}",
            files_copied=names,
        )

    memory_dir.mkdir(parents=True, exist_ok=True)

    # Read existing MEMORY.md index (if any).
    index_path = memory_dir / "MEMORY.md"
    existing_index = ""
    existing_names: set[str] = set()
    if index_path.is_file():
        existing_index = index_path.read_text(encoding="utf-8")
        # Extract existing slugs from index lines like "- [Title](slug.md) — ..."
        existing_names = set(re.findall(r'\]\(([^)]+)\.md\)', existing_index))

    new_index_lines: list[str] = []
    updated_count = 0
    new_count = 0
    written_fact_paths: list[Path] = []

    try:
        for fact in facts:
            slug = fact["name"]
            fact_path = memory_dir / f"{slug}.md"

            # Write the fact file (overwrite if exists — the user approved this).
            # Frontmatter matches Claude Code's memory schema: node_type + type.
            fact_content = f"""---
name: {slug}
description: {fact['description']}
metadata:
  node_type: memory
  type: project
---

{fact['body']}
"""
            fact_path.write_text(fact_content, encoding="utf-8")
            written_fact_paths.append(fact_path)
            files_written.append(f"{slug}.md")

            if slug in existing_names:
                updated_count += 1
            else:
                new_count += 1

            # Index line — escape brackets in title to avoid breaking markdown links.
            safe_title = fact['title'].replace(']', '\\]').replace('[', '\\[')
            index_line = f"- [{safe_title}]({slug}.md) — {fact['description']}"
            new_index_lines.append(index_line)
    except Exception as e:
        # Rollback: remove any partially-written fact files.
        for p in written_fact_paths:
            try:
                p.unlink(missing_ok=True)
            except OSError:
                pass
        return InstallResult(
            False, "error", str(memory_dir),
            f"memory write failed after {len(written_fact_paths)} facts, rolled back: {e}",
        )

    # Update MEMORY.md: append new lines, skip duplicates.
    if existing_index:
        # Remove old lines for slugs we're updating, then append new ones.
        for slug in [f["name"] for f in facts]:
            existing_index = re.sub(
                r'^- \[[^\]]+\]\(' + re.escape(slug) + r'\.md\).*\n?',
                '', existing_index, flags=re.MULTILINE
            )
        # Append new lines, skipping any that are already present.
        existing_index = existing_index.rstrip() + '\n'
        for line, fact in zip(new_index_lines, facts):
            if f"]({fact['name']}.md)" not in existing_index:
                existing_index += line + '\n'
        index_path.write_text(existing_index, encoding="utf-8")
    else:
        index_path.write_text("# Memory Index\n\n" + "\n".join(new_index_lines) + "\n", encoding="utf-8")
    files_written.append("MEMORY.md (updated)")

    detail = f"installed {new_count} new, updated {updated_count} existing memory facts"
    return InstallResult(
        True, "copied", str(memory_dir),
        detail,
        files_copied=files_written,
    )


def _install_instructions_md(
    facts: list[dict],
    agent: AgentTarget,
    dry_run: bool,
) -> InstallResult:
    """Append personal context as a section to instructions.md (Codex convention)."""
    instructions_path = Path(agent.memory_dir)

    if dry_run:
        return InstallResult(
            True, "dry_run", str(instructions_path),
            f"would append {len(facts)} memory facts to {instructions_path.name}",
        )

    # Build the section.
    lines = ["", "## Personal Context", ""]
    for fact in facts:
        lines.append(f"### {fact['title']}")
        lines.append("")
        lines.append(fact['body'])
        lines.append("")

    section = "\n".join(lines)

    if instructions_path.exists():
        existing = instructions_path.read_text(encoding="utf-8")
        # Replace existing Personal Context section if present (case-insensitive).
        existing = re.sub(
            r'\n?## Personal Context\n.*?(?=\n## |\Z)',
            '', existing, flags=re.DOTALL | re.IGNORECASE
        )
        instructions_path.write_text(existing.rstrip() + "\n" + section, encoding="utf-8")
    else:
        instructions_path.write_text("# Instructions\n" + section, encoding="utf-8")

    return InstallResult(
        True, "copied", str(instructions_path),
        f"appended {len(facts)} memory facts to {instructions_path.name}",
        files_copied=[instructions_path.name],
    )


def _install_agents_md(
    facts: list[dict],
    agent: AgentTarget,
    dry_run: bool,
) -> InstallResult:
    """Install memory facts into AGENTS.md in the project root (Codex standard).

    Codex uses AGENTS.md in the repository root for project-specific instructions
    and context. We append a ## Personal Context section, replacing any existing one.
    The memory_dir for Codex is None — we write to AGENTS.md in the current cwd.
    """
    agents_path = Path(os.getcwd()) / "AGENTS.md"

    if dry_run:
        return InstallResult(
            True, "dry_run", str(agents_path),
            f"would append {len(facts)} memory facts to AGENTS.md",
        )

    lines = ["", "## Personal Context", ""]
    for fact in facts:
        lines.append(f"### {fact['title']}")
        lines.append("")
        lines.append(fact['body'])
        lines.append("")

    section = "\n".join(lines)

    if agents_path.exists():
        existing = agents_path.read_text(encoding="utf-8")
        existing = re.sub(
            r'\n?## Personal Context\n.*?(?=\n## |\Z)',
            '', existing, flags=re.DOTALL | re.IGNORECASE
        )
        agents_path.write_text(existing.rstrip() + "\n" + section, encoding="utf-8")
    else:
        agents_path.write_text("# Agents\n" + section, encoding="utf-8")

    return InstallResult(
        True, "copied", str(agents_path),
        f"appended {len(facts)} memory facts to AGENTS.md",
        files_copied=["AGENTS.md"],
    )


def _install_user_md(
    facts: list[dict],
    agent: AgentTarget,
    dry_run: bool,
) -> InstallResult:
    """Install memory facts into USER.md in OpenClaw's workspace.

    OpenClaw uses USER.md for stable preferences and active context. We write
    all facts into a single USER.md file, replacing any existing Personal Context
    section.
    """
    workspace = Path(agent.memory_dir) if agent.memory_dir else Path(os.getcwd())
    user_md_path = workspace / "USER.md"

    if dry_run:
        return InstallResult(
            True, "dry_run", str(user_md_path),
            f"would write {len(facts)} memory facts to USER.md",
        )

    lines = ["# User", ""]
    for fact in facts:
        lines.append(f"## {fact['title']}")
        lines.append("")
        lines.append(fact['body'])
        lines.append("")

    content = "\n".join(lines)

    if user_md_path.exists():
        existing = user_md_path.read_text(encoding="utf-8")
        # Preserve any content that isn't under ## headings we're writing.
        # For simplicity, replace the entire file since USER.md is memory-managed.
        user_md_path.write_text(content, encoding="utf-8")
    else:
        workspace.mkdir(parents=True, exist_ok=True)
        user_md_path.write_text(content, encoding="utf-8")

    return InstallResult(
        True, "copied", str(user_md_path),
        f"wrote {len(facts)} memory facts to USER.md",
        files_copied=["USER.md"],
    )
