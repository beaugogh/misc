# Output Patterns

Read this reference when a skill must produce consistent artifacts or quality standards.

## Contract pattern

Specify required content and invariants before presentation details:

```markdown
Produce a report containing:

- a one-paragraph decision summary;
- findings tied to inspected evidence;
- severity and confidence for each finding;
- concrete remediation for actionable findings;
- explicit limitations and unverified assumptions.

Do not report a claim as verified without identifying its evidence.
```

Use exact schemas only when a downstream parser requires them. Otherwise allow the executing agent to adapt headings and ordering to the task.

## Template pattern

Provide a template when stable structure reduces omissions:

```markdown
# [Artifact title]

## Outcome
[What changed or what was concluded]

## Evidence
[Checks, artifacts, or observations supporting the outcome]

## Limitations
[Anything unresolved or not tested]
```

Mark optional sections explicitly. Avoid templates that encourage empty filler.

## Example pattern

Use compact input/output pairs when quality depends on style or boundary judgment. Include varied examples and at least one near miss. Explain the governing property so examples do not become accidental hard-coded rules.

## Assertion pattern

Make evaluation criteria observable:

```json
{
  "text": "The output preserves every input identifier exactly.",
  "critical": true
}
```

Prefer assertions about user-visible outcomes over implementation trivia. A grader should be able to cite evidence for pass or failure.

## Structured-output pattern

When machine-readable output is required:

- provide a schema and one valid example;
- define required versus optional fields;
- define unknown-value and error representation;
- forbid commentary outside the structure only if the consumer requires it;
- validate generated output with a parser or schema checker.
