from orchestration.orchestrator import REQUIRED_GATES, orchestrate


def demo_context():
    context = {gate: True for gate in REQUIRED_GATES}
    context.update(
        research_question="Parkinson research workflow",
        patient_specific_diagnosis_requested=False,
        prescription_requested=False,
        treatment_authorization_requested=False,
        unsupported_causal_claim=False,
        fabricated_or_unverified_evidence=False,
        unresolved_research_questions=[],
        human_approval=True,
    )
    return context


if __name__ == "__main__":
    print(orchestrate(demo_context()))
