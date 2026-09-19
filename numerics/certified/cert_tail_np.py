"""RC step 2 (double precision): the quantities of Theorem 4.2 (cross-term-free tail bound)
   Phi - Phi_W <= Phi_22 + (c0/2)||Xi0||^2 + (c1/2)||Xi1||^2 + ||T||_2^2/(2(1-||T||)).
Q_N from the ball-certified enclosure (mid values, radius <= 6e-18); Dhat from ../Dhat_exact_*.npz.
Usage: cert_tail_np.py <Dhat.npz> <qball.pkl> <eps>"""
import sys, pickle, numpy as np, mpmath as mp
from scipy.linalg import sqrtm, polar
def herm(M): return (M + M.conj().T)/2
def fsq(M):
    w, U = np.linalg.eigh(herm(M)); w = np.clip(w, 0, None)
    return (U*np.sqrt(w)) @ U.conj().T
def logfid(Q1, Q2, dps=60):
    mp.mp.dps = dps; n = Q1.shape[0]
    M1 = mp.matrix([[mp.mpc(Q1[i,j]) for j in range(n)] for i in range(n)])
    M2 = mp.matrix([[mp.mpc(Q2[i,j]) for j in range(n)] for i in range(n)])
    H = lambda M: (M + M.transpose_conj())/2
    w1, V1 = mp.eighe(H(M1)); w2, V2 = mp.eighe(H(M2))
    G1h = V1*mp.diag([mp.sqrt(x/(1-x)) for x in w1])*V1.transpose_conj()
    G2 = V2*mp.diag([x/(1-x) for x in w2])*V2.transpose_conj()
    tt, _ = mp.eighe(H(G1h*G2*G1h))
    s = mp.mpf(0)
    for x in w1: s += mp.log(1-x)/2
    for x in w2: s += mp.log(1-x)/2
    for x in tt: s += mp.log(1+mp.sqrt(max(x, mp.mpf(0))))
    return -s
def main(dhat, qball, eps):
    z = np.load(dhat, allow_pickle=True); D = z['Dhat']; kap = z['kappa']
    s = float(z['s']); a = float(z['a']); L = float(z['L']); zeta = a*s/(a+L)
    P = pickle.load(open(qball,"rb")); Q0 = P['mid']; N = len(kap)
    Qt = herm(Q0 - D); Q0 = herm(Q0)
    w, U = np.linalg.eigh(Q0)                       # E is a coordinate projection in this basis
    X = herm(U.conj().T @ Qt @ U)
    win = np.where((w > eps) & (w < 1-eps))[0]; out = np.where((w <= eps) | (w >= 1-eps))[0]
    ip = out[w[out] <= eps]; im = out[w[out] >= 1-eps]; kc = -np.log(eps)
    A = np.zeros_like(X)
    A[np.ix_(win,win)] = X[np.ix_(win,win)]; A[np.ix_(out,out)] = X[np.ix_(out,out)]; A = herm(A)
    tau_p = float(np.sum(np.real(np.diag(X)[ip]))); tau_m = float(np.sum(1-np.real(np.diag(X)[im])))
    nu = float(np.sum(w[ip]) + np.sum(1-w[im]))
    W12 = X[np.ix_(win,out)]
    SA, CA = fsq(A), fsq(np.eye(N)-A); SX, CX = fsq(X), fsq(np.eye(N)-X)
    Xi0, Xi1 = SX-SA, CX-CA
    SQ = np.diag(np.sqrt(w)); CQ = np.diag(np.sqrt(1-w))
    GQh = np.diag(np.sqrt(w/(1-w))); GAh = fsq(A @ np.linalg.inv(np.eye(N)-A))
    Up, _ = polar(GQh @ GAh)                        # optimal Uhlmann unitary for (Q, A)
    MA = SQ@SA + CQ@Up@CA; iMA = np.linalg.inv(MA)
    T = iMA @ (SQ@Xi0 + CQ@Up@Xi1)
    Y0 = herm(iMA@SQ); Y1 = herm(iMA@CQ@Up)
    iA = np.linalg.inv(SA); iC = np.linalg.inv(CA)
    c0 = float(np.max(np.abs(np.linalg.eigvalsh(herm(fsq(iA)@Y0@fsq(iA))))))
    c1 = float(np.max(np.abs(np.linalg.eigvalsh(herm(fsq(iC)@Y1@fsq(iC))))))
    Phi22 = float(logfid(np.diag(w[out]).astype(complex), herm(X[np.ix_(out,out)])))
    PhiW = float(sys.argv[4]) if len(sys.argv) > 4 else float('nan')
    sgn, ld = np.linalg.slogdet(np.eye(N) + T); Phioff = -float(ld)
    n0 = float(np.sum(np.abs(Xi0)**2)); n1 = float(np.sum(np.abs(Xi1)**2))
    nT2 = float(np.sum(np.abs(T)**2)); nT = float(np.linalg.norm(T, 2))
    bd = Phi22 + Phioff
    bdg = Phi22 + c0*n0/2 + c1*n1/2 + nT2/(2*(1-nT))
    ptb = 0.173*zeta**2/kc + 0.88*zeta**2/kc**2
    print(f"zeta={zeta:.6f} eps={eps:.0e} kc={kc:.2f} N={N} nwin={len(win)} "
          f"PhiW={PhiW:.8e} tau+={tau_p:.3e} tau-={tau_m:.3e} nu={nu:.2e} "
          f"|X12|^2={float(np.sum(np.abs(W12)**2)):.3e} Phi22={Phi22:.3e} "
          f"|Xi0|^2={n0:.3e} |Xi1|^2={n1:.3e} c0={c0:.4f} c1={c1:.4f} |T|2^2={nT2:.3e} |T|={nT:.3e} "
          f"Phioff={Phioff:.3e} NEW={bd:.4e} GUAR={bdg:.3e} PT={ptb:.4e} gain={ptb/bd:.1f} width={100*bd/PhiW:.2f}%")
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
