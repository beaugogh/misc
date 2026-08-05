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
    action: str               # "copied" | "skipped" | "conflict" | "error" | "unsupported" | "dry_run"
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
    # (same structure quick_validate checks).
    copied: list[str] = []
    try:
        shutil.copytree(source, target)
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


# ---------------------------------------------------------------------------
# Memory installation (personal-context → agent memory system)
# ---------------------------------------------------------------------------

def _parse_personal_context(content: str) -> list[dict]:
    """Parse personal-context/SKILL.md body into individual memory facts.

    Extracts sections marked by ## headings. Each becomes one memory file.
    Returns a list of {name, description, body} dicts.
    """
    facts: list[dict] = []
    # Split on ## headings (but not # which is the title).
    sections = re.split(r'^## ', content, flags=re.MULTILINE)
    for section in sections[1:]:  # skip content before first ##
        lines = section.strip().split('\n')
        title = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        if not title:
            continue
        # Derive a slug from the title.
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        if not slug:
            slug = "unnamed-fact"
        # Description: first sentence of body, truncated.
        first_sentence = body.split('.')[0][:100] if body else title
        facts.append({
            "name": slug,
            "title": title,
            "description": first_sentence,
            "body": body,
        })
    return facts


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

    if agent.memory_format == "none" or agent.memory_dir is None:
        return InstallResult(
            False, "unsupported", "",
            f"{agent.display_name} has no supported memory mechanism"
        )

    if agent.memory_format == "claude_memory":
        return _install_claude_memory(facts, agent, dry_run)
    elif agent.memory_format == "instructions_md":
        return _install_instructions_md(facts, agent, dry_run)
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

    for fact in facts:
        slug = fact["name"]
        fact_path = memory_dir / f"{slug}.md"

        # Write the fact file (overwrite if exists — the user approved this).
        fact_content = f"""---
name: {slug}
description: {fact['description']}
metadata:
  type: user
---

{fact['body']}
"""
        fact_path.write_text(fact_content, encoding="utf-8")
        files_written.append(f"{slug}.md")

        if slug in existing_names:
            updated_count += 1
        else:
            new_count += 1

        # Index line.
        index_line = f"- [{fact['title']}]({slug}.md) — {fact['description']}"
        new_index_lines.append(index_line)

    # Update MEMORY.md: append new lines, skip duplicates.
    if existing_index:
        # Remove old lines for slugs we're updating, then append new ones.
        for slug in [f["name"] for f in facts]:
            existing_index = re.sub(
                r'^- \[[^\]]+\]\(' + re.escape(slug) + r'\.md\).*\n?',
                '', existing_index, flags=re.MULTILINE
            )
        # Append new lines.
        existing_index = existing_index.rstrip() + '\n'
        for line in new_index_lines:
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
        # Replace existing Personal Context section if present.
        existing = re.sub(
            r'\n?## Personal Context\n.*?(?=\n## |\Z)',
            '', existing, flags=re.DOTALL
        )
        instructions_path.write_text(existing.rstrip() + "\n" + section, encoding="utf-8")
    else:
        instructions_path.write_text("# Instructions\n" + section, encoding="utf-8")

    return InstallResult(
        True, "copied", str(instructions_path),
        f"appended {len(facts)} memory facts to {instructions_path.name}",
        files_copied=[instructions_path.name],
    )
