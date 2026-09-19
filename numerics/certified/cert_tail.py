"""RC / certified numerics, step 2: the quantities of Theorem 4.2 (cross-term-free tail bound)
   Phi - Phi_W  <=  Phi_22 + (c0/2)||Xi0||_2^2 + (c1/2)||Xi1||_2^2 + ||T||_2^2/(2(1-||T||)).
Everything is evaluated in the eigenbasis of the box symbol Q_N (so E is a coordinate projection),
at mpmath precision `dps`, from the ball-certified Q_N (numerics/certified/qball_*.pkl) and the
defect Dhat of numerics/Dhat_exact_*.npz.   Usage: cert_tail.py <Dhat.npz> <qball.pkl> <eps> [dps]
"""
import sys, pickle, time
import numpy as np, mpmath as mp

def herm(M): return (M + M.transpose_conj())/2
def fsqrt(M):
    w, U = mp.eighe(herm(M)); w = [mp.sqrt(max(x, mp.mpf(0))) for x in w]
    return U * mp.diag(w) * U.transpose_conj()
def logfid(Q1, Q2):
    """-log Fid of two quasi-free states with symbols Q1,Q2 (Note 5 Thm 2.1)."""
    n = Q1.rows
    w1, V1 = mp.eighe(herm(Q1)); w2, V2 = mp.eighe(herm(Q2))
    G1h = V1*mp.diag([mp.sqrt(x/(1-x)) for x in w1])*V1.transpose_conj()
    G2  = V2*mp.diag([x/(1-x) for x in w2])*V2.transpose_conj()
    tt, _ = mp.eighe(herm(G1h*G2*G1h))
    s = mp.mpf(0)
    for x in w1: s += mp.log(1-x)/2
    for x in w2: s += mp.log(1-x)/2
    for x in tt: s += mp.log(1+mp.sqrt(max(x, mp.mpf(0))))
    return -s
def opnorm(M):
    w, _ = mp.eighe(herm(M*M.transpose_conj())); return mp.sqrt(max(w))
def hs2(M):
    s = mp.mpf(0)
    for i in range(M.rows):
        for j in range(M.cols): s += abs(M[i,j])**2
    return s

def main(dhat, qball, eps, dps=40):
    mp.mp.dps = dps
    z = np.load(dhat, allow_pickle=True); D = z['Dhat']; kap = z['kappa']; s = float(z['s'])
    a = float(z['a']); L = float(z['L']); zeta = a*s/(a+L)
    P = pickle.load(open(qball, "rb")); Qf = P['mid']; rad = P['rad'].max()
    N = len(kap); assert Qf.shape == (N, N)
    Q = mp.matrix([[mp.mpc(Qf[i,j].real, Qf[i,j].imag) for j in range(N)] for i in range(N)])
    Dm = mp.matrix([[mp.mpc(D[i,j].real, D[i,j].imag) for j in range(N)] for i in range(N)])
    Qt = herm(Q - Dm); Q = herm(Q)
    w, U = mp.eighe(Q)                                 # eigenbasis of Q: E is a coordinate projection
    idx = sorted(range(N), key=lambda i: w[i])
    w = [w[i] for i in idx]; U = mp.matrix([[U[r, i] for i in idx] for r in range(N)])
    X = U.transpose_conj()*Qt*U                        # Qtilde in the Q-eigenbasis
    win = [i for i in range(N) if eps < w[i] < 1-eps]
    out = [i for i in range(N) if i not in win]
    ip = [i for i in out if w[i] <= eps]; im = [i for i in out if w[i] >= 1-eps]
    kc = -mp.log(eps)
    sub = lambda M, r, c: mp.matrix([[M[i,j] for j in c] for i in r])
    X11 = herm(sub(X, win, win)); X22 = herm(sub(X, out, out))
    tau_p = sum(X[i,i].real for i in ip); tau_m = sum((1-X[i,i]).real for i in im)
    A = mp.zeros(N)
    for r, c in ((win, win), (out, out)):
        B = sub(X, r, c)
        for p, i in enumerate(r):
            for q, j in enumerate(c): A[i,j] = B[p,q]
    A = herm(A)
    SA = fsqrt(A); CA = fsqrt(mp.eye(N)-A); SX = fsqrt(X); CX = fsqrt(mp.eye(N)-X)
    Xi0 = SX - SA; Xi1 = CX - CA
    QD = mp.diag([w[i] for i in range(N)]); SQ = mp.diag([mp.sqrt(w[i]) for i in range(N)])
    CQ = mp.diag([mp.sqrt(1-w[i]) for i in range(N)])
    # optimal Uhlmann unitary for the block-diagonal pair (Q, A): polar unitary of G_Q^{1/2} G_A^{1/2}
    GQh = mp.diag([mp.sqrt(w[i]/(1-w[i])) for i in range(N)])
    GAh = fsqrt(mp.matrix([[A[i,j] for j in range(N)] for i in range(N)]) *
                (mp.eye(N)-A)**-1)
    Y = GQh*GAh
    Uh, Sv, Vh = mp.svd_c(Y); Upol = Uh*Vh
    MA = SQ*SA + CQ*Upol*CA
    T = MA**-1*(SQ*Xi0 + CQ*Upol*Xi1)
    Y0 = (MA**-1*SQ + SQ*(MA**-1).transpose_conj())/2
    Y1 = (MA**-1*CQ*Upol + (CQ*Upol).transpose_conj()*(MA**-1).transpose_conj())/2
    iSA = mp.matrix([[SA[i,j] for j in range(N)] for i in range(N)])**-1
    isqA = fsqrt(iSA); isqC = fsqrt(CA**-1)
    c0 = opnorm(isqA*Y0*isqA); c1 = opnorm(isqC*Y1*isqC)
    Q22 = mp.diag([w[i] for i in out]); Phi22 = logfid(Q22, herm(X22))
    PhiW = logfid(mp.diag([w[i] for i in win]), X11)
    n0 = hs2(Xi0); n1 = hs2(Xi1); nT2 = hs2(T); nT = opnorm(T)
    bound = Phi22 + c0*n0/2 + c1*n1/2 + nT2/(2*(1-nT))
    print(f"# {dhat} eps={eps:.1e} kc={float(kc):.2f} zeta={zeta:.6f} N={N} nwin={len(win)} Qrad={rad:.1e} dps={dps}")
    print(f"PhiW      = {mp.nstr(PhiW,10)}")
    print(f"tau+={float(tau_p):.4e} tau-={float(tau_m):.4e} Phi22={mp.nstr(Phi22,6)}")
    print(f"|Xi0|_2^2={float(n0):.4e} |Xi1|_2^2={float(n1):.4e} c0={float(c0):.5f} c1={float(c1):.5f}")
    print(f"|T|_2^2={float(nT2):.4e} |T|={float(nT):.4e}")
    print(f"NEWBOUND  = {float(bound):.6e}   (Phi-PhiW <= this)")
    ptb = 0.173*zeta**2/float(kc) + 0.88*zeta**2/float(kc)**2
    print(f"PT bound  = {ptb:.6e};  ratio = {ptb/float(bound):.1f}")
    print(f"BRACKET   = [{float(PhiW):.6e}, {float(PhiW+bound):.6e}]  width/Phi = {float(bound/PhiW)*100:.2f}%")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 40)
