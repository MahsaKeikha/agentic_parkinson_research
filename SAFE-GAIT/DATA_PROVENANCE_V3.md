# FoG-STAR v3 provenance gate — 28 October 2026

**Status:** official manifest checked; full 119.6 MB CSV has NOT yet been locally processed in this phase. No full-v3 performance measurements are claimed.

## Primary source
- Official release: https://zenodo.org/records/17838806 (v3, DOI 10.5281/zenodo.17838806).
- Scientific Data article: https://doi.org/10.1038/s41597-026-06645-1 (2026).
- Official release lists 22 subjects, 60 Hz, 31 sensor columns; sensor file MD5 `952a37ab147da35e6d4e7a1e9bac44cb`, clinical file MD5 `8b9a2339c8fcb8eaa470bcb1784d31c5`.
- Publication reports 329,027 sensor rows and 101 annotated freezing episodes. These are *paper-reported*, not independently verified against v3 here.
- Historical analysis was based on an earlier release/download with 143,530 rows, nine distinct sensor subject IDs and 28 label runs under project segmentation. It is not a full cohort benchmark.

## Why episode counts can differ
The paper's clinician-annotated FoG events need not equal the number of contiguous binary-positive runs after splitting at recording gaps or changing event-matching conventions. Do not silently redefine the article's 101 episodes from a simple positive-run count.

## Verification workflow
1. Download both CSV files from the official v3 Zenodo record into a local `data/` directory ignored by Git.
2. Run `python audit_fogstar_v3.py --sensor-data data/sensor_data.csv --clinical-data data/clinical_data.csv --out results/fogstar_v3_audit.json`.
3. Inspect row count, 31 columns, sensor and clinical identifiers, checksums, and timestamp discontinuities. Any failure of the manifest gate means **STOP**, not silent correction.
4. Compare groupwise positive-run summaries against expert-annotated episodes using the authors' notebook `FoG_Star_Analytics.ipynb` and clinical publication.
5. Re-run grouped subject-independent experiments on v3. Record exact hashes, fold IDs, parser revisions and model seeds.
6. Because earlier FoG-STAR labels have already been inspected, new v3 analyses are **not an untouched independent external confirmation** without an independent dataset.

The README describes timestamps as milliseconds but earlier parser audits observed increments suggesting seconds; this mismatch must be investigated explicitly before all new event analyses.
