"""Clean version: same sub-compression DIMENSION (61) for both, so the comparison isolates the
endpoint term rather than the change of n_sub."""
import sys, numpy as np, mpmath as mp
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics")
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/rigor")
from compression_box import Q_box
from v4_fid import to_mp, logfid_route_A
NUM = "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/"
z = np.load(NUM+"Dhat_exact_s0.2_Lam60_k30_g12.npz", allow_pickle=True)
D = z['Dhat']; kap = z['kappa']; Lam = 60.0; zeta = 1/15.
nt = 400001; w0 = Lam/(2*(nt-1)); k = kap/(2*np.pi)
Qw = Q_box(kap, Lam)
Qn = Qw.copy(); Qn[np.arange(len(k)), np.arange(len(k))] += (1/(2*np.pi*Lam))*w0*2*Lam*k
mp.mp.dps = 40
for tag, QQ in [("with t->0 endpoint (code)", Qw), ("endpoint omitted", Qn)]:
    Qm = to_mp(QQ); Dm = to_mp(D); Qt = Qm-Dm
    w, V = mp.eighe(Qm); N = Qm.rows
    order = sorted(range(N), key=lambda i: abs(w[i]-mp.mpf('0.5')))[:61]
    P = mp.matrix(N, 61)
    for c, i in enumerate(order):
        for r in range(N): P[r, c] = V[r, i]
    ws = [w[i] for i in order]
    A = float(logfid_route_A(mp.diag(ws), P.H*Qt*P).real)
    print(f"  {tag:28s}: n_sub=61 (fixed)  -logF_sub={A:.8e}", flush=True)
