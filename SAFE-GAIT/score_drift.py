"""Label-free prediction-score drift audit for Daphnet to FoG-STAR.

The source scores below are in-sample model scores. Consequently their
comparison to target scores is descriptive, not a calibrated drift test.
The target was previously inspected, so this is post-hoc exploratory work.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from cross_dataset import load_daphnet, load_fogstar, new_model
from cross_dataset_invariant import orientation_invariant


def ecdf_distance(left, right):
    """Two-sample empirical CDF sup distance; no iid p-value reported."""
    a, b = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    if len(a) == 0 or len(b) == 0 or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Nonempty finite score arrays required")
    grid = np.sort(np.unique(np.r_[a, b]))
    left_values = np.searchsorted(np.sort(a), grid, side="right") / len(a)
    right_values = np.searchsorted(np.sort(b), grid, side="right") / len(b)
    return float(np.max(np.abs(left_values - right_values)))


def distribution(scores):
    values = np.asarray(scores, dtype=float)
    return {"n_windows": int(len(values)), "mean_score": float(np.mean(values)),
            "fraction_above_0_5": float(np.mean(values >= 0.5)),
            "quantile_10": float(np.quantile(values, 0.1)),
            "median": float(np.median(values)),
            "quantile_90": float(np.quantile(values, 0.9))}


def audit(source, target):
    xs, ys, gs = source
    xt, _, gt = target
    model = new_model().fit(orientation_invariant(xs), ys)
    ps = model.predict_proba(orientation_invariant(xs))[:, 1]
    pt = model.predict_proba(orientation_invariant(xt))[:, 1]
    source_subject = {str(int(s)): distribution(ps[gs == s]) for s in np.unique(gs)}
    target_subject = {str(int(s)): distribution(pt[gt == s]) for s in np.unique(gt)}
    return {"status": "post-hoc label-free score-distribution diagnostic",
            "limitations": "source scores are in-sample; overlapping windows and site differences invalidate iid p-values; no alarm threshold is validated",
            "source": distribution(ps), "target": distribution(pt),
            "ecdf_sup_distance": ecdf_distance(ps, pt),
            "source_subjects": source_subject, "target_subjects": target_subject}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daphnet-dir", type=Path, required=True)
    p.add_argument("--fogstar-sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = audit(load_daphnet(args.daphnet_dir), load_fogstar(args.fogstar_sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    dest = args.out / "score_drift.json"
    dest.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {dest}")


if __name__ == "__main__":
    main()
