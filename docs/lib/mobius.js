/* mobius.js — Moebius maps as 2x2 matrices and the Schwarzian calculus of C^1
   piecewise-Moebius maps, following rigor/network_corner_calculus.tex:
   Def. 4.1 (the class PM), Lem. 4.2 (the Schwarzian is a sum of point masses),
   Lem. 4.3 (a parabolic corner has mass -2 sigma from either side),
   Lem. 4.4 (composition), Thm. 5.2 (the unconditional transformation rule).

   A map is stored as [a,b,c,d] acting by x |-> (a x + b)/(c x + d), ad - bc > 0.
   A piecewise-Moebius map is {domain:[lo,hi], breaks:[q1<...<qN], pieces:[M0..MN]},
   pieces[i] being the Moebius map on the i-th component of domain \ breaks.
*/

export const ID = [1, 0, 0, 1];

export const mob = (a, b, c, d) => [a, b, c, d];
export const det = ([a, b, c, d]) => a * d - b * c;

/** f o g, i.e. (f o g)(x) = f(g(x)); the 2x2 product, then rescaled to det 1. */
export function compose(f, g) {
  const [a, b, c, d] = f, [e, h, i, j] = g;
  return normalize([a * e + b * i, a * h + b * j, c * e + d * i, c * h + d * j]);
}
export function inverse([a, b, c, d]) { return normalize([d, -b, -c, a]); }

/** rescale to |det| = 1 so that long compositions do not drift in magnitude */
export function normalize(M) {
  const D = det(M);
  if (!isFinite(D) || D === 0) return M;
  const s = 1 / Math.sqrt(Math.abs(D));
  return [M[0] * s, M[1] * s, M[2] * s, M[3] * s];
}

export const apply = ([a, b, c, d], x) => (a * x + b) / (c * x + d);
export const deriv = ([a, b, c, d], x) => (a * d - b * c) / Math.pow(c * x + d, 2);
export const deriv2 = ([a, b, c, d], x) => -2 * c * (a * d - b * c) / Math.pow(c * x + d, 3);
/** v = M''/M' = (log M')' = -2c/(cx+d); its jump at a breakpoint is the Schwarzian mass */
export const vlog = ([a, b, c, d], x) => -2 * c / (c * x + d);

/** the parabolic compression of (C3)/(3) toward p, moving the right-hand side */
export function parabolicRight(p, sigma) { return normalize([1 + sigma * p, -sigma * p * p, sigma, 1 - sigma * p]); }
/** ... and the one moving the left-hand side; both give the corner mass -2 sigma */
export function parabolicLeft(p, sigma) { return normalize([1 - sigma * p, sigma * p * p, -sigma, 1 + sigma * p]); }

// ---------------------------------------------------------------- PM maps

export function pm(domain, breaks, pieces) {
  if (pieces.length !== breaks.length + 1) throw new Error('pm: pieces must be breaks+1');
  return { domain, breaks, pieces };
}
export const pmIdentity = domain => pm(domain, [], [ID]);

/** one step of a protocol: the parabolic compression at the corner p. */
export function pmStep(p, sigma, side) {
  return side === 'L'
    ? pm([-Infinity, Infinity], [p], [parabolicLeft(p, sigma), ID])
    : pm([-Infinity, Infinity], [p], [ID, parabolicRight(p, sigma)]);
}

export function pieceAt(P, x) {
  let i = 0;
  while (i < P.breaks.length && x >= P.breaks[i]) i++;
  return i;
}
export const pmEval = (P, x) => apply(P.pieces[pieceAt(P, x)], x);
export const pmDeriv = (P, x) => deriv(P.pieces[pieceAt(P, x)], x);
export const pmDeriv2 = (P, x) => deriv2(P.pieces[pieceAt(P, x)], x);
export const pmRange = P => [pmEval(P, P.domain[0]), pmEval(P, P.domain[1])];

/** the preimage of y under the increasing map P, or null when y is outside its range */
export function pmPreimage(P, y) {
  const [lo, hi] = P.domain;
  const edges = [lo, ...P.breaks.filter(q => q > lo && q < hi), hi];
  for (let i = 0; i < edges.length - 1; i++) {
    const a = pmEval(P, edges[i]), b = pmEval(P, edges[i + 1]);
    if (y >= Math.min(a, b) - 1e-12 && y <= Math.max(a, b) + 1e-12) {
      const mid = 0.5 * (edges[i] + edges[i + 1]);
      return apply(inverse(P.pieces[pieceAt(P, mid)]), y);
    }
  }
  return null;
}

/** f o g on g's domain.  Breakpoints of f that fall outside g's range are dropped:
    that is exactly the "swallowed corner" of Thm. 5.2. */
export function pmCompose(f, g) {
  const [lo, hi] = g.domain;
  const [ra, rb] = pmRange(g);
  const cuts = g.breaks.filter(q => q > lo + 1e-12 && q < hi - 1e-12);
  for (const r of f.breaks) {
    if (r <= Math.min(ra, rb) + 1e-12 || r >= Math.max(ra, rb) - 1e-12) continue;
    const x = pmPreimage(g, r);
    if (x !== null && x > lo + 1e-12 && x < hi - 1e-12) cuts.push(x);
  }
  cuts.sort((a, b) => a - b);
  const breaks = cuts.filter((q, i) => i === 0 || Math.abs(q - cuts[i - 1]) > 1e-11);
  const edges = [lo, ...breaks, hi];
  const pieces = [];
  for (let i = 0; i < edges.length - 1; i++) {
    let mid;
    if (isFinite(edges[i]) && isFinite(edges[i + 1])) mid = 0.5 * (edges[i] + edges[i + 1]);
    else if (isFinite(edges[i])) mid = edges[i] + 1;
    else if (isFinite(edges[i + 1])) mid = edges[i + 1] - 1;
    else mid = 0;
    const Mg = g.pieces[pieceAt(g, mid)];
    const Mf = f.pieces[pieceAt(f, apply(Mg, mid))];
    pieces.push(compose(Mf, Mg));
  }
  return pm(g.domain, breaks, pieces);
}

/** Lem. 4.2: Sch(Phi) = sum_j [v]_{q_j} delta_{q_j}, with no square term.
    Returns [{x, mass}], masses at coinciding points added, tiny masses dropped. */
export function pmSchwarzian(P, tol = 1e-9) {
  const out = [];
  for (let i = 0; i < P.breaks.length; i++) {
    const q = P.breaks[i];
    if (q <= P.domain[0] + 1e-12 || q >= P.domain[1] - 1e-12) continue;   // boundary carries no mass
    const mass = vlog(P.pieces[i + 1], q) - vlog(P.pieces[i], q);
    if (Math.abs(mass) < tol) continue;
    const prev = out[out.length - 1];
    if (prev && Math.abs(prev.x - q) < 1e-9) prev.mass += mass;
    else out.push({ x: q, mass });
  }
  return out;
}

// ------------------------------------------------- protocols (C4) and Thm 5.2

/** Phi = k_1 o k_2 o ... o k_N on J_N, the FIRST step outermost (eq. (4)). */
export function composeSteps(steps, domain) {
  let P = pmIdentity(domain);
  for (let m = steps.length - 1; m >= 0; m--) {
    P = pmCompose(pmStep(steps[m].p, steps[m].sigma, steps[m].side), P);
  }
  return P;
}

/** Thm. 5.2, unconditional: the mass of step m sits at x_m = G_m^{-1}(p^(m)) and is
    scaled by G_m'(x_m), where G_m = k_{m+1} o ... o k_N.  A step whose corner is
    outside the range of G_m contributes nothing at all. */
export function theoremGeneral(steps, domain) {
  const N = steps.length;
  const G = new Array(N + 1);
  G[N] = pmIdentity(domain);
  for (let m = N - 1; m >= 0; m--) G[m] = pmCompose(pmStep(steps[m].p, steps[m].sigma, steps[m].side), G[m + 1]);
  const out = [];
  for (let m = 0; m < N; m++) {
    const Gm = G[m + 1];                                  // G_m in the paper's 1-based index
    const [ra, rb] = pmRange(Gm);
    const p = steps[m].p;
    const inside = p > Math.min(ra, rb) + 1e-12 && p < Math.max(ra, rb) - 1e-12;
    if (!inside) { out.push({ m, step: steps[m], swallowed: true, x: null, gprime: null, mass: 0 }); continue; }
    const x = pmPreimage(Gm, p);
    const gp = pmDeriv(Gm, x);
    out.push({ m, step: steps[m], swallowed: false, x, gprime: gp, mass: -2 * steps[m].sigma * gp,
               displaced: Math.abs(x - p) > 1e-9 });
  }
  return out;
}

/** Hypothesis (H) of Def. 5.1: no EARLIER corner lies in the interior of a LATER
    step's moving part M = A_B u A_new.  Tested on the configuration, never inferred
    from the shape of the protocol. */
export function hypothesisH(steps) {
  const bad = [];
  for (let m = 0; m < steps.length; m++) {
    for (let mp = m + 1; mp < steps.length; mp++) {
      const M = steps[mp].moving;                         // [lo,hi] of M_{m'}
      if (!M) continue;
      const p = steps[m].p;
      if (p > Math.min(M[0], M[1]) + 1e-12 && p < Math.max(M[0], M[1]) - 1e-12) bad.push({ m, mp, p, M });
    }
  }
  return { holds: bad.length === 0, violations: bad };
}

/** Thm. 5.3, the junction form, valid only under (H): kappa_k = sum of the sigmas
    of the steps whose corner is p_k. */
export function cornerMeasure(steps) {
  const map = new Map();
  for (const s of steps) {
    const key = s.p.toFixed(10);
    map.set(key, { x: s.p, kappa: (map.get(key)?.kappa || 0) + s.sigma });
  }
  return [...map.values()].sort((a, b) => a.x - b.x);
}

/** the modular frame of (C5): beta_I(x) = (x-p1)(pn-x)/T, zeta = kappa beta_I(p) */
export const betaI = (x, p1, pN) => (x - p1) * (pN - x) / (pN - p1);
export const thetaT = t => 0.5 * (1 + Math.exp(-2 * Math.PI * t));
/** sigma of a step: sigma = s/(l_B + l_new), s = 2 theta_t l_new/l_B  (C3) */
export const sigmaOf = (lB, lNew, theta = 1) => 2 * theta * lNew / (lB * (lB + lNew));
