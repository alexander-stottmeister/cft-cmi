# AUTH-CFT-B, 2026-09-23; stdlib only. Run from anywhere: python3 phi_prime_check.py
# Refutation of card phi-derivative-nondecreasing ("Phi' nondecreasing on (0, inf)"), numerical side.
# Data: cft_cmi/numerics/results_largezeta_certified.txt (sec. 1 raw windows, sec. 4 certified brackets,
# sec. 5 local log-slopes), single chiral component (r = 1), zeta = s/3 (a=1, L=2).
# (1) A convex Phi with Phi(0+) = 0 has Phi(zeta)/zeta nondecreasing; the data show it decreasing.
# (2) Analytic bound used by the refutation (r = 1): Phi(2z) <= (1/6) log(1+z), i.e. Phi(zeta) <= (1/6) log(1+zeta/2).
# (3) zeta Phi'(zeta) = slope * Phi (the weaker property that would suffice for the minimum at lambda = 0).
import math, os, re
here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, "..", "results_largezeta_certified.txt")
txt = open(os.path.normpath(path)).read()
sec4 = txt.split("## 4.")[1].split("## 5.")[0]
sec5 = txt.split("## 5.")[1]
best, lower = {}, {}
for line in sec4.splitlines():
    m = re.match(r"\s+([\d.]+)\s+([\d.e+-]+)\s+.*\s([\d.e+-]+)\s+\+-", line)
    if m:
        z = float(m.group(1)); lower[z] = float(m.group(2)); best[z] = float(m.group(3))
slope = {}
for line in sec5.splitlines():
    m = re.match(r"\s+([\d.]+)\s+([\d.e+-]+)\s+([\d.]+)\s", line)
    if m:
        slope[float(m.group(1))] = float(m.group(3))
print(" zeta     Phi_best     Phi/zeta     rigorous lower   (1/6)log(1+zeta/2)   zeta*Phi' (slope*Phi)")
for z in sorted(best):
    print(f"{z:7.3f}  {best[z]:.5e}  {best[z]/z:.4e}  {lower[z]:.5e}      {math.log(1+z/2)/6:.4f}             "
          f"{slope.get(z, float('nan'))*best[z]:.4e}")
# rigorous-lower-bound version of (1): convexity and Phi(0+)=0 would force Phi(2x) >= 2 Phi(x)
z1, z2 = 4.267, 8.533
p1 = [v for k, v in lower.items() if abs(k - z1) < 1e-3][0]
est82 = [float(l.split()[4]) for l in txt.split("## 2.")[1].split("## 3.")[0].splitlines() if l.strip().startswith("8.533")]
print(f"convexity would need Phi(8.533) >= 2 Phi(4.267) >= 2 x rigorous lower = {2*p1:.4e};"
      f" all Phi_inf(p=1) estimates at 8.533 (the largest extrapolations): {est82}")
