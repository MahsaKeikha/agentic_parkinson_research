"""Predeclared SAFE-GAIT alert-policy sensitivity grid.

Re-evaluates the SAME frozen session records under each hold/tolerance setting.
Does not select an optimal policy from target outcomes. All settings and results
must be reported; this is not a full FoG-STAR v3 experiment.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "safe_gait_participant_audit", Path(__file__).with_name("participant_event_audit.py")
)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)


def sensitivity_grid(recordings, hold_seconds=(0.0, 0.25, 1.0),
                     tolerance_seconds=(0.0, 0.5, 1.0)):
    if not isinstance(recordings, list) or not recordings:
        raise ValueError("nonempty recordings required")
    if not hold_seconds or not tolerance_seconds:
        raise ValueError("nonempty hold and tolerance grids required")
    if len(set(hold_seconds)) != len(hold_seconds) or len(set(tolerance_seconds)) != len(tolerance_seconds):
        raise ValueError("duplicate policy settings")
    rows = []
    for hold in hold_seconds:
        for tolerance in tolerance_seconds:
            # Do not mutate caller data or accidentally carry settings between runs.
            changed = [{**record, "alert_hold_s": hold,
                        "tolerance_s": tolerance} for record in recordings]
            result = _module.audit_cohort(changed)
            rows.append({"alert_hold_s": hold, "tolerance_s": tolerance,
                         "event_recall": result["pooled"]["event_recall"],
                         "matched_event_count": result["pooled"]["matched_event_count"],
                         "reference_event_count": result["pooled"]["reference_event_count"],
                         "unmatched_alert_count": result["pooled"]["unmatched_alert_count"],
                         "unmatched_alerts_per_hour": result["pooled"]["unmatched_alerts_per_hour"],
                         "participant_count": result["participant_count"]})
    return {"policy_selection": "none; all predeclared settings reported",
            "results": rows, "status": "DESCRIPTIVE_ONLY"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    result = sensitivity_grid(payload["recordings"])
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
