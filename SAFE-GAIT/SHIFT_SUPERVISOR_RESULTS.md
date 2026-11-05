# Source-Only Shift-Abstention Supervisor

**29 October 2026. Exploratory post-hoc experiment. Not clinical validation.**

## Question

Can a label-free feature-distance gate detect unfamiliar FoG-STAR acceleration
windows after learning only from Daphnet magnitude features, and abstain on
those windows before the Parkinson's freezing-of-gait classifier acts?

## Protocol

The same Daphnet source and FoG-STAR target windows as the prior cross-dataset
experiment were used. A gradient-boosted classifier fits three rotation-
invariant magnitude features on Daphnet only. A separate gate computes
Euclidean distance after centering each feature by its Daphnet median and
dividing by its Daphnet interquartile range. Its cutoffs correspond to Daphnet
distance percentiles of 80%, 90%, 95%, and 100%. FoG-STAR outcomes play no
role in fitting the classifier, distance scales, or gate cutoffs. The fixed
classification threshold is 0.5. No gate configuration is selected by target
results. However, the experiment was designed after previous FoG-STAR results
were inspected, so all conclusions are **post-hoc exploratory**.

## Observations

| Source retention target | Actual source retention | FoG-STAR retained | FoG-STAR positive windows abstained | Positive windows detected |
|---|---:|---:|---:|---:|
| 80% | 80.0% | 95.1% | 4 / 581 | 0 / 581 |
| 90% | 90.0% | 99.2% | 0 / 581 | 0 / 581 |
| 95% | 95.0% | 100.0% | 0 / 581 | 0 / 581 |
| 100% | 100.0% | 100.0% | 0 / 581 | 0 / 581 |

The underlying FoG-STAR classifier scored AUROC 0.3538, AUPRC 0.1937,
and zero sensitivity at the fixed 0.5 threshold. Selective AUROC among
retained windows was approximately 0.360 at 80% source retention and 0.357
at 90%, offering no convincing rescue of discrimination. These windows
overlap in time, and the experiment does not report independent event-level
performance.

### Participant-cluster uncertainty

FoG-STAR includes only **nine distinct sensor-data participants**. Resampling
whole participants with replacement (seed 2027; 1,000 iterations) yielded 998
bootstrap samples containing both classes. The AUROC 2.5th to 97.5th
percentile interval was **0.2413 to 0.5537**. This wide interval is a
descriptive cluster-bootstrap sensitivity analysis, not a prospectively
validated confidence guarantee. It acknowledges overlapping windows within
individuals; it does not resolve cohort-selection or annotation limitations.

## Interpretation

**The source-distance supervisor failed to flag most target windows even
though the classifier failed to transfer.** In particular, source retention
does not imply comparable target retention. This is a failure of a simple
feature-density proxy as a reliable warning mechanism, not evidence that
abstention resolves clinical deployment risk. Marginal feature distance can
overlook changes in the relationship between features and FoG labels.

Accepted-only metrics can be misleading: rejecting positive examples can
artificially improve selected performance. The implementation therefore
reports positive windows abstained, positive windows actually detected, and
overall sensitivity counting abstention as no alert. None of these window
metrics establish reliable clinical event recognition.

## Next steps

1. Separate covariate shift from label prevalence or conditional changes.
2. Fit and audit source-grouped out-of-distribution thresholds without target labels.
3. Consider a predeclared shift-warning monitor with a different unlabeled
   target population for validation, then test on an independent clinical cohort.
4. Evaluate episode-level false-alert burden and missed event duration, with
   participant-level confidence intervals.

## Reproduce

```bash
python shift_supervisor.py \
  --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

Writes `results/shift_supervisor.json`. Raw datasets and derived individual
prediction files are excluded from version control.
