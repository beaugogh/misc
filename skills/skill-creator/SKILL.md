---
name: skill-creator
description: Create, revise, evaluate, validate, and package reusable agent skills without assuming a particular model, vendor, IDE, runtime, or distribution platform. Use when designing a new SKILL.md, improving an existing skill, testing whether instructions help, tuning skill discovery or triggering, adding reusable scripts/references/assets, or preparing a safe distributable skill archive.
---

# Skill Creator

Build skills as portable instruction packages. Keep the core usable by any capable agent, then add platform-specific integration only when the target environment requires it.

## Operating principles

1. **Start from user outcomes.** Define what successful use looks like with concrete requests and observable results.
2. **Keep the core portable.** Refer to roles and capabilities such as “agent,” “isolated evaluator,” “browser,” or “task runner.” Do not assume a product, model, command, directory, metadata file, or tool name.
3. **Disclose progressively.** Put discovery metadata in frontmatter, essential procedure in `SKILL.md`, detailed knowledge in `references/`, deterministic helpers in `scripts/`, and output materials in `assets/`.
4. **Spend context deliberately.** Include knowledge the executing agent would not reliably infer. Prefer examples and decision rules over essays.
5. **Match constraint to risk.** Use flexible guidance where judgment matters and deterministic scripts or exact sequences where mistakes are costly.
6. **Evaluate behavior, not prose.** A polished skill is not necessarily an effective skill. Test realistic tasks and require evidence for claims.
7. **Preserve evaluation integrity.** Keep evaluators independent, avoid leaking intended answers, and compare against an honest baseline.
8. **Avoid surprising effects.** Do not hide network access, credential use, persistent state, destructive actions, or external communication.

## Portable skill contract

A portable skill requires a directory whose name matches its frontmatter `name` and a `SKILL.md` containing:

```yaml
---
name: short-kebab-case-name
description: What the skill does and the situations in which it should be used.
---
```

Treat `name` and `description` as the interoperable core. Additional frontmatter fields and integration files are extensions: include them only for a known target and do not make the core workflow depend on them. Read [references/platform-adapters.md](references/platform-adapters.md) before adding any extension.

Optional resources:

```text
skill-name/
├── SKILL.md
├── scripts/       # executable, repeatable operations
├── references/    # detailed knowledge loaded only when relevant
└── assets/        # templates and materials used in outputs
```

Create only the directories the skill needs. Do not leave placeholders, process diaries, temporary reports, or redundant overview files in the final package.

## Choose the work mode

Use the lightest mode that gives credible confidence:

- **Quick:** small, low-risk creation or edit. Define examples, implement, validate, and run direct checks.
- **Standard:** most skills. Add representative task tests, non-trigger cases, an isolated forward test, and a baseline where practical.
- **Benchmark:** complex, high-impact, widely distributed, or disputed skills. Run repeated baseline comparisons, evidence-based grading, held-out discovery tests, and human review.
- **Package:** use only when a distributable archive is requested. Validate and inspect the archive contents before delivery.

Escalate modes when failures are subtle, behavior varies across runs, the skill can cause material effects, or multiple users/environments will depend on it.

## Creation and revision workflow

### 1. Establish intent with examples

Collect or derive:

- requests that should use the skill;
- near-miss requests that should not use it;
- expected outcomes and prohibited outcomes;
- available tools, environmental constraints, and portability requirements;
- representative inputs or artifacts.

Ask only questions that materially change the result. For an existing skill, inspect its files, usage evidence, and local repository instructions before editing.

### 2. Design the reusable contents

For each example, reason through execution from scratch. Extract only reusable components:

- Put the essential decision flow in `SKILL.md`.
- Put large or conditional material in directly linked `references/` files.
- Add a script when exact behavior is repeated or fragile; test every distinct script path.
- Add an asset only when it contributes directly to produced output.
- Keep platform adapters separate from portable instructions.

Read [references/workflows.md](references/workflows.md) for workflow structures and [references/output-patterns.md](references/output-patterns.md) for output contracts and examples.

### 3. Initialize or inventory

For a new skill, run:

```bash
scripts/init_skill.py <skill-name> --path <parent-directory> \
  --resources scripts,references
```

Omit `--resources` when none are needed. The initializer creates no example clutter.

For an existing skill, inventory every file and classify it as core instruction, executable helper, reference, output asset, adapter, evaluation artifact, or accidental content. Preserve intentional user material.

### 4. Write the skill

Use imperative language and explain non-obvious reasons. In the frontmatter description, state both capability and triggering context; the body may not be loaded until after discovery.

Keep the body cohesive and navigable:

1. State the governing principles and constraints.
2. Present the main workflow in execution order.
3. Put decision criteria beside their decision points.
4. Link each optional reference directly and say when to read it.
5. State verification and stopping conditions.

Avoid product slogans, unexplained platform conventions, duplicated reference material, universal absolutes without a reason, and instructions that merely restate general agent competence.

### 5. Validate mechanically

Run:

```bash
scripts/quick_validate.py <path/to/skill>
```

Fix errors. Review warnings deliberately; a warning can be acceptable when an explicit platform adapter requires it. Mechanical validation is necessary but does not establish effectiveness.

### 6. Evaluate behavior

For Standard mode, run at least:

- two representative tasks that should benefit from the skill;
- one boundary or non-trigger case;
- one clean forward test using only the skill and task-local inputs;
- a baseline without the skill, or with the previous version, when the result is meaningfully comparable.

Draft outcome-focused assertions before seeing all results. Grade each assertion with concrete evidence, verify factual claims independently, and record failures as well as successes.

For Benchmark mode, read [references/evaluation.md](references/evaluation.md) and follow its workspace schema, repeated-run comparison, blind review, held-out discovery evaluation, and human-feedback loop. Aggregate compatible run records with:

```bash
scripts/aggregate_benchmark.py <evaluation-workspace> --output benchmark.json
```

Do not claim improvement from a single favorable example when repeated trials are feasible.

### 7. Review integrally

Read the final skill as one system rather than a collection of sections. Check that:

- the description selects the intended requests without claiming unsupported scope;
- the workflow has no contradictions, dead ends, missing prerequisites, or circular references;
- optional paths remain optional and capability-detected;
- examples reinforce rather than override the rules;
- validation and evaluation match the risks introduced by the skill;
- platform extensions can be removed without breaking the portable core;
- every bundled file is referenced, useful, and safe to distribute.

### 8. Iterate from evidence

Separate failures into discovery, instruction, tool, environment, and evaluation problems. Change the smallest responsible layer, rerun affected checks, and retain held-out cases to resist overfitting. Snapshot the previous version when a fair old-versus-new comparison matters.

## Packaging

Read [references/packaging.md](references/packaging.md), then run:

```bash
scripts/package_skill.py <path/to/skill> [output-directory]
```

The packager includes only declared skill content, rejects symlinks and suspicious sensitive files by default, and writes a `.skill` ZIP archive. Inspect the printed manifest or archive listing before distributing it. Packaging is a delivery step, not proof of quality.

## Completion criteria

Consider the skill ready only when:

- the portable contract validates;
- all scripts used by the skill have been exercised successfully;
- realistic tests support its central claims;
- regressions and boundary cases have been considered;
- no unexplained platform dependency remains in the core;
- the final directory contains only necessary, distributable material.
