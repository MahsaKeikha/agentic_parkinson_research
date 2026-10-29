import unittest

import numpy as np

from calibrated_drift import source_calibration


class TestCalibratedDrift(unittest.TestCase):
    def test_threshold_only_depends_on_source_features(self):
        rng = np.random.default_rng(7)
        features = rng.normal(size=(100, 3))
        subjects = np.repeat(np.arange(10), 10)
        labels = np.tile([0, 0, 0, 1, 1, 1, 1, 0, 0, 0], 10)
        first, cutoff = source_calibration(features, labels, subjects)
        second, again = source_calibration(features, labels, subjects)
        self.assertEqual(first, second)
        self.assertEqual(cutoff, again)
        self.assertEqual(len(first), 5)
        self.assertTrue(0 <= cutoff <= 1)


if __name__ == "__main__":
    unittest.main()
