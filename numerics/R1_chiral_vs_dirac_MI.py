import numpy as np
np.set_printoptions(precision=6)

def corr(idx, kF=np.pi/2):
    n = np.array(idx)[:,None]-np.array(idx)[None,:]
    with np.errstate(divide='ignore', invalid='ignore'):
        C = np.sin(kF*n)/(np.pi*n)
    C[np.arange(len(idx)),np.arange(len(idx))] = kF/np.pi
    return C

def ent(idx):
    C = corr(idx)
    ev = np.linalg.eigvalsh(C)
    ev = np.clip(ev, 1e-14, 1-1e-14)
    return float(-np.sum(ev*np.log(ev)+(1-ev)*np.log(1-ev)))

def mi(L1,g,L2):
    A = list(range(0,L1))
    B = list(range(L1+g, L1+g+L2))
    return ent(A)+ent(B)-ent(A+B)

# continuum cross-ratio: intervals (x1,x2)=(0,L1), (x3,x4)=(L1+g, L1+g+L2)
def eta(L1,g,L2):
    x1,x2,x3,x4 = 0.0, L1, L1+g, L1+g+L2
    # F = k*ln[(x3-x1)(x4-x2)/((x3-x2)(x4-x1))]
    return (x3-x2)*(x4-x1)/((x3-x1)*(x4-x2))

print(f"{'L1':>5}{'g':>5}{'L2':>5}{'MI':>12}{'-ln eta':>12}{'MI/(-ln eta)':>15}")
for (L1,g,L2) in [(40,40,40),(80,80,80),(160,160,160),(200,100,200),(300,150,300),(200,400,200),(400,800,400),(300,60,300),(600,120,600)]:
    m = mi(L1,g,L2); e = eta(L1,g,L2)
    print(f"{L1:5d}{g:5d}{L2:5d}{m:12.6f}{-np.log(e):12.6f}{m/(-np.log(e)):15.6f}")
print()
print("1/3 =", 1/3, "  1/6 =", 1/6)
