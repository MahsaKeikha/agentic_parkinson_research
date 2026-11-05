"""Fail-closed readiness gate contract tests."""
import importlib.util
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "scientific_readiness_gate.py"
spec = importlib.util.spec_from_file_location("scientific_readiness_gate", MODULE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def test_empty_record_blocked():
    result = gate.evaluate({})
    assert result["status"] == "BLOCKED"
    assert result["passed_gate_count"] == 0


def test_ci_green_not_enough():
    result = gate.evaluate({"ci": {"status": "success"}})
    assert result["status"] == "BLOCKED"


def test_fake_hash_is_rejected():
    record = {"evidence": {"official_v3_provenance": {
        "verified": True, "artifact": "manifest.json", "sha256": "placeholder"}}}
    result = gate.evaluate(record)
    assert any("invalid artifact SHA-256" in s for s in result["blockers"])


def test_missing_full_run_checks_block_even_when_artifact_fields_present():
    sha = "a" * 64
    record = {"evidence": {key: {
        "verified": True, "artifact": f"{key}.json", "sha256": sha
    } for key in gate.REQUIRED}}
    result = gate.evaluate(record)
    assert result["status"] == "BLOCKED"
    assert any("checksum verification absent" in s for s in result["blockers"])
    assert any("historical estimates not replaced" in s for s in result["blockers"])


def test_complete_claims_pass_structural_gate_only():
    sha = "a" * 64
    evidence = {key: {"verified": True, "artifact": f"{key}.json",
                      "sha256": sha} for key in gate.REQUIRED}
    evidence["full_v3_run"].update(dataset_version="FoG-STAR v3",
                                   checksum_verified=True)
    evidence["corrected_event_results"]["historical_estimates_replaced"] = True
    evidence["acm_pdf_traceability"]["cites_corrected_results"] = True
    result = gate.evaluate({"evidence": evidence})
    assert not result["blockers"]
    # This is deliberately a schema/attestation check, not independent verification.
    assert result["status"] == "SCIENTIFICALLY_READY_FOR_HUMAN_SUBMISSION_DECISION"
