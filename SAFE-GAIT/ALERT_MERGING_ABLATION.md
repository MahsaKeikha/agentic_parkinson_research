# Alert-Burst Merging Ablation

**Exploratory engineering comparison, 29 October 2026. Not a clinically validated improvement.**

## Design

Predictions and participant-held-out models are identical in both arms. The only change is a fixed two-second gap-merging rule: two adjacent predicted alert episodes in the *same uninterrupted recording block* are combined if the interval separating them is at most two seconds. Event matching is one-to-one with strict temporal overlap, and alert onset remains the first available window-end prediction.

The 2-second threshold was selected **after inspecting the initial unmerged baseline**, so this is exploratory ablation analysis, not a preregistered confirmatory comparison. Threshold sensitivity and independent confirmation are needed.

## Results

| Quantity | No merging | Merge gaps <= 2 seconds |
|---|---:|---:|
| Reference FoG episodes | 28 | 28 |
| Detected reference episodes | 14 | 14 |
| Missed reference episodes | 14 | 14 |
| Unmatched alert runs | 56 | 36 |
| Total alert runs | 70 | 50 |
| FoG event sensitivity | 50.0% | 50.0% |
| Unmatched alert runs/hour | 84.28 | 54.18 |

Exploratory reduction of unmatched alert runs: 20/56 = 35.7%, with no change in detected reference episodes in this dataset. This is **not** a statistically established or generalizable safety gain; merged alerts represent a different counting convention and might suppress distinct alerts in other settings. The remaining false-alert burden is still substantial.

## Methodological safeguards and outstanding work

1. Evaluate an explicit range of merging gaps using inner development subjects, then freeze a rule before external testing.
2. Report subject-level tradeoffs, error bars and event delays, not only pooled counts.
3. Report intervention/alert burden as well as raw event sensitivity; different alert definitions change rates by construction.
4. Test whether a merged alert spans more than one true FoG event; one-to-one matching deliberately prevents double credit.
5. Compare a learned quality-aware supervisor against this simple engineering baseline, with identical event matching and participant splits.

## Reproduction

```
python event_baseline.py --sensor-data data/sensor_data.csv --out results
```

Both arms are in `results/event_baseline_cv.json` as `unmerged` and `merged_2s`.
