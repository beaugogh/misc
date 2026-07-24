#!/usr/bin/env bash
# Generate CATALOG.md — a machine- and human-readable catalog of EVERY
# discoverable agent-facing artifact in this repo: skills (own + 3 submodules)
# and OpenCLI plugins. One file an external agent reads to survey what's
# available and how each artifact is activated.
#
#   - Skills:       name + description pulled from each SKILL.md's YAML
#                   frontmatter (handles plain + block-scalar descriptions,
#                   nested submodule layouts, excludes junk dirs).
#   - Plugins:      name + commands pulled from each plugin's
#                   opencli-plugin.json `commands` array (the manifest is the
#                   catalog source of truth; search.ts is the runtime source
#                   of truth — keep them in sync).
#
# Supersedes the former generate-skills-catalog.sh + SKILLS.md (skills-only).
# Usage: ./scripts/generate-catalog.sh   (writes CATALOG.md at repo root)
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

OUT="CATALOG.md"

# --- skills helpers ---------------------------------------------------------

# extract_description <SKILL.md path>
# prints the description value, flattening YAML block scalars (>, |) to one line.
extract_description() {
  local f="$1"
  awk '
    BEGIN { in_fm=0; desc_started=0; block=0; buf="" }
    /^---[[:space:]]*$/ { in_fm++; if (in_fm==2) exit; next }
    {
      if (in_fm==1) {
        if (!desc_started && /^description:[[:space:]]*(>.?|\|.*)[[:space:]]*$/) {
          desc_started=1; block=1; next
        }
        if (!desc_started && /^description:[[:space:]]*(.+)/) {
          s=$0
          sub(/^description:[[:space:]]*/,"",s)
          gsub(/^["'\'']|["'\'']$/,"",s)
          sub(/[[:space:]]*$/,"",s)
          print s
          exit
        }
        if (desc_started && block) {
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

# render_skill_section <heading> <skill-dir-base> <link-prefix>
# Globs all SKILL.md under base (excluding junk), one row each. Flags
# deprecated/in-progress skills in nested submodule layouts.
render_skill_section() {
  local heading="$1"
  local base="$2"          # e.g. skills  or  anthropic-skills/skills
  local linkprefix="$3"    # e.g. ./skills or ./anthropic-skills/skills
  local count=0
  local rows=""
  local nested=0

  if find "$base" -mindepth 3 -name SKILL.md -type f 2>/dev/null | grep -q .; then
    nested=1
  fi

  while IFS= read -r f; do
    [ -z "$f" ] && continue
    case "$f" in
      */_analysis/*|*/node_modules/*|*/.git/*) continue ;;
    esac
    local skilldir
    skilldir="$(dirname "$f")"
    skilldir="${skilldir#$base/}"
    local name
    name="$(basename "$skilldir")"
    local desc
    desc="$(extract_description "$f")"
    [ -z "$desc" ] && desc="(no description)"
    desc="$(printf '%s' "$desc" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^ //; s/ $//')"
    if [ "$nested" -eq 1 ]; then
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

# --- plugin helper ----------------------------------------------------------
# Emit one TSV row per plugin: name <TAB> commands-json <TAB> readme-path.
# JSON parsing in pure bash/awk is fragile, so use node (already a hard
# prerequisite for this repo's OpenCLI side). Output is plain TSV for bash to
# format into markdown; descriptions are kept as-is (may contain pipes/Unicode
# — escaped below when rendered).
emit_plugins_tsv() {
  node -e '
    const fs = require("fs");
    const path = require("path");
    const dir = "opencli-plugins";
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); }
    catch { process.exit(0); }  // no plugins dir -> no rows
    const rows = [];
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      const manifest = path.join(dir, e.name, "opencli-plugin.json");
      if (!fs.existsSync(manifest)) continue;
      let m;
      try { m = JSON.parse(fs.readFileSync(manifest, "utf8")); }
      catch (err) { console.error(`skip ${e.name}: invalid opencli-plugin.json (${err.message})`); continue; }
      const name = m.name || e.name;
      const commands = Array.isArray(m.commands) ? m.commands : [];
      const cmds = commands.map(c => ({
        name: c.name || "",
        description: c.description || "",
        args: Array.isArray(c.args) ? c.args.map(a => ({
          name: a.name || "",
          positional: !!a.positional,
          required: !!a.required,
          type: a.type || "",
          default: a.default !== undefined ? String(a.default) : null,
          help: a.help || ""
        })) : [],
        columns: Array.isArray(c.columns) ? c.columns : []
      }));
      const readme = path.join(dir, e.name, "README.md");
      const hasReadme = fs.existsSync(readme) ? `./${readme.split(path.sep).join("/")}` : "";
      // TSV: name \t JSON(commands) \t readme-link
      rows.push([name, JSON.stringify(cmds), hasReadme].join("\t"));
    }
    process.stdout.write(rows.join("\n") + "\n");
  '
}

# Escape pipes for a markdown table cell without collapsing newlines (so
# multi-line command cells keep their line breaks). Trims leading/trailing
# space per line.
md_cell_multiline() {
  printf '%s' "$1" | sed 's/|/\\|/g; s/  *$//; s/^  *//'
}

render_plugin_section() {
  local count=0
  local rows=""
  local tsv
  tsv="$(emit_plugins_tsv)"
  while IFS=$'\t' read -r name cmds_json readme; do
    [ -z "$name" ] && continue
    # Format commands: "**`search`** <query> · --limit <int> · --language"
    # followed by a "columns: ..." line. Keep newlines (md_cell_multiline
    # preserves them) so each command + its columns render on separate lines.
    local cmds_md=""
    if [ -n "$cmds_json" ] && [ "$cmds_json" != "[]" ]; then
      cmds_md="$(printf '%s' "$cmds_json" | node -e '
        let s = ""; process.stdin.on("data", d => s += d);
        process.stdin.on("end", () => {
          const cmds = JSON.parse(s);
          const out = cmds.map(c => {
            const args = c.args.map(a => {
              let n = a.positional ? `<${a.name}>` : `--${a.name}`;
              if (!a.positional && a.type === "int") n += " <int>";
              return n;
            }).join(" · ");
            const cols = c.columns.join(", ");
            return `**\`${c.name}\`** ${args}<br>columns: \`${cols}\``;
          });
          process.stdout.write(out.join("<br><br>"));
        });
      ')"
    fi
    local name_cell
    if [ -n "$readme" ]; then
      name_cell='[`'"$name"'`]('"$readme"')'
    else
      name_cell='[`'"$name"'`]'
    fi
    rows+="| $name_cell | $(md_cell_multiline "$cmds_md") |"$'\n'
    count=$((count+1))
  done <<< "$tsv"

  printf '### Plugins (%d)\n\n' "$count"
  printf '| Plugin | Commands |\n'
  printf '|---|---|\n'
  printf '%s' "$rows"
  printf '\n'
}

# --- assemble CATALOG.md ----------------------------------------------------
{
  cat <<'HEADER'
# Catalog

A machine- and human-readable index of **every agent-facing artifact** in this
repo — skills (own + three external collections) and OpenCLI plugins — so an
external agent can survey what's available in one place.

## How an agent should use this

Read the sections below, pick the artifacts relevant to the user's task, and
**recommend** them (name + path). The user activates picks manually — do not
attempt to install anything yourself. Prefer stable skills; skip any flagged
⚠️ deprecated or 🚧 in-progress unless the user asks for them.

There are **two kinds** of artifact, with different activation models — an
agent must know which is which:

- **Skill** — open its `SKILL.md` (linked from the path) and follow the steps.
  Self-contained instructions, no prerequisites. Portable as a document.
- **OpenCLI plugin** — a CLI command `opencli <plugin> <command>` you call.
  Needs `opencli` + the Browser Bridge set up and (for Huawei-site plugins) a
  logged-in Huawei session in Chrome — all human one-time setup. Portable as a
  *command*, not as pure code. See [`opencli-plugins/README.md`](./opencli-plugins/README.md)
  for prerequisites and install.

Regenerate after adding/removing skills or plugins: `./scripts/generate-catalog.sh`

## Skills

HEADER

  render_skill_section "Own skills (skills/)" "skills" "./skills"

  cat <<'MID'

### External collections (git submodules)

Tracked upstream and updated via `git submodule update --remote`. Their skills
are read-only references — don't edit in place.

MID

  render_skill_section "Anthropic skills (anthropic-skills/skills/)" "anthropic-skills/skills" "./anthropic-skills/skills"
  render_skill_section "Superpowers (superpowers/skills/)" "superpowers/skills" "./superpowers/skills"
  render_skill_section "Mattpocock skills (mattpocock-skills/skills/)" "mattpocock-skills/skills" "./mattpocock-skills/skills"

  cat <<'PLUGHDR'

## OpenCLI plugins

Each plugin's `opencli-plugin.json` `commands` array declares the command
surface (args + output columns) — that manifest is the catalog source of
truth. Full recon notes and setup live in each plugin's `README.md`.

PLUGHDR

  render_plugin_section

  cat <<'FOOTER'

## Using a picked skill

Activate manually. For Claude Code, symlink (or copy) the skill folder into
your personal skills dir:

```bash
# Windows (Git Bash)
ln -s "$(pwd)/<path-from-catalog>/<skill-name>" "$HOME/.claude/skills/<skill-name>"
```

For the submodules, use the full path from the table, e.g.
`./anthropic-skills/skills/pdf` or `./mattpocock-skills/skills/engineering/tdd`.

For other agents, follow their skill-discovery convention, or just open the
skill's `SKILL.md` and follow the steps directly — every skill is self-contained.

## Using a picked plugin

Install once (see `opencli-plugins/README.md`), then call as a CLI command:

```bash
opencli <plugin> <command> [args]        # e.g. opencli huawei-jiaxian search "盘古" --limit 3
```
FOOTER
} > "$OUT"

skills_count=$(grep -cE '^\| \[`' "$OUT" || true)
echo "Wrote $OUT (rows: $skills_count)"
