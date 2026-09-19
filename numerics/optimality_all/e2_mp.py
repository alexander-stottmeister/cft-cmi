"""E2: high-precision (mpmath) recomputation of the key scalar
     R := ||M||^2 - ||Pi M||^2 - ||Proj_Ext M||^2 = dist((1-Pi)M, Ext)^2
at small L, to decide whether the double-precision values (+-1e-10, sign-changing) are
roundoff or a genuine defect.  Everything is built in closed form:
  P_jk = (1/L) sum_{n=0}^{L/2-1} w^{n(j-k)},  w = exp(2 pi i / L)   (NS, nu = n+1/2 > 0)
  d_jk = (1/L) sum_n i nu_n s_n w^{n(j-k)}   (UV-tapered derivative, as in s10_theta)
Usage: e2_mp.py [L] [dps]
"""
import sys, mpmath as mp
L = int(sys.argv[1]) if len(sys.argv) > 1 else 32
mp.mp.dps = int(sys.argv[2]) if len(sys.argv) > 2 else 60
a, Lg, alpha = mp.mpf(2), mp.mpf(1), mp.mpf(3)
a1, a2 = mp.mpf('0.30'), mp.mpf('0.42')
w = mp.exp(2j*mp.pi/L)
ns = list(range(0, L//2)) + list(range(-L//2, 0))          # fftfreq order
nus = [mp.mpf(n)+mp.mpf('0.5') for n in ns]
def sm(x):
    x = min(max(x, mp.mpf(0)), mp.mpf(1)); return x*x*(3-2*x)
sfac = [sm(1-(abs(nu)/L-a1)/(a2-a1)) for nu in nus]
P = mp.zeros(L, L); dd = mp.zeros(L, L)
for j in range(L):
    for k in range(L):
        D = (j-k) % L
        P[j, k] = mp.fsum([w**((n*D) % L) for n in range(L//2)])/L
        dd[j, k] = mp.fsum([1j*nus[i]*sfac[i]*w**((ns[i]*D) % L) for i in range(L)])/L
P = (P+P.H)/2; dd = (dd-dd.H)/2
thD = 2*mp.atan(Lg); thA = -2*mp.atan(a)
th = [2*mp.pi*j/L for j in range(L)]
thw = [t-2*mp.pi if t > mp.pi else t for t in th]
inD = [0 < t < thD for t in thw]; inA = [thA < t < 0 for t in thw]
inI = [x or y for x, y in zip(inD, inA)]
chi = []
for j, t in enumerate(thw):
    if inD[j]: chi.append(mp.cos(t)-1)
    elif inI[j]: chi.append(mp.mpf(0))
    else:
        tt = t+2*mp.pi if t < thA else t
        chi.append((mp.cos(tt)-1)*mp.exp(-alpha*(tt-thD)**2))
Dc = mp.zeros(L, L)
for j in range(L):
    for k in range(L): Dc[j, k] = (chi[j]*dd[j, k]+dd[j, k]*chi[k])/2
Dc = (Dc-Dc.H)/2
Pp = mp.eye(L)-P
M = Pp*Dc*P
I = [j for j in range(L) if inI[j]]; Ic = [j for j in range(L) if not inI[j]]
def sub(A, R, C): 
    B = mp.zeros(len(R), len(C))
    for i, r in enumerate(R):
        for j, c in enumerate(C): B[i, j] = A[r, c]
    return B
def quad(A, idx, herm):
    B = sub(A+A.H if herm else A-A.H, idx, idx)
    Q = sub(P, idx, idx); Q = (Q+Q.H)/2
    q, U = mp.eighe(Q)
    E = U.H*B*U
    tot = mp.mpf(0); leak = mp.mpf(0); dmin = mp.mpf(1)
    for i in range(len(idx)):
        for j in range(len(idx)):
            den = q[i]*(1-q[j])+q[j]*(1-q[i])
            v = abs(E[i, j])**2
            if den > mp.mpf(10)**(-mp.mp.dps+10): tot += v/den; dmin = min(dmin, den)
            else: leak += v
    return tot/2, leak, dmin
n2 = mp.fsum([abs(M[j, k])**2 for j in range(L) for k in range(L)])
pi2, lkN, dN = quad(M, I, True)
ex2, lkE, dE = quad(M, Ic, False)
R = n2-pi2-ex2
print(f"L={L} dps={mp.mp.dps} |I|={len(I)} |Ic|={len(Ic)}")
print(f"  ||M||^2          = {mp.nstr(n2,20)}")
print(f"  ||Pi M||^2       = {mp.nstr(pi2,20)}   leak={mp.nstr(lkN,5)} den_min={mp.nstr(dN,5)}")
print(f"  ||Proj_Ext M||^2 = {mp.nstr(ex2,20)}   leak={mp.nstr(lkE,5)} den_min={mp.nstr(dE,5)}")
print(f"  R = dist((1-Pi)M,Ext)^2 = {mp.nstr(R,10)}   R/||(1-Pi)M||^2 = {mp.nstr(R/(n2-pi2),10)}")
print(f"  rel. distance = {mp.nstr(mp.sqrt(abs(R)/(n2-pi2)),8)}  (sign of R: {mp.sign(R)})")
