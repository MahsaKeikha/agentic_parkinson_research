"""Read-only FoG-STAR v3 sensor/clinical structure and annotation audit.

This script does not invent expert event identifiers: contiguous fog=1 sample
runs are *binary-label runs*, not necessarily the 101 clinically adjudicated
episodes described by the authors. It refuses to claim reconciliation.
"""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

REQUIRED_SENSOR = {"timestamp", "subjectID", "sessionID", "taskID", "fog", "fog_severity"}
REQUIRED_CLINICAL = {"subjectID"}
EXPECTED_ROWS = 329027
EXPECTED_PARTICIPANTS = 22


def audit(root):
    root = Path(root)
    sensor, clinical = root / "sensor_data.csv", root / "clinical_data.csv"
    if not sensor.is_file() or not clinical.is_file():
        raise FileNotFoundError("both official sensor and clinical CSV files are required")
    with clinical.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not REQUIRED_CLINICAL.issubset(reader.fieldnames):
            raise ValueError("clinical schema missing subjectID")
        clinical_ids = [row["subjectID"].strip() for row in reader]
    if len(clinical_ids) != len(set(clinical_ids)):
        raise ValueError("duplicate clinical subjectID")
    rows = 0
    ids = set()
    labels = Counter()
    segments = Counter()
    binary_runs = 0
    previous_key = None
    previous_positive = False
    previous_time = None
    discontinuities = 0
    with sensor.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not REQUIRED_SENSOR.issubset(reader.fieldnames):
            raise ValueError("sensor schema missing required columns")
        for row in reader:
            rows += 1
            key = tuple(row[name].strip() for name in ("subjectID", "sessionID", "taskID"))
            ids.add(key[0])
            segments[key] += 1
            label = row["fog"].strip()
            if label not in {"0", "1"}:
                raise ValueError(f"row {rows}: fog label is not binary")
            labels[label] += 1
            timestamp = float(row["timestamp"])
            if not math.isfinite(timestamp):
                raise ValueError(f"row {rows}: nonfinite timestamp")
            boundary = key != previous_key
            if not boundary and previous_time is not None and timestamp <= previous_time:
                discontinuities += 1
                boundary = True
            positive = label == "1"
            if positive and (boundary or not previous_positive):
                binary_runs += 1
            previous_key, previous_positive, previous_time = key, positive, timestamp
    if not ids.issubset(set(clinical_ids)):
        raise ValueError("sensor participant missing from clinical file")
    return {
        "sensor_rows_observed": rows,
        "published_sensor_rows": EXPECTED_ROWS,
        "row_count_matches_publication": rows == EXPECTED_ROWS,
        "sensor_participants_observed": len(ids),
        "published_participants": EXPECTED_PARTICIPANTS,
        "participant_count_matches_publication": len(ids) == EXPECTED_PARTICIPANTS,
        "clinical_participants_observed": len(clinical_ids),
        "subject_session_task_combinations": len(segments),
        "fog_binary_label_counts": dict(labels),
        "binary_positive_runs_in_file_order": binary_runs,
        "nonincreasing_timestamp_boundaries": discontinuities,
        "published_expert_episodes": 101,
        "expert_episode_reconciliation": "NOT VERIFIED: binary runs cannot substitute for adjudicated episodes",
        "scientific_release_approved": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.data_root)
    output = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
