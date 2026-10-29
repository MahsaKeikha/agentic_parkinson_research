# SAFE-GAIT

**Risk-aware, explainable freezing-of-gait detection for Parkinson's research**  
**Research status: exploratory public-data experiments completed; no clinical validity claimed.**

**Data audit alert:** The checksum-verified FoG-STAR v2 sensor CSV currently contains 9 participant IDs, whereas the accompanying clinical file lists 22. Earlier 22-participant baseline figures have been marked superseded. Do not cite results until the release discrepancy has been resolved.

This subproject supports the proposed ACM TRUST 2027 REED-AI manuscript. It is distinct from the parent repository's agentic literature-research architecture.

## Research question

Can signal-quality-aware uncertainty calibration and an abstaining decision policy reduce errors among automated FoG monitoring decisions without sacrificing useful detection coverage?

## What is implemented

- `baseline.py`: FoG-STAR CSV audit, deterministic window features and participant-grouped baseline validation.
- `selective.py`: nested participant separation for model fitting, Platt-style calibration and selective prediction.
- `events.py`: explicit one-to-one event matching, latency and false-alert metrics.
- `event_audit.py`: raw-annotation episode counts with source-order and timestamp-gap controls.
- `daphnet_audit.py`: independent Daphnet recording and episode audit with explicit non-experiment label exclusion.
- `event_baseline.py`: model-generated alerts matched against raw annotated episodes in participant-held-out folds.
- `supervisor.py`: first three-action, validation-thresholded, quality-aware supervisory ablation.
- `constrained.py`: event-level threshold search with explicit infeasibility when validation safety targets cannot be met.
- `cross_dataset.py`: Daphnet-to-FoG-STAR accelerometer feature alignment and untouched-target shift test.
- `cross_dataset_invariant.py`: post-hoc rotation-invariant transfer comparison and label-free shift audit.
- `shift_supervisor.py`: exploratory source-only magnitude-distance abstention with explicit missed-positive accounting.
- `shift_supervisor.py` also reports a participant-cluster AUROC bootstrap, avoiding a naive independent-window uncertainty calculation.
- `cross_dataset_events.py`: source-trained end-of-window event-level replay on raw FoG-STAR episodes, with and without source-only abstention.
- `score_drift.py`: label-free descriptive comparison of model score distributions across source and target (not a calibrated alarm).
- `calibrated_drift.py`: preliminary participant-held-out source cutoff for a subject-level score-distribution warning; calibration is not patient-level valid.
- `test_baseline.py`: synthetic tests guarding group separation, window extraction and basic metric integrity.
- `dashboard.py`: Streamlit research explorer with **synthetic demonstration data only**. It does not imply clinical validation or display real patient records.
- `PROTOCOL.md`: endpoints, leakage safeguards, dataset provenance, evaluation design and paper outline.

## Installation

Use Python 3.11 or later and a virtual environment:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s . -p 'test_*.py'
```

## Real-data baseline

Download FoG-STAR from the authors' dataset release at https://zenodo.org/records/17037669 and verify the current version, license, and files. Do not commit the dataset to GitHub.

```bash
python baseline.py --sensor-data /path/to/sensor_data.csv --out results
python selective.py --sensor-data /path/to/sensor_data.csv --out results
python event_audit.py --sensor-data /path/to/sensor_data.csv --out results
python event_baseline.py --sensor-data /path/to/sensor_data.csv --out results
```

The result is `results/baseline_grouped_cv.json`. This is a **window-level, uncalibrated baseline**, not the SAFE-GAIT safety supervisor or an event-level clinical result.

## Interactive research demonstration

```bash
streamlit run dashboard.py
```

The dashboard explores synthetic prediction probabilities and abstention thresholds. It intentionally does not load personal health records, perform diagnosis, issue medical advice or make real-world alerts.

## Roadmap

- [x] Written analysis protocol
- [x] Participant-grouped baseline
- [x] Synthetic research dashboard
- [x] Dataset download, MD5 verification and preliminary schema inspection
- [x] Initial grouped baseline, reported as exploratory in `INITIAL_RESULTS.md`
- [ ] Detailed annotation and event audit
- [x] Initial event annotation audit: 28 episodes across 5 positive participants; see `EVENT_AUDIT.md`
- [x] Independent Daphnet event audit: 237 events across 8 positive participants; see `EXTERNAL_DATA_AUDIT.md`
- [x] First raw-event baseline: 14/28 detected episodes, 56 unmatched alert runs; see `EVENT_BASELINE_RESULTS.md`
- [x] Exploratory burst-merging ablation: 36 unmatched runs at the same 14/28 detected episodes; see `ALERT_MERGING_ABLATION.md`
- [x] First supervisor pilot: higher event sensitivity but unacceptable false-alert burden; see `SUPERVISOR_PILOT.md`
- [x] Event-constrained feasibility pilot: only one of five folds feasible; see `CONSTRAINED_EVENT_PILOT.md`
- [x] Daphnet-to-FoG-STAR shift test: AUROC 0.349 and 0% target sensitivity at fixed threshold; see `CROSS_DATASET_RESULTS.md`
- [x] Orientation-invariant transfer follow-up: source CV improved but target failed; see `ORIENTATION_INVARIANT_RESULTS.md`
- [x] Source-only distance-gate experiment: target shift largely undetected; see `SHIFT_SUPERVISOR_RESULTS.md`
- [x] Cross-dataset event replay: 0/28 episodes detected, with 5 to 6 false alert runs; see `CROSS_DATASET_EVENT_RESULTS.md`
- [x] Label-free score-drift diagnostic: ECDF distance 0.144, without an alarm validity claim; see `SCORE_DRIFT_RESULTS.md`
- [x] Source-fold score-warning pilot: 6/9 FoG-STAR participants flagged; caveats in `CALIBRATED_DRIFT_RESULTS.md`
- [ ] Subject-level train/validation/test protocol freeze
- [ ] Calibrated score and uncertainty estimation
- [x] First calibrated selective benchmark (results pending validation)
- [x] Pilot selective benchmark reported transparently in `SELECTIVE_RESULTS.md`; safety gains **not** demonstrated
- [ ] Risk-aware supervisor and ablation study
- [ ] FoG event metrics and latency
- [ ] Sensor corruption and cross-domain evaluation
- [ ] Reproducibility report, full manuscript and verified bibliography

## Scientific integrity

The implementation has been run on public FoG-STAR and Daphnet recordings, and exploratory outcomes are documented with explicit failures. No clinical utility, prospective validation, or statistically established safety improvement is claimed. The verified FoG-STAR sensor file contains only nine participant IDs despite 22 clinical-metadata rows. Validate dataset provenance, event conventions, sensor units, timing and fold distributions before further use. Controlled movement datasets do not establish reliable autonomous home care.

## Citation and provenance

- Borzi et al., FoG-STAR dataset, https://zenodo.org/records/17037669
- Daphnet FoG, UCI dataset 245, https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait
- ACM TRUST 2027 author instructions, https://eigtrust.acm.org/trust2027/authors-guidelines/

Licensed code is a research prototype. Dataset licensing remains with original data publishers.
# Recent exploratory transfer analysis

The [orientation-invariant transfer follow-up](ORIENTATION_INVARIANT_RESULTS.md)
compares magnitude-only and axis-dependent features with source-only training.
Improved source cross-validation did **not** fix poor FoG-STAR transfer. Its
post-hoc status is documented explicitly; the result is not clinical validation.

