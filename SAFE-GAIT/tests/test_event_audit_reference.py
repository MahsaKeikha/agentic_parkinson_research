"""Contract tests for the independent SAFE-GAIT event-audit reference."""
import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "tools" / "event_audit_reference.py"
spec = importlib.util.spec_from_file_location("event_audit_reference", MODULE)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


def test_one_alert_cannot_match_two_events():
    pairs = audit_module.maximum_matching([(1, 2), (3, 4)], [(1.5, 3.5)])
    assert len(pairs) == 1


def test_maximum_not_greedy_matching():
    # First event can match either alert; second event only first alert.
    pairs = audit_module.maximum_matching([(1, 4), (1, 2)], [(1, 2), (3, 4)])
    assert len(pairs) == 2


def test_window_end_prevents_lookahead():
    result = audit_module.audit({"events": [[0, 1]], "windows": [
        {"end_s": 2, "positive": True}], "recording_hours": 1,
        "alert_hold_s": 0, "tolerance_s": 0})
    assert result["matched_event_count"] == 0


def test_abstention_is_not_negative_or_alert():
    result = audit_module.audit({"events": [[1, 2]], "windows": [
        {"end_s": 1.5, "positive": True, "abstain": True}],
        "recording_hours": 2})
    assert result["missed_event_count"] == 1
    assert result["alert_count"] == 0
    assert result["abstained_window_count"] == 1


def test_no_events_undefined_recall():
    result = audit_module.audit({"events": [], "windows": [],
                                 "recording_hours": 1})
    assert result["event_recall"] is None


def test_invalid_exposure_rejected():
    with pytest.raises(ValueError):
        audit_module.audit({"events": [], "windows": [], "recording_hours": 0})


def test_tolerance_changes_matching():
    e, a = [(1, 2)], [(2.2, 2.2)]
    assert not audit_module.maximum_matching(e, a, 0)
    assert len(audit_module.maximum_matching(e, a, 0.25)) == 1


def test_overlapping_positive_windows_are_one_alert_run():
    result = audit_module.audit({
        "events": [[2.1, 2.8]],
        "windows": [
            {"end_s": 2, "positive": True},
            {"end_s": 2.5, "positive": True},
            {"end_s": 3, "positive": True},
        ],
        "recording_hours": 1,
        "alert_hold_s": 1,
    })
    assert result["alert_count"] == 1
    assert result["matched_event_count"] == 1
    assert result["unmatched_alert_count"] == 0


def test_disjoint_alert_runs_remain_separate():
    result = audit_module.audit({
        "events": [],
        "windows": [
            {"end_s": 2, "positive": True},
            {"end_s": 5, "positive": True},
        ],
        "recording_hours": 2,
        "alert_hold_s": 1,
    })
    assert result["alert_count"] == 2
    assert result["unmatched_alerts_per_hour"] == 1


def test_touching_alert_intervals_merge():
    result = audit_module.audit({
        "events": [],
        "windows": [
            {"end_s": 2, "positive": True},
            {"end_s": 3, "positive": True},
        ],
        "recording_hours": 1,
        "alert_hold_s": 1,
    })
    assert result["alert_count"] == 1
