"""REF-RR-B: card vwz-protocol-ordering. (A) parse numerics/networks/N3.out: per eta block R21, R31/P31, ordering of the
raw rows; (B) recompute the closed-form second-order ratio Phi(2)/Phi(1) and S = Ghat(log 1/eta)/Ghat(0) independently
with mpmath from Ghat(D) = (1/(12 pi^2))[cosh(D/2) - sinh^2(D/2) log coth(|D|/4)], plus the bracket of cor:W3W4(i).
Run from the cft_cmi root: ${PYTHON:-python3} rigor/repair/ref_rr_b_vwz.py > rigor/repair/ref_rr_b_vwz.out
Tolerances fixed before the run: closed form vs N3.out printed S to 5e-6 (printed digits); ordering exact."""
import os, re, mpmath as mp
mp.mp.dps = 40
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
txt = open(os.path.join(root, 'numerics/networks/N3.out')).read().splitlines()
blocks = []; cur = None
for ln in txt:
    m = re.match(r'^(\w+) eta=([\d.]+) \(a,b\)=\((\d+),(\d+)\)', ln)
    if m: cur = dict(tag=m.group(1), eta=float(m.group(2)), a=int(m.group(3)), b=int(m.group(4)), rows=[]); blocks.append(cur); continue
    if cur is None: continue
    t = ln.split()
    if len(t) >= 9 and t[0].isdigit() and t[1].isdigit():
        cur['rows'].append((int(t[1]), float(t[2]), float(t[3]), float(t[4])))
    m = re.match(r'\s+R21 normalised fit.*: ([\d.]+) \+- ([\d.e+-]+)', ln)
    if m: cur['R21'] = (float(m.group(1)), float(m.group(2)))
    m = re.match(r'\s+R31_inf/P31 = ([\d.]+) \+- ([\d.e+-]+)', ln)
    if m: cur['R31P31'] = (float(m.group(1)), float(m.group(2)))
nrows = 0; ordok = True
print('(A) N3.out blocks')
for B in blocks:
    for (n, p1, p2, p3) in B['rows']:
        nrows += 1; ordok &= (p1 < p2 < p3)
    print('  %-6s eta=%.4f a/b=%d/%d rows=%d R21=%s R31/P31=%s' % (B['tag'], B['eta'], B['a'], B['b'], len(B['rows']), B.get('R21'), B.get('R31P31')))
r21 = [B['R21'][0] for B in blocks if 'R21' in B]; dev = [abs(B['R31P31'][0] - 1) for B in blocks if 'R31P31' in B]
print('  total rows %d, Phi1<Phi2<Phi3 in all: %s' % (nrows, ordok))
print('  R21 range %.4f .. %.4f;  max |R31/P31 - 1| = %.4f %%' % (min(r21), max(r21), 100 * max(dev)))
print('  max |R31/P31 - 1| + its fit spread = %.4f %%' % (100 * max(abs(B['R31P31'][0] - 1) + B['R31P31'][1] for B in blocks if 'R31P31' in B)))
def G(D):
    D = mp.mpf(D)
    if D == 0: return 1 / (12 * mp.pi**2)
    return (mp.cosh(D / 2) - mp.sinh(D / 2)**2 * mp.log(mp.coth(abs(D) / 4))) / (12 * mp.pi**2)
G0 = G(0); G0lim = G(mp.mpf('1e-30'))
print('(B) closed form: Ghat(0) = %s, Ghat(1e-30) = %s, 1/(12 pi^2) = %s' % (mp.nstr(G0, 12), mp.nstr(G0lim, 12), mp.nstr(1/(12*mp.pi**2), 12)))
for eta in ['0.05', '0.2', '0.01', '1e-4']:
    e = mp.mpf(eta); a = e; b = (1 - e) / 2   # eta = a/(a+2b) with a+2b = 1
    z1 = a / b; z2 = a * (a + 2 * b) / (2 * b * (a + b)); z3 = a / b
    S = G(mp.log(1 / e)) / G0
    ratio = (z2**2 + z3**2) / z1**2 + 2 * z2 * z3 / z1**2 * S
    lo, hi = mp.sqrt(e) * (4 - e) / 3, 4 * mp.sqrt(e) / 3
    mid = (z2 + z3)**2 / z1**2
    print('  eta=%s: z1=%s z2=%s S=%s bracket[%s,%s] in=%s ratio2=%s  (z2+z3)^2/z1^2=%s  4 (Phi3/Phi1)  ratio2<=mid<4: %s' % (
        eta, mp.nstr(z1, 8), mp.nstr(z2, 8), mp.nstr(S, 8), mp.nstr(lo, 8), mp.nstr(hi, 8), lo <= S <= hi,
        mp.nstr(ratio, 8), mp.nstr(mid, 8), ratio <= mid < 4))
print('  S at log(1/0.05) vs N3.out S=0.29514: %s' % mp.nstr(G(mp.log(20)) / G0, 8))
print('  min of Ghat on a grid D in [0, 40]: %s (positivity check)' % mp.nstr(min(G(mp.mpf(k) / 10) for k in range(0, 401)), 6))
