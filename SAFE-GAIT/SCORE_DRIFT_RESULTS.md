# Label-Free Prediction-Score Drift Diagnostic

**29 October 2026. Exploratory descriptive analysis, not a safety alarm.**

## Question

Does a source-only Daphnet freezing-of-gait classifier emit systematically
different score distributions for FoG-STAR data, despite a magnitude-distance
gate failing to flag most target windows?

## Protocol

Fit the fixed three-magnitude-feature gradient-boosted classifier to Daphnet
windows. Calculate its probability scores on Daphnet and on FoG-STAR without
using target labels. Compare empirical score summaries and the maximum
absolute difference of the two empirical cumulative distribution functions
(ECDF sup distance). Record participant-specific target score means.

**Critical limitation:** Daphnet scores are in-sample, while FoG-STAR scores
are out-of-sample. Model fit differences can therefore affect the comparison.
The windows overlap, observations are clustered by participant, and this
analysis was designed after prior target outcomes were seen. No iid
two-sample p-value, drift-alarm threshold, or statistical detection guarantee
is claimed. A future prospective warning requires source-participant
holdout calibration and independent target evaluation.

## Measurements

| Quantity | Daphnet | FoG-STAR |
|---|---:|---:|
| Windows | 18,052 | 2,263 |
| Mean predicted FoG probability | 0.09551 | 0.05837 |
| Median predicted FoG probability | 0.03459 | 0.02387 |
| 90th percentile | 0.30750 | 0.17390 |
| Fraction of predictions at least 0.5 | 0.7866% | 0.2651% |

The empirical CDF sup distance was **0.14367**. FoG-STAR participant mean
scores ranged approximately from 0.014 to 0.145. The lower target scores
are consistent with the model's missed freezing episodes in the separately
reported outcome audit, but score distribution difference alone cannot
identify conditional failure or establish clinical validity.

## Reproduce

```bash
python score_drift.py \
  --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

Writes `results/score_drift.json`, not committed with raw data.
