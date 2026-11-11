"""Acquire official FoG-STAR v3 files and create a locally verified SHA-256 manifest.

Usage:
  python SAFE-GAIT/tools/acquire_fogstar_v3.py --data-root /path/to/fogstar-v3

Uses authoritative Zenodo API metadata and checks each file against the
publisher's MD5 checksum before recording SHA-256. An independently reviewed
acquisition record is STILL required before declaring scientific provenance.
Never commit participant-level raw data to GitHub.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import urllib.request

API = "https://zenodo.org/api/records/17838806"
RECORD = "https://zenodo.org/records/17838806"
REQUIRED = {"sensor_data.csv", "clinical_data.csv", "README.txt"}
MAX_FILE_BYTES = 500_000_000
# Independently transcribed from the official v3 Zenodo record (not API metadata).
PINNED_V3_MD5 = {
    "sensor_data.csv": "952a37ab147da35e6d4e7a1e9bac44cb",
    "clinical_data.csv": "8b9a2339c8fcb8eaa470bcb1784d31c5",
    "README.txt": "5b424641b0fcf2780037c0e9e838ae10",
}


def digest_file(path, algorithm):
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def acquire(root, metadata=None):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    metadata = fetch_json(API) if metadata is None else metadata
    if str(metadata.get("id")) != "17838806":
        raise ValueError("unexpected Zenodo record identifier")
    files = metadata.get("files", [])
    indexed = {item.get("key"): item for item in files}
    if not REQUIRED.issubset(indexed):
        raise ValueError("official record lacks expected required files")
    entries = []
    for name in sorted(REQUIRED):
        item = indexed[name]
        expected = item.get("checksum", "")
        if not expected.startswith("md5:") or len(expected) != 36:
            raise ValueError(f"{name}: authoritative MD5 missing")
        if expected[4:].lower() != PINNED_V3_MD5[name]:
            raise ValueError(f"{name}: Zenodo metadata differs from independently pinned v3 checksum")
        expected_bytes = item.get("size")
        if (isinstance(expected_bytes, bool) or not isinstance(expected_bytes, int)
                or not 0 < expected_bytes <= MAX_FILE_BYTES):
            raise ValueError(f"{name}: unexpected size")
        url = item.get("links", {}).get("self", "")
        if not isinstance(url, str) or not url.startswith("https://zenodo.org/"):
            raise ValueError(f"{name}: untrusted download URL")
        dest = root / name
        if dest.is_symlink():
            raise ValueError(f"{name}: symlink forbidden")
        if not dest.exists() or dest.stat().st_size != expected_bytes or digest_file(dest, "md5") != expected[4:]:
            tmp = root / (name + ".part")
            if tmp.is_symlink():
                raise ValueError(f"{name}: temporary symlink forbidden")
            try:
                with urllib.request.urlopen(url, timeout=120) as response, tmp.open("wb") as out:
                    total = 0
                    for chunk in iter(lambda: response.read(1024 * 1024), b""):
                        total += len(chunk)
                        if total > expected_bytes:
                            raise ValueError(f"{name}: exceeds expected byte size")
                        out.write(chunk)
                if tmp.stat().st_size != expected_bytes or digest_file(tmp, "md5") != expected[4:]:
                    raise ValueError(f"{name}: publisher checksum or size mismatch")
                os.replace(tmp, dest)
            finally:
                tmp.unlink(missing_ok=True)
        entries.append({"path": name, "size_bytes": expected_bytes,
                        "sha256": digest_file(dest, "sha256"),
                        "zenodo_md5": expected})
    manifest = {"dataset": "FoG-STAR", "version": "v3",
                "source_record": RECORD, "record_id": 17838806,
                "record_doi": metadata.get("doi"),
                "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "files": entries,
                "provenance_status": "PUBLISHER_MD5_MATCHED; INDEPENDENT_REVIEW_PENDING"}
    output = root / "fogstar_v3_acquisition_manifest.json"
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(acquire(args.data_root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
