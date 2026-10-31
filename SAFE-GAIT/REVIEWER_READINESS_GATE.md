# SAFE-GAIT reviewer-readiness and verification gates

**Research stage:** exploratory, not clinical or confirmatory validation. Explicit STOP conditions below must be resolved before submitting numerical full-cohort claims.

## 1. Provenance (blocking)
- [ ] Retrieve complete v3 Zenodo record 17838806 and preserve exact downloadable file names and identifiers.
- [ ] Verify raw sensor and clinical file digests; record actual file shape, subjects, sessions, tasks, annotation codes and time units.
- [ ] Reconcile 329,027 paper-reported rows, 22 participants and 101 reported episodes with actual sensor rows and annotation conventions.
- [ ] Explain the historical 143,530-row and 9-participant subset and whether it represents a partial download or a documented subset.
- [ ] Freeze dataset snapshot hash and inclusion/exclusion policy before reporting reruns.

## 2. Causality and leakage (blocking)
- [ ] Split by participant for all trained transforms, feature selection, calibration, threshold tuning and uncertainty estimation.
- [ ] Separate model-development, validation and external test sets. FoG-STAR already inspected is *not* untouched test data.
- [ ] Verify model score assigned only at window completion; no pre-onset prediction claim.
- [ ] Verify alert-run construction and protocol sensitivity to its assumed duration, refractory merge and matching tolerance.
- [ ] Count episodes that cannot be detected by the window schedule; report eligible-event denominators separately from all episodes, never silently omit short events.
- [ ] Ensure source-derived warning cutoff does not use target labels or target tuning.

## 3. Metrics and inferential validity (blocking)
- [ ] AUROC, AUPRC, fixed-threshold sensitivity/specificity; distinguish discrimination from real-world operating point.
- [ ] Raw-event TP/FN, unmatched alert runs/hour, latency for detected episodes, abstained positive windows and missed episodes.
- [ ] Aggregate patient-level estimates and intervals by participant, not independent overlapping windows.
- [ ] Compare no-gate, feature-distance gate, pooled score-shift and participant-matched score-shift with identical test protocols.
- [ ] Report infeasible validation constraints explicitly and no false safety guarantees.
- [ ] Provide exact subject-wise results and audit any subject with zero positive events.

## 4. Strong baseline study (blocking for strong acceptance claim)
- [ ] Compare credible frequency-domain FoG baselines and recent externally validated architecture, not only a shallow magnitude classifier.
- [ ] Control sampling frequency, placement and units; justify any impossible sensor-matching assumptions.
- [ ] Repeat main conclusions with alternative models and exposure denominators.
- [ ] Preregister main analysis on an independent dataset; document all post-hoc analyses as exploratory.

## 5. Manuscript and reproducibility
- [ ] Verify every reference metadata field from publisher/DOI or primary indexed record.
- [ ] Complete at least 30 relevant citations **without padding**; 30 candidates are not 30 verified final references.
- [ ] Produce figures from versioned aggregate analysis outputs; never hand-draw results curves.
- [ ] Compile ACM review LaTeX, inspect the resulting PDF, fix warnings, tables, legibility and citation resolution.
- [ ] Verify venue page limits, anonymity, research-ethics disclosures, data licenses and AI-use policy.
- [ ] Have a FoG clinician validate what constitutes an actionable detection and sensible alert-timing tolerance.

## Scientific red lines
No clinical-readiness claim; no false prospective claim; no significance tests on overlapping windows as independent data; no substitution of naive binary-label runs for published annotated episode definitions; no unverified numeric result from full v3.
