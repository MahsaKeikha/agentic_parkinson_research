# SAFE-GAIT

**Risk-aware, explainable freezing-of-gait detection for Parkinson's research**  
**Research status: protocol and baseline implementation; no empirical result claimed.**

This subproject supports the proposed ACM TRUST 2027 REED-AI manuscript. It is distinct from the parent repository's agentic literature-research architecture.

## Research question

Can signal-quality-aware uncertainty calibration and an abstaining decision policy reduce errors among automated FoG monitoring decisions without sacrificing useful detection coverage?

## What is implemented

- `baseline.py`: FoG-STAR CSV audit, deterministic window features and participant-grouped baseline validation.
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
- [ ] Dataset download and schema audit
- [ ] Subject-level train/validation/test protocol freeze
- [ ] Calibrated score and uncertainty estimation
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
