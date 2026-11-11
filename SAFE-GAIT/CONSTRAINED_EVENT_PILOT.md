# Event-Constrained Supervisor Pilot

**29 October 2026. Exploratory feasibility test, not evidence of clinical safety.**

## Protocol

Five outer participant-held-out folds. Each development portion is split again by participant ID, so model fitting and operating-point selection use disjoint people. Nineteen fixed probability thresholds, 0.05 through 0.95 in steps of 0.05, are evaluated against annotated episodes on **validation participants only** with the same 2-second alert-merging and one-to-one event rule.

A threshold is marked feasible only if validation event sensitivity is at least 70% **and** unmatched alert runs per recorded hour are at most 30. Among feasible settings, select the lowest alert burden, breaking ties by sensitivity and threshold. This target pair is a research stress-test specification, **not** a medically established safety requirement. No test label selects or repairs thresholds. If no validation candidate qualifies, report `infeasible` and issue no selected test operating-point result.

## Outcomes

| Outer fold | Validation annotated events | Feasible selection? | Selected threshold | Held-out test outcome |
|---|---:|---|---:|---|
| 1 | 13 | No | None | Not evaluated as selected policy |
| 2 | 13 | No | None | Not evaluated as selected policy |
| 3 | 3 | No | None | Not evaluated as selected policy |
| 4 | 25 | No | None | Not evaluated as selected policy |
| 5 | 5 | Yes | 0.55 | 0 episodes detected; 0 false alert runs |

Only **one of five** development folds identified a feasible threshold. Its test result missed the held-out episode, illustrating that empirical validation feasibility does not guarantee transfer across patients.

## Interpretation

This experiment establishes a failure of a simple event-level constrained-threshold approach on the current nine-participant dataset. It is scientifically preferable to report infeasibility rather than to relax constraints after inspecting held-out test data. It does not establish any formal selective-risk guarantee; such claims would require much larger independent samples, carefully stated exchangeability assumptions, and prospective investigation of distribution shift.

## Reproduction

```
python constrained.py --sensor-data data/sensor_data.csv --out results
```

The script saves `results/constrained_event_pilot.json`, containing all fold diagnostics but no raw sensor data.

## Implications for the proposed paper

The core research question should now be framed as **feasibility-aware and shift-aware supervisory risk control**. Before proposing a new method, compare robust thresholds, subgroup-aware uncertainty, class-sensitive abstention and hierarchical control against the no-policy and simple policy baselines. Report feasible coverage, unsafe/infeasible cases, and clinical error tradeoffs instead of optimization success alone.
