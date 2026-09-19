"""Build fidelity_tables.tex from the corrected-basis results (2026-09-05): results_final2.txt (convergence), results_L120_2.txt + results_hp2.txt + results_A2.txt (scan), results_first3.txt (second order)."""
import re, glob
def parse(fn):
    out=[]
    for l in open(fn):
        if not l.startswith(('exact_','mobius_','Dhat_exact')): continue
        tag=l.split(':')[0].replace('Dhat_','').replace('_g12.npz','')
        g=lambda k: float(re.search(k+r'=(-?[\d.e+-]+)',l).group(1))
        n=int(re.search(r'n_sub=(\d+)',l).group(1)); N=int(re.search(r'N=(\d+)',l).group(1)); kc=float(re.search(r'kc=([\d.]+)',l).group(1))
        Lam=int(re.search(r'Lam(\d+)',tag).group(1)); k=int(re.search(r'_k(\d+)',tag).group(1))
        raw=g('-logF_sub'); cor=float(re.search(r'-logF_sub=[-\d.e+]+ \+tail=([\d.e+-]+)',l).group(1))
        mS=re.search(r'S(?:_sub)?=(nan|[\d.e+-]+)(?: \+tail=(nan|[\d.e+-]+))?',l); Ssub=float(mS.group(1)); S=float(mS.group(2) or mS.group(1))
        z=g('zeta'); import math; bnd=2*cor/(math.log(1+z/2)/6)
        out.append(dict(tag=tag,Lam=Lam,k=k,N=N,n=n,kc=kc,zeta=z,raw=raw,cor=cor,S=S,Ssub=Ssub,bnd=bnd))
    return out
conv=[r for r in parse('results_final2.txt') if abs(r['zeta']-1/15)<1e-4 and not r['tag'].startswith('mobius')]
scan120=parse('results_L120_2.txt')+[r for r in parse('results_final2.txt') if r['Lam']==120 and r['k']==45]; scanhp=parse('results_hp2.txt'); scan60=parse('results_A2.txt')
T=[]
T.append(r'''\begin{table}[ht]\centering\small
\caption{Convergence of \(\Phi(1/15)\) (\(\eps=10^{-8}\), \(\kappa_c=18.4\)). Raw values are rigorous lower bounds; corrected values add \(\zeta^2/(15\kappa_c^2)=8.73\times10^{-7}\).}\label{tab:convergence}
\begin{tabular}{rrrr r r}\toprule
\(\Lambda\) & \(\kappa_{\max}\) & \(N\) & \(n_{\mathrm{sub}}\) & \(10^5\,\Phi_{\mathrm{sub}}\) & \(10^5\,(\Phi_{\mathrm{sub}}+\text{tail})\) \\\midrule''')
for r in sorted(conv,key=lambda r:(r['Lam'],r['k'])): T.append(f"{r['Lam']} & {r['k']} & {r['N']} & {r['n']} & {1e5*r['raw']:.5f} & {1e5*r['cor']:.5f} \\\\")
T.append(r'\bottomrule\end{tabular}\end{table}')
T.append(r'''\begin{table}[ht]\centering\small
\caption{Second-order coefficients from the first-order kernel (corrected basis) in the spectral window \(\eps<w<1-\eps\) of the box compression, \(\kappa_c=\log(1/\eps)\). \(f_2^{\rm sub}\) and \(s_2^{\rm sub}\) are rigorous lower bounds; the tail \(\zeta^2/(15\kappa_c^2)\) is added to \(f_2\). Last row: \(f_2\) from the stable tail-corrected values at \(\kappa_c\ge25\); \(s_2\) from two-point \(1/\kappa_c\) extrapolations (\(0.0841\) from \(\kappa_c=18.4,25.3\); \(0.0833\) from \(25.3,32.2\)). Windows below \(10^{-14}\) are at the double-precision floor and omitted.}\label{tab:second-order}
\begin{tabular}{r r r r r r r}\toprule
\(\eps\) & \(\kappa_c\) & \(\Lambda\) & \(\kappa_{\max}\) & \(f_2^{\rm sub}\) & \(f_2^{\rm sub}+\)tail & \(s_2^{\rm sub}\) \\\midrule''')
rows=[]
for l in open('results_first_window.txt'):
    m=re.search(r'eps=([\de.-]+) first_s1\.0_Lam(\d+)_k(\d+): N=(\d+) kc=([\d.]+)\s+f2_sub=([\d.]+)\s+f2=([\d.]+)\s+s2_sub=([\d.]+)',l)
    if m and float(m.group(1))>1e-15: rows.append((float(m.group(1)),int(m.group(2)),int(m.group(3)),m.group(5),m.group(6),m.group(7),m.group(8)))
for eps_,Lam,k,kc,f2s,f2c,s2s in sorted(rows,key=lambda r:(-r[0],r[1],r[2])): T.append(f"\\(10^{{{int(round(__import__('math').log10(eps_)))}}}\\) & {kc} & {Lam} & {k} & {f2s} & {f2c} & {s2s} \\\\")
T.append(r'\(\to0\) & \(\infty\) & & & & 0.008444(1) & 0.0837(5) \\')
T.append(r'\bottomrule\end{tabular}\end{table}')
T.append(r"""\begin{table}[ht]\centering\small
\caption{\(\Phi(\zeta)\) (tail-corrected) and relative entropy. A: \(\Lambda=60,\kappa_{\max}=30,\eps=10^{-8}\); B: \(\Lambda=120,\kappa_{\max}=45,\eps=10^{-8}\); C: \(\Lambda=60,\kappa_{\max}=30,\eps=10^{-11}\). \(S_\infty\) is the \(1/\kappa_c\) extrapolation of the sub-compressed relative entropy from \(\kappa_c=18.4\) (A) and \(25.3\) (C). Last column: \(-2\log\Fid/I_\omega(A{:}C|B)\).}\label{tab:scan}
\begin{tabular}{r rrr r r r r}\toprule
\(\zeta\) & \(\Phi\) (A) & \(\Phi\) (B) & \(\Phi\) (C) & \(\Phi/\zeta^2\) (C) & \(S_\infty\) & \(S_\infty/\zeta^2\) & ratio \\\midrule""")
def find(lst,z):
    c=[r for r in lst if abs(r['zeta']-z)<1e-4]; return c[0] if c else None
for r in sorted(scan60,key=lambda r:r['zeta']):
    z=r['zeta']; b=find(scan120,z); c=find(scanhp,z)
    if c is not None:
        Sinf = c['Ssub'] + (c['Ssub']-r['Ssub'])*(1/c['kc'])/(1/r['kc']-1/c['kc'])
        T.append(f"{z:.4f} & {r['cor']:.4e} & {(b['cor'] if b else float('nan')):.4e} & {c['cor']:.4e} & {c['cor']/z**2:.5f} & {Sinf:.4e} & {Sinf/z**2:.4f} & {c['bnd']:.4f} \\\\")
    else:
        T.append(f"{z:.4f} & {r['cor']:.4e} & {(b['cor'] if b else float('nan')):.4e} & -- & {r['cor']/z**2:.5f} & -- & -- & {r['bnd']:.4f} \\\\")
T.append(r'\bottomrule\end{tabular}\end{table}')
open('../fidelity_tables.tex','w').write('\n'.join(T)+'\n'); print("tables written")
