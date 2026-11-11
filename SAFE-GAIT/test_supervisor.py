import unittest

import numpy as np

from supervisor import apply_policy, choose_alert_threshold


class TestSupervisor(unittest.TestCase):
    def test_validation_recall_threshold(self):
        p = np.array([0.1, 0.3, 0.7, 0.9])
        y = np.array([0, 1, 1, 1])
        threshold = choose_alert_threshold(p, y, target_recall=2 / 3)
        self.assertAlmostEqual(threshold, 0.7)

    def test_actions_and_low_quality_abstain(self):
        actions = apply_policy([0.1, 0.55, 0.9, 0.95], [1, 1, 1, 0.2],
                               high=0.6, uncertainty_width=0.1)
        self.assertEqual(actions.tolist(), [0, -1, 1, -1])

    def test_requires_positive_validation(self):
        self.assertIsNone(choose_alert_threshold(np.array([0.2, 0.7]),
                                                 np.array([0, 0])))


if __name__ == "__main__":
    unittest.main()
