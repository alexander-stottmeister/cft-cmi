"""REF-P6-1: is VWZ Fig. 25 a 'rough measurement of Ghat at Delta <~ 2'?

Symmetric setup L_A = L_D = a, L_B = L_C = b = 1; VWZ (5.9) eta = a/(a+2b), so a = 2 eta/(1-eta).
Corner strengths (REF-P6-0, exact):  zeta_1 = a/b, zeta_2 = a(a+2b)/(2b(a+b)), zeta_3 = a/b,
zeta_eff = 2a/b;  modular separation of Protocol 2's corners  Delta_23 = log(1/eta).

Second-order law:  Phi^(2) = f2 (zeta_2^2 + zeta_3^2 + 2 zeta_2 zeta_3 X),  Phi^(3) = f2 zeta_eff^2,
X = Ghat(Delta_23)/Ghat(0), and positive-definiteness forces |X| <= 1.
Print the X that VWZ's "Phi^(2) ~ Phi^(3)" would require.
"""
import numpy as np
print(" eta     eta^2   Delta_23  zeta_1   (z2+z3)/z_eff   X needed for Phi2 = Phi3   |X|<=1?")
for eta in (0.632, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01):
    b = 1.0; a = 2 * eta / (1 - eta)
    z1 = a / b
    z2 = a * (a + 2 * b) / (2 * b * (a + b))
    z3 = a / b
    zeff = 2 * a / b
    D = np.log(1 / eta)
    X = (zeff ** 2 - z2 ** 2 - z3 ** 2) / (2 * z2 * z3)
    print("  %-6.3f %-7.4f %-9.3f %-8.4f %-15.6f %-26.4f %s"
          % (eta, eta ** 2, D, z1, (z2 + z3) / zeff, X, "OK" if abs(X) <= 1 else "IMPOSSIBLE"))
print("""
Delta_23 = log(1/eta): the axis bound eta^2 <= 0.4 (eta <= 0.632) bounds Delta_23 from BELOW,
Delta_23 >= log(1/0.632) = %.3f.  Delta_23 <= 2.3 is eta >= 0.1, i.e. eta^2 >= 0.01.
Phi^(2) < Phi^(3) STRICTLY at second order for every eta > 0, because
zeta_2 + zeta_3 < 2 zeta_1 = zeta_eff  <=>  (a+2b)/(2(a+b)) < 1  <=>  a > 0,
so even X = +1 cannot make them equal; equality is approached only as eta -> 0, X -> 1.""" % np.log(1/0.632))
