# SAFE-GAIT: Primary-Source Literature and Novelty Audit

**29 October 2026. First verified tranche. Not yet a complete bibliography.**

This audit records primary publication or original study pages, rather than
secondary summaries. Titles, publication venues and URLs were checked during
the literature search. This is an initial source list, **not** a claim that
30 fully verified references are already available. Final BibTeX metadata,
page numbers and every DOI must be checked before submission.

## A. Parkinson's freezing-of-gait studies and datasets

| ID | Primary work | Link | Why it matters for SAFE-GAIT |
|---|---|---|---|
| F1 | Bächlin et al. (2010), *Wearable assistant for Parkinson's disease patients with the freezing of gait symptom*, IEEE Transactions on Information Technology in Biomedicine | https://pubmed.ncbi.nlm.nih.gov/19906597/ | Foundational wearable detection/cueing and provenance of the Daphnet research lineage |
| F2 | *Development, Validation, and Limits of Freezing of Gait Detection Using a Single Waist-Worn Device* (2024) | https://pubmed.ncbi.nlm.nih.gov/38814761/ | Direct precedent for reporting validation limits rather than only accuracy |
| F3 | *Freezing of gait detection: The effect of sensor type, position, activities, datasets, and machine learning model* (2025) | https://pubmed.ncbi.nlm.nih.gov/40091409/ | Very close domain precedent: activity, placement, external-data evaluation, event sensitivity and false alarms |
| F4 | *A multi-level annotated sensor dataset of gait freezing manifestations and severity in Parkinson's disease* (FoG-STAR data paper, 2026) | https://pubmed.ncbi.nlm.nih.gov/41588027/ | Original dataset paper reports 22 participants and 101 episodes in the full resource; our analyzed sensor file has only 9 IDs and 28 episodes, a discrepancy requiring reconciliation |
| F5 | Lin and Grewal (2026), *Deep Learning for Freezing of Gait Detection: Cross-Dataset Validation Reveals Critical Deployment Gaps Between Laboratory and Daily Living Wearable Monitoring*, Sensors 26(4):1352 | https://pubmed.ncbi.nlm.nih.gov/41755290/ | Closest direct cross-dataset generalization precedent; prohibits claiming the generalization gap itself as novel |
| F6 | *Technology for measuring freezing of gait: Current state of the art and recommendations* (2025) | https://pubmed.ncbi.nlm.nih.gov/39973491/ | Domain methodology and clinical-measurement expectations |
| F7 | *Wearable Online Freezing of Gait Detection and Cueing System* (2024) | https://pubmed.ncbi.nlm.nih.gov/39451423/ | Operational latency and cueing context; separates retrospective window accuracy from real-time deployment |
| F8 | *Toward a Wearable System for Predicting Freezing of Gait in People Affected by Parkinson's Disease* (2019) | https://pubmed.ncbi.nlm.nih.gov/31715577/ | Distinguishes prediction before onset from detection after observing a window |

## B. Trustworthy classification and distribution shift

| ID | Primary work | Link | Why it matters for SAFE-GAIT |
|---|---|---|---|
| T1 | Geifman and El-Yaniv (2019), *SelectiveNet: A Deep Neural Network with an Integrated Reject Option*, ICML / PMLR 97 | https://proceedings.mlr.press/v97/geifman19a.html | The reject-option/risk-coverage paradigm is established, not novel to SAFE-GAIT |
| T2 | Pouget et al. (2025), *Suitability Filter: A Statistical Framework for Classifier Evaluation in Real-World Deployment Settings*, ICML / PMLR 267 | https://proceedings.mlr.press/v267/pouget25a.html | Explicit precedent for monitoring degradation with unlabeled model-output signals |
| T3 | Ai and Ren (2024), *Not all distributional shifts are equal: Fine-grained robust conformal inference*, ICML / PMLR 235 | https://proceedings.mlr.press/v235/ai24a.html | Distinguishes changes in input distributions from changes in conditional outcome relationships |
| T4 | Jonkers et al. (2024), *Conformal Predictive Systems Under Covariate Shift*, COPA / PMLR 230 | https://proceedings.mlr.press/v230/jonkers24a.html | Relevant assumptions for calibration under shift; do not imply distribution-free safeguards without them |
| T5 | Lee (2026), *Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study*, UAI / PMLR 337 | https://proceedings.mlr.press/v337/lee26g.html | Related general point: identifying shifts is not equivalent to predicting harmful model failures |

**Count so far: 13 primary work records.** These must not be padded to 30
with unverified or irrelevant citations.

## Novelty assessment

### Claims we should **not** make

1. "We are first to discover that laboratory FoG models fail in another
   dataset." F3 and F5 already investigate external-data behavior.
2. "We introduce the reject option or risk-coverage analysis." T1 and other
   established selective-classification work precede this study.
3. "We introduce distribution-shift warnings based on model scores." T2
   directly studies a related output-signal warning principle.
4. "Our model is more trustworthy, generalizable or clinically safe."
   Our own target results show zero detected freezing episodes.

### Potentially defensible, bounded contribution

An **operational failure-analysis protocol** for FoG monitoring that jointly
audits (i) end-of-window, one-to-one event detection and unmatched alerts,
(ii) positive episodes missed during abstention, (iii) source-versus-target
shift warnings, and (iv) sensitivity to the unit of drift-warning calibration.
The specific quantified reversal from six of nine flagged participants
under pooled source folds to one of nine under matched single-participant
calibration is a reproducible case study, but its uniqueness relative to
prior publications still needs systematic review.

### High-priority reviewer challenge

F3 reports strong external episode sensitivity from sensor and model choices
that differ from our intentionally simple trunk/back transfer experiment.
Therefore our 0/28 finding must be framed as a **specific failure case**, not
as proof that transfer from Daphnet or all wearable FoG detection is
impossible. F5 already presents major cross-dataset FoG performance gaps.
Our stronger potential angle is why seemingly reasonable warning or
abstention mechanisms can mask the failure, and how to audit them correctly.

### Minimum next research gates

- Reconcile FoG-STAR source files with the full 22-participant, 101-episode
  dataset publication and record any release difference in the methods.
- Verify a further 17 or more relevant original publications and create
  exact BibTeX entries. Include event-detection metric definitions,
  participant-clustered inference, calibration and failure-monitoring works.
- Produce a claim-to-source matrix with citations in each manuscript section.
- Ask whether a reproducibility or negative-results framing fits the actual
  REED-AI submission category; confirm acceptance of such papers.
- Have a clinical FoG expert review matching tolerance and the interpretation
  of decision latency before claiming clinically meaningful episodes.
