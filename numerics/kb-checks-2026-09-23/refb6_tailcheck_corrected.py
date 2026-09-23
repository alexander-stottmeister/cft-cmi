# REF-DEP-CFT-B6: eq:final of tail_bound.tex cor:rate with the corrected thm:main chain
# Phi - Phi_W <= Pd + Y/(1-Y), Y = e^{Phi_W} y <= e^{f z^2} y, y = 2 e^{2Pd} sqrt(Phi Pd)  (step <1>5 fixed).
# Same grid and inputs as tailcheck_ext.py in this folder.
import math
def T_exact(z,k): return 2*z*z/(3*k*k)+4.6*z*z/k**3+(12+0.51*z*(1+k))*math.exp(-k)
def chain(z,k,f,corr):
    T=T_exact(z,k); Pd=T/(2*(1-T)); y=2*math.exp(2*Pd)*math.sqrt(f*z*z*Pd)
    Y=y*math.exp(f*z*z) if corr else y
    return Pd+Y/(1-Y)
def claim(z,k): return 0.173*z*z/k+0.88*z*z/(k*k)
def adm(z,k): return k>=10 and k>=2*math.log(1/z)+2*math.log(1+k)+3
zs=sorted(set([i/2000 for i in range(1,2001)]+[10**(-e/10) for e in range(1,81)]))
ks=[10+j*0.02 for j in range(0,2001)]+[50+j*0.25 for j in range(1,601)]
for f in (0.0085,0.008516):
    for corr in (False,True):
        best=(0,None)
        for z in zs:
            for k in ks:
                if adm(z,k):
                    r=chain(z,k,f,corr)/claim(z,k)
                    if r>best[0]: best=(r,(z,round(k,2)))
        print(f'f={f} corrected={corr}: max chain/claim = {best[0]:.4f} at {best[1]}')
