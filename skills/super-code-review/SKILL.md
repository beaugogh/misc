---
name: super-code-review
description: >
  Multi-axis final review of code and every delivery artifact — configuration,
  scripts, prompts, skills, workflows, specs, docs, schemas, and evaluations —
  as if you are the senior engineer and final approver. Spec & Intent, Standards & Craft, and
  Adversarial & Robustness reviewers inspect the change in isolated context;
  run them in parallel when the host supports it, otherwise sequentially. A
  synthesis pass dedups findings, assigns
  CRITICAL/MODERATE/NITPICK severity, and produces an APPROVED / APPROVED WITH
  CONCERNS / REJECTED verdict plus a corrected artifact. Use for the final gate
  before merge, handoff, or ship.
---

# Final Review

A rigorous multi-axis artifact review as if you are the senior engineer, staff
architect, and final approver responsible for shipping the work. Three
isolated reviewers examine orthogonal axes; a synthesis pass deduplicates,
assigns severity, and renders the verdict.

## Quick Start

1. **Read the complete artifact and relevant context** before forming an opinion; never review a diff in isolation when surrounding files are available.
2. **Identify artifact types** and select all applicable Core, code-specific, and prompt/skill/spec-specific dimensions.
3. **Pin the change and pre-flight.** Resolve the fixed point / file / diff and validate it is non-empty before dispatching reviewers.
4. **Resolve spec + standards sources** via the priority chains in § Process.
5. **Dispatch the 3 axes in isolated context.** Run them in parallel when the host supports independent reviewers; otherwise run them sequentially with the same axis-specific prompts. Then synthesize inline (§ Synthesis).

Invocation examples:
- `/super-code-review since main` — fixed-point git mode (three-dot merge-base diff vs `main`).
- `/super-code-review HEAD~5` — fixed point with explicit count.
- `/super-code-review <sha>` — fixed point at a commit.
- `/super-code-review <file>` — file mode.
- `/super-code-review <directory>` — directory-scoped git diff or directory listing.
- `/super-code-review <artifact>` — a standalone prompt, skill, workflow, spec, document, schema, or evaluation.
- `/super-code-review` (no args) — auto-detect: unstaged+staged `git diff HEAD` if dirty; ask if clean.
- Pasted diff — review inline, read surrounding code if in a repo.

## Scope

Review source code, configuration, scripts, diffs, prompts, `SKILL.md`,
`AGENTS.md`, `CLAUDE.md`, workflow and agent definitions, specifications,
documentation, tool schemas, and evaluations. Identify the artifact type before
dispatching reviewers; apply Core dimensions to every artifact and all matching
code- and prompt/skill/spec-specific dimensions. Do not mechanically apply an
irrelevant dimension.

## Mindset — falsify first

- Assume the change contains flaws even if it appears correct.
- Temporarily assume it was written by another engineer who may have introduced subtle defects.
- Do not defend the implementation. Do not assume design decisions were intentional.
- Treat every assumption as potentially incorrect until validated.
- Actively search for evidence that the solution is **wrong** before searching for evidence that it is **right**.
- Spend at least as much effort attempting to break the solution as was spent creating it.

This mindset is the charter for Axis 3 and the posture for synthesis; it colors all three axes.

Before reporting, mentally simulate realistic use, malformed and boundary inputs,
dependency and partial-failure paths, broken invariants, scale, and how another
engineer, user, or agent could misunderstand or misuse the artifact.

## The three axes

Three orthogonal axes use isolated reviewer contexts so they do not pollute one another. Each is defined by its source techniques and dimensions.

### Axis 1 — Spec & Intent

Sources: requirements alignment, the spec axis (scope-creep detection), and the Karpathy "Think Before Coding" + "Goal-Driven Execution" maxims. Dimensions: **Requirements Alignment** (does it satisfy stated requirements/acceptance criteria?), **Scope Creep** (behaviour not asked for), **Intent Fidelity** (implemented-but-wrong), **Instruction Fidelity**, **Agent Decision Boundaries**, **Specification Completeness**, and **Evaluation Readiness**.

### Axis 2 — Standards & Craft

Sources: code dimensions 6–11 (State & Data, Security, Performance, Architecture, Maintainability, Language best-practices), **Tool Usage Correctness**, the 12 Fowler smells (hard-violation vs judgement-call, repo-standards-override), and the Karpathy "Simplicity First" + "Surgical Changes" maxims. Repo-documented standards (`CODING_STANDARDS.md`, `CONTRIBUTING.md`) override the smell baseline.

### Axis 3 — Adversarial & Robustness

Sources: the falsify-first mindset applied to dimensions 1–4 and 6–8 plus **Prompt Robustness**: **Correctness & Logic**, **Hidden Assumptions**, **Edge Cases**, **Reliability & Failure Handling**, **Security**, **State & Data Integrity**, **Performance & Scalability**, and prompt-injection, instruction-hierarchy, context-sensitivity, and hallucination risks. Each finding gives a concrete counterexample or failure scenario as evidence.

> **Intentional overlap** — State/Data, Security, and Performance appear in *both* Axis 2 and Axis 3, by design. Axis 2 approaches them as **craft** (is it idiomatic/sanitized per standards?). Axis 3 approaches them as **robustness** (can it be broken? what's the failure scenario?). The consolidation rule in § Synthesis resolves the overlap: a finding spotted by both axes is filed once under the more relevant axis, with merged evidence.

## Severity definitions

- **CRITICAL** — will cause incorrect behavior, data loss, a security vulnerability, or deployment failure in production; fix before shipping.
- **MODERATE** — degrades quality, maintainability, or robustness and is likely to cause issues under edge conditions or future changes; fix before shipping.
- **NITPICK** — a style, naming, or minor clarity improvement; optional.

## Process

### 1. Pin the change and pre-flight validate

Resolve the fixed point / file / diff per the invocation mode (§ Invocation modes). For git modes: `git rev-parse <fixed-point>` must resolve and the diff must be non-empty. Fail here on a bad ref or empty diff.

Pin with SHAs (not branch names) so the review is reproducible even if the branch moves:
```
BASE_SHA=$(git rev-parse <fixed-point>)
HEAD_SHA=$(git rev-parse HEAD)
```

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`). If `gh` is available, fetch via `gh issue view <num>`; else note the ref and proceed with commit-message intent.
2. A path the user passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. For a standalone specification, policy, workflow, prompt, skill, schema, or evaluation, use the artifact itself as the primary source and note any missing external intent.
5. Ask the user. If they say there is no spec, **Axis 1 still runs** — it infers intent from the commit messages and states that explicitly. Commit-message intent is still reviewable.

### 3. Identify the standards sources

Anything in the repo that documents how artifacts should be written or operated: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, security policies, runbooks, or equivalent. Paste applicable material into the Axis 2 prompt. For code artifacts, also paste the **Fowler smell baseline** from `references/fowler-smells.md` in full (the reviewer has no other access to it). For non-code artifacts, set `{FOWLER_SMELLS}` to "Not applicable: this artifact contains no code."

### 4. Build context and dispatch the three axes

Build one self-contained prompt per axis. Give each reviewer only crafted, axis-specific context, never ambient session history. Dispatch independently in parallel when available; otherwise dispatch sequentially. Each prompt is built from the corresponding template under `references/`:

- Axis 1: `references/axis-1-spec-intent.md` — `{CHANGE_MATERIAL}` `{REVIEW_CONTEXT}` `{COMMIT_LIST}` `{SPEC_SOURCE}` `{MODE}`
- Axis 2: `references/axis-2-standards-craft.md` — `{CHANGE_MATERIAL}` `{REVIEW_CONTEXT}` `{COMMIT_LIST}` `{STANDARDS_FILES}` `{FOWLER_SMELLS}`
- Axis 3: `references/axis-3-adversarial-robustness.md` — `{CHANGE_MATERIAL}` `{REVIEW_CONTEXT}` `{COMMIT_LIST}`

`CHANGE_MATERIAL` is either a read-only inspection command, pasted diff, or pasted standalone artifact. `REVIEW_CONTEXT` contains affected files' relevant surrounding content and any repository instructions that govern them. For file, standalone-artifact, and non-git directory modes, it contains the full requested file(s).

For prompts, skills, specifications, workflows, schemas, and evaluations,
`REVIEW_CONTEXT` must also include their full text, all referenced tool schemas
or instructions, and concrete examples or acceptance criteria when available.

Every axis prompt carries the **read-only enforcement clause**: reviewers must not mutate files, the index, HEAD, branch state, Git configuration, or worktree metadata. Use `git show`, `git diff`, `git log`, and `git show <revision>:<path>` to inspect another revision; never use `git worktree add`.

Each axis **suggests** severity per finding; **synthesis owns the final severity** (so axes never rank each other — see § Synthesis).

### 5. Gather validation evidence, then synthesize inline

Before deciding approval, inspect documented validation and CI commands. Run the smallest relevant existing test, lint, type-check, build, or static-analysis command when it is safe and available. Do not install dependencies, alter configuration, or run a command expected to modify the checkout. Record the exact command and pass/fail/blocked outcome. If no safe command is available, say so; a test gap is not a passing result.

After reviewers return and validation evidence is gathered, perform synthesis inline (no fourth reviewer). Apply § Synthesis.

## Synthesis

The inline pass that turns three axis reports into one verdict.

### Dedup (consolidation rule)

Each axis returns findings tagged with root cause, location, and axis-of-origin. Group findings by **normalized root cause** — the same underlying defect, even if spotted by different axes with different framings. Example: Axis 2 flags "missing input validation per CONTRIBUTING.md §3"; Axis 3 flags "SQL injection exploitable via unsanitized `user_input`" — same root cause: unsanitized input.

Each group becomes **one consolidated finding**, filed under the **most relevant axis** (the axis whose brief the finding most directly matches — the SQL-injection case files under Axis 3, robustness; "function exceeds 200 lines" files under Axis 2, craft). The consolidated finding's **Evidence** field merges the union of evidence from all contributing axes, so no signal is lost.

> **This is not the same as merging/reranking axes.** The source two-axis skill forbids merging or reranking *axes* — that prohibition is preserved here: `AXIS SUMMARIES` (in the output) gives each axis its own independent summary line, and synthesis never declares one axis "more important" than another. What synthesis merges is *duplicate findings* (same root cause), which is the adversarial consolidation rule. Synthesis ranks **issues** by severity; it never ranks **axes**.

### Severity (final, owned by synthesis)

Each axis *suggested* a severity. Synthesis assigns the **final** severity:

- **Default:** take the **max** of suggested severities across the merged findings — two independent axes flagging the same root cause is a stronger signal.
- **Override (with stated reasoning):** synthesis may upgrade or downgrade based on cross-axis context. Upgrade example: Axis 2 calls a smell MODERATE (judgement call), but Axis 3 confirms the smell enables a real exploit → upgrade to CRITICAL. Downgrade example: Axis 3 says a security issue is CRITICAL, but Axis 1 reports the spec explicitly excludes that threat model → downgrade to MODERATE with reasoning.
- **Anti-inflation:** "Not everything is Critical." A judgement-call smell with no exploit path stays MODERATE or NITPICK; a hard-standards violation with no user impact is MODERATE, not CRITICAL. Acknowledge what was done well before listing issues — accurate praise helps the implementer trust the rest of the feedback.

### Verdict (mechanically derived)

Bright-line rule, no judgement:

- **REJECTED** if ≥1 CRITICAL finding exists.
- **APPROVED WITH CONCERNS** if 0 CRITICAL and ≥1 MODERATE.
- **APPROVED** if 0 CRITICAL and 0 MODERATE (only NITPICK, or none).

State the counts inline: `Verdict: REJECTED (2 CRITICAL, 3 MODERATE, 1 NITPICK).`

Validation can change confidence and must be reported, but a failing relevant validation command is itself a finding. Classify its severity from observed impact; do not approve while treating an unexplained failure as merely a gap.

### Corrected artifact (adaptive)

- **A diff with ≤ ~100 changed lines, or a standalone artifact with ≤ ~100 lines:** for a diff, output the complete corrected diff; for a standalone file or pasted artifact, output the complete corrected artifact. Preserve intended functionality. No placeholders, TODOs, or pseudocode.
- **Larger:** output only targeted fixes — per issue, the location and the corrected snippet. Do not regenerate the full file/diff. End with a summary of what changed.
- **No issues:** explicitly justify production-readiness across the three axes, then state that no corrected artifact is needed.

> **Surgical discipline (Karpathy) applies to the corrected artifact.** The corrected artifact touches only what the findings require. Do not "improve" adjacent code, do not refactor unbroken things, and do not remove pre-existing dead code (flag it, don't delete it). Remove only orphans the *findings'* fixes created. Every changed line in the corrected artifact must trace to a finding.

### YAGNI gate before elaboration

Before recommending "implement X properly," verify X is actually used — `grep` for usage. If unused, recommend **removal**, not elaboration. If used, then recommend proper implementation. Do not elaborate speculative features.

### Anti-patterns (bright-line "DO NOT")

- **No padding.** Do not invent issues to fill sections. If an axis returned no findings, `AXIS SUMMARIES` says so plainly.
- **No cross-axis reranking.** Do not declare Axis A's findings more important than Axis B's as a blanket. Synthesis ranks *issues* by severity, never *axes*. Each axis keeps its own summary line.
- **No silent drops.** When consolidating, keep the union of evidence. Never drop an axis's finding because another axis found something similar — merge them.

## Output Format

Structure the response exactly as follows.

### INTENT ALIGNMENT

- State the primary goal of the change in 1–3 sentences.
- State assumptions being made about intended behavior.
- State the **spec source used** (issue ref + fetched text / PRD path / commit-messages-only / none). If none, flag the gap.

### AXIS SUMMARIES

One line per axis — **do not merge or rerank these**:

- **Axis 1 — Spec & Intent:** N findings (C/M/N by suggested severity); worst: …; what's solid: …
- **Axis 2 — Standards & Craft:** …
- **Axis 3 — Adversarial & Robustness:** …

The "what's solid" note per axis enforces acknowledging strengths before issues.

### ANALYSIS SCRATCHPAD

- Record the adversarial reasoning that materially supports the findings: realistic usage simulation, edge and failure paths, invariant-breaking counterexamples, and likely human or agent misuse.
- Keep it concise and evidence-based; do not expose private reasoning unrelated to the review.

### REVIEW

Consolidated findings, each with:

- **Severity:** CRITICAL / MODERATE / NITPICK (final, from synthesis)
- **Axis:** the axis it was filed under (preserves axis attribution)
- **Location:** file, line, or hunk
- **Category:** the review dimension
- **Root Cause:** why the issue exists
- **Impact:** what goes wrong if unaddressed
- **Recommended Fix:** specific corrective action

Sorted CRITICAL → MODERATE → NITPICK. Consolidation rule: report each root cause once, under the most relevant axis. Do not invent issues — every issue must reference a specific code path or observable consequence. If an axis has no findings, say so plainly rather than padding.

### TEST / EVALUATION GAPS

- **Validation evidence:** command, outcome (passed / failed / not run), and reason. Include only commands actually attempted.
- List important scenarios not currently validated (failure paths, edge cases, adversarial cases, stress cases).

### ALTERNATIVE DESIGN ASSESSMENT

- **Simpler Alternative:** at least one.
- **More Robust Alternative:** at least one.
- **Why Current Design Was or Was Not Chosen:** explain the tradeoff.

### CONFIDENCE ASSESSMENT

- High / Medium / Low.
- Explain remaining uncertainty and what evidence would increase confidence. Lower confidence when no spec was available.

### APPROVAL DECISION

One of:

- **APPROVED** — no CRITICAL or MODERATE issues.
- **APPROVED WITH CONCERNS** — no CRITICAL, but MODERATE issues exist.
- **REJECTED** — CRITICAL issues exist; do not ship without fixes.

State the counts inline.

### CORRECTED ARTIFACT

Per § Synthesis → Corrected artifact (adaptive by changed lines for diffs or total lines for standalone artifacts). Surgical discipline applies — touch only what the findings require. If no issues, justify production-readiness across the three axes and state no corrected artifact is needed.

## Invocation modes

### A — Fixed-point git (`since main`, `HEAD~5`, `<sha>`, `<branch>`)

Pre-flight: `git rev-parse <fixed-point>` resolves; `git diff <fixed-point>...HEAD` non-empty. Pin: `BASE_SHA`/`HEAD_SHA`. Diff (three-dot, merge-base comparison): `git diff <BASE_SHA>...<HEAD_SHA>`. Commit list: `git log <BASE_SHA>..<HEAD_SHA> --oneline`. Three-dot is safer than two-dot for the diverged-branch case.

### B — File or standalone artifact (`/super-code-review <file>`)

Read the full file/artifact and relevant callers, callees, schemas, tool contracts, examples, and repository instructions. If tracked and modified, also capture `git diff HEAD -- <file>`. Put the full artifact and relevant context in `REVIEW_CONTEXT`; put the diff, raw pasted artifact, or a clear "full-file review; no diff" marker in `CHANGE_MATERIAL`. No BASE/HEAD pinning.

### C — Pasted diff or standalone artifact

For a pasted diff, if in a git repo, resolve its file paths and include relevant surrounding code in `REVIEW_CONTEXT`; otherwise review it as-is with a stated caveat. For a pasted standalone artifact, put its complete text in both `CHANGE_MATERIAL` and `REVIEW_CONTEXT`, and set `MODE` to `pasted-artifact`. Never present inline text as a command.

### D — Directory (`/super-code-review <dir>`)

If in git, require an explicit fixed point (or use the no-args dirty-tree mode) and use `git diff <fixed-point>...HEAD -- <dir>`; rest follows Mode A. If not in git, list the in-scope files, read each, and put their contents in `REVIEW_CONTEXT` before reviewing as a set.

### E — No args (`/super-code-review`)

If dirty (unstaged or staged): review `git diff HEAD` (unstaged + staged combined). BASE = HEAD. If clean: ask for a fixed point or file.

## Edge cases

- **Empty diff.** Fail at pre-flight: "No changes to review between <fixed-point> and HEAD." Do not dispatch reviewers.
- **No spec found.** Axis 1 runs anyway, infers from commit messages, and opens with "No spec available — reviewed against intent inferred from commit messages only." Note the gap in INTENT ALIGNMENT; lower CONFIDENCE. Axes 2 & 3 are unaffected.
- **Single-file vs multi-file.** No special handling; synthesis dedups across files. The corrected-artifact size rule keys off changed lines for diffs and total lines for standalone artifacts.
- **Very large diffs.** The per-axis word budget (≤400–500 words) caps each axis's output. If synthesis sees >15 consolidated findings: group by file, detail all CRITICAL findings, and summarize MODERATE/NITPICK as counts per file with a note "rerun on <subdir> for detail." The corrected artifact uses targeted fixes by the size rule. Optionally warn: "Large diff (X changed lines); consider reviewing in smaller fixed-point increments."
- **Clean axis (0 findings).** `AXIS SUMMARIES` says so plainly. No padding. If all three axes return 0 findings → APPROVED, and the corrected-artifact section justifies production-readiness across the three axes.
- **A reviewer suggests a fix that synthesis judges wrong (YAGNI).** Apply the YAGNI gate: if the fix elaborates an unused thing, replace the recommendation with "remove (YAGNI)" and note the grep that confirmed non-use.
- **Mixed artifacts.** Classify each hunk or file, apply every matching dimension, and synthesize cross-artifact findings. Do not exclude prompts, skills, specs, documentation, workflows, schemas, or evaluations.

## Boundaries

- This skill reviews; it does not implement, deploy, or merge. Its output is a recommendation the human or calling agent decides whether to act on.
- Reviewers are read-only on the checkout — they never mutate files, the index, HEAD, branch, Git configuration, or worktree metadata.
- Do not invent issues to fill sections. If a dimension has no findings, say so plainly.
- The corrected artifact is a proposal. Surface it for review; do not silently apply it to the original files.
