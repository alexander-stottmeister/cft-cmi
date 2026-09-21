# REF-MOD710 — site modules 7-10 and the extra extractor (2026-09-21) — FAIL, nine repairs

Scope: `docs/explore/{separation,off-criticality,relative-entropy,claim-map}.html`, `docs/lib/separation.js`, `docs/lib/extra.css`, `tools/build_site_data_extra.py`, against `rigor/public_site_plan.md` §2 rows 7-10. Method: a jsdom run of each page (boot, every slider, button, select and search, arrow keys on every handle, theme, three failure injections), 12 guard-break tests in a symlink shadow tree, a walk of all 88 claim-map cards, a 30-record provenance audit. Nothing was modified.

## What holds
`--check` is byte-exact, exit 0, from the repository root **and from /tmp** (REF-MOD345 R3 does not recur: `ROOT = Path(__file__).resolve().parent.parent`). Breaking one digit of `ref_p6_3_separation.out` → `DRIFTED`, exit 1. Twelve guard breaks all raised Drift: five column headers (thermal, gap, c-function, two-branch, separation), four `declare` units (`beta_len = 2 beta`, `kappa_F L_B/beta`, `PRIMARY DEFINITION c_M := c_M^(2)`, the `1/kappa_c` caption), the gap geometry `for L in (6, 8, 12)` read from the driver, the mass ladder, and the 14/5-row counts. No record comes from `docs/results/`; all nine sources are git-tracked; 30/30 sampled numbers verify at the exact file and line their record names.

**M7:** `separation.js` reproduces 6.8134, 20.0499, 66.6817, 200.0050, 666.6682 exactly; its quadratic `(c+1)E²−(4/ζ+2c)E+(c−1)=0`, the degenerate last corner `E = 1+2/ζ`, `γ = 2/(E−1)` and the fixed point `2ε/(2−ε)` all re-derive from Lemma 10.3 / Theorem 11.1, `zetaOf` round-trips to 1e-16, and the lede's 2.2 % and two-parts-in-a-million are the recorded ratios 1.022015 and 1.000002. The page says "approached, never attained" in the lede, the theorem box, the static figure and the third panel's heading.
**M8:** the live gap law reproduces the pipeline's own `I_cont` to 4.6e-7 and the live KMS form reproduces `CMI_cont` to 4.0e-8 at the pipeline's integer `L_B` — the 5e-7 claim holds. Every lattice value is a record, none recomputed. The page correctly says the rates are fitted only at β = 4 and 8 (the `.out` has 6 fit rows at those two; `thermal_rg_gap_summary.md:29` still tables a β = 16 fit the `.out` no longer carries).
**M9:** both bracket ends carry `conditional` with hypotheses named ((V), open; H3 + Araki, NOT OBTAINED, Gap RK2), s₂ is `conjectural` throughout, and the refuted lemma states what it asserted, the true infimum and why it fails.
**M10, recomputed:** 88 cards, 8 areas, 147 edges, 10 private pointers over 8 files, 245 public, 8 kb, 0 missing. The one never-refereed card is chipped in list, graph title and detail head; 0 of 10 private pointers became links; all 303 rendered links resolve to tracked files; the test is `git ls-files` on both repositories, with a Drift if it returns nothing.
Inherited fixes that do reach these pages: `draggable()` rewrites `role="img"` → `role="group"` on `#zplot` (R6); arrow keys move `aria-valuenow` the right way; `color-scheme` is declared; `#main` has `tabindex="-1"`; every static figure uses theme tokens, so the theme button no longer inverts it.

## Repairs required
- **D1** `off-criticality.html:119` "A 2–3% overshoot c_M > 1 at R = 6, 8" is the `c_M^(Rich)` column, which the page never plots and the extractor excludes by name. The plotted `c_M = c_M^(2)` reaches 1.1079 (m = 0.05, R = 6) and stays > 1 to R = 14; at m = 0 both c_M and c_E exceed 1 at every R. State the plotted values.
- **D2** `off-criticality.html:293-296` `liveBadge` hardcodes `badge proved` over panels of `numerical` records — on the thermal panel, above the words "the rates are fits". Use `badge('numerical')`, or drop the cell.
- **D3** `off-criticality.html:69` "confirmed to 0.06%" holds only at L = 12 (0.055%); the panel defaults to L = 6, where I/I_cont = 1.00116. Say "0.06% at L = 12, 0.12% at L = 6".
- **D4** `off-criticality.html:468` labels `(c_M/c_E)/(mR)` "→ 1 in the infrared" beside 0.5632 (m = 1.6) and 4.0609 (m = 0.05, R = 6). Name the mass: it reaches 1 only near m = 0.4 (1.196, 1.078, 1.020 at R = 6, 10, 16).
- **D5** `separation.html:377` `r.label.split(':')[0].split('(')[0]` renders two checks as the bare word "min" and one as "e^{Delta_{n-1}}/". One "min" is 0.999999996, which reads as breaking the page's own bound; it is a 400000-chain float scan, against the exact rational 1.000000276. Print the full label and mark which is float.
- **D6** `separation.html:247` `rec()` returns `undefined` for a missing record and `renderRecord` prints "—" while `has-js` stays on: the page shows blanks instead of falling back, unlike the other three. Throw, as `D.get` does.
- **D7** `tools/build_site_data_extra.py:503` gives `gauge.factor` status `refuted`, so module 9 badges the true infimum 11.09 as refuted while the plot colours it `--proved`. Make it `proved`; the lemma cell carries the refutation already.
- **D8** all four pages, head script line 16: `addEventListener('error', …)` has no capture flag although its comment claims one, so a blocked ES module still never reaches it. Append `, true` (REF-MOD345 R4, half done).
- **D9** the card's note says 2 never refereed and 3 awaiting; the live extraction gives 1 and 1, and its Statement still says "86 cards" against 88. Re-note it. (Recording any verdict on this card drifts `extra-claim-map.json`, so `make data` must follow.)

## Shared files, for central repair
`docs/lib/plot.js:46` — `fmt` still emits `×10^-4` where `ui.js` emits `×10⁻⁴`; both appear in one readout list on module 8 and in module 7's `aria-valuetext`. `docs/lib/site.css:134` — `table { display: block }` still strips the table role from "Claims this module carries" on all four pages. Nits: `claim-map.html` `#graph` keeps `role="img"` over 88 clickable non-focusable nodes, pruning the `<title>`s that carry "never refereed" (the list beside it is the working keyboard path); module 8's thermal curve is evaluated at non-integer `L_B = x·β` while the source prints `x` to two decimals, so the dots sit up to 4% off the curve at β = 32. `docs/lib/extra.css` is clean: every colour is a site.css token, so both themes follow.

## Second pass — REF-MOD710b (2026-09-21) — FAIL, four repairs, all in `off-criticality.html`

Re-verified fixed: D2 (`liveBadge` takes a status; both call sites read `numerical` and name closed form vs
lattice fit, the thermal one adding "at two temperatures only"), D5 (full check labels, no bare "min"), D6
(a missing record throws; both injections drop `has-js` and show the notice), D7 (11.09 now `proved`). Shared:
`plot.js` `fmt` and `ui.js` `fmtValue` agree — `3.91111×10⁻⁴` beside `9.25215×10⁻⁸` in one readout; `table`
keeps its role inside `.table-wrap`, 11/11 pages wrapped; all 11 head scripts parse and a non-bubbling resource
error now drops `has-js` on all four pages; `#zplot` and `#graph` are `group`. `--check` exit 0 from root and
/tmp; claim map recounts to 88/8/147, 12 private pointers over 9 files (`plan_page/petz_program_plan.html` left
the public index and the git test followed it), 0 rendered as links, 301/301 links tracked, the "awaiting a
pass" chip now exercised.

- **E1** `:468` prints `fmt(S.m, 3)` — the slider *index*, not the mass: "at m = 6" for m = 1.6 and "at m = 1"
  for m = 0.05. Use `fmt(Number(m), 3)`; `m` is already bound on line 459.
- **E2** `:468` "tending to 1 as mR grows" is false for m ≥ 0.4, which settle at 0.972, 0.825 and 0.563 at
  R = 40. Say it approaches 1 from above for m ≤ 0.2 and lands below 1 for the heavier masses.
- **E3** `:119` "The Richardson-extrapolated column overshoots by 2–3%, c_M > 1, at R = 6, 8 does not collapse"
  has no main verb, and the plotted `c_M^(2)` overshoot is still unstated: 1.1079 at m = 0.05, R = 6, above 1
  to R = 14, and above 1 at every R when m = 0, where c_E is too. Name both columns.
- **E4** `:69` "to 0.116% at the default block length and to 0.06% at L_G = 96" reads as two gaps; both are at
  L_G = 96 and differ by L. Write "at L_G = 96, to 0.116% at L = 6 (the default) and 0.055% at L = 12".
