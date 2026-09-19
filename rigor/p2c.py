import mpmath as mp
mp.mp.dps=30
def chk(k,kp):
    q=1/(1+mp.e**k); qp=1/(1+mp.e**kp); u=k-kp; v=k+kp
    N=q*(1-qp)+qp*(1-q); W=(mp.sqrt(q*(1-qp))+mp.sqrt(qp*(1-q)))**2
    return [N-mp.cosh(u/2)/(mp.cosh(v/2)+mp.cosh(u/2)),
            W-(1+mp.cosh(u/2))/(mp.cosh(v/2)+mp.cosh(u/2)),
            (q-qp)**2-mp.sinh(u/2)**2/(mp.cosh(v/2)+mp.cosh(u/2))**2,
            (q-qp)**2/N-mp.sinh(u/2)**2/(mp.cosh(u/2)*(mp.cosh(v/2)+mp.cosh(u/2))),
            (q-qp)**2/W-mp.sinh(u/2)**2/((1+mp.cosh(u/2))*(mp.cosh(v/2)+mp.cosh(u/2)))]
for k,kp in [(mp.mpf('0.7'),mp.mpf('-2.3')),(mp.mpf('5'),mp.mpf('9')),(mp.mpf('-11'),mp.mpf('3'))]:
    print(k,kp,[mp.nstr(x,3) for x in chk(k,kp)])
# closed-form reduction of g_B and Psi_2 to 1D
f=lambda u: mp.sinh(u/2)**2/mp.cosh(u/2)/(u**2*(u**2+4*mp.pi**2)**2)*(2*u*(u**2+4*mp.pi**2)/(3*mp.sinh(u/2)))
g=lambda u: mp.sinh(u/2)**2/(1+mp.cosh(u/2))/(u**2*(u**2+4*mp.pi**2)**2)*(2*u*(u**2+4*mp.pi**2)/(3*mp.sinh(u/2)))
gB=2*mp.mpf('0.5')*mp.quad(f,[-mp.inf,-1,0,1,mp.inf])   # 2 * (1/2) int du [ ... ]
Ps=mp.mpf('0.5')*mp.mpf('0.5')*mp.quad(g,[-mp.inf,-1,0,1,mp.inf])
print("g_B =",gB," 2/(3pi^2)=",2/(3*mp.pi**2))
print("Psi2=",Ps," log2/(6pi^2)=",mp.log(2)/(6*mp.pi**2))
