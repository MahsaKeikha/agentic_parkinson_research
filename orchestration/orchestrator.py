from __future__ import annotations

from typing import Any

from AGENTS.biomarker_evidence_agent import BiomarkerEvidenceAgent
from AGENTS.cohort_design_agent import CohortDesignAgent
from AGENTS.evidence_quality_agent import EvidenceQualityAgent
from AGENTS.human_review_agent import HumanReviewAgent
from AGENTS.literature_scout_agent import LiteratureScoutAgent
from AGENTS.study_design_agent import StudyDesignAgent

REQUIRED_GATES = {
    "research_question_defined": "research question is not defined",
    "literature_sources_traceable": "literature sources are not traceable",
    "data_provenance_verified": "data provenance is not verified",
    "cohort_definition_reviewed": "cohort definition has not been reviewed",
    "endpoint_definition_reviewed": "study endpoints have not been reviewed",
    "biomarker_claims_evidence_linked": "biomarker claims are not linked to evidence",
    "statistical_plan_reviewed": "statistical analysis plan has not been reviewed",
    "ethics_scope_confirmed": "research ethics scope is not confirmed",
    "privacy_controls": "privacy controls are incomplete",
    "conflicts_disclosed": "relevant conflicts or limitations are not disclosed",
}


AGENTS = (
    LiteratureScoutAgent,
    CohortDesignAgent,
    BiomarkerEvidenceAgent,
    StudyDesignAgent,
    EvidenceQualityAgent,
    HumanReviewAgent,
)


def evaluate_research(context: dict[str, Any]) -> dict[str, Any]:
    blockers = [
        message for gate, message in REQUIRED_GATES.items() if context.get(gate) is not True
    ]

    if context.get("patient_specific_diagnosis_requested"):
        blockers.append("patient-specific diagnosis is outside this research workflow")
    if context.get("prescription_requested"):
        blockers.append("prescribing medication or treatment is outside this research workflow")
    if context.get("treatment_authorization_requested"):
        blockers.append("treatment authorization is outside this research workflow")
    if context.get("unsupported_causal_claim"):
        blockers.append("unsupported causal claims must not be promoted as research conclusions")
    if context.get("fabricated_or_unverified_evidence"):
        blockers.append("fabricated or unverified evidence is not permitted")
    if context.get("unresolved_research_questions"):
        blockers.append("unresolved research questions remain")
    if context.get("human_approval") is not True:
        blockers.append("qualified human scientific review and approval are required")

    return {
        "status": "READY_FOR_AUTHORIZED_RESEARCH_REVIEW" if not blockers else "BLOCKED",
        "blockers": blockers,
        "human_approval_required": True,
        "patient_specific_clinical_authority": False,
        "autonomous_treatment_authority": False,
        "evidence_traceability_required": True,
    }


def _run_specialists(context: dict[str, Any]) -> dict[str, Any]:
    specialists = [agent_class() for agent_class in AGENTS]
    return {agent.name: agent.run(context) for agent in specialists}


def orchestrate(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "specialists": _run_specialists(context),
        "governance": evaluate_research(context),
    }
