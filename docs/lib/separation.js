/* separation.js — the backward recursion of Theorem 11.1 of
   rigor/network_corner_calculus.tex, in closed form.

   Notation, as in the document.  An L->R ordinary-Petz chain has corners
   p_2..p_{n-1} at modular positions y_2 < ... < y_{n-1}; Delta_k = y_{k+1}-y_k
   is the modular length of A_k, with Delta_n = +infinity, and zeta_k is the
   corner strength.  Lemma 10.3 makes the strengths functions of the modular
   lengths alone,

       1/zeta_k = sinh^2(Delta_k/2) coth(Delta_{k+1}/2) + (1/2) sinh(Delta_k),

   which in E := e^{Delta_k} and c := coth(Delta_{k+1}/2) = 1 + gamma_{k+1} is
   the quadratic

       (c+1) E^2 - (4/zeta_k + 2c) E + (c-1) = 0,          gamma_j := 2/(E_j-1).

   Everything below is that quadratic, solved from the right end of the chain
   inwards.  No fitting, no iteration: one square root per corner.  */

/** e^{Delta_j} from the strength at j and gamma at j+1.  gammaNext = 0 is the
    last corner, where the quadratic degenerates to E = 1 + 2/zeta exactly. */
export function solveE(zeta, gammaNext) {
  const c = 1 + gammaNext;
  const b = 4 / zeta + 2 * c;
  const disc = b * b - 4 * (c + 1) * (c - 1);
  return (b + Math.sqrt(Math.max(0, disc))) / (2 * (c + 1));
}

/** The chain, computed backwards.  `zetas[0]` is the corner k the bound is
    about and the last entry is the last corner n-1.  Returns one row per
    corner, in the same order, each with its gamma, E = e^{Delta} and Delta. */
export function backward(zetas) {
  const rows = new Array(zetas.length);
  let gamma = 0;                      // gamma_n = 0: Delta_n = +infinity
  for (let i = zetas.length - 1; i >= 0; i--) {
    const zeta = zetas[i];
    const E = solveE(zeta, gamma);
    const row = { i, zeta, gammaNext: gamma, E, delta: Math.log(E) };
    gamma = 2 / (E - 1);
    row.gamma = gamma;
    rows[i] = row;
  }
  return rows;
}

/** The exact constrained minimum: every corner as strong as the hypothesis
    allows, zeta_j = eps, with m corners at and to the right of k.  This is the
    closed backward recursion REF-P6-3 used, and it reproduces the recorded
    minima 6.8134, 20.0499, 66.6817, 200.0050, 666.6682. */
export function minChain(eps, m) {
  return backward(new Array(m).fill(eps));
}

/** min e^{Delta_k} over all-weak chains with m corners to the right. */
export const minValue = (eps, m) => minChain(eps, m)[0].E;

/** The bound of Theorem 11.1, and the fixed point of its recursion bound
    gamma_j <= zeta_j (1 + gamma_{j+1}/2). */
export const bound = eps => 2 / eps;
export const fixedPoint = eps => 2 * eps / (2 - eps);

/** The exact strength implied by two modular lengths (Lemma 10.3, first form),
    used to check the recursion against the definition it came from. */
export function zetaOf(delta, deltaNext) {
  const s = x => Math.sinh(x / 2);
  if (!isFinite(deltaNext)) return 2 / (Math.exp(delta) - 1);
  return s(deltaNext) / (s(delta) * Math.sinh((delta + deltaNext) / 2));
}
