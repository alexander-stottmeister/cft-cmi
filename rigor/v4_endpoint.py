"""Effect of the t->0 endpoint term of the Q_box diagonal on Phi (note: 'O(h) error of 0.2%')."""
import sys, numpy as np, mpmath as mp
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics")
sys.path.insert(0, "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/rigor")
from compression_box import Q_box
from v4_fid import subcompress, logfid_route_A
NUM = "/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/"
z = np.load(NUM+"Dhat_exact_s0.2_Lam60_k30_g12.npz", allow_pickle=True)
D = z['Dhat']; kap = z['kappa']; Lam = 60.0; zeta = 1/15.; eps = 1e-8
kc = np.log((1-eps)/eps); tail = zeta**2/(15*kc**2)
nt = 400001; w0 = Lam/(2*(nt-1)); k = kap/(2*np.pi)
Qw = Q_box(kap, Lam)
Qn = Qw.copy(); Qn[np.arange(len(k)), np.arange(len(k))] += (1/(2*np.pi*Lam))*w0*2*Lam*k
for tag, QQ in [("with t->0 endpoint (code)", Qw), ("endpoint omitted", Qn)]:
    ws, Qsub, _ = subcompress(QQ, D, eps)
    A = float(logfid_route_A(mp.diag(ws), Qsub).real)
    print(f"  {tag:28s}: n_sub={len(ws):3d}  -logF_sub={A:.8e}  +tail={A+tail:.8e}", flush=True)
