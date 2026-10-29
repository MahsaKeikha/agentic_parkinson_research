"""Participant-held-out FoG-STAR event-level baseline.

Experimental software, not medical monitoring. Window alerts occur at the END
of a 2-second window, so this code does not use future sensor measurements for
the reported alert onset. Raw reference episodes retain sample-level timing.
"""

import argparse
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline

from events import episodes, event_summary


def prepare(df, hz=60, window_seconds=2, stride_seconds=1):
    names = [c for c in df if "_acc_" in c or "_gyro_" in c]
    required = {"subjectID", "sessionID", "taskID", "timestamp", "fog"}
    if not required.issubset(df.columns) or not names:
        raise ValueError("FoG-STAR columns missing")
    times = df["timestamp"].to_numpy(dtype=float)
    keys = df[["subjectID", "sessionID", "taskID"]]
    steps = np.diff(times)
    positive = steps[(steps > 0) & np.isfinite(steps)]
    if len(positive) == 0:
        raise ValueError("No positive timestamp differences")
    to_seconds = 1 if np.median(positive) < 1 else 0.001
    period = 1 / hz
    change = keys.ne(keys.shift()).any(axis=1).to_numpy()
    break_at = np.r_[True, (steps <= 0) | (steps * to_seconds > 1.5 * period)] | change
    edges = np.r_[np.flatnonzero(break_at), len(df)]
    size, hop = int(window_seconds * hz), int(stride_seconds * hz)
    features, labels, subjects, window_times, block_index = [], [], [], [], []
    blocks = []
    for begin, end in zip(edges[:-1], edges[1:]):
        if end - begin < size:
            continue
        segment = df.iloc[begin:end]
        sid = int(segment["subjectID"].iloc[0])
        seconds = times[begin:end] * to_seconds
        truth = segment["fog"].to_numpy(dtype=float)
        raw_events = episodes(seconds, truth, period)
        true_count = int(np.isin(truth, [0, 1]).sum())
        bid = len(blocks)
        blocks.append({"subject": sid, "reference": raw_events,
                       "exposure_seconds": true_count / hz})
        values = segment[names].to_numpy(dtype=float)
        for start in range(0, len(segment) - size + 1, hop):
            ys = truth[start:start + size]
            valid = np.isin(ys, [0, 1])
            if valid.mean() < 0.9:
                continue
            sample = values[start:start + size]
            with np.errstate(invalid="ignore"), warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                row = np.r_[np.nanmean(sample, axis=0), np.nanstd(sample, axis=0),
                            np.sqrt(np.nanmean(sample ** 2, axis=0)),
                            np.isfinite(sample).mean(axis=0)]
            features.append(row)
            labels.append(int(ys[valid].mean() >= 0.5))
            subjects.append(sid)
            # A prediction is issued only when the entire window is available.
            window_times.append(float(seconds[start + size - 1] + period))
            block_index.append(bid)
    if not features:
        raise ValueError("No eligible windows")
    return (np.asarray(features), np.asarray(labels), np.asarray(subjects),
            np.asarray(window_times), np.asarray(block_index), blocks)


def evaluate_fold(test_indices, probabilities, times, block_index, blocks, threshold=0.5, hop_seconds=1):
    result = {"reference_episodes": 0, "alerts": 0, "event_tp": 0, "event_fn": 0,
              "event_fp": 0, "exposure_seconds": 0.0, "latencies": []}
    for bid in np.unique(block_index[test_indices]):
        local = test_indices[block_index[test_indices] == bid]
        ordered = local[np.argsort(times[local])]
        alert_events = episodes(times[ordered],
                                (probabilities[ordered] >= threshold).astype(float),
                                sample_period=hop_seconds)
        annotated = blocks[int(bid)]
        r = event_summary(annotated["reference"], alert_events,
                          recorded_seconds=annotated["exposure_seconds"])
        result["reference_episodes"] += len(annotated["reference"])
        result["alerts"] += len(alert_events)
        result["event_tp"] += r["event_tp"]
        result["event_fn"] += r["event_fn"]
        result["event_fp"] += r["event_fp"]
        result["exposure_seconds"] += annotated["exposure_seconds"]
        result["latencies"].extend(r["latency_seconds"])
    result["sensitivity"] = (result["event_tp"] / result["reference_episodes"]
                              if result["reference_episodes"] else None)
    result["precision"] = result["event_tp"] / result["alerts"] if result["alerts"] else None
    result["false_alerts_per_hour"] = 3600 * result["event_fp"] / result["exposure_seconds"]
    result["mean_detected_latency_seconds"] = (float(np.mean(result["latencies"]))
                                                if result["latencies"] else None)
    return result


def run(df):
    x, y, group, times, bids, blocks = prepare(df)
    scores = np.full(len(y), np.nan)
    folds = []
    for fold, (training, test) in enumerate(GroupKFold(n_splits=5).split(x, y, groups=group), 1):
        if len(np.unique(y[training])) < 2:
            folds.append({"fold": fold, "skipped": "single-class training fold"})
            continue
        model = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True),
            HistGradientBoostingClassifier(max_iter=120, learning_rate=0.05, random_state=17))
        model.fit(x[training], y[training])
        scores[test] = model.predict_proba(x[test])[:, 1]
        r = evaluate_fold(test, scores, times, bids, blocks)
        folds.append({"fold": fold, "subjects": [int(n) for n in np.unique(group[test])], **r})
    return {"status": "exploratory fixed-threshold event baseline; source-order segmentation",
            "window_count": len(y), "participant_count": len(np.unique(group)), "folds": folds}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = run(pd.read_csv(args.sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    filename = args.out / "event_baseline_cv.json"
    filename.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {filename}")


if __name__ == "__main__":
    main()
