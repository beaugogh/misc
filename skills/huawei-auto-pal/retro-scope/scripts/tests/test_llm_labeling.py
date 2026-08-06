"""Tests for LLM-based task labeling (Phase 7.3).

After the v1.0.15 redesign:
  - In-process LLM backends (ollama, llama_cpp, transformers) are removed.
  - is_available always returns False; label_tasks is a no-op.
  - The agent itself is the LLM — it can produce richer labels post-retro-scope.
  - _build_prompt and _clean_label are retained for tests and agent-side use.

Verifies that:
  - LLMLabeler.is_available is always False
  - LLMLabeler.backend_name is always "none"
  - label_task returns None
  - label_tasks returns tasks unchanged (no llm_label added)
  - _build_prompt produces a grounded prompt from task content
  - _clean_label strips prefixes/quotes/periods
"""

import unittest
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from llm_labeling import LLMLabeler, label_task, label_tasks, get_labeler


class TestLLMLabelerNoBackend(unittest.TestCase):
    """The labeler always reports unavailable — no in-process LLM."""

    def test_is_available_always_false(self):
        labeler = LLMLabeler()
        self.assertFalse(labeler.is_available)

    def test_backend_name_always_none(self):
        labeler = LLMLabeler()
        self.assertEqual(labeler.backend_name, "none")

    def test_label_task_returns_none(self):
        labeler = LLMLabeler()
        task = {"subject": "fix login bug", "source_kind": "ai_session"}
        self.assertIsNone(labeler.label_task(task))

    def test_legacy_kwargs_accepted(self):
        """Constructor accepts legacy kwargs (ollama_model, timeout) without error."""
        labeler = LLMLabeler(ollama_model="qwen2.5:3b", timeout=30)
        self.assertFalse(labeler.is_available)

    def test_module_level_label_task_returns_none(self):
        task = {"subject": "fix login bug", "source_kind": "ai_session"}
        self.assertIsNone(label_task(task))


class TestLabelTasksNoOp(unittest.TestCase):
    """label_tasks is a no-op — tasks returned unchanged."""

    def test_tasks_unchanged(self):
        tasks = [
            {"subject": "task1", "source_kind": "ai_session"},
            {"subject": "task2", "source_kind": "ai_session"},
        ]
        result = label_tasks(tasks)
        self.assertEqual(len(result), 2)
        for t in result:
            self.assertNotIn("llm_label", t)

    def test_empty_tasks(self):
        self.assertEqual(label_tasks([]), [])

    def test_preserves_existing_labels(self):
        """If a task already has a label (e.g. from rule-based classifier), it's preserved."""
        tasks = [{"subject": "task1", "llm_label": "existing"}]
        result = label_tasks(tasks)
        self.assertEqual(result[0].get("llm_label"), "existing")


class TestBuildPrompt(unittest.TestCase):
    """_build_prompt is retained for agent-side labeling use."""

    def setUp(self):
        self.labeler = LLMLabeler()

    def test_build_prompt_includes_subject(self):
        task = {"subject": "fix the login bug", "source_kind": "ai_session"}
        prompt = self.labeler._build_prompt(task)
        self.assertIn("fix the login bug", prompt)
        self.assertIn("ai_session", prompt)

    def test_build_prompt_includes_inputs(self):
        task = {
            "subject": "test",
            "inputs": ["prompt: do thing", "read: file.py"],
        }
        prompt = self.labeler._build_prompt(task)
        self.assertIn("do thing", prompt)
        self.assertIn("file.py", prompt)

    def test_build_prompt_includes_errors(self):
        task = {"subject": "test", "errors": 42, "tool_names": ["Bash", "Edit"]}
        prompt = self.labeler._build_prompt(task)
        self.assertIn("42", prompt)
        self.assertIn("Bash", prompt)

    def test_build_prompt_includes_narrative(self):
        task = {
            "subject": "test",
            "context": {"narrative": "Goal: sync git. Failed with 407 proxy error."},
        }
        prompt = self.labeler._build_prompt(task)
        self.assertIn("sync git", prompt)
        self.assertIn("407", prompt)

    def test_build_prompt_caps_length(self):
        task = {
            "subject": "test",
            "inputs": [f"input line {i} " * 20 for i in range(50)],
        }
        prompt = self.labeler._build_prompt(task)
        self.assertLessEqual(len(prompt), 2200)  # MAX_PROMPT_CHARS + prompt template

    def test_build_prompt_empty_task(self):
        prompt = self.labeler._build_prompt({})
        # Even an empty task should produce a prompt (with "(no subject)").
        self.assertIn("(no subject)", prompt)


class TestCleanLabel(unittest.TestCase):
    """_clean_label is retained for agent-side labeling use."""

    def setUp(self):
        self.labeler = LLMLabeler()

    def test_strips_label_prefix(self):
        self.assertEqual(self.labeler._clean_label("Label: debugging git proxy"), "debugging git proxy")

    def test_strips_category_prefix(self):
        self.assertEqual(self.labeler._clean_label("Category: writing tests"), "writing tests")

    def test_strips_quotes(self):
        self.assertEqual(self.labeler._clean_label('"debugging auth"'), "debugging auth")

    def test_strips_trailing_period(self):
        self.assertEqual(self.labeler._clean_label("writing tests."), "writing tests")

    def test_keeps_first_line_only(self):
        self.assertEqual(self.labeler._clean_label("debugging git\nmore text"), "debugging git")

    def test_caps_length(self):
        long_label = "a" * 100
        result = self.labeler._clean_label(long_label)
        self.assertLessEqual(len(result), 60)


class TestGetLabeler(unittest.TestCase):
    """Module-level singleton works correctly."""

    def test_returns_same_instance(self):
        l1 = get_labeler()
        l2 = get_labeler()
        self.assertIs(l1, l2)

    def test_singleton_is_unavailable(self):
        labeler = get_labeler()
        self.assertFalse(labeler.is_available)


if __name__ == "__main__":
    unittest.main()
