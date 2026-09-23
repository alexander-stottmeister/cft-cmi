# REF-DEP-CFT-B6: accurate double-precision check of thm:main eq:Psi (tail_bound.tex:464-467) in the saturating case
# of the Bures-angle triangle inequality used at <1>3: cos A1 = e^{-w} (w = Phi_W), cos A2 = e^{-d} (d = Phi_partial),
# e^{-Phi} = cos(A1+A2)  =>  Phi - w = -log(cos A2 - tan A1 sin A2) = -log1p(expm1(-d) - sqrt(expm1(2w)) sqrt(-expm1(-2d))).
# Printed bound: d + y/(1-y), y = 2 e^{2d} sqrt(Phi d).  Corrected (what <1>3-<1>4 give): d + Y/(1-Y), Y = e^{w} y.
import math
for w in [0.0085, 0.005, 0.001]:
    for d in [1e-4, 1e-6, 1e-8, 1e-10]:
        lhs = -math.log1p(math.expm1(-d) - math.sqrt(math.expm1(2*w))*math.sqrt(-math.expm1(-2*d)))
        Phi = w + lhs
        y = 2*math.exp(2*d)*math.sqrt(Phi*d)
        Y = math.exp(w)*y
        print(f'w={w} d={d:g}: ratio to printed = {lhs/(d+y/(1-y)):.6f}, to corrected = {lhs/(d+Y/(1-Y)):.6f}, sqrt((e^2w-1)/2w) = {math.sqrt(math.expm1(2*w)/(2*w)):.6f}')
