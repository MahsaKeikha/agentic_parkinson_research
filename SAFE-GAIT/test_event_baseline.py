import unittest

import numpy as np
import pandas as pd

from event_baseline import prepare


class TestEventBaseline(unittest.TestCase):
    def test_window_decision_uses_only_available_samples(self):
        rows = []
        for subject in (1, 2):
            for t in range(120):
                rows.append({"subjectID": subject, "sessionID": 1, "taskID": 1,
                             "timestamp": t / 60, "fog": int(t >= 60),
                             "back_acc_x": float(t % 4)})
        x, y, groups, decision_times, bids, blocks = prepare(pd.DataFrame(rows))
        self.assertEqual(len(y), 2)
        self.assertAlmostEqual(decision_times[0], 2.0)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(set(groups), {1, 2})


if __name__ == "__main__":
    unittest.main()
