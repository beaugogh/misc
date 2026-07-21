# OpenCLI plugins

[OpenCLI](https://github.com/jackwener/OpenCLI) plugins — site-specific adapters
that turn a website into a deterministic `opencli` command an agent (or a human)
can call. Each subdirectory is a self-contained plugin, version-controlled here
and installed into `~/.opencli/plugins/` on demand.

These are **OpenCLI-coupled artifacts**, not harness-agnostic code. An adapter
imports OpenCLI's own API (`@jackwener/opencli/registry`, `Strategy`, the
browser `page` object) and only runs inside the OpenCLI runtime. Portability is
"any agent/harness with Bash, on a machine that has `opencli` set up" — the
same runtime dependency the [`chatgpt-web-imagegen`](../skills/chatgpt-web-imagegen)
skill already assumes. They live here, separately from `skills/`, because they
are a different *kind* of artifact: coupled code + a native `opencli` command,
versus portable instruction documents.

## Prerequisites — human, one-time (an agent cannot do these)

Each browser-based plugin drives your **logged-in Chrome** via the OpenCLI Browser Bridge, so a human must set these up before any agent can use the plugins:

1. **Node.js ≥ 20** — https://nodejs.org
2. **OpenCLI + the Browser Bridge extension** — `npm i -g @jackwener/opencli`, then add the **OpenCLI** extension to Chrome from the [Chrome Web Store](https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk) (or load it unpacked from the [GitHub Releases](https://github.com/jackwener/opencli/releases) zip). Keep Chrome running.
3. **Sign in to the target site** in Chrome (e.g. https://3ms.huawei.com/terminology) — adapters reuse this session's cookies.

`opencli doctor` must be green before any browser-based adapter will work; it verifies step 2. Step 3 is verified by the plugin's own smoke test.

## Install a plugin from this repo

The easiest path — each plugin ships a `setup.sh` that an agent can run directly. It verifies the prerequisites, installs the plugin, ensures the peer-dep symlink, and runs a smoke test, printing clear instructions if a human step is missing:

```bash
./<plugin>/setup.sh
```

Manual install (what `setup.sh` does under the hood):

```bash
# Local development install (symlinks the folder into ~/.opencli/plugins/):
opencli plugin install D:/workspace/misc/opencli-plugins/<plugin>

# Or, after pushing the repo, install from GitHub:
opencli plugin install github:<user>/misc/opencli-plugins/<plugin>
```

List / update / remove:

```bash
opencli plugin list
opencli plugin update <plugin>
opencli plugin uninstall <plugin>
```

## Use

Once installed, a plugin's commands are normal `opencli` commands:

```bash
opencli <plugin> <command> [args]
opencli <plugin> <command> --help
```

## Layout

```
opencli-plugins/
  <plugin>/                 # one OpenCLI plugin per folder
    opencli-plugin.json     # manifest: name, version, opencli range, description
    package.json            # ESM package; @jackwener/opencli as peerDependency
    <command>.ts (or .js)   # one or more commands via cli() from the registry
    README.md               # what it does, commands, install
```

## Adding a new plugin

1. Scaffold it with OpenCLI's own generator, targeting this directory:

   ```bash
   opencli plugin create <name> --dir opencli-plugins/<name>
   ```

   This writes `opencli-plugin.json`, `package.json`, sample commands, and a
   README in the correct shape.

2. Replace the sample commands with real adapters (see
   [Extending OpenCLI](https://github.com/jackwener/OpenCLI/blob/main/docs/guide/extending-opencli.md)).
   Prefer `browser: true` adapters that drive your logged-in Chrome for
   JS-rendered or login-gated sites; use `browser: false` only when the site
   exposes a clean public search endpoint.

3. Verify locally before committing:

   ```bash
   opencli plugin install file://$(pwd)/opencli-plugins/<name>
   opencli <name> <command> --help
   opencli browser verify <name>/<command>   # for browser adapters
   ```

4. Add a row to the table below.

## Plugins

| Plugin | Commands | Description |
|---|---|---|
| [`huawei-terminology`](./huawei-terminology) | `search` | Search the Huawei terminology database (3ms.huawei.com/terminology) — English/Chinese term, domain, confidence, definition. Requires a logged-in Huawei session via the Browser Bridge. |
