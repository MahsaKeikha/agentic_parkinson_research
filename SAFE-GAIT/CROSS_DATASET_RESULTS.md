# Cross-Dataset Generalization Stress Test

**29 October 2026. Exploratory transfer experiment. No clinical validity claim.**

## Question

Does a classifier trained on Daphnet trunk accelerometer windows transfer without target tuning to FoG-STAR back accelerometer windows?

## Protocol

- Source: Daphnet 10 participants, 17 recording runs, trunk tri-axial acceleration originally in mg, converted to g. Source annotation 0 (outside experiment) excluded.
- Target: checksum-verified FoG-STAR sensor file, 9 participant IDs, back tri-axial acceleration in g.
- Two-second windows with a one-second stride, with run and timestamp-gap isolation.
- Twelve features: axis means, standard deviations, RMS; magnitude mean/SD; magnitude-difference RMS.
- Source participant-grouped five-fold CV for an internal diagnostic.
- Final classifier fitted to all Daphnet feature windows. Target FoG-STAR **labels are used only for evaluation**. No target normalization, threshold calibration, hyperparameter selection or fitting.
- Same histogram gradient-boosted model and training-only imputation across all comparisons. Fixed threshold 0.5.

## Findings

| Measurement | Result |
|---|---:|
| Daphnet source windows | 18,052 |
| Daphnet source positive windows | 1,737 |
| FoG-STAR target windows | 2,263 |
| FoG-STAR target positive windows | 581 |
| FoG-STAR target AUROC | **0.3488** |
| FoG-STAR target AUPRC | **0.1893** |
| FoG-STAR target positive sensitivity, threshold 0.5 | **0.0%** |

Within Daphnet, source-held-out fold AUROCs were 0.8100, 0.6918, 0.7340, 0.8423 and 0.6780. Sensitivity at a fixed 0.5 threshold was also low and heterogeneous within the source population.

## Scientific interpretation

This is a striking failure of direct cross-dataset transfer, not a demonstration that a novel method solves it. Differences in sensor orientation, attachment position, signal distributions, movement tasks and cohort characteristics may explain the result. An AUROC below 0.5 may reflect rank reversal or domain mismatch. We cannot attribute the cause without further experiments.

Do **not** retune the model, reverse scores, recalibrate using FoG-STAR outcomes or select features based on target labels while still claiming untouched external validation. Any adaptation experiment must be labeled separately, with a further held-out target cohort.

## Next analyses

An exploratory magnitude-only and label-free feature-shift follow-up has now
been completed. See [ORIENTATION_INVARIANT_RESULTS.md](ORIENTATION_INVARIANT_RESULTS.md).

1. Compare axis-specific versus magnitude-only orientation-invariant features under predefined source-only choices.
2. Quantify feature distribution shift and sensor signal-quality mismatch without target labels.
3. Examine medication/activity and protocol comparability and whether acceleration magnitudes reflect equivalent physical axes.
4. Evaluate participant-level uncertainty, not just pooled overlapping windows.
5. Consider alternative training/target direction as a separately preregistered experiment, without optimizing after seeing target results.

## Reproduce

```
python cross_dataset.py --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

Output: `results/cross_dataset_shift.json`, excluded from version control. Raw datasets remain uncommitted.
