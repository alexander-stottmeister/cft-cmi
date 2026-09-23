# Provenance: written by referee REF-DEP-CFT-B2 (2026-09-23), stored by AUTH-CFT-B. Run: python3 tailcheck.py (stdlib only).
# Checks tail_bound.tex cor:rate eq:final: chain of the printed proof with eq:taunu's T versus the claimed 0.173 z^2/k + 0.88 z^2/k^2 on the admissible region k >= 10, k >= 2 log(1/z) + 2 log(1+k) + 3.
import math
def bound(z,k,f=0.0085,crude=False):
    T = 2*z*z/(3*k*k) + 4.6*z*z/k**3 + (12+0.51*z*(1+k))*math.exp(-k)
    if crude: T = 1.75*z*z/k/k
    Pd = T/(2*(1-T))
    Phi = f*z*z
    y = 2*math.exp(2*Pd)*math.sqrt(Phi*Pd)
    return Pd + y/(1-y)
def claim(z,k): return 0.173*z*z/k + 0.88*z*z/k/k
worst=(0,None); worstc=(0,None)
for i in range(1,2001):
    z = i/2000
    for j in range(0,4001):
        k = 10 + j*0.01
        if k < 2*math.log(1/z)+2*math.log(1+k)+3: continue
        r = bound(z,k)/claim(z,k); rc = bound(z,k,crude=True)/claim(z,k)
        if r>worst[0]: worst=(r,(z,k))
        if rc>worstc[0]: worstc=(rc,(z,k))
print("exact-T chain: max ratio", worst)
print("crude T<=1.75: max ratio", worstc)
for f in [0.0085,0.008516]:
    print(f, "at (1,10):", bound(1,10,f), claim(1,10), " at (0.3322,10):", bound(0.3322,10,f)/claim(0.3322,10))
