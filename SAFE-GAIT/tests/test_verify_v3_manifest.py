"""Synthetic-only tests of checksum manifest verification."""
import hashlib
import importlib.util
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "verify_v3_manifest.py"
spec = importlib.util.spec_from_file_location("verify_v3_manifest", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record(payload=b"fixture"):
    return {"dataset": "FoG-STAR", "version": "v3",
            "source_record": "https://zenodo.org/records/17838806",
            "files": [{"path": "sample.bin", "size_bytes": len(payload),
                       "sha256": hashlib.sha256(payload).hexdigest()}]}


def test_valid_fixture_integrity_only(tmp_path):
    (tmp_path / "sample.bin").write_bytes(b"fixture")
    result = module.verify(tmp_path, record())
    assert result["status"] == "CHECKSUMS_VERIFIED"
    assert result["verified_files"] == 1


def test_modified_data_blocked(tmp_path):
    (tmp_path / "sample.bin").write_bytes(b"changed")
    assert module.verify(tmp_path, record())["status"] == "BLOCKED"


def test_missing_file_blocked(tmp_path):
    assert module.verify(tmp_path, record())["status"] == "BLOCKED"


def test_traversal_blocked(tmp_path):
    m = record()
    m["files"][0]["path"] = "../sample.bin"
    assert module.verify(tmp_path, m)["status"] == "BLOCKED"


def test_duplicate_file_blocked(tmp_path):
    (tmp_path / "sample.bin").write_bytes(b"fixture")
    m = record()
    m["files"].append(dict(m["files"][0]))
    assert module.verify(tmp_path, m)["status"] == "BLOCKED"


def test_empty_manifest_blocked(tmp_path):
    m = record()
    m["files"] = []
    assert module.verify(tmp_path, m)["status"] == "BLOCKED"


def test_symlink_blocked(tmp_path):
    (tmp_path / "actual.bin").write_bytes(b"fixture")
    (tmp_path / "sample.bin").symlink_to(tmp_path / "actual.bin")
    assert module.verify(tmp_path, record())["status"] == "BLOCKED"
