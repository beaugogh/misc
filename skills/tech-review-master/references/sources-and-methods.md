# Package boundaries and verification

All methodology guidance is contained in [the entry point](../SKILL.md) and its local references. Applying the skill does not require another skill, an external writing guide, an online methodology, a downloaded vocabulary, or an external evaluation dataset.

## Bundled resources

- Code, document, and prompt/specification review guides define the checks for each requested scope.
- [Deep review](deep-review.md) contains its full additional process and optional reviewer briefs. Independent agents remain optional and require explicit authorization and host support.
- [Review examples](review-examples.md) and [review scenarios](review-scenarios.md) illustrate the expected decisions and boundaries.
- [Behavioral evaluation](behavioral-evaluation.md) describes how to assess revisions without relying on an outside benchmark.
- The optional Python utilities and their tests use only the standard library. Python 3.10 or newer is needed only to run those tools; see [tool usage](optional-tools.md). Ordinary review does not require them.

The files being reviewed, their requirements, and task-specific evidence are inputs to a review. They are distinct from dependencies on outside methodology. Missing evidence must be reported as a verification limit, not replaced with an invented fact.

## Attribution and validation limits

Keep the bundled [MIT license and copyright notice](../LICENSE) with the package and applicable copies. Attribution does not require loading any outside material.

Assess factual fidelity, useful issue detection, comprehension, natural expression, concision, actionable fixes, and authorization behavior separately. A factual error or unauthorized edit cannot be offset by smoother prose. Allow ties and cases where the original needs no revision.

Report only checks and evaluations actually completed. Tool tests, syntax checks, and valid file structure do not establish superior review quality or universal effectiveness. Self-checks are not independent validation.
