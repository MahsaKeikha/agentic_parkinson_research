# Independent Daphnet FoG Annotation Audit

**29 October 2026. Annotation-only findings, not model performance.**

## Provenance

- Public UCI repository dataset 245: https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait
- Download: `https://archive.ics.uci.edu/static/public/245/daphnet+freezing+of+gait.zip`
- Original dataset authors' documentation: file names `S<subject>R<run>.txt`; 11 columns per line; timestamp in milliseconds; nine accelerometer axes across ankle, thigh and trunk; annotation 0 is outside experiment, 1 is no freeze, 2 is freeze.
- Original citation: Bächlin et al., Wearable Assistant for Parkinson's Disease Patients With the Freezing of Gait Symptom, *IEEE Transactions on Information Technology in Biomedicine*, 14(2), 436-446 (2010).

## Computed audit

| Quantity | Result |
|---|---:|
| Participants | 10 |
| Recorded runs | 17 |
| Contiguous annotation-defined FoG events | 237 |
| Participants with positive events | 8 |
| Participants with no positive events | 2 |

| Subject | Events | Experiment-annotated seconds |
|---|---:|---:|
| 1 | 23 | 1,945.65 |
| 2 | 24 | 1,448.99 |
| 3 | 49 | 2,058.30 |
| 4 | 0 | 2,119.71 |
| 5 | 66 | 2,140.26 |
| 6 | 10 | 2,037.84 |
| 7 | 24 | 1,648.67 |
| 8 | 14 | 788.54 |
| 9 | 27 | 1,781.84 |
| 10 | 0 | 2,283.55 |

The script uses raw consecutive annotation intervals and breaks at run boundaries and sampling discontinuities. These counts should be checked against the original benchmark's event definition before publication. No subject-level clinical records are published here.

## External evaluation caveats

The two datasets are not interchangeable: FoG-STAR uses accelerometer and gyroscope channels across ankles, back and wrist; Daphnet has accelerometers on ankle, thigh and trunk, with a different acquisition protocol. A defensible external evaluation requires explicit channel harmonization, unit conversions, resampling, source-only preprocessing, and a protocol that forbids target test labels from entering model calibration. Comparisons must be labeled cross-dataset shift tests and should not be described as independent clinical validation.

## Reproduction

```
python daphnet_audit.py --dataset-dir data/daphnet/dataset_fog_release/dataset --out results
```

Do not commit raw data to GitHub.
