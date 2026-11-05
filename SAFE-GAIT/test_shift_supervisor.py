import unittest

import numpy as np

from shift_supervisor import SourceDistanceGate, evaluate_gate, participant_bootstrap


class TestShiftSupervisor(unittest.TestCase):
    def test_gate_accepts_source_but_rejects_extreme_shift(self):
        rng = np.random.default_rng(5)
        source = rng.normal(size=(1000, 3))
        gate = SourceDistanceGate(0.9).fit(source)
        self.assertGreaterEqual(gate.accept(source).mean(), 0.9)
        self.assertFalse(gate.accept(np.array([[100.0, 100.0, 100.0]]))[0])

    def test_no_optimistic_coverage_with_abstained_positives(self):
        result = evaluate_gate([1, 1, 0, 0], [0.9, 0.8, 0.2, 0.1], [1, 0, 1, 0])
        self.assertEqual(result["positive_windows_abstained"], 1)
        self.assertEqual(result["coverage"], 0.5)
        self.assertEqual(result["overall_sensitivity_counting_abstention_as_no_alert"], 0.5)

    def test_invalid_fraction(self):
        with self.assertRaises(ValueError):
            SourceDistanceGate(1.1)

    def test_participant_bootstrap_is_repeatable(self):
        subjects = np.repeat(np.arange(4), 6)
        labels = np.tile([0, 0, 0, 1, 1, 1], 4)
        predictions = np.tile([0.1, 0.4, 0.3, 0.8, 0.6, 0.9], 4)
        a = participant_bootstrap(labels, predictions, subjects, repetitions=40, seed=5)
        b = participant_bootstrap(labels, predictions, subjects, repetitions=40, seed=5)
        self.assertEqual(a, b)
        self.assertEqual(a["participants"], 4)
        self.assertEqual(a["valid_resamples"], 40)


if __name__ == "__main__":
    unittest.main()
