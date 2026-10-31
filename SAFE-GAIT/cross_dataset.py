"""Accelerometer-only cross-dataset shift stress test: Daphnet -> FoG-STAR.

Not independent clinical validation. No target labels are used for feature
normalization, classifier fitting or operating-threshold selection.
"""

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, roc_auc_score, recall_score, precision_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline


def three_axis_features(values):
    """Orientation-sensitive and orientation-reduced inertial features."""
    values = np.asarray(values, dtype=float)
    magnitude = np.linalg.norm(values, axis=1)
    differences = np.diff(magnitude)
    return np.r_[np.mean(values, axis=0), np.std(values, axis=0),
                 np.sqrt(np.mean(values ** 2, axis=0)),
                 np.mean(magnitude), np.std(magnitude),
                 np.sqrt(np.mean(differences ** 2)) if len(differences) else 0.0]


def windows_from_run(time_seconds, acceleration_g, labels, subject, hz):
    size, hop = int(round(2 * hz)), int(round(hz))
    features, outcomes, groups = [], [], []
    for start in range(0, len(labels) - size + 1, hop):
        y = labels[start:start + size]
        valid = np.isin(y, [0, 1])
        if valid.mean() < 0.9:
            continue
        x = acceleration_g[start:start + size]
        if not np.isfinite(x).all():
            continue
        features.append(three_axis_features(x))
        outcomes.append(int(y[valid].mean() >= 0.5))
        groups.append(subject)
    return features, outcomes, groups


def split_runs(t, hz):
    steps = np.diff(t)
    starts = np.r_[0, np.flatnonzero((steps <= 0) | (steps > 1.5 / hz)) + 1]
    return zip(starts, np.r_[starts[1:], len(t)])


def load_daphnet(directory):
    features, labels, groups = [], [], []
    paths = sorted(directory.glob("S??R??.txt"))
    if not paths:
        raise FileNotFoundError("Daphnet recording files not found")
    for path in paths:
        sid = int(re.match(r"S(\d+)R", path.name).group(1))
        data = np.loadtxt(path)
        t = data[:, 0] / 1000
        hz = round(1 / np.median(np.diff(t)[np.diff(t) > 0]))
        # Daphnet columns 8-10 (one-based): trunk XYZ acceleration in mg.
        x = data[:, 7:10] / 1000
        # Annotation 0 is outside experiment; 1=no freeze; 2=freeze.
        y = np.where(data[:, 10] == 2, 1.0, np.where(data[:, 10] == 1, 0.0, np.nan))
        for begin, end in split_runs(t, hz):
            a, b, c = windows_from_run(t[begin:end], x[begin:end], y[begin:end], sid, hz)
            features.extend(a); labels.extend(b); groups.extend(c)
    return np.asarray(features), np.asarray(labels), np.asarray(groups)


def load_fogstar(file, timestamp_unit='s'):
    if timestamp_unit not in ('s', 'ms'):
        raise ValueError('timestamp_unit must be explicitly s or ms')
    d = pd.read_csv(file)
    cols = ["back_acc_x", "back_acc_y", "back_acc_z"]
    features, labels, groups = [], [], []
    keys = d[["subjectID", "sessionID", "taskID"]]
    times = d["timestamp"].to_numpy(dtype=float) * (0.001 if timestamp_unit == "ms" else 1.0)
    if not np.isfinite(times).all():
        raise ValueError("Nonfinite target timestamps")
    positive_steps = np.diff(times)
    positive_steps = positive_steps[positive_steps > 0]
    if not len(positive_steps) or not 0.01 <= np.median(positive_steps) <= 0.025:
        raise ValueError("Timestamp unit incompatible with nominal 60 Hz")
    steps = np.diff(times)
    change = keys.ne(keys.shift()).any(axis=1).to_numpy()
    starts = np.flatnonzero(np.r_[True, (steps <= 0) | (steps > 1.5 / 60)] | change)
    for begin, end in zip(starts, np.r_[starts[1:], len(d)]):
        if end - begin < 120:
            continue
        block = d.iloc[begin:end]
        x = block[cols].to_numpy(dtype=float)
        y = block["fog"].to_numpy(dtype=float)
        sid = int(block["subjectID"].iloc[0])
        a, b, c = windows_from_run(times[begin:end], x, y, sid, 60)
        features.extend(a); labels.extend(b); groups.extend(c)
    return np.asarray(features), np.asarray(labels), np.asarray(groups)


def metrics(y, p):
    pred = p >= 0.5
    return {"windows": int(len(y)), "positives": int(y.sum()),
            "auroc": float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None,
            "auprc": float(average_precision_score(y, p)) if y.sum() else None,
            "sensitivity": float(recall_score(y, pred, zero_division=0)),
            "precision": float(precision_score(y, pred, zero_division=0))}


def new_model():
    return make_pipeline(SimpleImputer(strategy="median"),
                         HistGradientBoostingClassifier(max_iter=120, learning_rate=0.05, random_state=17))


def run(daphnet, fogstar):
    xs, ys, gs = daphnet
    xt, yt, gt = fogstar
    source_cv = []
    for fold, (training, test) in enumerate(GroupKFold(n_splits=5).split(xs, ys, gs), 1):
        model = new_model()
        model.fit(xs[training], ys[training])
        source_cv.append({"fold": fold, "test_subjects": list(map(int, np.unique(gs[test]))),
                          **metrics(ys[test], model.predict_proba(xs[test])[:, 1])})
    model = new_model()
    model.fit(xs, ys)
    target_pred = model.predict_proba(xt)[:, 1]
    target_by_subject = [{"subject": int(s), **metrics(yt[gt == s], target_pred[gt == s])}
                         for s in np.unique(gt)]
    return {"status": "cross-dataset shift stress test, source-only training",
            "source": "Daphnet trunk 3-axis accelerometer (mg to g)",
            "target": "FoG-STAR back 3-axis accelerometer (g)",
            "source_participants": int(len(np.unique(gs))),
            "target_participants": int(len(np.unique(gt))),
            "source_group_cv": source_cv,
            "target_aggregate": metrics(yt, target_pred),
            "target_per_subject": target_by_subject}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daphnet-dir", type=Path, required=True)
    p.add_argument("--fogstar-sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    p.add_argument("--timestamp-unit", choices=["s","ms"], default="s")
    args = p.parse_args()
    report = run(load_daphnet(args.daphnet_dir), load_fogstar(args.fogstar_sensor_data, timestamp_unit=args.timestamp_unit))
    args.out.mkdir(parents=True, exist_ok=True)
    destination = args.out / "cross_dataset_shift.json"
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {destination}")


if __name__ == "__main__":
    main()
