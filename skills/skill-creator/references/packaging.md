# Safe Packaging

Read this reference before creating or distributing a skill archive.

## Inclusion policy

Package from an allowlist, not an unrestricted recursive copy. The included packager allows:

- `SKILL.md`;
- top-level license and notice files;
- regular files below `scripts/`, `references/`, and `assets/`.

Keep platform adapters only when the intended recipient needs them and explicitly add them with `--include`. Review custom includes carefully.

## Default exclusions

Reject or exclude:

- version-control metadata, caches, virtual environments, build outputs, and editor state;
- evaluation workspaces, generated reports, and temporary notes;
- environment files, credentials, private keys, token stores, and suspicious secret-bearing names;
- symlinks, sockets, devices, and paths escaping the skill root;
- a previously generated archive inside the skill directory.

Scan text files for common credential patterns. Automated scans are fallible, so inspect the manifest and sample sensitive-looking content manually.

## Reproducibility and inspection

Validate before packaging. Sort archive paths and use stable metadata where the packaging tool supports it. After creation:

1. list the archive entries;
2. confirm that `skill-name/SKILL.md` is present;
3. confirm that every entry is intentional;
4. extract to a temporary location and validate the extracted skill when distribution risk warrants it.

Never weaken a failed safety check merely to complete packaging. Use an explicit override only after identifying and accepting the exact flagged file.
