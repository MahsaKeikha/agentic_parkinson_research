"""Synthetic checks for predeclared sensitivity-grid reporting."""
import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "tools" / "alert_policy_sensitivity.py"
spec = importlib.util.spec_from_file_location("alert_policy_sensitivity", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    return [{"participant_id": "p1", "session_id": "s1",
             "events": [[2, 3]], "windows": [{"end_s": 3.5, "positive": True}],
             "recording_hours": 1, "alert_hold_s": 9, "tolerance_s": 9}]


def test_all_settings_reported_without_selection():
    result = module.sensitivity_grid(fixture())
    assert len(result["results"]) == 9
    assert result["policy_selection"].startswith("none")


def test_tolerance_affects_matching():
    result = module.sensitivity_grid(fixture(), hold_seconds=(0,), tolerance_seconds=(0, 0.5))
    assert result["results"][0]["matched_event_count"] == 0
    assert result["results"][1]["matched_event_count"] == 1


def test_original_records_not_mutated():
    records = fixture()
    module.sensitivity_grid(records)
    assert records[0]["alert_hold_s"] == 9
    assert records[0]["tolerance_s"] == 9


def test_duplicate_policy_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        module.sensitivity_grid(fixture(), hold_seconds=(1, 1))
