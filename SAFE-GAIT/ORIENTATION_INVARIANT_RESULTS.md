# Exploratory Orientation-Invariant Transfer Analysis

**29 October 2026. Post-hoc follow-up after observing the original target test.**

## Research question

Does discarding orientation-sensitive accelerometer features improve transfer from
Daphnet trunk recordings to FoG-STAR back recordings?

## Experimental controls

- Identical pre-existing two-second windows, labels, subject groups, and source-only learner.
- The original 12-feature model uses axis means, axis SDs, axis RMS values,
  magnitude mean/SD, and magnitude-difference RMS.
- The reduced three-feature model retains only magnitude mean, magnitude SD,
  and magnitude-difference RMS. These are invariant to any fixed orthogonal
  three-dimensional rotation of the measured acceleration axes.
- Same five-fold participant-grouped Daphnet CV and final Daphnet-only fitting.
- Threshold fixed at 0.5 for both models. No target fitting, feature scaling,
  or threshold optimization.
- **Because prior FoG-STAR target results were observed before choosing this
  analysis, this is explicitly exploratory.** The target cannot be described
  as an untouched confirmatory external validation cohort.

## Measured results

| Metric | 12-feature model | Magnitude-only model |
|---|---:|---:|
| Source grouped CV AUROC, five-fold mean | 0.7512 | 0.8160 |
| Source grouped CV AUROC, fold range | 0.6780 to 0.8423 | 0.7320 to 0.8550 |
| Target AUROC, 2,263 windows | 0.3488 | 0.3538 |
| Target AUPRC, 581 positive windows | 0.1893 | 0.1937 |
| Target sensitivity at threshold 0.5 | 0% | 0% |

The reduced model improved mean source CV AUROC but did not meaningfully improve
target discrimination. Both models missed all positive target windows at the
fixed 0.5 operating threshold. **No successful transfer is claimed.**

### Label-free source-target feature differences

These descriptive comparisons use only accelerometry feature distributions,
not FoG-STAR labels or predictions. Standardized mean difference uses the
square root of mean source and target variances as denominator.

| Magnitude feature | Daphnet mean | FoG-STAR mean | Standardized difference |
|---|---:|---:|---:|
| Mean norm (g) | 1.0043 | 1.0227 | +0.1672 |
| Norm SD (g) | 0.0842 | 0.0553 | -0.3851 |
| First-difference norm RMS (g) | 0.0654 | 0.0372 | -0.4783 |

Feature distribution differences suggest non-equivalence in recorded movement
variability or sensing conditions. The descriptive statistics cannot determine
whether differences originate in cohort, tasks, attachment, sampling, disease
severity, or annotation protocols. Overlapping windows are correlated; values
above are not inferential effect sizes or significance tests.

## Interpretation and next defensible study

The orientational sensitivity hypothesis alone cannot explain the transfer
failure. An important failure mode is that improved source-grouped CV did not
provide a trustworthy predictor for a second dataset. Next work should
evaluate source-only out-of-distribution warning indicators, quality-based
abstention, subject-level uncertainty, and an additional prospectively held-out
dataset or population before claiming a generalizable detection method.

Avoid selecting a better model on the observed FoG-STAR target metrics and then
reporting FoG-STAR as a fresh validation dataset. This comparison is useful as
an explicit negative result and method-development diagnostic.

## Reproduce

```bash
python cross_dataset_invariant.py \
  --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

The resulting `results/cross_dataset_invariant.json` and the raw datasets are
not committed to GitHub.
