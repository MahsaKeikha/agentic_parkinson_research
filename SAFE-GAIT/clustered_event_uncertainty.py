"""Participant-clustered uncertainty for operational SAFE-GAIT event metrics.

Inputs are the per-participant dictionaries emitted by cross_dataset_events.py.
Never resample windows or use patient-level point estimates as independent events.
"""
import argparse
import json
from pathlib import Path
import numpy as np

FIELDS = ("reference_episodes", "event_tp", "event_fn", "event_fp",
          "alerts", "exposure_seconds", "windows", "abstained_windows")

def metrics(rows):
    totals = {key: sum(float(row[key]) for row in rows) for key in FIELDS}
    if totals["event_tp"] + totals["event_fn"] != totals["reference_episodes"]:
        raise ValueError("Event accounting inconsistent")
    if totals["event_tp"] + totals["event_fp"] != totals["alerts"]:
        raise ValueError("Alert accounting inconsistent")
    if totals["abstained_windows"] > totals["windows"]:
        raise ValueError("Abstentions exceed window count")
    return {
        "event_recall": totals["event_tp"] / totals["reference_episodes"]
            if totals["reference_episodes"] else None,
        "false_alerts_per_hour": 3600 * totals["event_fp"] / totals["exposure_seconds"]
            if totals["exposure_seconds"] else None,
        "abstention_fraction": totals["abstained_windows"] / totals["windows"]
            if totals["windows"] else None,
        "totals": totals,
    }

def summarize_subjects(by_subject, replicates=2000, seed=2026):
    if replicates < 1 or not by_subject:
        raise ValueError("Nonempty subjects and positive replicates required")
    subjects = sorted(by_subject)
    rows = [by_subject[k] for k in subjects]
    estimate = metrics(rows)
    rng = np.random.default_rng(seed)
    draws = {key: [] for key in ("event_recall", "false_alerts_per_hour",
                                "abstention_fraction")}
    for _ in range(replicates):
        sample = [rows[i] for i in rng.integers(0, len(rows), len(rows))]
        res = metrics(sample)
        for key in draws:
            if res[key] is not None and np.isfinite(res[key]):
                draws[key].append(float(res[key]))
    ci = {}
    for key, vals in draws.items():
        ci[key] = {
            "lower": float(np.quantile(vals, 0.025)) if vals else None,
            "upper": float(np.quantile(vals, 0.975)) if vals else None,
            "evaluable_replicates": len(vals),
            "requested_replicates": replicates,
        }
    return {"participants": len(subjects), "point": estimate, "bootstrap_95_percentile": ci,
            "seed": seed, "status": "exploratory participant-clustered interval; not clinical validation"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--event-results", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--replicates", type=int, default=2000)
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()
    report = json.loads(args.event_results.read_text())
    output = {policy: summarize_subjects(result["by_subject"], args.replicates, args.seed)
              for policy, result in report["policies"].items()}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"source_file": str(args.event_results),
                                     "policies": output}, indent=2))

if __name__ == "__main__":
    main()
