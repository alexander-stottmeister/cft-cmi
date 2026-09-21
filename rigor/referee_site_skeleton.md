# REF-SITE-P3 — interactive site skeleton (`interactive-site`, `public-site-plan`)
2026-09-21. `docs/index.html`, `docs/explore/*.html`, `docs/lib/*`, `tools/build_site_data.py` against `rigor/public_site_plan.md`
§2 and its module 6 paragraph. **PASS** on both cards. Run, not read: `mobius.js` in node with `plan/mkStep/analyse` copied
verbatim out of `networks.html`, so the numbers below are the page's own.
## Module 6 — no defect (the item that could have taught a falsehood)
- Thm 5.2 is what is evaluated: `theoremGeneral` against the composite map's own `pmSchwarzian`, max deviation 8.9e-16
  over all nine protocols x t in {0, 0.37, 1.5}, no unmatched mass.
- (H) is tested, not inferred: over 4000 random configurations `hypothesisH` agreed *exactly* (0 mismatches) with the
  ground truth "the junction form reproduces Sch(Phi)" — 3112 hold, 888 fail.
- VWZ 1(A): (H) holds, N=1. 1(B): (H) holds, both corners p_2, conditions on the union BC. "D on C then A on BC" (EXD):
  (H) fails, p^(1)=3.4 in int M_2=(0,4.3). All three correct.
- Ex. 5.5 to the document's last digit: sigma_1 1.452991, sigma_2 0.201550, x_0 3.200568, k_2'(x_0) 0.670114, mass
  -1.947339, total 71.030% of the naive -3.309084. Ex. 5.6: corner 1 swallowed (p_2=1 outside range k_2 = [4/3,3]).
- Protocol 3 states *and measures* the Moebius quotient: max|Phi-R| = 1.768421, max|Phi-M o R| = 6.2e-15; both orders
  identical; s' = 3.95 > 2 lambda' = 1.50. Nowhere, including the static SVG, is order independence stated unconditionally.
## Defects (none blocking the pass; D1 and D7 blocking for P4 — both live in the shared layer)
- **D1 extractor.** `build_site_data.py:368,371` hard-codes `* 1e-5` for the `10^5 Phi_sub` header of `tab:convergence`
  with no guard, unlike the parallel `10^2` guard at :230. Rewriting that header to `10^6` in a scratch copy left `--check`
  at exit 0, four files "ok", while the 18 `conv.*` records were wrong by 10x. Add the same `Drift` check beside :363.
- **D7 keyboard, `plot.js`.** `render()` (:89-95) wipes and rebuilds the whole `root` subtree, destroying the focused drag
  handle; `draggable`'s keydown (:261) runs `onMove`->`setPoint`->`redraw()` synchronously and the site's only `.focus()`
  (:255) sits in the `pointerdown` branch. One arrow key moves the handle, then focus falls to `<body>`. Restore the active
  handle across `render()` by a stable `data-handle` key; and `role="slider"` (:244) has zero `aria-value*` anywhere.
- **D2 no-JS fallback.** `quadratic-law.html:170` removes `has-js` in its catch so the static figure returns;
  `geometry.html:349` and `networks.html:677` do not, so a failed data load leaves `.has-js .no-js{display:none}`
  (site.css:150) hiding it behind an empty frame — the file:// case the pages' own boot text names. Add that line to both
  catches and to `onerror`. (With JS off all four pages are correct: 1128/472/351/727 words, three with their static SVG.)
- **D3 four wrong citations, shown on the test page.** `mobius.test.js:150` `Thm. 8.4` -> **8.5** (8.4 is Prop. Protocol 2);
  `:173` "Table 9.3" -> **Table 1**; `:187` "Table 9.4" -> **Table 2**; `:198` `Rem. 9.5` -> **Rem. 9.3**, the same wrong
  number in visible page text at `networks.html:478`.
- **D4 line anchors / D5 unchecked duplicate.** The 11 `n5.*` records point at a multi-line row's first line
  (1405/1408/1411/1414); the zeta tuple is two lines below — record the cell's line. `index.html:104` hard-codes
  `0.616 +- 0.003` as the no-JS fallback for `theta:one_minus_theta`; teach `--check` the `data-record` attributes.
- **D6 non-text contrast.** `--line` is 1.35-1.54:1 on `--bg`/`--panel` in both themes and is the only boundary cue for
  `<select>`/`input[number]` (whose `--bg` fill is 1.04:1 against `--panel`) and the stroke of `svg .axis line`
  (site.css:139) — under 3:1, WCAG 1.4.11. All text passes (worst 5.02:1 light, 6.74:1 dark).
## Verified clean
282 records, 7 sources, all exist, none from `docs/results/*.md`; all 13 displayed records match their source line.
`renderRecord` throws on missing/empty/null `source`. Both named guards trip (exit 2); a one-digit tamper gives exit 1.
114 assertions / 0 failures / 14 groups, with Ex. 5.5, Ex. 5.6, Protocol 3 and the n=4 table pinning literals to the .tex.
114 links, 0 broken, no third-party host; the only `fetch` is same-origin JSON; 20 woff2 only, every `url()` in
`katex.min.css` present, KaTeX 0.18.7 MIT vendored and recorded in THIRD-PARTY.md. Badges per claim, `numerical` never
styled as `proved`, vocabulary matches `docs/status.md`. 16px gutter; tables and display math scroll locally at 390px.
Every claim in `public-site-plan`'s P3 note holds, including the 1642-char provenance text verbatim from paper1/main.tex.
