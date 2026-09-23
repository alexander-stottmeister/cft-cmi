# Provenance: written by referee REF-DEP-CFT-B1 (2026-09-23), stored by AUTH-CFT-B. Run: /usr/bin/python3 hypU_m2.py (needs numpy).
# M_2 check of Hypothesis (U): standard form (HS space, left mult., J x = x^*, P = {x >= 0}).
import numpy as np

def psd_sqrt(r):
    w,v = np.linalg.eigh(r); w = np.clip(w,0,None); return (v*np.sqrt(w))@v.conj().T
def cone_rep(rho):  # xi in P with <xi, a xi> = Tr(rho a): xi = rho^{1/2}
    return psd_sqrt(rho)
def fid(rho,sig):   # F = sqrt(P_tr) = Tr|rho^{1/2} sig^{1/2}| (Uhlmann/Alberti-Uhlmann root fidelity)
    return np.linalg.svd(psd_sqrt(rho)@psd_sqrt(sig),compute_uv=False).sum()
def inner(x,y): return np.trace(x.conj().T@y)
# check the representative really represents the state
rng=np.random.default_rng(1)
a=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); A=a@a.conj().T
# (1) pure states |0>, |+>
k0=np.array([1,0]); kp=np.array([1,1])/np.sqrt(2)
r=np.outer(k0,k0.conj()); s=np.outer(kp,kp.conj())
xi,eta=cone_rep(r),cone_rep(s)
print("pure: state check", np.allclose(np.trace(xi.conj().T@A@xi), np.trace(r@A)))
print("pure: <xi,eta> =", inner(xi,eta).real, " F =", fid(r,s), " F^2 =", fid(r,s)**2)
# (2) faithful, non-commuting
r=np.array([[0.9,0],[0,0.1]]); s=0.5*np.eye(2)+0.4*np.array([[0,1],[1,0]])
xi,eta=cone_rep(r),cone_rep(s)
print("faithful: <xi,eta> =", inner(xi,eta).real, " F =", fid(r,s), " F^2 =", fid(r,s)**2)
# (3) random pairs: F^2 <= <xi,eta> <= F
worst=0
for _ in range(20000):
    x=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); r=x@x.conj().T; r/=np.trace(r).real
    y=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); s=y@y.conj().T; s/=np.trace(s).real
    A_=inner(cone_rep(r),cone_rep(s)).real; F=fid(r,s)
    assert F**2-1e-12<=A_<=F+1e-12
    worst=max(worst,F-A_)
print("random: F^2 <= <xi,eta> <= F on 20000 pairs; max(F-<xi,eta>) =",worst)
