"""Fail-closed orchestrator for exploratory full-release FoG-STAR analysis.

Never claims independent validation. Data bytes, manifest, and explicit time
units are required. The current classifiers assume timestamps in seconds.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from provenance_audit import audit

def plan(report, *, timestamp_unit, source_dir):
    if report.get("status") != "PASS":
        raise ValueError("Manifest audit must PASS before experiments")
    if timestamp_unit != "s":
        raise ValueError("Existing model parsers assume seconds; convert timestamps in a documented, separately checked preprocessing step")
    if not source_dir.is_dir() or not list(source_dir.glob("S??R??.txt")):
        raise FileNotFoundError("Verified Daphnet source recordings required")
    groups=report.get("groups",[])
    medians=[g.get("median_positive_time_step") for g in groups if g.get("median_positive_time_step") is not None]
    if not medians or not all(0.01 <= x <= 0.025 for x in medians):
        raise ValueError("Sensor timestamps inconsistent with nominal 60 Hz in seconds")
    return [
        "cross_dataset.py",
        "cross_dataset_invariant.py",
        "cross_dataset_events.py"
    ]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--sensor-data",type=Path,required=True)
    p.add_argument("--clinical-data",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--daphnet-dir",type=Path,required=True)
    p.add_argument("--timestamp-unit",choices=["s","ms"],required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    if not args.sensor_data.is_file() or not args.clinical_data.is_file() or not args.manifest.is_file():
        p.error("Official local files and independent manifest are required")
    report=audit(args.sensor_data,args.clinical_data,json.loads(args.manifest.read_text()))
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"manifest_check.json").write_text(json.dumps(report,indent=2))
    if report["status"] != "PASS":
        raise SystemExit("STOP: provenance did not PASS. No experiments run.")
    pipeline=plan(report,timestamp_unit=args.timestamp_unit,source_dir=args.daphnet_dir)
    manifest={"status":"exploratory_posthoc_full_v3_reanalysis_not_independent",
              "dataset_verified":"manifest_check.json",
              "scripts":pipeline,"results":[]}
    for script in pipeline:
        command=[sys.executable,str(Path(__file__).with_name(script)),
                 "--daphnet-dir",str(args.daphnet_dir.resolve()),
                 "--fogstar-sensor-data",str(args.sensor_data.resolve()),
                 "--out",str(args.out.resolve())]
        subprocess.run(command,check=True)
        manifest["results"].append(script)
    (args.out/"experiment_run_manifest.json").write_text(json.dumps(manifest,indent=2))
    print("Exploratory analysis completed; do not treat results as independent validation.")
if __name__=="__main__":
    main()
