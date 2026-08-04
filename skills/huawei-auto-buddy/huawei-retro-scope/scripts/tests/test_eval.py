"""Tests for the segmentation evaluation harness (Phase 9.8).

Run with: python -m unittest tests.test_eval -v

Tests WindowDiff, Collar-Based F1, evaluate_segmentation, and the --eval flag
integration. Uses stdlib unittest only — no external dependencies.
"""

import unittest
import os
import sys
import json
import tempfile

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from eval_segmentation import (
    windowdiff,
    collar_f1,
    evaluate_segmentation,
    _build_binary_sequence,
    load_benchmark,
    extract_reference_boundaries,
    extract_predicted_boundaries,
    run_eval,
    format_metrics_report,
)


class TestWindowDiff(unittest.TestCase):
    """Tests for the WindowDiff metric (Pevzner & Hearst, 2002)."""

    def test_identical_sequences_yield_zero(self):
        """When ref == hyp, WindowDiff must be 0.0 (perfect agreement)."""
        ref = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        hyp = ref[:]
        k = 3
        result = windowdiff(ref, hyp, k)
        self.assertEqual(result, 0.0)

    def test_one_boundary_difference(self):
        """A single shifted boundary should produce a small non-zero WindowDiff.

        With k=3 and sequences of length 8:
          ref = [0,0,1,0,0,0,1,0]  (boundaries at positions 2 and 6)
          hyp = [0,0,0,1,0,0,1,0]  (boundary shifted from 2 to 3)

        Windows (i=0..5, each size 3):
          i=0: ref[0:3]=[0,0,1] sum=1, hyp[0:3]=[0,0,0] sum=0 -> disagree (1)
          i=1: ref[1:4]=[0,1,0] sum=1, hyp[1:4]=[0,0,1] sum=1 -> agree
          i=2: ref[2:5]=[1,0,0] sum=1, hyp[2:5]=[0,1,0] sum=1 -> agree
          i=3: ref[3:6]=[0,0,0] sum=0, hyp[3:6]=[1,0,0] sum=1 -> disagree (2)
          i=4: ref[4:7]=[0,0,1] sum=1, hyp[4:7]=[0,0,1] sum=1 -> agree
          i=5: ref[5:8]=[0,1,0] sum=1, hyp[5:8]=[0,1,0] sum=1 -> agree

        Total: 2 disagreements out of 6 windows = 2/6 = 0.3333...
        """
        ref = [0, 0, 1, 0, 0, 0, 1, 0]
        hyp = [0, 0, 0, 1, 0, 0, 1, 0]
        k = 3
        result = windowdiff(ref, hyp, k)
        self.assertAlmostEqual(result, 2.0 / 6.0, places=6)

    def test_completely_different_sequences(self):
        """If hyp has no boundaries but ref has many, WindowDiff should be high."""
        ref = [1, 0, 1, 0, 1, 0, 1, 0]
        hyp = [0, 0, 0, 0, 0, 0, 0, 0]
        k = 2
        result = windowdiff(ref, hyp, k)
        self.assertGreater(result, 0.5)

    def test_too_short_for_window(self):
        """If the sequence is shorter than k, WindowDiff returns 0.0."""
        ref = [0, 1, 0]
        hyp = [0, 0, 0]
        k = 5
        result = windowdiff(ref, hyp, k)
        self.assertEqual(result, 0.0)

    def test_length_mismatch_raises(self):
        """ref and hyp of different lengths should raise ValueError."""
        with self.assertRaises(ValueError):
            windowdiff([0, 1, 0], [0, 1], 2)


class TestCollarF1(unittest.TestCase):
    """Tests for the Collar-Based F1 metric."""

    def test_exact_match_is_true_positive(self):
        """A predicted boundary exactly at a reference boundary is a TP."""
        ref = [1000.0, 2000.0, 3000.0]
        pred = [1000.0, 2000.0, 3000.0]
        result = collar_f1(pred, ref, collar=300)
        self.assertEqual(result["tp"], 3)
        self.assertEqual(result["fp"], 0)
        self.assertEqual(result["fn"], 0)
        self.assertAlmostEqual(result["precision"], 1.0)
        self.assertAlmostEqual(result["recall"], 1.0)
        self.assertAlmostEqual(result["f1"], 1.0)

    def test_within_collar_is_true_positive(self):
        """A predicted boundary 10s from a ref boundary (within 300s collar) is a TP."""
        ref = [1000.0]
        pred = [1010.0]  # 10 seconds away, within 300s collar
        result = collar_f1(pred, ref, collar=300)
        self.assertEqual(result["tp"], 1)
        self.assertEqual(result["fp"], 0)
        self.assertEqual(result["fn"], 0)
        self.assertAlmostEqual(result["f1"], 1.0)

    def test_outside_collar_is_false_positive(self):
        """A predicted boundary 400s from a ref boundary (outside 300s collar) is a FP."""
        ref = [1000.0]
        pred = [1400.0]  # 400 seconds away, outside 300s collar
        result = collar_f1(pred, ref, collar=300)
        self.assertEqual(result["tp"], 0)
        self.assertEqual(result["fp"], 1)
        self.assertEqual(result["fn"], 1)
        self.assertAlmostEqual(result["precision"], 0.0)
        self.assertAlmostEqual(result["recall"], 0.0)
        self.assertAlmostEqual(result["f1"], 0.0)

    def test_empty_predictions(self):
        """No predicted boundaries means 0 precision, 0 recall."""
        ref = [1000.0, 2000.0]
        pred = []
        result = collar_f1(pred, ref, collar=300)
        self.assertEqual(result["tp"], 0)
        self.assertEqual(result["fn"], 2)
        self.assertAlmostEqual(result["f1"], 0.0)

    def test_empty_reference(self):
        """No reference boundaries means all predictions are false positives."""
        ref = []
        pred = [1000.0, 2000.0]
        result = collar_f1(pred, ref, collar=300)
        self.assertEqual(result["tp"], 0)
        self.assertEqual(result["fp"], 2)
        self.assertAlmostEqual(result["f1"], 0.0)

    def test_both_empty(self):
        """Empty ref and pred should yield perfect F1 (trivially correct)."""
        result = collar_f1([], [], collar=300)
        self.assertAlmostEqual(result["f1"], 1.0)

    def test_one_to_one_matching(self):
        """Two predictions near the same reference: only the closest matches."""
        ref = [1000.0]
        pred = [1005.0, 1010.0]  # both within collar, but only one can match
        result = collar_f1(pred, ref, collar=300)
        self.assertEqual(result["tp"], 1)
        self.assertEqual(result["fp"], 1)
        self.assertEqual(result["fn"], 0)
        self.assertAlmostEqual(result["precision"], 0.5)
        self.assertAlmostEqual(result["recall"], 1.0)


class TestEvaluateSegmentation(unittest.TestCase):
    """Tests for the top-level evaluate_segmentation function."""

    def test_returns_all_expected_keys(self):
        """evaluate_segmentation must return all required metric keys."""
        timeline = [1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0,
                    1600.0, 1700.0, 1800.0, 1900.0, 2000.0]
        ref = [1300.0, 1700.0]
        pred = [1300.0, 1700.0]
        result = evaluate_segmentation(pred, ref, timeline, collar_seconds=300)
        expected_keys = {
            "windowdiff", "precision", "recall", "f1",
            "collar_seconds", "n_ref_boundaries", "n_pred_boundaries",
        }
        self.assertTrue(expected_keys.issubset(set(result.keys())))

    def test_perfect_prediction(self):
        """When predicted == reference, all metrics should be near-perfect."""
        timeline = [1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0,
                    1600.0, 1700.0, 1800.0, 1900.0, 2000.0]
        ref = [1300.0, 1700.0]
        pred = [1300.0, 1700.0]
        result = evaluate_segmentation(pred, ref, timeline, collar_seconds=300)
        self.assertEqual(result["windowdiff"], 0.0)
        self.assertAlmostEqual(result["precision"], 1.0)
        self.assertAlmostEqual(result["recall"], 1.0)
        self.assertAlmostEqual(result["f1"], 1.0)
        self.assertEqual(result["n_ref_boundaries"], 2)
        self.assertEqual(result["n_pred_boundaries"], 2)

    def test_collar_seconds_in_result(self):
        """The collar_seconds value should be echoed in the result."""
        timeline = [1000.0, 2000.0, 3000.0, 4000.0]
        result = evaluate_segmentation([2000.0], [3000.0], timeline, collar_seconds=120)
        self.assertEqual(result["collar_seconds"], 120)


class TestBenchmarkLoading(unittest.TestCase):
    """Tests for benchmark fixture loading and boundary extraction."""

    def test_load_benchmark_fixture(self):
        """The benchmark fixture loads and has the expected structure."""
        benchmark = load_benchmark()
        self.assertIn("date", benchmark)
        self.assertIn("session_files", benchmark)
        self.assertIn("reference_boundaries", benchmark)
        self.assertIsInstance(benchmark["reference_boundaries"], list)
        self.assertGreater(len(benchmark["reference_boundaries"]), 0)
        # Each boundary has a timestamp and a note
        for b in benchmark["reference_boundaries"]:
            self.assertIn("timestamp", b)
            self.assertIn("note", b)
            self.assertIsInstance(b["timestamp"], (int, float))

    def test_extract_reference_boundaries(self):
        """extract_reference_boundaries returns a list of floats."""
        benchmark = load_benchmark()
        boundaries = extract_reference_boundaries(benchmark)
        self.assertIsInstance(boundaries, list)
        self.assertGreater(len(boundaries), 0)
        for b in boundaries:
            self.assertIsInstance(b, (int, float))

    def test_extract_predicted_boundaries(self):
        """extract_predicted_boundaries drops the first task start (session start)."""
        tasks = [
            {"start": 1000.0},
            {"start": 2000.0},
            {"start": 3000.0},
        ]
        boundaries = extract_predicted_boundaries(tasks)
        self.assertEqual(boundaries, [2000.0, 3000.0])

    def test_extract_predicted_boundaries_single_task(self):
        """A single task yields no boundaries (no task transitions)."""
        tasks = [{"start": 1000.0}]
        boundaries = extract_predicted_boundaries(tasks)
        self.assertEqual(boundaries, [])

    def test_extract_predicted_boundaries_empty(self):
        """No tasks yields no boundaries."""
        boundaries = extract_predicted_boundaries([])
        self.assertEqual(boundaries, [])


class TestRunEval(unittest.TestCase):
    """Tests for the run_eval function (the --eval flag's core logic)."""

    def test_run_eval_with_mocked_benchmark(self):
        """run_eval should work when the benchmark fixture is loaded,
        even if session files are not available (graceful degradation)."""
        # Create a temporary benchmark fixture with non-existent session files
        with tempfile.TemporaryDirectory() as tmp:
            fixture = {
                "date": "2026-07-14",
                "session_files": ["/nonexistent/path.jsonl"],
                "reference_boundaries": [
                    {"timestamp": 1783993904.0, "note": "test boundary 1"},
                    {"timestamp": 1784010167.0, "note": "test boundary 2"},
                ],
            }
            fixture_path = os.path.join(tmp, "eval_benchmark.json")
            with open(fixture_path, "w") as f:
                json.dump(fixture, f)

            metrics = run_eval(benchmark_path=fixture_path)
            # Should return a dict with all expected keys
            self.assertIn("windowdiff", metrics)
            self.assertIn("f1", metrics)
            self.assertIn("n_ref_boundaries", metrics)
            self.assertEqual(metrics["n_ref_boundaries"], 2)
            self.assertEqual(metrics["n_pred_boundaries"], 0)
            self.assertIn("note", metrics)  # graceful degradation note

    def test_format_metrics_report(self):
        """format_metrics_report produces a readable string with key metrics."""
        metrics = {
            "windowdiff": 0.15,
            "window_k": 5,
            "precision": 0.8,
            "recall": 0.6,
            "f1": 0.69,
            "tp": 12,
            "fp": 3,
            "fn": 8,
            "collar_seconds": 300,
            "n_ref_boundaries": 20,
            "n_pred_boundaries": 15,
            "n_predicted_tasks": 16,
        }
        report = format_metrics_report(metrics)
        self.assertIn("WindowDiff", report)
        self.assertIn("Precision", report)
        self.assertIn("Recall", report)
        self.assertIn("F1", report)
        self.assertIn("0.1500", report)


if __name__ == "__main__":
    unittest.main()
