# REF-DEP-CFT-B9: one smoothly truncated Blaschke winding u = e^{i theta}, u = 1 outside [a-2R, a+2R].
# P_+ = positive frequencies (ghat(z) = int g e^{-ixz} dx, g = u - 1).
# ||P_- M_u P_+||_2^2 = (1/4pi^2) int_{z<0} |z| |ghat|^2 ,  ||P_+ M_u P_-||_2^2 = (1/4pi^2) int_{z>0} z |ghat|^2.
import numpy as np
def smoothstep(t):
    t=np.clip(t,0,1); f=lambda s: np.where(s>0,np.exp(-1/np.maximum(s,1e-300)),0.0)
    return f(t)/(f(t)+f(1-t))
def run(R,b=1.0,a=0.0,Lbox=4000.0,n=2**22):
    x=np.linspace(-Lbox/2,Lbox/2,n,endpoint=False); dx=x[1]-x[0]
    th=np.unwrap(np.angle((x-a-1j*b)/(x-a+1j*b)))
    th=th-th[0]                                    # 0 at -inf side ... 2pi at +inf side (approx)
    # force exactly 0 left of a-2R and 2pi right of a+2R, blending on [a-2R,a-R] and [a+R,a+2R]
    wl=smoothstep((x-(a-2*R))/R); wr=smoothstep((x-(a+R))/R)
    thc=np.where(x<a, wl*th, (1-wr)*th+wr*2*np.pi)
    g=np.exp(1j*thc)-1
    gh=np.fft.fft(g)*dx; z=2*np.pi*np.fft.fftfreq(n,d=dx); dz=2*np.pi/(n*dx)
    Pm=np.sum(np.abs(z[z<0])*np.abs(gh[z<0])**2)*dz/(4*np.pi**2)
    Pp=np.sum(z[z>0]*np.abs(gh[z>0])**2)*dz/(4*np.pi**2)
    return Pm,Pp
for R in [5,20,80]:
    Pm,Pp=run(R)
    print(f'R/b={R}: ||P_- M_u P_+||_2^2 = {Pm:.5f}, ||P_+ M_u P_-||_2^2 = {Pp:.5f}, difference = {Pp-Pm:.5f}')
