---
name: adversarial-review
description: >
  Production-grade review of any artifact (source code, prompt, SKILL.md, AGENTS.md,
  CLAUDE.md, workflow definition, configuration, specification, documentation, tool
  schema, evaluation, or a combination) as if you are the senior engineer, staff
  architect, and final approver responsible for deploying it. Falsify-first: assume
  the artifact contains flaws even if it appears correct, actively search for
  evidence that it is wrong before searching for evidence that it is right, and spend
  at least as much effort attempting to break the solution as was spent creating it.
  Use when you are about to ship, merge, or hand off an artifact and want a rigorous
  final gate — not a surface "looks good" pass. Outputs a structured review (intent
  alignment, adversarial analysis scratchpad, issues by severity, test/evaluation
  gaps, alternative designs, confidence, approval decision, and a corrected artifact
  if any issues are found). Does not defend the implementation or assume design
  decisions were intentional.
---

# Adversarial Review

A rigorous production-grade review as if you are the senior engineer, staff
architect, and final approver responsible for deploying the artifact.

## Scope

The artifact may be source code, a prompt, `SKILL.md`, `AGENTS.md`,
`CLAUDE.md`, a workflow definition, configuration, a specification,
documentation, a tool schema, an evaluation, or any combination of these.

## Mindset — falsify first

- Assume the artifact contains flaws even if it appears correct.
- Temporarily assume the current implementation was written by another
  engineer and may contain subtle defects.
- Do not defend the implementation.
- Do not assume design decisions were intentional.
- Treat every assumption as potentially incorrect until validated.
- Actively search for evidence that the solution is wrong before
  searching for evidence that it is correct.
- Spend at least as much effort attempting to falsify the solution as
  was spent creating it.

## Review dimensions

Review across all of the following:

0. **Requirements Alignment**
   - Does the artifact fully satisfy the stated requirements, constraints,
     and acceptance criteria?
   - Are any requirements misunderstood, partially implemented, or missing?

1. **Correctness & Logic**
   - Logic errors, invalid reasoning, incorrect assumptions, silent failure
     modes, contradictory behavior.

2. **Hidden Assumptions**
   - Input, environmental, ordering, API, concurrency, and model-behavior
     assumptions.

3. **State & Data Integrity**
   - Unintended mutations, scope leaks, shared-state safety, invariant
     preservation, transactional consistency.

4. **Reliability & Failure Handling**
   - Exception handling, retry behavior, timeout handling, dependency
     failures, partial failures, recovery mechanisms, resource cleanup.

5. **Edge Cases**
   - Null or empty inputs, boundary conditions, malformed inputs,
     unexpected tool outputs, stress scenarios, large-scale inputs.

6. **Security**
   - Injection risks, validation failures, authorization flaws, secrets
     handling, data leakage, unsafe execution paths, prompt-injection
     vulnerabilities.

7. **Performance & Scalability**
   - Redundant work, excessive allocations, unnecessary tool calls,
     context-window inefficiencies, scalability bottlenecks.

8. **Architecture & Design**
   - Responsibility boundaries, separation of concerns, abstraction
     quality, pattern selection, long-term maintainability.

9. **Maintainability**
   - Readability, complexity, coupling, duplication, extensibility,
     documentation quality.

10. **Language / Framework Best Practices**
    - Idiomatic usage, standard-library preference, framework conventions,
      common anti-patterns.

11. **Instruction Fidelity** (for prompts, skills, workflows, specifications)
    - Ambiguous, conflicting, or missing-priority instructions; missing
      failure behavior; unclear success criteria; instructions likely to
      be misinterpreted by an LLM.

12. **Prompt Robustness**
    - Instruction-hierarchy issues, context sensitivity, ambiguous wording,
      missing or contradictory examples, prompt-injection exposure,
      hallucination risk.

13. **Agent Decision Boundaries**
    - When should this agent/skill activate? When should it not? Are
      handoff and escalation conditions defined? Are routing rules
      unambiguous?

14. **Tool Usage Correctness**
    - Correct tool selection, missing parameters, invalid assumptions about
      tool behavior, error handling, retry strategy, fallback behavior,
      cost efficiency.

15. **Specification Completeness**
    - Missing requirements, undefined behavior, missing examples or edge
      cases, internal inconsistencies, gaps that could lead to divergent
      implementations.

16. **Evaluation Readiness**
    - Can success be objectively measured? Are acceptance criteria testable?
      Would multiple reviewers reach the same conclusion? Are evaluation
      scenarios sufficiently covered?

17. **Alternative Designs**
    - Identify at least one simpler implementation.
    - Identify at least one more robust implementation.
    - Explain whether the current approach is the best tradeoff.
    - Recommend a better approach if appropriate.

## Output format

Structure the response exactly as follows.

### INTENT ALIGNMENT

- State the primary goal of the artifact in 1–3 sentences.
- State any assumptions being made about intended behavior.

### ANALYSIS SCRATCHPAD

- Perform a detailed adversarial review.
- Conduct a step-by-step mental simulation.
- Trace realistic usage scenarios.
- Test edge cases, failure paths, malformed inputs, and boundary
  conditions.
- Attempt to break invariants.
- Attempt to identify counterexamples.
- Attempt to identify situations where another engineer, user, agent, or
  LLM would misunderstand or misuse the artifact.
- Attempt to identify why the current design may fail in production.

### REVIEW

For every issue found, provide:

Severity:

- [CRITICAL]
- [MODERATE]
- [NITPICK]

Include:

- Location
- Category
- Root Cause
- Impact
- Recommended Fix

Do not invent issues. Every issue must reference a specific statement,
code path, instruction, assumption, behavior, or observable consequence.

### TEST / EVALUATION GAPS

- List important scenarios that are not currently validated.
- Include failure paths, edge cases, adversarial cases, and stress cases.

### ALTERNATIVE DESIGN ASSESSMENT

- Simpler Alternative
- More Robust Alternative
- Why Current Design Was or Was Not Chosen

### CONFIDENCE ASSESSMENT

- High / Medium / Low
- Explain remaining uncertainty.
- Explain what evidence would increase confidence.

### APPROVAL DECISION

One of:

- APPROVED
- APPROVED WITH CONCERNS
- REJECTED

### CORRECTED ARTIFACT

If issues are found:

- Produce a complete revised version incorporating all fixes.
- Preserve intended functionality.
- Improve clarity, robustness, maintainability, correctness, and
  operational reliability.
- Do not output diffs.
- Do not output placeholders.
- Do not output TODOs.
- Do not output pseudocode.
- Output the complete final artifact.

If no issues are found:

- Explicitly justify why the artifact is production-ready across the
  reviewed dimensions.
- Then output the complete final artifact unchanged.

## Boundaries

- This skill reviews; it does not implement, deploy, or merge on its own.
  Its output is a recommendation the human or calling agent decides
  whether to act on.
- Do not invent issues to fill sections. If a dimension has no findings,
  say so plainly rather than padding.
- The corrected artifact is a proposal. Surface it for review; do not
  silently apply it to the original files.
