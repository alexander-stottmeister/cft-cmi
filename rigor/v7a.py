import mpmath as mp
mp.mp.dps=30
print("== L5.2 v-integral, independent quad vs closed form 2a(a^2+pi^2)/(3 sinh a) ==")
for a in ['0.3','1.7','5','0.01','12']:
    a=mp.mpf(a)
    q=mp.quad(lambda w: w**2/(mp.cosh(w)+mp.cosh(a)),[-mp.inf,-1,0,1,mp.inf])
    cf=2*a*(a**2+mp.pi**2)/(3*mp.sinh(a))
    print(f"  a={a}: quad={mp.nstr(q,25)} closed={mp.nstr(cf,25)} rel.err={mp.nstr(abs(q-cf)/cf,3)}")
print("== V(u) = 2u(u^2+4pi^2)/(3 sinh(u/2)) ==")
for u in ['0.5','3','9']:
    u=mp.mpf(u)
    q=mp.quad(lambda v: v**2/(mp.cosh(v/2)+mp.cosh(u/2)),[-mp.inf,-1,0,1,mp.inf])
    cf=2*u*(u**2+4*mp.pi**2)/(3*mp.sinh(u/2))
    print(f"  u={u}: {mp.nstr(q,25)} vs {mp.nstr(cf,25)} rel={mp.nstr(abs(q-cf)/cf,3)}")
print("== L5.3 u-integrals ==")
J1=mp.quad(lambda u: mp.tanh(u/2)/(u*(u**2+4*mp.pi**2)),[-mp.inf,-1,0,1,mp.inf])
J2=mp.quad(lambda u: mp.tanh(u/4)/(u*(u**2+4*mp.pi**2)),[-mp.inf,-1,0,1,mp.inf])
print("  J1=",mp.nstr(J1,25)," 1/pi^2=",mp.nstr(1/mp.pi**2,25))
print("  J2=",mp.nstr(J2,25)," log2/pi^2=",mp.nstr(mp.log(2)/mp.pi**2,25))
print("== 2D: gB=2*iint|D|^2/N, h2=(1/2)iint|D|^2/W  (kappa,kappa' plane, mpmath) ==")
def D1(k,kp):
    u=k-kp; v=k+kp
    q=1/(1+mp.e**k); qp=1/(1+mp.e**kp)
    if abs(u)<mp.mpf('1e-12'):
        return -k*q*(1-q)/(2*mp.pi**2)
    return (q-qp)*v/(u*(u**2+4*mp.pi**2))
def NN(k,kp):
    q=1/(1+mp.e**k); qp=1/(1+mp.e**kp); return q*(1-qp)+qp*(1-q)
def WW(k,kp):
    q=1/(1+mp.e**k); qp=1/(1+mp.e**kp); return (mp.sqrt(q*(1-qp))+mp.sqrt(qp*(1-q)))**2
mp.mp.dps=20
gB=2*mp.quad(lambda k: mp.quad(lambda kp: D1(k,kp)**2/NN(k,kp),[-40,k,40]),[-40,0,40])
h2=mp.mpf(1)/2*mp.quad(lambda k: mp.quad(lambda kp: D1(k,kp)**2/WW(k,kp),[-40,k,40]),[-40,0,40])
print("  gB=",mp.nstr(gB,15)," 2/(3pi^2)=",mp.nstr(2/(3*mp.pi**2),15))
print("  gB/8=",mp.nstr(gB/8,15)," 1/(12pi^2)=",mp.nstr(1/(12*mp.pi**2),15))
print("  h2=",mp.nstr(h2,15)," log2/(6pi^2)=",mp.nstr(mp.log(2)/(6*mp.pi**2),15), " ratio h2/(gB/8)=",mp.nstr(h2/(gB/8),15)," 2log2=",mp.nstr(2*mp.log(2),15))
