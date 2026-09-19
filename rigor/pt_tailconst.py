import mpmath as mp
mp.mp.dps=30
def g_ge2(t,z):
    # int_0^1 Fge2(t s, t(1-s)) ds ; Fge2 = -2 z^2 A^2/(B^2 (B+2 z A)), A=sinh(ts/2)sinh(t(1-s)/2), B=sinh(t/2)
    if t==0: return mp.mpf(0)
    B=mp.sinh(t/2)
    f=lambda s:(lambda A: -2*z**2*A**2/(B**2*(B+2*z*A)))(mp.sinh(t*s/2)*mp.sinh(t*(1-s)/2))
    return mp.quad(f,[0,mp.mpf(1)/2,1])
def g1(t):
    if t==0: return mp.mpf(1)/6
    return (t*mp.cosh(t/2)-2*mp.sinh(t/2))/(2*t*mp.sinh(t/2)**2)
# (i) check g'(0) = -z^2/30 and g_ge2 ~ -z^2 t/30
for z in [mp.mpf('0.1'),mp.mpf('1')]:
    h=mp.mpf('1e-6'); print('z=%s  g2p(0)=%s   -z^2/30=%s'%(z, mp.nstr(g_ge2(h,z)/h,8), mp.nstr(-z**2/30,8)))
# (ii) A3 = sup_z z^-2 || d^3/dt^3 g_ge2 ||_L1(0,inf)
def d3(t,z):
    h=mp.mpf('1e-3')
    return (g_ge2(t+2*h,z)-2*g_ge2(t+h,z)+2*g_ge2(t-h,z)-g_ge2(t-2*h,z))/(2*h**3)
for z in ['0.05','0.2','0.5','1.0']:
    z=mp.mpf(z)
    ts=[mp.mpf(x)/20 for x in range(1,20)]+[1+mp.mpf(x)/4 for x in range(0,40)]+[11+mp.mpf(x) for x in range(0,30)]
    tot=mp.mpf(0)
    prev=None
    for t in ts:
        v=abs(d3(t,z))
        if prev is not None: tot+= (v+prev[1])/2*(t-prev[0])
        prev=(t,v)
    print('z=%-5s  ||g2\'\'\'||_1 = %s   /z^2 = %s'%(z, mp.nstr(tot,6), mp.nstr(tot/z**2,6)))
