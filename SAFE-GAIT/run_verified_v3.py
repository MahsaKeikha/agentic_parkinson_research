"""Fail-closed orchestrator for exploratory full-release FoG-STAR analysis.

Never claims independent validation. Data bytes, manifest, and explicit time
units are required. The current classifiers assume timestamps in seconds.
"""
import argparse
import json
import hashlib
import platform
import subprocess
import sys
from pathlib import Path

from provenance_audit import audit

def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(part)
    return digest.hexdigest()

def write_manifest(path, record):
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

OUTPUT_MAP = {
    "cross_dataset.py": "cross_dataset_shift.json",
    "cross_dataset_invariant.py": "cross_dataset_invariant.json",
    "cross_dataset_events.py": "cross_dataset_events.json",
}

def require_clean_outputs(out_dir, pipeline):
    stale = [str(out_dir / OUTPUT_MAP[name]) for name in pipeline
             if (out_dir / OUTPUT_MAP[name]).exists()]
    if stale:
        raise FileExistsError("Refusing to reuse results from a previous run: " + ", ".join(stale))

def plan(report, *, timestamp_unit, source_dir):
    if report.get("status") != "PASS":
        raise ValueError("Manifest audit must PASS before experiments")
    if timestamp_unit not in ("s", "ms"):
        raise ValueError("Explicit timestamp unit required")
    if not source_dir.is_dir() or not list(source_dir.glob("S??R??.txt")):
        raise FileNotFoundError("Verified Daphnet source recordings required")
    groups=report.get("groups",[])
    medians=[g.get("median_positive_time_step") for g in groups if g.get("median_positive_time_step") is not None]
    scale = 0.001 if timestamp_unit == "ms" else 1.0
    if not medians or not all(0.01 <= x * scale <= 0.025 for x in medians):
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
    require_clean_outputs(args.out, pipeline)
    record={"status":"running", "claim_scope":"exploratory_posthoc_full_v3_reanalysis_not_independent",
            "python":sys.version, "platform":platform.platform(),
            "sensor_sha256":file_sha256(args.sensor_data),
            "clinical_sha256":file_sha256(args.clinical_data),
            "manifest_sha256":file_sha256(args.manifest),
            "dataset_verified":"manifest_check.json", "scripts":pipeline,
            "results":[], "failure":None}
    record_path=args.out/"experiment_run_manifest.json"
    write_manifest(record_path,record)
    for script in pipeline:
        command=[sys.executable,str(Path(__file__).with_name(script)),
                 "--daphnet-dir",str(args.daphnet_dir.resolve()),
                 "--fogstar-sensor-data",str(args.sensor_data.resolve()),
                 "--out",str(args.out.resolve())]
        command.extend(["--timestamp-unit", args.timestamp_unit])
        step={"script":script, "command":command, "status":"running"}
        record["results"].append(step)
        write_manifest(record_path,record)
        try:
            subprocess.run(command,check=True)
        except subprocess.CalledProcessError as exc:
            step["status"]="failed"
            step["returncode"]=exc.returncode
            record["failure"]=script
            record["status"]="failed"
            write_manifest(record_path,record)
            raise
        expected=OUTPUT_MAP[script]
        output=args.out/expected
        if not output.is_file():
            step["status"]="failed"
            record["failure"]=f"{script} produced no {expected}"
            record["status"]="failed"
            write_manifest(record_path,record)
            raise RuntimeError(record["failure"])
        step.update({"status":"completed", "output":expected,
                     "output_sha256":file_sha256(output)})
        write_manifest(record_path,record)
    record["status"]="completed_exploratory"
    write_manifest(record_path,record)
    print("Exploratory analysis completed; do not treat results as independent validation.")
if __name__=="__main__":
    main()
