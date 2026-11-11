# SAFE-GAIT adversarial conference review — blocking issues

Status: internal pre-submission review; NOT an acceptance prediction. The PaperPlaza thank-you note for reviewing an ACC paper contains no rejection reasons for the author's own manuscript.

## Reviewer decision at current evidence level
**Major revision / not submission-ready.** A technical-review draft is available, but a scientifically defensible submission requires empirical validation and a sharply bounded contribution.

## Ranked objections and acceptance criteria
1. **Insufficient demonstrated novelty.** A source-to-target degradation example, standard abstention, and ECDF drift warnings are not individually new. Articulate the testable contribution as an operational failure audit and calibration-unit sensitivity; compare to prior cross-dataset FoG studies and selective prediction. Do not claim a new safety guarantee.
2. **Unverified dataset and endpoint validity.** Full FoG-STAR v3 SHA-256 manifest, expert episode reconciliation, participant/session/task audit and exclusions must be present. Binary positive-label runs cannot silently replace expert clinical episodes.
3. **Uncorrected event estimates.** Historical 0/28 matches, 6 vs 5 unmatched alerts, and warning fractions must be labeled historical; recompute using corrected causal window-end timestamps and maximum-cardinality one-to-one matching. Independently test the evaluator.
4. **Weak comparators.** Run identical-cohort, identical-clock time-domain, magnitude, spectral and at least one documented published or strong comparator. Clearly label any adaptation.
5. **Operating-point selection and leakage.** Freeze source-only threshold, preprocessing, model selection and gates. Prior target inspection prevents calling full-v3 evaluation untouched confirmation. Publish threshold sensitivity without choosing favorable target outcomes.
6. **Statistical fragility.** Report per-participant outcomes and participant-clustered uncertainty, undefined estimates and evaluable bootstrap counts; avoid independent-window confidence intervals or broad clinical generalization.
7. **Alert policy ambiguity.** Specify event matching, hold time, tolerance, merging, exposure denominator, zero-window episodes, and abstention consequences; include protocol-sensitivity analyses.
8. **Unsupported safety language.** No claim of patient benefit, clinical safety, real-time suitability, or prospective monitoring from retrospective recordings.
9. **Literature and venue fit.** Verify all DOI, authorship and bibliographic metadata; show what existing FoG cross-dataset papers and warning/calibration literature do and do not establish. Confirm ACM track relevance and formatting policies.
10. **Paper artifacts not traceable.** Every number in abstract, tables and figures must map to an immutable run ID, verified input hashes, script commit, and generated result. A successful CI/PDF build is not experimental validation.

## Reviewer-facing paper structure
- Introduction: decision-relevant failure mode, precise gap, bounded contributions.
- Related work: cross-dataset FoG transfer, event-based evaluation, reject options and shift warnings.
- Dataset/provenance: full release vs historical subset, episode semantics, acquisition mismatch.
- Methods: frozen causal event policy, comparator parity, calibration units and uncertainty.
- Results: subject-level table, event recall and unmatched alerts/hour, coverage, warning audit, sensitivity grid, uncertainty; no fabricated values.
- Discussion: why observed failure occurs only as hypotheses; limitations and no clinical inference.
- Reproducibility: public protocol, manifest hashes, environment, executable commands and traceable outputs.

## Release rule
Do not describe SAFE-GAIT as scientifically submission-ready until all blocking empirical, provenance, comparison, citation and artifact checks are independently verified. A negative result can be publishable if it is reproducible, appropriately contextualized and novel in what it establishes.
