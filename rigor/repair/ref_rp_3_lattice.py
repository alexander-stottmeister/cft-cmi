"""REF-RP-3: recompute from numerics/lattice/petz_lattice.out the card numbers of two-branch-law-lattice:
single-branch factor range (sections [2] and [6], lambda > 0), ratio at lambda = 0, L(1 - ratio) of [8].
Run: ${PYTHON:-python3} rigor/repair/ref_rp_3_lattice.py > rigor/repair/ref_rp_3_lattice.out"""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
lines = open(os.path.join(ROOT, 'numerics/lattice/petz_lattice.out')).read().split('\n')
sec = None; lam = None; r2 = {}; r6 = {}
for ln in lines:
    m = re.match(r'^\[(\d)\]', ln)
    if m: sec = int(m.group(1)); continue
    if sec == 2:
        m = re.match(r'\s*lambda = ([\d.]+)', ln)
        if m: lam = float(m.group(1)); continue
        t = ln.split()
        if len(t) >= 9 and re.match(r'^[\d.]+$', t[0]):
            r2.setdefault(lam, []).append(float(t[8]))
    if sec == 6:
        t = ln.split()
        if len(t) == 8 and re.match(r'^[\d.]+$', t[0]):
            r6.setdefault(float(t[0]), []).append(float(t[7]))
for nm, d in [('[2]', r2), ('[6]', r6)]:
    for l in sorted(d): print(f"{nm} lambda={l}: single-branch factor min {min(d[l]):.4g} max {max(d[l]):.4g} (n={len(d[l])})")
allpos = [x for d in (r2, r6) for l in d if l > 0 for x in d[l]]
print("lambda>0, both sections: min %.4g  max %.4g" % (min(allpos), max(allpos)))
print("lambda=0 [2]: all equal 2.0000:", all(abs(x-2) < 1e-4 for x in r2.get(0.0, [])))
