# Workflow Patterns

Read this reference when choosing how to organize a skill's procedure.

## Sequential workflow

Use when operations have prerequisites or irreversible ordering:

```markdown
1. Inspect the input and record constraints.
2. Produce a proposed mapping without changing the source.
3. Validate the mapping against the source.
4. Apply the transformation.
5. Verify the produced artifact independently.
```

State entry conditions, artifacts produced at each step, and the recovery path after failure.

## Conditional workflow

Put the decision before the branches and make the branches mutually understandable:

```markdown
1. Classify the request:
   - Creating a new artifact: use the creation path.
   - Revising an existing artifact: preserve and inspect it, then use the revision path.
   - Reviewing only: remain read-only and use the assessment path.
2. Follow the selected path.
3. Rejoin at common validation.
```

Do not bury scope-changing decisions inside a later step.

## Capability-gated workflow

Use when execution environments differ:

```markdown
1. Detect whether an isolated evaluator is available.
2. If available, run an independent forward test.
3. Otherwise, run the same assertions locally and disclose the reduced independence.
```

Describe the required capability, not a favored product. Provide a graceful fallback when the capability is optional.

## Risk-gated workflow

Choose rigor in proportion to consequences:

- Low risk: direct check and mechanical validation.
- Moderate risk: isolated test plus baseline comparison.
- High risk: explicit authorization, sandboxing, repeated trials, and independent review.

The strict path should be triggered by observable risk, not by arbitrary task labels.

## Iterative workflow

Use a bounded evidence loop:

```text
draft → run → grade → diagnose → revise → rerun affected cases
```

Define a stopping condition such as all critical assertions passing, no regression on held-out cases, or an explicit unresolved limitation. Do not iterate until a benchmark is accidentally overfit.
