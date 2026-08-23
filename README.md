# F61 Agentic Parkinson Research

**Maturity:** L3 Gold Standard  
**Version:** 1.0

A governed six-agent research architecture for Parkinson disease literature synthesis, cohort definition, biomarker evidence mapping, study design, evidence-quality review, and qualified human scientific approval.

F61 is designed as a reusable research reference for teams exploring multi-agent systems in Parkinson disease and related movement-disorder research. It separates literature retrieval, cohort reasoning, biomarker appraisal, study planning, evidence grading, provenance, and scientific review so that unsupported conclusions or missing research evidence are surfaced rather than hidden.

This repository supports research workflows only. It does not diagnose Parkinson disease, determine an individual's disease stage, prescribe medication, recommend patient-specific treatment, alter deep-brain-stimulation settings, authorize clinical care, or replace neurologists, movement-disorder specialists, statisticians, clinical investigators, ethics reviewers, or other qualified professionals.

## Why Parkinson research benefits from a multi-agent architecture

Parkinson disease research spans heterogeneous evidence sources and measurement domains. A single research question can involve clinical phenotypes, motor symptoms, non-motor symptoms, imaging, wearable sensors, digital biomarkers, electrophysiology, fluid biomarkers, genetics, cognition, medication state, disease duration, longitudinal change, and treatment exposure.

A useful governed workflow is:

```text
research question
       |
       v
literature evidence
       |
       v
cohort definition
       |
       v
biomarker evidence
       |
       v
study design
       |
       v
evidence-quality review
       |
       v
qualified human scientific review
```

Each stage creates evidence for the next stage. A plausible biomarker does not compensate for a poorly defined cohort, and a well-defined cohort does not justify an unsupported causal claim.

## Six-agent architecture

| Agent | Responsibility | Core research question |
|---|---|---|
| Literature Scout Agent | Finds and organizes relevant scientific evidence | What literature directly supports the research question, and what is the provenance of each source? |
| Cohort Design Agent | Defines populations, inclusion/exclusion logic, stratification, and confounders | Who exactly is being studied, and are the groups scientifically comparable? |
| Biomarker Evidence Agent | Maps candidate biomarkers to evidence, modality, endpoint, and limitations | What evidence supports each biomarker and what does it actually measure? |
| Study Design Agent | Structures hypotheses, endpoints, variables, analysis plans, and study workflow | Can the research question be tested with a coherent and reproducible study design? |
| Evidence Quality Agent | Reviews bias, evidence strength, causal language, gaps, and contradictions | How strong is the evidence and what claims are justified? |
| Human Review Agent | Represents qualified scientific authority | Has a qualified researcher reviewed the consequential scientific conclusions and unresolved issues? |

The system is deliberately modular. Agents support one another, but they do not erase each other's blockers.

## Repository structure

```text
AGENTS/
├── literature_scout_agent.py
├── cohort_design_agent.py
├── biomarker_evidence_agent.py
├── study_design_agent.py
├── evidence_quality_agent.py
└── human_review_agent.py

SKILLS/
├── literature_synthesis.py
├── cohort_reasoning.py
├── biomarker_reasoning.py
├── study_planning.py
└── evidence_appraisal.py

TOOLS/
├── literature_index_tool.py
├── provenance_tool.py
├── cohort_criteria_tool.py
├── biomarker_table_tool.py
└── evidence_grade_tool.py

benchmarks/
└── reference_case.json

evals/
├── evaluate.py
└── heldout_suite.py

config/
docs/
examples/
memory/
observability/
orchestration/
prompts/
safety/
schemas/
state/
tests/
.github/workflows/tests.yml
run.py
README.md
```

The architecture separates probabilistic reasoning from deterministic research artifacts such as provenance records, cohort criteria, biomarker tables, and evidence grades.

## Research question definition

Every workflow begins with a clearly scoped research question.

A strong research question should make explicit:

- population
- phenotype or disease stage of interest
- exposure or intervention if applicable
- comparator if applicable
- endpoint or outcome
- time horizon
- study context
- intended inference

Examples of research-level questions include:

- whether a wearable gait feature is associated with longitudinal motor decline
- whether a candidate digital biomarker tracks symptom fluctuations
- whether sleep-related measures correlate with non-motor burden
- whether a multimodal signal improves cohort stratification
- whether a biomarker is suitable for exploratory, prognostic, monitoring, or response-to-intervention research

The system should distinguish association, prediction, prognosis, treatment response, and causality rather than treating them as interchangeable claims.

## Literature evidence and provenance

The Literature Scout Agent organizes evidence rather than simply producing summaries.

`TOOLS/literature_index_tool.py` and `TOOLS/provenance_tool.py` support source tracking.

Useful literature records can include:

```text
source_id
title
authors
year
study_type
population
sample_size
endpoint
key_result
limitations
source_location
retrieval_date
verification_state
```

Evidence should remain traceable to the original source. The workflow should never fabricate citations, authors, sample sizes, effect sizes, study outcomes, or publication details.

### Source hierarchy

The appropriate evidence hierarchy depends on the question, but useful categories can include:

- systematic reviews and meta-analyses
- randomized controlled trials
- prospective cohorts
- longitudinal observational studies
- cross-sectional studies
- diagnostic or biomarker-validation studies
- case-control studies
- feasibility studies
- pilot studies
- technical validation studies
- expert consensus or guidelines

Study design should be considered when deciding what conclusions are justified.

## Cohort design

The Cohort Design Agent turns a broad Parkinson population into explicit research groups.

`TOOLS/cohort_criteria_tool.py` provides deterministic representation of cohort logic.

A cohort definition can include:

```text
cohort_id
inclusion_criteria
exclusion_criteria
diagnostic_definition
disease_duration
medication_state
age_range
sex_distribution
motor_stage
cognitive_status
comorbidities
assistive_device_use
sensor_availability
follow_up_window
```

### Parkinson-specific cohort considerations

Depending on the question, relevant factors may include:

- idiopathic Parkinson disease versus atypical parkinsonism
- diagnostic criteria used
- time since diagnosis
- age at onset
- levodopa exposure
- ON versus OFF medication state
- dyskinesia
- freezing of gait
- falls
- tremor-dominant versus postural-instability/gait-difficulty phenotypes
- cognitive impairment
- sleep disturbance
- autonomic symptoms
- depression or anxiety
- hallucinations or psychosis
- deep-brain stimulation status
- rehabilitation exposure

These variables can materially affect observed outcomes and should not be ignored when relevant.

## Clinical scales and outcomes

F61 can organize research endpoints but does not perform clinical assessment autonomously.

Depending on the study, research datasets may contain measures such as:

- MDS-UPDRS domains
- Hoehn and Yahr stage
- timed mobility measures
- gait speed
- stride variability
- balance measures
- fall frequency
- freezing episodes
- sleep measures
- cognitive assessments
- quality-of-life measures
- caregiver-reported outcomes
- patient-reported outcomes

The system should preserve the instrument name, version, measurement context, rater, timing, and medication state when those factors affect interpretation.

## Biomarker evidence

The Biomarker Evidence Agent evaluates candidate markers in context rather than treating every measurable signal as a validated biomarker.

`TOOLS/biomarker_table_tool.py` provides the structured evidence table.

A biomarker record can include:

```text
biomarker_id
modality
biological_or_behavioral_target
measurement_method
intended_research_role
supporting_sources
population
validation_state
repeatability
sensitivity_to_context
confounders
limitations
```

### Candidate biomarker domains

Research may involve:

- gait and mobility signals
- tremor features
- bradykinesia-related movement features
- postural stability
- activity patterns
- sleep metrics
- heart-rate variability
- electrodermal signals
- EEG features
- speech and voice features
- imaging markers
- fluid biomarkers
- genetic markers
- cognitive signals
- digital interaction patterns

A measurable feature should not be described as clinically validated unless the evidence supports that claim.

## Wearables and digital biomarkers

Wearable and home-monitoring studies can capture behavior outside the clinic, but they introduce their own validity concerns.

A robust review should consider:

- sensor placement
- sampling rate
- device version
- firmware version
- missing data
- adherence
- battery interruptions
- calibration
- synchronization
- ground truth
- algorithm version
- activity context
- assistive-device use
- environmental effects
- medication timing

A digital biomarker can appear statistically strong while actually reflecting device behavior, adherence, age, or context rather than disease biology.

## Longitudinal research

Longitudinal Parkinson research requires careful handling of repeated measures and changing clinical context.

Important factors include:

- baseline definition
- visit windows
- follow-up duration
- attrition
- medication changes
- device changes
- disease progression
- rehabilitation or exercise exposure
- intercurrent illness
- missingness mechanism

A model should not treat repeated observations from one participant as independent observations unless the analysis design explicitly supports that assumption.

## Study design

The Study Design Agent converts the question, cohort, and evidence base into a structured plan.

A study-design record can include:

```text
hypothesis
primary_endpoint
secondary_endpoints
exploratory_endpoints
exposure_or_predictor
covariates
confounders
sample_size_rationale
statistical_plan
missing_data_plan
validation_strategy
sensitivity_analyses
ethics_scope
privacy_scope
```

The system should state whether a study is exploratory, confirmatory, observational, interventional, retrospective, prospective, cross-sectional, or longitudinal.

## Statistical planning boundary

F61 can organize a statistical analysis plan, but consequential analyses should be reviewed by a qualified statistician or methodologist.

Relevant considerations include:

- prespecified primary endpoint
- multiplicity
- effect-size assumptions
- confidence intervals
- missing data
- repeated measures
- confounding
- model assumptions
- overfitting
- train/validation/test separation
- external validation
- subgroup analysis
- sensitivity analysis

The workflow should distinguish statistical significance from clinical significance.

## AI and machine-learning research

Parkinson research increasingly uses machine learning for classification, prediction, phenotyping, or digital biomarker development.

F61 should require explicit documentation of:

- target definition
- feature provenance
- participant-level train/test separation
- preprocessing
- leakage controls
- model version
- hyperparameter strategy
- evaluation metrics
- calibration
- class imbalance
- external validation
- subgroup performance
- uncertainty

A model trained on multiple samples from the same participants can appear to perform well if participant identity leaks across splits. Held-out evaluation should therefore respect the true unit of generalization.

## Evidence-quality review

The Evidence Quality Agent challenges conclusions before they reach human review.

`TOOLS/evidence_grade_tool.py` supports explicit grading.

Relevant questions include:

- Is the evidence direct or indirect?
- Is the population representative of the intended inference?
- Is the study adequately powered?
- Is the endpoint validated?
- Are confounders controlled?
- Is there selection bias?
- Is there measurement bias?
- Is attrition important?
- Are multiple comparisons addressed?
- Is the result replicated?
- Are contradictory studies acknowledged?
- Are causal claims justified?

The system should preserve uncertainty rather than converting weak evidence into strong language.

## Causal language

Association does not automatically establish causation.

The workflow should avoid statements such as:

```text
X causes Parkinson progression
```

when the evidence only supports:

```text
X was associated with progression in the studied cohort
```

Causal claims require an appropriate design, assumptions, analysis, and qualified scientific review.

## Ethics and privacy

Parkinson research may involve health records, wearable data, video, audio, movement traces, cognitive data, genetics, or longitudinal home-monitoring information.

Production research workflows should define:

- IRB or ethics scope where applicable
- consent
- permitted data use
- de-identification or pseudonymization
- access controls
- retention
- data-sharing limitations
- re-identification risk
- external collaboration rules
- withdrawal handling where applicable

Research authorization must be established by the responsible institution or study team, not inferred by the agents.

## Shared memory and evidence state

`memory/research_memory.py` supports structured research context across agents.

Useful state includes:

- research-question version
- literature sources
- provenance records
- cohort definition
- candidate biomarkers
- endpoint definitions
- study design
- statistical assumptions
- evidence grades
- ethics scope
- privacy constraints
- unresolved conflicts
- unresolved questions
- human review state

Research state should be versioned so a conclusion can be reconstructed after the evidence base changes.

## Observability and auditability

`observability/trace.py` records workflow execution.

Useful trace fields include:

```text
run_id
research_question_id
agent
input_version
tool_calls
sources_used
findings
uncertainties
conflicts
gate_result
review_state
```

The goal is to make research reasoning inspectable and reproducible rather than allowing conclusions to emerge from an opaque chain.

## Fail-closed research governance

The orchestrator is designed to block a consequential research output when required evidence is incomplete.

Potential blockers include:

- research question undefined
- literature source unverified
- source provenance missing
- cohort definition incomplete
- diagnostic definition unclear
- medication state relevant but unspecified
- endpoint undefined
- biomarker evidence missing
- biomarker validation overstated
- statistical plan incomplete
- leakage risk unresolved
- ethics scope unresolved
- privacy controls incomplete
- unsupported causal claim
- fabricated or unverifiable evidence
- unresolved contradiction
- unresolved consequential question
- qualified human review missing

Passing earlier agents does not override a later blocker.

## Human authority boundary

F61 must not autonomously:

- diagnose Parkinson disease
- distinguish Parkinson disease from atypical parkinsonism for an individual
- assign clinical stage to a patient
- prescribe or adjust levodopa or other medication
- recommend deep-brain-stimulation settings
- recommend individualized rehabilitation
- determine patient eligibility for treatment
- replace informed consent
- approve a human-subject research protocol
- authorize access to protected research data
- claim a biomarker is clinically validated without evidence
- publish consequential conclusions without qualified review

Qualified scientific and clinical professionals retain authority.

## End-to-end reference workflow

A typical F61 research run follows this sequence:

1. Define the research question and intended inference.
2. Establish evidence-search scope and source provenance.
3. Retrieve and organize relevant literature.
4. Define the cohort and key stratification variables.
5. Identify confounders and Parkinson-specific context variables.
6. Map candidate biomarkers to supporting evidence.
7. Define primary, secondary, and exploratory endpoints.
8. Create the study design and statistical plan.
9. Review leakage, bias, missingness, and validity risks.
10. Grade evidence strength and identify contradictory findings.
11. Confirm ethics and privacy scope.
12. Consolidate limitations and unresolved questions.
13. Apply fail-closed governance gates.
14. Require qualified human scientific review before consequential use.

## Reproduce the reference implementation

Run static checks and tests:

```bash
ruff check .
python -m pytest -q
```

Run held-out evaluation:

```bash
python evals/heldout_suite.py
```

Run the example:

```bash
python examples/example.py
```

Run the main workflow:

```bash
python run.py
```

CI under `.github/workflows/tests.yml` validates Python 3.10, 3.11, and 3.12.

## Benchmarks and evaluation

The repository includes:

```text
benchmarks/reference_case.json
evals/evaluate.py
evals/heldout_suite.py
```

Evaluation should test research integrity, not only textual quality.

Useful evaluation dimensions include:

- provenance preservation
- source-verification behavior
- cohort-definition completeness
- confounder detection
- endpoint completeness
- biomarker-evidence linkage
- unsupported-validation detection
- causal-language detection
- evidence-grading consistency
- leakage-risk detection
- ethics-scope handling
- privacy-scope handling
- contradiction propagation
- human-review enforcement

Strong held-out cases should intentionally include weak sources, incomplete cohorts, mixed medication states, unsupported biomarker claims, data leakage, contradictory studies, and causal overstatement.

## Failure states

Useful explicit states include:

```text
RESEARCH QUESTION INCOMPLETE
SOURCE UNVERIFIED
PROVENANCE MISSING
COHORT DEFINITION INCOMPLETE
ENDPOINT UNDEFINED
BIOMARKER EVIDENCE INCOMPLETE
BIOMARKER VALIDATION OVERSTATED
STATISTICAL PLAN INCOMPLETE
DATA LEAKAGE RISK
ETHICS REVIEW REQUIRED
PRIVACY REVIEW REQUIRED
CAUSAL CLAIM UNSUPPORTED
EVIDENCE CONFLICT UNRESOLVED
HUMAN SCIENTIFIC REVIEW REQUIRED
```

The system should never fabricate literature, cohort information, biomarker evidence, clinical outcomes, statistics, ethics approval, or human review.

## L3 Gold Standard

F61 is structured as an L3 Gold Standard repository through:

- six specialist agents
- explicit deterministic tools
- structured research memory
- provenance tracking
- fail-closed governance
- clinical-scope restrictions
- held-out evaluation
- observability
- CI across supported Python versions
- mandatory human scientific review

The L3 designation describes repository engineering maturity. It does not establish clinical validity, regulatory approval, institutional review-board approval, scientific consensus, or suitability for patient care.

## Extending F61

Common extensions include:

- PubMed and bibliographic-database adapters
- systematic-review tooling
- citation managers
- clinical-trial registries
- cohort databases
- EDC and research-data platforms
- wearable sensor pipelines
- gait and IMU analysis
- speech and voice research
- EEG research
- imaging research
- genetics and omics datasets
- digital biomarker registries
- statistical-analysis pipelines
- machine-learning experiment tracking
- preregistration workflows
- research dashboards
- reproducible report generation

New integrations should preserve provenance, cohort identity, privacy, versioning, uncertainty, and human scientific review.

## Example research applications

F61 can serve as a reference architecture for:

- Parkinson literature reviews
- digital biomarker research
- wearable sensing studies
- gait and mobility research
- symptom-fluctuation studies
- non-motor symptom research
- longitudinal progression studies
- multimodal biomarker studies
- cohort stratification
- observational study planning
- research protocol preparation
- AI/ML research governance

## Design principles

1. Define the research question before collecting evidence.
2. Preserve source provenance for every consequential claim.
3. Define cohorts explicitly and include disease-context variables.
4. Distinguish candidate biomarkers from validated biomarkers.
5. Keep endpoint definitions precise.
6. Prevent participant and temporal leakage in predictive studies.
7. Distinguish association from causation.
8. Preserve contradictory evidence and limitations.
9. Fail closed when research integrity requirements are incomplete.
10. Keep scientific and clinical authority with qualified humans.

## Documentation

Additional architecture documentation is available under:

- `docs/ARCHITECTURE.md`

## Citation and reuse

This repository is intended to be studied, referenced, and adapted as part of a broader multi-agent engineering library. When reusing the architecture, preserve attribution, evidence provenance, scientific limitations, and the human-review boundary specified by the repository license and citation metadata where provided.

## Responsible use

Use F61 as a Parkinson research workflow and multi-agent architecture reference. Validate scientific sources, cohort definitions, measurements, biomarkers, statistical assumptions, privacy requirements, ethics obligations, and conclusions against the actual research program. Patient-specific diagnosis, treatment, and clinical decisions remain outside the authority of this system.