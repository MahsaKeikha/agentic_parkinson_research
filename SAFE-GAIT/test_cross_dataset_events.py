import unittest

import numpy as np
import pandas as pd

from cross_dataset_events import target_blocks, summarize_policy


class FixedModel:
    def predict_proba(self, values):
        p = np.ones(len(values)) * 0.95
        return np.stack([1 - p, p], axis=1)


class RejectGate:
    def accept(self, values):
        return np.zeros(len(values), dtype=bool)


class TestEventReplay(unittest.TestCase):
    def test_alerts_cannot_precede_window_completion(self):
        rows = [{"subjectID": 1, "sessionID": 1, "taskID": 1,
                 "timestamp": i / 60, "fog": int(i >= 60),
                 "back_acc_x": 1., "back_acc_y": 0., "back_acc_z": 0.}
                for i in range(120)]
        blocks = target_blocks(pd.DataFrame(rows))
        self.assertEqual(len(blocks), 1)
        self.assertAlmostEqual(blocks[0]["decisions"][0], 2.0)
        self.assertEqual(len(blocks[0]["reference"]), 1)
        active = summarize_policy(blocks, FixedModel())["aggregate"]
        rejected = summarize_policy(blocks, FixedModel(), RejectGate())["aggregate"]
        self.assertEqual(active["event_tp"], 0)  # 2s decision after 1s event ends
        self.assertEqual(rejected["event_fn"], 1)
        self.assertEqual(rejected["abstained_windows"], 1)
        self.assertEqual(rejected["alerts"], 0)


if __name__ == "__main__":
    unittest.main()
