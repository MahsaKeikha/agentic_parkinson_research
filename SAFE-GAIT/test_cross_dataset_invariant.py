import unittest

import numpy as np

from cross_dataset import three_axis_features
from cross_dataset_invariant import label_free_shift, orientation_invariant


class TestOrientationInvariant(unittest.TestCase):
    def test_magnitude_features_survive_orthogonal_rotation(self):
        rng = np.random.default_rng(14)
        xyz = rng.normal(size=(120, 3))
        rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        left = orientation_invariant(three_axis_features(xyz)[None, :])
        right = orientation_invariant(three_axis_features(xyz @ rotation)[None, :])
        np.testing.assert_allclose(left, right, rtol=1e-12, atol=1e-12)

    def test_rejects_unexpected_layout(self):
        with self.assertRaises(ValueError):
            orientation_invariant(np.ones((4, 11)))

    def test_shift_is_descriptive_and_zero_for_identical_data(self):
        rng = np.random.default_rng(9)
        x = rng.normal(size=(30, 12))
        result = label_free_shift(x, x.copy())
        self.assertEqual(len(result), 3)
        self.assertTrue(all(abs(r["standardized_mean_difference"]) < 1e-12 for r in result))


if __name__ == "__main__":
    unittest.main()
