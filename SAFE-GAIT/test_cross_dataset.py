import unittest

import numpy as np

from cross_dataset import three_axis_features, windows_from_run


class TestCrossDataset(unittest.TestCase):
    def test_feature_dimension_and_unit_invariance(self):
        constant_g = np.ones((120, 3))
        f = three_axis_features(constant_g)
        self.assertEqual(len(f), 12)
        self.assertAlmostEqual(f[0], 1.0)
        self.assertAlmostEqual(f[-1], 0.0)

    def test_excludes_unannotated_windows(self):
        x = np.ones((120, 3))
        y = np.full(120, np.nan)
        a, b, c = windows_from_run(np.arange(120) / 60, x, y, 1, 60)
        self.assertEqual(len(a), 0)


if __name__ == "__main__":
    unittest.main()
