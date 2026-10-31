# SAFE-GAIT: When Shift Warnings Fail in Parkinson's Freezing-of-Gait Monitoring

**Consolidated research manuscript, version 0.1, 29 October 2026**

**Target:** ACM TRUST 2027 REED-AI track. **Status:** exploratory empirical study,
not ready for submission. Blind-review author details omitted. All reported
results are retrospective public-data research findings.

## Abstract

Wearable classifiers for freezing of gait (FoG) in Parkinson's disease may
produce confident decisions under conditions that differ from their training
data. Whether uncertainty and distribution-shift warnings reliably recognize
such failures remains uncertain. We present a reproducible stress-test of
three accelerometer-based warning mechanisms using Daphnet as source and
FoG-STAR as target: orientation-invariant features, source-calibrated feature
distance abstention, and score-distribution drift monitoring. Participant-
grouped Daphnet cross-validation yielded mean AUROC 0.751 with 12 features
and 0.816 with three magnitude-only features. However, target AUROC remained
0.349 and 0.354, respectively, with no positive windows detected at a fixed
0.5 threshold. A timestamp-faithful replay found that the magnitude-only
source model detected none of the 28 annotated FoG episodes in 2,392.15
seconds of FoG-STAR recordings, while generating six unmatched alert runs.
A source-only distance gate reduced unmatched runs to five at two settings
but still missed every episode. A score-shift warning flagged six of nine
target participants when calibrated on pooled source folds, but only one
when the calibration unit was changed to single held-out participants.
These exploratory failures illustrate the sensitivity of apparent safety
benefits to evaluation and calibration choices. They motivate participant-
matched monitoring, event-level endpoints and explicit failure reporting
before any clinical reliability claims.

**Keywords:** Parkinson's disease; freezing of gait; trustworthy AI;
distribution shift; abstention; event detection; wearable accelerometry.

## 1. Introduction

FoG can seriously disrupt mobility in Parkinson's disease. Wearable-sensor
classifiers offer the prospect of longitudinal monitoring, but an algorithm
that predicts FoG well in one recorded cohort can fail when sensor placement,
activity, population or annotation conditions change. The consequences of a
missed episode and a false alert differ; neither can be represented solely
by window-level AUROC. In addition, abstaining on difficult windows can
improve selected-window performance by silently withholding relevant alerts.

Our question is narrower than clinical deployment: **when a source-trained
FoG detector fails under public-dataset shift, do simple and transparent
uncertainty or drift indicators identify that failure?** We study negative
results as evidence about evaluation requirements, not as proof of a new
safety-guaranteed algorithm. The contributions are:

1. A reproducible, source-order-preserving event replay with explicit
   end-of-window alert timing and unmatched-alert burden.
2. A controlled comparison of axis-dependent and rotation-invariant
   acceleration features under source-only learning.
3. An abstention audit that counts rejected positive windows and missed
   events rather than interpreting lower alert volume as success.
4. A calibration-unit sensitivity study contrasting pooled-fold and
   single-participant score-drift thresholds.

## 2. Data and scope

### Prior work and precise research gap

Wearable FoG monitoring has an established history beginning with early
wearable detection and cueing systems, including Bächlin and colleagues'
2010 work. A 2025 study directly investigated sensor placement, activity,
dataset choice and external FoG event detection, while a 2026 cross-dataset
study reported a pronounced laboratory-to-daily-living performance gap.
Consequently, **cross-dataset failure itself is not our novelty claim**.
In trustworthy ML, reject-option classification and model-output-based
deployment suitability checks are also established, as illustrated by
SelectiveNet (2019) and the suitability-filter framework (2025). Our narrower
contribution is the combined operational audit of missed FoG episodes,
abstention, alert burden and calibration-unit sensitivity under a clearly
documented failure case. See `LITERATURE_NOVELTY_AUDIT.md` for primary-source
links and the ongoing full bibliography review.


We use Daphnet wearable FoG recordings as the training source: ten
participants and 17 recordings, with trunk three-axis acceleration converted
from mg to g. Samples annotated as outside the experiment are not treated
as negatives. We use back three-axis acceleration from a locally verified
FoG-STAR release as the shifted target. The target sensor file contains
**nine distinct participant IDs**, although the accompanying clinical
metadata contains 22 rows. The discrepancy is unresolved and constrains
all sample-size claims. The analyzed target has 2,263 eligible two-second
windows, 581 positive windows, and 28 raw FoG episodes from five
participants, recorded over 2,392.15 seconds of valid annotation time.

The comparison involves different attachment sites, protocols and cohorts.
It is a distribution-shift stress test, **not** a matched-site validation
study or evidence of home-care performance.

## 3. Methods

### 3.1 Preprocessing and leakage controls

We retain original recording order, split at participant/session/task changes
and nonmonotonic or excessive timestamp gaps, and construct two-second
windows at one-second intervals. Each window is eligible only when at least
90% of its samples have valid binary annotations. Window targets use at
least 50% positive samples. Each model uses only Daphnet during fitting;
no FoG-STAR labels are used for model parameters, feature normalization,
operating threshold or warning cutoff. Source internal diagnostics use
participant-grouped five-fold validation.

### 3.2 Predictive representations

The primary learner is a fixed histogram gradient-boosting classifier with
median imputation. The 12-feature representation summarizes axis-wise
means, standard deviations and RMS values, plus magnitude mean, SD and
first-difference RMS. The three-feature variant retains only magnitude
statistics invariant to a fixed rotation of the sensor axes. Both use the
same fixed class threshold of 0.5. Model and feature choices are exploratory
and were not selected through a fresh external target.

### 3.3 Feature-distance abstention

An independent gate uses robust source medians and interquartile ranges to
calculate diagonal standardized Euclidean distance in the three magnitude
features. Distance thresholds retain approximately 80%, 90%, 95% or 100%
of Daphnet windows. Target windows beyond the chosen cutoff abstain and
emit no alert. We measure accepted coverage, accepted-only discrimination,
abstained positive windows and overall sensitivity with abstention counted
as no alert.

### 3.4 Score drift and calibration unit

We compare model probability-score distributions using the supremum
distance between empirical cumulative distribution functions (ECDFs).
A first pilot used five pooled participant-held-out Daphnet folds to set an
empirical 95th-percentile cutoff. To correct the mismatch between pooled
calibration and individual target participants, a second pilot used ten
leave-one-participant-out Daphnet distances. Each target subject is scored
against a source reference fitted without target data. These procedures
are **not exchangeability-certified drift tests** and their quantile
cutoffs do not imply population false-warning guarantees.

### 3.5 Event and uncertainty evaluation

Raw sample-level FoG runs define reference episodes. Alert runs are formed
from predictions at the completion of each eligible window, not its onset.
Events are matched one-to-one by temporal overlap without additional
tolerance or alert merging. We count detected and missed episodes, unmatched
alert runs and false alerts per annotated hour. We also compute a descriptive
participant-cluster bootstrap AUROC interval by resampling whole target
participants rather than dependent windows.

## 4. Results

| Experiment | Source/internal observation | FoG-STAR observation |
|---|---|---|
| 12-feature classifier | Grouped CV mean AUROC 0.751 | AUROC 0.3488; sensitivity at 0.5 = 0% |
| 3-feature magnitude classifier | Grouped CV mean AUROC 0.816 | AUROC 0.3538; sensitivity at 0.5 = 0% |
| Feature-distance gate, 80% source retention | Source coverage 80% | Target coverage 95.1%; no positive windows detected |
| Feature-distance gate, 90% source retention | Source coverage 90% | Target coverage 99.2%; no positive windows detected |
| Pooled-fold score-drift warning | Empirical cutoff 0.1871 | 6/9 target participants flagged |
| Single-participant score-drift warning | Empirical cutoff 0.3838 | 1/9 target participants flagged |

At event level, the magnitude-only classifier detected **0/28 annotated
episodes**, with six unmatched alert runs (9.03 per recorded hour). The
80% and 90% feature-distance gates produced five unmatched runs (7.52/hour)
and **still detected 0/28 episodes**. Reducing alerts without detecting
events is not evidence of safer detection. A descriptive participant-level
bootstrap yielded an AUROC percentile interval of 0.241 to 0.554 from 998
evaluable of 1,000 resamples over nine target participants. The interval
reflects substantial uncertainty, not a confirmatory external estimate.

The three magnitude features themselves showed source-to-target standardized
mean differences of +0.167 for norm mean, -0.385 for norm SD and -0.478
for norm-difference RMS. The model score ECDF distance was 0.144 when
comparing in-sample source scores with target scores. These are descriptive
statistics; task and cohort differences prevent causal interpretation.

## 5. Discussion

Three lessons emerge. First, stronger internal discrimination on
orientation-reduced features did not ensure transfer. Second, marginal
distance in input-feature space did not reliably signal the detector's
failure, illustrating that output-label relationships may change even
when features appear familiar. Third, the score-drift warning changed
substantially when its calibration unit was made comparable with the
intended patient-level decision. This cautions against treating an
apparently favorable warning fraction as validation.

The study's distinctive empirical contribution is a transparent failure
audit with consistent attention to model fitting, target-label boundaries,
raw event time and warning calibration. We do **not** claim that our
abstention or drift methods outperform previous work, that they have
calibrated error guarantees, or that any system here is clinically safe.
An improved prospective design needs source-participant-matched warning
calibration, another untouched external population, and explicit evidence
for event-level sensitivity and false-alert burden at chosen operating
points. Human oversight and governance remain design requirements rather
than tested interventions.

## 6. Limitations and ethics

The target sensor file is smaller than its clinical metadata implies, with
nine participants and only five having recorded positive episodes.
Overlapping windows are correlated; event matching depends on a specified
zero-tolerance convention; sensor sites and participant activities differ;
and source score references are often in-sample. Several analyses were
designed after earlier FoG-STAR outcomes were inspected. **FoG-STAR is no
longer an untouched confirmatory dataset for these post-hoc models.**
Participants may differ in clinical severity, treatment state, mobility
and demographic characteristics, none of which can be adequately assessed
for fairness with this small subset. This is experimental software and
must not generate autonomous care decisions.

## 7. Conclusion

In this retrospective Parkinson's FoG stress test, a transferable safety
warning did not emerge from feature invariance, source-distance abstention,
or simple score-shift calibration. The failures are informative: reliability
claims must be evaluated with comparable calibration units and explicit
clinical event outcomes, including the costs of abstention. Independent
evaluation is required before a positive trustworthy-AI claim.

## Reference and submission gates

The following data and venue records have been used in the project. Full
authorship, titles, versions, permanent identifiers and license conditions
must be verified against original sources before they are placed into an
ACM bibliography:

1. FoG-STAR release: https://zenodo.org/records/17037669
2. Daphnet Freezing of Gait: https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait
3. ACM TRUST 2027 author guidance: https://eigtrust.acm.org/trust2027/authors-guidelines/

**Not yet submission-ready:** At least 30 correctly verified literature
references, related-work contrast, ACM double-column LaTeX conversion,
reproducible figures with consistent type, disclosure/compliance audit,
confirmed conference instructions, and independent follow-up evaluation
remain outstanding. The existing historical working draft is retained for
research traceability; it is not the clean submission draft.
