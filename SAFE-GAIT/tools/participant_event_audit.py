"""Participant-cluster event audit for SAFE-GAIT.

Each recording is evaluated separately, preventing alerts from merging across
participants, sessions, or clock resets. Cluster bootstrap resamples participants
(not windows or sessions) and recomputes pooled event and exposure denominators.
This is an analysis utility, not a FoG-STAR v3 empirical result.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "safe_gait_event_audit", Path(__file__).with_name("event_audit_reference.py")
)
_event_audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_event_audit)


def _ratio(num, den):
    return num / den if den else None


def _aggregate(rows):
    keys = ("reference_event_count", "alert_count", "matched_event_count",
            "missed_event_count", "unmatched_alert_count", "abstained_window_count")
    totals = {key: sum(row[key] for row in rows) for key in keys}
    totals["recording_hours"] = sum(row["recording_hours"] for row in rows)
    totals["event_recall"] = _ratio(
        totals["matched_event_count"], totals["reference_event_count"]
    )
    totals["unmatched_alerts_per_hour"] = _ratio(
        totals["unmatched_alert_count"], totals["recording_hours"]
    )
    return totals


def audit_cohort(recordings, bootstrap_replicates=0, seed=2026):
    if not isinstance(recordings, list) or not recordings:
        raise ValueError("nonempty recordings list required")
    if isinstance(bootstrap_replicates, bool) or not isinstance(bootstrap_replicates, int) or bootstrap_replicates < 0:
        raise ValueError("bootstrap_replicates must be nonnegative integer")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be integer")
    seen = set()
    per_recording = []
    for record in recordings:
        if not isinstance(record, dict):
            raise ValueError("each recording must be an object")
        participant = record.get("participant_id")
        session = record.get("session_id")
        if not isinstance(participant, str) or not participant.strip():
            raise ValueError("participant_id required")
        if not isinstance(session, str) or not session.strip():
            raise ValueError("session_id required")
        key = (participant, session)
        if key in seen:
            raise ValueError("duplicate participant/session recording")
        seen.add(key)
        # A session's monotonic clock is independent of all other sessions.
        result = _event_audit.audit(record)
        per_recording.append({"participant_id": participant, "session_id": session,
                              "recording_hours": float(record["recording_hours"]),
                              **result})
    participants = sorted({r["participant_id"] for r in per_recording})
    grouped = {
        p: _aggregate([r for r in per_recording if r["participant_id"] == p])
        for p in participants
    }
    pooled = _aggregate(per_recording)
    # Primary estimand from frozen protocol: participant-macro recall.
    # Participants with zero reference events have undefined recall and are excluded,
    # never silently assigned a perfect score or zero.
    def macro_recall(groups):
        values = [row["event_recall"] for row in groups if row["event_recall"] is not None]
        return sum(values) / len(values) if values else None

    primary_macro = macro_recall(grouped.values())
    bootstrap = {"replicates_requested": bootstrap_replicates, "seed": seed,
                 "unit": "participant", "evaluable_event_recall": 0,
                 "evaluable_false_alert_rate": 0, "event_recall_percentile_95": None,
                 "participant_macro_recall_percentile_95": None,
                 "evaluable_participant_macro_recall": 0,
                 "unmatched_alerts_per_hour_percentile_95": None}
    if bootstrap_replicates:
        rng = random.Random(seed)
        recall_samples, rate_samples, macro_samples = [], [], []
        for _ in range(bootstrap_replicates):
            draws = [grouped[rng.choice(participants)] for _ in participants]
            sampled = _aggregate(draws)
            macro = macro_recall(draws)
            if macro is not None:
                macro_samples.append(macro)
            if sampled["event_recall"] is not None:
                recall_samples.append(sampled["event_recall"])
            if sampled["unmatched_alerts_per_hour"] is not None:
                rate_samples.append(sampled["unmatched_alerts_per_hour"])

        def percentile_interval(samples):
            if not samples:
                return None
            ordered = sorted(samples)

            def percentile(q):
                pos = (len(ordered) - 1) * q
                lo = math.floor(pos)
                hi = math.ceil(pos)
                return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)
            return [percentile(0.025), percentile(0.975)]

        bootstrap.update({
            "evaluable_event_recall": len(recall_samples),
            "evaluable_participant_macro_recall": len(macro_samples),
            "participant_macro_recall_percentile_95": percentile_interval(macro_samples),
            "evaluable_false_alert_rate": len(rate_samples),
            "event_recall_percentile_95": percentile_interval(recall_samples),
            "unmatched_alerts_per_hour_percentile_95": percentile_interval(rate_samples),
        })
    return {"recording_count": len(per_recording), "participant_count": len(participants),
            "per_recording": per_recording, "per_participant": grouped,
            "pooled": pooled, "participant_macro_event_recall": primary_macro,
            "participant_bootstrap": bootstrap,
            "limitations": "Descriptive cluster bootstrap; no clinical safety or population guarantee"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--bootstrap-replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    report = audit_cohort(payload["recordings"], args.bootstrap_replicates, args.seed)
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
