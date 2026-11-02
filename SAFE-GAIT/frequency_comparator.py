"""Frequency-domain FoG stress-test comparator, trained on Daphnet only.

Spectral power features are descriptive and NOT claimed to reproduce a
published FoG detector. Both cohorts use the same 2-second window algorithm.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupKFold

from cross_dataset import load_daphnet, load_fogstar, metrics, new_model

FS = 60.0
BANDS = ((0.5, 3.0), (3.0, 8.0), (8.0, 15.0))

def spectral_features(samples):
    samples = np.asarray(samples, dtype=float)
    if samples.ndim != 2 or samples.shape[1] != 3 or len(samples) < 4:
        raise ValueError("Expected a 3-axis time-series window")
    if not np.isfinite(samples).all():
        raise ValueError("Nonfinite sensor samples")
    magnitude = np.linalg.norm(samples, axis=1)
    centered = magnitude - magnitude.mean()
    window = np.hanning(len(centered))
    freqs = np.fft.rfftfreq(len(centered), d=1 / FS)
    power = np.abs(np.fft.rfft(centered * window)) ** 2
    bands = [float(power[(freqs >= low) & (freqs < high)].sum())
             for low, high in BANDS]
    total = max(float(power.sum()), 1e-12)
    return np.asarray([np.log1p(v) for v in bands]
                      + [v / total for v in bands]
                      + [float(np.std(magnitude))], dtype=float)

def compare(source, target):
    xs, ys, gs = source
    xt, yt, gt = target
    folds = []
    for fold, (train, test) in enumerate(GroupKFold(n_splits=5).split(xs, ys, gs), 1):
        model = new_model().fit(xs[train], ys[train])
        folds.append({"fold": fold,
                      "test_subjects": list(map(int, np.unique(gs[test]))),
                      **metrics(ys[test], model.predict_proba(xs[test])[:, 1])})
    model = new_model().fit(xs, ys)
    prediction = model.predict_proba(xt)[:, 1]
    return {"status": "post-hoc exploratory frequency-feature comparator",
            "warning": "Novel adaptation, not a faithful replication of a published FoG baseline",
            "feature_bands_hz": [list(b) for b in BANDS],
            "source_cv": folds,
            "target_aggregate": metrics(yt, prediction),
            "target_per_subject": [{"subject": int(s),
                                    **metrics(yt[gt == s], prediction[gt == s])}
                                   for s in np.unique(gt)]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--daphnet-dir", type=Path, required=True)
    p.add_argument("--fogstar-sensor-data", type=Path, required=True)
    p.add_argument("--timestamp-unit", choices=["s", "ms"], required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    results = compare(load_daphnet(args.daphnet_dir, extractor=spectral_features),
                      load_fogstar(args.fogstar_sensor_data,
                                   timestamp_unit=args.timestamp_unit,
                                   extractor=spectral_features))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "frequency_comparator.json").write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
