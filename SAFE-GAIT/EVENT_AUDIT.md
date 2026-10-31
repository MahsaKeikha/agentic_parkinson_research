# FoG-STAR Event Annotation Audit

**Source: checksum-verified FoG-STAR sensor CSV, 29 October 2026.**

This is an annotation-counting audit, **not a classifier evaluation**. The episode convention is a contiguous positive-label run, split whenever the source task/session/subject changes, timestamps reset, or the observed gap exceeds 1.5 sampling periods. The sample period is 1/60 seconds. Runs shorter than one sample are not possible in this representation.

## Counted episodes and exposure

| Quantity | Verified audit value |
|---|---:|
| Participants represented in sensor CSV | 9 |
| Participants with at least one FoG-positive sample | 5 |
| Participants with no observed FoG-positive samples | 4 |
| Annotated FoG episodes | 28 |
| Annotated recording time | 2,392.15 seconds (39.87 minutes) |

| Subject ID | Annotated episodes | Positive samples | Annotated seconds |
|---|---:|---:|---:|
| 1 | 5 | 10,583 | 358.15 |
| 2 | 13 | 18,129 | 570.25 |
| 3 | 7 | 5,226 | 337.83 |
| 4 | 2 | 642 | 322.83 |
| 5 | 1 | 354 | 157.42 |
| 6 | 0 | 0 | 145.05 |
| 7 | 0 | 0 | 312.23 |
| 8 | 0 | 0 | 124.03 |
| 10 | 0 | 0 | 64.35 |

## Implications

1. Event-level sensitivity for many held-out subjects is undefined, not zero: they experienced no positive annotated episodes.
2. A single missed event can produce a very large change in participant-level sensitivity because many participants have only one or two events.
3. False-alert burden must be normalized by actual valid observation time, not by the number of overlapping windows.
4. Only a prospective or external cohort can support broader claims about home deployment and different movement contexts.
5. The event convention, permissible onset tolerance and minimum episode duration must be fixed before model evaluation.

## Reproduction

```
python event_audit.py --sensor-data data/sensor_data.csv --out results
```

The script writes `results/event_annotation_audit.json`, deliberately excluded from version control alongside raw datasets. The summary above contains only aggregate and subject-indexed counts with no clinical metadata.
