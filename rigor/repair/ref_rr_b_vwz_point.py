"""REF-RR-B: one small raw lattice point of the VWZ sweep (e020, m=2: a=2, b=4, n=12), recomputed with the
script's own gauss() and compared with the saved line of numerics/networks/vwz_C.raw (tolerance 1e-12 relative).
Run from the cft_cmi root: ${PYTHON:-python3} rigor/repair/ref_rr_b_vwz_point.py > rigor/repair/ref_rr_b_vwz_point.out"""
import os, sys, time
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(root, 'numerics', 'networks'))
import lattice_chain as lc
saved = {}
for ln in open(os.path.join(root, 'numerics/networks/vwz_C.raw')):
    if ln.startswith('DATA set=e020') and ' m=2 ' in ln:
        d = dict(kv.split('=') for kv in ln.split()[1:]); saved[d['prot']] = float(d['mlogF'])
L = (2, 4, 4, 2); vac = None; T = time.time(); res = {}
for pr in ('1A', '2', '3LR'):
    mF, D, nrm, un, vac = lc.gauss(L, pr, 0.0, vac=vac); res[pr] = float(mF)
    print('prot=%s mlogF=%.15e saved=%s rel=%.1e' % (pr, res[pr], saved.get(pr), abs(res[pr] / saved[pr] - 1) if pr in saved else float('nan')))
print('order Phi1<Phi2<Phi3:', res['1A'] < res['2'] < res['3LR'], ' wall %.1f s' % (time.time() - T))
