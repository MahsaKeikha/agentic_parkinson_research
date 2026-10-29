"""Exploratory quality-aware supervisory policy for FoG event detection.

Development subjects choose an alert threshold; held-out subjects never enter
threshold selection. This is a research ablation, not clinical risk control.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.pipeline import make_pipeline

from event_baseline import evaluate_fold, prepare


def choose_alert_threshold(prob, truth, target_recall=0.80):
    """Highest threshold attaining required recall on validation positives.

    A finite set of candidate thresholds is used. There is no population-level
    sensitivity guarantee and a single-positive calibration set is unstable.
    """
    prob = np.asarray(prob)
    truth = np.asarray(truth)
    if not np.any(truth == 1):
        return None
    candidates = np.unique(np.r_[0, prob, 1])
    feasible = [t for t in candidates if np.mean(prob[truth == 1] >= t) >= target_recall]
    return float(max(feasible)) if feasible else None


def apply_policy(prob, quality, high, uncertainty_width=0.1, minimum_quality=0.75):
    """Actions 1 alert, 0 no alert, -1 abstain.

    Poor quality causes abstention. Uncertain probabilities in the pre-alert
    band also cause abstention; scores above high cause alerts.
    """
    p = np.asarray(prob)
    q = np.asarray(quality)
    if high is None or len(p) != len(q):
        raise ValueError("Missing threshold or shape mismatch")
    low = max(0.0, high - uncertainty_width)
    action = np.where(p >= high, 1, np.where(p <= low, 0, -1)).astype(int)
    action[q < minimum_quality] = -1
    return action


def run(df, target_recall=0.80):
    x, y, subjects, times, bids, blocks = prepare(df)
    # The final quarter of the feature vector contains per-channel
    # nonmissing fractions, all computed before imputation.
    quality = np.mean(x[:, 3 * (x.shape[1] // 4):], axis=1)
    reports = []
    for fold, (development, test) in enumerate(GroupKFold(n_splits=5).split(x, y, groups=subjects), 1):
        splitter = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=fold * 119)
        fitting_rel, validation_rel = next(splitter.split(x[development], y[development], subjects[development]))
        fitting, validation = development[fitting_rel], development[validation_rel]
        if len(np.unique(y[fitting])) < 2 or not np.any(y[validation] == 1):
            reports.append({"fold": fold, "skipped": "insufficient positive training/validation cases"})
            continue
        model = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True),
            HistGradientBoostingClassifier(max_iter=120, learning_rate=0.05, random_state=17))
        model.fit(x[fitting], y[fitting])
        p_val = model.predict_proba(x[validation])[:, 1]
        high = choose_alert_threshold(p_val, y[validation], target_recall)
        if high is None:
            reports.append({"fold": fold, "skipped": "no valid validation threshold"})
            continue
        p_test = model.predict_proba(x[test])[:, 1]
        actions = apply_policy(p_test, quality[test], high)
        # Only positive actions generate event alerts; abstentions are not
        # silently reported as confident negatives in decision-coverage data.
        baseline = np.full(len(y), np.nan)
        baseline[test] = p_test
        supervisor_alerts = np.full(len(y), np.nan)
        supervisor_alerts[test] = (actions == 1).astype(float)
        raw = evaluate_fold(test, baseline, times, bids, blocks, merge_gap_seconds=2.0)
        supervised = evaluate_fold(test, supervisor_alerts, times, bids, blocks,
                                   threshold=0.5, merge_gap_seconds=2.0)
        reports.append({
            "fold": fold,
            "test_subjects": [int(s) for s in np.unique(subjects[test])],
            "train_subjects": int(len(np.unique(subjects[fitting]))),
            "validation_subjects": int(len(np.unique(subjects[validation]))),
            "validation_positive_windows": int(y[validation].sum()),
            "selected_threshold": high,
            "heldout_action_coverage": float(np.mean(actions != -1)),
            "heldout_abstention": float(np.mean(actions == -1)),
            "heldout_positive_retention": float(np.mean(actions[y[test] == 1] != -1))
            if np.any(y[test] == 1) else None,
            "baseline_merged_2s": raw,
            "supervisor_merged_2s": supervised,
        })
    return {"status": "exploratory validation-tuned policy; no risk or safety guarantee",
            "target_validation_window_recall": target_recall,
            "folds": reports}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = run(pd.read_csv(args.sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "supervisor_pilot.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
