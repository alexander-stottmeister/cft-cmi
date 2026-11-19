"""REF-RP-4: constants of prop:ranges and card const-f2, mpmath 30 digits. Tolerance: exact closed forms vs
the quoted decimals, |quoted - exact| < half a unit of the last quoted digit."""
import mpmath as mp
mp.mp.dps = 30
f2 = 1 / (12 * mp.pi**2)
rows = [("f2 = 1/(12 pi^2)", f2, "0.0084434"),
        ("(4 f2)^(-1/2)", (4 * f2) ** -0.5, "5.4414"), ("pi sqrt3", mp.pi * mp.sqrt(3), "5.4414"),
        ("(2 f2)^(-1/2)", (2 * f2) ** -0.5, "7.6953"), ("pi sqrt6", mp.pi * mp.sqrt(6), "7.6953"),
        ("2 f2", 2 * f2, "0.0169"), ("8 f2 = 8/(12 pi^2)", 8 * f2, "0.0675"), ("8 f2 (4 digits)", 8 * f2, "0.067547"),
        ("1/(0.8 sqrt2) old range index_zero_check", 1 / (mp.mpf('0.8') * mp.sqrt(2)), "0.8839"),
        ("0.8 sqrt2", mp.mpf('0.8') * mp.sqrt(2), "1.1314"), ("log2/pi^2", mp.log(2) / mp.pi**2, "0.0702")]
for name, v, q in rows:
    d = len(q.split('.')[1]); ok = abs(v - mp.mpf(q)) < mp.mpf(10) ** (-d) / 2
    print(f"{name:42s} {mp.nstr(v, 15):>20s} quoted {q:>9s} rounds-correctly: {ok}")
