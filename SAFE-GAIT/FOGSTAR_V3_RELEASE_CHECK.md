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

## Timestamp conversion status
The model feature loader, the orientation-invariant analysis, the event replay, and the verified runner now accept explicit `s` or `ms` units. The official v3 release requires `--timestamp-unit ms`. All model loaders convert milliseconds to seconds before run splitting. Median sample-period plausibility checks reject wrong-unit declarations.

**Do not run until** local official CSV files and manifest pass the provenance audit. The timestamp code change also requires a fresh passing CI result and an end-to-end execution on real v3 data. Earlier exploratory results are not revalidated by this code change.

## Recommended audit manifest fields
```json
{
  "sensor": {"md5": "952a37ab147da35e6d4e7a1e9bac44cb", "rows": 329027, "columns": 31},
  "clinical": {"md5": "8b9a2339c8fcb8eaa470bcb1784d31c5", "rows": 22, "columns": 10},
  "subject_count": 22
}
```
This manifest contains author-published expectations only. A provenance PASS requires reading the actual downloaded bytes and cross-checking these values locally.
