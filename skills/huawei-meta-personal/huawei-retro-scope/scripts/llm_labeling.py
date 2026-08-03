"""LLM-based task labeling (Phase 7.3).

Uses a **local LLM** to read a task's events (prompts, tool calls, file paths,
errors) and produce a natural-language category label like "debugging corporate
proxy authentication for git" or "writing unit tests for the summarizer module."

This is richer than the deterministic classifier (Phase 7.1, 15 fixed categories)
because it can produce arbitrary labels grounded in the actual task content.

**Constraints:**
  - Offline only — no external API calls (personal time data stays local).
  - No closed-source/paywalled dependencies (Constitution hard requirement).
  - Falls back to the rule-based classifier when no local LLM is available.
  - Non-blocking — if the LLM fails or is slow, the rule-based label stands.

**Supported local LLM backends (auto-detected):**
  1. Ollama (`ollama` in PATH) — most common local LLM server.
     Uses `ollama run <model>` with a small prompt model (default: qwen2.5:3b).
  2. llama-cpp-python (`llama_cpp` Python package) — direct GGUF inference.
  3. Hugging Face transformers (`transformers` package) — pipeline inference.

The first available backend is used. If none is available, `label_task()`
returns None and the caller falls back to `classify_task()` / `detect_domain()`.

**Prompt design:**
  The prompt is minimal — task subject + top inputs + key tool calls + error
  count — capped at ~500 tokens. The model is asked for a 3-5 word label.
  This keeps inference fast even on small models.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from typing import Optional

# Default model for Ollama (small + fast + good enough for labeling).
DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"

# Max prompt tokens (rough char estimate: 4 chars/token).
MAX_PROMPT_CHARS = 2000

# Label cleanup: strip quotes, periods, "Label:" prefixes, etc.
_LABEL_CLEANUP_RE = re.compile(r'^(label|category|task type)\s*:\s*', re.IGNORECASE)


class LLMLabeler:
    """Local LLM-based task labeler.

    Auto-detects the best available backend. Falls back gracefully when
    no local LLM is installed.
    """

    def __init__(self, ollama_model: str = DEFAULT_OLLAMA_MODEL,
                 timeout: int = 30):
        self._ollama_model = ollama_model
        self._timeout = timeout
        self._backend = self._detect_backend()
        # Cached model instances (loaded once, reused for all tasks).
        self._llm: object = None        # llama_cpp.Llama instance
        self._pipe: object = None       # transformers pipeline instance

    def _detect_backend(self) -> Optional[str]:
        """Detect the best available local LLM backend.

        Returns the backend name ("ollama", "llama_cpp", "transformers")
        or None if no local LLM is available.
        """
        # 1. Ollama (preferred — fastest server-based inference).
        if shutil.which("ollama"):
            try:
                result = subprocess.run(
                    ["ollama", "list"], capture_output=True, text=True,
                    timeout=10,
                )
                if result.returncode == 0 and result.stdout.strip():
                    return "ollama"
            except (subprocess.TimeoutExpired, OSError):
                pass

        # 2. llama-cpp-python (direct GGUF inference).
        try:
            import llama_cpp  # noqa: F401
            return "llama_cpp"
        except ImportError:
            pass

        # 3. Hugging Face transformers (pipeline inference).
        try:
            import transformers  # noqa: F401
            return "transformers"
        except ImportError:
            pass

        return None

    @property
    def is_available(self) -> bool:
        """True if a local LLM backend is available."""
        return self._backend is not None

    @property
    def backend_name(self) -> str:
        """The detected backend name, or 'none' if unavailable."""
        return self._backend or "none"

    def label_task(self, task: dict) -> Optional[str]:
        """Produce a natural-language category label for a task.

        Returns a 3-5 word label like "debugging git proxy auth", or None
        if no LLM backend is available or the LLM fails.

        The label is grounded in the task's actual content: subject, inputs,
        tool calls, errors, and files touched.
        """
        if not self._backend:
            return None

        prompt = self._build_prompt(task)
        if not prompt:
            return None

        try:
            if self._backend == "ollama":
                return self._label_with_ollama(prompt)
            elif self._backend == "llama_cpp":
                return self._label_with_llama_cpp(prompt)
            elif self._backend == "transformers":
                return self._label_with_transformers(prompt)
        except Exception:
            # Any LLM failure — fall back to None (caller uses rule-based label).
            return None

        return None

    def _build_prompt(self, task: dict) -> str:
        """Build a minimal prompt for the LLM.

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

    def _label_with_ollama(self, prompt: str) -> Optional[str]:
        """Generate a label using Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "run", self._ollama_model],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self._timeout,
            )
            if result.returncode == 0 and result.stdout.strip():
                return self._clean_label(result.stdout.strip())
        except (subprocess.TimeoutExpired, OSError):
            pass
        return None

    def _label_with_llama_cpp(self, prompt: str) -> Optional[str]:
        """Generate a label using llama-cpp-python.

        The Llama instance is cached on first use and reused for all subsequent
        calls (loading a GGUF model takes seconds — doing it per-task would be
        impractical for large task sets).
        """
        try:
            if self._llm is None:
                from llama_cpp import Llama
                # The user must download a .gguf model and set LLM_MODEL_PATH.
                model_path = os.environ.get("LLM_MODEL_PATH")
                if not model_path or not os.path.isfile(model_path):
                    return None  # No model file configured.
                self._llm = Llama(model_path=model_path, n_ctx=512, verbose=False)
            response = self._llm(
                prompt,
                max_tokens=20,
                temperature=0.3,
                stop=["\n"],
            )
            text = response["choices"][0]["text"].strip()
            return self._clean_label(text) if text else None
        except Exception:
            return None

    def _label_with_transformers(self, prompt: str) -> Optional[str]:
        """Generate a label using Hugging Face transformers.

        The pipeline is cached on first use. IMPORTANT: the model must already
        be cached locally — this method does NOT download models from the
        internet (offline-only constraint). Set LLM_MODEL_NAME to a model that's
        already in the HF cache, or pre-download with `huggingface-cli download`.
        """
        try:
            if self._pipe is None:
                from transformers import pipeline
                model_name = os.environ.get("LLM_MODEL_NAME", "google/flan-t5-small")
                # Check if the model is already cached locally (offline safety).
                # transformers caches under ~/.cache/huggingface/hub/models--<org>--<name>.
                # If not cached, pipeline() would try to download — violating the
                # offline constraint. We check the cache and skip if not present.
                if not self._is_model_cached(model_name):
                    return None  # Model not cached — skip (offline constraint).
                self._pipe = pipeline("text2text-generation", model=model_name, max_length=20)
            result = self._pipe(prompt)
            text = result[0]["generated_text"].strip()
            return self._clean_label(text) if text else None
        except Exception:
            return None

    def _is_model_cached(self, model_name: str) -> bool:
        """Check if a Hugging Face model is already cached locally.

        Returns True if the model exists in the HF cache directory, False
        otherwise. This prevents internet downloads (offline constraint).
        """
        # HF cache is typically at ~/.cache/huggingface/hub/models--<org>--<name>.
        cache_dir = os.environ.get(
            "HF_HOME",
            os.path.join(os.path.expanduser("~"), ".cache", "huggingface"),
        )
        hub_dir = os.path.join(cache_dir, "hub")
        if not os.path.isdir(hub_dir):
            return False
        # Model name format: "org/name" → "models--org--name".
        model_dir_name = "models--" + model_name.replace("/", "--")
        return os.path.isdir(os.path.join(hub_dir, model_dir_name))

    def _clean_label(self, raw: str) -> str:
        """Clean up the LLM output into a proper label.

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

    Returns the LLM-generated label, or None if no LLM is available.
    The caller should fall back to classify_task() / detect_domain() when None.
    """
    return get_labeler().label_task(task)


def label_tasks(tasks: list[dict]) -> list[dict]:
    """Label all tasks with LLM-generated category labels.

    Adds ``task["llm_label"]`` to each task. Tasks that can't be labeled
    (no LLM, or LLM failure) are left unchanged.

    This is an optional post-processing step — the existing classify_task()
    and detect_domain() provide rule-based labels that stand alone. This adds
    a richer, content-grounded label on top.
    """
    labeler = get_labeler()
    if not labeler.is_available:
        # No LLM available — skip silently (rule-based labels stand).
        return tasks

    for t in tasks:
        label = labeler.label_task(t)
        if label:
            t["llm_label"] = label

    return tasks


if __name__ == "__main__":
    # Quick self-test.
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    labeler = LLMLabeler()
    print(f"Backend: {labeler.backend_name}")
    print(f"Available: {labeler.is_available}")

    if labeler.is_available:
        # Test with a synthetic task.
        task = {
            "subject": "sync local main branch with remote",
            "source_kind": "ai_session",
            "tool_names": ["Bash", "Read", "Edit"],
            "errors": 46,
            "inputs": ["prompt: sync local main branch with remote",
                       "read: .git/config"],
            "context": {
                "narrative": "Goal: sync local main with remote. Git fetch failed with 407 proxy auth.",
                "files_touched": [".git/config", "MEMORY.md"],
            },
        }
        label = labeler.label_task(task)
        print(f"Label: {label}")
    else:
        print("No local LLM detected. Install ollama or llama-cpp-python to enable.")
        print("Falling back to rule-based classification (classify_task/detect_domain).")
