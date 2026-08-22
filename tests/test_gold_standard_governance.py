from orchestration.orchestrator import AGENTS, REQUIRED_GATES, evaluate_research, orchestrate
from safety.clinical_gate import clinical_gate


def ready_context():
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


def test_ready_research_requires_all_gates_and_human_approval():
    result = evaluate_research(ready_context())
    assert result["status"] == "READY_FOR_AUTHORIZED_RESEARCH_REVIEW"
    assert result["blockers"] == []
    assert result["autonomous_treatment_authority"] is False
    assert result["patient_specific_clinical_authority"] is False


def test_each_required_gate_fails_closed():
    for gate in REQUIRED_GATES:
        context = ready_context()
        context[gate] = False
        result = evaluate_research(context)
        assert result["status"] == "BLOCKED", gate


def test_clinical_requests_are_out_of_scope():
    for key in (
        "patient_specific_diagnosis_requested",
        "prescription_requested",
        "treatment_authorization_requested",
    ):
        context = ready_context()
        context[key] = True
        assert evaluate_research(context)["status"] == "BLOCKED", key
        assert clinical_gate(context)["allowed"] is False


def test_unverified_evidence_and_unsupported_causality_block():
    context = ready_context()
    context["fabricated_or_unverified_evidence"] = True
    context["unsupported_causal_claim"] = True
    result = evaluate_research(context)
    assert result["status"] == "BLOCKED"
    assert len(result["blockers"]) >= 2


def test_human_approval_is_mandatory():
    context = ready_context()
    context["human_approval"] = False
    result = evaluate_research(context)
    assert result["status"] == "BLOCKED"
    assert any("human" in blocker for blocker in result["blockers"])


def test_all_specialists_execute():
    result = orchestrate(ready_context())
    expected = {agent_class().name for agent_class in AGENTS}
    assert set(result["specialists"]) == expected
    assert len(result["specialists"]) == 6
    assert result["governance"]["status"] == "READY_FOR_AUTHORIZED_RESEARCH_REVIEW"


def test_clinical_gate_never_grants_clinical_authority():
    result = clinical_gate(ready_context())
    assert result["allowed"] is True
    assert result["requires_human_review"] is True
    assert result["clinical_authority"] is False
