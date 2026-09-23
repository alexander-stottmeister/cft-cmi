# REF-DEP-CFT-B6: integrate d/ds k = -chi(k), chi(x)=x^2 beta(x-1) (x>0), 0 (x<=0), for several admissible beta
import math
def f(t): return math.exp(-1.0/t) if t>0 else 0.0
def step(t):            # standard smooth step: 1 on t<=0, 0 on t>=1, decreasing
    a,b=f(1-t),f(t); return a/(a+b)
def step_sq(t):         # a steeper admissible variant
    return step(t)**2
def step_late(t, e=0.5):  # beta == 1 on (-inf,e], smooth decrease on [e,1]
    return 1.0 if t<=e else step((t-e)/(1-e))
def make_chi(beta):
    return lambda x: 0.0 if x<=0 else x*x*beta(x-1)
def flow(chi, x, s, n=200000):
    h=s/n; k=x
    for _ in range(n):
        k1=-chi(k); k2=-chi(k+h*k1/2); k3=-chi(k+h*k2/2); k4=-chi(k+h*k3)
        k+=h*(k1+2*k2+2*k3+k4)/6
    return k
for name,beta in [('standard step',step),('step^2',step_sq),('beta=1 on [0,.5]',step_late)]:
    chi=make_chi(beta)
    print(name, ': s=-1,x=0.9 flow =', round(flow(chi,0.9,-1.0),6), ' x/(1+sx) =', 0.9/(1-0.9),
          '| s=0.5,x=0.9 flow =', round(flow(chi,0.9,0.5),6), 'vs', round(0.9/1.45,6),
          '| s=-0.2,x=1 flow =', round(flow(chi,1.0,-0.2),6), 'vs', round(1/0.8,6))
# eta(s) = sup_x |x - k~_s(x)| for the standard step, s in {0.25,0.5,1,-0.5,-1}
chi=make_chi(step)
for s in [0.25,0.5,1.0,-0.5,-1.0]:
    xs=[0.02*i for i in range(1,100)]
    eta=max(abs(x-flow(chi,x,s,n=4000)) for x in xs)
    print('standard step: s =',s,' eta ~',round(eta,4))
