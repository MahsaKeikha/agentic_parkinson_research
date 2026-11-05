import unittest

import pandas as pd

from event_audit import audit


class TestAnnotationAudit(unittest.TestCase):
    def test_source_order_and_timestamp_reset(self):
        # Two distinct runs at the same timestamps must not merge.
        d = pd.DataFrame({"subjectID": [1] * 8, "sessionID": [1] * 8,
                          "taskID": [1] * 8,
                          "timestamp": [0, 1 / 60, 2 / 60, 3 / 60] * 2,
                          "fog": [0, 1, 1, 0, 0, 1, 1, 0]})
        result = audit(d)
        self.assertEqual(result["subject_count"], 1)
        self.assertEqual(result["total_episodes"], 2)


if __name__ == "__main__":
    unittest.main()
