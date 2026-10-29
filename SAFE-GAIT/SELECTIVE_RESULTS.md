# Pilot Selective Prediction Results

**Exploratory experiment, 28 October 2026 Pacific Time. Not suitable for a clinical performance claim.**

## Method

The 5,326 eligible FoG-STAR windows from 22 participants were divided using a five-fold subject-held-out outer split. Within each development fold, `GroupShuffleSplit` allocated 30% of development participants to a separate probability-calibration set. A histogram gradient-boosting classifier was trained only on the remaining participants. A sigmoid logistic calibration model was then fit on the disjoint calibration participants. Calibration-set quantiles defined selective acceptance thresholds targeting 60%, 80%, or 95% coverage; held-out test labels were not used for those threshold choices. The policy abstains on predictions nearest probability 0.5.

This is a **calibrated selective baseline**, not a demonstrated SAFE-GAIT safety solution. The model does not yet incorporate explicit sensor-quality control or event-level supervision.

## Results

| Fold | Raw Brier | Calibrated Brier | All-decision error | 80%-target actual coverage | Accepted error | Accepted positive sensitivity |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.5352 | 0.2727 | 45.66% | 78.76% | 46.07% | 4.21% |
| 2 | 0.4091 | 0.2699 | 41.99% | 90.29% | 39.78% | 4.05% |
| 3 | 0.2007 | 0.1917 | 19.78% | 80.44% | 18.23% | 0.00% |
| 4 | 0.0242 | 0.1326 | 6.37% | 95.82% | 5.96% | 0.00% |
| 5 | 0.0178 | 0.1361 | 17.40% | 73.79% | 11.64% | 33.33% |

## What these findings mean

1. Calibration improved Brier score in folds 1 to 3 but worsened it considerably in folds 4 and 5. There is **no consistent calibration benefit**.
2. Nominal 80% selective coverage did not reliably transfer to held-out participants. Observed coverage ranged from 73.79% to 95.82%, consistent with cohort shift or poorly representative calibration splits.
3. The acceptance mechanism failed to preserve positive-event sensitivity in several folds. In particular, zero accepted-positive sensitivity occurred in folds 3 and 4. It is therefore unsuitable for clinical-alert use.
4. Lower overall accepted error is not by itself evidence of safety because it may be achieved largely by avoiding positive cases.

## Required changes before scientific claims

- Audit class prevalence for model-training, calibration and testing participants in every fold.
- Examine negative sigmoid slopes and calibration-set representation; preserve ranking constraints only if explicitly justified and compared as an ablation.
- Add class-specific selective coverage, positive-event retention, and abstention by true class.
- Evaluate event-level FoG sensitivity and detection latency; window-level success is insufficient.
- Compare to an uncalibrated selective policy under identical group splits and coverage.
- Include risk controls or group-aware conformal methods only with clearly specified assumptions. Cross-patient shift invalidates naive exchangeability guarantees.
- Move toward calibration designed to account for subject heterogeneity, but do not select methods using held-out test outcomes.
- Add confidence intervals across participants and investigate whether samples are too small for the proposed claims.

**Consequence for manuscript:** SAFE-GAIT is currently a research question, not a validated method. This pilot provides honest motivation for why conventional uncertainty-based abstention is insufficient in heterogeneous clinical monitoring.
