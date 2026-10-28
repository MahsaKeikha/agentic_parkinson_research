"""SAFE-GAIT reproducible first-pass FoG-STAR dataset audit and grouped baseline.

Usage:
  python safe_gait_baseline.py --sensor-data sensor_data.csv --out results

Requires numpy, pandas, scikit-learn. Research prototype, not medical software.
No participant-level test data is used to fit preprocessing or models.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    average_precision_score, balanced_accuracy_score, brier_score_loss,
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline


def extract_windows(df, sample_hz=60, seconds=2, overlap=0.5):
    """Windows do not cross subject/session/task boundaries or timestamp gaps."""
    if not 0 <= overlap < 1:
        raise ValueError("overlap must be between 0 and 1")
    sensor_cols = [c for c in df.columns if ("_acc_" in c or "_gyro_" in c)]
    required = {"subjectID", "sessionID", "taskID", "timestamp", "fog"}
    missing = required.difference(df.columns)
    if missing or not sensor_cols:
        raise ValueError(f"Missing required columns: {sorted(missing)}; sensors={len(sensor_cols)}")
    win = int(seconds * sample_hz)
    hop = max(1, int(win * (1 - overlap)))
    feature_rows, labels, groups = [], [], []
    for (sid, sess, task), block in df.groupby(["subjectID", "sessionID", "taskID"], sort=False):
        block = block.sort_values("timestamp")
        # Break runs at timestamps differing materially from expected period;
        # timestamp is documented in milliseconds, 60 Hz.
        diffs = block["timestamp"].diff().fillna(1000 / sample_hz)
        run_ids = (diffs.le(0) | diffs.gt(1.75 * 1000 / sample_hz)).cumsum()
        for _, run in block.groupby(run_ids, sort=False):
            x = run[sensor_cols].to_numpy(dtype=float)
            y = pd.to_numeric(run["fog"], errors="coerce").to_numpy()
            for start in range(0, len(run) - win + 1, hop):
                segment = x[start : start + win]
                target = y[start : start + win]
                valid = np.isin(target, [0, 1])
                if valid.mean() < 0.9:
                    continue
                positive = int(np.mean(target[valid]) >= 0.5)
                with np.errstate(invalid="ignore"):
                    means = np.nanmean(segment, axis=0)
                    stds = np.nanstd(segment, axis=0)
                    rms = np.sqrt(np.nanmean(np.square(segment), axis=0))
                finite_frac = np.isfinite(segment).mean(axis=0)
                row = np.r_[means, stds, rms, finite_frac]
                feature_rows.append(row)
                labels.append(positive)
                groups.append(sid)
    if not labels:
        raise RuntimeError("No eligible windows: verify sampling frequency, timestamps, and labels")
    return np.asarray(feature_rows), np.asarray(labels), np.asarray(groups), sensor_cols


def evaluate(y, prob):
    prediction = (prob >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    out = {
        "n_windows": int(len(y)), "n_positive": int(y.sum()),
        "precision": float(precision_score(y, prediction, zero_division=0)),
        "sensitivity": float(recall_score(y, prediction, zero_division=0)),
        "specificity": float(tn / (tn + fp)) if tn + fp else None,
        "f1": float(f1_score(y, prediction, zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y, prediction)),
        "brier": float(brier_score_loss(y, prob)),
        "auprc": float(average_precision_score(y, prob)) if y.sum() else None,
        "auroc": float(roc_auc_score(y, prob)) if len(np.unique(y)) == 2 else None,
    }
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    p.add_argument("--folds", type=int, default=5)
    args = p.parse_args()
    data = pd.read_csv(args.sensor_data)
    x, y, subjects, cols = extract_windows(data)
    unique_subjects = np.unique(subjects)
    if len(unique_subjects) < 2:
        raise ValueError("At least two subjects required for grouped testing")
    splitter = GroupKFold(n_splits=min(args.folds, len(unique_subjects)))
    reports = []
    for fold, (train, test) in enumerate(splitter.split(x, y, groups=subjects), start=1):
        if len(np.unique(y[train])) != 2:
            reports.append({"fold": fold, "skipped": "one class in training"})
            continue
        model = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True),
            HistGradientBoostingClassifier(max_iter=120, learning_rate=0.05, random_state=17),
        )
        model.fit(x[train], y[train])
        prob = model.predict_proba(x[test])[:, 1]
        reports.append({"fold": fold, "n_train_subjects": len(np.unique(subjects[train])),
                        "n_test_subjects": len(np.unique(subjects[test])),
                        "metrics": evaluate(y[test], prob)})
    args.out.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "baseline only; uncalibrated; not event-level or externally validated",
        "total_windows": len(y), "participants": len(unique_subjects),
        "sensor_channels": cols, "positive_window_fraction": float(y.mean()),
        "folds": reports,
    }
    dest = args.out / "baseline_grouped_cv.json"
    dest.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {dest}")


if __name__ == "__main__":
    main()
