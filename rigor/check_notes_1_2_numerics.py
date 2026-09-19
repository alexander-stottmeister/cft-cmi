import numpy as np, mpmath as mp
rng=np.random.default_rng(7)
def G(iv,r=1.0):   # LX Def 3.17 / Thm 4.1(4): iv = list of (a_i,b_i) increasing
    a=[x[0] for x in iv]; b=[x[1] for x in iv]; n=len(iv); s=0.0
    for i in range(n):
        for j in range(n): s+=np.log(abs(b[i]-a[j]))
    for i in range(n):
        for j in range(i+1,n): s-=np.log(abs(a[i]-a[j]))+np.log(abs(b[i]-b[j]))
    return r/6.0*s
def F2(I1,I2,r=1.0):  # LX Thm 3.18 for two disjoint sets of intervals
    return r*( G(I1,1.0)+G(I2,1.0)-G(sorted(I1+I2),1.0) )/1.0 if False else (G(I1,r)+G(I2,r)-G(sorted(I1+I2),r))
maxerr=0.0
for trial in range(2000):
    x=np.sort(rng.uniform(0,10,4)); x0,x1,x2,x3=x
    a,b,c=x1-x0,x2-x1,x3-x2
    if min(a,b,c)<1e-3: continue
    r=rng.uniform(0.5,4)
    # (1) N1 direct G-identity  vs  closed form
    Gc=lambda u,v: r/6*np.log(v-u)
    lhs=Gc(x0,x2)+Gc(x1,x3)-Gc(x0,x3)-Gc(x1,x2)
    rhs=r/6*np.log((a+b)*(b+c)/(b*(a+b+c)))
    eta=b*(a+b+c)/((a+b)*(b+c))
    maxerr=max(maxerr,abs(lhs-rhs),abs(rhs+r/6*np.log(eta)))
    assert 0<eta<1
    # (2) LX p.24 formula  -r/6 ln |(b2-a2)(b3-a1)/((b3-a2)(b2-a1))| with a1,a2,b2,b3=x0..x3
    lx24=-r/6*np.log(abs((x2-x1)*(x3-x0)/((x3-x1)*(x2-x0))))
    maxerr=max(maxerr,abs(lx24-rhs))
    # (3) collar: exact I_eps from Thm 3.18 vs N2 eq (Ieps-free)
    eps=rng.uniform(1e-6,0.9)*a
    Ae=(x0,x1-eps)
    Ieps_lx = F2([Ae],[(x1,x3)],r) - F2([Ae],[(x1,x2)],r)
    Ieps_n2 = r/6*np.log((a+b)*(b+c+eps)/((a+b+c)*(b+eps)))
    maxerr=max(maxerr,abs(Ieps_lx-Ieps_n2))
    # (4) generalized-F definitional identity (LX) for 3 separated regions vs G-form
    g1,g2=rng.uniform(0.05,0.5,2)
    X=(x1,x2); Y=(x0,x1-g1); Z=(x2+g2,x3+g2)
    lhsF=F2([Y],[X],r)*0  # placeholder
    FXYZ=F2([X],[Y,Z],r)+F2([Y],[Z],r)-F2([X],[Z],r)-F2([X],[Y],r)
    Gform=G([Y,X],r)+G([X,Z],r)-G([Y,X,Z],r)-G([X],r)
    maxerr=max(maxerr,abs(FXYZ-Gform))
    # (5) Thm 4.1(5): F(X u Y, X u Z) = F(Y, X u Z) - F(Y,X)
    alt=F2([Y],[X,Z],r)-F2([Y],[X],r)
    maxerr=max(maxerr,abs(FXYZ-alt))
    # (6) positivity identity
    maxerr=max(maxerr,abs((a+b)*(b+c)-b*(a+b+c)-a*c))
print("max abs discrepancy over checks (1)-(6):", maxerr)
# (7) asymptotics: N1 eq(asymptotic) vs exact
a,d,r=1.3,2.7,2.0
for eps in [1e-2,1e-3,1e-4]:
    exact=r/6*np.log(a*(d+eps)/(eps*(a+d)))
    approx=r/6*np.log(a*d/((a+d)*eps))
    print(f"eps={eps:g}  exact-approx={exact-approx:.3e}   (should be O(eps)={r/6*eps/d:.3e})")
# (8) large-b expansion
a,c,r=0.7,1.9,3.0
print("large-b: b, I, (r/6)ac/b^2, ratio, (I-lead)*b^3")
for b in [10,100,1000,10000]:
    I=r/6*np.log((a+b)*(b+c)/(b*(a+b+c))); lead=r/6*a*c/b**2
    print(f"  {b:6d}  {I:.12e}  {lead:.12e}  {I/lead:.9f}  {(I-lead)*b**3:.6f}  [-r/6*ac(a+c)={-r/6*a*c*(a+c):.6f}]")
# (9) fidelity/norm bounds and their large-b expansions
for b in [10,100,1000]:
    I=r/6*np.log((a+b)*(b+c)/(b*(a+b+c)))
    F=np.exp(-I/2); Nb=2*np.sqrt(1-np.exp(-I))
    print(f"b={b}: F={F:.12f} vs 1-r*a*c/(12 b^2)={1-r*a*c/(12*b**2):.12f} ; norm={Nb:.9f} vs (2/b)sqrt(r a c/6)={2/b*np.sqrt(r*a*c/6):.9f}")
# (10) p(t) normalisation
print("int p =", mp.quad(lambda t: mp.pi/(1+mp.cosh(2*mp.pi*t)), [-mp.inf,0,mp.inf]))
# (11) eta^{r/12} = exp(-I/2)
a,b,c,r=1.1,2.3,0.6,2.5
eta=b*(a+b+c)/((a+b)*(b+c)); I=-r/6*np.log(eta)
print("exp(-I/2)-eta^{r/12} =", np.exp(-I/2)-eta**(r/12), " 2sqrt(1-eta^{r/6})-2sqrt(1-e^{-I}) =", 2*np.sqrt(1-eta**(r/6))-2*np.sqrt(1-np.exp(-I)))
# (12) chiral modular-Hamiltonian weights: CTT identity fails for adjacent intervals
def be(u,v,x): return (x-u)*(v-x)/(v-u) if u<x<v else 0.0
x0,x1,x2,x3=0.,1.,2.,3.
for x in [1.2,1.5,1.8,0.5,2.5]:
    val=be(x0,x2,x)+be(x1,x3,x)-be(x0,x3,x)-be(x1,x2,x)
    print(f"  x={x}: beta_AB+beta_BC-beta_ABC-beta_B = {val:+.4f}")
