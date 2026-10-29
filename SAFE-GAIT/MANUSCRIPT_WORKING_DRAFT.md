# SAFE-GAIT: Risk-Aware and Explainable AI for Trustworthy Freezing-of-Gait Detection in Parkinson's Disease

**Working manuscript, pre-submission research draft.** Intended for ACM TRUST 2027, REED-AI track. All numerical statements below refer to exploratory benchmarks and are subject to validation. Author names and affiliations are deliberately omitted for double-blind review.

> **Data audit correction (29 October 2026):** The downloaded sensor file contains only 9 distinct participant IDs, despite 22 rows of clinical metadata. Previous 22-participant and 5,326-window results are superseded and must not be submitted. Quantitative claims below are retained as historical draft text pending a complete rewrite after dataset reconciliation.

## Abstract (working version)

**Retrospective cross-dataset episode audit:** On 2,392.15 seconds of
annotated FoG-STAR recordings containing 28 freezing episodes, the
Daphnet-trained magnitude classifier detected zero reference episodes and
generated six unmatched alert runs (9.03 per hour). Source-only distance
abstention at 80% and 90% Daphnet retention reduced unmatched runs to five
(7.52 per hour) but still missed all 28 episodes. Decisions were timestamped
at the completion of two-second windows; no matching tolerance or alert
merging was applied. These exploratory findings demonstrate that a marginal
reduction in false alerts does not imply safety when event sensitivity
remains zero. See `CROSS_DATASET_EVENT_RESULTS.md`.


**Additional exploratory failure analysis, 29 October 2026:** A source-only
robust magnitude-distance gate calibrated to retain 80% of Daphnet windows
retained 95.1% of FoG-STAR windows; a gate calibrated to 90% source retention
retained 99.2% of target windows. Neither setting detected any of the 581
positive target windows with the fixed 0.5 classifier decision threshold.
Thus, this simple out-of-distribution mechanism did not identify the model's
severe cross-dataset failure. These are overlapping-window diagnostics, not
event-level safety guarantees; details in `SHIFT_SUPERVISOR_RESULTS.md`.

When uncertainty was resampled at the participant rather than window level,
the FoG-STAR AUROC cluster-bootstrap percentile interval was 0.241 to 0.554
(998 evaluable of 1,000 resamples from nine participants). The interval
underscores limited precision and should not be construed as confirmatory
external validation.


Reliable freezing-of-gait (FoG) detection from wearable sensors is challenging because motor patterns differ between people with Parkinson's disease and recorded monitoring conditions. Predictive confidence is frequently interpreted as actionable certainty despite potential distribution shift. We investigate risk-aware selective prediction for FoG classification using wearable inertial data. Our evaluation protocol separates participants for model training, probability calibration and outer testing, and reports not only prediction accuracy but also the coverage, class-specific retention and error of automated decisions. A preliminary nine-participant subset of the FoG-STAR sensor file illustrates a discrepancy between discrimination and fixed-threshold sensitivity and exposes unstable calibration transfer across participant groups. Rather than assuming that uncertainty-based abstention improves safety, we quantify where its error reductions are offset by missed positive episodes. We outline a quality-aware supervisory architecture that explicitly accounts for such failure modes. This work aims to establish reproducible evaluation criteria for trustworthy FoG monitoring. The proposed supervisory method and external evaluation remain under development.

**Keywords:** Parkinson's disease, freezing of gait, trustworthy AI, wearable sensing, probability calibration, selective prediction, risk-aware control.

## 1. Introduction

Wearable inertial sensors can capture changes in movement that may indicate freezing of gait, a disabling motor manifestation of Parkinson's disease. Automating such assessments is appealing because clinical observations are intermittent and movement patterns vary between contexts. However, a binary score is only useful for clinical decision support when its expected reliability under changing patients and sensor conditions is understood. False negative classifications can suppress potentially important observations, whereas false positives may increase unnecessary alarms and undermine confidence in the system.

The distinction between **discrimination** and **decision reliability** is central. A classifier may have strong rank-based performance, as measured by AUROC or AUPRC, yet be unsuitable at a fixed operating threshold. Similarly, a calibrated risk score on one group need not remain calibrated in another. Selective classifiers add an abstention option, but their apparent error reduction may be misleading if they disproportionately withhold decisions for the very episodes a monitoring system is intended to detect.

We study these failure modes with a reproducible participant-independent protocol on FoG-STAR, an annotated public inertial-sensor dataset. The long-term goal is SAFE-GAIT, a risk-aware supervisor that combines predictive uncertainty with input-quality information and explicit restrictions on positive-event retention. The present experimental results are preliminary baselines, not evidence of clinical efficacy.

The scientific contributions targeted by the completed paper are: (i) a controlled evaluation of the relationship between patient shift, score calibration and selective risk; (ii) a risk-aware policy that can decline unreliable automated decisions without concealing missed FoG events; (iii) transparent event-level evaluation with sensor degradation and external-domain stress tests. At present, only the first part has an initial implementation.

## 2. Related Work: Scope of the Comparison

FoG-STAR provides synchronized inertial measurements, activity and severity labels, and subject-level clinical measures. Daphnet has served as a foundational accelerometer dataset for FoG recognition but differs in sensor placements and protocols. The PADS dataset studies Parkinson's-related movement features using smartwatch measurements, with a different primary prediction task. Prior work has investigated cross-dataset deployment gaps in FoG monitoring and self-explaining Parkinson's screening with calibration. Thus neither wearing a sensor, explaining a deep model, nor applying temperature/sigmoid calibration is novel by itself. The intended novelty must be established as the **jointly evaluated decision and risk-control mechanism**, with direct comparisons to strong prior baselines and explicit negative outcomes.

## 3. Problem Formulation

For sensor window X and label Y in {0,1}, a trained classifier estimates p(X) = P(Y=1 | X). Let q(X) denote quality measurements and u(X) a model uncertainty score. An automated supervisory decision a(X) is either positive, negative, or abstain. Define automated decision coverage C = P(a != abstain) and selective risk R = P(a != Y | a != abstain), assuming a binary action for accepted cases. These metrics must be reported together with positive-class retention P(a != abstain | Y=1) and episode-level sensitivity. Otherwise a policy can achieve superficially low selective risk by abstaining disproportionately on positive cases.

For empirical group-held-out tests, no finite-sample distribution-free risk guarantee is assumed. Calibration is performed only on participants absent from the classifier-fitting group and the final test group. Target coverage is tuned exclusively on calibration participants; actual test coverage remains an outcome, not a constraint secretly enforced using test labels.

## 4. Methods (pilot implementation)

Signals are segmented into two-second windows with one-second stride. Eligible windows require at least 90% valid FoG annotations, and majority-positive labels determine binary outcomes. Per-channel mean, standard deviation, RMS and observed-data fraction are extracted. A histogram gradient-boosting model fits the features, with imputation fit on training participants only. Five outer GroupKFold splits provide participant-held-out testing. For selective experiments, an internal group split allocates disjoint participants to classifier fitting and sigmoid calibration. For each nominal coverage, an uncertainty cutoff based on the calibration distribution selects accepted test decisions.

Data-processing checks identify a discrepancy between the documented timestamp unit and the observed CSV increments. The implementation infers seconds versus milliseconds from positive intersample differences and splits runs at observed timestamp gaps; this behavior requires further audit before final reporting.

## 5. Preliminary Results

The corrected uncalibrated baseline used 2,336 eligible windows from nine distinct participant IDs in the downloaded sensor file, 25.1% labeled positive. Fixed-threshold positive sensitivity ranged from 0% to 54.5% across five participant-held-out folds. The preliminary calibrated selective benchmark did not consistently improve Brier scores. At a nominal 80% coverage target, realized test coverage ranged approximately from 74% to 96%, and sensitivity among accepted positives was 0% in two folds. These failures preclude any conclusion of improved clinical safety. Five folds drawn from only nine participants are inadequate for robust inferential claims. The accompanying clinical metadata includes 22 participant entries, a discrepancy requiring reconciliation with the provider. Reproducibility details and corrections appear in the dataset audit and results reports.

An independent annotation audit identifies 28 contiguous positive FoG episodes in the sensor file, distributed across only five participants; four participants have no observed positive episodes. The 2,392.15 seconds of annotated recording time and concentrated episode distribution severely limit statistical power.

A subsequently implemented source-order, end-of-window event evaluation detected 14 of the 28 reference episodes, with 56 unmatched alert runs across the annotated observation time. An exploratory two-second gap-merging rule preserved the 14 detected episodes while reducing unmatched alert runs to 36. This is a post-hoc engineering ablation, not an independently confirmed safety gain. The method still misses half of the annotated episodes and creates substantial alert burden. The manuscript must evaluate quality-aware supervision on distinct held-out data and report subject-level uncertainty before claiming an advance.

A first three-action quality-aware pilot selected alert thresholds using disjoint validation participants with a target 80% positive-window recall. Against a comparator trained on the same restricted fitting participants, the pilot increased detected episodes from 5 to 23 but also increased unmatched alert runs from 11 to 91. The selected threshold approached zero in several folds. This adverse tradeoff demonstrates that validation-window sensitivity alone is insufficient as a clinical risk objective. These exploratory analyses do not support a positive safety claim; the intended contribution must involve explicit event-level alert burden constraints and uncertainty about their feasibility under participant shift.

An additional event-level threshold-feasibility study required at least 70% episode sensitivity and at most 30 false alert runs/hour on internal validation participants. Four of five outer folds were infeasible under a fixed candidate grid. The one feasible validation threshold missed the held-out test episode. The result supports explicit feasibility reporting and cautions against interpreting empirical validation constraints as out-of-distribution safety guarantees. These thresholds are exploratory research criteria, not clinically established operating limits.

To probe cross-dataset shift without target label tuning, a Daphnet-trained trunk accelerometer classifier was evaluated on FoG-STAR back accelerometer features. Target AUROC was 0.3488 and fixed-threshold positive sensitivity was zero across 2,263 eligible target windows. Source held-out fold AUROCs ranged from 0.6780 to 0.8423, although source threshold sensitivity was also weak. Direct transfer therefore failed. Sensor orientation, placement, activities and participant differences confound attribution, and no specific causal source of the failure has been established. This test is an external distribution-shift stress test, not clinical validation.

## 6. Discussion and Limitations

**Source-calibrated score-warning pilot:** Using the empirical 95th percentile
of five Daphnet participant-held-out score ECDF distances yielded a cutoff
of 0.1871. Six of nine FoG-STAR participants exceeded the cutoff. However,
source calibration used pooled held-out folds whereas the target application
used individual participant scores. Their comparison is not distributionally
matched; a nominal 95th percentile from only five folds does not confer a
valid patient-level error rate. This result is a post-hoc hypothesis-generating
pilot, not a validated shift alarm. See `CALIBRATED_DRIFT_RESULTS.md`.


**Label-free output-shift follow-up:** The Daphnet-fitted magnitude classifier
assigned mean predicted FoG probabilities of 0.0955 to its training windows
and 0.0584 to FoG-STAR windows. The score ECDF sup distance was 0.1437.
Source-score summaries are in-sample, target scores are out-of-sample, and
overlapping windows are dependent. These descriptive differences might prompt
additional scrutiny but do not constitute a calibrated failure detector or
establish any alerting threshold. See `SCORE_DRIFT_RESULTS.md`.


The principal pilot finding is a warning about treating confidence-based abstention as inherently beneficial. Interparticipant differences may cause severe miscalibration and asymmetric acceptance of negative versus positive cases. The evaluation is limited by a small patient sample, overlapping correlated windows, artificial task conditions, absence of event-level validation and uncertain cross-dataset compatibility. Event sensitivity, false alarms per hour, timing and quality-aware supervision must be evaluated before deployment claims. Clinical governance, fairness and usability are future research questions, not validated outcomes of this work.

## 7. Conclusion (provisional)

Preliminary FoG-STAR experiments motivate a control-inspired framework that treats model uncertainty as a signal for scrutiny rather than automatic trust. Before drawing affirmative conclusions, further work must demonstrate reproducible improvements in accepted error while preserving positive-event retention, under participant and sensor shift.

## Verified starting references (to expand to >=30 before submission)

1. Borzi, L., et al. FoG-STAR wearable and clinical dataset, Zenodo, 2025, https://zenodo.org/records/17037669.
2. Daphnet Freezing of Gait, UCI Machine Learning Repository, dataset 245, https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait.
3. Varghese, J., et al. Machine Learning in the Parkinson's disease smartwatch (PADS) dataset. *npj Parkinson's Disease* 10, 9 (2024). https://doi.org/10.1038/s41531-023-00625-7.
4. Deep Learning for Freezing of Gait Detection: Cross-Dataset Validation Reveals Critical Deployment Gaps Between Laboratory and Daily Living Wearable Monitoring (2026). https://pmc.ncbi.nlm.nih.gov/articles/PMC12944384/.
5. Self-Explaining Neural Networks for Transparent Parkinson's Disease Screening (2026). https://pmc.ncbi.nlm.nih.gov/articles/PMC13165671/.

**Author checklist:** no fabricated experiments; no clinical efficacy claims; verify each final citation and its metadata; enforce ACM page limit; prepare original figures with consistent typography; review GenAI disclosure instructions; retain anonymization.
# Orientation-invariant transfer follow-up (exploratory)

In a post-hoc analysis motivated by the failure of an accelerometer-only
Daphnet-to-FoG-STAR model, three rotation-invariant acceleration-magnitude
features were compared with the original 12-feature representation. Mean
five-fold participant-grouped Daphnet AUROC increased from 0.751 to 0.816,
but FoG-STAR AUROC remained poor (0.349 versus 0.354) and sensitivity at the
fixed 0.5 threshold remained zero for both models. Label-free standardized
mean differences for magnitude mean, magnitude SD, and magnitude-difference
RMS were +0.167, -0.385, and -0.478, respectively. This result is exploratory
because the original external target outcomes were already inspected before
designing the orientation-invariance experiment. It supports analysis of
generalization failures but is not prospective validation.

