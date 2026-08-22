import json
from pathlib import Path

from orchestration.orchestrator import REQUIRED_GATES, evaluate_research


def base_context():
    context = {gate: True for gate in REQUIRED_GATES}
    context.update(
        patient_specific_diagnosis_requested=False,
        prescription_requested=False,
        treatment_authorization_requested=False,
        unsupported_causal_claim=False,
        fabricated_or_unverified_evidence=False,
        unresolved_research_questions=[],
        human_approval=True,
    )
    return context


SCENARIOS = [
    ("ready", {}, "READY_FOR_AUTHORIZED_RESEARCH_REVIEW"),
    ("missing_provenance", {"data_provenance_verified": False}, "BLOCKED"),
    ("missing_traceability", {"literature_sources_traceable": False}, "BLOCKED"),
    ("cohort_gap", {"cohort_definition_reviewed": False}, "BLOCKED"),
    ("biomarker_evidence_gap", {"biomarker_claims_evidence_linked": False}, "BLOCKED"),
    ("patient_diagnosis_request", {"patient_specific_diagnosis_requested": True}, "BLOCKED"),
    ("prescription_request", {"prescription_requested": True}, "BLOCKED"),
    ("unsupported_causality", {"unsupported_causal_claim": True}, "BLOCKED"),
    ("unverified_evidence", {"fabricated_or_unverified_evidence": True}, "BLOCKED"),
    ("missing_human_approval", {"human_approval": False}, "BLOCKED"),
]


def main():
    rows = []
    for name, changes, expected in SCENARIOS:
        context = base_context()
        context.update(changes)
        actual = evaluate_research(context)["status"]
        rows.append(
            {
                "scenario": name,
                "expected": expected,
                "actual": actual,
                "passed": actual == expected,
            }
        )

    passed = sum(row["passed"] for row in rows)
    result = {
        "passed": passed,
        "total": len(rows),
        "pass_rate": passed / len(rows),
        "results": rows,
    }
    Path("heldout-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed == len(rows) else 1)


if __name__ == "__main__":
    main()
