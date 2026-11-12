# Optional deep review

Read for an explicitly requested deep/final-gate review or a concrete risk warranting additional review process. Use the bundled code, document, or prompt guide for the actual review dimensions. All additional methods needed for this mode are described below.

## Define exactly what is being reviewed

- Record the requested targets and comparison: selected files, full artifacts, committed changes, staged changes, unstaged changes, or their requested combination. Do not silently replace a whole-file review with a diff or omit requested uncommitted changes.
- For committed changes, resolve moving Git references to commit SHAs. State the comparison semantics: a branch-change review normally compares the merge base with the pinned head; an explicit endpoint comparison uses those endpoints. Record the effective base and head so another reviewer can inspect the same material.
- For working-tree review, record the base commit and inspect the requested staged and/or unstaged differences. Untracked files are not included in `git diff HEAD`; inspect them separately when in scope. Paths and a commit SHA alone do not freeze uncommitted content: preserve the relevant content or content hashes in permitted review output, or explicitly state that the review reflects the inspected working-tree state.
- For standalone or non-Git material, identify the supplied version or inspected content. If evidence changes during review, reread affected material before finalizing findings. Do not create worktrees, stage, commit, alter branches, or modify targets merely to establish the review boundary.
- Invalid references, missing targets, or an empty requested change set are scope problems to report before dispatching reviewers. Do not substitute another comparison without explanation.

## Optional independent perspectives

Use independent reviewers only when the host supports them and delegation is explicitly authorized by the user or governing instructions. A deep-review request alone does not authorize spawning agents. Otherwise conduct the applicable passes in the current context and describe them as self-review, not independent validation.

Choose only perspectives that add value; there is no mandatory reviewer count:

| Perspective | Brief |
|---|---|
| Requirements and intent | Compare the change with requirements and acceptance criteria; find omissions, unintended behavior, and scope creep |
| Implementation quality | Check relevant project standards, responsibility boundaries, complexity, and maintainability; distinguish preferences from defects |
| Failure behavior | Investigate concrete counterexamples, trust boundaries, partial failures, state integrity, and other consequential risks |

Give each reviewer the same defined change boundary, relevant requirements, applicable project instructions, and the context needed for its brief. Supply facts rather than the author's preferred conclusions; omit ambient conversation history and other reviewers' findings. Allow targeted read-only inspection rather than pasting the whole repository or every reference into every prompt.

Reviewers are read-only: no edits, Git-state changes, deployment, or execution with live side effects. Ask for concise findings with location, triggering conditions, evidence, impact, and a proposed correction. No findings is valid. Independence requires separate contexts; sequential passes in the same context do not provide it.

## Validate and synthesize

- Check each recommendation against the actual contract, code, document, and relevant evidence before adopting it. A reviewer can be mistaken. Unsupported or incorrect findings should be rejected with a concrete reason; unresolved claims remain questions or verification gaps.
- Consolidate duplicate root causes once, merging useful evidence. Repetition or agreement across reviewers is not by itself evidence of greater impact or certainty. Resolve disagreements using the triggering conditions and consequences, not voting.
- Assign final severity using [the shared definitions](../SKILL.md). Do not automatically take the highest suggested severity. Preserve material evidence when correcting a severity assessment.
- Run suitable focused checks where safe, and report actual results and important gaps. A validation failure needs interpretation; a lack of reproduction does not automatically invalidate a finding supported by a clear reachable code path.
- Deliver the normal concise findings and scoped verdict. Mention independent coverage only when it actually occurred. Propose alternatives only when they improve a real decision; apply fixes only within existing approval.
