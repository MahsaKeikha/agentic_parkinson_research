"""Fail-closed SAFE-GAIT scientific evidence gate.

Usage:
 python SAFE-GAIT/tools/scientific_readiness_gate.py evidence.json

The gate checks the presence and internal consistency of independently verified
evidence records; it does not independently validate scientific truth.
An absent, placeholder, or unverified field blocks submission readiness.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
REQUIRED = (
    "official_v3_provenance",
    "expert_episode_reconciliation",
    "frozen_source_only_protocol",
    "full_v3_run",
    "corrected_event_results",
    "participant_level_uncertainty",
    "comparator_results",
    "methods_citation_audit",
    "acm_pdf_traceability",
    "independent_scientific_review",
)


def evaluate(record):
    if not isinstance(record, dict):
        raise ValueError("Evidence must be a JSON object")
    blockers = []
    evidence = record.get("evidence", {})
    if not isinstance(evidence, dict):
        raise ValueError("evidence must be an object")
    for name in REQUIRED:
        item = evidence.get(name)
        if not isinstance(item, dict):
            blockers.append(f"{name}: missing evidence record")
            continue
        if item.get("verified") is not True:
            blockers.append(f"{name}: not independently verified")
        if not isinstance(item.get("artifact"), str) or not item["artifact"].strip():
            blockers.append(f"{name}: missing artifact reference")
        if not isinstance(item.get("sha256"), str) or not HEX64.fullmatch(item["sha256"]):
            blockers.append(f"{name}: missing or invalid artifact SHA-256")
    # Never infer successful scientific validation from a CI status field.
    run = evidence.get("full_v3_run", {})
    if isinstance(run, dict):
        if run.get("dataset_version") != "FoG-STAR v3":
            blockers.append("full_v3_run: dataset version not verified as FoG-STAR v3")
        if run.get("checksum_verified") is not True:
            blockers.append("full_v3_run: dataset checksum verification absent")
    results = evidence.get("corrected_event_results", {})
    if isinstance(results, dict) and results.get("historical_estimates_replaced") is not True:
        blockers.append("corrected_event_results: historical estimates not replaced")
    pdf = evidence.get("acm_pdf_traceability", {})
    if isinstance(pdf, dict) and pdf.get("cites_corrected_results") is not True:
        blockers.append("acm_pdf_traceability: updated PDF does not cite corrected run")
    return {
        "status": "SCIENTIFICALLY_READY_FOR_HUMAN_SUBMISSION_DECISION" if not blockers else "BLOCKED",
        "blockers": blockers,
        "passed_gate_count": len(REQUIRED) - sum(
            not isinstance(evidence.get(name), dict)
            or evidence[name].get("verified") is not True
            or not isinstance(evidence[name].get("artifact"), str)
            or not evidence[name]["artifact"].strip()
            or not isinstance(evidence[name].get("sha256"), str)
            or not HEX64.fullmatch(evidence[name]["sha256"])
            for name in REQUIRED
        ),
        "total_gate_count": len(REQUIRED),
        "ci_success_is_not_scientific_evidence": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_json", type=Path)
    args = parser.parse_args()
    report = evaluate(json.loads(args.evidence_json.read_text(encoding="utf-8")))
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not report["blockers"] else 2)


if __name__ == "__main__":
    main()
