"""F3 T3: restrict the admissible G class in the modular coordinate xi of AD.
(i)  support window:  G supported on {xi0 <= xi <= xi0+W} inside D
(ii) bandwidth:       G in the span of modular Fourier modes |kappa| <= K on the D window
Both are frame-independent continuum classes, so the two discretisations can be matched."""
import sys, time, numpy as np
sys.path.insert(0,'/Users/alex/Documents/Uni/Hannover/claude-team/cft_cmi/numerics/optimality_all')
import f3_gal as G
f2 = 1.0/(12*np.pi**2)

def xi_of(x, a, L): return np.log((x+a)/(L-x))

def gal_setup(a=1.0, L=2.0, s=0.1, h=0.08, Lam=12, kind='first'):
    edges,nA,nB,nC,Q,Dc = G.setup(a,L,s,h,Lam,kind,uni=True)
    ctr = 0.5*(edges[:-1]+edges[1:]); xi0 = np.log(a/L)
    return dict(edges=edges,nA=nA,Q=Q,Dc=Dc,ctr=ctr[nA:],xi0=xi0,h=h,
                zeta=a*s/(a+L),N=len(Q),m=len(Q)-nA)

def Bsupport(S, W):
    sel = np.where(S['ctr'] - S['xi0'] <= W)[0]
    B = np.zeros((S['m'], len(sel))); B[sel, np.arange(len(sel))] = 1.0
    return B, len(sel)

def Bband(S, K, W=None):
    """orthonormal modular Fourier modes |kappa|<=K on the window (weight = cell width)."""
    xi = S['ctr']; sel = np.arange(len(xi)) if W is None else np.where(xi-S['xi0']<=W)[0]
    xs = xi[sel]; Wlen = xs[-1]-xs[0]+S['h']
    kmax = int(np.floor(K*Wlen/(2*np.pi)))
    ks = np.arange(-kmax, kmax+1); kap = 2*np.pi*ks/Wlen
    M = np.exp(1j*np.outer(xs, kap))
    Bf = np.zeros((S['m'], len(ks)), complex); Bf[sel,:] = M
    Bq,_ = np.linalg.qr(Bf)
    return Bq, len(ks), kmax

def run_gal(S, B=None, lab=''):
    t0=time.time(); th,g0,k,hist,x = G.theta(S['Q'], S['Dc'], S['nA'], B=B, iters=8000)
    r = S['m'] if B is None else B.shape[1]
    print(f"  GAL h={S['h']} {lab} r={r} theta={th:.5f} gQ/(f2z^2)={g0/(f2*S['zeta']**2):.5f} "
          f"cg={k} {time.time()-t0:.0f}s", flush=True)
    return th

if __name__=='__main__':
    job = sys.argv[1] if len(sys.argv)>1 else 'win'
    if job=='win':
        for h in (0.12, 0.06):
            S = gal_setup(h=h)
            print(f"# D window in xi: [xi0, xi0+{S['ctr'][-1]-S['xi0']:.2f}]  m={S['m']}",flush=True)
            for W in (1.5,2.5,3.5,4.5,5.5,7.0,9.0,12.0,99.0):
                B,r = Bsupport(S,W); run_gal(S,B,f"W={W}")
    elif job=='band':
        for h in (0.12, 0.06):
            S = gal_setup(h=h)
            for K in (1.0,2.0,4.0,8.0,16.0,32.0,1e9):
                if K>1e8: run_gal(S,None,"K=inf"); continue
                B,r,km = Bband(S,K); run_gal(S,B,f"K={K} kmax={km}")
    elif job=='bandwin':
        S = gal_setup(h=0.06)
        for W in (4.5, 9.0, 15.4):
            for K in (1.0,2.0,4.0,8.0,16.0):
                B,r,km = Bband(S,K,W=W); run_gal(S,B,f"W={W} K={K}")
