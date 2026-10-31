import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from download_official_v3 import EXPECTED, RECORD_ID, parse_files, verified_download

def record():
    return {"id": RECORD_ID, "files": [
        {"key": name, "checksum": "md5:" + md5,
         "links": {"self": "https://zenodo.org/api/records/17838806/files/" + name + "/content"}}
        for name, md5 in EXPECTED.items()
    ]}

class DownloaderTests(unittest.TestCase):
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
