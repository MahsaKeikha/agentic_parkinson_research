"""Matched single-participant source-only score-shift calibration.

All analyses remain post-hoc and exploratory. The source threshold is derived
from leave-one-Daphnet-participant-out models and target labels are unused.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from cross_dataset import load_daphnet, load_fogstar, new_model
from cross_dataset_invariant import orientation_invariant
from score_drift import ecdf_distance


def leave_one_participant_out(source, labels, groups):
    """One held-out person's score distribution versus its training reference."""
    source = np.asarray(source)
    labels, groups = np.asarray(labels), np.asarray(groups)
    unique = np.unique(groups)
    if len(unique) < 3:
        raise ValueError("At least three source participants required")
    records = []
    for subject in unique:
        test = groups == subject
        train = ~test
        if len(np.unique(labels[train])) != 2:
            raise ValueError("Training group has only one class")
        model = new_model().fit(source[train], labels[train])
        training_scores = model.predict_proba(source[train])[:, 1]
        heldout_scores = model.predict_proba(source[test])[:, 1]
        records.append({"source_subject": int(subject), "heldout_windows": int(test.sum()),
                        "reference_windows": int(train.sum()),
                        "ecdf_distance": ecdf_distance(training_scores, heldout_scores)})
    return records


def audit(source_data, target_data):
    xs, ys, gs = source_data
    xt, _, gt = target_data
    source, target = orientation_invariant(xs), orientation_invariant(xt)
    calibration = leave_one_participant_out(source, ys, gs)
    distances = np.array([r["ecdf_distance"] for r in calibration])
    cutoff = float(np.quantile(distances, 0.95))
    full_model = new_model().fit(source, ys)
    reference = full_model.predict_proba(source)[:, 1]
    scores = full_model.predict_proba(target)[:, 1]
    target_rows = []
    for subject in np.unique(gt):
        selected = gt == subject
        distance = ecdf_distance(reference, scores[selected])
        target_rows.append({"target_subject": int(subject), "windows": int(selected.sum()),
                            "ecdf_distance": distance, "warning": bool(distance > cutoff)})
    return {"status": "exploratory matched single-participant calibration",
            "source_calibration": calibration, "cutoff_95th_percentile": cutoff,
            "source_calibration_warnings_in_sample": int((distances > cutoff).sum()),
            "target": target_rows,
            "target_warnings": int(sum(r["warning"] for r in target_rows)),
            "target_participants": len(target_rows),
            "limitations": "Only ten source participants; cutoff estimated on same source leave-one-out distances; different sites, window counts and subject distributions; external target previously inspected; no false-warning guarantee"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daphnet-dir", type=Path, required=True)
    p.add_argument("--fogstar-sensor-data", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    report = audit(load_daphnet(args.daphnet_dir), load_fogstar(args.fogstar_sensor_data))
    args.out.mkdir(parents=True, exist_ok=True)
    destination = args.out / "participant_drift.json"
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {destination}")


if __name__ == "__main__":
    main()
