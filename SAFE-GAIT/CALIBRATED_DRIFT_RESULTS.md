# Participant-Held-Out Source-Calibrated Score Drift Warning

**29 October 2026. Post-hoc pilot, not validated clinical safety monitoring.**

## Question

Can a score-distribution warning threshold derived entirely from Daphnet
participant-held-out variation flag unfamiliar FoG-STAR subject recordings?

## Design

Using three orientation-invariant magnitude features and the fixed classifier,
we ran five participant-grouped Daphnet folds. Each fold compared model scores
on its training participants with scores on held-out participants by the
supremum distance between empirical CDFs. The empirical 95th percentile of
those five source fold distances provided the warning cutoff. Next, a model
fitted to all Daphnet subjects scored FoG-STAR participants; each target
subject's score-distribution distance to the in-sample source distribution
was compared with the source-only cutoff. **Target labels were not involved
in threshold selection.**

## Measurements

Source calibration fold distances were approximately 0.198, 0.144, 0.074,
0.079, and 0.066. The five-fold empirical 95th percentile was **0.1871**.

| FoG-STAR participant | Score ECDF distance | Warning |
|---|---:|---|
| 1 | 0.105 | No |
| 2 | 0.393 | Yes |
| 3 | 0.254 | Yes |
| 4 | 0.201 | Yes |
| 5 | 0.180 | No |
| 6 | 0.166 | No |
| 7 | 0.327 | Yes |
| 8 | 0.238 | Yes |
| 10 | 0.292 | Yes |

**Six of nine** target participants triggered a warning. This is a descriptive
observation, not measured warning sensitivity or specificity: target site is
not a ground-truth label for an individual clinical model failure, and target
participants have already been evaluated in preceding experiments.

## Key methodological limitations

1. Only five source-fold distances set a nominal 95th-percentile cutoff.
   This cannot support a valid patient-level 5% false-warning claim.
2. Source folds compare pooled training participants with pooled held-out
   participants, while target tests compare pooled source to a **single**
   participant. Different sample sizes and mixture distributions can
   change ECDF distance. The calibration distributions are not exchangeable.
3. The source reference score distribution is in-sample and target scores
   are out-of-sample. Windows within people and runs are dependent.
4. The design is post-hoc after examination of the target dataset. A new
   independent test cohort is necessary before a generalization claim.
5. The warning does not prevent the previously documented missed FoG events;
   it only signals a potential reason to withhold reliance on a model.

## Next research design

Create a matched participant-level calibration protocol with one target
subject compared to a reference distribution built independently of that
subject. Use leave-one-subject-out reference scores and a new cohort for
prospective threshold evaluation. Report source false-warning frequency,
target warning coverage, event sensitivity, and missed-event counts together.

## Reproduce

```bash
python calibrated_drift.py \
  --daphnet-dir data/daphnet/dataset_fog_release/dataset \
  --fogstar-sensor-data data/sensor_data.csv --out results
```

Writes `results/calibrated_drift.json`, excluded from version control.
