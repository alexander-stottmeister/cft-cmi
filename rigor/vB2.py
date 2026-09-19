import numpy as np
def run(N,Lb,gam):
    dx=2*Lb/N; x=-Lb+dx*np.arange(N); dp=2*np.pi/(N*dx)
    p=np.fft.fftfreq(N,d=dx)*2*np.pi; sw=np.abs(p)**1.5
    u=x-1.0; pos=u>0
    def ft(f): return (np.fft.fft(f)*dx)*sw
    f=np.zeros(N); m=(x>0)&(x<=1); f[m]=-x[m]**2
    a=gam+2.0; f[pos]=-(1+a*u[pos])*np.exp(-gam*u[pos]); F0=ft(f)
    B=[]
    for k in (2,3,4):
        for al in (0.008,0.02,0.05,0.125,0.3,0.8,2.0,5.0,12.0):
            g=np.zeros(N); g[pos]=u[pos]**k*np.exp(-al*u[pos]); B.append(ft(g))
    for q in (2.1,2.3,2.6,3,3.5,4,5,6,8):
        g=np.zeros(N); g[pos]=u[pos]**2/(1+u[pos])**q; B.append(ft(g))
    A=np.array(B); sc=dp/(2*np.pi)
    nrm=np.sqrt(np.real(np.sum(np.abs(A)**2,axis=1))*sc); A=A/nrm[:,None]
    M=np.real(A@A.conj().T)*sc; bb=np.real(A@F0.conj())*sc; n0=np.real(F0@F0.conj())*sc
    c=np.linalg.lstsq(M,-bb,rcond=1e-9)[0]
    return n0, n0+2*c@bb+c@M@c
for N,Lb in ((1<<20,512.0),(1<<20,1024.0),(1<<20,2048.0)):
    for gam in (1.0,):
        n0,nm=run(N,Lb,gam)
        print(f"N={N} Lb={Lb} gam={gam}: |G0|^2={n0:.6f} min={nm:.6f} Q={nm/(48*np.pi):.8f}")
print("target: |G|^2=8/pi=",8/np.pi," Q=1/(6pi^2)=",1/(6*np.pi**2))
