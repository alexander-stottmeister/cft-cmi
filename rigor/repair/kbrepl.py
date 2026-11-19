#!/usr/bin/env python3
"""ORCHESTRATOR ONLY. Exact-replacement edits of card sections through `kb set` (never the card file).
JSON list of {"id", "key": statement|verify|title|next, "old", "new"}; `old` must occur once in that section/field.
  python3 rigor/repair/kbrepl.py CHANGES.json [--apply]
"""
import glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
KB = os.path.join(ROOT, "kb", "bin", "kb")
HEAD = {"statement": "## Statement", "verify": "## How to verify"}

def get(cid, key):
    fs = glob.glob(os.path.join(ROOT, "kb", "projects", "cft_cmi", "*", cid + ".md"))
    assert len(fs) == 1, (cid, fs)
    t = open(fs[0], encoding="utf-8").read()
    if key in HEAD:
        m = re.search(re.escape(HEAD[key]) + r"\n(.*?)(?=\n## |\Z)", t, re.S)
        return m.group(1).strip()
    m = re.search(rf"^{key}: (.*)$", t, re.M)
    return m.group(1)

items = json.load(open(sys.argv[1])); cur = {}; bad = 0
for n, it in enumerate(items):
    k = (it["id"], it["key"])
    if k not in cur: cur[k] = get(*k)
    c = cur[k].count(it["old"])
    if c != 1:
        print(f"item {n} {k}: old occurs {c} times: {it['old'][:60]!r}"); bad += 1; continue
    cur[k] = cur[k].replace(it["old"], it["new"])
print(len(items), "items,", bad, "problems")
if bad: sys.exit(1)
if "--apply" in sys.argv:
    env = dict(os.environ, KB_ACTOR="orchestrator")
    for (cid, key), text in cur.items():
        r = subprocess.run([KB, "-p", "cft_cmi", "set", cid, f"{key}={text}"], env=env, capture_output=True, text=True)
        print(cid, key, r.returncode, (r.stdout + r.stderr).strip()[:150])
