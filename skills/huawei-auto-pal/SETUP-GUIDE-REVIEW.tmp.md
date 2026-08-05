# Temporary follow-up review: huawei-auto-pal setup and memory architecture

## Review target

- Original setup commit: `ea2520812ec9abfb5cd95b01fd403bd1d94a1bf2`
- First review commit: `bcfe8d5d8`
- Follow-up implementation: `1ebc1d017e4065748fddeec51b435a3138635a8d`
- Merge reviewed on `main`: `943c633cd`
- Review date: 2026-08-05

This file replaces the temporary review deleted by the follow-up merge. It records what
the follow-up fixed, what remains open, and an additional review of skill-forge's
memory-as-skill architecture.

## Current decision

The follow-up is a substantial improvement, but it is **not complete**. Keep the changes
that correctly distinguish detector-only adapters, protect the legacy output path, and
disable the unsafe GitHub integration. Revise `--check` before treating it as a safe
first-run command: it currently reads Claude session records before reaching its early
return. Legacy state migration and CodeHub readiness also remain unfinished.

Recommended decision: **approve with another targeted revision**.

## Disposition of the original findings

| Original finding | Status | Follow-up assessment |
|---|---|---|
| Legacy output / first-run migration | Partially fixed | Root ignore now prevents accidental commits, but no detection or migration workflow exists. |
| `--check` conflates detection and collection | Partially fixed | Status vocabulary is better, but `--check` still performs real Claude collection before the status branch. |
| CodeHub setup stops before usable integration | Open | The guide still verifies only uvx/token prerequisites, not a callable wrapper or MCP tool. |
| GitHub onboarding contradicts disabled policy | Resolved | GitHub is consistently disabled and token creation is no longer requested. |
| No targeted tests | Partially fixed | Twelve tests were added, but they depend on the real user environment and fail to assert the key no-collection property. |
| Setup details duplicated across files | Open | The revision did not consolidate ownership of setup facts. |

## Follow-up findings

### 1. High: `--check` collects personal Claude session data

The current control flow is:

```text
run.py:657    parse arguments
run.py:659    begin two-pass collection setup
run.py:664    construct ClaudeCodeAdapter
run.py:666    detect Claude records
run.py:667    call list(ai_adapter.collect())
run.py:679    finally enter the --check branch
```

Therefore `python retro-scope/scripts/run.py --check` is not merely an environment check.
When Claude records exist, it parses real session events before printing adapter status.

A direct instrumented check produced:

```text
ClaudeCodeAdapter.collect calls before --check: 1
```

This conflicts with:

- the first-run guide's presentation of `--check` as a setup-only command;
- retro-scope's consent and data-minimization boundaries; and
- the unit-test contract requiring temporary stores and mocks rather than installed
  applications, accounts, or personal files.

#### Required revision

Move true early-return modes before two-pass AI collection. At minimum, `--check` and
`--eval` must not enumerate session records. Build a detection-only registry for
`--check`, or separate registry construction from project-root discovery.

Add an explicit regression test:

```python
with patch.object(ClaudeCodeAdapter, "collect") as collect:
    run_main("--check")
    collect.assert_not_called()
```

Also consider whether `--sources` is intended to collect or only report detection. Its
current name suggests detection; make the contract explicit and test it.

### 2. Medium: the new tests inspect the developer's real environment

`test_check_output.py` repeatedly invokes the complete `run.main()` path with the real
registry. Because of finding 1, those invocations read local Claude sessions. Even after
the control-flow fix, real `detect()` methods scan installed applications and personal
directories.

The full suite now took approximately 52.6 seconds in this checkout, compared with about
5.3 seconds before these tests. The slowdown is consistent with repeated environment
inspection.

`test_not_detected_shows_hint` also assumes iCalendar is absent “on most CI machines.”
That is not deterministic: an `.ics` file in an auto-discovered directory or a configured
`RETRO_SCOPE_ICS_PATHS` makes the assertion fail.

#### Required revision

Extract status rendering into a function that accepts an adapter registry or a list of
adapter capability records. Test it with fake adapters representing:

- detected and ready;
- detected but detector-only;
- absent with a hint;
- absent without a hint;
- detection exception; and
- authentication required, if that state is introduced.

Keep one CLI wiring test, but mock registry construction and assert that no adapter
`collect()` method runs.

### 3. Medium: legacy output is protected but still abandoned

The new repository-level rule:

```text
skills/huawei-auto-buddy/output/
```

correctly prevents old private output from appearing in Git. Preserve this rule.

However, `SKILL.md` still defines first use solely as the absence of the new `output/`
directory. It does not check the former directory or offer migration. Other existing
users can therefore lose continuity for:

- retro-scope and skill-forge watermarks;
- tasks and reports;
- session evidence;
- `personal-context/SKILL.md`;
- skill-forge policy; and
- rollback snapshots.

#### Required revision

Before declaring a first run:

1. inspect existence only at both exact output paths;
2. if only the old path exists, explain source and destination and request approval to
   migrate it;
3. if both exist, report a conflict and do not merge or overwrite automatically;
4. preserve permissions, timestamps, watermark units, policies, and backups;
5. never print personal contents during the inventory; and
6. verify the final location is ignored and absent from `git status --untracked-files=all`.

Tests must cover neither path, old only, new only, both paths, and destination conflict.

### 4. Medium: CodeHub readiness remains token-only

The setup guide installs `uvx` and explains `CODEHUB_TOKEN`, while the skill-forge table
still uses `CODEHUB_TOKEN in .env` as its read-only check. A token does not establish that
the wrapper or MCP integration is installed, configured, reachable, authenticated, or
capable of listing tools.

The authoritative CodeHub documentation already provides three execution paths:

1. bundled Python wrapper;
2. Claude Code MCP configuration; or
3. opencode/codeagent MCP configuration.

#### Required revision

Add a concise “choose one integration path” step and keep the detailed mechanics in the
CodeHub tool documentation. For the portable wrapper path, validate with:

```bash
python3 mcp-tools/huawei-codehub/codehub.py --list-tools
```

Check credentials without printing them. Update skill-forge's dependency contract to
require a callable tool surface, not merely an environment variable. Never put a real
token into a tracked MCP configuration.

### 5. Low: setup knowledge still has multiple sources of truth

Setup facts remain duplicated across the parent README, `.env.example`, parent
`SKILL.md`, skill-forge, `_ADAPTER_HINTS`, and MCP-tool documentation. The previous drift
around GitHub, Wiki, W3, and WeLink demonstrates the cost.

Keep auto-pal focused on capability impact, authority, and direct navigation. Treat each
underlying tool's documentation as authoritative for installation and platform-specific
configuration. Prefer a clearly named reference file for auto-pal-specific onboarding
details rather than duplicating exact commands across several skill files.

## Improvements that should be preserved

- The root compatibility ignore protects legacy private output from accidental staging.
- `READY`, `DETECTOR-ONLY`, `NOT DETECTED`, and `ERROR` are clearer than the former flat
  `OK` status.
- 3ms, CloudDevOps Wiki, and W3 are correctly marked detector-only.
- Wiki/W3 hints now describe OpenCLI rather than claiming credentials or MCP enable them.
- The WeLink recordings hint correctly describes the environment variable as an override.
- GitHub is consistently disabled in the parent guide, `.env.example`, and skill-forge.
- The guide no longer encourages creation of an unusable GitHub credential.
- Detection exceptions remain isolated so one adapter does not stop the status report.

## Additional architecture review: memories represented as skills

### Is that the current design?

Yes, with an important qualification.

Skill-forge distinguishes the concepts semantically:

- a **memory proposal** is a stable preference, environment fact, project fact, or
  decision useful across sessions; and
- a **skill proposal** is a reusable behavior or workflow with triggers and procedure.

But the durable personal-memory container is explicitly:

```text
output/personal-context/SKILL.md
```

So memories are currently persisted through a skill-shaped artifact. The existing local
personal-context artifact passes structural skill validation. It is a **memory-backed
skill**, not proof that a memory and a procedural skill are the same semantic object.

### What is good about the pattern

Using a skill-shaped container can be effective because it provides:

- a portable Markdown representation;
- a standard frontmatter and validation path;
- an explicit place to describe when context should be loaded;
- compatibility with agents that already understand skills;
- human-readable review and diffs;
- local, ignored storage; and
- one governed write path with approval, backup, and rollback.

For a small set of stable preferences and behavioral rules, this is pragmatic. It avoids
building a database or vendor-specific memory API and fits the project's platform-
agnostic goals.

### Where the abstraction becomes dangerous

Skills and memories have different semantics:

| Dimension | Skill | Memory |
|---|---|---|
| Purpose | Tell an agent how to act | Preserve a fact, preference, or decision |
| Activation | Triggered by a task/context | Retrieved by relevance, scope, and recency |
| Content | Procedure, constraints, examples | Declarative state plus provenance |
| Evaluation | Does the workflow produce the right behavior? | Is the item true, current, authorized, and relevant? |
| Lifecycle | Versioned capability | Can expire, be superseded, corrected, or forgotten |
| Authority | May instruct actions | Must not gain authority merely by being remembered |

If raw facts are written directly as skill instructions, several failures become likely:

- a remembered observation can accidentally become an imperative;
- stale facts have no expiry or supersession mechanism;
- broad skill triggering can inject irrelevant private context;
- a narrowly triggered skill may never retrieve a relevant memory;
- provenance and confidence can be lost during paraphrase;
- memory edits can be mistaken for authorization to act; and
- all memories compete for the same context budget.

### Current retrieval weakness

Persisting a `SKILL.md` file does not guarantee that an agent will discover or load it.
The personal-context artifact lives beneath ignored `output/`, not in a conventional
installed-skills root. The parent skill does not currently define a deterministic
retrieval step for applicable personal context during every relevant workflow.

The local artifact also produced this validator warning:

```text
warning: description may not explain when the skill should be selected
```

That warning matters architecturally: a memory container without a precise loading
contract is durable storage without dependable recall.

The current file mode was observed as `0644` (`-rw-r--r--`) even though generated output
is described as sensitive and the design calls for restrictive permissions. The memory
container should normally be `0600`, with its containing private directories restricted
where the platform supports it.

### Recommended pattern: skill as router, memories as typed data

Keep the useful portability of the skill interface, but separate the control plane from
the data plane:

```text
output/personal-context/
├── SKILL.md                 # retrieval policy, safety rules, and usage contract
└── references/
    ├── preferences.md       # stable user preferences and interaction style
    ├── environment.md       # confirmed environment facts with review dates
    ├── projects.md          # project-scoped facts and decisions
    └── decisions.md         # durable decisions and supersession history
```

For more deterministic lifecycle handling, the references may instead be JSONL records
with fields such as:

```text
id, type, scope, statement, provenance, confirmed_at,
review_after, sensitivity, status, supersedes
```

The `SKILL.md` should contain only:

- when to load personal context;
- which scopes to select;
- privacy and non-disclosure rules;
- the rule that memory is evidence/context, not autonomous authority;
- conflict, expiry, and supersession handling; and
- instructions to load only the smallest relevant reference section.

This preserves platform-agnostic skill compatibility without pretending every memory is
a procedural skill.

### Classification rule for skill-forge

Use this boundary:

- Persist **“When situation X occurs, perform procedure Y under constraints Z”** as a
  skill or behavioral rule.
- Persist **“The user/project/environment has confirmed property P within scope S”** as
  a memory record.
- If a preference directly governs behavior, store the declarative preference as memory
  and, only when useful, derive a separately reviewable behavioral rule. Link the two by
  provenance rather than silently converting one into the other.

New skills and structural memory-container changes remain explicitly approved Tier 3
writes. Automatic behavioral-rule sedimentation must not auto-apply personal facts,
identity, project state, or environment observations.

### Recommended memory acceptance tests

Add evaluations for:

1. relevant preference is retrieved for a matching task;
2. unrelated memory is not loaded;
3. project-scoped memory does not leak into another project;
4. expired or superseded memory is not treated as current;
5. conflicting memories produce clarification rather than arbitrary selection;
6. trace-derived text cannot turn a memory into an instruction;
7. deletion/revocation removes future retrieval;
8. memory provenance is preserved without exposing raw sensitive evidence;
9. structural validator and trigger tests cover the personal-context router; and
10. file and directory permissions remain restrictive after creation and update.

## Validation performed on the follow-up

- Pulled and reviewed current `main` at `943c633cd`.
- Directly proved that `ClaudeCodeAdapter.collect()` is called once by `--check`.
- Ran the complete test suite: 584 passed, 5 skipped.
- Validated the parent, retro-scope, and skill-forge metadata.
- Validated the evaluation JSON.
- Ran `git diff --check` over the follow-up change.
- Structurally validated the local personal-context memory artifact without printing its
  contents; it is valid but has an imprecise selection description.
- Confirmed the memory artifact remains ignored by Git.
- Confirmed current `main` was otherwise clean before recreating this temporary review.

## Acceptance criteria for the next revision

1. `--check` calls no adapter `collect()` method.
2. `--check` tests use fake adapters and no personal or installed-application state.
3. Tests are deterministic regardless of local `.ics` files, credentials, or tools.
4. Legacy output is both ignored and handled through a safe migration decision.
5. CodeHub readiness verifies a callable wrapper or MCP tool surface.
6. GitHub remains disabled until a separately validated TLS-safe path exists.
7. Setup details have clear authoritative ownership and do not drift across files.
8. Personal context has a deterministic, relevance-bounded retrieval contract.
9. Memory facts remain declarative data and never acquire action authority by storage.
10. Memory records support provenance, scope, correction, expiry/review, and deletion.
11. Sensitive personal-context files use restrictive permissions where supported.
12. All skill, JSON, CLI, migration, retrieval, permission, and existing regression tests
    pass.

## Scope discipline

- Keep the intentional `huawei-auto-pal` name.
- Preserve the detector-only status improvement and GitHub-disabled policy.
- Do not redesign retro-scope's analysis model while fixing setup checks.
- Do not install tools, authenticate, create credentials, or change global proxy/TLS
  configuration during validation.
- Do not print personal memory or output contents in tests or reports.
- Do not merge conflicting legacy and current output automatically.
- Do not make the memory representation dependent on one commercial agent platform.
