"""E2 common: the real Hilbert space S_2(PH,P^perp H), the visible space N, its
projection Pi, the exterior space Ext and its projection, in S10's NS-circle model.

Real inner product <A,B> = Re Tr(A^* B) on  V := {A : A = P^perp A P}.
  N    = span_R{ P^perp l P : l = l^* = E_I l E_I }
  Ext  = span_R{ P^perp Z P : Z^* = -Z = E_c Z E_c },   E_c = E_{I^c}
Pairings (A in V):
  <P^perp l P, A>   = (1/2) Tr( l  E_I (A+A^*) E_I )          -> N^perp: E_I(A+A^*)E_I = 0
  <P^perp Z P, A>   = -(1/2) Tr( Z  E_c (A-A^*) E_c )         -> Ext^perp: E_c(A-A^*)E_c = 0
Gram (exact, no truncation, because l = E_I l E_I and Z = E_c Z E_c):
  E_I(P^perp l P + P l P^perp)E_I = (1-Q) l Q + Q l (1-Q),    Q  = E_I P E_I
  E_c(P^perp Z P + P Z P^perp)E_c = (1-Qc) Z Qc + Qc Z (1-Qc), Qc = E_c P E_c
so in the eigenbasis of Q (resp. Qc) both maps are multiplication by
  den_ij = q_i(1-q_j)+q_j(1-q_i)  (resp. denc_ij).  Hence
  ||Pi A||^2        = (1/2) sum_ij |eta_ij|^2 / den_ij ,  eta = E_I(A+A^*)E_I  in Q-basis
  ||Proj_Ext A||^2  = (1/2) sum_ij |K_ij|^2  / denc_ij ,  K   = E_c(A-A^*)E_c in Qc-basis
and the Tikhonov-regularised exterior optimum (bounded ||Z||_F) is den -> den+mu.
"""
import numpy as np, scipy.linalg as sla

def build(L=128, a=2.0, Lg=1.0, alpha=3.0, uv=(0.30, 0.42), cap=1e10, cg=80):
    th = 2*np.pi*np.arange(L)/L; thw = np.where(th > np.pi, th-2*np.pi, th)
    n = np.fft.fftfreq(L, d=1.0/L); nu = n+0.5
    F = np.fft.fft(np.eye(L), axis=0)/L; Fi = np.fft.ifft(np.eye(L), axis=0)*L
    P = Fi@np.diag((nu > 0).astype(float))@F; P = 0.5*(P+P.conj().T); Pp = np.eye(L)-P
    a1, a2 = uv; xx = (np.abs(nu)/L-a1)/(a2-a1); s_ = np.clip(1-xx, 0, 1); s_ = s_*s_*(3-2*s_)
    d = Fi@np.diag(1j*nu*s_)@F; d = 0.5*(d-d.conj().T)
    thD = 2*np.arctan(Lg); thA = -2*np.arctan(a)
    inD = (thw > 0) & (thw < thD); inA = (thw > thA) & (thw < 0); inI = inD | inA
    chi = np.zeros(L); chi[inD] = np.cos(thw[inD])-1.0
    t = thw.copy(); t[t < thA] += 2*np.pi; mm = ~inI
    chi[mm] = (np.cos(t[mm])-1.0)*np.exp(-alpha*(t[mm]-thD)**2)
    X = np.diag(chi); Dc = 0.5*(X@d+d@X); Dc = 0.5*(Dc-Dc.conj().T)
    I = np.where(inI)[0]; Ic = np.where(~inI)[0]; D = np.where(inD)[0]
    Q = P[np.ix_(I, I)]; Q = 0.5*(Q+Q.conj().T); q, U = np.linalg.eigh(Q)
    qc = P[np.ix_(Ic, Ic)]; qc = 0.5*(qc+qc.conj().T); qcv, Uc = np.linalg.eigh(qc)
    q = np.clip(q, 0.0, 1.0); qcv = np.clip(qcv, 0.0, 1.0)
    den = q[:, None]*(1-q)[None, :] + q[None, :]*(1-q)[:, None]
    denc = qcv[:, None]*(1-qcv)[None, :] + qcv[None, :]*(1-qcv)[:, None]
    S = dict(L=L, P=P, Pp=Pp, I=I, Ic=Ic, D=D, Dc=Dc, q=q, U=U, den=den,
             qc=qcv, Uc=Uc, denc=denc, thD=thD, thA=thA, cap=cap)
    return S

def etaI(S, A):
    """E_I(A+A^*)E_I in the Q-eigenbasis (A must satisfy A = P^perp A P)."""
    I, U = S['I'], S['U']
    H = (A+A.conj().T)[np.ix_(I, I)]
    return U.conj().T@H@U

def etaC(S, A):
    """E_c(A-A^*)E_c in the Qc-eigenbasis."""
    Ic, Uc = S['Ic'], S['Uc']
    K = (A-A.conj().T)[np.ix_(Ic, Ic)]
    return Uc.conj().T@K@Uc

def normPi2(S, A, tol=0.0):
    """||Pi A||^2 = (1/2) sum |eta|^2/den  (modes with den<=tol dropped; also
    returns the leaked weight on those modes, which must be ~0)."""
    e = etaI(S, A); den = S['den']; ok = den > tol
    val = 0.5*np.sum(np.abs(e[ok])**2/den[ok])
    leak = 0.5*np.sum(np.abs(e[~ok])**2) if (~ok).any() else 0.0
    return val, leak

def normExt2(S, A, mu=0.0, tol=0.0):
    """||Proj_Ext A||^2 and, for mu>0, the Tikhonov data:
    returns (proj2, dist2(mu), ||Z||_F^2(mu)) with Z_ij = -K_ij/(denc_ij+mu)."""
    K = etaC(S, A); dc = S['denc']; ok = dc > tol
    proj2 = 0.5*np.sum(np.abs(K[ok])**2/dc[ok])
    leak = 0.5*np.sum(np.abs(K[~ok])**2) if (~ok).any() else 0.0
    w = 1.0/(dc+mu)
    z2 = np.sum(np.abs(K)**2*w**2)
    red = np.sum(np.abs(K)**2*w) - 0.5*np.sum(dc*np.abs(K)**2*w**2)
    return proj2, leak, red, z2

def Zext(S, A, mu=0.0):
    """the minimising exterior anti-Hermitian Z_e (L x L, supported on I^c)."""
    Ic, Uc, dc, L = S['Ic'], S['Uc'], S['denc'], S['L']
    K = etaC(S, A); z = -K/(dc+mu)
    Zb = Uc@z@Uc.conj().T; Zb = 0.5*(Zb-Zb.conj().T)
    Z = np.zeros((L, L), complex); Z[np.ix_(Ic, Ic)] = Zb
    return Z

def PiA(S, A, tol=0.0):
    """Pi A as an L x L matrix."""
    I, U, den, L = S['I'], S['U'], S['den'], S['L']
    e = etaI(S, A); w = np.where(den > tol, 1.0/np.where(den > tol, den, 1.0), 0.0)
    l = U@(w*e)@U.conj().T; Lf = np.zeros((L, L), complex); Lf[np.ix_(I, I)] = l
    return S['Pp']@Lf@S['P']

def riesz_G(S, G):
    """v_G = Pi(P^perp G P) for anti-Hermitian G; returns (v, ||v||^2)."""
    A = S['Pp']@G@S['P']; v = PiA(S, A); n2, _ = normPi2(S, A)
    return v, n2

def Gstar(S, iters=80):
    """CG for the S10 optimal rotation direction; returns (theta, G (raw x), eps_star, |u|^2, u)."""
    L, D, Pp, P = S['L'], S['D'], S['Pp'], S['P']
    M = Pp@S['Dc']@P
    nu2, _ = normPi2(S, M); u = PiA(S, M)
    def emb(g):
        G = np.zeros((L, L), complex); G[np.ix_(D, D)] = g; return G
    def Aop(g):
        v, _ = riesz_G(S, emb(g)); R = v[np.ix_(D, D)]; return 0.5*(R-R.conj().T)
    R = u[np.ix_(D, D)]; b = 0.5*(R-R.conj().T)
    x = np.zeros_like(b); r = b.copy(); p = r.copy(); rs = np.real(np.vdot(r, r))
    for k in range(iters):
        Ap = Aop(p); pAp = np.real(np.vdot(p, Ap))
        if pAp <= 1e-30: break
        al = rs/pAp; x = x+al*p; r = r-al*Ap
        rs2 = np.real(np.vdot(r, r)); p = r+(rs2/rs)*p; rs = rs2
    theta = np.real(np.vdot(b, x))/nu2
    G = emb(x); G = 0.5*(G-G.conj().T)
    v, nv2 = riesz_G(S, G); eps = -np.real(np.vdot(u, v))/nv2
    return theta, G, eps, nu2, u, M
