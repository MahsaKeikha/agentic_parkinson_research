"""Event-level constrained threshold search with explicit infeasibility.

This script tests a research hypothesis; its validation constraints are not
clinical specifications or statistical guarantees. No test labels select the
threshold. A no-solution result is kept as no-solution, not overridden.
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


THRESHOLDS = tuple(np.round(np.linspace(0.05, 0.95, 19), 4))


def choose_feasible(rows, minimum_sensitivity, maximum_false_alerts_per_hour):
    """Choose best feasible validation setting; return None if none qualifies."""
    feasible = [r for r in rows if r["sensitivity"] is not None
                and r["sensitivity"] >= minimum_sensitivity
                and r["false_alerts_per_hour"] <= maximum_false_alerts_per_hour]
    if not feasible:
        return None
    return min(feasible, key=lambda r: (r["false_alerts_per_hour"],
                                         -r["sensitivity"], -r["threshold"]))


def run(df, minimum_sensitivity=0.70, maximum_false_alerts_per_hour=30.0):
    x, y, groups, times, bids, blocks = prepare(df)
    reports = []
    for fold, (development, test) in enumerate(GroupKFold(n_splits=5).split(x, y, groups=groups), 1):
        split = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=fold * 119)
        fit_local, validation_local = next(split.split(x[development], y[development], groups[development]))
        fit_idx, validation = development[fit_local], development[validation_local]
        if len(np.unique(y[fit_idx])) != 2:
            reports.append({"fold": fold, "status": "infeasible: one training class"})
            continue
        model = make_pipeline(
            SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True),
            HistGradientBoostingClassifier(max_iter=120, learning_rate=0.05, random_state=17))
        model.fit(x[fit_idx], y[fit_idx])
        scores = np.full(len(y), np.nan)
        scores[validation] = model.predict_proba(x[validation])[:, 1]
        scores[test] = model.predict_proba(x[test])[:, 1]
        settings = []
        for threshold in THRESHOLDS:
            metrics = evaluate_fold(validation, scores, times, bids, blocks,
                                    threshold=float(threshold), merge_gap_seconds=2.0)
            settings.append({"threshold": float(threshold), **metrics})
        best = choose_feasible(settings, minimum_sensitivity, maximum_false_alerts_per_hour)
        # Held-out comparison at 0.5 is descriptive only; test outcomes never
        # modify validation thresholds or declared feasibility.
        baseline_test = evaluate_fold(test, scores, times, bids, blocks,
                                      threshold=0.5, merge_gap_seconds=2.0)
        entry = {"fold": fold, "train_subjects": [int(s) for s in np.unique(groups[fit_idx])],
                 "validation_subjects": [int(s) for s in np.unique(groups[validation])],
                 "test_subjects": [int(s) for s in np.unique(groups[test])],
                 "validation_episode_count": int(settings[0]["reference_episodes"]),
                 "validation_candidate_count": len(settings),
                 "baseline_test_0_5": baseline_test}
        if best is None:
            entry.update(status="infeasible: no validation operating point satisfies both constraints",
                         selected_threshold=None, selected_test=None)
        else:
            entry.update(status="validation feasible; test outcome not guaranteed",
                         selected_threshold=best["threshold"], validation_selected=best,
                         selected_test=evaluate_fold(test, scores, times, bids, blocks,
                                                     threshold=best["threshold"], merge_gap_seconds=2.0))
        reports.append(entry)
    return {"status": "exploratory event-constrained threshold selection",
            "minimum_validation_event_sensitivity": minimum_sensitivity,
            "maximum_validation_false_alerts_per_hour": maximum_false_alerts_per_hour,
            "candidate_thresholds": list(THRESHOLDS),
            "folds": reports}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = run(pd.read_csv(args.sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / "constrained_event_pilot.json"
    target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {target}")


if __name__ == "__main__":
    main()
