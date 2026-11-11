"""Verify a frozen, independently obtained dataset manifest before SAFE-GAIT experiments.

Manifest schema:
{
  "dataset": "FoG-STAR",
  "version": "v3",
  "source_record": "https://zenodo.org/records/17838806",
  "files": [{"path": "relative/file.csv", "size_bytes": 123, "sha256": "<64 hex>"}]
}
The manifest hashes MUST originate from an independently audited source or a
frozen, separately reviewed acquisition record. Rehashing files does not prove
that they are the official release or that their annotations are valid.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HEX = re.compile(r"^[0-9a-fA-F]{64}$")


def verify(root: Path, manifest: dict) -> dict:
    errors = []
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    if manifest.get("dataset") != "FoG-STAR" or manifest.get("version") != "v3":
        errors.append("dataset and version must identify FoG-STAR v3")
    if not isinstance(manifest.get("source_record"), str) or not manifest["source_record"].strip():
        errors.append("source_record missing")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        return {"status": "BLOCKED", "errors": errors + ["nonempty files list required"], "verified_files": 0}
    root = root.resolve(strict=True)
    seen = set()
    verified = 0
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"file[{i}]: invalid record")
            continue
        rel = entry.get("path")
        size = entry.get("size_bytes")
        digest = entry.get("sha256")
        if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
            errors.append(f"file[{i}]: unsafe relative path")
            continue
        if rel in seen:
            errors.append(f"file[{i}]: duplicate path")
            continue
        seen.add(rel)
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            errors.append(f"file[{i}]: invalid size")
            continue
        if not isinstance(digest, str) or not HEX.fullmatch(digest):
            errors.append(f"file[{i}]: invalid SHA-256")
            continue
        file_path = root / rel
        if file_path.is_symlink():
            errors.append(f"file[{i}]: symlink forbidden")
            continue
        resolved = file_path.resolve()
        if not resolved.is_relative_to(root) or not resolved.is_file():
            errors.append(f"file[{i}]: missing or outside root")
            continue
        if resolved.stat().st_size != size:
            errors.append(f"file[{i}]: byte size mismatch")
            continue
        hasher = hashlib.sha256()
        with resolved.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                hasher.update(chunk)
        if hasher.hexdigest().lower() != digest.lower():
            errors.append(f"file[{i}]: checksum mismatch")
            continue
        verified += 1
    return {"status": "CHECKSUMS_VERIFIED" if not errors else "BLOCKED",
            "errors": errors, "verified_files": verified,
            "manifest_files": len(entries),
            "note": "File integrity only; not official provenance, episode validity, or scientific readiness"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.data_root, json.loads(args.manifest.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "CHECKSUMS_VERIFIED" else 2)


if __name__ == "__main__":
    main()
