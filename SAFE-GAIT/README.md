# SAFE-GAIT

**Risk-aware, explainable freezing-of-gait detection for Parkinson's research**  
**Research status: protocol and baseline implementation; no empirical result claimed.**

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
- [ ] Subject-level train/validation/test protocol freeze
- [ ] Calibrated score and uncertainty estimation
- [x] First calibrated selective benchmark (results pending validation)
- [x] Pilot selective benchmark reported transparently in `SELECTIVE_RESULTS.md`; safety gains **not** demonstrated
- [ ] Risk-aware supervisor and ablation study
- [ ] FoG event metrics and latency
- [ ] Sensor corruption and cross-domain evaluation
- [ ] Reproducibility report, full manuscript and verified bibliography

## Scientific integrity

The source data has not yet been run through this implementation. Results, improvement claims, statistical significance and clinical utility are unknown. Validate event annotation conventions, sensor units, sample timing and fold distributions before use. Controlled movement datasets do not establish reliable autonomous home care.

## Citation and provenance

- Borzi et al., FoG-STAR dataset, https://zenodo.org/records/17037669
- Daphnet FoG, UCI dataset 245, https://archive.ics.uci.edu/dataset/245/daphnet+freezing+of+gait
- ACM TRUST 2027 author instructions, https://eigtrust.acm.org/trust2027/authors-guidelines/

Licensed code is a research prototype. Dataset licensing remains with original data publishers.
