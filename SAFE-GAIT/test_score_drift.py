import unittest

from score_drift import ecdf_distance


class TestScoreDrift(unittest.TestCase):
    def test_identical_distributions_have_zero_distance(self):
        self.assertAlmostEqual(ecdf_distance([0.1, 0.4, 0.9], [0.9, 0.1, 0.4]), 0.0)

    def test_disjoint_distributions_have_distance_one(self):
        self.assertAlmostEqual(ecdf_distance([0.1, 0.2], [0.8, 0.9]), 1.0)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            ecdf_distance([], [0.1])


if __name__ == "__main__":
    unittest.main()
