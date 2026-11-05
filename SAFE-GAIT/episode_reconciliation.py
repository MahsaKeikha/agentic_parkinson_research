"""Research-only FoG-STAR binary-label run reconciliation; not expert episodes."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

KEYS = ("subjectID", "sessionID", "taskID")
REQUIRED = set(KEYS) | {"timestamp", "fog"}

def reconcile(frame, *, timestamp_unit, sampling_hz=60, max_gap_factor=1.5):
    if timestamp_unit not in ("s", "ms"):
        raise ValueError("timestamp_unit must be s or ms")
    if sampling_hz <= 0 or max_gap_factor <= 1:
        raise ValueError("sampling_hz > 0 and max_gap_factor > 1 required")
    if not REQUIRED.issubset(frame.columns):
        raise ValueError(f"Missing columns: {sorted(REQUIRED - set(frame.columns))}")
    if frame[list(KEYS)].isna().any().any():
        raise ValueError("Missing group identifiers")
    scale = 1.0 if timestamp_unit == "s" else 0.001
    period = 1.0 / sampling_hz
    times = frame.timestamp.to_numpy(dtype=float) * scale
    if not np.isfinite(times).all():
        raise ValueError("Nonfinite timestamps")
    if not len(frame):
        return {"total_rows": 0, "participants": 0, "binary_positive_runs": 0,
                "number_of_contiguous_blocks": 0, "blocks": [],
                "interpretation": "No records; NOT expert-annotated episodes"}
    group_break = frame[list(KEYS)].ne(frame[list(KEYS)].shift()).any(axis=1).to_numpy()
    group_break[0] = True
    dt = np.diff(times)
    gaps = np.r_[False, dt > max_gap_factor * period]
    backward = np.r_[False, dt <= 0]
    starts = np.flatnonzero(group_break | gaps | backward)
    blocks = []
    for no, (lo, hi) in enumerate(zip(starts, np.r_[starts[1:], len(frame)])):
        b = frame.iloc[lo:hi]
        y = b.fog.to_numpy()
        positives = y == 1
        s = np.flatnonzero(positives & ~np.r_[False, positives[:-1]])
        e = np.flatnonzero(positives & ~np.r_[positives[1:], False])
        durations = times[lo+e] - times[lo+s] + period
        reason = ("recording_key_change" if group_break[lo] and lo else
                  "nonincreasing_timestamp" if backward[lo] else
                  "timestamp_gap" if gaps[lo] else "first_row")
        blocks.append({"block": no, "start_row": int(lo), "end_row_exclusive": int(hi),
                       **{k: str(b[k].iloc[0]) for k in KEYS}, "rows": int(hi-lo),
                       "valid_labeled_rows": int(np.isin(y, [0, 1]).sum()),
                       "positive_samples": int(positives.sum()),
                       "binary_positive_runs": int(len(s)),
                       "positive_run_durations_s": [round(float(v), 6) for v in durations],
                       "block_boundary_reason": reason})
    return {"status": "exploratory_reconciliation_only", "timestamp_unit": timestamp_unit,
            "sampling_hz": sampling_hz, "max_gap_factor": max_gap_factor,
            "total_rows": int(len(frame)), "participants": int(frame.subjectID.nunique()),
            "number_of_contiguous_blocks": len(blocks),
            "binary_positive_runs": sum(b["binary_positive_runs"] for b in blocks),
            "n_gaps": int((gaps & ~group_break).sum()),
            "n_nonincreasing_timestamp_steps": int((backward & ~group_break).sum()),
            "blocks": blocks,
            "interpretation": "Binary label runs are NOT the publication's expert episodes"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--timestamp-unit", choices=["s","ms"], required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    result = reconcile(pd.read_csv(a.sensor_data), timestamp_unit=a.timestamp_unit)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2))
    print(result["total_rows"], result["participants"], result["binary_positive_runs"])
if __name__ == "__main__":
    main()
