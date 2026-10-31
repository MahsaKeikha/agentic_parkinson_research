"""Offline preflight for the SAFE-GAIT ACM manuscript; no external dependencies."""
import argparse
import re
from pathlib import Path

CITE = re.compile(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}")
BIB = re.compile(r"@\w+\s*\{\s*([^,]+),")
PLACEHOLDER = re.compile(r"\band others\b|verify|placeholder|to be confirmed|complete author", re.I)

def validate(tex, bib, strict=False):
    cited = {k.strip() for group in CITE.findall(tex) for k in group.split(",")}
    keys = BIB.findall(bib)
    known = set(keys)
    warnings = []
    errors = []
    if len(known) != len(keys):
        errors.append("Duplicate BibTeX keys")
    missing = sorted(cited-known)
    if missing:
        errors.append("Citations absent from bibliography: " + ", ".join(missing))
    unused = sorted(known-cited)
    if unused:
        warnings.append("Unused bibliography keys: " + ", ".join(unused))
    placeholders = [k for k in keys if PLACEHOLDER.search(
        bib.split("{" + k + ",",1)[1].split("\n}",1)[0] if "{"+k+"," in bib else "")]
    if placeholders:
        warnings.append("Bibliography metadata needs verification: " + ", ".join(placeholders))
    if len(known) < 30:
        warnings.append(f"Only {len(known)} bibliography entries; target >=30 verified and relevant works")
    if "nine-participant" in tex and "v3" not in tex.lower():
        errors.append("Historical subset lacks v3 provenance warning")
    if strict and warnings:
        errors.extend(warnings)
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "cited_keys": sorted(cited), "bibliography_keys": sorted(known)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--tex",type=Path,default=Path("paper/main.tex"))
    p.add_argument("--bib",type=Path,default=Path("paper/references.bib"))
    p.add_argument("--strict",action="store_true")
    args=p.parse_args()
    r=validate(args.tex.read_text(),args.bib.read_text(),args.strict)
    for msg in r["errors"]:
        print("ERROR:",msg)
    for msg in r["warnings"]:
        print("WARNING:",msg)
    print("PASS" if r["ok"] else "FAIL")
    raise SystemExit(0 if r["ok"] else 2)
if __name__=="__main__":
    main()
