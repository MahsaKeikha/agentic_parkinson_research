"""Source-only distance-based abstention under cross-dataset shift.

Exploratory, not independent clinical validation. The external target labels
were already inspected in earlier research phases. All distance calibration
uses Daphnet features only; FoG-STAR labels are evaluation-only.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from cross_dataset import load_daphnet, load_fogstar, metrics, new_model
from cross_dataset_invariant import orientation_invariant


class SourceDistanceGate:
    """Robust diagonal feature-distance score with source-only quantile cutoff."""

    def __init__(self, retained_fraction=0.9):
        if not 0 < retained_fraction <= 1:
            raise ValueError("retained_fraction must be in (0,1]")
        self.retained_fraction = retained_fraction

    def fit(self, source):
        source = np.asarray(source, dtype=float)
        if source.ndim != 2 or not np.isfinite(source).all():
            raise ValueError("source must be a finite 2D matrix")
        self.median_ = np.median(source, axis=0)
        self.scale_ = np.percentile(source, 75, axis=0) - np.percentile(source, 25, axis=0)
        self.scale_[self.scale_ < 1e-8] = 1.0
        self.cutoff_ = float(np.quantile(self.distance(source), self.retained_fraction))
        return self

    def distance(self, features):
        x = np.asarray(features, dtype=float)
        if x.ndim != 2 or x.shape[1] != len(self.median_):
            raise ValueError("incompatible feature shape")
        return np.sqrt(np.sum(((x - self.median_) / self.scale_) ** 2, axis=1))

    def accept(self, features):
        return self.distance(features) <= self.cutoff_


def evaluate_gate(labels, probabilities, accept):
    labels = np.asarray(labels, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    accept = np.asarray(accept, dtype=bool)
    if not (len(labels) == len(probabilities) == len(accept)):
        raise ValueError("Evaluation arrays must have equal length")
    predicted = probabilities >= 0.5
    positive = labels == 1
    return {
        "total_windows": int(len(labels)),
        "coverage": float(np.mean(accept)),
        "accepted_windows": int(accept.sum()),
        "positive_windows_abstained": int(np.sum(positive & ~accept)),
        "negative_windows_abstained": int(np.sum(~positive & ~accept)),
        "detected_positive_windows": int(np.sum(positive & accept & predicted)),
        "false_positive_accepted_windows": int(np.sum(~positive & accept & predicted)),
        "accepted_only_metrics": metrics(labels[accept], probabilities[accept]) if accept.any() else None,
        "overall_sensitivity_counting_abstention_as_no_alert":
            float(np.sum(positive & accept & predicted) / positive.sum()) if positive.sum() else None,
    }


def run(source_data, target_data):
    xs, ys, _ = source_data
    xt, yt, gt = target_data
    source = orientation_invariant(xs)
    target = orientation_invariant(xt)
    model = new_model().fit(source, ys)
    prediction = model.predict_proba(target)[:, 1]
    policies = {}
    for retained in (0.8, 0.9, 0.95, 1.0):
        gate = SourceDistanceGate(retained).fit(source)
        accepted = gate.accept(target)
        policies[str(retained)] = {
            "source_calibration_coverage": float(gate.accept(source).mean()),
            "source_distance_cutoff": gate.cutoff_,
            "target": evaluate_gate(yt, prediction, accepted),
            "target_per_subject": [{"subject": int(g), **evaluate_gate(
                yt[gt == g], prediction[gt == g], accepted[gt == g])}
                for g in np.unique(gt)]}
    return {
        "status": "post-hoc exploratory shift-abstention experiment",
        "protocol": "source-only robust distances; fixed 0.5 classifier threshold; no target tuning",
        "warning": "Window-level selective metrics exclude rejected windows and cannot establish safe event-level alerts",
        "target_base": metrics(yt, prediction),
        "policies": policies}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--daphnet-dir", type=Path, required=True)
    parser.add_argument("--fogstar-sensor-data", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    report = run(load_daphnet(args.daphnet_dir), load_fogstar(args.fogstar_sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "shift_supervisor.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
