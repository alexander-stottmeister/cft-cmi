"""RC (post-referee): high-precision evaluation of the computable bound of Theorem 4.2.
   Phi <= Bcan := -log|det(S_Q sqrt(Q~) + C_Q U sqrt(1-Q~))|,   U = polar(G_Q^{1/2} G_A^{1/2}),
   Phi - Phi_W <= Bcan - Phi_W = Phi_22 + Phi_off   (control identity: -log|det M_A| = Phi_W + Phi_22).
All in mpmath at dps digits, in the eigenbasis of the ball-certified Q_N.  Phi_W is recomputed from
the same ball Q_N (no trapezoid input).   Usage: cert_tail_hp.py <Dhat.npz> <qball.pkl> <eps> <dps>
"""
import sys, pickle, time
import numpy as np, mpmath as mp
def H(M): return (M + M.transpose_conj())/2
def tomp(A):
    n, m = A.shape
    return mp.matrix([[mp.mpc(A[i,j]) for j in range(m)] for i in range(n)])
def fun_h(M, f):
    w, V = mp.eighe(H(M)); return V*mp.diag([f(x) for x in w])*V.transpose_conj(), w
def logdet_abs(M):
    """log|det M| via python-flint acb_mat (C level, ball arithmetic) at the current mp precision."""
    from flint import acb, acb_mat, ctx, arb
    ctx.prec = int(mp.mp.prec) + 64
    n = M.rows
    A = acb_mat([[acb(str(mp.nstr(mp.re(M[i,j]), mp.mp.dps+5)), str(mp.nstr(mp.im(M[i,j]), mp.mp.dps+5)))
                  for j in range(n)] for i in range(n)])
    d = A.det()
    return mp.mpf(abs(d).log().str(mp.mp.dps, radius=False).replace(' ',''))
def logfid(Q1, Q2):
    n = Q1.rows
    w1, V1 = mp.eighe(H(Q1)); w2, V2 = mp.eighe(H(Q2))
    G1h = V1*mp.diag([mp.sqrt(x/(1-x)) for x in w1])*V1.transpose_conj()
    G2 = V2*mp.diag([x/(1-x) for x in w2])*V2.transpose_conj()
    tt, _ = mp.eighe(H(G1h*G2*G1h))
    s = mp.mpf(0)
    for x in w1: s += mp.log(1-x)/2
    for x in w2: s += mp.log(1-x)/2
    for x in tt: s += mp.log(1+mp.sqrt(max(x, mp.mpf(0))))
    return -s
def main(dhat, qball, eps, dps):
    mp.mp.dps = dps; t0 = time.time()
    z = np.load(dhat, allow_pickle=True); D = z['Dhat']; kap = z['kappa']
    s = float(z['s']); a = float(z['a']); L = float(z['L']); zeta = a*s/(a+L)
    P = pickle.load(open(qball, "rb")); Q0 = P['mid']; N = len(kap)
    w0, U0 = np.linalg.eigh((Q0+Q0.conj().T)/2)             # float eigenbasis of Q_N (only a basis)
    Qm = H(tomp(U0.conj().T @ ((Q0+Q0.conj().T)/2) @ U0))   # exact rotate, still Hermitian
    Xm = H(tomp(U0.conj().T @ ((Q0-D+(Q0-D).conj().T)/2) @ U0))
    wq, Vq = mp.eighe(Qm)                                    # exact spectrum of Q_N in mp
    idx = sorted(range(N), key=lambda i: wq[i]); wq = [wq[i] for i in idx]
    Vq = mp.matrix([[Vq[r,i] for i in idx] for r in range(N)])
    X = H(Vq.transpose_conj()*Xm*Vq)                         # Q~ in the exact Q-eigenbasis
    win = [i for i in range(N) if eps < wq[i] < 1-eps]; out = [i for i in range(N) if not (eps < wq[i] < 1-eps)]
    sub = lambda M, r, c: mp.matrix([[M[i,j] for j in c] for i in r])
    A = mp.zeros(N)
    for r in (win, out):
        for p, i in enumerate(r):
            for q, j in enumerate(r): A[i,j] = X[i,j]
    A = H(A)
    wx, Vx = mp.eighe(X)                                 # one 91x91 eigendecomposition
    mk = lambda f: Vx*mp.diag([f(x) for x in wx])*Vx.transpose_conj()
    SX = mk(mp.sqrt); CX = mk(lambda t: mp.sqrt(1-t))
    SA = mp.zeros(N); CA = mp.zeros(N); GAh = mp.zeros(N); Up = mp.zeros(N)
    SQ = mp.diag([mp.sqrt(x) for x in wq]); CQ = mp.diag([mp.sqrt(1-x) for x in wq])
    for r in (win, out):                                 # A is block diagonal: work per block
        Ab = H(sub(X, r, r)); wa, Va = mp.eighe(Ab)
        f = lambda g: Va*mp.diag([g(x) for x in wa])*Va.transpose_conj()
        sa = f(mp.sqrt); ca = f(lambda t: mp.sqrt(1-t)); ga = f(lambda t: mp.sqrt(t/(1-t)))
        gq = mp.diag([mp.sqrt(wq[i]/(1-wq[i])) for i in r])
        Yb = gq*ga; wy, Vy = mp.eighe(H(Yb.transpose_conj()*Yb))
        up = Yb*(Vy*mp.diag([1/mp.sqrt(x) for x in wy])*Vy.transpose_conj())
        for p_, i in enumerate(r):
            for q_, j in enumerate(r):
                SA[i,j] = sa[p_,q_]; CA[i,j] = ca[p_,q_]; GAh[i,j] = ga[p_,q_]; Up[i,j] = up[p_,q_]
    MA = SQ*SA + CQ*Up*CA
    Bcan = -logdet_abs(SQ*SX + CQ*Up*CX)
    ctrl = -logdet_abs(MA)
    PhiW = logfid(mp.diag([wq[i] for i in win]), H(sub(X, win, win)))
    Phi22 = logfid(mp.diag([wq[i] for i in out]), H(sub(X, out, out)))
    off = Bcan - ctrl
    print(f"zeta={zeta:.6f} eps={eps:.0e} kc={-np.log(eps):.2f} N={N} nwin={len(win)} dps={dps} "
          f"PhiW={mp.nstr(PhiW,12)} Phi22={mp.nstr(Phi22,8)} Phioff={mp.nstr(off,8)} "
          f"ctrl-(PhiW+Phi22)={mp.nstr(ctrl-PhiW-Phi22,4)} bound={mp.nstr(Bcan-PhiW,8)} "
          f"width={float((Bcan-PhiW)/PhiW)*100:.3f}% ({time.time()-t0:.0f}s)", flush=True)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]))
