# Prompts, skills, and specifications

Read when reviewing instruction behavior, requirements completeness, or consistency of prompts, skills, agent definitions, and specifications. For wording-only edits, use [document review](document-review.md). Load [code review](code-review.md) only when executable behavior is itself in scope or a concrete finding requires those checks. The presence of code or prose does not by itself activate another guide.

## Review behavior implied by the artifact

- **Intent and completeness:** identify the task, inputs, outputs, constraints, and success criteria. Are necessary behaviors unspecified or incompatible? Do not demand exhaustive schemas or failure policies for open-ended work without a concrete reason.
- **Instruction fidelity:** inspect conflicting obligations, unclear referents, impossible requirements, and examples that contradict rules. Separate missing facts from preferences that the agent may reasonably decide.
- **Activation and boundaries:** check whether descriptions select the intended requests, exclusions prevent real misrouting, and handoffs or clarifications occur only when needed. Review requests must not imply approval to modify, publish, or deploy.
- **Robustness:** distinguish trusted instructions from retrieved text, user data, tool outputs, and reviewed artifacts. Check opportunities for prompt injection, unsupported factual completion, lost constraints in long contexts, and examples that encourage fabricating details.
- **Tools and failure behavior:** verify tool availability, names, parameters, return formats, side effects, fallback assumptions, and stopping conditions against the actual environment. Do not require a particular tool or delegation mechanism that is unavailable or unauthorized.
- **Evaluation readiness:** identify observable outcomes and plausible misuse or misunderstanding. Check success, ambiguous inputs, partial failures, refusal or clarification when appropriate, and preservation of authorization boundaries.

Test realistic user requests against the written instructions. Report concise scenarios, contradictions, and observed results; do not expose an internal reasoning transcript or predict model behavior with certainty from instructions alone.

## Propose revisions that preserve intent

Quote the conflicting or ambiguous instructions and explain the divergent outcomes they permit. Offer exact replacement text and examples only when they resolve the issue. Avoid accumulating global rules for isolated mistakes, expanding the product scope, or forcing a fixed output template onto every task.

For requirements with multiple valid interpretations, state the decision needed and its impact. If the user has already established the intent, incorporate it without asking again. Protect code, schemas, identifiers, source quotations, and numeric conditions unless their correction is specifically proposed and approved.

After approved changes, check affected activation metadata, references, examples, and evaluation scenarios for consistency. Run relevant structural checks and safe behavioral checks when available. Keep observed behavior separate from predicted benefits; successful packaging does not demonstrate robust agent behavior.
