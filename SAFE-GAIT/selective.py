"""Group-separated calibrated selective FoG baseline.

This is an experimental selective-prediction benchmark, not a validated
clinical safety system. It fits a model on training participants, calibrates
on disjoint calibration participants, and evaluates on held-out participants.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.pipeline import make_pipeline

from baseline import extract_windows


def logit(probs):
    safe = np.clip(np.asarray(probs), 1e-5, 1 - 1e-5)
    return np.log(safe / (1 - safe)).reshape(-1, 1)


def fit_sigmoid(raw_cal, y_cal):
    """Platt-style calibration, fit on disjoint participants only."""
    if len(np.unique(y_cal)) != 2:
        return None
    return LogisticRegression(C=1.0, solver="lbfgs", random_state=17).fit(logit(raw_cal), y_cal)


def calibrated(raw, calibrator):
    return calibrator.predict_proba(logit(raw))[:, 1] if calibrator is not None else raw


def nonconformity(probs):
    """Larger value means closer to the uncertain 0.5 boundary."""
    return np.minimum(probs, 1 - probs)


def threshold_for_coverage(cal_scores, target_coverage):
    """Threshold selected using calibration participants, never test labels."""
    if not 0 < target_coverage <= 1:
        raise ValueError("coverage target must lie in (0, 1]")
    if target_coverage == 1:
        return float("inf")
    return float(np.quantile(cal_scores, target_coverage, method="inverted_cdf"))


def policy_metrics(labels, probabilities, accept):
    predictions = probabilities >= 0.5
    n = int(np.sum(accept))
    if not n:
        return {"coverage": 0.0, "accepted_windows": 0, "accepted_error": None,
                "accepted_sensitivity": None, "accepted_specificity": None,
                "positive_retention": None, "negative_retention": None}
    yt, yp = labels[accept], predictions[accept]
    pos = int(yt.sum())
    neg = int(len(yt) - pos)
    return {
        "coverage": float(np.mean(accept)),
        "accepted_windows": n,
        "accepted_error": float(np.mean(yp != yt)),
        "accepted_sensitivity": float(np.sum(yp & (yt == 1)) / pos) if pos else None,
        "accepted_specificity": float(np.sum(~yp & (yt == 0)) / neg) if neg else None,
        # Retention must be reported separately from sensitivity conditional
        # on acceptance. A model can game accepted risk by rejecting positives.
        "positive_retention": float(np.sum(accept & (labels == 1)) / np.sum(labels == 1))
        if np.sum(labels == 1) else None,
        "negative_retention": float(np.sum(accept & (labels == 0)) / np.sum(labels == 0))
        if np.sum(labels == 0) else None,
    }


def run(x, y, groups, coverage_targets=(0.6, 0.8, 0.95), folds=5):
    reports = []
    for fold, (development, test) in enumerate(GroupKFold(n_splits=folds).split(x, y, groups), 1):
        split = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=fold * 119)
        model_relative, calib_relative = next(split.split(x[development], y[development], groups[development]))
        fit_idx, cal_idx = development[model_relative], development[calib_relative]
        assert not (set(groups[fit_idx]) & set(groups[cal_idx]))
        assert not (set(groups[test]) & set(groups[development]))
        if len(np.unique(y[fit_idx])) != 2 or len(np.unique(y[cal_idx])) != 2:
            reports.append({"fold": fold, "skipped": "training or calibration split has one class"})
            continue
        model = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True),
            HistGradientBoostingClassifier(max_iter=120, learning_rate=0.05, random_state=17),
        )
        model.fit(x[fit_idx], y[fit_idx])
        raw_cal = model.predict_proba(x[cal_idx])[:, 1]
        raw_test = model.predict_proba(x[test])[:, 1]
        calibrator = fit_sigmoid(raw_cal, y[cal_idx])
        p_cal = calibrated(raw_cal, calibrator)
        p_test = calibrated(raw_test, calibrator)
        entry = {
            "fold": fold,
            "fit_subjects": int(len(np.unique(groups[fit_idx]))),
            "calibration_subjects": int(len(np.unique(groups[cal_idx]))),
            "test_subjects": int(len(np.unique(groups[test]))),
            "test_windows": int(len(test)),
            "test_positive_windows": int(y[test].sum()),
            "fit_positive_prevalence": float(y[fit_idx].mean()),
            "calibration_positive_prevalence": float(y[cal_idx].mean()),
            "test_positive_prevalence": float(y[test].mean()),
            "calibrator_slope": float(calibrator.coef_[0, 0]) if calibrator is not None else None,
            "calibrator_intercept": float(calibrator.intercept_[0]) if calibrator is not None else None,
            "brier_raw": float(brier_score_loss(y[test], raw_test)),
            "brier_calibrated": float(brier_score_loss(y[test], p_test)),
            "auroc": float(roc_auc_score(y[test], p_test)) if len(np.unique(y[test])) == 2 else None,
            "all_decisions": policy_metrics(y[test], p_test, np.ones(len(test), dtype=bool)),
            "selective": [],
            "raw_selective": [],
        }
        for target in coverage_targets:
            cutoff = threshold_for_coverage(nonconformity(p_cal), target)
            accepted = nonconformity(p_test) <= cutoff
            entry["selective"].append({"target_coverage": target, "calibration_cutoff": cutoff,
                                        **policy_metrics(y[test], p_test, accepted)})
            # Compare raw and calibrated models on exactly the same held-out
            # participants, each with a threshold chosen on calibration subjects.
            raw_cutoff = threshold_for_coverage(nonconformity(raw_cal), target)
            raw_accepted = nonconformity(raw_test) <= raw_cutoff
            entry["raw_selective"].append({"target_coverage": target,
                                            "calibration_cutoff": raw_cutoff,
                                            **policy_metrics(y[test], raw_test, raw_accepted)})
        reports.append(entry)
    return {"status": "exploratory: sigmoid-calibrated selective prediction, no risk guarantee",
            "folds": reports}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sensor-data", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    x, y, groups, _ = extract_windows(pd.read_csv(args.sensor_data))
    report = run(x, y, groups)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "selective_grouped_cv.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
