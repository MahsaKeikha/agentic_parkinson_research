"""Verify official FoG-STAR v3 sensor and clinical CSV provenance."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

SENSOR_MD5 = "952a37ab147da35e6d4e7a1e9bac44cb"
CLINICAL_MD5 = "8b9a2339c8fcb8eaa470bcb1784d31c5"

def checksum(path):
    digest = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def run(sensor_path, clinical_path):
    s_md5, c_md5 = checksum(sensor_path), checksum(clinical_path)
    s, c = pd.read_csv(sensor_path), pd.read_csv(clinical_path)
    needed = {"timestamp", "fog", "subjectID", "sessionID", "taskID"}
    if not needed.issubset(s.columns):
        raise ValueError(f"Missing sensor columns: {sorted(needed-set(s.columns))}")
    if "subjectID" not in c.columns:
        raise ValueError("Missing clinical subjectID")
    ids = sorted(int(x) for x in s.subjectID.dropna().unique())
    clinical_ids = set(int(x) for x in c.subjectID.dropna().unique())
    summary = []
    for key, group in s.groupby(["subjectID", "sessionID", "taskID"], sort=False):
        t = group.timestamp.to_numpy(dtype=float)
        y = group.fog.to_numpy()
        positive = y == 1
        episodes = int(np.sum(positive & ~np.r_[False, positive[:-1]]))
        summary.append({"group": list(map(int, key)), "rows": int(len(group)),
                        "naive_positive_runs": episodes,
                        "nonincreasing_timestamps": int(np.sum(np.diff(t) <= 0))})
    checks = {"sensor_checksum": s_md5 == SENSOR_MD5,
              "clinical_checksum": c_md5 == CLINICAL_MD5,
              "sensor_columns": len(s.columns) == 31,
              "sensor_rows": len(s) == 329027,
              "sensor_subjects": len(ids) == 22,
              "sensor_ids_in_clinical": set(ids).issubset(clinical_ids)}
    return {"version": "Zenodo 17838806", "sensor_md5": s_md5,
            "clinical_md5": c_md5, "rows": len(s), "columns": len(s.columns),
            "sensor_ids": ids, "clinical_unique_ids": len(clinical_ids),
            "groups": summary, "checks": checks, "passes": all(checks.values()),
            "caveat": "Naive contiguous positive runs are not necessarily the publication's 101 expert episodes."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--clinical-data", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    report = run(args.sensor_data, args.clinical_data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2))
    print("FoG-STAR v3 manifest:", "PASS" if report["passes"] else "FAIL")
    if not report["passes"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
