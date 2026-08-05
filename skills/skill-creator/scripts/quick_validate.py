#!/usr/bin/env python3
"""Validate the portable core of a skill using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
KEY_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]*(.*))?$")
PORTABLE_FIELDS = {"name", "description"}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors


def parse_frontmatter(content: str) -> tuple[dict[str, str], str, str | None]:
    normalized = content.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}, "", "SKILL.md must start with YAML frontmatter"
    end = normalized.find("\n---\n", 4)
    if end < 0:
        return {}, "", "frontmatter closing delimiter not found"

    raw = normalized[4:end]
    body = normalized[end + 5 :]
    values: dict[str, str] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line[:1].isspace():
            index += 1
            continue
        match = KEY_PATTERN.match(line)
        if not match:
            return {}, body, f"unsupported or invalid frontmatter line {index + 1}: {line!r}"
        key, scalar = match.groups()
        if key in values:
            return {}, body, f"duplicate frontmatter field: {key}"
        scalar = (scalar or "").strip()
        if scalar in {"|", ">", "|-", ">-", "|+", ">+"}:
            block: list[str] = []
            index += 1
            while index < len(lines) and (lines[index][:1].isspace() or not lines[index]):
                block.append(lines[index].lstrip())
                index += 1
            values[key] = ("\n" if scalar.startswith("|") else " ").join(block).strip()
            continue
        if scalar and scalar[0:1] in {'"', "'"} and scalar[-1:] == scalar[0]:
            scalar = scalar[1:-1]
        values[key] = scalar
        index += 1
    return values, body, None


def validate_skill(skill_path: str | Path, strict_portable: bool = False) -> ValidationResult:
    path = Path(skill_path).resolve()
    result = ValidationResult()
    if not path.is_dir():
        result.errors.append(f"skill directory not found: {path}")
        return result

    skill_file = path / "SKILL.md"
    if not skill_file.is_file():
        result.errors.append("SKILL.md not found")
        return result

    try:
        content = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        result.errors.append(f"cannot read SKILL.md as UTF-8: {error}")
        return result

    frontmatter, body, parse_error = parse_frontmatter(content)
    if parse_error:
        result.errors.append(parse_error)
        return result

    for required in sorted(PORTABLE_FIELDS):
        if not frontmatter.get(required, "").strip():
            result.errors.append(f"missing or empty frontmatter field: {required}")

    name = frontmatter.get("name", "").strip()
    if name:
        if len(name) > 64:
            result.errors.append("name exceeds 64 characters")
        if not NAME_PATTERN.fullmatch(name):
            result.errors.append("name must use lowercase letters, digits, and single hyphens")
        if name != path.name:
            result.errors.append(f"frontmatter name {name!r} does not match directory {path.name!r}")

    description = frontmatter.get("description", "").strip()
    if description:
        if len(description) > 1024:
            result.errors.append("description exceeds 1024 characters")
        if "<" in description or ">" in description:
            result.warnings.append("description contains angle brackets; some consumers reject them")
        lowered = description.lower()
        if not any(term in lowered for term in ("use when", "when ", "for ", "requests", "tasks")):
            result.warnings.append("description may not explain when the skill should be selected")

    extension_fields = set(frontmatter) - PORTABLE_FIELDS
    if strict_portable and extension_fields:
        result.errors.append(
            "strict portable mode permits only name and description; extension fields: "
            + ", ".join(sorted(extension_fields))
        )
    else:
        if extension_fields:
            result.warnings.append(
                "platform or distribution extensions require target-specific validation: "
                + ", ".join(sorted(extension_fields))
            )

    if not body.strip():
        result.errors.append("SKILL.md body is empty")
    if "TODO" in body:
        result.warnings.append("SKILL.md still contains TODO markers")
    if len(body.splitlines()) > 500:
        result.warnings.append("SKILL.md body exceeds 500 lines; consider progressive disclosure")

    for target in LINK_PATTERN.findall(body):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        decoded = target.replace("%20", " ")
        linked = (path / decoded).resolve()
        try:
            linked.relative_to(path)
        except ValueError:
            result.warnings.append(f"relative link escapes the skill directory: {target}")
            continue
        if not linked.exists():
            result.errors.append(f"referenced file does not exist: {target}")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument(
        "--strict-portable",
        action="store_true",
        help="reject all frontmatter fields except name and description",
    )
    args = parser.parse_args()
    result = validate_skill(args.skill_directory, args.strict_portable)
    for warning in result.warnings:
        print(f"warning: {warning}")
    for error in result.errors:
        print(f"error: {error}")
    if result.valid:
        print("valid")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
