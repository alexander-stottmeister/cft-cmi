/* mobius.test.js — assertions for mobius.js, run by mobius.test.html in the browser.
   Every numeric target is quoted from rigor/network_corner_calculus.tex, with the
   label of the statement it comes from. */
import * as M from './mobius.js';

export const tests = [];
const test = (name, source, fn) => tests.push({ name, source, fn });

// ------------------------------------------------------------- the algebra
test('apply / compose / inverse are the 2x2 matrix operations', 'Def. (C6)', t => {
  const f = [2, 1, 1, 3], g = [1, -2, 0.5, 1.7];
  for (const x of [-3.3, -0.4, 0.7, 5.1]) {
    t.close(M.apply(M.compose(f, g), x), M.apply(f, M.apply(g, x)), 1e-12, 'compose at x=' + x);
    t.close(M.apply(M.inverse(f), M.apply(f, x)), x, 1e-11, 'inverse at x=' + x);
  }
  t.close(M.det(M.normalize(f)), 1, 1e-14, 'normalize gives det 1');
});

test('derivative and second derivative match finite differences', 'Def. (C6)', t => {
  const f = [2, 1, 1, 3], h = 1e-5;
  for (const x of [-2.2, 0.3, 4.7]) {
    const d1 = (M.apply(f, x + h) - M.apply(f, x - h)) / (2 * h);
    const d2 = (M.apply(f, x + h) - 2 * M.apply(f, x) + M.apply(f, x - h)) / (h * h);
    t.close(M.deriv(f, x), d1, 1e-6, "f' at x=" + x);
    t.close(M.deriv2(f, x), d2, 1e-4, 'f" at x=' + x);
    t.close(M.vlog(f, x), M.deriv2(f, x) / M.deriv(f, x), 1e-12, 'v = f"/f\' at x=' + x);
  }
});

test('the parabolic compression is the closed form of eq. (5)', 'eq:step-map', t => {
  const p = 1.7, s = 0.83;
  for (const x of [p + 0.1, p + 1, p + 4]) t.close(M.apply(M.parabolicRight(p, s), x), p + (x - p) / (1 + s * (x - p)), 1e-12, 'R at ' + x);
  for (const x of [p - 0.1, p - 1, p - 4]) t.close(M.apply(M.parabolicLeft(p, s), x), p + (x - p) / (1 - s * (x - p)), 1e-12, 'L at ' + x);
  t.close(M.apply(M.parabolicRight(p, s), p), p, 1e-12, 'R fixes the corner');
  t.close(M.deriv(M.parabolicRight(p, s), p), 1, 1e-12, "R' = 1 at the corner (C^1)");
  t.close(M.deriv(M.parabolicLeft(p, s), p), 1, 1e-12, "L' = 1 at the corner (C^1)");
});

test('a parabolic corner has Schwarzian mass -2 sigma from either side', 'Lem. 4.3', t => {
  for (const [side, p, s] of [['R', 1.7, 0.83], ['L', -0.4, 2.1], ['R', 0, 1]]) {
    const P = M.pmStep(p, s, side);
    P.domain = [p - 5, p + 5];
    const S = M.pmSchwarzian(P);
    t.eq(S.length, 1, 'one mass, side ' + side);
    t.close(S[0].x, p, 1e-12, 'mass sits at the corner');
    t.close(S[0].mass, -2 * s, 1e-12, 'mass = -2 sigma, side ' + side);
  }
});

test('two parabolic corners at the same point add: -2(s1+s2)', 'Lem. 8.1, eq:same-side', t => {
  const p = 0.9, s1 = 0.4, s2 = 1.1, dom = [p - 3, p + 3];
  const P = M.composeSteps([{ p, sigma: s1, side: 'R' }, { p, sigma: s2, side: 'R' }], dom);
  const S = M.pmSchwarzian(P);
  t.eq(S.length, 1, 'still one mass');
  t.close(S[0].mass, -2 * (s1 + s2), 1e-10, 'masses add');
  const one = M.parabolicRight(p, s1 + s2);
  for (const x of [p + 0.2, p + 2]) t.close(M.pmEval(P, x), M.apply(one, x), 1e-11, 'R o R = R at ' + x);
});

test('opposite sides commute and equal M o R_{s1+s2}', 'Lem. 8.1, eq:opposite-side', t => {
  const p = 2.0, s1 = 0.37, s2 = 0.91, dom = [p - 3, p + 3];
  const A = M.composeSteps([{ p, sigma: s1, side: 'L' }, { p, sigma: s2, side: 'R' }], dom);
  const B = M.composeSteps([{ p, sigma: s2, side: 'R' }, { p, sigma: s1, side: 'L' }], dom);
  const Mg = M.parabolicLeft(p, s1);            // the GLOBAL Moebius factor of eq. (30)
  const R = M.pmStep(p, s1 + s2, 'R');          // ... composed with the PIECEWISE compression
  for (const x of [p - 2, p - 0.3, p + 0.3, p + 2]) {
    t.close(M.pmEval(A, x), M.pmEval(B, x), 1e-10, 'the two orders agree at ' + x);
    t.close(M.pmEval(A, x), M.apply(Mg, M.pmEval(R, x)), 1e-10, 'equals M o R at ' + x);
  }
  t.close(M.pmSchwarzian(A)[0].mass, -2 * (s1 + s2), 1e-10, 'Schwarzian of the composite');
});

test('composition rule: a later map pulls a mass back and scales it', 'Lem. 4.4', t => {
  const g = M.pmStep(1.0, 0.7, 'L'), f = M.pmStep(2.5, 0.4, 'R');
  g.domain = [-2, 6];
  const C = M.pmCompose(f, g);
  const S = M.pmSchwarzian(C);
  const x = M.pmPreimage(g, 2.5);
  t.eq(S.length, 2, 'two masses');
  const at = v => S.find(s => Math.abs(s.x - v) < 1e-8);
  t.close(at(1.0).mass, -2 * 0.7, 1e-10, 'the outer-step mass is untouched');
  t.close(at(x).mass, -2 * 0.4 * M.pmDeriv(g, x), 1e-10, "the inner mass is scaled by g'");
});

// ------------------------------------------ the document's worked examples
test('Example 5.5 (ex:displaced): union conditioning moves the mass off p_3',
     'rigor/network_corner_calculus.tex, ex:displaced', t => {
  const l = [1.3, 2.1, 0.9, 1.7];
  const p = [0]; for (const li of l) p.push(p[p.length - 1] + li);   // 0,1.3,3.4,4.3,6.0
  const s1 = M.sigmaOf(l[2], l[3]);                                   // A_B = A_3, A_new = A_4
  const s2 = M.sigmaOf(l[1] + l[2], l[0]);                            // A_B = A_2A_3 (a union)
  t.close(s1, 1.452991, 5e-7, 'sigma_1 = 2 l4/(l3(l3+l4))');
  t.close(s2, 0.201550, 5e-7, 'sigma_2 = 2 l1/((l2+l3)(l1+l2+l3))');
  const steps = [
    { p: p[2], sigma: s1, side: 'R', moving: [p[2], p[4]] },          // corner p_3, M_1 = A_3A_4
    { p: p[3], sigma: s2, side: 'L', moving: [p[0], p[3]] }           // corner p_4, M_2 = A_1A_2A_3
  ];
  const H = M.hypothesisH(steps);
  t.ok(!H.holds, '(H) fails: p^(1) lies inside M_2');
  const G = M.theoremGeneral(steps, [p[0], p[4]]);
  t.ok(!G[0].swallowed && G[0].displaced, 'corner 1 is displaced, not swallowed');
  t.close(G[0].x, 3.200568, 5e-7, 'x_0 = k_2^{-1}(p_3)');
  t.close(G[0].gprime, 0.670114, 5e-7, "k_2'(x_0)");
  t.close(G[0].mass, -1.947339, 5e-7, 'the displaced mass');
  t.close(G[1].mass, -2 * s2, 1e-12, 'the mass at p_4 is -2 sigma_2');
  const total = G[0].mass + G[1].mass, naive = -2 * (s1 + s2);
  t.close(total / naive, 0.71, 5e-3, 'total is 71% of the naive corner measure');
  const S = M.pmSchwarzian(M.composeSteps(steps, [p[0], p[4]]));
  t.eq(S.length, 2, 'the composite really has two masses');
  t.close(S[0].x, G[0].x, 1e-8, 'Thm 5.2 position = the composite map’s own jump');
  t.close(S[0].mass, G[0].mass, 1e-8, 'Thm 5.2 mass = the composite map’s own jump');
  t.close(S[1].mass, G[1].mass, 1e-8, 'and at p_4 too');
});

test('Example 5.6 (ex:swallow): the first corner contributes nothing',
     'rigor/network_corner_calculus.tex, ex:swallow', t => {
  const p = [0, 1, 2, 3];
  const s1 = M.sigmaOf(1, 1), s2 = M.sigmaOf(1, 1);
  t.close(s1, 1, 1e-12, 'sigma_1 = 1');
  const steps = [
    { p: p[1], sigma: s1, side: 'R', moving: [p[1], p[3]] },   // degenerate step: corner is the far end
    { p: p[2], sigma: s2, side: 'L', moving: [p[0], p[2]] }
  ];
  t.ok(!M.hypothesisH(steps).holds, '(H) fails although both A_B are single intervals');
  const G = M.theoremGeneral(steps, [p[0], p[3]]);
  t.ok(G[0].swallowed, 'corner 1 is swallowed by step 2');
  const P = M.composeSteps(steps, [p[0], p[3]]);
  t.close(M.pmEval(M.pmStep(p[2], s2, 'L'), p[0]), 4 / 3, 1e-12, 'k_2(p_1) = 4/3, so p_2 is out of range');
  const S = M.pmSchwarzian(P);
  t.eq(S.length, 1, 'only one mass survives');
  t.close(S[0].x, p[2], 1e-10, 'it sits at p_3');
  t.close(S[0].mass, -2 * s2, 1e-10, 'and equals -2 sigma_2');
});

// ----------------------------------------------------- the VWZ protocols
test('VWZ 1(B) = 1(A) as point maps, for every rotation t', 'Prop. 8.2', t => {
  const [a, b, c, d] = [1.1, 0.8, 1.4, 0.6];
  const p2 = a, p5 = a + b + c + d;
  for (const tt of [0, 0.25, 1.0]) {
    const th = M.thetaT(tt);
    const sA = th * 2 * (c + d) / (b * (b + c + d));
    const s1 = th * 2 * c / (b * (b + c)), s2 = th * 2 * d / ((b + c) * (b + c + d));
    t.close(s1 + s2, sA, 1e-12, 'sigma_1 + sigma_2 = sigma_{1(A)} at t=' + tt);
    const B = M.composeSteps([{ p: p2, sigma: s1, side: 'R' }, { p: p2, sigma: s2, side: 'R' }], [0, p5]);
    const A = M.composeSteps([{ p: p2, sigma: sA, side: 'R' }], [0, p5]);
    for (const x of [0.3, 1.5, 2.9, 3.8]) t.close(M.pmEval(B, x), M.pmEval(A, x), 1e-11, 'maps agree at ' + x);
  }
});

test('VWZ Protocol 3: both orders, one double corner at p_3, zeta_eff', 'Thm. 8.5', t => {
  const [a, b, c, d] = [1.1, 0.8, 1.4, 0.6];
  const p1 = 0, p3 = a + b, p5 = a + b + c + d;
  const s1 = M.sigmaOf(b, a), s2 = M.sigmaOf(c, d);
  const left = { p: p3, sigma: s1, side: 'L', moving: [p1, p3] };
  const right = { p: p3, sigma: s2, side: 'R', moving: [p3, p5] };
  t.ok(M.hypothesisH([left, right]).holds, '(H) holds: both corners coincide');
  const A = M.composeSteps([left, right], [p1, p5]);
  const B = M.composeSteps([right, left], [p1, p5]);
  for (const x of [0.2, 1.4, 2.6, 3.7]) t.close(M.pmEval(A, x), M.pmEval(B, x), 1e-11, 'orders agree at ' + x);
  const S = M.pmSchwarzian(A);
  t.eq(S.length, 1, 'one mass');
  t.close(S[0].mass, -2 * (s1 + s2), 1e-10, 'mass = -2(sigma_1+sigma_2)');
  // ... and the map is the over-compressed Theorem-A step up to a global Moebius map
  const R = M.pmStep(p3, s1 + s2, 'R'), g = M.parabolicLeft(p3, s1);
  for (const x of [0.2, 1.4, 2.6, 3.7]) t.close(M.pmEval(A, x), M.apply(g, M.pmEval(R, x)), 1e-10, 'Phi^(3) = M o R at ' + x);
  const zEff = (s1 + s2) * M.betaI(p3, p1, p5);
  t.close(zEff, (s1 + s2) * (a + b) * (c + d) / (a + b + c + d), 1e-12, 'zeta_eff of eq. (33)');
  const sPrime = (s1 + s2) * (c + d);
  t.ok(sPrime > 2 * d / c, 's′ > 2 lambda′: the effective step is over-compressed');
});

// ----------------------------------------------- the published n=4, n=5 tables
test('Table 1 (n=4, equal lengths): the published zeta of every starting pair',
     'rigor/network_corner_calculus.tex, tab:n4', t => {
  const l = [1, 1, 1, 1], p = [0, 1, 2, 3, 4], T = 4;
  const sR = k => M.sigmaOf(l[k - 2], l[k - 1]);            // adjoin A_k on A_{k-1}
  const sL = k => M.sigmaOf(l[k], l[k - 1]);                // adjoin A_k on A_{k+1}
  const z = (kappa, x) => kappa * M.betaI(x, p[0], p[4]);
  t.close(z(sR(3), p[1]), 0.75, 1e-12, 'start A_1A_2: zeta at p_2');
  t.close(z(sR(4), p[2]), 1.00, 1e-12, 'start A_1A_2: zeta at p_3');
  t.close(z(sL(1) + sR(4), p[2]), 2.00, 1e-12, 'start A_2A_3: double corner at p_3');
  t.close(z(sL(1), p[2]), 1.00, 1e-12, 'start A_3A_4: zeta at p_3');
  t.close(z(sL(2), p[3]), 0.75, 1e-12, 'start A_3A_4: zeta at p_4');
  t.eq(T, p[4] - p[0], 'T = 4');
});

test('Table 2 (n=5, l=(1.0,1.3,0.7,1.9,1.1)): the published zeta of the L->R chain',
     'rigor/network_corner_calculus.tex, tab:n5', t => {
  const l = [1.0, 1.3, 0.7, 1.9, 1.1];
  const p = [0]; for (const li of l) p.push(p[p.length - 1] + li);
  const z = (kappa, x) => kappa * M.betaI(x, p[0], p[5]);
  t.close(z(M.sigmaOf(l[1], l[2]), p[1]), 0.4487, 5e-5, 'zeta at p_2');
  t.close(z(M.sigmaOf(l[2], l[3]), p[2]), 2.9614, 5e-5, 'zeta at p_3');
  t.close(z(M.sigmaOf(l[3], l[4]), p[3]), 0.5789, 5e-5, 'zeta at p_4');
  t.close(p[5], 6.0, 1e-12, 'T = 6.0');
});

test('order independence under (H), and its failure without it', 'Thm. 5.3, Rem. 9.3', t => {
  const l = [1.0, 1.3, 0.7, 1.9], p = [0]; for (const li of l) p.push(p[p.length - 1] + li);
  const add = (lB, lNew, corner, side, mv) => ({ p: corner, sigma: M.sigmaOf(lB, lNew), side, moving: mv });
  // start A_2A_3; LR and RL, both with single-interval conditioning
  const L = add(l[1], l[0], p[2], 'L', [p[0], p[2]]);        // adjoin A_1 on A_2, corner p_3
  const R = add(l[2], l[3], p[2], 'R', [p[2], p[4]]);        // adjoin A_4 on A_3, corner p_3
  t.ok(M.hypothesisH([L, R]).holds && M.hypothesisH([R, L]).holds, '(H) holds both ways');
  const SA = M.pmSchwarzian(M.composeSteps([L, R], [p[0], p[4]]));
  const SB = M.pmSchwarzian(M.composeSteps([R, L], [p[0], p[4]]));
  t.close(SA[0].mass, SB[0].mass, 1e-10, 'the corner measure does not see the order');
  t.close(SA[0].mass, -2 * (L.sigma + R.sigma), 1e-10, 'and equals the junction form');
  const km = M.cornerMeasure([L, R]);
  t.close(km[0].kappa, L.sigma + R.sigma, 1e-12, 'kappa at p_3');
});
