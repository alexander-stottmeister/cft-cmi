import mpmath as mp
mp.mp.dps=25
# integrand of iint |D|^2/N in (u,v):  (1/2) du dv * F(u,v)
def F(u,v):
    return (mp.sinh(u/2)**2/(mp.cosh(u/2)*(mp.cosh(v/2)+mp.cosh(u/2))))*v**2/(u**2*(u**2+4*mp.pi**2)**2)
def Vfull(u): return 2*u*(u**2+4*mp.pi**2)/(3*mp.sinh(u/2))
pref=lambda u: mp.sinh(u/2)**2/(mp.cosh(u/2)*u**2*(u**2+4*mp.pi**2)**2)
def tail_v(u,V0):   # int_{|v|>V0} v^2/(cosh(v/2)+cosh(u/2)) dv
    if V0<=0: return Vfull(u)
    return 2*mp.quad(lambda v: v**2/(mp.cosh(v/2)+mp.cosh(u/2)),[V0,V0+10,V0+40,mp.inf])
print("Lam   exact tail 2*iint_{Bc}|D|^2/N     2/(3L^2)      ratio    piece{|v|>L,|u|<=L}   L^-4 scaled")
for Lam in [10,20,40,80,160]:
    L=mp.mpf(Lam)
    # region |u|+|v| > 2L :  for |u|<2L, |v|>2L-|u| ; for |u|>=2L all v
    I1=2*mp.quad(lambda u: pref(u)*tail_v(u,2*L-u),[mp.mpf('1e-12'),L/2,L,3*L/2,2*L])   # u in (0,2L), doubled for u<0
    I2=2*mp.quad(lambda u: pref(u)*Vfull(u),[2*L,3*L,mp.inf])
    tot=2*mp.mpf('0.5')*(I1+I2)      # 2 * (1/2 du dv)
    # piece |v|>L, |u|<=L
    J=2*mp.quad(lambda u: pref(u)*tail_v(u,L),[mp.mpf('1e-12'),L/2,L])
    piece=2*mp.mpf('0.5')*J
    print(f"{Lam:4d}  {mp.nstr(tot,8):>20}  {mp.nstr(2/(3*L**2),8):>12}  {mp.nstr(tot/(2/(3*L**2)),5):>8}  {mp.nstr(piece,6):>14}  {mp.nstr(piece*L**4,6)}")
print()
print("check literal step <1>5:  2*iint_{|v|>Lam, all u} |D|^2/N   vs  C*L^2 exp(-L/2)")
for Lam in [10,20,40]:
    L=mp.mpf(Lam)
    J=2*mp.quad(lambda u: pref(u)*tail_v(u,L),[mp.mpf('1e-12'),L/2,L,2*L,4*L,mp.inf])
    val=2*mp.mpf('0.5')*J
    print(f"  L={Lam}: value={mp.nstr(val,6)}   L^2 e^(-L/2)={mp.nstr(L**2*mp.e**(-L/2),6)}   1/(6L^2)={mp.nstr(1/(6*L**2),6)}")
