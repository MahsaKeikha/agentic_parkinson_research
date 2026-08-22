from __future__ import annotations

from typing import Any


PROHIBITED_CLINICAL_REQUESTS = (
    "patient_specific_diagnosis_requested",
    "prescription_requested",
    "treatment_authorization_requested",
)


def clinical_gate(context: dict[str, Any]) -> dict[str, Any]:
    blocked_reasons = [key for key in PROHIBITED_CLINICAL_REQUESTS if context.get(key)]
    if context.get("fabricated_or_unverified_evidence"):
        blocked_reasons.append("fabricated_or_unverified_evidence")

    return {
        "allowed": not blocked_reasons,
        "blocked_reasons": blocked_reasons,
        "requires_human_review": True,
        "clinical_authority": False,
    }
