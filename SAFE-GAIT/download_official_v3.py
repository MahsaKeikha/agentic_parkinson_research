"""Fetch and independently verify FoG-STAR v3 files via the Zenodo API.

No download is trusted before a checksum match. The downloader never writes
raw source data to the repository and does not execute experiments.
"""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

RECORD_ID = 17838806
API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"
EXPECTED = {
    "sensor_data.csv": "952a37ab147da35e6d4e7a1e9bac44cb",
    "clinical_data.csv": "8b9a2339c8fcb8eaa470bcb1784d31c5",
}

def parse_files(record):
    """Match exact official filenames; fail closed on missing/ambiguous files."""
    if str(record.get("id")) != str(RECORD_ID):
        raise ValueError("Unexpected Zenodo record ID")
    found = {}
    for entry in record.get("files", []):
        name = Path(entry.get("key", "")).name
        if name not in EXPECTED:
            continue
        if name in found:
            raise ValueError(f"Duplicate filename in Zenodo record: {name}")
        checksum = entry.get("checksum", "").lower()
        if checksum != f"md5:{EXPECTED[name]}":
            raise ValueError(f"Zenodo checksum differs from pinned {name}")
        url = entry.get("links", {}).get("self")
        if not isinstance(url, str) or not url.startswith("https://zenodo.org/"):
            raise ValueError(f"Unexpected download URL for {name}")
        found[name] = url
    if set(found) != set(EXPECTED):
        raise ValueError(f"Official files missing: {set(EXPECTED) - set(found)}")
    return found

def fetch_json(url):
    with urllib.request.urlopen(url, timeout=45) as response:
        return json.load(response)

def verified_download(url, destination, expected_md5):
    """Stream to a temporary file, verify hash, then atomically rename."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = destination.with_suffix(destination.suffix + ".part")
    h = hashlib.md5()
    try:
        with urllib.request.urlopen(url, timeout=120) as response, tmp.open("wb") as out:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                out.write(block)
                h.update(block)
        if h.hexdigest() != expected_md5:
            raise ValueError(f"Checksum mismatch for {destination.name}")
        tmp.replace(destination)
    finally:
        tmp.unlink(missing_ok=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--destination", type=Path, required=True,
                   help="Private data directory OUTSIDE git repository")
    args = p.parse_args()
    if args.destination.resolve().is_relative_to(Path(__file__).resolve().parent):
        p.error("Destination must be outside SAFE-GAIT repository folder")
    files = parse_files(fetch_json(API_URL))
    for name, url in files.items():
        dest = args.destination / name
        if dest.exists():
            digest = hashlib.md5(dest.read_bytes()).hexdigest()
            if digest != EXPECTED[name]:
                raise SystemExit(f"Refusing existing file with wrong checksum: {dest}")
            print(f"Already verified: {dest}")
            continue
        verified_download(url, dest, EXPECTED[name])
        print(f"Verified: {dest}")
    print("Official file MD5 checks passed; complete manifest row/column audit is still required.")

if __name__ == "__main__":
    main()
