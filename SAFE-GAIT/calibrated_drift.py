"""Exploratory source-group-calibrated model-score drift warning.

Five Daphnet participant-held-out fold distances set an empirical threshold.
No FoG-STAR target labels or scores are used to choose the threshold. Only
five folds make 95th-percentile calibration highly uncertain, and all work
is post-hoc after previous inspection of FoG-STAR labels.
"""

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.model_selection import GroupKFold

from cross_dataset import load_daphnet, load_fogstar, new_model
from cross_dataset_invariant import orientation_invariant
from score_drift import ecdf_distance, distribution


def source_calibration(x, labels, groups):
    """Source-only grouped held-out shift distances and fixed percentile."""
    x = np.asarray(x, dtype=float)
    labels = np.asarray(labels, dtype=int)
    groups = np.asarray(groups)
    records = []
    for fold, (train, holdout) in enumerate(GroupKFold(n_splits=5).split(x, labels, groups), 1):
        model = new_model().fit(x[train], labels[train])
        training_scores = model.predict_proba(x[train])[:, 1]
        test_scores = model.predict_proba(x[holdout])[:, 1]
        records.append({"fold": fold,
                        "held_out_subjects": list(map(int, np.unique(groups[holdout]))),
                        "score_ecdf_distance": ecdf_distance(training_scores, test_scores)})
    threshold = float(np.quantile([r["score_ecdf_distance"] for r in records], 0.95))
    return records, threshold


def audit(source_data, target_data):
    xs, ys, gs = source_data
    xt, _, gt = target_data
    source, target = orientation_invariant(xs), orientation_invariant(xt)
    folds, cutoff = source_calibration(source, ys, gs)
    model = new_model().fit(source, ys)
    reference = model.predict_proba(source)[:, 1]
    target_scores = model.predict_proba(target)[:, 1]
    target_subjects = []
    for sid in np.unique(gt):
        scores = target_scores[gt == sid]
        distance = ecdf_distance(reference, scores)
        target_subjects.append({"subject": int(sid),
                                "windows": int(len(scores)),
                                "ecdf_distance": distance,
                                "warning": bool(distance > cutoff),
                                "mean_score": float(np.mean(scores))})
    return {"status": "exploratory source-only fold-calibrated warning; no clinical validity",
            "source_calibration_folds": folds, "cutoff_95th_percentile": cutoff,
            "source_score_summary": distribution(reference),
            "target_subjects": target_subjects,
            "warnings": sum(item["warning"] for item in target_subjects),
            "total_target_subjects": len(target_subjects),
            "limitations": "Only 5 correlated source fold distances; source reference scores in-sample; target previously inspected; warning is not calibrated at patient level"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daphnet-dir", type=Path, required=True)
    p.add_argument("--fogstar-sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = audit(load_daphnet(args.daphnet_dir), load_fogstar(args.fogstar_sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    dest = args.out / "calibrated_drift.json"
    dest.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {dest}")


if __name__ == "__main__":
    main()
