"""End-of-window cross-dataset episode replay with source-only abstention.

Research-only retrospective replay. Not real-time or prospective validation.
The FoG-STAR cohort has previously been inspected; results are exploratory.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from cross_dataset import load_daphnet, new_model, three_axis_features
from cross_dataset_invariant import orientation_invariant
from events import episodes, event_summary
from shift_supervisor import SourceDistanceGate


def target_blocks(df, hz=60):
    """Run-isolated raw episodes and end-of-window feature observations."""
    columns = ["subjectID", "sessionID", "taskID", "timestamp", "fog",
               "back_acc_x", "back_acc_y", "back_acc_z"]
    if not set(columns).issubset(df.columns):
        raise ValueError("Required FoG-STAR fields missing")
    keys = df[["subjectID", "sessionID", "taskID"]]
    time = df["timestamp"].to_numpy(dtype=float)
    delta = np.diff(time)
    positive = delta[(delta > 0) & np.isfinite(delta)]
    if not len(positive):
        raise ValueError("No valid sample rate")
    scale = 1.0 if np.median(positive) < 1 else 0.001
    breaks = np.r_[True, (delta <= 0) | ~np.isfinite(delta) |
                   (delta * scale > 1.5 / hz)] | keys.ne(keys.shift()).any(axis=1).to_numpy()
    starts = np.flatnonzero(breaks)
    blocks = []
    size, hop = 2 * hz, hz
    for start, stop in zip(starts, np.r_[starts[1:], len(df)]):
        if stop - start < size:
            continue
        block = df.iloc[start:stop]
        t = time[start:stop] * scale
        y = block["fog"].to_numpy(dtype=float)
        x = block[["back_acc_x", "back_acc_y", "back_acc_z"]].to_numpy(dtype=float)
        features, decisions = [], []
        for offset in range(0, len(y) - size + 1, hop):
            sample_labels = y[offset:offset + size]
            if np.isin(sample_labels, [0, 1]).mean() < 0.9:
                continue
            chunk = x[offset:offset + size]
            if not np.isfinite(chunk).all():
                continue
            features.append(three_axis_features(chunk))
            decisions.append(float(t[offset + size - 1] + 1 / hz))
        blocks.append({"subject": int(block["subjectID"].iloc[0]),
                       "reference": episodes(t, y, 1 / hz),
                       "exposure_seconds": float(np.isin(y, [0, 1]).sum() / hz),
                       "features": np.asarray(features).reshape(-1, 12),
                       "decisions": np.asarray(decisions)})
    return blocks


def summarize_policy(blocks, model, gate=None):
    totals = {"reference_episodes": 0, "event_tp": 0, "event_fn": 0,
              "event_fp": 0, "alerts": 0, "exposure_seconds": 0.,
              "windows": 0, "abstained_windows": 0}
    by_subject = {}
    for block in blocks:
        features = block["features"]
        if len(features):
            x = orientation_invariant(features)
            score = model.predict_proba(x)[:, 1]
            accepted = gate.accept(x) if gate else np.ones(len(score), dtype=bool)
            flags = ((score >= 0.5) & accepted).astype(float)
            alerts = episodes(block["decisions"], flags, 1.0)
        else:
            accepted = np.empty(0, dtype=bool)
            alerts = []
        result = event_summary(block["reference"], alerts, block["exposure_seconds"])
        row = {"reference_episodes": len(block["reference"]),
               "event_tp": result["event_tp"], "event_fn": result["event_fn"],
               "event_fp": result["event_fp"], "alerts": len(alerts),
               "exposure_seconds": block["exposure_seconds"],
               "windows": len(accepted),
               "abstained_windows": int((~accepted).sum())}
        subject = by_subject.setdefault(str(block["subject"]), {k: 0 for k in totals})
        for key, value in row.items():
            totals[key] += value
            subject[key] += value
    totals["event_sensitivity"] = (totals["event_tp"] / totals["reference_episodes"]
                                    if totals["reference_episodes"] else None)
    totals["false_alerts_per_hour"] = (3600 * totals["event_fp"] / totals["exposure_seconds"]
                                       if totals["exposure_seconds"] else None)
    totals["window_abstention_fraction"] = (totals["abstained_windows"] / totals["windows"]
                                            if totals["windows"] else None)
    return {"aggregate": totals, "by_subject": by_subject}


def run(daphnet, target_df):
    source_x, source_y, _ = daphnet
    source = orientation_invariant(source_x)
    model = new_model().fit(source, source_y)
    blocks = target_blocks(target_df)
    policies = {"no_gate": summarize_policy(blocks, model)}
    for fraction in (0.8, 0.9, 0.95):
        gate = SourceDistanceGate(fraction).fit(source)
        policies[f"source_retention_{fraction}"] = summarize_policy(blocks, model, gate)
    return {"status": "post-hoc retrospective FoG-STAR event replay",
            "note": "End-of-window alerts only; abstentions emit no alert; no event tolerance or alert merging",
            "policies": policies}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daphnet-dir", type=Path, required=True)
    p.add_argument("--fogstar-sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = run(load_daphnet(args.daphnet_dir), pd.read_csv(args.fogstar_sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "cross_dataset_events.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
