# Fail-closed FoG-STAR v3 provenance verification

**Release-manifest uncertainty identified:** prior notes assigned the same sensor MD5 to a nine-subject, 143,530-row historical file and a 22-subject, 329,027-row full release. The same exact byte checksum cannot certify different contents. Do not use the prior constant as proof of v3 completeness without retrieving the official API file listing and exact CSV.

The independent audit `provenance_audit.py` and four synthetic tests are distributed in the accompanying ChatGPT research package. This audit requires a separately sourced manifest JSON for each actual file. It verifies individual file MD5 values, rows, columns, participant ID mappings, recording-block timestamps, and reports naive label runs separately from expert episodes. A missing check gives `UNVERIFIED`; a failed check gives `FAIL`; only complete matching checks give `PASS`.

## Experiment gate

No recalculated full v3 classification results can be claimed until the file bytes are available and the manifest returns `PASS`. No existing FoG-STAR exploratory subset result is prospective confirmation. Even after passing, the expert-episode count must be reconciled with the original paper's annotation protocol.

## CLI

```bash
python provenance_audit.py --sensor-data data/sensor_data.csv --clinical-data data/clinical_data.csv --manifest verified_manifest.json --out results/provenance_audit.json
python -m unittest -v test_provenance_audit.py
```

The manifest must be constructed from the official release's individual file entries rather than from assumptions based on the publication abstract. It supports `sensor` and `clinical` objects with `md5`, `rows`, and `columns`, plus `subject_count`. Verify the row/column expectations independently and reconcile differing versions first.

**Local tests performed:** 4 synthetic audit tests passed on 28 October 2026. No complete official v3 file was downloaded or processed in this session.
