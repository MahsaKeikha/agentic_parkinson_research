# Evidence traceability and CI status — 29 October 2026

## Actual GitHub execution

GitHub workflow run [40834400300](https://github.com/MahsaKeikha/agentic_parkinson_research/actions/runs/40834400300) completed successfully for commit `3934339e47ddb3273d6cfb91aff2c9dcf9a695b4`.

- 45 research tests passed (Python `unittest` discovery under `SAFE-GAIT/`).
- 4 manuscript-preflight unit tests passed (explicit `SAFE-GAIT/paper/` discovery).
- Paper preflight completed in **draft** mode, not strict mode.
- Draft-preflight warnings: `fogstar2026`, `bachlin2010`, `lin2026` have incomplete bibliography metadata; only five BibTeX entries exist. These are **outstanding blocking corrections** for the final paper.
- Raw-data tracking check passed. This is a path-pattern safeguard, not a complete privacy audit.

## Claim-to-evidence ledger

| Claim | Report/code provenance | Dataset scope | Verification status |
|---|---|---|---|
| Nine sensor IDs, 143,530 CSV rows | `EVENT_AUDIT.md`, checksum/CSV audit | Historical release/subset | Historical observation; NOT verified full v3 |
| 28 annotated positive runs | `EVENT_AUDIT.md`, `event_audit.py` | Historical subset | Needs expert-event convention reconciliation |
| 12-feature source CV mean AUROC ~0.751, target AUROC ~0.349 | `CROSS_DATASET_RESULTS.md`, `cross_dataset.py` | Daphnet to historical FoG-STAR subset | Exploratory; target previously inspected |
| 3-feature source CV ~0.816, target AUROC ~0.354 | `ORIENTATION_INVARIANT_RESULTS.md`, `cross_dataset_invariant.py` | Daphnet to historical FoG-STAR subset | Exploratory, post-hoc |
| End-of-window 0/28 events detected, 6 unmatched alerts | `CROSS_DATASET_EVENT_RESULTS.md`, `cross_dataset_events.py` | Historical subset | Assumed alert hold 1 second, zero matching tolerance |
| Feature-distance gate 5 unmatched alerts, 0/28 events | `CROSS_DATASET_EVENT_RESULTS.md` | Historical subset | Exploratory; no safety benefit established |
| Pooled-fold warning flagged 6/9 | `CALIBRATED_DRIFT_RESULTS.md`, `calibrated_drift.py` | Historical subset | Calibration unit mismatched; not a clinical warning statistic |
| Matched-person warning flagged 1/9 | `PARTICIPANT_DRIFT_RESULTS.md`, `participant_drift.py` | Historical subset | Unit corrected, small-sample and post-hoc; not confirmatory |
| Full v3: publication describes 22 subjects and 101 episodes | Scientific Data source, Zenodo 17838806 | Published full dataset | Publication-reported only, not yet independently reproduced from raw v3 |

## Manuscript acceptance gates

1. **STOP for primary experiment** until official full v3 raw-file manifest and exact data bytes are validated. The same checksum was previously reported alongside inconsistent row counts and must not be accepted unquestioningly.
2. Freeze inclusion criteria, subject groups, timestamp scale and raw-event conventions on v3 before any new model analysis.
3. Keep the subject held out across every training, normalization, calibration and threshold-selection stage.
4. Report detected and missed events, false alerts per annotated hour, event timing sensitivity, source coverage, target coverage, and patient-wise results.
5. Compare strong published detectors and feature-processing baselines. An exploratory shallow model's failures do not prove all cross-dataset FoG classifiers fail.
6. Convert bibliography candidates into complete, original-source-checked BibTeX records. Run the **strict** citation preflight and ACM PDF compilation, with no warnings.
7. Regenerate every figure directly from versioned aggregate JSON and inspect PDF/SVG outputs. Historical exploratory figures must retain their subset disclaimers.
8. Independent evaluation is necessary for prospective/generalization claims because existing target information influenced post-hoc experiments.

**Interpretation:** Passing 49 automated tests establishes current code/test consistency. It does not establish clinical utility, robustness to a new cohort, completeness of source data, correctness of every citation, or likelihood of acceptance.
