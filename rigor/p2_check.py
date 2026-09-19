import numpy as np, scipy.linalg as sla
from scipy.integrate import quad, dblquad
import mpmath as mp
mp.mp.dps=30

print("== 1. integrals ==")
I1 = mp.quad(lambda u: mp.tanh(u/2)/(u*(u**2+4*mp.pi**2)), [-mp.inf,-1,0,1,mp.inf])
print("int tanh(u/2)/(u(u^2+4pi^2)) =", I1, " 1/pi^2 =", 1/mp.pi**2)
gB = mp.mpf(2)/3*I1; print("g_B =", gB, " 2/(3pi^2)=",2/(3*mp.pi**2), " f2=g_B/8=",gB/8, " 1/(12pi^2)=",1/(12*mp.pi**2))
I2 = mp.quad(lambda u: mp.tanh(u/4)/(u*(u**2+4*mp.pi**2)), [-mp.inf,-1,0,1,mp.inf])
print("int tanh(u/4)/(u(u^2+4pi^2)) =", I2, " log2/pi^2 =", mp.log(2)/mp.pi**2)
Psi2 = I2/6; print("Psi_2 =", Psi2, " log2/(6pi^2)=", mp.log(2)/(6*mp.pi**2), " ratio to f2 =", Psi2/(gB/8), " 2log2=",2*mp.log(2))

print("\n== 2. V(u) identity ==")
for a in [0.3, 1.7, 5.0]:
    num = mp.quad(lambda v: v**2/(mp.cosh(v/2)+mp.cosh(a/2)), [-mp.inf,0,mp.inf])
    print(f"  u={a}: quad={num}, closed={2*a*(a**2+4*mp.pi**2)/(3*mp.sinh(a/2))}")

print("\n== 3. direct 2D quadrature of g_B and Psi_2 from D1 kernel ==")
def D1(k,kp):
    u=k-kp; v=k+kp
    if abs(u)<1e-9: return -k/(8*np.pi**2*np.cosh(k/2)**2)
    q=1/(1+np.exp(k)); qp=1/(1+np.exp(kp))
    return (q-qp)*v/(u*(u**2+4*np.pi**2))
def Nw(k,kp):
    q=1/(1+np.exp(k)); qp=1/(1+np.exp(kp)); return q*(1-qp)+qp*(1-q)
def Ww(k,kp):
    q=1/(1+np.exp(k)); qp=1/(1+np.exp(kp)); return (np.sqrt(q*(1-qp))+np.sqrt(qp*(1-q)))**2
from numpy.polynomial.legendre import leggauss
X,Wq = leggauss(400); Lm=80.0; X=X*Lm; Wq=Wq*Lm
gBnum=0.0; Ps=0.0
for i,k in enumerate(X):
    d=np.array([D1(k,kp) for kp in X]); n=np.array([Nw(k,kp) for kp in X]); w=np.array([Ww(k,kp) for kp in X])
    gBnum += Wq[i]*np.sum(Wq*d**2/n); Ps += Wq[i]*np.sum(Wq*d**2/w)
print("  2*int|D|^2/N =", 2*gBnum, "  vs 2/(3pi^2) =", 2/(3*np.pi**2))
print("  (1/2)int|D|^2/W =", 0.5*Ps, "  vs log2/(6pi^2) =", np.log(2)/(6*np.pi**2))
