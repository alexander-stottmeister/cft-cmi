"""S10: spectral (circle) test of the obstruction (S).
L^2(S^1) on an L-point grid; P = Hardy projection (Fourier modes 1..L/2-1);
E_S = exact diagonal projections; Dchi = (1/2)(chi d + d chi) with a smooth UV taper
on d so that the wrap-around (spurious) Fermi point is switched off.
u = Pi_N M solves S_Q(l) = -(1/2) ddelta,  u = P^perp l P.
Report: |u|^2 (should be extension independent), and the anti-hermitian part of E_D u E_D."""
import numpy as np

def run(L=512, thD=1.0, thA=2.0, alpha=3.0, cap=1e12, uvfrac=(0.30,0.42), verbose=True):
    th = 2*np.pi*np.arange(L)/L
    n  = np.fft.fftfreq(L, d=1.0/L)                      # integer modes
    F  = np.fft.fft(np.eye(L), axis=0)/L                 # theta -> modes  (rows = modes)
    Fi = np.fft.ifft(np.eye(L), axis=0)*L
    # Hardy projection: modes 1 .. L/2-1
    lam = ((n >= 1) & (n <= L/2-1)).astype(float)
    P  = (Fi @ np.diag(lam) @ F).real + 1j*(Fi @ np.diag(lam) @ F).imag
    P  = 0.5*(P+P.conj().T)
    Pp = np.eye(L)-P
    # UV-tapered spectral derivative
    a1,a2 = uvfrac; x = (np.abs(n)/L - a1)/(a2-a1)
    sig = np.clip(1-x,0,1); sig = sig*sig*(3-2*sig)      # smoothstep
    d  = Fi @ np.diag(1j*n*sig) @ F
    d  = 0.5*(d - d.conj().T)
    # geometry: D=(0,thD), A=(2pi-thA,2pi), I'=rest
    inD = (th > 0) & (th < thD)
    inA = (th > 2*np.pi-thA)
    inI = inD | inA
    chi = np.zeros(L)
    chi[inD] = -th[inD]**2
    m = (th >= thD) & (th <= 2*np.pi-thA)
    chi[m] = -th[m]**2*np.exp(-alpha*(th[m]-thD)**2)
    X = np.diag(chi)
    Dchi = 0.5*(X@d + d@X); Dchi = 0.5*(Dchi - Dchi.conj().T)
    M  = Pp@Dchi@P
    EI = np.diag(inI.astype(float))
    ddelta_full = EI@(P@Dchi - Dchi@P)@EI
    I = np.where(inI)[0]; D = np.where(inD)[0]
    dd = ddelta_full[np.ix_(I,I)]
    Q  = P[np.ix_(I,I)]; Q = 0.5*(Q+Q.conj().T)
    q,U = np.linalg.eigh(Q); q = np.clip(q, 1e-300, 1-1e-16)
    den = q[:,None]*(1-q)[None,:] + q[None,:]*(1-q)[:,None]
    w   = np.minimum(1.0/den, cap)
    l   = U@(w*(U.conj().T@(-0.5*dd)@U))@U.conj().T
    Lf  = np.zeros((L,L), complex); Lf[np.ix_(I,I)] = l
    u   = Pp@Lf@P
    R   = u[np.ix_(D,D)]; Ra = 0.5*(R-R.conj().T)
    nu2 = -0.25*np.real(np.trace(l@dd))
    out = dict(nu2=nu2, nu=np.sqrt(abs(nu2)), nM2=np.linalg.norm(M)**2,
               nR=np.linalg.norm(R), nRa=np.linalg.norm(Ra),
               ratio=np.linalg.norm(Ra)/np.linalg.norm(R),
               theta_lb=np.linalg.norm(Ra)**2/abs(nu2))
    if verbose:
        print(f" L={L:4d} a={alpha:4.1f} cap={cap:6.0e} |u|^2={out['nu2']:.6f} |M|^2={out['nM2']:.6f}"
              f" |R|={out['nR']:.5f} antiherm/|R|={out['ratio']:.5f} theta_lb={out['theta_lb']:.5f}")
    return out

if __name__ == "__main__":
    print("--- extension independence (alpha) and cap stability ---")
    for L in (256,384,512):
        for alpha in (2.0,3.0,5.0):
            run(L=L, alpha=alpha, cap=1e10)
        print()
    print("--- cap ladder ---")
    for cap in (1e3,1e5,1e7,1e9,1e11):
        run(L=384, alpha=3.0, cap=cap)
