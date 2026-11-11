"""Synthetic contract tests: never confuse these with full-v3 outcomes."""
import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "tools" / "participant_event_audit.py"
spec = importlib.util.spec_from_file_location("participant_event_audit", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def session(person, name, events, ends, hours=1):
    return {"participant_id": person, "session_id": name,
            "events": events, "windows": [{"end_s": end, "positive": True} for end in ends],
            "recording_hours": hours, "alert_hold_s": 1}


def test_no_alert_merging_across_sessions():
    records = [session("p1", "a", [], [2]), session("p1", "b", [], [2])]
    result = module.audit_cohort(records)
    assert result["pooled"]["alert_count"] == 2
    assert result["pooled"]["unmatched_alert_count"] == 2


def test_same_clock_different_participants_are_independent():
    records = [session("p1", "a", [[2, 3]], [2]),
               session("p2", "a", [[2, 3]], [])]
    result = module.audit_cohort(records)
    assert result["pooled"]["matched_event_count"] == 1
    assert result["pooled"]["reference_event_count"] == 2
    assert result["pooled"]["event_recall"] == 0.5


def test_cluster_bootstrap_is_deterministic():
    records = [session("p1", "a", [[2, 3]], [2]),
               session("p2", "a", [[2, 3]], [])]
    a = module.audit_cohort(records, bootstrap_replicates=100, seed=42)
    b = module.audit_cohort(records, bootstrap_replicates=100, seed=42)
    assert a["participant_bootstrap"] == b["participant_bootstrap"]
    assert a["participant_bootstrap"]["evaluable_event_recall"] == 100


def test_zero_event_bootstrap_has_no_fake_recall_interval():
    records = [session("p1", "a", [], [2])]
    result = module.audit_cohort(records, bootstrap_replicates=25)
    assert result["pooled"]["event_recall"] is None
    assert result["participant_bootstrap"]["event_recall_percentile_95"] is None
    assert result["participant_bootstrap"]["evaluable_event_recall"] == 0


def test_duplicate_session_rejected():
    record = session("p1", "a", [], [])
    with pytest.raises(ValueError, match="duplicate"):
        module.audit_cohort([record, record])


def test_invalid_bootstrap_rejected():
    with pytest.raises(ValueError):
        module.audit_cohort([session("p1", "a", [], [])], bootstrap_replicates=-1)


def test_exposure_weighted_not_session_mean():
    records = [session("p1", "a", [], [2], hours=1),
               session("p2", "b", [], [], hours=3)]
    result = module.audit_cohort(records)
    assert result["pooled"]["unmatched_alerts_per_hour"] == 0.25
