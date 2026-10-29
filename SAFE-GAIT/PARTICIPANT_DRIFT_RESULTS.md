# Matched Participant-Level Score Drift Calibration

**29 October 2026. Retrospective exploratory result. No clinical validation.**

## Motivation

The preceding five-fold drift study calibrated a score-distance warning on
pooled held-out participant groups, then tested on single FoG-STAR people.
This mismatch in unit of analysis could artificially change sensitivity.
We therefore replaced the source calibration with ten leave-one-participant-
out comparisons: one Daphnet person versus the in-sample score distribution
from a model trained on all other Daphnet people. Each FoG-STAR comparison
also concerns one person versus a Daphnet-trained model's source reference.

## Frozen design

- Three rotation-invariant accelerometer magnitude features.
- Ten leave-one-Daphnet-participant-out models; each fit to the other nine.
- Score ECDF sup distance between the held-out person's score distribution
  and the training people's scores for that fitted model.
- Fixed empirical 95th percentile of the ten source distances.
- One full Daphnet model then scores each FoG-STAR participant against its
  source reference. FoG-STAR labels have no role in selecting the cutoff.
- This is **post-hoc**, after earlier analyses observed FoG-STAR target results.

## Results

Source-person distances ranged from **0.075 to 0.465**. The empirical
95th-percentile cutoff was **0.3838**. One of ten source calibration
participants exceeded this sample-derived cutoff (an in-sample proportion,
not an estimated future false-warning rate).

| FoG-STAR participant | Score distance | Exceeded cutoff? |
|---|---:|---|
| 1 | 0.105 | No |
| 2 | 0.393 | Yes |
| 3 | 0.254 | No |
| 4 | 0.201 | No |
| 5 | 0.180 | No |
| 6 | 0.166 | No |
| 7 | 0.327 | No |
| 8 | 0.238 | No |
| 10 | 0.292 | No |

**Only 1 of 9** target participants exceeded the matched-unit cutoff,
compared with 6 of 9 in the previous pooled-fold pilot. This substantial
disagreement shows that the apparent warning coverage depended strongly on
the calibration unit. The matched-unit approach is methodologically closer
to the target task but cannot identify most people in a target cohort in
which event detection had previously failed.

## Limits and implications

The two datasets still differ in subject-specific window counts, sensor
placement, tasks, label prevalence and population. Ten subjects cannot
justify a nominal 5% false-warning guarantee, and the empirical percentile
is fit and assessed on the same ten source calibration distances. The source
score distribution remains in-sample for each model. Warning presence is
not ground-truth detection of an unsafe clinical prediction. These findings
are a methodological sensitivity analysis and a **negative result**, not a
validated distribution-shift detector.

An independent source calibration and separate external cohort, plus
subject-clustered event-level outcomes, are required for further claims.

## Reproduce

```bash
python participant_drift.py \
  --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

Writes `results/participant_drift.json`, excluded from version control.
