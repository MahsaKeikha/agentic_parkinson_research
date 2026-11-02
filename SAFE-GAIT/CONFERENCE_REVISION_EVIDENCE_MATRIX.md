# SAFE-GAIT: conference revision evidence matrix (2026-11-02)

This file converts the skeptical reviewer critique into measurable acceptance criteria. It is a specification, not evidence that an experiment has been completed.

| Reviewer weakness | Required deliverable | Current state |
| --- | --- | --- |
| Historical event statistics use old matching and segmentation code | Rerun corrected event evaluator; publish event numerator, denominator and exposure by subject, exact commit and hashes | BLOCKED: data run not executed |
| Full v3 omitted | Verify both Zenodo files against pinned checksum, rows, columns, subject list; freeze inclusion table | BLOCKED: official full data not locally verified |
| Novelty unclear | Compare event-aware audit vs AUROC-only, abstention-only, and pooled-warning-only assessments using common held-out subjects | DESIGNED, not measured |
| Models weak | Add published frequency-domain feature baseline plus at least one stronger reproducible model, fit and select only with source data | NOT DONE |
| Shift warning not validated | Define warning-positive failure as an a priori operational event (e.g. source-chosen minimum event recall, maximum alert burden); evaluate on subjects not used to choose the rule | NOT DONE |
| Uncertainty missing | Report subject-clustered intervals and fold-by-fold source metrics; distinguish undefined AUROC for single-class subjects | NOT DONE |
| Confounding | State sensor sites, physical units, tasks, annotation conventions; add preprocessing ablations and unmatched-placement caveat | PARTIALLY DOCUMENTED |
| Clinical applicability | Provide event latency, alert/h, event recall, source/target abstention coverage and failure costs, avoid medical-device benefit claims | HISTORICAL AGGREGATES ONLY |
| Submission artifacts | Strict citation metadata check, figures tied to JSON, anonymized PDF and inspect final log | PDF CI AVAILABLE; strict bibliography not complete |

## Primary analysis (pre-specification for future exploratory rerun)
- Outcome 1: operational event recall, as matched binary-label runs over all annotated reference runs under one-to-one maximum-cardinality matching; label positive only if explicitly annotated.
- Outcome 2: unmatched alert runs per valid annotated recording hour.
- Outcome 3: participant-matched warning discrimination for **predeclared** reliability-failure outcome; do not interpret mere feature drift as clinical failure.
- Primary decision policy: end-of-window two-second feature extraction, one-second hop, 0.5 fixed source-defined probability threshold, no merging, one-second alert hold, zero tolerance. These define historical replay comparability rather than clinical optimality.
- Sensitivities: 0, 0.25 and 1 s alert hold; 0, 0.5 and 1 s matching tolerance; source-only operating-point sweep. Report all cells, never cherry-pick on target.
- Report zero-denominator quantities as undefined (null) and show counts of excluded/invalid labels and unscorable short segments.
- Separate published expert episodes (author's clinical construct), binary label runs (operational construct) and window-eligible events. A reconciliation table is mandatory.
- Data choices informed by prior FoG-STAR inspection: **post-hoc exploratory**. A new untouched cohort is required for confirmatory external evidence.

## Minimum review package
A frozen code commit, full-v3 manifest audit PASS, per-participant results, source-data manifest, versioned JSON outputs, evidence-to-figure mapping, compiled ACM PDF, complete and verified bibliography, and an explicit data/code-availability statement.

**Stop condition:** No claim of full-v3 or submission readiness without the checks above.
