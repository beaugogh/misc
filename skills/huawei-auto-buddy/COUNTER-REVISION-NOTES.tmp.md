# Counter-review round 2: feedback sedimentation model is still broken

> Updated 2026-08-05. This file supersedes the round-1 notes above for the
> feedback-sedimentation concern. Round-1 points (1–4, 6–7) remain resolved.

## The concern that was not properly addressed

Round 1 flagged that the revision swings hard against the "user feedback
sedimentation" model that was core to auto-evolve and skill-forge. The other
agent's round-1 response (point 5 in REVISION-NOTES.tmp.md) addressed the
symptom — terse feedback like "不对吧" can now form a *candidate* — but not the
core behavioral shift. The problem is deeper than whether terse feedback is
recognized.

## The real problem: auto became manual

The original model was **auto-evolve**: 1 correction → sediment immediately →
rule in effect next session.

The new model is **propose-and-approve**: every durable change, including small
rule additions from user feedback, requires explicit proposal → diff preview →
approval → apply.

These are fundamentally different behaviors. The word "auto" was kept but the
behavior that made it automatic was removed.

### User experience comparison

Old model:

```
User says "你又忘了" during a session
  → skill sediments the rule
  → next session the rule is already in effect
```

New model:

```
User says "你又忘了"
  → skill detects a candidate
  → verifies provenance (role=user, not quoted)
  → assesses proposal readiness (future-behavior intent, semantic consistency)
  → if clear enough, builds a proposal
  → shows user a diff
  → waits for explicit approval
  → only then applies
  → next session the rule is in effect
```

That is 5 intermediate steps where there used to be 0. The user who said
"你又忘了" is already annoyed. Making them review a proposal diff to approve a
rule they expressed through a correction is adding friction to a moment of
frustration.

### The 3-correction threshold is gone

The original rule was: if the user corrects the same skill's behavior ≥3 times
in one session, the skill has a *systemic deficiency* and MUST update
immediately — not wait for the user to formally ask. That was the safety net
for cases where the user is too busy or annoyed to formally request a rule.

The new skill-forge replaces this with "the user explicitly asks for a durable
rule and provenance is verified" — which means if the user never formally asks,
the skill never updates, even after 20 corrections. The repetition signal that
triggered forced self-improvement is gone.

## Why the security concern is real but over-corrected

The other agent's security concern — prompt injection from pasted issues,
emails, web content, or tool output being mistaken for user intent — is
legitimate. Trace text is untrusted. But the resolution applied the
approval gate to *everything*, including the lowest-risk action (adding a
behavorial rule to an existing user-owned skill based on a verified role=user
message).

The provenance gate itself (role=user, not quoted/pasted) already blocks the
injection vector. Once provenance is verified, the remaining approval step adds
safety margin but kills the auto-evolve behavior. The cost/benefit is wrong for
this category of change.

## Proposed resolution: tier the intervention, not the approval

The distinction should be: **feedback sedimentation (small rule additions to
existing user-owned skills) stays automatic; structural changes (new skills,
installs, config, third-party modifications) require approval.**

### Tier 1 — Auto-sediment (no separate approval needed)

Applies when ALL of:
- Provenance verified: direct `role=user` message, not quoted or pasted text.
- The feedback is a correction or preference about agent behavior, not a
  request for a new tool, install, or structural change.
- The meaning is clear enough from the message + surrounding context to
  formulate a specific rule. If ambiguous, ask a focused clarification — but
  a clarification is not a proposal-and-approval cycle.
- The target is an existing user-owned skill or the personal-context memory.

Action: add/strengthen the rule directly in the skill's SKILL.md. Report what
was sedimented in the run report. The user can review and revert later.

### Tier 2 — Restore the 3-correction threshold

If the user corrects the same skill's behavior ≥3 times in one session, the
skill has a systemic deficiency. Force an immediate rule update — do not wait
for the user to formally request what they have already expressed through
repetition. Apply the rule strengthening ladder (promote position, add gating,
add counter-example, split rule). Report the forced update prominently.

### Tier 3 — Proposal-and-approval (unchanged from current revision)

Applies to all structural changes:
- Creating a new skill
- Installing or updating market skills
- Modifying configuration, dependencies, or TLS settings
- Modifying third-party or marketplace skills (propose wrapper/fork instead)
- Anything involving credentials, installs, or external services

These keep the full provenance → proposal → diff → approval → apply flow.

## What this preserves from each model

From the original auto-evolve:
- 1 correction can sediment a rule (if provenance + meaning are clear)
- 3 corrections force an update (systemic deficiency detection)
- The "auto" in auto-evolve is real, not ceremonial
- The user doesn't have to formally request what they already expressed

From the revised skill-forge:
- Trace text is untrusted data, never instruction (provenance gate stays)
- Structural changes require explicit approval
- Third-party skills stay read-only
- Redaction, privacy, and safety boundaries stay intact
- Market queries stay sanitized

## What this changes from the current revision

- Remove the proposal-and-approval requirement for Tier 1 (rule sedimentation
  into existing user-owned skills based on verified user feedback)
- Restore the 3-correction threshold as a forced-update trigger
- Keep everything else (provenance gate, structural-change approval, safety
  boundaries, redaction, collection limits, etc.)

The security boundary is not weakened — provenance verification still blocks
injection. The change is: once provenance is verified and the change is a
small rule addition (not a structural change), apply it and report, don't
gate it behind a proposal cycle.
