"""Reference event audit: causal alert timing and maximum-cardinality one-to-one matching.

This is a dependency-free, testable implementation of the event-accounting rule,
NOT a clinical episode adjudicator and NOT a full FoG-STAR dataset run.

Input JSON:
{"events": [[start_s, end_s], ...],
 "windows": [{"end_s": 1.5, "positive": true, "abstain": false}, ...],
 "recording_hours": 1.0, "alert_hold_s": 1.0, "tolerance_s": 0.0}
Times must share the same monotonic recording clock. Events are [start,end]
intervals; zero-length alerts are treated as points.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def _finite_nonnegative(x, label):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0:
        raise ValueError(f"{label} must be finite and nonnegative")
    return float(x)


def _interval(pair):
    if len(pair) != 2:
        raise ValueError("event requires start and end")
    a, b = (_finite_nonnegative(pair[0], "start"), _finite_nonnegative(pair[1], "end"))
    if b <= a:
        raise ValueError("event end must exceed start")
    return a, b


def _overlaps(event, alert, tolerance):
    # Closed-interval contact counts as overlap; report convention explicitly.
    return alert[1] >= event[0] - tolerance and alert[0] <= event[1] + tolerance


def maximum_matching(events, alerts, tolerance_s=0.0):
    """Return (event_index, alert_index) pairs with maximum cardinality."""
    tol = _finite_nonnegative(tolerance_s, "tolerance_s")
    events = [_interval(e) for e in events]
    alerts = [tuple(a) for a in alerts]
    for a, b in alerts:
        _finite_nonnegative(a, "alert start")
        _finite_nonnegative(b, "alert end")
        if b < a:
            raise ValueError("alert end precedes start")
    adjacency = [[j for j, a in enumerate(alerts) if _overlaps(e, a, tol)] for e in events]
    matched_alert = {}

    def augment(i, seen):
        for j in adjacency[i]:
            if j in seen:
                continue
            seen.add(j)
            if j not in matched_alert or augment(matched_alert[j], seen):
                matched_alert[j] = i
                return True
        return False

    for i in range(len(events)):
        augment(i, set())
    return sorted((i, j) for j, i in matched_alert.items())


def audit(payload):
    events = [_interval(e) for e in payload["events"]]
    hold = _finite_nonnegative(payload.get("alert_hold_s", 1.0), "alert_hold_s")
    tol = _finite_nonnegative(payload.get("tolerance_s", 0.0), "tolerance_s")
    hours = _finite_nonnegative(payload["recording_hours"], "recording_hours")
    if hours == 0:
        raise ValueError("recording_hours must be positive")
    alerts = []
    abstained = 0
    for w in payload["windows"]:
        end = _finite_nonnegative(w["end_s"], "window end_s")
        if not isinstance(w.get("positive"), bool) or not isinstance(w.get("abstain", False), bool):
            raise ValueError("positive and abstain must be boolean")
        if w.get("abstain", False):
            abstained += 1
        elif w["positive"]:
            alerts.append((end, end + hold))
    # Merge overlapping/touching positive alert holds into alert *runs* before\n    # one-to-one matching. Individual positive windows are not independent alarms.\n    alerts.sort(key=lambda interval: (interval[0], interval[1]))\n    merged = []\n    for start, stop in alerts:\n        if merged and start <= merged[-1][1]:\n            merged[-1] = (merged[-1][0], max(merged[-1][1], stop))\n        else:\n            merged.append((start, stop))\n    alerts = merged\n    matches = maximum_matching(events, alerts, tol)
    unmatched = len(alerts) - len(matches)
    return {
        "reference_event_count": len(events),
        "alert_count": len(alerts),\n        "alert_count_definition": "merged contiguous or overlapping emitted alert intervals",
        "matched_event_count": len(matches),
        "missed_event_count": len(events) - len(matches),
        "unmatched_alert_count": unmatched,
        "unmatched_alerts_per_hour": unmatched / hours,
        "event_recall": len(matches) / len(events) if events else None,
        "abstained_window_count": abstained,
        "matching_pairs": matches,
        "policy": {"alert_hold_s": hold, "tolerance_s": tol,
                   "timestamp_rule": "window-end causal emission",
                   "overlap_rule": "closed intervals; boundary contact matches"},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.input_json.read_text(encoding="utf-8")))
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
