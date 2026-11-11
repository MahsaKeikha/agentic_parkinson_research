"""Audit Daphnet FoG event counts without making model performance claims."""

import argparse
import json
import re
from pathlib import Path

import numpy as np

from events import episodes


def audit_daphnet(directory):
    files = sorted(directory.glob("S??R??.txt"))
    if not files:
        raise FileNotFoundError("No Daphnet S??R??.txt files found")
    subjects = {}
    for path in files:
        parsed = re.fullmatch(r"S(\d{2})R(\d{2})\.txt", path.name)
        sid = str(int(parsed.group(1)))
        matrix = np.loadtxt(path)
        if matrix.ndim != 2 or matrix.shape[1] != 11:
            raise ValueError(f"Unexpected Daphnet schema in {path.name}")
        time_seconds = matrix[:, 0] / 1000
        annotation = matrix[:, 10]
        # 0 is outside experiment and must never be treated as nonfreeze.
        labels = np.where(annotation == 2, 1.0, np.where(annotation == 1, 0.0, np.nan))
        diffs = np.diff(time_seconds)
        median_period = float(np.median(diffs[diffs > 0]))
        # Avoid crossing recording gaps, nonmonotonic timestamps and excluded regions.
        breaks = np.r_[True, (diffs <= 0) | (diffs > 1.5 * median_period)]
        run_ids = np.cumsum(breaks)
        person = subjects.setdefault(sid, {"files": 0, "valid_samples": 0,
                                           "positive_samples": 0, "episodes": 0,
                                           "recorded_seconds": 0.0})
        person["files"] += 1
        for run in np.unique(run_ids):
            idx = np.where(run_ids == run)[0]
            if len(idx) == 0:
                continue
            ys = labels[idx]
            events = episodes(time_seconds[idx], ys, median_period)
            person["episodes"] += len(events)
            person["valid_samples"] += int(np.sum(np.isfinite(ys)))
            person["positive_samples"] += int(np.sum(ys == 1))
            person["recorded_seconds"] += float(np.sum(np.isfinite(ys)) * median_period)
    return {"status": "annotation-only independent benchmark audit",
            "run_files": len(files), "participants": len(subjects),
            "total_episodes": sum(s["episodes"] for s in subjects.values()),
            "per_subject": subjects}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    result = audit_daphnet(args.dataset_dir)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "daphnet_annotation_audit.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
