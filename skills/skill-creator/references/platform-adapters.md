# Platform Adapters

Read this reference only when a target environment requires integration beyond the portable `SKILL.md` contract.

## Boundary

Keep domain knowledge, user workflow, safety rules, and verification in the portable core. Put environment-specific discovery metadata, command names, tool declarations, installation paths, and UI fields in an adapter file or generator.

An adapter must be removable without making the core instructions incomplete.

## Adapter procedure

1. Identify the target environment and consult its current authoritative specification.
2. List the exact extension points it requires: additional frontmatter, a manifest, UI metadata, tool declarations, or packaging layout.
3. Generate the smallest conforming extension without changing portable semantics.
4. Validate the core with the portable validator and the adapter with the target environment's validator.
5. Test discovery and execution in that environment.
6. Document unavoidable incompatibilities as adapter constraints, not universal skill rules.

## Multiple targets

Prefer independent adapters generated from the same core over a single frontmatter block containing every platform's fields. When requirements conflict, produce separate distribution variants from one canonical source rather than weakening validation for all targets.

Do not assume that trigger behavior, supported metadata, tool syntax, archive format, or installation location transfers between environments.

## Capability language

Write core instructions using neutral roles:

| Core term | Meaning |
|---|---|
| executing agent | the agent following the skill |
| isolated evaluator | an independent context that can run a test without leaked conclusions |
| task runner | any facility that can execute a deterministic helper |
| discovery mechanism | whatever matches a request to skill metadata |
| integration metadata | optional target-specific fields outside the portable contract |

Mention a named product only inside its adapter or when the skill's domain is that product.
