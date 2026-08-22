from __future__ import annotations

from typing import Any


REQUIRED_SPECIALISTS = {
    "literature_scout",
    "cohort_design",
    "biomarker_evidence",
    "study_design",
    "evidence_quality",
    "human_review",
}


def evaluate(result: dict[str, Any]) -> dict[str, Any]:
    specialists = set(result.get("specialists", {}))
    governance = result.get("governance", {})
    missing = sorted(REQUIRED_SPECIALISTS - specialists)
    passed = (
        not missing
        and governance.get("human_approval_required") is True
        and governance.get("autonomous_treatment_authority") is False
        and governance.get("patient_specific_clinical_authority") is False
    )
    return {"passed": passed, "missing_specialists": missing}
