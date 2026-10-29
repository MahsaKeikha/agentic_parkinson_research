# Publication graphics: data provenance and reporting standard

Three publication-style figures were generated from documented **historical exploratory aggregate values**, not new predictions and not the complete v3 release.

1. **Source vs target AUROC:** Daphnet source grouped mean AUROC 0.7512 (12 features), 0.8160 (three magnitude features); FoG-STAR historical nine-person subset AUROC 0.3488 and 0.3538. Sources: `CROSS_DATASET_RESULTS.md`, `ORIENTATION_INVARIANT_RESULTS.md`.
2. **Calibration-unit warning counts:** pooled folds 6/9 flagged, matched single-person holdout 1/9 flagged. Sources: `CALIBRATED_DRIFT_RESULTS.md`, `PARTICIPANT_DRIFT_RESULTS.md`.
3. **Unmatched alerts per annotated hour:** no gate 9.03, source-retention 80% 7.52, 90% 7.52, 95% 9.03; 0/28 episodes detected in every case. Source: `CROSS_DATASET_EVENT_RESULTS.md`.

The vector figures and generation script are supplied as a reproducibility archive alongside the ChatGPT result. **Do not** use these graphics to support full-v3 or independently validated performance claims.

Graphics conventions: consistent vector typography, zero-based bar axes, plotted values printed directly, exploratory cohort identified in notes, no fictitious confidence bars, no unreported p-values, no clinical safety claim.

## Manuscript figure captions

**Fig. 1.** Source-internal discrimination compared with cross-dataset FoG-STAR subset performance for two feature representations. The source and target cohorts differ in participant composition, sensor site and tasks. Means across source grouped folds are descriptive. The figure is not a matched-patient performance comparison.

**Fig. 2.** Number of target participants exceeding a source-score distribution shift warning under pooled-fold versus individual-participant calibration. The calibration units are not identical; the warning rate is not calibrated for a prospective patient-level false-positive rate.

**Fig. 3.** Unmatched alert burden under source-only feature-distance abstention. All evaluated configurations detected zero of 28 annotated episodes under the historical zero-tolerance alert-timing convention. A decrease in unmatched alert counts is not evidence of increased clinical reliability.

## Figure replacement policy
Figures must be regenerated from **versioned v3 aggregate result JSON files** once checksums, participant counts, event annotations and timing conventions pass independent review. Historical images must never be silently relabeled as v3.
