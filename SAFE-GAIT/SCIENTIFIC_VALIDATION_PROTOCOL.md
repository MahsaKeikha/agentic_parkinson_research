# SAFE-GAIT: scientific validation protocol (prospective execution checklist)

Status: **PROTOCOL ONLY — NOT RESULTS OR SUBMISSION APPROVAL**.
Scope: Daphnet source to full FoG-STAR v3 external evaluation. Historical FoG-STAR subset inspection means the full-v3 analysis is *not* an untouched confirmatory test.

## Gate 1 — provenance (must fail closed)
- Obtain official FoG-STAR v3 files from the dataset's authoritative Zenodo record (17838806), recording DOI, version, retrieval date, licensing, and every file's SHA-256.
- Compare filenames, bytes, participant/session identifiers, channels, units, sample rates, and timestamps against a locked manifest. Preserve raw inputs unchanged.
- Produce an audit table distinguishing published 22 participants / 101 expert episodes from independently observed counts. Never infer that contiguous positive-label runs equal expert-defined episodes.
- Reconcile episode annotations and binary sensor labels, including mixed manifestations, gaps, short events, missing channels, and discontinuities; log every exclusion with reasons.

## Gate 2 — freeze analysis before full rerun
- Record git commit, environment lock, random seeds, inclusion rules, feature definitions, source-grouped folds, trained-model hashes, threshold-selection rules, and no target-label tuning.
- Primary estimand: participant-macro event recall at fixed, source-selected operating threshold and explicitly defined alert matching. Also report pooled matched/eligible events with denominator.
- Report unmatched alert runs per annotated recording hour, positive-event abstention, window AUROC/AUPRC, participant-level distributions, and coverage. Undefined metrics stay missing.
- Predictions are actionable at window end; define one-to-one maximum-cardinality matching with interval overlap. Prespecify whether zero-window events enter the denominator (default: yes).
- Secondary sensitivity grid: alert holds 0, 0.25, 1 seconds and matching tolerances 0, 0.5, 1 seconds. No post-hoc selection of a favorable grid cell as primary.
- Subject-cluster bootstrap with fixed seed and evaluable-replicate counts; also show raw per-subject event numerators and denominators.

## Gate 3 — comparators and falsification
- Run time-domain axis-sensitive, magnitude-only, and seven-feature spectral comparator on identical inclusion sets, clocks, folds and operating-point policy.
- Add a faithfully documented published FoG comparator when its preprocessing and sensor assumptions can be reconstructed; otherwise label it an adaptation.
- Include always-alert / never-alert controls, random-score sanity checks, shuffled-label checks, and threshold sensitivity chosen only from source data.
- Report drift warning participant-level flags separately from episode detection; estimate false-warning behavior on source held-out participants without claiming finite-sample guarantees.
- Analyze differences in sensor placement, task composition, sampling, missingness and medication state where metadata permit; avoid attributing transfer failure to a single cause without identification.

## Gate 4 — independently inspectable outputs
Required artifacts: manifest with verified hashes; provenance audit; frozen protocol/config; exact commands and logs; participant-level predictions and episode-match tables; metrics with uncertainty; exclusions; comparator outputs; figures; reproducible environment; citation audit.
A green GitHub Actions build proves only that specified checks executed, not that official data were available, checksums matched, event endpoints were clinically reconciled, or results are scientifically valid.

## Gate 5 — manuscript release
- Update abstract, methods, tables, limitations and figures from immutable output artifacts, with every numerical claim linked to a run ID and input hashes.
- Cite the FoG-STAR data descriptor and record, source dataset, relevant original FoG methods, selective prediction, and independent cross-dataset robustness studies. Verify bibliography metadata.
- Compile ACM PDF and inspect text, references, tables and figures. Mark the entire full-v3 evaluation exploratory due to prior target inspection.
- Request independent methodological/statistical review and verify conference scope, page limits and policies.

## Decision
**Technical-review draft**: complete coherent methods and clearly labeled historical exploratory results, with all pending experiments disclosed.
**Scientifically submission-ready**: gates 1–5 completed and independently reviewed; any remaining uncertainty explicitly bounded. A null or poor result can be publishable if rigorously validated, transparently reported, and positioned as a negative finding. Never replace missing results with plausible estimates.
