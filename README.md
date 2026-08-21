# Agentic Parkinson Research

F61 in the Agentic AI Library.

A standalone multi-agent research support system for Parkinson disease literature synthesis, cohort definition, evidence mapping, biomarker review, study planning, and research quality control.

This repository supports research workflows only. It does not diagnose, prescribe, recommend patient treatment, or replace qualified clinical or scientific review.

## Core agents

- [`literature_scout_agent.py`](AGENTS/literature_scout_agent.py)
- [`cohort_design_agent.py`](AGENTS/cohort_design_agent.py)
- [`biomarker_evidence_agent.py`](AGENTS/biomarker_evidence_agent.py)
- [`study_design_agent.py`](AGENTS/study_design_agent.py)
- [`evidence_quality_agent.py`](AGENTS/evidence_quality_agent.py)
- [`human_review_agent.py`](AGENTS/human_review_agent.py)

## Architecture

- [`AGENTS/`](AGENTS/)
- [`TOOLS/`](TOOLS/)
- [`SKILLS/`](SKILLS/)
- [`orchestration/`](orchestration/)
- [`memory/`](memory/)
- [`state/`](state/)
- [`schemas/`](schemas/)
- [`prompts/`](prompts/)
- [`config/`](config/)
- [`safety/`](safety/)
- [`observability/`](observability/)
- [`evals/`](evals/)
- [`benchmarks/`](benchmarks/)
- [`examples/`](examples/)
- [`tests/`](tests/)
- [`docs/`](docs/)

## Run

```bash
python run.py
```

Human review is required before any patient-specific, clinical, or consequential use.
