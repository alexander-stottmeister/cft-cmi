# REF-DEP-CFT-B10: unrounded maxima of refb6_tailcheck_corrected.py and the sup on the continuum admissible region
import math
def T_exact(z,k): return 2*z*z/(3*k*k)+4.6*z*z/k**3+(12+0.51*z*(1+k))*math.exp(-k)
def chain(z,k,f,corr):
    T=T_exact(z,k); Pd=T/(2*(1-T)); y=2*math.exp(2*Pd)*math.sqrt(f*z*z*Pd)
    Y=y*math.exp(f*z*z) if corr else y
    return Pd+Y/(1-Y)
def claim(z,k): return 0.173*z*z/k+0.88*z*z/(k*k)
def r(z,k,f,c): return chain(z,k,f,c)/claim(z,k)
def zmin(k): return (1+k)*math.exp((3-k)/2)   # boundary of k >= 2log(1/z)+2log(1+k)+3
print('z_min(10) =', repr(zmin(10.0)))
for f in (0.0085,0.008516):
    for c in (False,True):
        g=r(0.3325,10.0,f,c)
        # continuum: along k=10 for z in [zmin(10),1] and along boundary curve z=zmin(k), k>=10 (z<=1)
        best=(0,None)
        z0=zmin(10.0)
        for i in range(0,200001):
            z=z0+(1-z0)*i/200000
            v=r(z,10.0,f,c)
            if v>best[0]: best=(v,(z,10.0))
        for j in range(0,200001):
            k=10+j*1e-4
            z=zmin(k)
            if z<=1:
                v=r(z,k,f,c)
                if v>best[0]: best=(v,(z,k))
        print(f'f={f} corrected={c}: grid point (0.3325,10) ratio = {g:.7f};  continuum sup ~ {best[0]:.7f} at z={best[1][0]:.7f}, k={best[1][1]:.4f}')
# local 2D scan near the corner (k in [10,10.5], z in [zmin(k), zmin(k)+0.02]) and admissibility check of the corner
for f in (0.0085,0.008516):
    best=(0,None)
    for j in range(0,501):
        k=10+j*0.001
        z0=max(zmin(k),1e-12)
        for i in range(0,401):
            z=z0+0.02*i/400
            v=r(z,k,f,True)
            if v>best[0]: best=(v,(z,k))
    print(f'local 2D scan corrected f={f}: max {best[0]:.7f} at {best[1]}')
zc=11*math.exp(-3.5); k=10.0
print('corner admissible:', k>=10 and k>=2*math.log(1/zc)+2*math.log(1+k)+3-1e-12, ' kdagger(zc)=', 2*math.log(1/zc)+2*math.log(11)+3)
print('printed chain at (0.3322,10), f=0.0085:', r(0.3322,10,0.0085,False), ' f=0.008516:', r(0.3322,10,0.008516,False))
print('T k^2/z^2 at corner:', T_exact(zc,10.0)*100/zc**2, ' at (0.3325,10):', T_exact(0.3325,10.0)*100/0.3325**2)
for f in (0.0085,0.008516):
    print(f'corner (11e^-3.5,10), f={f}: corrected {r(zc,10.0,f,True):.6f}, printed {r(zc,10.0,f,False):.6f}')
