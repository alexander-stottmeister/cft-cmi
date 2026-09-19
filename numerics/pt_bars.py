import re,glob
def parse(fn):
    out={}
    for L in open(fn):
        m=re.search(r'zeta=([\d.]+).*?-logF_sub=([\deE.+-]+).*?kc=([\d.]+)',L) or None
        mk=re.search(r'kc=([\d.]+)',L); mz=re.search(r'zeta=([\d.]+)',L); mf=re.search(r'-logF_sub=([\d.eE+-]+)',L)
        mn=re.search(r'n_sub=(\d+)',L); mN=re.search(r'N=(\d+)',L)
        if mz and mf: out[round(float(mz.group(1)),5)]=(float(mf.group(1)),float(mk.group(1)),int(mn.group(1)),int(mN.group(1)))
    return out
A=parse('results_A2.txt'); C=parse('results_hp2.txt'); D=parse('results_hp14.txt')
kmax_eff=29.6
print("zeta      Phi_sub(kc=18.4)  Phi_sub(25.3)   Phi_sub(32.2)  kappa_eff  Sigma_proved  cert_upper_add  best")
rows=[]
for z in sorted(set(A)|set(C)|set(D)):
    a=A.get(z); c=C.get(z); d=D.get(z)
    best=max([x[0] for x in (a,c,d) if x])
    # window full at eps=1e-14 -> residual is the box cutoff, kappa_eff = kmax_eff, coeff 0.0641
    if d and d[2]==d[3]:
        keff=kmax_eff; Sig=0.0641*z*z/keff**2; kind='box'
    else:
        keff=(d or c or a)[1]; Sig=z*z/(15*keff**2); kind='win'
    cert=0.173*z*z/keff+0.88*z*z/keff**2
    rows.append((z,a[0] if a else 0,c[0] if c else 0,d[0] if d else 0,keff,kind,Sig,cert,best+Sig,best,best+cert))
    print("%8.5f  %.6e  %.6e  %.6e  %5.1f %s  %.4e  %.4e  %.6e"%(z,a[0] if a else 0,c[0] if c else 0,d[0] if d else 0,keff,kind,Sig,cert,best+Sig))
print()
print("LaTeX rows (zeta, Phi_sub, certified interval, best estimate):")
for r in rows:
    z,_,_,_,keff,kind,Sig,cert,bs,best,up=r
    print(r"%.4f & %.5f & [%.4f,\ %.4f] & %.5f & %.1f\%% \\"%(z,best*1e5,best*1e5,up*1e5,bs*1e5,100*cert/best))
