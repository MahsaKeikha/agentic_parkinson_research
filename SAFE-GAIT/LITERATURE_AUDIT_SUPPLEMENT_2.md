# SAFE-GAIT: Literature Audit — Supplement 2
**28 October 2026. Primary-source discovery tranche.** References below extend, rather than replace, `LITERATURE_NOVELTY_AUDIT.md`. The existing tranche contains 13 records. This supplement contains **17 additional, nonduplicate works** (30 candidates total). Bibliographic metadata, relevance and exact citation fields must be checked again before paper submission; 30 candidates do not mean 30 manuscript-ready citations.

## Original FoG and monitoring studies

| ID | Publication | Primary record | Relevance |
|---|---|---|---|
| F9 | Shi et al., 2022. Detection of Freezing of Gait Using Convolutional Neural Networks and Data From Lower Limb Motion Sensors. IEEE TBME. DOI 10.1109/TBME.2022.3140258 | https://pubmed.ncbi.nlm.nih.gov/34986092/ | Neural-model comparator and sensor-site contrast |
| F10 | Borzì et al., 2023. Real-time detection of freezing of gait in Parkinson's disease using multi-head convolutional neural networks and a single inertial sensor. Artificial Intelligence in Medicine. DOI 10.1016/j.artmed.2022.102459 | https://pubmed.ncbi.nlm.nih.gov/36628783/ | Real-time detection and latency |
| F11 | Haussler et al., 2025. Refinement of an Algorithm to Detect and Predict Freezing of Gait in Parkinson Disease Using Wearable Sensors. Sensors 25(1):124. DOI 10.3390/s25010124 | https://doi.org/10.3390/s25010124 | False-positive burden and onset prediction |
| F12 | A Comparative Study of Time Frequency Representation Techniques for Freeze of Gait Detection and Prediction. Sensors 21(19):6446 (2021). DOI 10.3390/s21196446 | https://pubmed.ncbi.nlm.nih.gov/34640763/ | Signal feature representations |
| F13 | A machine learning contest enhances automated freezing of gait detection and reveals time-of-day effects (2024) | https://pubmed.ncbi.nlm.nih.gov/38844449/ | Strong alternative models and continuous-life evaluation |
| F14 | Beyond the Leaderboard: Evaluating the Robustness of Deep Learning Models for Detecting Freezing of Gait (2026) | https://pubmed.ncbi.nlm.nih.gov/41657009/ | **Very close** independent external robustness precedent; models can sometimes generalize |
| F15 | Deep learning for freezing of gait assessment using inertial measurement units: a multicentre validation study (2026) | https://pubmed.ncbi.nlm.nih.gov/42230618/ | **Very close** multisite external evaluation; 85-source and 256-external-participant design |
| F16 | Wang et al., 2025. A Novel Dynamic Latent Variables-Based Framework for Enhancing Freezing of Gait Detection in Parkinson's Disease Patients. IEEE JBHI. DOI 10.1109/JBHI.2025.3567119 | https://pubmed.ncbi.nlm.nih.gov/40323751/ | Personalized process-control precedent |
| F17 | Yang et al., 2025. Multimodal Freezing of Gait Detection: Analyzing the Benefits and Limitations of Physiological Data. IEEE TNSRE. DOI 10.1109/TNSRE.2025.3545110 | https://pubmed.ncbi.nlm.nih.gov/40031584/ | IMU limitations and physiological modalities |
| F18 | Zhang et al., 2024. Detection and prediction of freezing of gait with wearable sensors in Parkinson's disease. Neurological Sciences 45:431–453. DOI 10.1007/s10072-023-07017-y | https://pubmed.ncbi.nlm.nih.gov/37843692/ | Review of inconsistent evaluation protocols |
| F19 | Huang et al., 2023. Recent trends in wearable device used to detect freezing of gait and falls in people with Parkinson's disease: A systematic review. Frontiers in Aging Neuroscience 15:1119956. DOI 10.3389/fnagi.2023.1119956 | https://pubmed.ncbi.nlm.nih.gov/36875701/ | Domain review, not evidence of a new algorithm |
| F20 | The Usefulness of Wearable Sensors for Detecting Freezing of Gait in Parkinson's Disease: A Systematic Review (2025) | https://pubmed.ncbi.nlm.nih.gov/40871963/ | Lab-versus-free-living distinction |
| F21 | Intelligent wearable system with accurate detection of abnormal gait and timely cueing for mobility enhancement of people with Parkinson's disease (2024) | https://pubmed.ncbi.nlm.nih.gov/38486907/ | Intervention and actual latency distinction |

## Foundational statistical and AI work

| ID | Publication | Primary record | Relevance |
|---|---|---|---|
| T6 | Geifman & El-Yaniv, 2017. Selective Classification for Deep Neural Networks. NeurIPS 30 | https://papers.neurips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html | Reject option and selective-risk precedent |
| T7 | Guo et al., 2017. On Calibration of Modern Neural Networks. ICML, PMLR 70:1321–1330 | https://proceedings.mlr.press/v70/guo17a.html | Calibration does not establish out-of-domain trust |
| T8 | Lipton, Wang & Smola, 2018. Detecting and Correcting for Label Shift with Black Box Predictors. ICML, PMLR 80:3122–3130 | https://proceedings.mlr.press/v80/lipton18a.html | Output-based label shift requires assumptions |
| T9 | Hendrycks & Gimpel, 2017. A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks. ICLR | https://openreview.net/references/pdf?id=HJ2Pfowdg | Confidence as warning baseline and limitations |

## Mandatory interpretation corrections

1. The 2025 Borzì and colleagues study already reported **88–95% detection of FoG episodes in external datasets**, while highlighting false alarms. We must not infer from our failed trunk-to-back transfer that transfer is impossible (https://pubmed.ncbi.nlm.nih.gov/40091409/).
2. The 2026 multi-centre study explicitly evaluates external heterogeneity and human-in-the-loop adaptation (https://pubmed.ncbi.nlm.nih.gov/42230618/). Our novelty is not simply calling for human oversight.
3. A 2026 robustness evaluation of contest-winning models found some models did transfer to home recordings, whereas episode counting and subtype tasks remained difficult (https://pubmed.ncbi.nlm.nih.gov/41657009/).
4. **FoG-STAR provenance gate:** published scientific paper describes 22 participants and 101 episodes; our audited CSV subset contains nine participant IDs and 28 episodes. The current dataset release, file selection, file integrity, missing sessions, annotation schema and exact event grouping must be reconciled **before any final population claim**. Compare https://www.nature.com/articles/s41597-026-06645-1 and https://zenodo.org/records/17037669.
5. We should name the central contribution a **failure-auditing case study**, not a clinically validated safety controller. The mismatch of pooled and single-participant warning calibration is potentially educational but may not be independently novel.

## Citation placement matrix (initial)
| Manuscript claim | Primary sources | Evidence still needed |
|---|---|---|
| FoG wearables have established detection and cueing work | F1, F7, F10, F11 | Exact quote-free paraphrase with numbered ACM citations |
| Sensor placement and protocols affect comparisons | F3, F15, F17, F20 | Protocol compatibility table |
| External performance is heterogeneous, but not invariably poor | F3, F5, F14, F15 | Comparison of sensor site, cohorts, events and thresholds |
| Abstention/risk-coverage are established | T1, T6 | Distinguish our empirical audit from inventing method |
| Source-score drift is not proof of harmful conditional failure | T2, T8, T9 | Independent source false-warning study |
| Probability calibration depends on evaluation distribution | T7, T4, T5 | Show target reliability rather than assume guarantees |
| Event detection and false alerts matter | F2, F3, F6, F11, F14 | Clinical matching-rule sensitivity analysis |
| Source calibration should match deployment unit | SAFE-GAIT empirical observation | Independent replication before general conclusion |

**Next:** reconcile data provenance, complete article metadata/BibTeX, integrate numbered references and figure provenance into the ACM manuscript.