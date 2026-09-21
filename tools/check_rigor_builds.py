#!/usr/bin/env python3
"""Compile every rigor document and compare the set of failures with a baseline.

A permanently red build teaches people to ignore the build, so this is a ratchet:
it fails when a document that used to build stops, and also when a document on the
known-broken list starts building, which means the list is stale.  The list is
empty as of 21 September 2026, when the last two failures were repaired, so any
failure now is a regression.  Note that --update rewrites the baseline without
argument: it is for recording a deliberate change, and the commit should say why.

    tools/check_rigor_builds.py            compile and compare with the baseline
    tools/check_rigor_builds.py --update   rewrite the baseline (say why in the commit)
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RIGOR = ROOT / "rigor"
BASELINE = RIGOR / "known_build_failures.json"
SKIP = {"rigor_preamble.tex", "findings_entries.tex"}   # fragments, not documents


def is_document(path: Path) -> bool:
    if path.name in SKIP:
        return False
    head = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    return "\\documentclass" in head


def compile_one(tex: Path) -> tuple:
    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name]
    # pdflatex emits whatever bytes the fonts and sources contain, so decode
    # defensively rather than assuming UTF-8
    r = subprocess.run(cmd, cwd=RIGOR, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode == 0:
        return True, ""
    m = re.search(r"^! (.+)$", r.stdout, re.M)
    line = re.search(r"^l\.(\d+)", r.stdout, re.M)
    why = (m.group(1).strip() if m else "compilation failed")
    if line:
        why += " (line %s)" % line.group(1)
    return False, why


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--update", action="store_true", help="rewrite the baseline")
    ap.add_argument("--only", help="compile one document, for a quick check")
    args = ap.parse_args()

    docs = sorted(p for p in RIGOR.glob("*.tex") if is_document(p))
    if args.only:
        docs = [p for p in docs if p.name == args.only or p.stem == args.only]
    failures = {}
    for tex in docs:
        ok, why = compile_one(tex)
        if not ok:
            failures[tex.name] = why
        print("  %-52s %s" % (tex.name, "ok" if ok else "FAILS: " + why))

    if args.update:
        BASELINE.write_text(json.dumps(failures, indent=2, sort_keys=True) + "\n")
        print("\nbaseline rewritten: %d known failure(s)" % len(failures))
        return 0

    known = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    new = sorted(set(failures) - set(known))
    fixed = sorted(set(known) - set(failures))
    print("\n%d document(s), %d failing, %d known" % (len(docs), len(failures), len(known)))
    for name in new:
        print("  REGRESSION %s: %s" % (name, failures[name]))
    for name in fixed:
        print("  NOW BUILDS  %s: remove it from %s" % (name, BASELINE.name))
    if new or fixed:
        print("\nRun tools/check_rigor_builds.py --update once the change is intended.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
