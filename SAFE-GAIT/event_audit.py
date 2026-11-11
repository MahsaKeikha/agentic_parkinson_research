"""Count annotated FoG episodes in source order, without model predictions.

Outputs dataset-level and subject-level summaries only. It deliberately does
not write participant clinical metadata or any raw sensor measurements.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from events import episodes


def audit(data, sample_rate=60):
    required = ["subjectID", "sessionID", "taskID", "timestamp", "fog"]
    if any(c not in data.columns for c in required):
        raise ValueError("FoG-STAR labels and timing columns are required")
    # Preserve original CSV order; sorting all timestamps can join distinct
    # recordings that restart at zero.
    keys = data[["subjectID", "sessionID", "taskID"]]
    transition = keys.ne(keys.shift()).any(axis=1)
    timestamp = pd.to_numeric(data["timestamp"], errors="coerce")
    delta = timestamp.diff()
    positive_delta = delta[(delta > 0) & np.isfinite(delta)]
    if positive_delta.empty:
        raise ValueError("No positive sample intervals")
    interval = float(positive_delta.median())
    # Near 0.0167 denotes seconds, near 16.7 denotes milliseconds.
    scale_to_seconds = 1.0 if interval < 1 else 0.001
    sample_period = 1 / sample_rate
    break_here = transition | ~np.isfinite(delta) | (delta <= 0) | (delta * scale_to_seconds > 1.5 * sample_period)
    block_id = break_here.cumsum()
    summary = {}
    for _, block in data.groupby(block_id, sort=False):
        if len(block) < 2:
            continue
        subject = str(int(block["subjectID"].iloc[0]))
        s = summary.setdefault(subject, {"samples": 0, "positive_samples": 0,
                                         "episodes": 0, "annotated_seconds": 0.0,
                                         "episode_seconds": 0.0})
        times = block["timestamp"].to_numpy(dtype=float) * scale_to_seconds
        labels = pd.to_numeric(block["fog"], errors="coerce").to_numpy(dtype=float)
        event_list = episodes(times, labels, sample_period)
        s["samples"] += len(block)
        s["positive_samples"] += int(np.sum(labels == 1))
        s["episodes"] += len(event_list)
        s["annotated_seconds"] += float(np.sum(np.isin(labels, [0, 1])) / sample_rate)
        s["episode_seconds"] += float(sum(x.duration for x in event_list))
    return {"status": "annotation-only event audit; not a model performance estimate",
            "timestamp_scale_to_seconds": scale_to_seconds,
            "subject_count": len(summary),
            "total_episodes": sum(x["episodes"] for x in summary.values()),
            "total_annotated_seconds": sum(x["annotated_seconds"] for x in summary.values()),
            "subject_summaries": summary}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    data = pd.read_csv(args.sensor_data, usecols=["subjectID", "sessionID", "taskID", "timestamp", "fog"])
    report = audit(data)
    args.out.mkdir(parents=True, exist_ok=True)
    result = args.out / "event_annotation_audit.json"
    result.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {result}")


if __name__ == "__main__":
    main()
