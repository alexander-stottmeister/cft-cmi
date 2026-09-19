"""S10: Moebius-correct circle model (NS sector, half-integer modes).
Cayley: x = tan(theta/2); line Moebius field -x^2 d/dx  ->  chi(theta)=cos(theta)-1.
Line geometry A=(-a,0), D=(0,Lg), I'=rest  ->  thA=-2 arctan(a), thD=2 arctan(Lg).
Check: |u|^2 should equal 2 f2 zeta^2/s^2 = 2 f2 (a/(a+Lg))^2,  f2=1/(12 pi^2)."""
import numpy as np

def run(L=512, a=2.0, Lg=1.0, alpha=3.0, cap=1e10, uv=(0.30,0.42), pr=True):
    th = 2*np.pi*np.arange(L)/L                       # theta in [0,2pi)
    thw = np.where(th > np.pi, th-2*np.pi, th)        # theta in (-pi,pi]
    n = np.fft.fftfreq(L, d=1.0/L); nu = n + 0.5      # NS modes
    F = np.fft.fft(np.eye(L), axis=0)/L; Fi = np.fft.ifft(np.eye(L), axis=0)*L
    P = Fi@np.diag((nu > 0).astype(float))@F; P = 0.5*(P+P.conj().T); Pp = np.eye(L)-P
    a1,a2 = uv; xx = (np.abs(nu)/L - a1)/(a2-a1); s_ = np.clip(1-xx,0,1); s_ = s_*s_*(3-2*s_)
    d = Fi@np.diag(1j*nu*s_)@F; d = 0.5*(d-d.conj().T)
    thD = 2*np.arctan(Lg); thA = -2*np.arctan(a)
    inD = (thw > 0) & (thw < thD); inA = (thw > thA) & (thw < 0); inI = inD | inA
    chi = np.zeros(L)
    chi[inD] = np.cos(thw[inD]) - 1.0
    m = ~inI                                          # I' : theta in (thD, 2pi+thA)
    t = thw.copy(); t[t < thA] = t[t < thA] + 2*np.pi  # unwrap I' to (thD, 2pi+thA)
    chi[m] = (np.cos(t[m])-1.0)*np.exp(-alpha*(t[m]-thD)**2)
    X = np.diag(chi); Dc = 0.5*(X@d + d@X); Dc = 0.5*(Dc - Dc.conj().T)
    EI = np.diag(inI.astype(float))
    I = np.where(inI)[0]; D = np.where(inD)[0]
    dd = (EI@(P@Dc - Dc@P)@EI)[np.ix_(I,I)]
    Q = P[np.ix_(I,I)]; Q = 0.5*(Q+Q.conj().T)
    q,U = np.linalg.eigh(Q); q = np.clip(q,1e-300,1-1e-16)
    den = q[:,None]*(1-q)[None,:] + q[None,:]*(1-q)[:,None]
    w = np.minimum(1.0/den, cap)
    l = U@(w*(U.conj().T@(-0.5*dd)@U))@U.conj().T
    Lf = np.zeros((L,L),complex); Lf[np.ix_(I,I)] = l
    u = Pp@Lf@P; R = u[np.ix_(D,D)]; Ra = 0.5*(R-R.conj().T)
    nu2 = -0.25*np.real(np.trace(l@dd))
    pred = 2*(1/(12*np.pi**2))*(a/(a+Lg))**2
    if pr:
        print(f" L={L:4d} a={a:4.1f} Lg={Lg:4.1f} al={alpha:4.1f} cap={cap:6.0e} "
              f"|u|^2={nu2:.6f} pred={pred:.6f} ratio={nu2/pred:.4f} "
              f"antiherm/|R|={np.linalg.norm(Ra)/np.linalg.norm(R):.5f} "
              f"theta_lb={np.linalg.norm(Ra)**2/nu2:.5f}")
    return nu2, pred, np.linalg.norm(Ra)**2/nu2

if __name__=="__main__":
    print("--- convergence in L (Moebius field), a=2, Lg=1 ---")
    for L in (256,384,512,768):  run(L=L)
    print("--- extension independence ---")
    for al in (1.5,3.0,6.0):     run(L=512, alpha=al)
    print("--- other geometries ---")
    for (a,Lg) in [(1.0,1.0),(4.0,1.0),(2.0,0.5),(8.0,1.0)]: run(L=512, a=a, Lg=Lg)
    print("--- cap ladder ---")
    for cap in (1e4,1e6,1e8,1e10,1e12): run(L=512, cap=cap)
