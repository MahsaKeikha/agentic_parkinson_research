import unittest

import numpy as np

from participant_drift import leave_one_participant_out


class TestParticipantDrift(unittest.TestCase):
    def test_each_calibration_unit_is_one_person(self):
        rng = np.random.default_rng(11)
        x = rng.normal(size=(60, 3))
        y = np.tile([0, 0, 1, 1, 0, 1], 10)
        g = np.repeat(np.arange(10), 6)
        records = leave_one_participant_out(x, y, g)
        self.assertEqual(len(records), 10)
        self.assertEqual({r["source_subject"] for r in records}, set(range(10)))
        self.assertTrue(all(r["heldout_windows"] == 6 for r in records))
        self.assertTrue(all(r["reference_windows"] == 54 for r in records))


if __name__ == "__main__":
    unittest.main()
