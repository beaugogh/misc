#!/usr/bin/env python3
"""Create a deterministic, safety-checked .skill ZIP archive."""

from __future__ import annotations

import argparse
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

from quick_validate import validate_skill

ALLOWED_ROOTS = {"scripts", "references", "assets"}
TOP_LEVEL_PREFIXES = ("LICENSE", "NOTICE")
BLOCKED_PARTS = {
    ".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".venv", "venv", "node_modules", "dist", "build", "evaluation-workspace",
}
SENSITIVE_NAMES = re.compile(
    r"(^|[._-])(env|credentials?|secrets?|tokens?|id_rsa|id_ed25519|private[-_]?key)([._-]|$)",
    re.IGNORECASE,
)
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{16,}"),
)
MAX_SCAN_BYTES = 2_000_000
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def is_default_candidate(relative: Path) -> bool:
    if relative == Path("SKILL.md"):
        return True
    if len(relative.parts) == 1 and relative.name.startswith(TOP_LEVEL_PREFIXES):
        return True
    return bool(relative.parts and relative.parts[0] in ALLOWED_ROOTS)


def collect_files(root: Path, includes: list[str]) -> tuple[list[Path], list[str]]:
    candidates: set[Path] = set()
    problems: list[str] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if is_default_candidate(relative):
            candidates.add(path)
    for requested in includes:
        unresolved = root / requested
        target = unresolved.resolve()
        try:
            target.relative_to(root)
        except ValueError:
            problems.append(f"include escapes skill directory: {requested}")
            continue
        if unresolved.is_symlink():
            problems.append(f"symlink is not packageable: {requested}")
        elif not target.exists():
            problems.append(f"include not found: {requested}")
        elif target.is_dir():
            candidates.update(target.rglob("*"))
        else:
            candidates.add(target)

    files: list[Path] = []
    for path in sorted(candidates):
        relative = path.relative_to(root)
        if any(part in BLOCKED_PARTS or part.startswith(".") for part in relative.parts):
            continue
        if path.is_symlink():
            problems.append(f"symlink is not packageable: {relative}")
            continue
        try:
            mode = path.stat().st_mode
        except OSError as error:
            problems.append(f"cannot inspect {relative}: {error}")
            continue
        if not stat.S_ISREG(mode):
            if not path.is_dir():
                problems.append(f"non-regular file is not packageable: {relative}")
            continue
        if SENSITIVE_NAMES.search(relative.name):
            problems.append(f"sensitive-looking filename: {relative}")
            continue
        try:
            data = path.read_bytes()[:MAX_SCAN_BYTES]
        except OSError as error:
            problems.append(f"cannot read {relative}: {error}")
            continue
        if any(pattern.search(data) for pattern in SECRET_PATTERNS):
            problems.append(f"possible secret content: {relative}")
            continue
        files.append(path)
    return files, problems


def package_skill(skill_path: str | Path, output_dir: str | Path | None = None, includes: list[str] | None = None) -> Path:
    root = Path(skill_path).resolve()
    validation = validate_skill(root)
    if not validation.valid:
        raise ValueError("validation failed: " + "; ".join(validation.errors))

    files, problems = collect_files(root, includes or [])
    if problems:
        raise ValueError("packaging safety checks failed: " + "; ".join(problems))
    if root / "SKILL.md" not in files:
        raise ValueError("SKILL.md is missing from package manifest")

    destination = Path(output_dir).resolve() if output_dir else Path.cwd().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f"{root.name}.skill"
    if archive.is_relative_to(root):
        raise ValueError("output archive must be outside the skill directory")

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in files:
            relative = PurePosixPath(root.name, *path.relative_to(root).parts)
            info = zipfile.ZipInfo(str(relative), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644) << 16
            bundle.writestr(info, path.read_bytes())
            print(relative)
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument("output_directory", nargs="?")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="explicit extra relative file or directory; repeat as needed",
    )
    args = parser.parse_args()
    try:
        archive = package_skill(args.skill_directory, args.output_directory, args.include)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"created: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
