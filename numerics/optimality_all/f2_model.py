"""F2 (Phase 5): shared circle-model builder for the fixed-geometry TANGENT problem.

Conventions are copied verbatim from S10 (s10_theta.py, s10_circle2.py,
rigor/sdp_dual_certificate.tex Sec. 7): NS circle on L sites, P = 1_{nu>0} exact,
smoothstep UV taper uv=(0.30,0.42) on the spectral derivative, alpha=3, a=2, Lg=1,
weight cap 1e10 (w = min(1/den, cap), q clipped to [1e-300, 1-1e-16]).

  Q = E_I P E_I,   q,U = eigh(Q),   den_ij = q_i(1-q_j)+q_j(1-q_i),  w = min(1/den,cap)
  g_Q(delta) = (1/4) sum_ij w_ij |(U^H delta U)_ij|^2       (optimality_second_order.tex)
  SLD        t = (1/2) U (w o delta~) U^H,   g_Q(delta) = (1/4) Tr(t delta)

First-order (tangent) defect delta = Q - Q_rec, in units of s (V = (1-sG) e^{s D_chi},
X X* = 1 - s N1, noise s Y1):
  delta_c   = E_I [P, D_chi] E_I                        (compression, = s^{-1} d/ds)
  delta_rot = E_I [G, P] E_I = [G, Q]                   (G = i H anti-Herm., supported on D)
  noise_DD  = (1/2){N1, Q_DD} - Y1,  noise_DA = (1/2) N1 Q_DA,  noise_AA = 0.
The relative sign of delta_c and the noise is fixed by delta = Q - Q_rec with
Q_rec,DD = V Q_BB V* - (s/2){N1, V Q_BB V*} + s Y1 and Q_rec,DA = (1-sN1/2) V Q_BA.
In I the block order is D first, then A (D = small site indices, A = wrapped ones).
"""
import numpy as np


def build(L=128, a=2.0, Lg=1.0, alpha=3.0, uv=(0.30, 0.42), cap=1e10):
    th = 2*np.pi*np.arange(L)/L
    thw = np.where(th > np.pi, th-2*np.pi, th)
    n = np.fft.fftfreq(L, d=1.0/L); nu = n + 0.5
    F = np.fft.fft(np.eye(L), axis=0)/L; Fi = np.fft.ifft(np.eye(L), axis=0)*L
    P = Fi@np.diag((nu > 0).astype(float))@F; P = 0.5*(P+P.conj().T)
    a1, a2 = uv; xx = (np.abs(nu)/L - a1)/(a2-a1)
    s_ = np.clip(1-xx, 0, 1); s_ = s_*s_*(3-2*s_)
    d = Fi@np.diag(1j*nu*s_)@F; d = 0.5*(d-d.conj().T)
    thD = 2*np.arctan(Lg); thA = -2*np.arctan(a)
    inD = (thw > 0) & (thw < thD); inA = (thw > thA) & (thw < 0); inI = inD | inA
    chi = np.zeros(L); chi[inD] = np.cos(thw[inD])-1.0
    t = thw.copy(); t[t < thA] += 2*np.pi; m = ~inI
    chi[m] = (np.cos(t[m])-1.0)*np.exp(-alpha*(t[m]-thD)**2)
    X = np.diag(chi); Dc = 0.5*(X@d + d@X); Dc = 0.5*(Dc - Dc.conj().T)
    I = np.where(inI)[0]; D = np.where(inD)[0]
    iD = np.searchsorted(I, D)                    # positions of D inside I
    iA = np.setdiff1d(np.arange(len(I)), iD)
    Q = P[np.ix_(I, I)]; Q = 0.5*(Q+Q.conj().T)
    q, U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1-1e-16)
    den = q[:, None]*(1-q)[None, :] + q[None, :]*(1-q)[:, None]
    w = np.minimum(1.0/den, cap)
    dc = (P@Dc - Dc@P)[np.ix_(I, I)]; dc = 0.5*(dc + dc.conj().T)   # E_I[P,D_chi]E_I
    return dict(L=L, a=a, Lg=Lg, uv=uv, alpha=alpha, cap=cap, I=I, D=D, iD=iD, iA=iA,
                nI=len(I), nD=len(D), nA=len(I)-len(D), Q=Q, q=q, U=U, w=w, den=den,
                dc=dc, QDD=Q[np.ix_(iD, iD)], QDA=Q[np.ix_(iD, iA)], P=P, Dchi=Dc)


def gQ(S, delta):
    """g_Q(delta) = (1/4) sum w |delta~|^2 for Hermitian delta on I."""
    dt = S['U'].conj().T@delta@S['U']
    return 0.25*float(np.sum(S['w']*np.abs(dt)**2))


def sld(S, delta):
    """t = (1/2) U (w o delta~) U^H ; then g_Q(delta) = (1/4) Tr(t delta)."""
    U = S['U']; dt = U.conj().T@delta@U
    t = 0.5*(U@(S['w']*dt)@U.conj().T)
    return 0.5*(t + t.conj().T)


def rot(S, G):
    """delta_rot = E_I[G,P]E_I = [G,Q] for G anti-Hermitian, supported on D (|D|x|D|)."""
    Gf = np.zeros((S['nI'], S['nI']), complex); Gf[np.ix_(S['iD'], S['iD'])] = G
    C = Gf@S['Q'] - S['Q']@Gf
    return 0.5*(C + C.conj().T)


def noise(S, N1, Y1):
    """the first-order noise block structure (in units of s)."""
    iD, iA, nI = S['iD'], S['iA'], S['nI']
    nz = np.zeros((nI, nI), complex)
    nz[np.ix_(iD, iD)] = 0.5*(N1@S['QDD'] + S['QDD']@N1) - Y1
    B = 0.5*N1@S['QDA']
    nz[np.ix_(iD, iA)] = B; nz[np.ix_(iA, iD)] = B.conj().T
    return 0.5*(nz + nz.conj().T)


def theta_cg(S, iters=300, tol=1e-15):
    """S10's theta = sup_G cos^2(u, v_G) by CG on A(G)=antiherm(E_D v_G E_D).
    Equivalent form used here: min_G g_Q(dc + [G,Q]) = (1 - theta) g_Q(dc)."""
    iD = S['iD']
    def Phi(G):  return rot(S, G)
    def PhiT(Y):                              # adjoint of G -> [G,Q]: antiherm E_D(YQ-QY)E_D
        C = Y@S['Q'] - S['Q']@Y
        R = C[np.ix_(iD, iD)]; return 0.5*(R - R.conj().T)
    W = lambda Y: S['U']@(S['w']*(S['U'].conj().T@Y@S['U']))@S['U'].conj().T
    ip = lambda A, B: float(np.real(np.vdot(A, B)))
    Aop = lambda G: 0.5*PhiT(W(Phi(G)))       # g_Q(Phi G) = (1/2)<G, A G>
    beta = -0.5*PhiT(W(S['dc']))              # f(G) = g0 - <beta,G> + (1/2)<G,A G>
    g0 = gQ(S, S['dc'])
    x = np.zeros_like(beta); r = beta.copy(); p = r.copy(); rs = ip(r, r); nb = np.sqrt(rs)
    for k in range(iters):
        Ap = Aop(p); pAp = ip(p, Ap)
        if pAp <= 1e-300: break
        al = rs/pAp; x = x + al*p; r = r - al*Ap
        rs2 = ip(r, r); p = r + (rs2/rs)*p; rs = rs2
        if np.sqrt(rs2) < tol*nb: break
    theta = 0.5*ip(beta, x)/g0                # min f = g0 - (1/2)<beta, A^{-1} beta>
    dstar = S['dc'] + Phi(x)
    return theta, x, dstar, g0, k+1
