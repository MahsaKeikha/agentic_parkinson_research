import tempfile
import unittest
from pathlib import Path
from run_verified_v3 import plan, file_sha256, write_manifest, require_clean_outputs, verify_official_manifest, OFFICIAL_V3

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
    def test_accept_milliseconds_in_verified_runner(self):
        report={"status":"PASS","groups":[{"median_positive_time_step":1000/60}]}
        self.assertEqual(len(plan(report,timestamp_unit="ms",source_dir=self.folder)),3)
    def test_reject_wrong_sampling_period(self):
        with self.assertRaises(ValueError):
            plan({"status":"PASS","groups":[{"median_positive_time_step":1.0}]},timestamp_unit="s",source_dir=self.folder)
    def test_reject_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            plan(self.good,timestamp_unit="s",source_dir=self.folder/"absent")
    def test_valid_gate_returns_scripts(self):
        self.assertEqual(len(plan(self.good,timestamp_unit="s",source_dir=self.folder)),3)
    def test_file_sha256_matches_content(self):
        import hashlib
        p=self.folder/"hash.txt"
        p.write_bytes(b"research-audit")
        self.assertEqual(file_sha256(p), hashlib.sha256(b"research-audit").hexdigest())
    def test_written_run_manifest(self):
        import json
        path=self.folder/"run.json"
        write_manifest(path, {"status":"failed","failure":"example"})
        self.assertEqual(json.loads(path.read_text())["status"],"failed")
    def test_stale_output_fails_closed(self):
        out=self.folder/"results"
        out.mkdir()
        (out/"cross_dataset_shift.json").write_text('{"old":true}')
        with self.assertRaises(FileExistsError):
            require_clean_outputs(out,["cross_dataset.py"])
    def test_empty_output_directory_is_accepted(self):
        out=self.folder/"fresh"
        out.mkdir()
        require_clean_outputs(out,["cross_dataset.py"])
    def test_exact_official_release_manifest(self):
        import copy
        verify_official_manifest(copy.deepcopy(OFFICIAL_V3))

    def test_consistent_subset_manifest_rejected(self):
        import copy
        candidate = copy.deepcopy(OFFICIAL_V3)
        candidate["sensor"]["rows"] = 143530
        with self.assertRaisesRegex(ValueError, "official FoG-STAR v3"):
            verify_official_manifest(candidate)

    def test_wrong_release_hash_rejected(self):
        import copy
        candidate = copy.deepcopy(OFFICIAL_V3)
        candidate["sensor"]["md5"] = "0" * 32
        with self.assertRaises(ValueError):
            verify_official_manifest(candidate)

if __name__=="__main__":
    unittest.main()
