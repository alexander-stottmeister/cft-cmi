import numpy as np, boson_recovery as B
T0=B.T0; M=lambda k: np.where(np.abs(k)<1e-12,1.0,np.pi*k/np.tanh(np.pi*k))
X=80.0; NG=2**19; h=2*X/NG; t=-X+h*np.arange(NG); kk=2*np.pi*np.fft.fftfreq(NG,d=h)
def VF(f,g=None):
    F=np.fft.fft(f)*h; G=F if g is None else np.fft.fft(g)*h
    return float(np.sum(M(kk)*np.conj(F)*G).real*(2*np.pi/(2*X))/(8*np.pi**3))
g5=lambda x,c,w: np.exp(-(x-c)**2/(2*w*w))
# coarse grid for the position-space double integrals
hp=0.004; up=np.arange(-9,T0,hp)+hp/2; vp=np.arange(T0,9,hp)+hp/2
Kp=1.0/(4*np.sinh((up[:,None]-vp[None,:])/2)**2)
# (1) disjoint bumps
f=g5(t,-3,0.5); g=g5(t,3,0.5)
Vp=-hp*hp/(4*np.pi**2)*float(g5(up,-3,0.5)@Kp@g5(vp,3,0.5))
print(f"(1) disjoint bumps: V_fourier={VF(f,g):.8e}  V_position={Vp:.8e}  rel={abs(VF(f,g)/Vp-1):.2e}")
# (2) Hermite matrix vs direct Fourier / position
b=B.Basis(12,1.6); rng=np.random.default_rng(0); a1=rng.normal(size=12); a2=rng.normal(size=12)
Ph=B.herm(12,(t-b.tc)/b.sig)/np.sqrt(b.sig); F1=Ph.T@a1; F2=Ph.T@a2
print(f"(2) Hermite V : matrix={a1@b.V@a2:.8e}  fourier={VF(F1,F2):.8e}")
print(f"    Hermite Om: matrix={a1@b.Om@a2:.8e}  position={1/(4*np.pi)*h*np.sum(F1*np.gradient(F2,h)):.8e}")
# (3) Moebius invariance for f supported in D
s=0.3; tmax=np.log((2/(1+s)+1)/(2-2/(1+s))); m=(t>T0)&(t<tmax)
fd=g5(t,2.0,0.6)*(t>T0); Fb=np.zeros_like(t); Fb[m]=g5(B.beta(t[m],s),2.0,0.6)
print(f"(3) Moebius : V(f)={VF(fd):.8e} V(f o beta)={VF(Fb):.8e} rel={abs(VF(Fb)/VF(fd)-1):.2e}")
# (4) full DeltaV on f = bump_A + bump_D
fa=g5(t,-2.0,0.6)*(t<T0); ftot=fa+fd
Ftot=np.zeros_like(t); Ftot[t<T0]=fa[t<T0]; Ftot[m]=Fb[m]
dv_num=VF(Ftot)-VF(ftot)
Gv=-g5(vp,2.0,0.6); mm=vp<tmax; Gv[mm]+=g5(B.beta(vp[mm],s),2.0,0.6)
dv_loc=-2*hp*hp/(4*np.pi**2)*float(g5(up,-2.0,0.6)@Kp@Gv)
print(f"(4) DeltaV  : direct={dv_num:.8e}  localised={dv_loc:.8e}  rel={abs(dv_loc/dv_num-1):.2e}")
