# Code review and fixes

Read when reviewing code or executable behavior, including examples embedded in documents. Shared scope, findings, and approval rules live in [SKILL.md](../SKILL.md). Read accompanying contracts or prose as evidence when needed. Load a prose or specification guide only if reviewing that material is requested or a concrete finding requires its checks; supporting material alone does not expand the review scope.

## Understand the affected behavior

- Establish the intended result from requirements, contracts, callers, and existing tests. Read complete affected functions and the dependencies needed to understand the change. For diffs, distinguish newly introduced defects from pre-existing issues and report the latter only when relevant to scope.
- Follow inputs through validation, authorization, mutation, persistence, outputs, and error handling. Identify who owns resources and which invariants must hold, including when execution stops halfway through.
- Use repository conventions and actual dependency versions. Check uncertain API behavior against the installed implementation or official documentation rather than guessing from memory.

## Investigate applicable failure paths

| Area | Questions that may expose material defects |
|---|---|
| Correctness and contracts | Do branches, comparisons, units, defaults, return types, and error outcomes meet requirements? Are null, empty, malformed, boundary, or large inputs handled where allowed or expected? |
| State and integrity | Are unintended mutations, aliasing, lost updates, duplicate effects, partial writes, or stale state possible? Are transaction and rollback boundaries appropriate? |
| Reliability | Can a timeout leave work running? Are retries bounded and safe for the operation? Do cancellation and exceptions release resources and preserve useful evidence? |
| Security | Does untrusted input cross an execution or trust boundary? Are authorization and ownership checked at the right point? Can logs, error messages, or outputs leak sensitive data? |
| Concurrency | Can ordering, races, locks, reentrancy, or shared state violate invariants under a plausible interleaving? Identify the actual participants and sequence. |
| Performance | Is there a relevant workload under which repeated calls, allocations, blocking, unbounded growth, or asymptotic work causes meaningful harm? Do not report speculative optimizations as defects. |
| Design and maintenance | Do responsibilities, dependencies, abstractions, and language conventions help meet the contract? Recommend redesign only when its benefit justifies the scope and cost. |
| Configuration and workflows | Are parsing, types, defaults, permissions, ordering, environment assumptions, and failure propagation correct for the actual runtime? |

Apply relevant checks deeply, not every row mechanically. A missing test is a validation gap, not proof that behavior is wrong. A hypothetical failure needs reachable conditions and a meaningful consequence before becoming a defect finding.

## Propose and apply focused fixes

Explain the triggering input or execution sequence, expected result, actual behavior, and supporting code or reproduction. Give a concrete patch or snippet. If multiple valid contracts exist, identify the decision instead of silently choosing one.

After approval, change the cause and necessary dependencies. Preserve unrelated behavior, public interfaces, and user edits. A contract change, migration, new dependency, or broad refactor must fit the authorized scope; prefer a smaller correction when it resolves the issue adequately. Update affected examples and docs when behavior intentionally changes.

## Code verification

- Inspect relevant test commands and environment before running them. Use isolated fixtures where the target could mutate data, send messages, incur cost, or affect a live service. Do not execute the artifact merely to discover what it does.
- For a substantive behavior fix, run or add a regression case for the triggering condition and relevant normal/failure behavior. Prefer a failing case before the fix when practical. Tests should assert the required outcome rather than duplicate the implementation.
- Use focused existing tests, type checks, syntax checks, or linters suited to the change. A low-impact naming or prose correction may need only inspection. Broaden testing when dependencies, failures, or unresolved concerns warrant it.
- Inspect the final diff for scope creep, changed contracts, missed call sites, error-path regressions, and necessary cross-artifact updates. Report the commands and outcomes actually observed, distinguishing a passed check from untested behavior.
- If execution is unavailable, state which static evidence supports the fix and which behavior remains unverified. Never claim a test passed because it was proposed or because the code appears correct.
