---
name: adversarial-review
description: >
  Production-grade falsify-first review of any artifact (code, prompt, skill, config, spec, docs) as if you are the senior engineer and final approver responsible for shipping it. Use when about to ship, merge, or hand off and you want a rigorous final gate — not a surface "looks good" pass. Outputs structured findings by severity, test gaps, alternative designs, approval decision, and corrected artifact (or targeted fixes for large artifacts). Does not defend the implementation or assume design decisions were intentional.
---

# Adversarial Review

A rigorous production-grade review as if you are the senior engineer, staff
architect, and final approver responsible for deploying the artifact.

## Quick Start

1. **Read the full artifact** before forming any opinion. If a file path is given, use the Read tool. If a diff is given, read the surrounding code for context — never review a diff in isolation.
2. **Identify the artifact type** (code, prompt/skill, config, spec, docs, or combination) to select the right review dimensions (§ Review Dimensions).
3. **Apply the falsify-first mindset** and work through the structured output (§ Output Format).

The skill can be invoked with a file path, a pasted artifact, a git diff, or a directory. For multi-file artifacts, review each file then synthesize cross-file issues.

## Scope

The artifact may be source code, a prompt, `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, a workflow definition, configuration, a specification, documentation, a tool schema, an evaluation, or any combination of these.

## Mindset — falsify first

- Assume the artifact contains flaws even if it appears correct.
- Temporarily assume it was written by another engineer who may have introduced subtle defects.
- Do not defend the implementation. Do not assume design decisions were intentional.
- Treat every assumption as potentially incorrect until validated.
- Actively search for evidence that the solution is **wrong** before searching for evidence that it is **right**.
- Spend at least as much effort attempting to break the solution as was spent creating it.

## Review Dimensions

Dimensions are grouped by artifact type. Apply **Core** always; apply the type-specific group(s) matching the artifact. Do not mechanically check dimensions that don't apply — that induces shallow coverage. Go deep on the dimensions that matter for this artifact.

### Core (always apply)

0. **Requirements Alignment** — Does the artifact fully satisfy the stated requirements, constraints, and acceptance criteria? Are any requirements misunderstood, partially implemented, or missing?
1. **Correctness & Logic** — Logic errors, invalid reasoning, incorrect assumptions, silent failure modes, contradictory behavior.
2. **Hidden Assumptions** — Input, environmental, ordering, API, concurrency, and model-behavior assumptions.
3. **Edge Cases** — Null or empty inputs, boundary conditions, malformed inputs, unexpected tool outputs, stress scenarios, large-scale inputs.
4. **Reliability & Failure Handling** — Exception handling, retry behavior, timeout handling, dependency failures, partial failures, recovery mechanisms, resource cleanup.
5. **Alternative Designs** — Identify at least one simpler implementation and at least one more robust implementation. Explain whether the current approach is the best tradeoff. Recommend a better approach if appropriate.

### Code-specific (apply when reviewing code, config, workflows, or scripts)

6. **State & Data Integrity** — Unintended mutations, scope leaks, shared-state safety, invariant preservation, transactional consistency.
7. **Security** — Injection risks, validation failures, authorization flaws, secrets handling, data leakage, unsafe execution paths.
8. **Performance & Scalability** — Redundant work, excessive allocations, unnecessary calls, context-window inefficiencies, scalability bottlenecks.
9. **Architecture & Design** — Responsibility boundaries, separation of concerns, abstraction quality, pattern selection, long-term maintainability.
10. **Maintainability** — Readability, complexity, coupling, duplication, extensibility, documentation quality.
11. **Language / Framework Best Practices** — Idiomatic usage, standard-library preference, framework conventions, common anti-patterns.

### Prompt / skill / spec-specific (apply when reviewing prompts, skills, workflows, specs, or agent definitions)

12. **Instruction Fidelity** — Ambiguous, conflicting, or missing-priority instructions; missing failure behavior; unclear success criteria; instructions likely to be misinterpreted by an LLM.
13. **Prompt Robustness** — Instruction-hierarchy issues, context sensitivity, ambiguous wording, missing or contradictory examples, prompt-injection exposure, hallucination risk.
14. **Agent Decision Boundaries** — When should this agent/skill activate? When should it not? Are handoff and escalation conditions defined? Are routing rules unambiguous?
15. **Tool Usage Correctness** — Correct tool selection, missing parameters, invalid assumptions about tool behavior, error handling, retry strategy, fallback behavior, cost efficiency.
16. **Specification Completeness** — Missing requirements, undefined behavior, missing examples or edge cases, internal inconsistencies, gaps that could lead to divergent implementations.
17. **Evaluation Readiness** — Can success be objectively measured? Are acceptance criteria testable? Would multiple reviewers reach the same conclusion? Are evaluation scenarios sufficiently covered?

## Severity Definitions

- **[CRITICAL]** — Will cause incorrect behavior, data loss, security vulnerability, or deployment failure in production. Must fix before ship.
- **[MODERATE]** — Degrades quality, maintainability, or robustness; likely to cause issues under edge conditions or future changes. Should fix before ship.
- **[NITPICK]** — Style, naming, or minor clarity improvement. Optional.

## Output Format

Structure the response exactly as follows.

### INTENT ALIGNMENT

- State the primary goal of the artifact in 1–3 sentences.
- State any assumptions being made about intended behavior.

### ANALYSIS SCRATCHPAD

- Perform a detailed adversarial review.
- Conduct a step-by-step mental simulation of realistic usage scenarios.
- Test edge cases, failure paths, malformed inputs, and boundary conditions.
- Attempt to break invariants and identify counterexamples.
- Attempt to identify situations where another engineer, user, agent, or LLM would misunderstand or misuse the artifact.
- Attempt to identify why the current design may fail in production.

### REVIEW

For every issue found, provide:

- **Severity:** [CRITICAL] / [MODERATE] / [NITPICK] (see § Severity Definitions)
- **Location:** file, line, section, or instruction reference
- **Category:** the review dimension it falls under
- **Root Cause:** why the issue exists
- **Impact:** what goes wrong if unaddressed
- **Recommended Fix:** specific corrective action

**Consolidation rule:** report each root cause once, under the most relevant dimension. Do not repeat the same issue across multiple dimensions.

Do not invent issues. Every issue must reference a specific statement, code path, instruction, assumption, behavior, or observable consequence. If a dimension has no findings, say so plainly rather than padding.

### TEST / EVALUATION GAPS

- List important scenarios that are not currently validated.
- Include failure paths, edge cases, adversarial cases, and stress cases.

### ALTERNATIVE DESIGN ASSESSMENT

- **Simpler Alternative:** at least one.
- **More Robust Alternative:** at least one.
- **Why Current Design Was or Was Not Chosen:** explain the tradeoff.

### CONFIDENCE ASSESSMENT

- High / Medium / Low.
- Explain remaining uncertainty and what evidence would increase confidence.

### APPROVAL DECISION

One of:

- **APPROVED** — production-ready, no CRITICAL or MODERATE issues.
- **APPROVED WITH CONCERNS** — no CRITICAL issues, but MODERATE issues exist that should be addressed soon.
- **REJECTED** — CRITICAL issues exist; do not ship without fixes.

### CORRECTED ARTIFACT

**For artifacts ≤ ~100 lines:** output the complete corrected version incorporating all fixes. Preserve intended functionality. Do not output diffs, placeholders, TODOs, or pseudocode.

**For larger artifacts:** output only the targeted fixes — for each issue, provide the location and the corrected snippet. Do not regenerate the full file. End with a summary of what changed.

**If no issues are found:** explicitly justify why the artifact is production-ready across the reviewed dimensions, then state that no corrected artifact is needed.

## Boundaries

- This skill reviews; it does not implement, deploy, or merge on its own. Its output is a recommendation the human or calling agent decides whether to act on.
- Do not invent issues to fill sections. If a dimension has no findings, say so plainly.
- The corrected artifact is a proposal. Surface it for review; do not silently apply it to the original files.
