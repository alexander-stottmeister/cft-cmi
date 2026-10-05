#!/usr/bin/env python3
"""corner_kernel.py -- Phase 6 track G3: the corner kernel Ghat(Delta) in two independent frames.

Quantity: R(Delta) := Ghat(Delta)/Ghat(0), G(Delta) = g_Q(delta_0, delta_Delta), the real bilinear form of
  g_Q(delta) = (1/4) sum_ij |delta_ij|^2 / (w_i(1-w_j) + w_j(1-w_i))   (eigenbasis of Q),
delta_Delta = y-translate by Delta of the first-order corner defect.
Grid (fixed in rigor/phase6_g3_brief.md): Delta in {0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8}; two-frame tolerance 1e-3.

Frames:  T0 (modular, I = (-inf,1), y = -log(1-x), ddot of f3_t0.py)  and  box (xi = log((x+a)/(L-x)), defect_matrix.py).
Usage:  $PYTHON numerics/networks/corner_kernel.py TASK, TASK in K0 (validation), K1, K1b, K1fit (T0 frame), K2, K2b,
        K2fit (box frame), K3 (comparison, decay, sign), K4, K4b, K4v (finite zeta); outputs kernel_*.out/.npz beside this
        file. Order: K0; K1, K1b, K1fit; K2, K2b, K2fit; K3; K4v, K4, K4b. Results: numerics/networks/KERNEL_RESULTS.md.
Imports f3_t0, kkt_continuum, f3_gal, defect_matrix, compression_box via sys.path; never edits them.
"""
import os, sys, time
sys.dont_write_bytecode = True                         # no __pycache__ beside the imported project modules
for _v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '4')                   # at most 4 cores (G2 runs in parallel)
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))          # project root cft_cmi/
for _d in (os.path.join(_ROOT, 'numerics'), os.path.join(_ROOT, 'numerics', 'optimality_all')):
    if _d not in sys.path:
        sys.path.insert(0, _d)

# ---------------------------------------------------------------- shared: constants, output, bilinear form g_Q
F2 = 1.0/(12*np.pi**2)                       # Ghat(0) = f2 = 1/(12 pi^2), c = 1 per chirality (card const-f2)
DGRID = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0)    # Delta grid, fixed in the brief before any run
TOL_FRAMES = 1e-3                            # two frames agree if |R_T0 - R_box| <= 1e-3 at each Delta (brief)
TOL_FIT = 1e-4                               # an h-fit is admissible if its residuals at the 3 finest h are <= 1e-4
TOL_BIL = 1e-12                              # K0(b): bilinear code at Delta = 0 vs g_Q, relative
TOL_POL = 1e-10                              # K2: polarised qfi_c2 vs direct bilinear sum, relative
T0_SYST = 3e-4                               # T0 h-extrapolation overshoot, calibrated on G0/f2 -> 1.00028 (limit 1,
                                             # Theorem A); added to the T0 fit half-spread (repair after REF-P6-5)

class Out:
    """Tee to numerics/networks/<name>; the header states resolution, resolved and cut-off modes, their weight."""
    def __init__(self, name, header):
        self.f = open(os.path.join(_HERE, name), 'w')
        self(f'# {name} -- written by numerics/networks/corner_kernel.py on {time.strftime("%Y-%m-%d %H:%M")}')
        for l in header.strip().splitlines():
            self('# ' + l.strip())
    def __call__(self, *a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); self.f.write(s + '\n'); self.f.flush()

def sld(Q):
    """Eigenvalues w, eigenvectors U of the symbol Q and the SLD denominators W_ij = w_i(1-w_j) + w_j(1-w_i)."""
    w, U = np.linalg.eigh(Q)
    return w, U, w[:, None]*(1 - w)[None, :] + w[None, :]*(1 - w)[:, None]

def to_eig(U, D):
    return U.conj().T @ D @ U

def bil(Nw, A, B):
    """Real bilinear form of g_Q(d) = (1/4) sum |d_ij|^2/W_ij: (1/4) Re sum conj(A_ij) B_ij/W_ij, A, B in Q's eigenbasis."""
    return 0.25*float(np.real(np.sum(np.conj(A)*B/Nw)))

# ---------------------------------------------------------------- T0 frame: I = (-inf, 1), y = -log(1-x), f3_t0.py
def t0_mesh(h, Y, Ymax):
    """f3_t0.mesh: uniform cells of width h on [-Y, Ymax] (nA = round(Y/h) cells left of the node y = 0)."""
    import f3_t0
    return f3_t0.mesh(h, Y, Ymax)

def t0_defect(e, Delta, ng=10):
    """delta_Delta(y1, y2) = ddot(y1 - Delta, y2 - Delta) in the cell basis e: f3_t0.ddot on the edges shifted so that
    the node y = Delta becomes the corner (the cell integrals are those of the translated kernel, the basis is unchanged)."""
    import f3_t0
    k = int(np.argmin(np.abs(e - Delta)))
    if abs(e[k] - Delta) > 1e-9:
        raise ValueError(f'Delta = {Delta} is not a node of the mesh')
    return f3_t0.ddot(e - e[k], k, ng)

# ---------------------------------------------------------------- K0 validation (before any production run)
def k0():
    import f3_t0, f3_gal, kkt_continuum as kc, defect_matrix as dm, compression_box as cb
    o = Out('kernel_validate.out', """K0 validation, brief rigor/phase6_g3_brief.md sec. 3; command: $PYTHON numerics/networks/corner_kernel.py K0
    (a) T0 frame (f3_t0.py: cell basis of y, kkt_continuum.Qmat exact, closed-form ddot, ng = 10): g_Q(ddot)/f2, Y = 6, Ymax = 20.
        Resolved: cell functions of width h on [-6, 20]; cut off: y < -6, y > 20 and all sub-cell structure; the weight of
        the cut-off modes is the deficit 1 - g/f2 (column g/f2). Reference: numerics/optimality_all/f3_t0_final.out.
    (b) bilinear code at Delta = 0 against f3_gal.theta's g0 on the same matrices (relative tolerance 1e-12).
    (c) box frame (defect_matrix.run 'first', a = 1, L = 2, s = 1, zeta = 1/3; compression_box.Q_box, qfi_c2):
        f2_box = c2/zeta^2. Resolved: box modes |kappa| <= kappa_max on the window |xi - xi0| <= Lam/2; cut off:
        |kappa| > kappa_max (weight f2 - f2_box ~ 0.0641/kappa_max^2, an unproved asymptotic) and |xi - xi0| > Lam/2.""")
    ref_a = {0.24: 0.91158, 0.12: 0.95454, 0.06: 0.97654, 0.03: 0.98699, 0.02: 0.99019}
    ok = True
    o('(a,b)  h      N    nA   g/f2 ours   F3 value  |diff|   g0 = f3_gal.theta(...)[1]   rel|bil-g0|   time')
    for h in (0.24, 0.12, 0.06, 0.03, 0.02):
        t = time.time(); e, nA = t0_mesh(h, 6.0, 20.0); Q = kc.Qmat(e); D = f3_t0.ddot(e, nA, 10)
        w, U, Nw = sld(Q); Dt = to_eig(U, D); g = bil(Nw, Dt, Dt)
        g0 = f3_gal.theta(Q, D, nA, iters=1)[1]
        pa = round(g/F2, 5) == ref_a[h]; pb = abs(g - g0)/g0 <= TOL_BIL; ok = ok and pa and pb
        o(f'      {h:5.3f} {len(Q):5d} {nA:4d}  {g/F2:.7f}  {ref_a[h]:.5f}  {abs(g/F2 - ref_a[h]):.1e}   {g0:.15e}  '
          f'{abs(g - g0)/g0:.1e}  {"PASS" if pa and pb else "FAIL"}  {time.time() - t:.0f}s')
    ref_c = {(60, 30): (0.0083698, 'numerics/results_batch3.txt:8 (0.00836978), numerics/line_so.txt:1'),
             (120, 45): (0.0084112, 'numerics/line_so.txt:4, rigor/check_note5_numerics.tex:677')}
    a, L, s = 1.0, 2.0, 1.0; zeta = a*s/(a + L)
    o('(c)  Lam kmax    N  kappa_max_eff  f2_box = c2/zeta^2   reference  |diff|   eig(Q_N): min, 1-max   source')
    for (Lam, km) in ((60, 30), (120, 45)):
        t = time.time(); Dh, kap = dm.run(a, L, s, Lam, km, 'first', ngl=12)
        Q = cb.Q_box(kap, Lam, xi0=np.log(a/L)); c2 = cb.qfi_c2(Q, Dh); ev = np.linalg.eigvalsh(Q)
        r, src = ref_c[(Lam, km)]; pc = round(c2/zeta**2, 7) == r
        if Lam == 60:
            ok = ok and pc                           # (120, 45): published value is line_so.py's LINE symbol, see (c')
        o(f'    {Lam:4d} {km:4d} {len(kap):4d}  {kap.max():7.2f}      {c2/zeta**2:.9f}   {r:.7f}  {abs(c2/zeta**2 - r):.1e}  '
          f'{ev.min():.2e}, {1 - ev.max():.2e}  {src}  {"PASS" if pc else "FAIL"}  {time.time() - t:.0f}s')
    o('    (120, 45) via compression_box.qfi_c2 in double precision: Q_N has eigenvalues ~ e^{-44.7} below machine epsilon,')
    o('    computed as negative -> W_ij <= 0 -> inf (code path not evaluable there); the published 0.0084112 is line_so.py.')
    ok = k0_box(o) and ok
    o(f'K0 overall (a), (b), (c) at (60,30), (c\') line symbol, (d), (e): {"PASS" if ok else "FAIL"}')
    return ok

# ---------------------------------------------------------------- K1 T0 frame: R(Delta) on h-ladders
H_DYADIC = (0.25, 0.125, 0.0625, 0.03125, 0.015625)   # every Delta of DGRID is a mesh node (see KERNEL_RESULTS.md K1)
H_BRIEF = (0.24, 0.12, 0.06, 0.03)                     # the brief's ladder: only Delta in {0, 3, 6} can be nodes

def t0_ladder(o, hs, Y, Ymax, Ds, ng=10):
    """G_h(Delta) = g_Q(delta_0, delta_Delta) on uniform meshes [-Y, Ymax] of width h; Deltas that are not nodes are
    skipped (an off-node corner would not be a translate of delta_0 on the mesh). Returns G0[h], G[h, Delta]."""
    import kkt_continuum as kc
    G = np.full((len(hs), len(Ds)), np.nan); G0 = np.zeros(len(hs))
    for ih, h in enumerate(hs):
        t = time.time(); e, nA = t0_mesh(h, Y, Ymax); Q = kc.Qmat(e); w, U, Nw = sld(Q)
        D0 = t0_defect(e, 0.0, ng); A0 = to_eig(U, D0); G0[ih] = bil(Nw, A0, A0); N = len(Q)
        o(f'  h = {h:.6f}  mesh [{e[0]:.3f}, {e[-1]:.3f}]  N = {N}  eig(Q) in [{w.min():.2e}, {w.max():.6f}]  '
          f'G0/f2 = {G0[ih]/F2:.7f}  (cut-off weight of the diagonal: 1 - G0/f2 = {1 - G0[ih]/F2:.2e})')
        for iD, D in enumerate(Ds):
            sh = int(round(D/h))
            if abs(D/h - sh) > 1e-9:
                continue
            DD = t0_defect(e, D, ng); B = to_eig(U, DD); g = bil(Nw, A0, B)
            pol = (bil(Nw, A0 + B, A0 + B) - bil(Nw, A0 - B, A0 - B))/4
            shift = np.abs(DD[sh:, sh:] - D0[:N - sh, :N - sh]).max()/np.abs(D0).max()
            G[ih, iD] = g
            o(f'     Delta = {D:3.1f}  R_h = G/G0 = {g/G0[ih]:+.8f}  G/f2 = {g/F2:+.8f}  |pol - bil|/G0 = '
              f'{abs(pol - g)/G0[ih]:.1e}  translate check {shift:.1e}  {time.time() - t:.0f}s')
    return G0, G

def k1():
    o = Out('kernel_t0.out', """K1, T0 frame (brief sec. 3); command: $PYTHON numerics/networks/corner_kernel.py K1 (background, ~30 min)
    Mesh: uniform cells of width h on [-Y, Ymax] (f3_t0.mesh), node at y = 0; Y = 14 >= Delta + 6, Ymax = 20 >= Delta + 10
    for every Delta <= 8 (the corner at Delta = 8 keeps 12 units of y on its D side); second Ymax = 24 at Delta = 0, 8.
    Q = kkt_continuum.Qmat (exact Galerkin), delta_Delta = corner_kernel.t0_defect (f3_t0.ddot, ng = 10, graded cells at
    the corner). Resolved: cell functions of width h on [-Y, Ymax]; cut off: sub-cell (UV) structure, y < -Y, y > Ymax.
    Weight of the cut-off modes: 1 - G0/f2 for the diagonal (printed per h); for Delta > 0 it is not separable and is
    removed by the extrapolation in h (kernel_t0_fits.out). |pol - bil| = polarisation identity check; 'translate check' =
    max|delta_Delta[i+s, j+s] - delta_0[i, j]|/max|delta_0| on the overlap (s = Delta/h), i.e. delta_Delta IS the translate.
    Ladders: dyadic h = 0.25 ... 0.015625 (all Delta are nodes); the brief's h = 0.24, 0.12, 0.06, 0.03 (Delta = 0, 3, 6).""")
    res = {}
    o('[A] dyadic ladder, Y = 14, Ymax = 20, all Delta'); res['A'] = t0_ladder(o, H_DYADIC, 14.0, 20.0, DGRID)
    o("[B] the brief's ladder, Y = 14, Ymax = 20, Delta = 0, 3, 6"); res['B'] = t0_ladder(o, H_BRIEF, 14.0, 20.0, (0.0, 3.0, 6.0))
    o('[C] dyadic ladder, Y = 14, Ymax = 24, Delta = 0, 8'); res['C'] = t0_ladder(o, H_DYADIC, 14.0, 24.0, (0.0, 8.0))
    np.savez(os.path.join(_HERE, 'kernel_t0.npz'), hA=H_DYADIC, DA=DGRID, G0A=res['A'][0], GA=res['A'][1],
             hB=H_BRIEF, DB=(0.0, 3.0, 6.0), G0B=res['B'][0], GB=res['B'][1], hC=H_DYADIC, DC=(0.0, 8.0),
             G0C=res['C'][0], GC=res['C'][1])
    o('saved numerics/networks/kernel_t0.npz')

def t0_ddot_fast(e, nA, ng=10, chunk=48):
    """f3_t0.ddot vectorised over the D side (same nodes kkt_continuum._nodes, graded cells nA-1, nA, same kernel
    f3_t0.kern); checked against f3_t0.ddot in K1b."""
    import f3_t0
    from kkt_continuum import _nodes
    N = len(e) - 1; al, be = e[:-1], e[1:]; hh = be - al
    nod, wei = [], []
    for m in range(N):
        g = 'right' if m == nA - 1 else ('left' if m == nA else None)
        n_, w_ = _nodes(al[m], be[m], ng, graded_at=g); nod.append(n_); wei.append(w_)
    Yd = np.concatenate(nod[nA:]); Wd = np.concatenate(wei[nA:]); starts = np.cumsum([0] + [len(x) for x in nod[nA:-1]])
    J = np.zeros((nA, N - nA))
    for m0 in range(0, nA, chunk):
        ms = range(m0, min(nA, m0 + chunk)); Xa = np.concatenate([nod[m] for m in ms]); Wa = np.concatenate([wei[m] for m in ms])
        Ka = (Wa[:, None]*f3_t0.kern(Xa[:, None], Yd[None, :]))*Wd[None, :]
        rows = np.add.reduceat(Ka, np.cumsum([0] + [len(nod[m]) for m in list(ms)[:-1]]), axis=0)
        J[m0:m0 + len(ms)] = np.add.reduceat(rows, starts, axis=1)
    J /= np.sqrt(hh[:nA])[:, None]; J /= np.sqrt(hh[nA:])[None, :]
    D = np.zeros((N, N), dtype=complex); D[:nA, nA:] = 1j/(2*np.pi)*J
    return D + D.conj().T

def k1b(hs=(0.125, 0.015625, 0.0078125), Y=14.0, Ymax=20.0):
    """h = 1/128 rung: delta_0 once on the extended mesh [-Y-8, Ymax] (t0_ddot_fast), delta_Delta = its translate restricted
    to [-Y, Ymax] (exact on a uniform mesh, K1 'translate check'); h = 0.125, 1/64 repeat K1 rungs as checks of this path."""
    import f3_t0, kkt_continuum as kc
    o = Out('kernel_t0b.out', """K1b, T0 frame, finer rung h = 1/128 (and K1 rungs 1/8, 1/64 recomputed by this path); command:
    $PYTHON numerics/networks/corner_kernel.py K1b (background). Same mesh [-14, 20], Q, kernel as K1 (kernel_t0.out header);
    delta_Delta = translate of delta_0 computed once on [-22, 20] by corner_kernel.t0_ddot_fast. Checks: t0_ddot_fast vs
    f3_t0.ddot at h = 1/8 (all Delta), and the K1 values at h = 1/8, 1/64.""")
    out = {}
    for h in hs:
        t = time.time(); eE, nE = t0_mesh(h, Y + 8.0, Ymax); DE = t0_ddot_fast(eE, nE); off = int(round(8.0/h))
        e, nA = t0_mesh(h, Y, Ymax); N = len(e) - 1; Q = kc.Qmat(e); w, U, Nw = sld(Q)
        o(f'  h = {h:.7f}  N = {N}  extended N = {len(eE) - 1}  eig(Q) in [{w.min():.2e}, {w.max():.6f}]  {time.time() - t:.0f}s')
        G = []
        for D in DGRID:
            s_ = int(round(D/h)); DD = DE[off - s_:off - s_ + N, off - s_:off - s_ + N]
            if h >= 0.125:
                ref = t0_defect(e, D); o(f'     check vs f3_t0.ddot, Delta = {D}: {np.abs(DD - ref).max()/np.abs(ref).max():.1e}')
            B = to_eig(U, DD)
            if D == 0:
                A0 = B
            G.append(bil(Nw, A0, B))
            o(f'     Delta = {D:3.1f}  R_h = {G[-1]/G[0]:+.8f}  G/f2 = {G[-1]/F2:+.8f}  {time.time() - t:.0f}s')
        out[h] = np.array(G)
    np.savez(os.path.join(_HERE, 'kernel_t0b.npz'), h=np.array(hs), D=DGRID, G=np.array([out[h] for h in hs]))

def hfits(hs, v, tol=TOL_FIT):
    """Fits in h (the measured convergence variable) on 4 consecutive rungs: 'lin' (1/L: v0 + c h), 'log' (log L:
    v0 + c log h, no finite limit), 'pow' (h^p: v0 + c h^p, p free on [0.1, 4]); windows '4f' = the 4 finest rungs and
    '4c' = the 4 rungs one step coarser. Admissible iff max |residual| at the 3 finest rungs <= tol (prediction
    for '4c'). Returns [(name, v0, p, maxres, admissible)]."""
    hs = np.asarray(hs, float); v = np.asarray(v, float); o_ = np.argsort(-hs); hs, v = hs[o_], v[o_]; out = []
    for win, sl in (('4f', slice(-4, None)), ('4c', slice(-5, -1))):
        if len(hs) < (4 if win == '4f' else 5):
            continue
        H, W = hs[sl], v[sl]
        for name in ('lin', 'log', 'pow'):
            best = None
            for p in (np.arange(0.1, 4.0001, 0.001) if name == 'pow' else (1.0,)):
                X = np.log(H) if name == 'log' else H**p
                M = np.vstack([np.ones_like(X), X]).T; c = np.linalg.lstsq(M, W, rcond=None)[0]
                Xf = np.log(hs[-3:]) if name == 'log' else hs[-3:]**p
                r = np.abs(v[-3:] - (c[0] + c[1]*Xf)).max(); rw = np.abs(W - M @ c).max()
                if best is None or rw < best[3]:
                    best = (c[0], p, r, rw)
            v0 = np.nan if name == 'log' else best[0]
            out.append((f'{name}-{win}', v0, best[1], best[2], best[2] <= tol))
    return out
# ---------------------------------------------------------------- box frame: I = (-a, L), xi = log((x+a)/(L-x)), defect_matrix.py
def box_kgrid(Lam, kmax):
    """defect_matrix.run's modes: k_j = 2 pi j/Lam, |j| <= M = floor(kmax Lam/(4 pi^2)); returns k and kappa = 2 pi k."""
    M = int(np.floor(kmax/(2*np.pi)*Lam/(2*np.pi))); k = 2*np.pi*np.arange(-M, M + 1)/Lam
    return k, 2*np.pi*k

def _panels(lo, hi, width, ngl):
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    ed = np.linspace(lo, hi, int(np.ceil((hi - lo)/width)) + 1)
    nod = ((ed[1:] + ed[:-1])/2)[:, None] + ((ed[1:] - ed[:-1])/2)[:, None]*xg[None, :]
    return nod.ravel(), (((ed[1:] - ed[:-1])/2)[:, None]*wg[None, :]).ravel()

def _pmesh(pmax, ngl):
    """defect_matrix.run's graded mesh in p = |xi - corner|: GL panels in log p on [1e-12, 0.2] (width 0.5), then
    GL panels of width 0.25 on [0.2, pmax]."""
    sig, wsig = _panels(np.log(1e-12), np.log(0.2), 0.5, ngl); p2, w2 = _panels(0.2, pmax, 0.25, ngl)
    return np.concatenate((np.exp(sig), p2)), np.concatenate((wsig*np.exp(sig), w2))

def box_corner(a, L, s, Lam, kmax, xic, kind='first', ngl=12, stable=True):
    """<e_j, D e_l> for the single-corner kernel of defect_matrix.py with corner x = 0 of the frame (a, L), i.e. at
    xi0 = log(a/L), integrated over the WINDOW [xic - Lam/2, xic + Lam/2] in the absolute basis e^{i k_j xi}/sqrt(Lam)
    (the basis of compression_box.Q_box(.., xi0=xic)). stable=False with xic = xi0 is defect_matrix.run (K0(d)); stable=True
    evaluates the same functions without cancellation (r = a/L): -x = a(1-e^{-p})/(1+r e^{-p}) on A (xi = xi0 - p),
    x = a(e^p - 1)/(1+r e^p) on D (xi = xi0 + p), beta_I = (a+L) r e^{-+p}/(1+r e^{-+p})^2; defect_matrix's L - x cancels
    for large p, which in a shifted frame (a', L') turns beta negative -> NaN (K0(d'))."""
    xi0 = np.log(a/L)
    x_of = lambda xi: (L*np.exp(xi) - a)/(1 + np.exp(xi))
    beta = lambda x: (x + a)*(L - x)/(a + L)
    if kind == 'exact':
        kern = lambda u, v: s*u*v/((u + v)*(L*(u + v) + s*u*v))
    else:
        kern = lambda u, v: (s/L)*u*v/(u + v)**2
    pA, wA = _pmesh(xi0 - (xic - Lam/2), ngl); pD, wD = _pmesh(xic + Lam/2 - xi0, ngl)
    if stable:
        r = a/L; eA = np.exp(-pA); eD = np.exp(pD)
        xA = -a*(-np.expm1(-pA))/(1 + r*eA); yD = a*np.expm1(pD)/(1 + r*eD)
        sa = np.sqrt((a + L)*r*eA/(1 + r*eA)**2)*wA; sd = np.sqrt((a + L)*r*eD/(1 + r*eD)**2)*wD
    else:
        xA = x_of(xi0 - pA); yD = x_of(xi0 + pD); sa = np.sqrt(beta(xA))*wA; sd = np.sqrt(beta(yD))*wD
    k, kap = box_kgrid(Lam, kmax)
    EA = np.exp(-1j*np.outer(k, xi0 - pA)); ED = np.exp(1j*np.outer(k, xi0 + pD))
    J = np.zeros((len(k), len(k)), dtype=complex); chunk = 1200
    for i0 in range(0, len(pA), chunk):
        Rm = kern(-xA[i0:i0 + chunk][:, None], yD[None, :])*sa[i0:i0 + chunk][:, None]*sd[None, :]
        J += EA[:, i0:i0 + chunk] @ (Rm @ ED.T)
    Dh = (1j/(2*np.pi))*J/Lam
    return Dh + Dh.conj().T, kap

def line_sld(kap):
    """SLD denominators of the LINE symbol q(kappa) = 1/(1+e^kappa) on the box modes (numerics/line_so.py), with q and
    1-q evaluated to full relative precision (no eigen-decomposition, no regulator)."""
    q = 1/(1 + np.exp(kap)); omq = 1/(1 + np.exp(-kap))
    return q[:, None]*omq[None, :] + q[None, :]*omq[:, None]

def p_of_Delta(a, L, Delta):
    """Position p' of the second corner with modular separation Delta from x = 0 in the frame of I = (-a, L):
    y_I(p') - y_I(0) = Delta with y_I(x) = log((x+a)/(L-x))  <=>  p' = a L (e^Delta - 1)/(L + a e^Delta)."""
    return a*L*np.expm1(Delta)/(L + a*np.exp(Delta))

def k0_box(o):
    """K0 (c') line symbol, (d) window code = defect_matrix.run, (e) p'(Delta), lem:field/lem:density, T0<->box kernel."""
    import f3_t0, defect_matrix as dm, compression_box as cb
    a, L, s = 1.0, 2.0, 1.0; zeta = a*s/(a + L); xi0 = np.log(a/L); ok = True
    o("(c') LINE symbol q(kappa_j) on the same box modes (numerics/line_so.py), and Q_box vs line where Q_box is resolved:")
    for (Lam, km, ref) in ((60, 30, 0.0083698), (120, 30, None), (120, 45, 0.0084112)):
        Dh, kap = dm.run(a, L, s, Lam, km, 'first', ngl=12); fl = bil(line_sld(kap), Dh, Dh)/zeta**2
        Q = cb.Q_box(kap, Lam, xi0=xi0); w, U, Nw = sld(Q)
        fb = bil(Nw, to_eig(U, Dh), to_eig(U, Dh))/zeta**2 if (w.min() > 0 and w.max() < 1) else float('nan')
        pc = True if ref is None else round(fl, 7) == ref; ok = ok and pc
        o(f'    (Lam, kmax) = ({Lam}, {km}): f2_line = {fl:.9f}  ref(line_so.txt) = {ref}  f2_box(Q_box) = {fb:.9f}  '
          f'|line - box| = {abs(fl - fb):.1e}  min eig Q_box = {w.min():.2e}  {"PASS" if pc else "FAIL"}')
    o('(d) box_corner(.., xic = xi0) against defect_matrix.run (same window, same graded mesh):')
    for (Lam, km) in ((60, 30), (120, 45)):
        D1, _ = dm.run(a, L, s, Lam, km, 'first', ngl=12); D2, _ = box_corner(a, L, s, Lam, km, xi0, stable=False)
        D3, _ = box_corner(a, L, s, Lam, km, xi0); r3 = np.abs(D1 - D3).max()/np.abs(D1).max()
        r = np.abs(D1 - D2).max()/np.abs(D1).max(); pd = r < 1e-13; ok = ok and pd
        o(f'    ({Lam}, {km}): max|diff|/max|D| = {r:.1e}  {"PASS" if pd else "FAIL"};  (d\') cancellation-free '
          f'formulas (production) vs defect_matrix.run: {r3:.1e}')
    o("(e) p'(Delta) = a L (e^Delta - 1)/(L + a e^Delta); second corner (a', L') = (a + p', L - p'), s' = zeta (a+L)/a' so that")
    o("    zeta' = sigma' beta_I(p') = (s'/L') (p'+a)(L-p')/(a+L) = zeta (lem:field, lem:density); kernels in half-density form:")
    import mpmath as mp
    mp.mp.dps = 30; rng = np.random.default_rng(1); worst = 0.0       # identities evaluated in 30-digit arithmetic
    def K(aa, LL, ss, y1, y2):                                          # sqrt(beta(x) beta(x')) R^(1)(-x, x'), frame (aa, LL)
        xo = lambda xi: (LL*mp.e**xi - aa)/(1 + mp.e**xi); be = lambda x: (x + aa)*(LL - x)/(aa + LL)
        x1, x2 = xo(y1), xo(y2); u, v = -x1, x2
        return mp.sqrt(be(x1)*be(x2))*(ss/LL)*u*v/(u + v)**2
    kT = lambda y1, y2: -mp.sinh(y1/2)*mp.sinh(y2/2)/mp.sinh((y1 - y2)/2)**2     # f3_t0.kern
    A, L_ = mp.mpf(a), mp.mpf(L); Z = A*mp.mpf(s)/(A + L_); X0 = mp.log(A/L_)
    for D in DGRID:
        Dm = mp.mpf(D); pp = A*L_*mp.expm1(Dm)/(L_ + A*mp.e**Dm); a2, L2 = A + pp, L_ - pp; s2 = Z*(A + L_)/a2
        dy = mp.log((pp + A)/(L_ - pp)) - X0 - Dm; dz = (s2/L2)*(pp + A)*(L_ - pp)/(A + L_) - Z
        e2 = e1 = mp.mpf(0)
        for _ in range(40):
            u1 = -mp.mpf(rng.uniform(0.01, 8)); u2 = mp.mpf(rng.uniform(0.01, 8))   # y - y_p on the A and the D side
            k1 = K(A, L_, mp.mpf(s), X0 + u1, X0 + u2); k2 = K(a2, L2, s2, X0 + Dm + u1, X0 + Dm + u2)
            e2 = max(e2, abs(k2/k1 - 1)); e1 = max(e1, abs(k1/(Z*kT(u1, u2)) - 1))
        worst = max(worst, float(max(abs(dy), abs(dz), e2, e1)))
        o(f"    Delta = {D:3.1f}: p' = {float(pp):.12f}  |y(p')-y(0)-Delta| = {float(abs(dy)):.1e}  |zeta'-zeta| = "
          f"{float(abs(dz)):.1e}  max|K2/K1 - 1| = {float(e2):.1e}  max|K1/(zeta kern_T0) - 1| = {float(e1):.1e}  (30 digits)")
    pe = worst < 1e-12; ok = ok and pe
    o(f'    (e): worst deviation {worst:.1e}  {"PASS" if pe else "FAIL"}')
    return ok
# ---------------------------------------------------------------- K2 box frame: two 'first' kernels in one box
BOXES = ((60, 30), (120, 30), (120, 45), (120, 60))   # brief: (60,30), (120,45), (120,60); + (120,30): kappa ladder at Lam = 120
EPS_WIN = (1e-13, 1e-12, 1e-11)                      # spectral window on Q_box where its eigenbasis is unresolved
BOXES2 = ((120, 75), (120, 90), (120, 105), (120, 120))   # extension of the kappa ladder (K2b): oscillating cut-off

def k2(boxes=BOXES, tag=''):
    import compression_box as cb
    o = Out(f'kernel_box{tag}.out', f"""K2{tag}, box frame (brief sec. 3); command: $PYTHON numerics/networks/corner_kernel.py K2{tag} (background)
    I = (-a, L) = (-1, 2), xi = log((x+a)/(L-x)); corner 1 at x = 0 (xi0 = log(1/2)), corner 2 at p'(Delta) (KERNEL_RESULTS.md
    (C3)), both 'first' kernels with zeta = 1/3, ONE window [xi0 - Lam/2, xi0 + Lam/2] (corner_kernel.box_corner, graded
    mesh of defect_matrix.py, ngl = 12). G(Delta) = g_Q(D1, D2)/zeta^2, R = G(Delta)/G(0).
    Resolved: box modes |kappa_j| <= kappa_max (kappa_j = 4 pi^2 j/Lam) on the window; cut off: |kappa| > kappa_max (weight of
    the diagonal f2 - G(0) printed per box; for Delta > 0 measured by the kappa_max ladder in kernel_box_fits.out) and
    |xi - xi0| > Lam/2 (corner 2 keeps Lam/2 - Delta on its D side; Lam = 60 vs 120 measures it).
    Symbols: [box] eigenbasis of Q_box (compression_box.Q_box), polarised qfi_c2 vs direct sum; where Q_box has eigenvalues
    below machine precision [box] is not evaluable and [win eps] drops the pairs with both eigenvalues < eps or both > 1 - eps
    (a regulator); [line] = q(kappa_j) = 1/(1+e^kappa_j) on the same modes (no eigen-decomposition, no regulator).""")
    a, L, s = 1.0, 2.0, 1.0; zeta = a*s/(a + L); xi0 = np.log(a/L); store = {}
    for (Lam, km) in boxes:
        t = time.time(); D1, kap = box_corner(a, L, s, Lam, km, xi0); Q = cb.Q_box(kap, Lam, xi0=xi0)
        w, U, Nw = sld(Q); resolved = bool(w.min() > 0 and w.max() < 1); Nl = line_sld(kap); A1 = to_eig(U, D1)
        wins = []
        for eps in EPS_WIN:
            m = ((w[:, None] < eps) & (w[None, :] < eps)) | (((1 - w)[:, None] < eps) & ((1 - w)[None, :] < eps))
            wins.append(np.where(m, np.inf, Nw))
            o(f'# ({Lam},{km}) window eps = {eps:.0e}: {int(m.sum())} pairs dropped, min kept W = {wins[-1][~m].min():.2e}')
        gl = np.zeros(len(DGRID)); gb = np.full(len(DGRID), np.nan); gw = np.zeros((len(EPS_WIN), len(DGRID)))
        o(f'({Lam}, {km}): N = {len(kap)}, kappa_max_eff = {kap.max():.2f}, eig(Q_box) in [{w.min():.2e}, 1 - {1 - w.max():.2e}]'
          f' -> [box] {"resolved" if resolved else "NOT resolved"}')
        for iD, D in enumerate(DGRID):
            pp = p_of_Delta(a, L, D); a2, L2 = a + pp, L - pp; s2 = zeta*(a + L)/a2
            D2 = D1 if D == 0 else box_corner(a2, L2, s2, Lam, km, xi0)[0]; A2 = to_eig(U, D2)
            gl[iD] = bil(Nl, D1, D2); pl = (bil(Nl, D1 + D2, D1 + D2) - bil(Nl, D1 - D2, D1 - D2))/4
            for ie in range(len(EPS_WIN)):
                gw[ie, iD] = bil(wins[ie], A1, A2)
            line = (f"   Delta = {D:3.1f}: [line] R = {gl[iD]/gl[0]:+.8f} G/f2 = {gl[iD]/zeta**2/F2:+.8f} (pol {abs(pl - gl[iD])/gl[0]:.0e})"
                    f"  [win] R = " + ' '.join(f'{gw[ie, iD]/gw[ie, 0]:+.8f}' for ie in range(len(EPS_WIN))))
            if resolved:
                gb[iD] = bil(Nw, A1, A2); pb = (cb.qfi_c2(Q, D1 + D2) - cb.qfi_c2(Q, D1 - D2))/4
                line += (f"  [box] R = {gb[iD]/gb[0]:+.8f} G/f2 = {gb[iD]/zeta**2/F2:+.8f} |polarised qfi_c2 - direct|/G0 = "
                         f"{abs(pb - gb[iD])/gb[0]:.1e} {'PASS' if abs(pb - gb[iD]) <= TOL_POL*gb[0] else 'FAIL'}  |R_line - R_box| = "
                         f"{abs(gl[iD]/gl[0] - gb[iD]/gb[0]):.1e}")
            o(line + f'  {time.time() - t:.0f}s')
        o(f'   diagonal cut-off weight 1 - G(0)/f2: [line] {1 - gl[0]/zeta**2/F2:.4e}  [box] {1 - gb[0]/zeta**2/F2:.4e}  '
          f'[win] ' + ' '.join(f'{1 - gw[ie, 0]/zeta**2/F2:.4e}' for ie in range(len(EPS_WIN))))
        store[f'{Lam}_{km}'] = dict(gl=gl, gb=gb, gw=gw, kmax=kap.max())
    np.savez(os.path.join(_HERE, f'kernel_box{tag}.npz'), D=DGRID, eps=EPS_WIN, zeta=zeta,
             **{f'{k}_{q}': v[q] for k, v in store.items() for q in v})
    o(f'saved numerics/networks/kernel_box{tag}.npz')
def estimate(fits):
    """Extrapolated value = centre of the admissible fits' limits, uncertainty = half their spread (AGENTS.md sec. 5);
    (nan, nan, []) if no fit with a finite limit is admissible."""
    v = [f[1] for f in fits if f[4] and np.isfinite(f[1])]
    if not v:
        return np.nan, np.nan, []
    return 0.5*(max(v) + min(v)), 0.5*(max(v) - min(v)), [f[0] for f in fits if f[4] and np.isfinite(f[1])]

def ploc(hs, v):
    """Local convergence exponents from consecutive halvings: p = log2((v_k - v_{k+1})/(v_{k+1} - v_{k+2}))."""
    d = np.diff(np.asarray(v, float))
    with np.errstate(all='ignore'):
        return [float(np.log((d[k])/(d[k + 1]))/np.log(hs[k]/hs[k + 1])) for k in range(len(d) - 1)]

def k1fit():
    z = np.load(os.path.join(_HERE, 'kernel_t0.npz')); hA = z['hA']; G0A, GA = z['G0A'], z['GA']
    zb = np.load(os.path.join(_HERE, 'kernel_t0b.npz')); chk = []         # K1b: the h = 1/128 rung and its checks
    for ih, h in enumerate(zb['h']):
        if h in list(hA):
            chk.append(np.abs(zb['G'][ih] - GA[list(hA).index(h)]).max()/G0A[list(hA).index(h)])
        else:
            hA = np.append(hA, h); G0A = np.append(G0A, zb['G'][ih][0]); GA = np.vstack([GA, zb['G'][ih]])
    o = Out('kernel_t0_fits.out', """K1 fits, T0 frame; command: $PYTHON numerics/networks/corner_kernel.py K1fit (reads kernel_t0.npz, kernel_t0b.npz)
    Convergence variable h (cell width). Fits (corner_kernel.hfits) on 4 consecutive rungs: lin = v0 + c h (1/L), log = v0 + c log h
    (log L, no finite limit), pow = v0 + c h^p (p free); window 4f = 4 finest rungs, 4c = 4 rungs one step coarser (its
    residual at the finest rung is a prediction). Admissible iff max |residual| at the 3 finest rungs <= 1e-4 (fixed in the
    brief). Estimate = centre of the admissible limits +- half their spread. Two estimators of the same R: R_h = G_h/G0_h and
    G_h/f2 (f2 = Ghat(0) exactly, Theorem A). Resolved/cut-off modes: see kernel_t0.out; the cut-off (sub-cell) weight of
    the diagonal is 1 - G0_h/f2 (first block). 'log' fits have no finite limit and are excluded from the estimate even when
    their residual passes (R_h at Delta = 0.5, 8): a log h drift has constant increments per halving of h, the measured
    increments shrink by factors 0.47 ... 0.69 per halving (p_loc) -- a data argument, not a proof. Uncertainty u = fit
    half-spread + T0_SYST = 3e-4, the overshoot of this procedure on the known diagonal limit (G0/f2 -> 1.00028).""")
    o(f'Ladder h = ' + ' '.join(f'{h:.7f}' for h in hA) + f'  (K1b path vs K1 at the shared rungs: max rel. diff {max(chk):.1e})')
    est = {}
    for iD, D in enumerate(z['DA']):
        for lab, v in (('R_h = G/G0', GA[:, iD]/G0A), ('G/f2', GA[:, iD]/F2)):
            if D == 0 and lab.startswith('R_h'):
                continue
            fits = hfits(hA, v); c, u, names = estimate(fits); est[(float(D), lab[:3])] = (c, u + T0_SYST, v[-1], abs(v[-1] - v[-2]))
            o(f'Delta = {D:3.1f} {lab:10s}: ' + ' '.join(f'{x:.8f}' for x in v) + '  p_loc = ' +
              ' '.join(f'{p:.3f}' for p in ploc(hA, v)))
            for f in fits:
                o(f'      {f[0]:7s} limit = {f[1]:+.7f}  p = {f[2]:.3f}  max res(3 finest) = {f[3]:.1e}  '
                  f'{"admissible" if f[4] else "-"}')
            o(f'   -> estimate {c:+.6f} +- {u:.6f} (fit half-spread) + {T0_SYST:.0e} (calibrated overshoot) = +- {u + T0_SYST:.6f}'
              f'  (admissible finite-limit fits: {", ".join(names) if names else "none"})')
    o("Brief's ladder h = 0.24, 0.12, 0.06, 0.03 (window 4f only), against the dyadic estimate:")
    for iD, D in enumerate(z['DB']):
        if D == 0:
            continue
        ok = np.isfinite(z['GB'][:, iD]); hb = z['hB'][ok]; v = z['GB'][ok, iD]/z['G0B'][ok]
        fits = hfits(hb, v) if len(hb) >= 4 else []; c, u, names = estimate(fits)
        o(f'   Delta = {D:3.1f}: h = {list(hb)}  R_h = ' + ' '.join(f'{x:.8f}' for x in v) +
          f'  -> {c:+.6f} +- {u:.6f} ({", ".join(names) if names else "no admissible fit / < 4 rungs"});'
          f'  dyadic estimate {est.get((float(D), "R_h"), (np.nan,))[0]:+.6f}')
    o('Ymax dependence (Y = 14): Ymax = 20 vs Ymax = 24, R_h and G/f2 at Delta = 8, and G0/f2:')
    i8 = list(z['DA']).index(8.0); j8 = list(z['DC']).index(8.0)
    for ih, h in enumerate(z['hC']):
        r20, r24 = GA[ih, i8]/G0A[ih], z['GC'][ih, j8]/z['G0C'][ih]
        o(f'   h = {h:.6f}: R_h(8) = {r20:.8f} / {r24:.8f} (diff {r24 - r20:+.1e});  G(8)/f2 diff {(z["GC"][ih, j8] - GA[ih, i8])/F2:+.1e};'
          f'  G0/f2 = {G0A[ih]/F2:.8f} / {z["G0C"][ih]/F2:.8f}')
    np.savez(os.path.join(_HERE, 'kernel_t0_est.npz'), D=z['DA'], R=[est[(float(D), 'R_h')] if D else (1.0, 0.0, 1.0, 0.0) for D in z['DA']],
             S=[est[(float(D), 'G/f')] for D in z['DA']])
    return est
# ---------------------------------------------------------------- K2fit: kappa_max extrapolation of the box frame
def k2fit():
    za = np.load(os.path.join(_HERE, 'kernel_box.npz')); zb = np.load(os.path.join(_HERE, 'kernel_boxb.npz'))
    D = za['D']; ie = list(za['eps']).index(1e-12); zz = float(za['zeta'])**2
    o = Out('kernel_box_fits.out', """K2 fits, box frame; command: $PYTHON numerics/networks/corner_kernel.py K2fit (reads kernel_box.npz, kernel_boxb.npz)
    Production box symbol: Q_box eigenbasis with the spectral window eps = 1e-12 ('win'; equal to the regulator-free [box] where
    Q_box is resolved, eps-spread printed). Convergence variable 1/kappa_max at Lam = 120, kappa_max = 30, 45, ..., 120
    (kappa_max_eff 29.94 ... 119.7): the fits of corner_kernel.hfits with h := 1/kappa_max_eff (lin = 1/L, log = log L,
    pow = h^p) on 4 consecutive rungs (4f finest, 4c one step coarser), admissible iff residuals at the 3 finest rungs <= 1e-4.
    Cut-off weight of the modes beyond kappa_max: v(kappa_max) - v(finest) is printed (no extrapolated value if no fit is
    admissible). Window effect: (60,30) vs (120,30). [line] = line_so.py weights on the same modes, shown as [line] - [win].""")
    keys = [('a', '120_30'), ('a', '120_45'), ('a', '120_60'), ('b', '120_75'), ('b', '120_90'), ('b', '120_105'), ('b', '120_120')]
    zs = {'a': za, 'b': zb}; km = np.array([float(zs[s][k + '_kmax']) for s, k in keys]); est = {}
    o('kappa_max_eff = ' + ' '.join(f'{x:.2f}' for x in km))
    for iD, Dl in enumerate(D):
        for j, lab in ((0, 'R'), (1, 'G/f2')):
            if Dl == 0 and j == 0:
                continue
            gw = [zs[s][k + '_gw'][ie] for s, k in keys]; gl = [zs[s][k + '_gl'] for s, k in keys]
            v = np.array([g[iD]/g[0] if j == 0 else g[iD]/zz/F2 for g in gw])
            vl = np.array([g[iD]/g[0] if j == 0 else g[iD]/zz/F2 for g in gl])
            epsr = max(np.ptp(zs[s][k + '_gw'][:, iD]/(zs[s][k + '_gw'][:, 0] if j == 0 else zz*F2)) for s, k in keys)
            g6 = za['60_30_gw'][ie]; v60 = g6[iD]/g6[0] if j == 0 else g6[iD]/zz/F2
            fits = hfits(1/km, v); c, u, names = estimate(fits); est[(float(Dl), lab)] = (c, u, v[-1], abs(v[-1] - v[-2]))
            o(f'Delta = {Dl:3.1f} {lab:5s}: ' + ' '.join(f'{x:.7f}' for x in v) + f'   window (60,30)-(120,30) {v60 - v[0]:+.1e}'
              f'   eps-spread {epsr:.0e}   max|[line]-[win]| {np.nanmax(np.abs(vl - v)):.0e}')
            o('      cut-off weight v(kappa_max) - v(120): ' + ' '.join(f'{x - v[-1]:+.1e}' for x in v[:-1]) +
              '   |v(105) - v(120)| = ' + f'{abs(v[-1] - v[-2]):.1e}')
            o('      fits: ' + '; '.join(f'{f[0]} {f[1]:+.7f} p={f[2]:.2f} res={f[3]:.0e}{"*" if f[4] else ""}' for f in fits) +
              f'  -> {"%+.7f +- %.7f" % (c, u) if names else "no admissible fit"}')
    np.savez(os.path.join(_HERE, 'kernel_box_est.npz'), D=D,
             R=[est[(float(d), 'R')] if d else (1.0, 0.0, 1.0, 0.0) for d in D], S=[est[(float(d), 'G/f2')] for d in D])

# ---------------------------------------------------------------- K3: two-frame comparison, decay and sign
def box_envelope():
    """Box estimator S = G/f2 at kappa_max = 120 (Lam = 120), uncertainty = max |S(k) - S(120)| over k = 75, 90, 105 (the
    kappa-convergence is oscillatory: sharp cut-off, period ~ 4 pi^2/Delta in kappa); same for R = G/G0."""
    za = np.load(os.path.join(_HERE, 'kernel_box.npz')); zb = np.load(os.path.join(_HERE, 'kernel_boxb.npz'))
    ie = list(za['eps']).index(1e-12); zz = float(za['zeta'])**2
    gw = [zb[k + '_gw'][ie] for k in ('120_75', '120_90', '120_105', '120_120')]
    S = np.array([[g[i]/zz/F2 for g in gw] for i in range(len(za['D']))]); R = np.array([[g[i]/g[0] for g in gw] for i in range(len(za['D']))])
    env = lambda M: np.array([(M[i, -1], np.abs(M[i, :-1] - M[i, -1]).max()) for i in range(len(M))])
    return za['D'], env(S), env(R)

def k3():
    t = np.load(os.path.join(_HERE, 'kernel_t0_est.npz')); D, Sb, Rb = box_envelope(); Rt, St = t['R'], t['S']
    o = Out('kernel_decay.out', """K3 + two-frame comparison; command: $PYTHON numerics/networks/corner_kernel.py K3 (reads kernel_t0_est.npz,
    kernel_box.npz, kernel_boxb.npz). Tolerance fixed in the brief: |R_T0 - R_box| <= 1e-3. Estimators of the same R(Delta):
    T0: R_h = G_h/G0_h extrapolated in h (kernel_t0_fits.out; centre +- (half spread of the admissible fits + 3e-4, the
    calibrated overshoot)) and S = G_h/f2;
    box: S = G/f2 at kappa_max = 120 +- the envelope of kappa_max = 75..120 (no admissible smooth fit at small Delta: the
    kappa-convergence oscillates), and R = G/G0 (biased by the diagonal cut-off weight 1 - G0/f2 = 5.3e-4 at kappa_max = 120).
    Primary comparison: R_T0 vs S_box (the best-converged estimator in each frame); the others are printed. Decay fits on
    Delta in {3,4,5,6,8}: A e^{-alpha Delta} and A Delta^b e^{-alpha Delta} (least squares in log R), for each primary
    estimator and for R +- u; alpha = centre +- half spread. Sign: positive where R > u in both frames; R/u printed.
    Agreed value = midpoint of R_T0 and S_box, u = |diff|/2 + max(u_T0, u_box).""")
    o('Delta  R_T0 (u)              S_box (u)             |diff| <=1e-3 | S_T0 (u)              R_box (u)             max|diff| all  sign'
      '             R/u (T0, box)   agreed (u)')
    for i, d in enumerate(D):
        diff = abs(Rt[i][0] - Sb[i][0]); allv = [Rt[i][0], St[i][0], Sb[i][0], Rb[i][0]]
        sg = 'positive' if (Rt[i][0] > Rt[i][1] and Sb[i][0] > Sb[i][1]) else 'not established'
        o(f'{d:4.1f}  {Rt[i][0]:+.6f} ({Rt[i][1]:.6f})  {Sb[i][0]:+.6f} ({Sb[i][1]:.6f})  {diff:.1e}  {"yes" if diff <= TOL_FRAMES else "NO "}  | '
          f'{St[i][0]:+.6f} ({St[i][1]:.6f})  {Rb[i][0]:+.6f} ({Rb[i][1]:.6f})  {max(allv) - min(allv):.1e}  {sg:15s}'
          f'  {"n/a (R(0) = 1 by definition)" if d == 0 else f"{Rt[i][0]/Rt[i][1]:.0f}, {Sb[i][0]/Sb[i][1]:.0f}"}'
          f'  {(Rt[i][0] + Sb[i][0])/2:+.6f} ({diff/2 + max(Rt[i][1], Sb[i][1]):.6f})')
    m = (D >= 3) & (D <= 8); x = D[m]; alphas = []
    for lab, arr in (('R_T0', Rt), ('S_box', Sb)):
        for sgn in (0, 1, -1):
            y = np.log(arr[m, 0] + sgn*arr[m, 1])
            c1 = np.polyfit(x, y, 1); A2 = np.vstack([np.ones_like(x), np.log(x), x]).T; c2 = np.linalg.lstsq(A2, y, rcond=None)[0]
            r1 = np.abs(y - np.polyval(c1, x)).max(); r2 = np.abs(y - A2 @ c2).max(); alphas += [-c1[0], -c2[2]]
            o(f'   {lab:5s} {["R", "R+u", "R-u"][sgn]:3s}: A e^-aD: alpha = {-c1[0]:.4f} A = {np.exp(c1[1]):.4f} (max|res log R| {r1:.1e});'
              f'  A D^b e^-aD: alpha = {-c2[2]:.4f}, b = {c2[1]:+.3f} (max|res| {r2:.1e})')
        lr = np.log(arr[m, 0]); o(f'   {lab:5s} local rates -dlogR/dDelta on 3-4-5-6-8: ' + ' '.join(f'{v:.4f}' for v in -np.diff(lr)/np.diff(x)))
    o(f'alpha over all fits: {0.5*(max(alphas) + min(alphas)):.4f} +- {0.5*(max(alphas) - min(alphas)):.4f}')

# ---------------------------------------------------------------- K4 finite zeta, two corners (box frame, exact kernels)
def _pmesh2(Dl, ngl):
    """Nodes q in (0, Dl), graded (as _pmesh) towards BOTH ends; returns q, weights."""
    q1, w1 = _pmesh(Dl/2, ngl)
    return np.concatenate((q1, Dl - q1[::-1])), np.concatenate((w1, w1[::-1]))

def box_composite(a, L, sg1, sg2, pp, Lam, kmax, xic, ngl=12):
    """<e_j, D e_l>, D = Q - Q_rec, Q_rec(x,y) = sqrt(Phi'(x)Phi'(y)) Q(Phi(x),Phi(y)), Phi = k1 o k2, k1 parabolic at x = 0
    (sigma1), k2 parabolic at x = pp (sigma2), on the pieces P1 = (-a,0], P2 = (0,pp], P3 = (pp,L) where Phi is Moebius.
    Between pieces D(x,y) = (i/2pi) K(x,y), K = sqrt(m'(y))/(x - m(y)) - 1/(x - y), m = g_i^-1 o g_j: K12 (m = k1), K23
    (m = k2) are defect_matrix's 'exact' kernel at each corner; K13 (m = k1 o k2) = N/(E (u+y)) with u = -x, v' = y - pp,
    N = s2 (pp+u) v' + s1 u (y + s2 pp v'), E = (u+y) + s2 (pp+u) v' + s1 u (y + s2 pp v') (all terms positive: no
    cancellation). Window [xic - Lam/2, xic + Lam/2]; nodes graded at both corners (_pmesh, _pmesh2)."""
    xi1 = np.log(a/L); a2, L2 = a + pp, L - pp; xi2 = np.log(a2/L2); Dl = xi2 - xi1; r1, r2 = a/L, a2/L2
    p1, w1 = _pmesh(xi1 - (xic - Lam/2), ngl); p3, w3 = _pmesh(xic + Lam/2 - xi2, ngl); q, w2 = _pmesh2(Dl, ngl)
    bet = lambda E: (a + L)*E/(1 + E)**2
    u1 = a*(-np.expm1(-p1))/(1 + r1*np.exp(-p1)); s1w = np.sqrt(bet(r1*np.exp(-p1)))*w1; X1 = xi1 - p1
    v3 = a2*np.expm1(p3)/(1 + r2*np.exp(p3)); s3w = np.sqrt(bet(r2*np.exp(p3)))*w3; X3 = xi2 + p3; y3 = pp + v3
    x2a = a*np.expm1(q)/(1 + r1*np.exp(q)); u2b = a2*(-np.expm1(-(Dl - q)))/(1 + r2*np.exp(-(Dl - q)))
    x2 = np.where(q < Dl/2, x2a, pp - u2b); u2 = np.where(q < Dl/2, pp - x2a, u2b)       # x and pp - x, stably
    s2w = np.sqrt(bet(r1*np.exp(q)))*w2; X2 = xi1 + q
    U = u1[:, None]
    K12 = sg1*U*x2[None, :]/((U + x2[None, :])*(U + x2[None, :] + sg1*U*x2[None, :]))
    K23 = sg2*u2[:, None]*v3[None, :]/((u2[:, None] + v3[None, :])*(u2[:, None] + v3[None, :] + sg2*u2[:, None]*v3[None, :]))
    V, Y = v3[None, :], y3[None, :]
    Nn = sg2*(pp + U)*V + sg1*U*(Y + sg2*pp*V); K13 = Nn/(((U + Y) + Nn)*(U + Y))
    k, kap = box_kgrid(Lam, kmax); J = np.zeros((len(k), len(k)), dtype=complex)
    for (Xl, sl, Xr, sr, K) in ((X1, s1w, X2, s2w, K12), (X2, s2w, X3, s3w, K23), (X1, s1w, X3, s3w, K13)):
        J += np.exp(-1j*np.outer(k, Xl)) @ ((K*sl[:, None]*sr[None, :]) @ np.exp(1j*np.outer(k, Xr)).T)
    Dh = (1j/(2*np.pi))*J/Lam
    return Dh + Dh.conj().T, kap

def logF_window(w, Qt_sub, dps=30):
    """-log F of the quasi-free states with symbols diag(w) and Qt_sub (Note 5 Thm 2.1/3.2), mpmath eigen-decompositions:
    the formula of numerics/fidelity_hp.py logF_flint (Theorem A pipeline, results_hp.txt) without its entropy part."""
    import mpmath as mp
    mp.mp.dps = dps; n = len(w); M = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            M[i, j] = mp.mpc(float(Qt_sub[i, j].real), float(Qt_sub[i, j].imag))
    E, V = mp.eighe(M); wm = [mp.mpf(float(x)) for x in w]
    assert min(E) > 0 and max(E) < 1, (float(min(E)), float(max(E)))
    Wm = mp.matrix(n, n)
    for l in range(n):
        g2h = mp.sqrt(E[l]/(1 - E[l]))
        for i in range(n):
            Wm[i, l] = mp.sqrt(wm[i]/(1 - wm[i]))*V[i, l]*g2h
    sv = mp.svd_c(Wm, compute_uv=False)        # sqrt(tau) = singular values of Wm (eighe of Wm Wm^H fails to converge
    return float(-sum(mp.log(1 - wm[i])/2 + mp.log(1 - E[i])/2 + mp.log(1 + sv[i]) for i in range(n)))   # at eps = 1e-11)

def k4(boxes=((60, 30),), epss=(1e-8,), tag=''):
    import compression_box as cb
    o = Out(f'kernel_k4{tag}.out', f"""K4{tag}, finite zeta, two corners; command: $PYTHON numerics/networks/corner_kernel.py K4{tag} (background)
    Box frame, I = (-1, 2), corners at x = 0 and p'(Delta) (KERNEL_RESULTS.md (C3)), zeta1 = zeta2 = zeta: sigma1 = zeta (a+L)/(a L),
    sigma2 = zeta (a+L)/((a+p')(L-p')). D = EXACT composite kernel of Phi = k1 o k2 (corner_kernel.box_composite); Phi_A(zeta_i)
    = the same code path with the other sigma = 0 (same box, modes and nodes: discretisation errors common to Phi_2 and Phi_A
    cancel at first order). compression_box.fid_relent is NOT used: in double precision it returns O(1) noise of either sign
    for exact kernels already at (60,30) (numerics/results_batch3.txt:1-7: -9.4 ... +3.1); instead the Theorem A pipeline's method (numerics/fidelity_hp.py):
    sub-compression onto the eigenvectors of Q_box with eigenvalue in [eps, 1-eps] (a compression, so -log F_eps <= -log F),
    30-digit mpmath fidelity (corner_kernel.logF_window). G_eps(Delta) = the 'first'-kernel bilinear form in the SAME window.
    rem = Phi_2 - Phi_A1 - Phi_A2 - 2 zeta^2 G_eps(Delta). Resolved: box modes with |kappa| <~ kappa_c = log((1-eps)/eps)
    (18.4 for eps = 1e-8, 25.3 for 1e-11) inside |kappa| <= kappa_max; cut off: the rest (tail of the diagonal ~ zeta^2/
    (15 kappa_c^2), numerics/fidelity_hp.py), common to all three Phi's.""")
    a, L = 1.0, 2.0; xi0 = np.log(a/L); z0 = 1/3
    for (Lam, km) in boxes:
        k_, kap = box_kgrid(Lam, km); Q = cb.Q_box(kap, Lam, xi0=xi0); w, U, Nw = sld(Q)
        D1f, _ = box_corner(a, L, 1.0, Lam, km, xi0)
        o(f'({Lam}, {km}): N = {len(kap)}, kappa_max_eff = {kap.max():.2f}')
        sg = 0.1*(a + L)/(a*L); Dc, _ = box_composite(a, L, sg, 0.0, p_of_Delta(a, L, 2.0), Lam, km, xi0)
        De, _ = box_corner(a, L, sg*L, Lam, km, xi0, kind='exact'); e1 = np.abs(Dc - De).max()/np.abs(De).max()
        pp = p_of_Delta(a, L, 2.0); s2 = 0.1*(a + L)/((a + pp)*(L - pp)); Dc2, _ = box_composite(a, L, 0.0, s2, pp, Lam, km, xi0)
        De2, _ = box_corner(a + pp, L - pp, s2*(L - pp), Lam, km, xi0, kind='exact'); e2 = np.abs(Dc2 - De2).max()/np.abs(De2).max()
        o(f'   code check: box_composite(sigma2 = 0) vs box_corner exact {e1:.1e}; (sigma1 = 0) vs box_corner exact at p\'(2) {e2:.1e}')
        for eps in epss:
            keep = (w > eps) & (w < 1 - eps); Pk = U[:, keep]; wk = w[keep]; Nk = Nw[np.ix_(keep, keep)]
            A1 = Pk.conj().T @ D1f @ Pk; o(f'   window eps = {eps:.0e}: {int(keep.sum())} of {len(w)} modes, G_eps(0)/f2 = {bil(Nk, A1, A1)/z0**2/F2:.6f}')
            for Dl in (1.0, 2.0, 4.0, 8.0):
                t = time.time(); pp = p_of_Delta(a, L, Dl); a2, L2 = a + pp, L - pp
                D2f, _ = box_corner(a2, L2, z0*(a + L)/a2, Lam, km, xi0); G = bil(Nk, A1, Pk.conj().T @ D2f @ Pk)/z0**2
                for z in (0.05, 0.1, 0.2):
                    s1, s2 = z*(a + L)/(a*L), z*(a + L)/((a + pp)*(L - pp))
                    ph = [logF_window(wk, Pk.conj().T @ (Q - box_composite(a, L, x1, x2, pp, Lam, km, xi0)[0]) @ Pk)
                          for (x1, x2) in ((s1, s2), (s1, 0.0), (0.0, s2))]
                    rem = ph[0] - ph[1] - ph[2] - 2*z*z*G
                    o(f'   eps {eps:.0e} Delta = {Dl:3.1f} zeta = {z:4.2f}: Phi_2 = {ph[0]:.10e} Phi_A1 = {ph[1]:.10e} Phi_A2 = '
                      f'{ph[2]:.10e} 2zeta^2 G = {2*z*z*G:.6e} rem = {rem:+.4e} rem/zeta^3 = {rem/z**3:+.6f} rem/(2zeta^2 G) = '
                      f'{rem/(2*z*z*G):+.3e} Phi_A1/zeta^2/G(0) - 1 = {ph[1]/z**2/(bil(Nk, A1, A1)/z0**2) - 1:+.3e}  {time.time() - t:.0f}s')

def k4v():
    """Validation of the K4 fidelity path against the Theorem A pipeline (single corner, exact kernel, same window)."""
    import compression_box as cb
    o = Out('kernel_k4_validate.out', """K4 validation; command: $PYTHON numerics/networks/corner_kernel.py K4v (about 2 min)
    box_composite with sigma2 = 0 (one corner, sigma1 = s/L) and logF_window in the window eps against the published
    sub-compressed values -log F_sub of numerics/results_A2.txt (eps = 1e-8, 61 modes) and numerics/results_hp.txt
    (eps = 1e-11, 81 modes, dps 40); box (60, 30), a = 1, L = 2.""")
    a, L = 1.0, 2.0; xi0 = np.log(a/L); k_, kap = box_kgrid(60, 30); Q = cb.Q_box(kap, 60, xi0=xi0); w, U, Nw = sld(Q)
    for (eps, s, ref, src) in ((1e-8, 0.025, 5.679016e-07, 'results_A2.txt:1'), (1e-8, 0.1, 8.863062e-06, 'results_A2.txt:3'),
                               (1e-11, 0.025, 5.744436e-07, 'results_hp.txt:1')):
        keep = (w > eps) & (w < 1 - eps); Pk = U[:, keep]
        D, _ = box_composite(a, L, s/L, 0.0, p_of_Delta(a, L, 1.0), 60, 30, xi0)
        v = logF_window(w[keep], Pk.conj().T @ (Q - D) @ Pk)
        o(f'   eps = {eps:.0e}, s = {s}: -log F_sub = {v:.9e}  published {ref:.6e} ({src})  rel. diff {abs(v - ref)/ref:.1e}')

if __name__ == '__main__':
    task = sys.argv[1] if len(sys.argv) > 1 else 'K0'
    {'K0': k0, 'K1': k1, 'K2': k2, 'K1fit': k1fit, 'K2fit': k2fit, 'K3': k3, 'K2b': lambda: k2(BOXES2, 'b'), 'K4': k4, 'K1b': k1b, 'K4b': lambda: k4(epss=(1e-11,), tag='b'), 'K4v': k4v}[task]()
