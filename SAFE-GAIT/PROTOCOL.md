# SAFE-GAIT: Risk-Aware and Explainable AI for Freezing-of-Gait Detection

**Research protocol v0.2, 28 October 2026**  
**Target:** ACM TRUST 2027, REED-AI track  
**Status:** Preregistered-style analysis plan; no results are claimed.

## Research objective

Determine whether a calibrated, quality-aware selective classifier can reduce errors among automated freezing-of-gait (FoG) decisions while retaining clinically useful event sensitivity, compared with conventional wearable-sensor classifiers.

This is **FoG detection** from recorded movement, not prediction of impending episodes, diagnosis of Parkinson's disease, fall prevention, or validation in home deployment.

## Data sources and provenance

1. **FoG-STAR**: Borzi et al., Zenodo DOI `10.5281/zenodo.16989602`; v2 record https://zenodo.org/records/17037669. Twenty-two participants, 60 Hz, synchronized ankle/back/wrist accelerometer and gyroscope signals, binary annotated FoG, activity/task and participant IDs. Verify newest stable release and checksum before analysis.
2. **Daphnet Freezing of Gait**: UCI dataset 245, https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait. Ten participants recorded with three accelerometers at hip and leg sites. Treat as a **sensor-placement and protocol shift**, not a matched external clinical cohort.

No downloaded data, training results, statistical significance, or comparative gains are claimed in this protocol.

## Primary endpoint

The *subject-held-out* **selective error among accepted windows**, assessed jointly with coverage and FoG event sensitivity. Report a full risk-coverage curve; prespecify at least one target coverage from validation data only, such as 80%, subject to support in the sample. Both false-positive and false-negative classes contribute to risk; additionally report asymmetric cost sensitivity over an explicit grid, without claiming a clinically established utility ratio.

## Secondary endpoints

- Event sensitivity and precision; event definitions and matching tolerance must be frozen before testing.
- False alerts per sensor-recording hour, not per window; count contiguous alert runs as a single alert after an explicitly chosen refractory period.
- Event-onset detection latency in seconds, with missed events separately counted.
- Window-level AUPRC, AUROC, sensitivity, specificity, macro-F1 and balanced accuracy.
- Calibration: Brier score, reliability diagrams and ECE with uncertainty intervals.
- Sensor quality vs uncertainty and abstention, simulated missing sensor channels, additive noise, dropout, rotation and sampling mismatch.
- Explanation faithfulness (perturbation/deletion tests), stability (small input perturbations), and domain plausibility of spectral and temporal features, avoiding claims of causal interpretation.

## Data handling

1. Load CSV, check column names, participant and session counts, units, sampling rate, annotations, missingness and timestamps against dataset documentation.
2. Exclude samples that have no valid FoG/non-FoG annotation; do not silently assign labels to unannotated records.
3. Segment into fixed 2-second windows with 50% overlap as an initial configuration, fixed by validation only. Assign a positive window when at least 50% of its *valid* samples carry a FoG annotation; also report sensitivity to alternative event/window labeling.
4. Avoid filtering across test/train subject boundaries or segment gaps; fit any normalization on training subjects only. Derive missingness and signal quality before imputation.
5. Split by `subjectID`, never by randomly sampled windows. Maintain a subject-level locked test partition and use group-aware internal cross-validation. Because there are only 22 people, report results from subject-wise held-out folds as the primary analysis and carefully handle calibration within each outer fold.
6. Prevent leakage from clinical measurements, patient IDs, and task labels into models intended to infer FoG from sensor input alone. Task labels may be used solely for evaluation strata, unless a separately named task-aware model is evaluated.
7. Publish preprocessing code and seeds; do not distribute identifiable clinical records beyond license permissions.

## Models and ablations

- Hand-engineered accelerometer features + logistic regression / random forest / gradient boosting.
- One-dimensional CNN as temporal baseline.
- CNN + posthoc temperature scaling (or an appropriately chosen calibrated score model).
- CNN + calibrated selective policy (abstention based on uncertainty).
- SAFE-GAIT: temporal model + calibrated score + quality-aware risk supervisor + signal feature explanation.
- Ablate calibration, quality signal, abstention, and feature explanation separately. Explanations are independently evaluated, not credited merely because they are produced.

**Safety supervisor:** actions `{alert, no alert, abstain}` chosen by a policy using calibrated FoG score, predictive uncertainty, and sensor quality. Its target utility and threshold are fit using validation participants only. Report risk and coverage jointly: trivial abstention on every sample does not count as success.

## Statistical plan

- Perform group-aware outer validation; use nested group-aware splits for tuning and calibration. Avoid treating overlapping windows as independent samples.
- Bootstrap participant-level units, respecting the fold structure where possible, to estimate 95% uncertainty intervals. Label confidence intervals as exploratory when the effective patient sample is very small.
- Compare paired participant-level results against each baseline. Preselect one primary comparison and endpoint; treat all other tests as secondary with multiplicity considered.
- Report positive prevalence, number of evaluable episodes, duration, class balance per fold, and failures to converge.
- Evaluate cross-dataset transfer only on carefully mapped comparable channels and signal transforms, without fitting any transforms on the target test labels. Document incompatibilities explicitly.

## Limits and ethical boundary

Dataset recordings are controlled motor tasks. Neither dataset demonstrates continuous in-home performance, prospective clinical benefit, caregiver usability, fairness across representative demographic subgroups, or safe autonomous intervention. A human review workflow is a proposed design, not a tested clinical workflow. Any formal selective-risk or conformal guarantee requires explicit exchangeability and calibration assumptions; cross-domain shift can break those assumptions.

## Initial paper organization (ACM sigconf, <=9 pages plus references/disclosure)

1. Introduction and contributions
2. Related work and concrete gap versus calibrated and explainable Parkinson's classifiers
3. Problem definition and operational risk metrics
4. SAFE-GAIT architecture and decision policy
5. Datasets, harmonization, splits, baselines and statistical analysis
6. Results: detection, selective risk, robustness, ablations, explanations
7. Limitations, responsible deployment and human oversight
8. Conclusion

## Minimum result tables to generate

1. Dataset audit (participants, events, valid/invalid time, prevalence, channel completeness)
2. Subject-independent baselines (event and window metrics, CIs)
3. Risk-coverage at validation-defined operating points
4. Robustness under predefined perturbations
5. Ablation and explanation faithfulness
6. External Daphnet transfer, separately labeled as shifted-domain analysis

## References for verification

- Borzi et al. FoG-STAR (Zenodo 2025), https://zenodo.org/records/17037669
- Daphnet Freezing of Gait, UCI, https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait
- Varghese et al. Machine Learning in the Parkinson's disease smartwatch (PADS) dataset, *npj Parkinson's Disease* 10:9 (2024), https://doi.org/10.1038/s41531-023-00625-7
- Deep Learning for Freezing of Gait Detection: Cross-Dataset Validation Reveals Critical Deployment Gaps Between Laboratory and Daily Living Wearable Monitoring (2026), https://pmc.ncbi.nlm.nih.gov/articles/PMC12944384/
- Self-Explaining Neural Networks for Transparent Parkinson's Disease Screening (2026), https://pmc.ncbi.nlm.nih.gov/articles/PMC13165671/
- ACM TRUST 2027 author guidance, https://eigtrust.acm.org/trust2027/authors-guidelines/

## Immediate research gates

- [ ] Verify dataset release, license, checksum and download
- [ ] Inspect schema and patient counts; identify sampling gaps and label semantics
- [ ] Freeze evaluation and decision thresholds before locked testing
- [ ] Train subject-independent baselines and audit errors
- [ ] Implement and compare calibrated selective policy
- [ ] Perform robustness and external-shift tests
- [ ] Replace proposal claims with measured outcomes and at least 30 fully verified references
