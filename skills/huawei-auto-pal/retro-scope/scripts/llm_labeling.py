"""LLM-based task labeling (Phase 7.3).

**Design change (v1.0.15):** The in-process local LLM backends (ollama,
llama-cpp-python, transformers) have been removed. They were fragile and
redundant — the agent running auto-pal (Claude Code, codeagent, Codex,
OpenClaw, etc.) already has an LLM. Requiring a *separate* local LLM
installation caused real failures: a colleague with ollama running only an
embedding model (bge-m3) hit 30s timeouts × 2347 tasks because `is_available`
returned True but the text generation model (qwen2.5:3b) didn't exist.

Now `is_available` always returns `False` and `label_tasks` is a no-op.
The rule-based classifier (classify_task / detect_domain in aggregate.py)
provides labels that stand alone. The agent itself can produce richer labels
as a post-retro-scope step — it reads the top time sinks from the report and
generates 3-5 word labels grounded in task content, using whatever model the
user chose. This is instructed in SKILL.md, not coded in run.py.

The `_build_prompt` and `_clean_label` helpers are retained for tests and
for potential future use by the agent-side labeling step.
"""

from __future__ import annotations

import os
import re
from typing import Optional

# Max prompt tokens (rough char estimate: 4 chars/token).
MAX_PROMPT_CHARS = 2000

# Label cleanup: strip quotes, periods, "Label:" prefixes, etc.
_LABEL_CLEANUP_RE = re.compile(r'^(label|category|task type)\s*:\s*', re.IGNORECASE)


class LLMLabeler:
    """Task labeler — always reports unavailable.

    The agent running auto-pal is the LLM. In-process local LLM backends have
    been removed (they were fragile and redundant). The rule-based classifier
    provides labels that stand alone; the agent can enrich them post-hoc.
    """

    def __init__(self, **kwargs):
        # Accept and ignore legacy kwargs (ollama_model, timeout) for
        # backward compatibility with existing callers and tests.
        pass

    @property
    def is_available(self) -> bool:
        """Always False — in-process LLM backends removed.

        The agent itself is the LLM. Labeling is done agent-side, not here.
        """
        return False

    @property
    def backend_name(self) -> str:
        """Always 'none'."""
        return "none"

    def label_task(self, task: dict) -> Optional[str]:
        """Always returns None — no in-process LLM backend.

        The caller falls back to the rule-based classifier.
        """
        return None

    def _build_prompt(self, task: dict) -> str:
        """Build a minimal prompt for an LLM.

        Retained for tests and for potential agent-side labeling use.
        Includes: task subject, source kind, key inputs, dominant tools,
        error count, files touched. Capped at MAX_PROMPT_CHARS.
        """
        parts: list[str] = []

        subject = task.get("subject") or "(no subject)"
        parts.append(f"Task: {subject}")

        sk = task.get("source_kind", "")
        if sk:
            parts.append(f"Type: {sk}")

        # Inputs (user prompts, file reads, searches — the what).
        inputs = task.get("inputs", [])[:5]
        if inputs:
            parts.append("Activity:")
            for inp in inputs:
                parts.append(f"  - {inp[:80]}")

        # Tools + errors — the struggle.
        tools = task.get("tool_names", [])
        if tools:
            parts.append(f"Tools: {', '.join(tools[:5])}")

        errors = task.get("errors", 0)
        if errors:
            parts.append(f"Errors: {errors}")

        # Context from the narrative (if available).
        ctx = task.get("context") or {}
        narrative = ctx.get("narrative")
        if narrative:
            parts.append(f"Summary: {narrative[:200]}")

        # Files touched.
        files = ctx.get("files_touched") or []
        if files:
            basenames = [os.path.basename(f) for f in files[:3]]
            parts.append(f"Files: {', '.join(basenames)}")

        task_text = "\n".join(parts)
        if len(task_text) > MAX_PROMPT_CHARS:
            task_text = task_text[:MAX_PROMPT_CHARS] + "..."

        return (
            f"Given this work activity, produce a 3-5 word label describing "
            f"what the person was doing (e.g. 'debugging git proxy auth', "
            f"'writing unit tests', 'researching memory layer libraries'). "
            f"Reply with ONLY the label, no explanation.\n\n{task_text}"
        )

    def _clean_label(self, raw: str) -> str:
        """Clean up LLM output into a proper label.

        Strips: "Label:" prefixes, quotes, trailing periods, multi-line text
        (keep only the first line), excessive whitespace.
        """
        label = raw.strip()
        # Keep only the first line.
        label = label.split("\n")[0].strip()
        # Strip "Label:" / "Category:" prefixes.
        label = _LABEL_CLEANUP_RE.sub("", label)
        # Strip surrounding quotes.
        label = label.strip('"\'').strip()
        # Strip trailing period.
        label = label.rstrip(".").strip()
        # Cap length.
        if len(label) > 60:
            label = label[:57] + "..."
        return label


# Module-level singleton (lazy-initialized).
_labeler: LLMLabeler | None = None


def get_labeler() -> LLMLabeler:
    """Get the module-level LLMLabeler singleton (lazy-initialized)."""
    global _labeler
    if _labeler is None:
        _labeler = LLMLabeler()
    return _labeler


def label_task(task: dict) -> Optional[str]:
    """Convenience: label a task using the module-level labeler.

    Always returns None — no in-process LLM backend. The caller should fall
    back to classify_task() / detect_domain().
    """
    return get_labeler().label_task(task)


def label_tasks(tasks: list[dict]) -> list[dict]:
    """No-op — always returns tasks unchanged.

    In-process LLM backends have been removed. The agent itself is the LLM
    and can produce richer labels post-retro-scope (instructed in SKILL.md).
    The rule-based classifier (classify_task / detect_domain) provides labels
    that stand alone.
    """
    return tasks


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    labeler = LLMLabeler()
    print(f"Backend: {labeler.backend_name}")
    print(f"Available: {labeler.is_available}")
    print("In-process LLM backends removed — the agent itself is the LLM.")
    print("Rule-based labels (classify_task/detect_domain) stand alone.")
