# Quality-Aware Supervisor: First Experimental Failure Analysis

**29 October 2026. Exploratory pilot, not a safety validation.**

## Method

Each outer held-out participant fold is split internally into disjoint classifier-fitting and validation participants. A threshold is selected as the highest predicted probability satisfying a target of at least 80% recall **on validation positive windows**. The three-action prototype produces `alert`, `no alert`, or `abstain` using a 0.1 probability margin below the alert threshold and a minimum observed-signal fraction of 0.75. Alerts are merged within 2 seconds. No test labels are used to select thresholds.

The fair internal comparator is the same classifier fitted to the same subset of development participants, operated at threshold 0.5 with identical 2-second merging. It is **not** the earlier full-development-fold benchmark; these results must not be compared as if their training data were the same.

## Pilot outcomes

| Held-out fold | Selected threshold | Decision coverage | Baseline detected / false runs | Supervisor detected / false runs |
|---|---:|---:|---:|---:|
| 1 | 0.000061 | 75.4% | 0 / 0 | 11 / 12 |
| 2 | 0.001820 | 62.6% | 2 / 2 | 5 / 17 |
| 3 | 0.320681 | 94.2% | 3 / 8 | 5 / 9 |
| 4 | 0.000038 | 29.2% | 0 / 0 | 1 / 29 |
| 5 | 0.006173 | 37.4% | 0 / 1 | 1 / 24 |
| **Descriptive totals** | | | **5 / 11** | **23 / 91** |

There are 28 annotated reference episodes. The supervisor pilot detected 23 (82.1%) but generated 91 unmatched alert runs, equivalent to approximately 136.95 per recorded hour. Its comparator detected only 5 (17.9%) and generated 11 unmatched alert runs (about 16.55 per hour). The supervisor therefore **does not demonstrate a usable risk reduction**. It trades a large increase in alert burden for higher episode detection.

## Failure analysis

1. Thresholds near zero are a symptom of poor transfer calibration and class imbalance, not evidence of reliable model uncertainty.
2. A validation *window-level* sensitivity constraint does not control event-level alert burden on other participants.
3. Abstention and event detection must be evaluated jointly. More automated episode detections do not justify unlimited false alerts.
4. The high alert rate, nine-subject sample, and unknown home-monitoring performance rule out clinical claims.

## Required methodological change

The next supervisor should explicitly evaluate operating points using **both validation event sensitivity and false alert runs/hour**, while measuring decision coverage and positive-episode abstention. It should expose infeasibility when no threshold simultaneously meets safety targets; it must not manufacture a successful setting by relaxing requirements after seeing test results. Predefine a utility family, assess Pareto tradeoffs, and reserve an independent dataset for stress testing. Event-level validation will require per-block timestamps, discontinuity handling and a fixed alert-merging convention.

## Reproduce

```
python supervisor.py --sensor-data data/sensor_data.csv --out results
```

Detailed outputs are in `results/supervisor_pilot.json` and excluded from GitHub.
