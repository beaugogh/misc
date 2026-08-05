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
PREVIOUS_CATALOG="$(mktemp)"
trap 'rm -f "$PREVIOUS_CATALOG"' EXIT
if [ -f "$OUT" ]; then
  cp "$OUT" "$PREVIOUS_CATALOG"
fi

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
  local base="$2"          # e.g. skills  or  skills/anthropic-skills/skills
  local linkprefix="$3"    # e.g. ./skills or ./skills/anthropic-skills/skills
  local count=0
  local rows=""
  local nested=0

  # Partial clones may have gitlinks without initialized submodule contents.
  # Preserve the last generated external section instead of replacing it with
  # an incorrect empty table.
  if [ "$base" != "skills" ] && [ -z "$(find "$base" -name SKILL.md -type f -print -quit 2>/dev/null)" ]; then
    awk -v marker="### $heading (" '
      index($0, marker) == 1 { found=1 }
      found && printed && ($0 ~ /^### / || $0 ~ /^## /) { exit }
      found { print; printed=1 }
    ' "$PREVIOUS_CATALOG"
    return
  fi

  if [ -n "$(find "$base" -mindepth 3 -name SKILL.md -type f -print -quit 2>/dev/null)" ]; then
    nested=1
  fi

  while IFS= read -r f; do
    [ -z "$f" ] && continue
    # A tracked skill may be intentionally deleted in the working tree before
    # the deletion is staged. Catalog the filesystem state, not the old index.
    [ -f "$f" ] || continue
    case "$f" in
      */_analysis/*|*/node_modules/*|*/.git/*) continue ;;
    esac
    # When scanning the own-skills base, skip vendored submodule collections
    # nested under skills/ — they are scanned in their own dedicated sections
    # below, so don't double-count. (Only relevant for base="skills".)
    if [ "$base" = "skills" ]; then
      case "$f" in
        skills/anthropic-skills/*|skills/mattpocock-skills/*|skills/superpowers/*) continue ;;
      esac
    fi
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
  done < <(
    if [ "$base" = "skills" ]; then
      # Include tracked and ordinary untracked skills, but never gitignored
      # generated output such as personal memories.
      git ls-files --cached --others --exclude-standard -- 'skills/**/SKILL.md' | sort
    else
      find "$base" -name SKILL.md -type f 2>/dev/null | sort
    fi
  )

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

# --- mcp-tool helper --------------------------------------------------------
# Emit one TSV row per MCP tool: name <TAB> transport <TAB> tools-json <TAB>
# readme-path. Mirrors emit_plugins_tsv but reads mcp-tool.json manifests.
emit_mcptools_tsv() {
  node -e '
    const fs = require("fs");
    const path = require("path");
    const dir = "mcp-tools";
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); }
    catch { process.exit(0); }  // no mcp-tools dir -> no rows
    const rows = [];
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      const manifest = path.join(dir, e.name, "mcp-tool.json");
      if (!fs.existsSync(manifest)) continue;
      let m;
      try { m = JSON.parse(fs.readFileSync(manifest, "utf8")); }
      catch (err) { console.error(`skip ${e.name}: invalid mcp-tool.json (${err.message})`); continue; }
      const name = m.name || e.name;
      const transport = m.transport || "remote";
      const tools = Array.isArray(m.tools) ? m.tools.map(t => ({
        name: t.name || "",
        description: t.description || "",
        args: Array.isArray(t.args) ? t.args.map(a => ({
          name: a.name || "",
          required: !!a.required,
          default: a.default !== undefined ? String(a.default) : null,
          help: a.help || ""
        })) : [],
        output_fields: Array.isArray(t.output_fields) ? t.output_fields : []
      })) : [];
      const readme = path.join(dir, e.name, "README.md");
      const hasReadme = fs.existsSync(readme) ? `./${readme.split(path.sep).join("/")}` : "";
      rows.push([name, transport, JSON.stringify(tools), hasReadme].join("\t"));
    }
    process.stdout.write(rows.join("\n") + "\n");
  '
}

render_mcptool_section() {
  local count=0
  local rows=""
  local tsv
  tsv="$(emit_mcptools_tsv)"
  while IFS=$'\t' read -r name transport tools_json readme; do
    [ -z "$name" ] && continue
    local tools_md=""
    if [ -n "$tools_json" ] && [ "$tools_json" != "[]" ]; then
      tools_md="$(printf '%s' "$tools_json" | node -e '
        let s = ""; process.stdin.on("data", d => s += d);
        process.stdin.on("end", () => {
          const tools = JSON.parse(s);
          const out = tools.map(t => {
            const args = t.args.map(a => {
              let n = a.required ? `<${a.name}>` : `--${a.name}`;
              if (a.default !== null) n += `=${a.default}`;
              return n;
            }).join(" · ");
            const cols = t.output_fields.join(", ");
            return `**\`${t.name}\`** ${args}${cols ? `<br>output: \`${cols}\`` : ""}`;
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
    rows+="| $name_cell | $transport | $(md_cell_multiline "$tools_md") |"$'\n'
    count=$((count+1))
  done <<< "$tsv"

  printf '### MCP tools (%d)\n\n' "$count"
  printf '| Tool | Transport | MCP tools |\n'
  printf '|---|---|---|\n'
  printf '%s' "$rows"
  printf '\n'
}

# --- assemble CATALOG.md ----------------------------------------------------
{
  cat <<'HEADER'
# Catalog

A machine- and human-readable index of **every agent-facing artifact** in this
repo — skills (own + three external collections), OpenCLI plugins, and MCP
tools — so an external agent can survey what's available in one place.

## How an agent should use this

Read the sections below, pick the artifacts relevant to the user's task, and
**recommend** them (name + path). The user activates picks manually — do not
attempt to install anything yourself. Prefer stable skills; skip any flagged
⚠️ deprecated or 🚧 in-progress unless the user asks for them.

There are **three kinds** of artifact, with different activation models — an
agent must know which is which:

- **Skill** — open its `SKILL.md` (linked from the path) and follow the steps.
  Self-contained instructions, no prerequisites. Portable as a document.
- **OpenCLI plugin** — a CLI command `opencli <plugin> <command>` you call.
  Needs `opencli` + the Browser Bridge set up and (for Huawei-site plugins) a
  logged-in Huawei session in Chrome — all human one-time setup. Portable as a
  *command*, not as pure code. See [`opencli-plugins/README.md`](./opencli-plugins/README.md)
  for prerequisites and install.
- **MCP tool** — a remote MCP server packaged to work out of the box for any
  agent. Load the bundled config (Claude Code `.mcp.json` / opencode
  `--mcp-config`) to expose its MCP tool, **or** run the bundled wrapper script
  via Bash + Python 3 — no MCP support required. No install step, no bundled
  credentials. See [`mcp-tools/README.md`](./mcp-tools/README.md).

Regenerate after adding/removing skills, plugins, or MCP tools: `./scripts/generate-catalog.sh`

## Skills

HEADER

  render_skill_section "Own skills (skills/)" "skills" "./skills"

  cat <<'MID'

### External collections (git submodules)

Tracked upstream and updated via `git submodule update --remote`. Their skills
are read-only references — don't edit in place.

MID

  render_skill_section "Anthropic skills (skills/anthropic-skills/skills/)" "skills/anthropic-skills/skills" "./skills/anthropic-skills/skills"
  render_skill_section "Superpowers (skills/superpowers/skills/)" "skills/superpowers/skills" "./skills/superpowers/skills"
  render_skill_section "Mattpocock skills (skills/mattpocock-skills/skills/)" "skills/mattpocock-skills/skills" "./skills/mattpocock-skills/skills"

  cat <<'PLUGHDR'

## OpenCLI plugins

Each plugin's `opencli-plugin.json` `commands` array declares the command
surface (args + output columns) — that manifest is the catalog source of
truth. Full recon notes and setup live in each plugin's `README.md`.

PLUGHDR

  render_plugin_section

  cat <<'MCPTHDR'

## MCP tools

Each tool's `mcp-tool.json` declares the transport (remote url, headers) and
the MCP tool surface (name, args, output fields) — that manifest is the catalog
source of truth. Each tool ships a ready-to-load config per harness plus a
pure-stdlib wrapper script, so it works with **no install** for any agent. Full
setup and the no-MCP fallback live in each tool's `README.md`.

MCPTHDR

  render_mcptool_section

  cat <<'FOOTER'

## Using a picked skill

Activate manually. For Claude Code, symlink (or copy) the skill folder into
your personal skills dir:

```bash
# Windows (Git Bash)
ln -s "$(pwd)/<path-from-catalog>/<skill-name>" "$HOME/.claude/skills/<skill-name>"
```

For the submodules, use the full path from the table, e.g.
`./skills/anthropic-skills/skills/pdf`, `./skills/mattpocock-skills/skills/engineering/tdd`, or `./skills/superpowers/skills/brainstorming`.

For other agents, follow their skill-discovery convention, or just open the
skill's `SKILL.md` and follow the steps directly — every skill is self-contained.

## Using a picked plugin

Install once (see `opencli-plugins/README.md`), then call as a CLI command:

```bash
opencli <plugin> <command> [args]        # e.g. opencli huawei-jiaxian search "盘古" --limit 3
```

## Using a picked MCP tool

No install. Two ways (see the tool's `README.md` for details):

```bash
# Any agent with Bash + Python 3 (no MCP support needed):
python3 mcp-tools/<tool>/<wrapper>.py "<query>"           # e.g. python3 mcp-tools/huawei-w3-search/w3_search.py "盘古"

# MCP-capable agent — load the bundled config:
#   Claude Code:   cp mcp-tools/<tool>/claude-code.mcp.json .mcp.json
#   opencode/cac:  codeagent --mcp-config mcp-tools/<tool>/opencode.mcp.json
```
FOOTER
} > "$OUT"

skills_count=$(grep -cE '^\| \[`' "$OUT" || true)
echo "Wrote $OUT (rows: $skills_count)"
