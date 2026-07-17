#!/usr/bin/env bash
# Generate SKILLS.md — a catalog of every skill across own skills/ + the three
# submodules, so an external agent can survey what's available and recommend
# the useful ones for a given task.
#
# Pulls name + description from each SKILL.md's YAML frontmatter. Handles:
#  - plain scalar descriptions (description: Foo bar)
#  - block-scalar descriptions (description: > / |- spanning lines)
#  - nested layouts (mattpocock skills/<category>/<skill>/)
#  - excludes _analysis/ and other non-skill dirs
#
# Usage: ./scripts/generate-skills-catalog.sh   (writes SKILLS.md at repo root)
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

OUT="SKILLS.md"

# --- helpers ----------------------------------------------------------------

# extract_description <SKILL.md path>
# prints the description value, flattening YAML block scalars (>, |) to one line.
extract_description() {
  local f="$1"
  # Grab frontmatter (between first two '---' lines), find the description,
  # and collapse block scalars. Using awk for portability.
  awk '
    BEGIN { in_fm=0; desc_started=0; block=0; buf="" }
    /^---[[:space:]]*$/ { in_fm++; if (in_fm==2) exit; next }
    {
      if (in_fm==1) {
        if (!desc_started && /^description:[[:space:]]*(>.?|\|.*)[[:space:]]*$/) {
          # block scalar — value is on following indented lines
          desc_started=1; block=1; next
        }
        if (!desc_started && /^description:[[:space:]]*(.+)/) {
          # plain or folded single-line — strip quotes
          s=$0
          sub(/^description:[[:space:]]*/,"",s)
          gsub(/^["'\'']|["'\'']$/,"",s)
          sub(/[[:space:]]*$/,"",s)
          print s
          exit
        }
        if (desc_started && block) {
          # indented continuation line of a block scalar
          if ($0 ~ /^[[:space:]]+/) {
            t=$0; sub(/^[[:space:]]+/,"",t); sub(/[[:space:]]*$/,"",t)
            buf = buf (buf=="" ? "" : " ") t
          } else { exit }
        }
      }
    }
    END { if (block) print buf }
  ' "$f"
}

# render a source section: <heading> <skill-dir-glob-base> <path-prefix-for-links>
# Globs all SKILL.md under the base, excluding junk dirs.
# For nested layouts (skill dir has a category parent), shows the category and
# flags deprecated/in-progress skills so an agent doesn't pick stale drafts.
render_section() {
  local heading="$1"
  local base="$2"          # e.g. skills  or  anthropic-skills/skills
  local linkprefix="$3"    # e.g. ./skills or ./anthropic-skills/skills
  local count=0
  local rows=""
  local nested=0

  # detect nested layout: any SKILL.md two levels under base (base/cat/skill/SKILL.md)
  if find "$base" -mindepth 3 -name SKILL.md -type f 2>/dev/null | grep -q .; then
    nested=1
  fi

  # find SKILL.md files, sorted by path
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    # skip non-skill dirs
    case "$f" in
      */_analysis/*|*/node_modules/*|*/.git/*) continue ;;
    esac
    # skill dir path relative to base
    local skilldir
    skilldir="$(dirname "$f")"
    skilldir="${skilldir#$base/}"
    local name
    name="$(basename "$skilldir")"
    local desc
    desc="$(extract_description "$f")"
    [ -z "$desc" ] && desc="(no description)"
    # collapse to a single line and trim
    desc="$(printf '%s' "$desc" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^ //; s/ $//')"
    if [ "$nested" -eq 1 ]; then
      # skilldir is <category>/<skill> — show category, flag drafts
      local cat status
      cat="${skilldir%%/*}"
      status=""
      case "$cat" in
        deprecated) status="⚠️ deprecated" ;;
        in-progress) status="🚧 in-progress" ;;
        *) status="$cat" ;;
      esac
      rows+="| [\`$name\`]($linkprefix/$skilldir) | $status | $desc |"$'\n'
    else
      rows+="| [\`$name\`]($linkprefix/$skilldir) | $desc |"$'\n'
    fi
    count=$((count+1))
  done < <(find "$base" -name SKILL.md -type f 2>/dev/null | sort)

  printf '### %s (%d)\n\n' "$heading" "$count"
  if [ "$nested" -eq 1 ]; then
    printf '| Skill | Category | Description |\n'
    printf '|---|---|---|\n'
  else
    printf '| Skill | Description |\n'
    printf '|---|---|\n'
  fi
  printf '%s' "$rows"
  printf '\n'
}

{
  cat <<'HEADER'
# Skills catalog

A machine- and human-readable index of **every skill** in this repo — own skills
plus three external collections tracked as git submodules.

## How an agent should use this

Read the tables below, pick the skills relevant to the user's task, and
**recommend** them (name + path). The user activates picks manually — do not
attempt to install anything yourself. Prefer stable skills; skip any flagged
⚠️ deprecated or 🚧 in-progress unless the user asks for them. Each skill's
`SKILL.md` (linked from the path) has the full instructions — open it when a
pick is relevant to follow its steps.

Regenerate after adding/removing skills: `./scripts/generate-skills-catalog.sh`

## Own skills (`skills/`)

HEADER

  render_section "Own skills (skills/)" "skills" "./skills"

  cat <<'MID'

## External collections (git submodules)

These are tracked upstream and updated via `git submodule update --remote`.
Their skills are read-only references — don't edit in place.

MID

  render_section "Anthropic skills (anthropic-skills/skills/)" "anthropic-skills/skills" "./anthropic-skills/skills"
  render_section "Superpowers (superpowers/skills/)" "superpowers/skills" "./superpowers/skills"
  render_section "Mattpocock skills (mattpocock-skills/skills/)" "mattpocock-skills/skills" "./mattpocock-skills/skills"

  cat <<'FOOTER'

## Using a picked skill

Once an agent recommends skills from the catalog, activate them manually. For
Claude Code, symlink (or copy) the skill folder into your personal skills dir:

```bash
# Windows (Git Bash)
ln -s "$(pwd)/<path-from-catalog>/<skill-name>" "$HOME/.claude/skills/<skill-name>"
```

For the submodules, use the full path from the table, e.g.
`./anthropic-skills/skills/pdf` or `./mattpocock-skills/skills/engineering/tdd`.

For other agents, follow their skill-discovery convention, or just open the
skill's `SKILL.md` and follow the steps directly — every skill is self-contained.
FOOTER
} > "$OUT"

echo "Wrote $OUT ($(grep -c '^| \[`' "$OUT") skills listed)"
