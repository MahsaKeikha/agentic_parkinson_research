# SAFE-GAIT: full FoG-STAR v3 reproducibility protocol

This protocol is **not** a claim that the full dataset has already been analyzed.

## 1. Download into a private directory outside the repository

```bash
python SAFE-GAIT/download_official_v3.py --destination /path/to/private/fogstar-v3
```

The downloader reads metadata from Zenodo record 17838806, requires the two exact dataset filenames and pinned MD5 checksums, streams downloads into temporary files, and renames them only after checksum verification. Network access and sufficient local disk space are necessary. The script never adds raw participant data to git.

## 2. Supply the official manifest

Write `/path/to/private/fogstar-v3/manifest.json` with this content:

```json
{
  "sensor": {"md5": "952a37ab147da35e6d4e7a1e9bac44cb", "rows": 329027, "columns": 31},
  "clinical": {"md5": "8b9a2339c8fcb8eaa470bcb1784d31c5", "rows": 22, "columns": 10},
  "subject_count": 22
}
```

These are expected official release values, **not** measurements made in our environment. The executable audit checks actual files.

## 3. Place authorized Daphnet source recordings in a separate private directory

Use the original `S??R??.txt` recordings, not a synthetic substitute. Inspect data-use terms before downloading or sharing any files.

## 4. Execute and archive

```bash
python SAFE-GAIT/run_verified_v3.py \
  --sensor-data /path/to/private/fogstar-v3/sensor_data.csv \
  --clinical-data /path/to/private/fogstar-v3/clinical_data.csv \
  --manifest /path/to/private/fogstar-v3/manifest.json \
  --daphnet-dir /path/to/private/daphnet \
  --timestamp-unit ms \
  --out /path/to/private/results/full-v3-run-001
```

The output directory must be clean. The orchestrator verifies the pinned full-v3 manifest, checks actual checksums and shapes, rejects wrong sampling units, records input/output SHA-256 hashes and per-step failures, and executes the three retrospective analyses. All results are **post-hoc exploratory**, not prospective clinical validation.

## 5. Manuscript acceptance gate

Do not replace historical findings until all three result JSON files and the final run manifest exist and are inspected. Cross-check patient counts, per-subject event totals, undefined metrics, event-matching policy, source window counts, and false-alert exposure units. Expert-determined 101 episodes are **not necessarily identical** to contiguous binary label runs. Discrepancies need annotation-level investigation, not numerical forcing. A new, untouched external cohort would still be required for independent confirmation.

## Current environment limitation

Zenodo could not be reached from the execution container during the October 30, 2026 session. No complete official v3 data were downloaded or hashed, and no full-v3 empirical results have been produced by these steps.
