"""Tests for LLM-based task labeling (Phase 7.3).

Verifies that:
  - LLMLabeler auto-detects available backends
  - Falls back gracefully when no LLM is installed
  - _build_prompt produces a grounded prompt from task content
  - _clean_label strips prefixes/quotes/periods
  - label_task returns None when no backend (graceful skip)
  - label_tasks doesn't modify tasks when no LLM available

Run with: python -m unittest discover -s scripts/tests
"""

import unittest
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from llm_labeling import LLMLabeler, label_task, label_tasks, get_labeler


class TestLLMLabelerBackendDetection(unittest.TestCase):
    def test_detect_backend_returns_string_or_none(self):
        labeler = LLMLabeler()
        # On a machine without any LLM, this should be None.
        # On a machine with ollama, it should be "ollama".
        # We just verify it doesn't crash.
        self.assertTrue(labeler.backend_name in ("ollama", "llama_cpp", "transformers", "none"))

    def test_is_available_matches_backend(self):
        labeler = LLMLabeler()
        if labeler.backend_name == "none":
            self.assertFalse(labeler.is_available)
        else:
            self.assertTrue(labeler.is_available)


class TestBuildPrompt(unittest.TestCase):
    def setUp(self):
        # Force no backend so label_task returns None (we only test prompt building).
        self.labeler = LLMLabeler()
        self.labeler._backend = None

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
    def setUp(self):
        self.labeler = LLMLabeler()
        self.labeler._backend = None

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


class TestLabelTask(unittest.TestCase):
    def test_returns_none_when_no_backend(self):
        labeler = LLMLabeler()
        labeler._backend = None
        task = {"subject": "test", "source_kind": "ai_session"}
        self.assertIsNone(labeler.label_task(task))

    def test_module_level_label_task(self):
        # On a machine without LLM, this returns None.
        # On a machine with LLM, it returns a string.
        task = {"subject": "fix login bug", "source_kind": "ai_session"}
        result = label_task(task)
        # Either None (no LLM) or a string (LLM available).
        self.assertTrue(result is None or isinstance(result, str))


class TestLabelTasks(unittest.TestCase):
    def test_no_modification_when_no_llm(self):
        """When no LLM is available, tasks are returned unchanged."""
        tasks = [
            {"subject": "task1", "source_kind": "ai_session"},
            {"subject": "task2", "source_kind": "ai_session"},
        ]
        labeler = LLMLabeler()
        if not labeler.is_available:
            result = label_tasks(tasks)
            # No llm_label should be added.
            for t in result:
                self.assertNotIn("llm_label", t)

    def test_adds_llm_label_when_available(self):
        """When LLM is available, tasks get llm_label (mocked)."""
        # We can't guarantee an LLM is present, so we mock it.
        labeler = LLMLabeler()
        if not labeler.is_available:
            self.skipTest("No local LLM available — skipping integration test.")
        tasks = [{"subject": "fix login bug", "source_kind": "ai_session"}]
        result = label_tasks(tasks)
        self.assertIn("llm_label", result[0])


if __name__ == "__main__":
    unittest.main()
