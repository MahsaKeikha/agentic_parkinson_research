"""Fast synthetic tests: no external patient data required."""
import unittest

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from baseline import evaluate, extract_windows


class TestBaseline(unittest.TestCase):
    def test_windows_separate_participants(self):
        rows = []
        for sid in (1, 2, 3, 4):
            for idx in range(150):
                rows.append({"subjectID": sid, "sessionID": 1, "taskID": 1,
                             "timestamp": 1000 * idx / 60,
                             "fog": int(idx >= 90), "back_acc_x": float(idx % 7)})
        x, y, groups, channels = extract_windows(pd.DataFrame(rows))
        self.assertGreater(len(x), 0)
        self.assertEqual(channels, ["back_acc_x"])
        for train, test in GroupKFold(n_splits=2).split(x, y, groups):
            self.assertFalse(set(groups[train]) & set(groups[test]))

    def test_metrics_perfect(self):
        scores = evaluate(np.array([0, 1, 0, 1]), np.array([0.1, 0.9, 0.1, 0.9]))
        self.assertEqual(scores["f1"], 1.0)
        self.assertEqual(scores["auroc"], 1.0)


if __name__ == "__main__":
    unittest.main()
