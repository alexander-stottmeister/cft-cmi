# REF-README-1 — `readme-and-figures`: pass 1 FAIL, pass 2 FAIL, **pass 3 (REF-README-1c) PASS** (2026-09-21)

**Pass 3.** The last three are closed. D8: the Kubo-Mori lower end now reads "rests on results of Araki
whose sources were NOT OBTAINED, so it too is carried as a hypothesis (Gap RK2)" — the correct one of the
four §11 dispositions, and the ends are attributed as `kubo_mori_gauge_lemma.tex` l.811/815/816 has them.
D6: the window is named and every figure reproduces — nine geometries at η_V ≤ 0.02, ratio 0.9686-0.9953
(λ=0.5), 0.9715-0.9907 (λ=1), 0.9795-0.9917 (λ=1.5), and over all 52 geometries 0.8151/0.6396/0.4111 →
"0.82, 0.64, 0.41". D7: no `superseded` badge; the README says in words that the reconciliation supersedes
the S10 value and admits no card carries that status; the SVG caption is grammatical; orphan comment gone.
No regression in D1-D5, D9, D10: `make figures` byte-identical, AST finds 0 unreachable lines, no CHECKLIST
link, `tools/check_links.py` reports 1103 links resolving with github.com the only external host.
Pass-1 table below; every row not marked a defect was verified against the cited file and still holds.

| README | claim | source | verdict |
|---|---|---|---|
| 20,128 | θ = 0.384 ± 0.003, 1−θ = 0.616 ± 0.003 | F3_RESULTS.md §4 l.13,15,163 | OK |
| 20,127 | optimum value, `numerical` + H1,H2,H3 | card `all-channel-optimum-value` | OK |
| 64-65 | f₂ = 0.008444(1), s₂ = 0.0837(5) | fidelity_tables.tex `tab:second-order` last row | OK |
| 66 | range ζ = 0.0083 … 17.067 | results_hp2.txt says **0.00833**; F2 itself says 0.00833 | minor |
| 77-79 | [0.05739, 0.06412], 0.0641(43); slope 1.29→0.69 | fidelity_table_largezeta.tex (10²Φ) | OK |
| 102 | boson 0.00844(2), 0.083(2) vs 0.0084434, 0.0833333 | numerics/boson/README.md §4 l.104-105 | OK |
| 104-105 | 0.008454 at ζ=0.03175, n=72, ratio 1.0316 | petz_lattice.out table [1] l.15 | OK |
| 110 | "What **is proved** is the bracket 0.0338c … 0.924c" | kubo_mori l.811 proved **under (V)** ((V) *open*), l.816 proved **modulo** Araki | **D8** |
| 121-125 | "`proved`. compression is **not** the minimiser" | card is **`numerical`** ("theta > 0 is numerical, not proved") | **D1** |
| 121-125 | "`proved` … optimum attained on the isometric orbit" | exact_optimum §Conditional(4): "under H3 … modulo H1,H2,H3, and (a),(e) on meshes" | **D2** |
| 142-146 | 0.3835-0.3847, 0.37442 @ h=0.02, 0.28958→0.36178 | F3_RESULTS.md §4(iii), §5(b) | OK |
| 143 | S10 value badged `superseded` | no card is `superseded`; `docs/status.md` l.17 lists 2, neither this | **D7** |
| 173-178 | −3.634274/−3.634266, x₀=3.200568, k₂′=0.670114, 71%, −2δ(p₃) | network_corner_calculus.tex l.762-767, 771-786 | OK |
| 187-194 | 2ⁿ⁻² protocols → n−1 classes; the two conjectures | true (`prop:startblock`) but **no file cited**; holonomy needs \|J₀\|≥2 | **D9** |
| 203-206 | 1.986,1.912,1.635,1.151 vs 2.00,1.90,1.70,1.20; 0.1525,0.1444,0.1357 | petz_lattice.out [3] l.287-291, [8] l.579-581 | OK |
| 205 | "reproduces −log F to ratio **1.0000** (table [2])" | 1.0000 only at λ=0, where Φ_lat ≡ ½(−log F⁰) makes it definitional; λ=0.5/1/1.5 give 0.969-0.990 | **D6** |
| 215-222 | κ_F 5.863/6.237/6.293, κ_I 3.129/3.159/3.150, gap law, 1.0006, κ_g≈0.09 | numerics/lattice/README.md §1, §3 | OK |
| 315 | "every document still compiles" | contradicts l.309 and §13 | **D4** |
| 367 | "both PDFs on disk date from 8 September" | `rigor/referee_implementation_C11.pdf` does not exist | **D5** |
| 368 | link `CHECKLIST.md` | `.gitignore:40 /CHECKLIST.md`; untracked ⇒ dead in a clone | **D3** |

**D10** `tools/make_figures.py`: 114 of 1127 lines unreachable (656-690, 778-819, 924-960), duplicated tails after a `return`; the dead copies carry divergent caption text, so a repair could silently miss.
