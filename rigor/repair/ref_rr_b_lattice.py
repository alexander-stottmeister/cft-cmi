"""REF-RR-B: independent parse of numerics/lattice/petz_lattice.out sections [2], [3], [6], [8].
Run from the cft_cmi root:  ${PYTHON:-python3} rigor/repair/ref_rr_b_lattice.py > rigor/repair/ref_rr_b_lattice.out
Tolerance (fixed before the run): a quoted number agrees if it equals the file value rounded to the quoted digits."""
import os, re, statistics
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
L = open(os.path.join(root, 'numerics/lattice/petz_lattice.out')).read().splitlines()
sec = None; lam = None; rows2 = []; fixed = {}; Lcur = None; lam6 = None
for ln in L:
    m = re.match(r'^\[(\d)\]', ln)
    if m: sec = int(m.group(1)); continue
    if sec == 2:
        m = re.match(r'\s+lambda = ([\d.]+)', ln)
        if m: lam = float(m.group(1)); continue
        t = ln.split()
        if len(t) >= 9 and re.match(r'^[\d.]+$', t[0]):
            rows2.append((lam, float(t[0]), int(t[1]), float(t[8]), ln.rstrip().endswith('*')))
    if sec == 6:
        m = re.match(r'\s+L_A=L_C=(\d+)', ln)
        if m: Lcur = int(m.group(1)); continue
        t = ln.split()
        if len(t) == 8 and re.match(r'^[\d.]+$', t[0]):
            fixed.setdefault((Lcur, float(t[0])), []).append((float(t[1]), float(t[5])))
print('[2] rows parsed:', len(rows2), ' lambdas:', sorted(set(r[0] for r in rows2)))
l0 = [r[3] for r in rows2 if r[0] == 0.0]
print('  lambda=0 single-branch factor: min %.4f max %.4f' % (min(l0), max(l0)))
pos = [r for r in rows2 if r[0] > 0]
mn = min(pos, key=lambda r: r[3]); mx = max(pos, key=lambda r: r[3])
print('  lambda>0 all rows: min %.4f at lam=%.1f eta=%.5f star=%s; max %.1f at lam=%.1f eta=%.5f' % (mn[3], mn[0], mn[1], mn[4], mx[3], mx[0], mx[1]))
uns = [r for r in pos if not r[4]]
mu = min(uns, key=lambda r: r[3])
print('  lambda>0 unstarred rows (large branch in range): min %.4f at lam=%.1f eta=%.5f (n=%d rows)' % (mu[3], mu[0], mu[1], len(uns)))
print('  rows with factor < 4.0:', [(r[0], r[1], r[3], r[4]) for r in pos if r[3] < 4.0])
for lm in sorted(set(r[0] for r in pos)):
    rr = [r for r in pos if r[0] == lm]
    print('   lam=%.1f: n=%d min %.4f max %.1f unstarred-min %s' % (lm, len(rr), min(r[3] for r in rr), max(r[3] for r in rr),
          ('%.4f' % min(r[3] for r in rr if not r[4])) if any(not r[4] for r in rr) else 'none'))
print('[6] fixed-L ratios:')
for (Lv, lm), v in sorted(fixed.items()):
    small = [x[1] for x in v if x[0] <= 0.05]; big = [x for x in v if x[0] > 0.05]
    print('  L=%d lam=%.1f: eta<=0.05: n=%d ratio %.4f..%.4f mean %.5f a=L(1-mean)=%.4f | eta>0.05: %s' % (Lv, lm, len(small), min(small), max(small),
          statistics.mean(small), Lv * (1 - statistics.mean(small)), ', '.join('%.3f@%.3f' % (x[1], x[0]) for x in big)))
