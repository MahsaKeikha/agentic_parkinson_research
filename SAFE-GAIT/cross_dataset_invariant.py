"""Exploratory orientation-invariant follow-up to cross_dataset.py.

The prior FoG-STAR evaluation has already been inspected. Accordingly this
follow-up is post-hoc and cannot be described as independent external testing.
No target outcomes are used for training, thresholds, or feature scaling.
"""

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.model_selection import GroupKFold

from cross_dataset import load_daphnet, load_fogstar, metrics, new_model


MAGNITUDE_INDICES = (9, 10, 11)
MAGNITUDE_NAMES = ("magnitude_mean_g", "magnitude_sd_g", "magnitude_difference_rms_g")


def orientation_invariant(x):
    """Select features invariant to any fixed orthogonal axis rotation."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or x.shape[1] != 12:
        raise ValueError("Expected the 12 features produced by three_axis_features")
    return x[:, MAGNITUDE_INDICES]


def label_free_shift(source, target):
    """Descriptive standardized mean differences, never used in fitting."""
    s = orientation_invariant(source)
    t = orientation_invariant(target)
    pooled_sd = np.sqrt((np.var(s, axis=0) + np.var(t, axis=0)) / 2)
    standardized = np.divide(np.mean(t, axis=0) - np.mean(s, axis=0), pooled_sd,
                             out=np.full(len(MAGNITUDE_NAMES), np.nan), where=pooled_sd > 0)
    return [{"feature": name, "source_mean": float(np.mean(s[:, i])),
             "target_mean": float(np.mean(t[:, i])),
             "standardized_mean_difference": float(standardized[i])}
            for i, name in enumerate(MAGNITUDE_NAMES)]


def compare(daphnet, fogstar):
    xs, ys, gs = daphnet
    xt, yt, gt = fogstar
    variants = {"axis_and_magnitude_12": (xs, xt),
                "magnitude_only_3": (orientation_invariant(xs), orientation_invariant(xt))}
    reports = {}
    for name, (source, target) in variants.items():
        source_cv = []
        for fold, (train, test) in enumerate(GroupKFold(n_splits=5).split(source, ys, gs), 1):
            model = new_model()
            model.fit(source[train], ys[train])
            source_cv.append({"fold": fold, "test_subjects": list(map(int, np.unique(gs[test]))),
                              **metrics(ys[test], model.predict_proba(source[test])[:, 1])})
        model = new_model()
        model.fit(source, ys)
        scores = model.predict_proba(target)[:, 1]
        reports[name] = {"source_group_cv": source_cv,
                         "target_aggregate": metrics(yt, scores),
                         "target_per_subject": [
                             {"subject": int(s), **metrics(yt[gt == s], scores[gt == s])}
                             for s in np.unique(gt)]}
    return {"status": "exploratory post-hoc follow-up; not independent validation",
            "policy": "fixed source-only model and 0.5 threshold; target labels evaluation only",
            "source_participants": int(len(np.unique(gs))),
            "target_participants": int(len(np.unique(gt))),
            "source_windows": int(len(ys)), "target_windows": int(len(yt)),
            "label_free_magnitude_shift": label_free_shift(xs, xt),
            "variants": reports}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--daphnet-dir", required=True, type=Path)
    parser.add_argument("--fogstar-sensor-data", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    report = compare(load_daphnet(args.daphnet_dir), load_fogstar(args.fogstar_sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "cross_dataset_invariant.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
