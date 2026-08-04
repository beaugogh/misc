---
name: super-code-review
description: >
  Multi-axis code review of source, config, scripts, or diffs as if you are the
  senior engineer and final approver. Three parallel sub-agents — Spec & Intent,
  Standards & Craft, Adversarial & Robustness — review the change in isolated
  context, then a synthesis pass dedups findings across axes, assigns
  CRITICAL/MODERATE/NITPICK severity, and produces an APPROVED / APPROVED WITH
  CONCERNS / REJECTED verdict plus a corrected artifact. Use for the final gate
  before merge or ship. For prompts, skills, specs, or agent definitions, use
  adversarial-review instead.
---

# Code Review

A rigorous multi-axis code review as if you are the senior engineer, staff
architect, and final approver responsible for deploying the change. Three
sub-agents review in isolated context along orthogonal axes; a synthesis pass
deduplicates, assigns severity, and renders the verdict.

## Quick Start

1. **Pin the change and pre-flight.** Resolve the fixed point / file / diff and validate it is non-empty *before* spawning sub-agents (a bad ref or empty diff must fail here, not inside three parallel sub-agents).
2. **Resolve spec + standards sources** via the priority chains in § Process.
3. **Dispatch 3 axes in parallel** (one message, three `general-purpose` Agent tool calls), then synthesize inline (§ Synthesis).

Invocation examples:
- `/super-code-review since main` — fixed-point git mode (three-dot merge-base diff vs `main`).
- `/super-code-review HEAD~5` — fixed point with explicit count.
- `/super-code-review <sha>` — fixed point at a commit.
- `/super-code-review <file>` — file mode.
- `/super-code-review <directory>` — directory-scoped git diff or directory listing.
- `/super-code-review` (no args) — auto-detect: unstaged+staged `git diff HEAD` if dirty; ask if clean.
- Pasted diff — review inline, read surrounding code if in a repo.

## Scope

Review **source code, configuration, scripts, and diffs.** Do **not** review prompts, `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, specs, agent definitions, or documentation — those belong to `adversarial-review`, which carries the prompt/skill/spec-specific dimensions (12–17) this skill deliberately omits. If a diff mixes code and non-code, review only the code hunks and tell the user to run `adversarial-review` on the non-code portions.

## Mindset — falsify first

- Assume the change contains flaws even if it appears correct.
- Temporarily assume it was written by another engineer who may have introduced subtle defects.
- Do not defend the implementation. Do not assume design decisions were intentional.
- Treat every assumption as potentially incorrect until validated.
- Actively search for evidence that the solution is **wrong** before searching for evidence that it is **right**.
- Spend at least as much effort attempting to break the solution as was spent creating it.

This mindset is the charter for Axis 3 and the posture for synthesis; it colors all three axes.

## The three axes

Three orthogonal axes run as parallel sub-agents so they don't pollute each other's context. Each is defined by its source techniques and dimensions.

### Axis 1 — Spec & Intent

Sources: requirements alignment, the spec axis (scope-creep detection), and the Karpathy "Think Before Coding" + "Goal-Driven Execution" maxims. Dimensions: **Requirements Alignment** (does it satisfy stated requirements/acceptance criteria?), **Scope Creep** (behaviour in the diff not asked for), **Intent Fidelity** (implemented-but-wrong).

### Axis 2 — Standards & Craft

Sources: code dimensions 6–11 (State & Data, Security, Performance, Architecture, Maintainability, Language best-practices), the 12 Fowler smells (hard-violation vs judgement-call, repo-standards-override), and the Karpathy "Simplicity First" + "Surgical Changes" maxims. Repo-documented standards (`CODING_STANDARDS.md`, `CONTRIBUTING.md`) override the smell baseline.

### Axis 3 — Adversarial & Robustness

Sources: the falsify-first mindset applied to dimensions 1–4 and 6–8: **Correctness & Logic**, **Hidden Assumptions**, **Edge Cases**, **Reliability & Failure Handling**, **Security**, **State & Data Integrity**, **Performance & Scalability**. Each finding gives a concrete counterexample or failure scenario as evidence.

> **Intentional overlap** — State/Data, Security, and Performance appear in *both* Axis 2 and Axis 3, by design. Axis 2 approaches them as **craft** (is it idiomatic/sanitized per standards?). Axis 3 approaches them as **robustness** (can it be broken? what's the failure scenario?). The consolidation rule in § Synthesis resolves the overlap: a finding spotted by both axes is filed once under the more relevant axis, with merged evidence.

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
4. Ask the user. If they say there is no spec, **Axis 1 still runs** — it infers intent from the commit messages and states that explicitly. (This is an enhancement over the source two-axis skill, which skipped the Spec sub-agent entirely; commit-message intent is still reviewable.)

### 3. Identify the standards sources

Anything in the repo that documents how code should be written: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, or equivalent. Paste these into the Axis 2 prompt. On top of whatever the repo documents, Axis 2 always carries the **Fowler smell baseline** from `references/fowler-smells.md` — paste it in full (the sub-agent has no other access to it).

### 4. Dispatch 3 axes in parallel

Send a single message with three `general-purpose` `Agent` tool calls. Each sub-agent gets only its axis's context (crafted context, never session history). Each axis's prompt is built by filling the placeholders in the corresponding template under `references/`:

- Axis 1: `references/axis-1-spec-intent.md` — placeholders `{DIFF_CMD}` `{COMMIT_LIST}` `{SPEC_SOURCE}` `{MODE}`
- Axis 2: `references/axis-2-standards-craft.md` — placeholders `{DIFF_CMD}` `{COMMIT_LIST}` `{STANDARDS_FILES}` `{FOWLER_SMELLS}`
- Axis 3: `references/axis-3-adversarial-robustness.md` — placeholders `{DIFF_CMD}` `{COMMIT_LIST}`

Every axis prompt carries the **read-only enforcement clause**: the sub-agent must not mutate the working tree, index, HEAD, or branch state; it uses `git show` / `git diff` / `git log` and, if it needs a working copy of another revision, `git worktree add /tmp/review-<SHA> <SHA>` — never moves HEAD.

Each axis **suggests** severity per finding; **synthesis owns the final severity** (so axes never rank each other — see § Synthesis).

### 5. Synthesize inline

After the three sub-agents return, perform synthesis inline (no fourth sub-agent). Apply § Synthesis.

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

### Corrected artifact (adaptive)

- **Total changed lines ≤ ~100:** output the complete corrected diff incorporating all fixes. Preserve intended functionality. No placeholders, TODOs, or pseudocode.
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

Per § Synthesis → Corrected artifact (adaptive by changed-line count). Surgical discipline applies — touch only what the findings require. If no issues, justify production-readiness across the three axes and state no corrected artifact is needed.

## Invocation modes

### A — Fixed-point git (`since main`, `HEAD~5`, `<sha>`, `<branch>`)

Pre-flight: `git rev-parse <fixed-point>` resolves; `git diff <fixed-point>...HEAD` non-empty. Pin: `BASE_SHA`/`HEAD_SHA`. Diff (three-dot, merge-base comparison): `git diff <BASE_SHA>...<HEAD_SHA>`. Commit list: `git log <BASE_SHA>..<HEAD_SHA> --oneline`. Three-dot is safer than two-dot for the diverged-branch case.

### B — File (`/super-code-review <file>`)

Read the file. If tracked+modified, also capture `git diff HEAD -- <file>` for change context. Read surrounding code for context — never review a diff in isolation. Sub-agents get the file path (they may Read it — Read is read-only) plus the working diff. No BASE/HEAD pinning.

### C — Pasted diff

If in a git repo, resolve the diff's file paths to read surrounding context. If not in a repo, review as-is with a stated caveat. Pass the diff as inline text in `{DIFF_CMD}`.

### D — Directory (`/super-code-review <dir>`)

If in git: `git diff <fixed-point>...HEAD -- <dir>` (scope to the dir); rest follows Mode A. If not in git: list files under the dir, Read each, review as a set.

### E — No args (`/super-code-review`)

If dirty (unstaged or staged): review `git diff HEAD` (unstaged + staged combined). BASE = HEAD. If clean: ask for a fixed point or file.

## Edge cases

- **Empty diff.** Fail at pre-flight: "No changes to review between <fixed-point> and HEAD." Do not spawn sub-agents.
- **No spec found.** Axis 1 runs anyway, infers from commit messages, and opens with "No spec available — reviewed against intent inferred from commit messages only." Note the gap in INTENT ALIGNMENT; lower CONFIDENCE. Axes 2 & 3 are unaffected.
- **Single-file vs multi-file.** No special handling; synthesis dedups across files. The corrected-artifact size rule keys off total changed lines, not file count.
- **Very large diffs.** The per-axis word budget (≤400–500 words) caps each axis's output. If synthesis sees >15 consolidated findings: group by file, detail all CRITICAL findings, and summarize MODERATE/NITPICK as counts per file with a note "rerun on <subdir> for detail." The corrected artifact uses targeted fixes by the size rule. Optionally warn: "Large diff (X changed lines); consider reviewing in smaller fixed-point increments."
- **Clean axis (0 findings).** `AXIS SUMMARIES` says so plainly. No padding. If all three axes return 0 findings → APPROVED, and the corrected-artifact section justifies production-readiness across the three axes.
- **Sub-agent suggests a fix that synthesis judges wrong (YAGNI).** Apply the YAGNI gate: if the fix elaborates an unused thing, replace the recommendation with "remove (YAGNI)" and note the grep that confirmed non-use.
- **Non-code in diff.** Review only code/config/script hunks; tell the user to run `adversarial-review` on the prompt/skill/spec portions; note which hunks were excluded and why.

## Boundaries

- This skill reviews; it does not implement, deploy, or merge. Its output is a recommendation the human or calling agent decides whether to act on.
- Sub-agents are read-only on the checkout — they never mutate the working tree, index, HEAD, or branch.
- Do not invent issues to fill sections. If a dimension has no findings, say so plainly.
- The corrected artifact is a proposal. Surface it for review; do not silently apply it to the original files.
