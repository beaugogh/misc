# Round-three resolution: safe automatic feedback sedimentation

> Updated on 2026-08-05 after counter-review round 2.
>
> Both `.tmp.md` review documents are intentionally retained. The user will remove
> them manually.

## Resolution

Counter-review round 2 correctly identified that the prior revision recognized terse
feedback but still removed the original automatic sedimentation behavior. Every durable
rule required a proposal, diff, and approval, and the former three-correction systemic
trigger had disappeared.

The counter-review was also too broad in claiming that provenance alone makes automatic
mutation safe. Provenance establishes that text came from the user; it does not prove
that a task-local correction should become a persistent cross-session rule, that the
chosen target is correct, or that a proposed rule will not conflict with existing
instructions. Ignored personal skills may also lack ordinary version-control rollback.

The accepted design restores meaningful automation without making every verified phrase
persistent authority.

## Final authority model

### Tier 0: immediate session adaptation

Clear verified feedback changes behavior immediately in the current session. No
persistent write or separate approval is needed.

### Tier 1: automatic candidate, bounded persistence

One clear verified correction or preference is sufficient evidence for a behavioral-rule
candidate. The user does not need to formally request a durable rule. Ambiguous meaning
gets one focused clarification rather than a proposal ceremony.

Default persistence uses one concise approve/reject action stating the rule, exact target,
conflicts, validation, and rollback. The full diff remains available and is mandatory
when the change is not obviously small.

### Tier 2: three-correction systemic trigger

Three verified corrections to the same confirmed user-owned target behavior in one
session mark a systemic deficiency. This forces immediate patch construction,
strengthening, validation, and prominent reporting. It does not by itself authorize an
unbounded write.

If the target has eligible per-target auto-sedimentation authority, apply automatically.
Otherwise present the same single low-friction approve/reject action. This restores the
original safety-net signal while avoiding false root-cause mutation.

### Tier 3: structural proposal and approval

Explicit current approval remains mandatory for:

- new skills;
- frontmatter, description, or trigger changes;
- scripts, assets, dependencies, configuration, credentials, TLS, or external actions;
- identity, project, environment, or other factual memories;
- authority expansion;
- third-party or marketplace artifacts.

## Explicit per-target opt-in

Automatic persistent rule edits are disabled by default. A user may enable them for an
exact confirmed user-owned target in local ignored state:

```text
output/skill_forge_policy.json
```

Policy entries use exact normalized paths relative to `output/`, never globs or absolute
paths. Creating or broadening policy requires explicit approval. Revocation is immediate
when the user directly asks to disable the policy or remove a target.

The policy permits only `behavioral-rules` scope. It does not delegate structural or
external authority.

## Auto-apply eligibility

Every condition must hold:

1. Feedback authorship and meaning are clear.
2. The existing target is confirmed user-owned.
3. The exact target is enabled for `behavioral-rules` in policy.
4. Only the `SKILL.md` body changes.
5. The patch is one logical rule and at most 20 changed lines.
6. Frontmatter, triggers, tools, dependencies, configuration, credentials, TLS,
   external actions, personal facts, and authority are unchanged.
7. The rule does not materially conflict with existing instructions.
8. Validation and relevant tests pass.
9. The per-run rule budget is not exhausted.

Any failure routes the change back to approval or no change; it never silently widens
the auto-apply boundary.

## Backup, rollback, and reporting

Before auto-apply, skill-forge snapshots the original file under:

```text
output/.skill-forge-backups/<target-id>/<UTC-timestamp>/
```

The snapshot includes the original `SKILL.md` and a manifest with target, source hash,
evidence reference, and policy version. Files use restrictive permissions, symlinks are
rejected, and writes are atomic.

If validation or a post-write check fails, restore immediately. After success, report:

- the sedimented rule and triggering feedback category;
- exact target and diff;
- whether authority came from current approval or per-target opt-in;
- validation results;
- backup location and one-step rollback command.

This makes automatic evolution visible and directly reversible rather than relying on
the user to discover a hidden mutation later.

## Active-session feedback

The prior scope rule excluded the currently running session entirely, which would miss
the freshest corrections. The revised rule excludes it only from incomplete work
diagnosis while still inspecting verified direct `role=user` messages for feedback.
Other current-session content remains untrusted evidence.

## Generated-skill ownership

Ownership continues to use creation records, approved proposals, other local provenance,
or explicit current confirmation—not an `auto-buddy-created-*` prefix. This allows
gracefully named user-owned skills such as `npm-corporate-proxy` to participate without
making location alone sufficient authority.

## Retained prior resolutions

The following round-one and round-two conclusions remain unchanged:

- `personal-context` exists locally and its private body was preserved; ignored output
  does not synchronize to another checkout.
- old personal content remains in Git history unless a separate destructive history
  rewrite is explicitly chosen.
- component watermarks are namespaced and legacy cleanup is approval-gated.
- corporate npm may use command-scoped `--strict-ssl=false` for the approved Huawei
  intranet registry, never as global or public-host configuration.
- generated-skill ownership is provenance-based.
- `retro-scope` links its research material through progressive disclosure.
- both `.tmp.md` review documents remain until the user removes them manually.

## Evaluation scenarios

The tracked `skill-forge/evals/feedback-sedimentation.json` fixture defines six cases:

1. one clear correction with default approval policy;
2. one ambiguous correction;
3. three repeated corrections without opt-in;
4. an eligible opted-in automatic edit;
5. a structural change that must ignore auto-sedimentation authority;
6. validation failure requiring immediate rollback.

These cases verify the authority routing. They do not prove general behavioral quality
across all real conversations.

## Current conclusion

Auto Buddy is automatic where automation is both useful and explicitly delegated:
detecting feedback, adapting the current session, constructing candidates, identifying
systemic deficiencies, and applying narrowly scoped rules to opted-in targets. It
remains approval-gated where changes are structural, external, factual, ambiguous, or
outside an exact grant.

This is a coherent middle ground between ceremonial “auto” behavior and unsafe
unconditional self-modification.
