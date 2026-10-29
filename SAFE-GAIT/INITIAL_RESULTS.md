# Exploratory FoG-STAR Baseline Results

**Generated 28 October 2026 (Pacific Time).** These are preliminary measurements from real data, not final manuscript claims.

## Provenance and reproducibility

- Dataset: FoG-STAR v2, Zenodo record https://zenodo.org/records/17037669
- `sensor_data.csv` downloaded from Zenodo API, 119,629,580 bytes.
- MD5 verification: `952a37ab147da35e6d4e7a1e9bac44cb`, matching the record listing.
- Exact command: `python baseline.py --sensor-data data/sensor_data.csv --out results`
- Model: histogram gradient boosting on per-window mean, standard deviation, RMS, and finite-sample fraction of inertial channels. Missing features median-imputed within training folds only.
- Window length: 2 seconds, stride: 1 second. Positive windows have >=50% FoG-labeled samples; >=90% samples must have valid labels.
- Split: five-fold `GroupKFold` with participant IDs as groups, all held-out subjects unseen during training.
- Classification threshold: 0.5; not calibrated or selected by validation.

## Preliminary cohort/window audit

| Quantity | Value |
|---|---:|
| Distinct participants in eligible windows | 22 |
| Eligible analysis windows | 5,326 |
| Positive windows | 1,082 |
| Positive-window fraction | 20.315% |

## Cross-validation metrics

| Fold | Windows | Positive | Sensitivity | Precision | F1 | AUPRC | AUROC | Brier |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,098 | 345 | 0.6261 | 0.8640 | 0.7261 | 0.8326 | 0.8982 | 0.1193 |
| 2 | 1,002 | 168 | 0.1310 | 1.0000 | 0.2316 | 0.8748 | 0.9703 | 0.1021 |
| 3 | 1,111 | 283 | 0.0636 | 0.7826 | 0.1176 | 0.7098 | 0.9155 | 0.2050 |
| 4 | 1,118 | 212 | 0.2830 | 0.6316 | 0.3909 | 0.4875 | 0.7954 | 0.1345 |
| 5 | 997 | 74 | 0.2027 | 0.4839 | 0.2857 | 0.4071 | 0.8541 | 0.0562 |

## Interpretation and required follow-up

Although ranking metrics in some folds are substantial, sensitivity at a fixed threshold varies markedly. The result motivates **investigation** of calibration and threshold selection; it does not prove effectiveness of a new safety architecture.

These are window-level results on constrained activities, not prospective, event-level, personalized, cross-site or clinical outcomes. Participant sample size is small. Overlapping windows create dependencies. No calibration, confidence intervals, hyperparameter selection, cross-dataset transfer or event-latency assessment has been performed. Fold differences can reflect subject composition and episode prevalence. All scientific claims remain provisional until a locked evaluation protocol, annotation audit and comparison against multiple baselines are completed.

## Data publication rule

Raw FoG-STAR files must remain excluded from the repository. Do not publish individual clinical metadata or identifiable records.
