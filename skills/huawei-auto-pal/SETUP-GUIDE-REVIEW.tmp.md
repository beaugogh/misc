# Temporary review: huawei-auto-pal setup-guide revision

## Review target

- Commit: `ea2520812ec9abfb5cd95b01fd403bd1d94a1bf2`
- Subject: `docs: bilingual setup guide and first-run onboarding`
- Reviewed against current `main` at `6402a21ac`.
- Scope reviewed:
  - `.env.example`
  - `README.md`
  - `SKILL.md`
  - `retro-scope/scripts/run.py`
  - `skill-forge/SKILL.md`

## Overall assessment

The revision is directionally good and materially improves onboarding. The bilingual
guide, separation of core and optional capabilities, credential-safety reminders, and
non-blocking first-run flow are useful. The revision is not fully ready as written,
however, because several onboarding claims do not match the actual runtime capability
or the steps required to activate an integration.

Recommended decision: **approve with changes**.

The intentional rename from `huawei-auto-buddy` to `huawei-auto-pal` should remain.
The problems below concern state migration and setup accuracy, not the new name.

## Findings

### 1. High: first-run detection can misclassify an existing user

Current instruction:

```text
SKILL.md:63
When a user invokes huawei-auto-pal for the first time (no `output/` directory yet) ...
```

Absence of `huawei-auto-pal/output/` does not necessarily mean first use. After the
intentional directory rename, existing ignored state can remain at:

```text
skills/huawei-auto-buddy/output/
```

Git cannot rename ignored or untracked files. Without migration handling, an existing
user may appear new while their previous state remains under the old directory. The
abandoned state can include:

- `retro_scope_last_run.txt`;
- `skill_forge_last_run_ms.txt`;
- `tasks.jsonl` and reports;
- session evidence;
- `personal-context/SKILL.md`;
- `skill_forge_policy.json`; and
- rollback snapshots.

This can reset incremental processing, hide previously approved context or policy, and
leave sensitive local data outside the new directory's ignore rule.

#### Required revision

Before declaring a first run:

1. Check the new output path.
2. Check the former `skills/huawei-auto-buddy/output/` path.
3. If only the old path exists, explain the exact source and destination and ask for
   approval to migrate it.
4. If both paths exist, do not merge automatically. Report the conflict and inventory
   filenames without reading or printing sensitive contents.
5. Preserve permissions, watermark units, policy files, backups, and timestamps.
6. Keep a repository-level compatibility ignore for
   `skills/huawei-auto-buddy/output/` until old installations have had a reasonable
   migration window.
7. Verify the destination is ignored and `git status --untracked-files=all` does not
   expose personal output.

Do not silently delete the old directory or overwrite an existing new output directory.

#### Required tests

- neither path exists: run normal first-run guidance;
- only old output exists: report migration, do not silently initialize new state;
- only new output exists: treat as an existing installation;
- both paths exist: report a conflict and perform no merge;
- legacy output remains protected from Git staging.

### 2. Medium: `--check` conflates detection with usable collection

The new `--check` branch prints every successful `detect()` result as `OK`:

```text
retro-scope/scripts/run.py:679-698
```

Some registered adapters are explicitly detector-only and cannot currently emit an
event:

- `3ms` — `more_adapters.py:722-746`;
- `clouddevops_wiki` — `unverified_adapters.py:390-438`; and
- `w3` — `unverified_adapters.py:445+`.

For example, `3ms` can print `OK` merely because `opencli` exists, while its `collect()`
method immediately returns without yielding data. This makes an environment check look
more capable than the pipeline actually is.

The heading also says “Green sources work with zero setup,” but the implementation adds
no colors and prints only `OK` or `not detected`.

#### Required revision

Model capability separately from presence. Suggested statuses:

- `READY`: detected and collection is implemented;
- `DETECTOR-ONLY`: integration detected, but no usable collector is shipped;
- `NOT DETECTED`: collection exists but its dependency/source is absent;
- `ERROR`: detection failed;
- optionally `AUTH REQUIRED`: executable exists but authentication is unavailable.

Avoid claiming that detector-only sources contribute coverage. State explicitly that
they currently yield no events.

Prefer structured adapter metadata over a detached `_ADAPTER_HINTS` dictionary, for
example `capability_status`, `missing_impact`, and `setup_reference`. If that is too broad
for this revision, add a small explicit detector-only set and test it.

Correct inaccurate hints as part of this change:

- CloudDevOps Wiki detection checks for an OpenCLI command, not credentials.
- Its current collector yields nothing, so obtaining a credential does not enable
  retro-scope collection.
- W3 similarly checks OpenCLI and remains detector-only.
- WeLink recordings can use the conventional Windows location; the environment variable
  is an override, not always a requirement.

#### Required tests

Add CLI tests that mock adapter detection and assert output for:

- ready adapter;
- absent adapter with hint;
- detector-only adapter;
- detection exception; and
- an unknown adapter without hint metadata.

Also assert that `--check` exits without collecting personal activity.

### 3. Medium: CodeHub setup stops before the integration is usable

The setup guide tells users to install `uvx` and create a `CODEHUB_TOKEN`, while the
skill-forge dependency table uses only `CODEHUB_TOKEN in .env` as its read-only check.
Neither condition proves the CodeHub tool is callable.

The authoritative `mcp-tools/huawei-codehub/README.md` documents three actual execution
paths:

1. call the bundled Python wrapper directly;
2. load the Claude Code MCP configuration; or
3. load the opencode/codeagent MCP configuration.

It also documents an effective readiness check:

```bash
python3 mcp-tools/huawei-codehub/codehub.py --list-tools
```

After following only the auto-pal guide, a new user can have both uvx and a token but no
MCP configuration or verified wrapper path. The onboarding sequence therefore ends
before the promised MR/review/issue capability is established.

#### Required revision

Add a concise “choose one integration path” step:

- portable wrapper path; or
- harness-specific MCP configuration path.

Link directly to the relevant headings in the CodeHub MCP documentation instead of only
mentioning `CODEHUB_UVX_ARGS`. Use a readiness check that verifies all of:

- `uvx` exists;
- credentials exist without printing their value;
- the wrapper/server starts; and
- tools can be enumerated.

Update `skill-forge/SKILL.md` so the CodeHub dependency check verifies tool availability,
not merely the presence of an environment variable. Never place a real token directly
into a tracked MCP configuration.

### 4. Medium: GitHub credential onboarding contradicts the operational policy

The parent first-run guide directs users to a GitHub-token walkthrough. The README then
states:

```text
README.md:197-200
The current GitHub wrapper uses ssl.CERT_NONE and is skipped by this skill until it is
independently fixed.
```

The skill-forge table nevertheless presents `GITHUB_TOKEN in .env` as the dependency
check. This encourages users to create and store a sensitive credential for an
integration that the skill declares unusable.

#### Required revision

Choose one coherent state:

1. **Disabled state:** Remove GitHub token creation from first-run onboarding, label the
   integration unavailable, retain only a short explanation, and do not ask for a token.
2. **Supported state:** Independently fix and validate TLS handling, document an approved
   proxy override rather than assuming one proxy endpoint, verify the actual tool path,
   and only then offer token setup.

Until the second state is complete, the first is safer and clearer.

Also avoid treating a token as proof that an MCP tool is installed, configured, or
reachable.

### 5. Low: the new onboarding behavior has no targeted tests

The commit states that 572 tests pass, and the full current suite does pass. However,
the commit adds no test for `_ADAPTER_HINTS`, the new `--check` output, first-run
classification, or setup-path integrity. Existing passing tests therefore do not
validate most of the new behavior.

Add focused tests for the cases specified above. Documentation references should also
be checked for existence, including images and relative MCP links.

### 6. Low: setup details are duplicated and can drift

Detailed setup knowledge now appears across:

- `huawei-auto-pal/README.md`;
- `.env.example`;
- `huawei-auto-pal/SKILL.md`;
- `skill-forge/SKILL.md`;
- `_ADAPTER_HINTS` in `run.py`; and
- the MCP tools' own README files.

Several inconsistencies already demonstrate the drift risk. Keep auto-pal's main skill
focused on routing and authority. Treat the MCP tool documentation as authoritative for
installation and harness configuration, and keep only capability impact plus direct
links in auto-pal.

If reorganizing, prefer a clearly named `references/setup.md` over expanding the core
skill body. Do not duplicate exact proxy/TLS/configuration mechanics unless auto-pal has
a test that verifies them against the underlying tool contract.

## Strengths to preserve

Do not discard the useful parts of the revision while fixing the findings:

- English/Chinese onboarding is approachable for the intended audience.
- Required and optional capabilities are separated clearly.
- The guide repeatedly says optional tools must not block the pipeline.
- Installation and authentication remain explicitly user-approved actions.
- `.env` instructions warn that `.gitignore` does not untrack committed files.
- Token values are not printed or embedded in skill instructions.
- The guide explains what each optional dependency is intended to add.
- `--check` isolates detection exceptions and remains read-only.
- Relative image and local-document references currently resolve.

## Validation already performed

The following checks passed on current `main`:

- `git diff ea2520812^ ea2520812 --check`
- portable validation of `huawei-auto-pal`;
- portable validation of `retro-scope`;
- portable validation of `skill-forge` (with the expected warning that its link to the
  parent README escapes the component directory);
- JSON validation of `skill-forge/evals/feedback-sedimentation.json`;
- Python 3.9 grammar parsing of all retro-scope Python files;
- `python retro-scope/scripts/run.py --check`;
- 572 unit tests passed, 5 skipped.

The passing suite does not invalidate the findings because it contains no targeted test
for the newly added environment-check presentation or the rename/first-run migration
case.

## Acceptance criteria

The follow-up revision is ready when all of the following are true:

1. Existing legacy output cannot become visible to Git and is not silently abandoned.
2. First-run logic distinguishes a new installation from a renamed existing one.
3. `--check` distinguishes usable collection from detector-only presence.
4. Every displayed setup hint matches the adapter's actual detection and collection
   contract.
5. Following the CodeHub guide ends with a verified callable tool path.
6. GitHub credential setup is not offered while the integration is intentionally
   disabled.
7. Dependency checks verify capability, not just credential presence.
8. New CLI and migration tests cover success, absence, detector-only, error, and conflict
   cases.
9. All existing 572 tests continue to pass, aside from any intentional count increase.
10. Skill validation, JSON validation, link checks, and `git diff --check` pass.

## Requested scope discipline

- Keep the intentional `huawei-auto-pal` name.
- Do not redesign retro-scope's analysis model as part of this fix.
- Do not weaken the existing user-approval boundaries.
- Do not install tools, create credentials, authenticate, or change global proxy/TLS
  configuration during validation.
- Do not read or print personal output contents when testing legacy migration.
- Keep fixes small enough to review independently: migration safety, capability-status
  accuracy, integration completion, then documentation deduplication.
