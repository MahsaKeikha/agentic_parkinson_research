# Agentic Parkinson Research

**F61 | L3 Gold Standard | v1.0**

A standalone governed multi-agent research support system for Parkinson disease literature synthesis, cohort definition, evidence mapping, biomarker review, study planning, and research quality control.

This repository supports research workflows only. It does not diagnose, prescribe, authorize treatment, recommend patient-specific care, or replace qualified clinical or scientific review.

## Core agents

- [`literature_scout_agent.py`](AGENTS/literature_scout_agent.py)
- [`cohort_design_agent.py`](AGENTS/cohort_design_agent.py)
- [`biomarker_evidence_agent.py`](AGENTS/biomarker_evidence_agent.py)
- [`study_design_agent.py`](AGENTS/study_design_agent.py)
- [`evidence_quality_agent.py`](AGENTS/evidence_quality_agent.py)
- [`human_review_agent.py`](AGENTS/human_review_agent.py)

## Gold standard governance

The orchestrator fails closed unless the research question, source traceability, data provenance, cohort definition, endpoints, biomarker evidence links, statistical plan, ethics scope, privacy controls, conflicts and limitations, and qualified human approval are complete.

The workflow blocks patient-specific diagnosis, prescribing, treatment authorization, unsupported causal claims, fabricated or unverified evidence, and unresolved consequential research questions.

The system never receives autonomous clinical or treatment authority.

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

## Verification gates

Gold Standard CI runs on Python 3.10, 3.11, and 3.12 and requires:

```bash
ruff check .
python -m pytest -q
python evals/heldout_suite.py
python examples/example.py
python run.py
```

The held-out suite includes ready-state, provenance, traceability, cohort, biomarker evidence, clinical-boundary, causality, evidence-integrity, and human-approval scenarios.

## Run

```bash
python run.py
```

Human scientific review is mandatory before consequential use.
