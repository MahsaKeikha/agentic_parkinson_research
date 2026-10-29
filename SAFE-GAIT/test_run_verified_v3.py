import tempfile
import unittest
from pathlib import Path
from run_verified_v3 import plan

class TestFullV3Gate(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder=Path(self.tmp.name)
        (self.folder/"S01R01.txt").write_text("synthetic placeholder")
        self.good={"status":"PASS","groups":[{"median_positive_time_step":1/60}]}
    def test_reject_unverified(self):
        with self.assertRaises(ValueError):
            plan({"status":"UNVERIFIED"},timestamp_unit="s",source_dir=self.folder)
    def test_reject_milliseconds_in_existing_parser(self):
        with self.assertRaises(ValueError):
            plan(self.good,timestamp_unit="ms",source_dir=self.folder)
    def test_reject_wrong_sampling_period(self):
        with self.assertRaises(ValueError):
            plan({"status":"PASS","groups":[{"median_positive_time_step":1.0}]},timestamp_unit="s",source_dir=self.folder)
    def test_reject_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            plan(self.good,timestamp_unit="s",source_dir=self.folder/"absent")
    def test_valid_gate_returns_scripts(self):
        self.assertEqual(len(plan(self.good,timestamp_unit="s",source_dir=self.folder)),3)
if __name__=="__main__":
    unittest.main()
