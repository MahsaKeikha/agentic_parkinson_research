# FoG-STAR v3 release verification — 2026-10-30

Official record: https://zenodo.org/records/17838806
Scientific Data descriptor: https://doi.org/10.1038/s41597-026-06645-1

## Officially published file-level identifiers (NOT locally revalidated)
- sensor_data.csv: MD5 `952a37ab147da35e6d4e7a1e9bac44cb`
- clinical_data.csv: MD5 `8b9a2339c8fcb8eaa470bcb1784d31c5`
- The original scientific descriptor reports 329027 sensor rows and 31 columns, 22 participants, 60 Hz.
- Official dataset README defines `timestamp` in **milliseconds**. Do not treat this as seconds.
- The clinical CSV is documented to contain 22 subjects and 10 fields. The sensor CSV is ~119.6 MB.
- Checksums are sourced from the v3 Zenodo record, *not* measured against local downloaded files in this session.

## Critical no-run gate
`cross_dataset.py` and `cross_dataset_invariant.py` currently interpret target timestamps in **seconds**. `cross_dataset_events.py` now accepts an explicit `--timestamp-unit` option. `run_verified_v3.py` currently rejects `ms` to prevent silently wrong results in the first two scripts.

**Do not bypass this gate** by falsely declaring v3 timestamps to be seconds. Before running the full release, implement and test a consistent explicit ms-to-s conversion in both classification loaders, and verify complete release file hashes and the manifest. The official data paper's episode counts are separate from binary label-run counts.

## Recommended audit manifest fields
```json
{
  "sensor": {"md5": "952a37ab147da35e6d4e7a1e9bac44cb", "rows": 329027, "columns": 31},
  "clinical": {"md5": "8b9a2339c8fcb8eaa470bcb1784d31c5", "rows": 22, "columns": 10},
  "subject_count": 22
}
```
This manifest contains author-published expectations only. A provenance PASS requires reading the actual downloaded bytes and cross-checking these values locally.
