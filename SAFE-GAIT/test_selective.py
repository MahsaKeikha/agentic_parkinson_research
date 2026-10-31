import unittest

import numpy as np

from selective import nonconformity, policy_metrics, threshold_for_coverage


class TestSelectivePolicy(unittest.TestCase):
    def test_uncertainty(self):
        self.assertTrue(np.allclose(nonconformity(np.array([0.1, 0.5, 0.9])), [0.1, 0.5, 0.1]))

    def test_policy_error(self):
        y = np.array([0, 1, 1, 0])
        p = np.array([0.1, 0.8, 0.3, 0.9])
        result = policy_metrics(y, p, np.array([1, 1, 1, 0], dtype=bool))
        self.assertAlmostEqual(result["coverage"], 0.75)
        self.assertAlmostEqual(result["accepted_error"], 1 / 3)

    def test_calibration_cutoff(self):
        scores = np.array([0.01, 0.02, 0.30, 0.40, 0.49])
        cutoff = threshold_for_coverage(scores, 0.6)
        self.assertEqual(cutoff, 0.30)

    def test_class_retention_is_reported(self):
        y = np.array([1, 1, 0, 0])
        p = np.array([0.9, 0.6, 0.1, 0.2])
        metrics = policy_metrics(y, p, np.array([1, 0, 1, 1], dtype=bool))
        self.assertAlmostEqual(metrics["positive_retention"], 0.5)
        self.assertAlmostEqual(metrics["negative_retention"], 1.0)


if __name__ == "__main__":
    unittest.main()
