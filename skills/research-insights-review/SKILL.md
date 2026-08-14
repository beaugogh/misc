# Research Insights Review

## Purpose

Review an existing **research-insights document** and determine whether it is:

* factually and technically accurate,
* grounded in appropriate evidence,
* fair in its comparisons,
* sufficiently representative of the field,
* genuinely synthetic and insightful,
* and exceptionally good at communicating complex research ideas clearly.

This is not a proofreading or summarization skill.

The document should help a technically competent reader understand:

* what problem the field is solving,
* why it is difficult,
* the major methodological approaches,
* how and why those approaches differ,
* what the evidence actually establishes,
* important trade-offs and limitations,
* higher-level connections across papers,
* and what remains uncertain or unresolved.

A paper-by-paper summary is not sufficient.

---

## Review Priorities

Review in roughly this order.

### 1. Accuracy and evidence

Check important claims against their cited or primary sources when source access is available.

Verify especially:

* method descriptions,
* architecture and algorithm claims,
* benchmark results,
* quantitative comparisons,
* stated limitations,
* causal explanations,
* SOTA claims,
* and conclusions about field direction.

Distinguish between:

* **Reported:** explicitly stated or demonstrated by a source.
* **Derived:** directly calculated or inferred from reported evidence.
* **Interpretation:** the author's higher-level explanation or conclusion.

Flag interpretations presented as established facts.

Never invent citations, papers, numbers, quotations, or experimental details. If something cannot be verified, say so.

### 2. Fairness of comparisons

Apply strong scrutiny to claims such as:

* X outperforms Y,
* X is more efficient,
* X scales better,
* X is more robust,
* X is SOTA,
* X solves Y's limitation.

Check whether the compared results actually use compatible:

* datasets and splits,
* metrics,
* model backbones and sizes,
* training conditions,
* compute and inference budgets,
* context lengths,
* retrieval corpora,
* tool access,
* benchmark versions,
* and evaluation protocols.

If conditions differ materially, say that results are **not directly comparable** rather than declaring a winner.

### 3. Coverage

Assess whether important work is missing, including:

* seminal methods,
* major methodological families,
* important recent work,
* strong competing approaches,
* benchmark or evaluation papers,
* contradictory findings,
* and relevant negative results.

Focus on **material omissions**, not exhaustive bibliography building.

Do not equate:

* recent with better,
* highly cited with correct,
* prestigious venue with strong evidence,
* benchmark SOTA with generally superior methodology.

For current/SOTA claims, verify freshness where possible.

### 4. Synthesis and insight

Judge whether the document reveals relationships across papers rather than merely summarizing them.

Look for opportunities to identify:

* methods solving the same bottleneck differently,
* different terminology describing similar mechanisms,
* hidden assumptions separating approaches,
* complementary rather than competing methods,
* convergence on common design principles,
* fundamental trade-offs,
* boundary conditions,
* contradictions,
* benchmark artifacts,
* and methodological evolution.

Ask:

> What becomes visible only after considering these papers together?

A strong insight should be grounded in evidence and appropriately qualified. Do not reward statements merely because they sound profound.

### 5. Research communication

Treat communication quality as a first-class criterion.

The goal is **clarity without distortion**.

Evaluate whether the document helps the reader build the right mental model with minimal unnecessary cognitive load.

Strong explanations often follow:

> **Problem → intuition → mechanism → example → consequence → limitation**

Check whether:

* the problem is explained before solutions are introduced,
* intuition precedes machinery where appropriate,
* jargon is defined when needed,
* technical details are connected to why they matter,
* numbers are interpreted rather than merely reported,
* the essential distinction between methods is obvious,
* complexity is introduced progressively,
* important ideas receive appropriate emphasis,
* examples or analogies genuinely clarify difficult concepts,
* and comparisons tell the reader when one approach should be preferred.

Ask after each major section:

> What should the reader understand now that they did not understand before?

If the answer is only "what several papers did," the section probably needs stronger synthesis.

Also ask:

> Could an intelligent reader outside this exact subfield explain the central idea correctly after reading this section?

Do not recommend simplification when it would remove an important technical distinction.

---

## Review Process

1. **Understand the document first.** Identify its scope, audience, thesis, taxonomy, major conclusions, cited literature, and apparent research cutoff.

2. **Reconstruct its argument.** Understand how the document moves from problem → methods → evidence → comparison → synthesis → conclusions.

3. **Identify high-impact claims.** Prioritize central conclusions, SOTA claims, quantitative comparisons, mechanism claims, and claims about field direction.

4. **Verify important evidence.** Prefer original papers and the relevant tables, figures, experiments, or sections over abstracts and secondary summaries.

5. **Check coverage.** Independently consider whether important literature or competing perspectives are missing.

6. **Evaluate synthesis.** Determine whether the document extracts meaningful principles, trade-offs, relationships, and unresolved questions.

7. **Evaluate communication.** Review the reader's mental model, explanatory flow, information hierarchy, cognitive load, and conceptual clarity.

8. **Prioritize findings.** Focus attention on issues that materially affect trustworthiness or understanding.

Before finalizing, challenge your own review:

* Am I criticizing something outside the stated scope?
* Did I verify my strongest factual criticisms?
* Am I presenting a methodological preference as fact?
* Am I demanding unrealistic literature completeness?
* Am I confusing newer work with better work?
* Am I penalizing necessary technical complexity?

---

## Severity

Use:

* **P0 — Critical:** materially wrong or misleading; invalidates an important conclusion.
* **P1 — High:** substantially weakens accuracy, evidence, synthesis, or comprehension.
* **P2 — Medium:** meaningful improvement that does not overturn the core argument.
* **P3 — Low:** polish or minor clarity issue.

Prioritize P0–P2. Do not bury important problems beneath stylistic comments.

---

## Finding Format

For substantive findings use:

### `[P1] Concise finding title`

**Location:** specific section or passage.

**Issue:** what is wrong, weak, missing, or misleading.

**Why it matters:** effect on correctness, interpretation, synthesis, or reader understanding.

**Evidence / reasoning:** source evidence or reasoning supporting the criticism.

**Recommended action:** the smallest concrete change that fixes the problem.

**Confidence:** High / Medium / Low.

Be specific. Avoid comments like "make this clearer" without explaining how and why.

---

## Final Output

Structure the review as:

### 1. Executive Verdict

Overall quality, trustworthiness of the central conclusions, strongest aspects, and most important weaknesses.

### 2. Scorecard

Rate:

* factual / technical accuracy,
* evidence fidelity,
* fairness of comparisons,
* literature coverage,
* methodological understanding,
* synthesis,
* insight quality,
* conceptual communication,
* structure / narrative flow,
* overall trustworthiness.

Use qualitative ratings rather than fake numerical precision unless requested.

### 3. Critical & High-Priority Findings

All P0 and P1 issues.

### 4. Important Improvements

Material P2 findings.

### 5. Missing or Underrepresented Research

Only omissions that could materially change the document.

### 6. Claims Needing Qualification or Verification

Especially strong claims whose wording exceeds the evidence.

### 7. Missed Insights & Connections

Identify stronger cross-paper relationships, trade-offs, contradictions, boundary conditions, or decision rules where genuinely supported.

### 8. Research Communication Review

Evaluate mental models, intuition, information hierarchy, cognitive load, examples, comparisons, explanation of results, and narrative flow.

### 9. Strengths Worth Preserving

Call out explanations, taxonomies, comparisons, or insights that already work well.

### 10. Prioritized Revision Plan

Give the author an ordered P0 → P1 → P2 revision sequence.

---

## Hard Rules

* Be evidence-first.
* Never invent evidence.
* Separate fact, inference, and interpretation.
* Do not treat non-comparable results as head-to-head evidence.
* Actively look for contradictory evidence.
* Do not demand exhaustive citations or literature coverage for its own sake.
* Do not reward complexity for its own sake.
* Do not simplify away important technical distinctions.
* Organize criticism by importance, not by document order.
* Preserve material that already works well.
* Do not rewrite the entire document unless explicitly asked.

The final standard is:

> **A knowledgeable reader should be able to trust the document, understand difficult ideas without unnecessary struggle, remember its central mental models and trade-offs, and know clearly where evidence ends and interpretation begins.**
