import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from download_official_v3 import EXPECTED, RECORD_ID, parse_files, verified_download, assert_private_destination, local_md5

def record():
    return {"id": RECORD_ID, "files": [
        {"key": name, "checksum": "md5:" + md5,
         "links": {"self": "https://zenodo.org/api/records/17838806/files/" + name + "/content"}}
        for name, md5 in EXPECTED.items()
    ]}

class DownloaderTests(unittest.TestCase):
    def test_reject_any_path_within_git_checkout(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            (base / ".git").mkdir()
            with self.assertRaises(ValueError):
                assert_private_destination(base / "subfolder" / "data")

    def test_allow_private_path_outside_git(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(assert_private_destination(Path(root)), Path(root).resolve())

    def test_streaming_existing_file_hash(self):
        import hashlib
        with tempfile.TemporaryDirectory() as root:
            file = Path(root) / "sample.csv"
            file.write_bytes(b"sample")
            self.assertEqual(local_md5(file), hashlib.md5(b"sample").hexdigest())

    def test_official_metadata_accepted(self):
        self.assertEqual(set(parse_files(record())), set(EXPECTED))

    def test_wrong_record_rejected(self):
        data = record()
        data["id"] = RECORD_ID + 1
        with self.assertRaises(ValueError):
            parse_files(data)

    def test_wrong_checksum_rejected(self):
        data = record()
        data["files"][0]["checksum"] = "md5:" + "0" * 32
        with self.assertRaises(ValueError):
            parse_files(data)

    def test_duplicate_file_rejected(self):
        data = record()
        data["files"].append(dict(data["files"][0]))
        with self.assertRaises(ValueError):
            parse_files(data)

    def test_partial_download_does_not_replace_data(self):
        with tempfile.TemporaryDirectory() as root:
            dest = Path(root) / "sensor_data.csv"
            with patch("download_official_v3.urllib.request.urlopen") as fetch:
                response = fetch.return_value.__enter__.return_value
                response.read.side_effect = [b"wrong bytes", b""]
                with self.assertRaises(ValueError):
                    verified_download("https://zenodo.org/official", dest, EXPECTED["sensor_data.csv"])
            self.assertFalse(dest.exists())
            self.assertFalse(dest.with_suffix(".csv.part").exists())

if __name__=="__main__":
    unittest.main()
