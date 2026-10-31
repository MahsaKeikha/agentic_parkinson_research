# First Participant-Held-Out Event-Level Baseline

**Experimental run: 29 October 2026. Exploratory, not clinical validation.**

## Protocol

- FoG-STAR v2 source sensor CSV verified by checksum, nine distinct participant IDs.
- Source-order segments are broken at changes in participant/session/task, timestamp resets and sampling discontinuities.
- Two-second sensor windows, evaluated with a one-second stride; predictions are assigned to the **end** of each observed window to avoid look-ahead.
- A histogram gradient-boosting classifier with hand-engineered channel features and training-only imputation.
- Five subject-grouped outer folds, threshold 0.5, no tuning, calibration, event merging or refractory period.
- Reference events are contiguous annotated FoG-positive runs. Predicted alert runs are matched one-to-one with strict temporal overlap, no onset tolerance.
- False-alert rate uses the sum of valid annotated recording time, not overlapping window durations.

## Results

| Fold | Test subject IDs | Reference episodes | Detected | Missed | False alert runs | Episode sensitivity | False alerts/hour |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 13 | 11 | 2 | 41 | 84.6% | 258.83 |
| 2 | 1, 10 | 5 | 1 | 4 | 0 | 20.0% | 0.00 |
| 3 | 3, 8 | 7 | 1 | 6 | 2 | 14.3% | 15.59 |
| 4 | 4, 6 | 2 | 1 | 1 | 12 | 50.0% | 92.33 |
| 5 | 5, 7 | 1 | 0 | 1 | 1 | 0.0% | 7.67 |
| **Combined descriptive totals** | **9** | **28** | **14** | **14** | **56** | **50.0%** | **84.28** |

Combined false alerts/hour is 56 / (2,392.15 / 3,600), or approximately 84.28. The combined episode sensitivity is a descriptive ratio, not an independent patient-level estimate or confidence interval. The reported false alerts are **unmerged alert runs**. Fragmented alerts from one episode can create multiple false-alert runs, making this a deliberately stringent and operationally incomplete first benchmark.

## Interpretation

This classifier is unsuitable for automatic clinical alerts in its present form. Fixed-threshold episode detection is highly heterogeneous between held-out subjects, and the false-alert burden is too high for a credible home-monitoring claim. Any improvement must be measured against this baseline using the same held-out splits, explicit alert-merging policy, positive-event retention, latency, and paired subject-level comparison.

## Limitations and next steps

1. The available sensor file has only nine participants; most folds contain one or two people.
2. Four participants have no annotated positive events, and positive episode counts are strongly imbalanced.
3. Prediction timestamps correspond to window ends; this prevents retrospective advance warning claims.
4. Event annotation conventions and matching tolerance require comparison with the dataset authors' reference benchmark.
5. Alert-refractory grouping, threshold selection and sensor-quality abstention must be prespecified using development data only.
6. External evaluation on Daphnet requires channel/sampling harmonization; it is not yet performed.

## Reproduce

```
python event_baseline.py --sensor-data data/sensor_data.csv --out results
```

The output is `results/event_baseline_cv.json` and is excluded from source control.
