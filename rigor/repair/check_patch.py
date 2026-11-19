#!/usr/bin/env python3
"""Exact-replacement patches for the repair round of 2026-11-19.

A patch file is JSON: a list of {"file": path relative to the repository root, "old": str, "new": str,
"finding": council locator, "reason": one sentence}.  Each "old" must occur exactly once in its file
(after the earlier items of the same patch file have been applied to that file).

  python3 rigor/repair/check_patch.py PATCH.json                 check only (exit 1 on any miss)
  python3 rigor/repair/check_patch.py PATCH.json --sibling TAG   also write DIR/_stage_TAG_NAME next to each file
  python3 rigor/repair/check_patch.py PATCH.json --stage DIR     also copy each patched file's directory (top level
                                                                 files only) to DIR/<dirname>/ with the patches applied
  python3 rigor/repair/check_patch.py PATCH.json --apply         ORCHESTRATOR ONLY: write the patched files in place
"""
import json, os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    items = json.load(open(a[0]))
    texts, bad = {}, 0
    for n, it in enumerate(items):
        for k in ("file", "old", "new", "finding", "reason"):
            if k not in it:
                print(f"item {n}: missing key {k}"); bad += 1
        f = it["file"]
        if f not in texts:
            texts[f] = open(os.path.join(ROOT, f), encoding="utf-8").read()
        c = texts[f].count(it["old"])
        if c != 1:
            print(f"item {n}: {f}: 'old' occurs {c} times: {it['old'][:70]!r}"); bad += 1
            continue
        texts[f] = texts[f].replace(it["old"], it["new"])
    print(f"{len(items)} items, {len(texts)} files, {bad} problems")
    if bad:
        sys.exit(1)
    if "--sibling" in a:
        tag = a[a.index("--sibling") + 1]
        for f, t in texts.items():
            p = os.path.join(ROOT, os.path.dirname(f), f"_stage_{tag}_{os.path.basename(f)}")
            open(p, "w", encoding="utf-8").write(t); print("wrote", p)
    if "--stage" in a:
        d = a[a.index("--stage") + 1]
        for sub in sorted({os.path.dirname(f) for f in texts}):
            dst = os.path.join(d, sub or "root"); os.makedirs(dst, exist_ok=True)
            src = os.path.join(ROOT, sub)
            for name in os.listdir(src):
                if os.path.isfile(os.path.join(src, name)):
                    shutil.copy2(os.path.join(src, name), os.path.join(dst, name))
        for f, t in texts.items():
            p = os.path.join(d, os.path.dirname(f) or "root", os.path.basename(f))
            open(p, "w", encoding="utf-8").write(t); print("staged", p)
    if "--apply" in a:
        for f, t in texts.items():
            open(os.path.join(ROOT, f), "w", encoding="utf-8").write(t); print("applied", f)

if __name__ == "__main__":
    main()
