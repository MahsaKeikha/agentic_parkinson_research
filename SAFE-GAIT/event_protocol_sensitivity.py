"""Sensitivity of one-to-one episode matching to alert-duration assumptions.

Does not retrain classifiers. The input is an event-level JSON with references
and decision timestamps for ONE recording block. No new empirical claim is made.
"""
import argparse
import json
from pathlib import Path
from events import Episode, match_events

def score_at_decisions(reference, decision_times, flags, hold_seconds=0.0,
                       tolerance_seconds=0.0):
    if len(decision_times) != len(flags):
        raise ValueError("decision_times and flags length mismatch")
    if hold_seconds < 0:
        raise ValueError("hold_seconds cannot be negative")
    if any(b <= a for a,b in zip(decision_times, decision_times[1:])):
        raise ValueError("decision times must be strictly increasing")
    # An instantaneous decision needs a strictly positive epsilon interval for
    # interval-overlap matching; this is an approximation, NOT a measured hold.
    duration = max(float(hold_seconds), 1e-9)
    alerts = [Episode(float(t), float(t) + duration)
              for t, flag in zip(decision_times, flags) if flag]
    refs = [Episode(float(s),float(e)) for s,e in reference]
    return match_events(refs, alerts, tolerance_seconds=tolerance_seconds)

def sensitivity_grid(reference, decision_times, flags,
                     durations=(0., 0.25, 1.), tolerances=(0., 0.5, 1.)):
    output = []
    for hold in durations:
        for tolerance in tolerances:
            m = score_at_decisions(reference,decision_times,flags,hold,tolerance)
            output.append({"assumed_alert_hold_seconds":hold,
                           "matching_tolerance_seconds":tolerance,
                           "event_tp":m["event_tp"],"event_fn":m["event_fn"],
                           "event_fp":m["event_fp"],
                           "event_sensitivity":m["event_sensitivity"]})
    return output

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True,
                   help="JSON with reference [[start,end],...] and decisions/flags, one block")
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    data=json.loads(args.input.read_text())
    report={"status":"protocol sensitivity, not clinical validation",
            "assumptions":"decisions are emitted at end of each window; hold is hypothetical",
            "grid":sensitivity_grid(data["reference"],data["decision_times"],data["flags"])}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2))
if __name__=="__main__":
    main()
