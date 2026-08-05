# Skill Evaluation

Read this reference for Standard and Benchmark modes when behavioral evidence matters.

## Contents

1. Evaluation questions
2. Workspace layout
3. Test cases and assertions
4. Configurations and baselines
5. Execution integrity
6. Grading
7. Comparison and analysis
8. Discovery evaluation
9. Human review
10. Iteration and stopping

## Evaluation questions

Separate five questions:

1. **Discovery:** Does the description select intended requests and reject near misses?
2. **Compliance:** Does the executing agent follow critical instructions?
3. **Outcome:** Is the produced result correct and useful?
4. **Efficiency:** Does the skill improve time, retries, or resource use enough to justify its context cost?
5. **Portability:** Does the core work when platform-specific adapters are absent or replaced?

Do not collapse them into one subjective score.

## Workspace layout

Keep evaluation artifacts outside the distributable skill:

```text
<skill-name>-workspace/
└── iteration-1/
    ├── eval-001/
    │   ├── case.json
    │   ├── with-skill/
    │   │   ├── output/
    │   │   ├── grading.json
    │   │   └── timing.json
    │   └── baseline/
    │       ├── output/
    │       ├── grading.json
    │       └── timing.json
    └── benchmark.json
```

Use an external workspace or ignored temporary directory so test outputs cannot contaminate later runs or be packaged accidentally.

## Test cases and assertions

Represent each case with a stable identifier, prompt, input artifacts, and assertions:

```json
{
  "id": "eval-001",
  "prompt": "Revise the supplied skill without introducing platform assumptions.",
  "inputs": ["fixtures/example-skill"],
  "assertions": [
    {"text": "The revised core names no vendor-specific runtime.", "critical": true},
    {"text": "All referenced relative files exist.", "critical": true}
  ]
}
```

Draft assertions before inspecting all outputs. Include positive, boundary, adversarial, and regression cases. Assertions should describe observable outcomes and permit evidence-based grading.

## Configurations and baselines

For a new skill, compare `with-skill` against execution without the skill. For a revision, compare against a frozen copy of the previous version. Hold the prompt, inputs, available capabilities, and resource budget constant.

Run comparable configurations close together. Use repeated trials when results may vary; three runs per case and configuration is a useful default, not a universal minimum.

Do not give a baseline information that the skill configuration lacks, or leak the expected result to either side.

## Execution integrity

- Use fresh contexts for independent runs.
- Pass raw task artifacts, not the author's diagnosis or intended fix.
- Record the skill version or content hash.
- Record start/end time, token or resource use when observable, exit status, and tool failures.
- Remove or isolate outputs between runs.
- Preserve failed runs; do not silently rerun until favorable.
- Treat unavailable capabilities as limitations, not fabricated evidence.

## Grading

Grade every assertion as `pass`, `fail`, or `unverified`, with evidence:

```json
{
  "case_id": "eval-001",
  "configuration": "with-skill",
  "trial": 1,
  "expectations": [
    {
      "text": "All referenced relative files exist.",
      "critical": true,
      "status": "pass",
      "evidence": "Validated links A, B, and C against the produced directory."
    }
  ],
  "duration_seconds": 18.4,
  "input_units": 3200,
  "output_units": 740,
  "errors": []
}
```

Require the grader to identify the inspected artifact or observation. Absence of evidence is `unverified`, not `pass`. Independently verify factual claims, file contents, calculations, and executable behavior where possible.

## Comparison and analysis

Aggregate pass rates, critical-failure rates, duration, and observable resource use by configuration. Report sample count and dispersion; means without variability can hide instability. Calculate deltas against the baseline where the metrics are comparable.

Use blind review for subjective quality when practical: conceal configuration labels, randomize output order, and ask a comparator to state a preference with reasons. After grading, analyze failure clusters and distinguish skill defects from task-runner, environment, or grader defects.

The included aggregator accepts `grading.json` files anywhere below a workspace directory. See `scripts/aggregate_benchmark.py --help` for its schema and output.

## Discovery evaluation

Create a balanced set of realistic requests:

- requests that clearly should select the skill;
- indirect phrasings that should still select it;
- adjacent requests that should not select it;
- ambiguous cases near the boundary.

Keep a held-out set. A 60/40 train/test split is a useful default for a small suite. Optimize the description against the training set, choose among candidates using held-out performance, and inspect false positives as carefully as false negatives. Do not add exaggerated scope merely to increase selection rate.

If the environment exposes no observable discovery mechanism, review the cases manually and disclose that automated triggering was not tested.

## Human review

Present outputs, grades, and configuration-blinded comparisons in a form a reviewer can inspect. Collect structured feedback per case: acceptable, preferred output, problems, and suggested changes. Keep reviewer feedback separate from generated grades.

A static HTML page, notebook, or ordinary directory of artifacts is sufficient; no particular UI or browser is required.

## Iteration and stopping

Diagnose before revising:

- discovery failure → revise the description or adapter metadata;
- instruction failure → clarify ordering, decision rules, or constraints;
- tool failure → fix and directly test the helper;
- environment failure → add capability detection or document a prerequisite;
- grading failure → repair ambiguous assertions or grader instructions.

Rerun changed and regression cases. Stop when critical assertions pass, held-out behavior does not regress, improvements justify added complexity, and remaining limitations are explicit. Preserve an honest inconclusive result when evidence is insufficient.
