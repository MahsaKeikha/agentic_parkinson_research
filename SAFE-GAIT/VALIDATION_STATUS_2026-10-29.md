# SAFE-GAIT validation status — 29 October 2026

## Verified CI evidence
- [Gold Standard CI, run 40836605827](https://github.com/MahsaKeikha/agentic_parkinson_research/actions/runs/40836605827): **success** for all three tested Python matrix jobs (3.10, 3.11, 3.12).
- [SAFE-GAIT research checks, run 40836605839](https://github.com/MahsaKeikha/agentic_parkinson_research/actions/runs/40836605839): **success**.
- The preceding issue was an unused NumPy import reported by Ruff in `test_event_baseline.py`; the fix now passes the broader quality workflow.
- The runner now records input SHA-256 hashes, per-step outputs and failure states, and refuses preexisting result JSON files. These are *software reproducibility checks*, not evidence of model validity.

## Limits that remain
- Full FoG-STAR v3 raw file bytes have not been verified and processed in this research session. The published full dataset is not the same as the historical nine-participant analysis.
- The paper-reported 101 expert events have not yet been independently reconciled to the `fog` binary series, recording gaps and window-eligible events.
- Earlier exploratory target experiments were inspected repeatedly; subsequent analyses are not untouched confirmatory evaluations.
- Publication bibliography is incomplete; passing draft-mode citation checks does not mean final references are verified.
- Full-v3 tables, publication figures and final ACM PDF cannot be represented as completed.

## Full-v3 verification protocol
1. Obtain verified individual file listing/checksums from the official Zenodo v3 record; validate actual source files against independently obtained manifest.
2. Require provenance audit PASS and document timestamp unit and annotation coding.
3. Execute `episode_reconciliation.py`, compare per-subject run totals with the data-paper episode conventions, and review discrepancy with clinical domain expert.
4. Execute `run_verified_v3.py` only on validated files with a fresh output directory; archive result JSON and run manifest.
5. Inspect model results, subject-wise error distributions, event-tolerance sensitivity and alert burden. Report negative findings unfiltered.
6. Regenerate figures from archived JSON outputs and complete citation-by-claim review, then compile and inspect ACM PDF.

**Claims policy:** Never convert automated test success into a clinical or external-generalization claim.
