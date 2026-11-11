# Cross-Dataset Event-Level Abstention Audit

**29 October 2026. Exploratory retrospective replay, not clinical validation.**

## Clinical evaluation question

When a magnitude-only freezing-of-gait classifier trained on Daphnet is
replayed on FoG-STAR, does source-calibrated distribution-shift abstention
improve true freezing-episode detection or reduce only false alerts?

## Reproducible protocol

- Daphnet trunk acceleration is converted from mg to g; the source classifier
  and robust-distance gate use the three orientation-invariant features.
- The raw FoG-STAR recording is segmented in **original file order** at
  participant/session/task changes and nonmonotonic or excessive timestamp
  gaps. No window is allowed across those boundaries.
- Two-second windows overlap with a one-second stride. Each prediction is
  assigned the timestamp immediately **after the last sample in its window**.
- Source-only gate retention settings: 80%, 90%, and 95%. Classifier
  threshold is fixed at 0.5. Abstention means no alert.
- Raw sample-level FoG annotations, not window majority-vote labels, define
  reference episodes. A one-to-one temporal overlap rule matches alerts to
  episodes. No tolerance margin and no alert merging.
- A false alert is an unmatched predicted alert run. Reported denominator is
  2,392.15 seconds of valid annotated sensor time. Individual windows are
  dependent; counts are descriptive.
- This investigation follows earlier inspection of the FoG-STAR labels and
  target performance; it is a **post-hoc exploratory analysis**.

## Findings

| Policy | Detected episodes | Missed episodes | Unmatched alert runs | False alerts/hour | Target windows abstained |
|---|---:|---:|---:|---:|---:|
| No gate | 0/28 | 28 | 6 | 9.03 | 0 / 2,263 |
| 80% source retention | 0/28 | 28 | 5 | 7.52 | 111 / 2,263 |
| 90% source retention | 0/28 | 28 | 5 | 7.52 | 19 / 2,263 |
| 95% source retention | 0/28 | 28 | 6 | 9.03 | 1 / 2,263 |

The gate reduced one false alert run at the 80% and 90% source-retention
settings. However, all 28 freezing episodes remained undetected. Lower
false-alert rates with zero event sensitivity do **not** demonstrate a useful
or safe clinical detector. Missed events are counted against the detector even
where abstention suppresses its output.

## Limitations

The FoG-STAR sensor file has only nine distinguishable participant IDs,
despite 22 clinical-metadata rows. The target protocol may differ substantially
from Daphnet in sensor position, sampling and activity context, cohort and
labeling. Windows overlapping an onset may issue a decision only after
completion, which can prevent detection of short episodes without a latency
tolerance. The event-matching convention is an explicit operational choice,
not a clinically standardized endpoint. No independent target cohort remains
for confirmatory assessment after this exploratory sequence.

## Reproduce

```bash
python cross_dataset_events.py \
  --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

Generates `results/cross_dataset_events.json`, excluded from version control.
