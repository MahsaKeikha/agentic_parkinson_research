import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from daphnet_audit import audit_daphnet


class TestDaphnetAudit(unittest.TestCase):
    def test_zero_annotation_is_excluded(self):
        with TemporaryDirectory() as temp:
            matrix = np.zeros((5, 11))
            matrix[:, 0] = np.arange(5) * 20
            matrix[:, 10] = [0, 1, 2, 2, 0]
            np.savetxt(Path(temp) / "S01R01.txt", matrix)
            result = audit_daphnet(Path(temp))
            self.assertEqual(result["total_episodes"], 1)
            self.assertEqual(result["per_subject"]["1"]["valid_samples"], 3)


if __name__ == "__main__":
    unittest.main()
