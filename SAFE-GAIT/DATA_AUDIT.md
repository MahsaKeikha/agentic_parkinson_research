# FoG-STAR Dataset Integrity Audit

**29 October 2026, methodological correction.**

## Verified local sources

- Zenodo v2 `sensor_data.csv`: 119,629,580 bytes, MD5 `952a37ab147da35e6d4e7a1e9bac44cb` (matches published listing).
- Zenodo v3 (https://zenodo.org/records/17838806) is the latest record, and **lists the same sensor file MD5**. Thus upgrading from v2 to v3 does not resolve the nine-versus-22 participant discrepancy; v3 updates accompanying documentation and analysis files.
- Sensor CSV rows: **143,530**.
- Distinct sensor `subjectID` values: **1, 2, 3, 4, 5, 6, 7, 8, 10**, only **9** participant IDs.
- Accompanying `clinical_data.csv`: **22** participant metadata rows. The publication's overall study cohort size must not be substituted for the cohort present in this particular sensor file.
- Median observed sample interval: approximately **0.0166667**, consistent with **60 Hz timestamps expressed in seconds**, despite the accompanying documentation describing milliseconds.

## Reason for correction

An earlier windowing implementation compared the observed ~0.0167 increments to a presumed 16.7-millisecond numerical step, allowing large timestamp gaps to be treated as continuous. Its reported 5,326 windows and 22 participants are marked superseded. Strict timestamp-aware segmentation yields a different evaluation cohort. This supersession is documented to keep the research record auditable.

## Recomputed strict-segmentation baseline

| Value | Corrected result |
|---|---:|
| Sensor participant IDs | 9 |
| Eligible 2-second windows | 2,336 |
| Positive windows | 587 |
| Positive-window prevalence | 25.128% |

| Held-out fold | Windows | Positive | Sensitivity | AUROC |
|---|---:|---:|---:|---:|
| 1 | 565 | 304 | 0.4013 | 0.8283 |
| 2 | 412 | 177 | 0.0056 | 0.6506 |
| 3 | 450 | 89 | 0.0337 | 0.8111 |
| 4 | 455 | 11 | 0.5455 | 0.9115 |
| 5 | 454 | 6 | 0.0000 | 0.8702 |

The large variation in participant-specific prevalence and very low number of positive test windows in folds 4 and 5 make these metrics highly unstable. Do not present pooled window-level confidence intervals as though they represented independent patients.

## Outstanding issues

1. Confirm why the published sensor CSV includes only nine subject IDs while clinical metadata has 22 subjects; inspect current dataset versions and contact maintainers if needed.
2. Audit timestamp discontinuities using original row ordering and session/task markers. Avoid sorting that interleaves repeated timestamps across separately concatenated runs.
3. Generate per-subject event counts, duration, missing-channel rates and per-task overlap before final modeling.
4. Reconsider five-fold testing with such a small effective cohort; leave-one-subject-out descriptive reporting may be more transparent.
5. Do not treat this dataset as a 22-patient wearable cohort until the discrepancy is resolved.
