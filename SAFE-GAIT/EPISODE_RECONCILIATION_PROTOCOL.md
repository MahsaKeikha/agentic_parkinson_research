# FoG-STAR episode reconciliation protocol

**29 October 2026 — awaiting complete v3 raw files.**

An independent `episode_reconciliation.py` plus six passing synthetic tests were created in the attached reproducibility package. The code is not yet committed to the repository; this file specifies the adopted protocol.

## Critical distinction
Three different quantities must not be conflated:
1. **Published clinician-annotated episodes**: the FoG-STAR *Scientific Data* article reports 101 for its full cohort.
2. **Contiguous runs of binary `fog==1` labels**: depends on actual input rows, recording boundaries, timestamp units and gaps; not necessarily equal to clinical episodes.
3. **Detector-eligible reference events**: events capable of being detected by the designated window and decision schedule; eligibility must be reported separately and never silently excluded from overall sensitivity.

## Deterministic reconciliation
- Require explicit `--timestamp-unit s|ms` rather than auto-inferring from timestamp step.
- Preserve CSV row order; split at every change to subject, session or task, and at nonincreasing timestamps or gaps exceeding 1.5 sample periods.
- Within each contiguous block, compute labeled duration, positive sample count, positive label runs and their durations.
- Report boundary reason, block row range and per-subject rollup. No joins with clinical metadata may multiply sensor observations.
- Match to expert event annotations only after the publication's onset/offset convention is independently understood.
- Treat zero-tolerance window-end alert matching as an exploratory convention, not a clinical gold standard.
- Keep complete v3 experiments blocked until verified file manifest checks succeed.

## Local tests completed
Six synthetic tests passed: two runs separated by labels, runs split by gaps, runs split by participant changes, millisecond scale, rejected invalid timestamp unit, and nonincreasing timestamp reset. The tests do not validate the official dataset.

## Sources
- https://zenodo.org/records/17838806
- https://doi.org/10.1038/s41597-026-06645-1

## Planned outputs
`results/fogstar_v3_episode_reconciliation.json` with source file hashes; diagnostic plots from versioned JSON; clinically reviewed annotation mapping; figure captions specifying denominator conventions.
