# Referee report — `repo-split-public-private` (REF-INFRA-1, 2026-09-20)

Verdict: **pass** — every number reproduces, the public clone builds, sets are disjoint.

## Claimed vs measured

| Claim | Claimed | Measured |
|---|---|---|
| public files / size | 405 / 5.9 MB | 405 / 5,888,415 B = 5.89 MB |
| private files / size | 228 / 47.7 MB | 228 / 47,750,584 B = 47.75 MB (truncated) |
| overlap public ∩ private | 0 | 0 |
| tracked by neither / size | 331 / 196 MB | 331 (+1, my packet) / 196,019,119 B |
| excerpts / source PDFs | 178 / 47 | 178 / 47 |
| result captures | 97 | 97 tracked `.out` |
| call sites / documents | 255 / 19 | 255 / 19 |
| python scripts / literals | 24 / 37 | 24 / 37 (diff of f9ffae4) |
| refs listed / fetchable / library | 36 / 20 / 16 | 36 / 20 / 16 |
| network_corner_calculus | 42 pp with images | 42 pp, 10 images, 0 placeholders |
| remotes | none | none in either repo |

## Tests

1. **Layout.** Both git dirs present; private has `core.bare=false`, `core.worktree` =
   project root. `./pgit check` → overlap 0, shots 178/178.
2. **Coverage.** The 331 untracked files are 96 `.npz`, 77 `.log`, 55 `.pdf`, 31 `.out`,
   31 `.aux`, 26 `.toc`, 10 `.pkl`, 6 review packets. Every untracked `.pdf` has a
   tracked `.tex` source (0 orphans); all `.npz`/`.pkl` are under `numerics/`.
   **No `.tex`, `.py`, `.sh` or `.bib` falls through** — the design property holds.
3. **With excerpts.** `quadratic_limit` → 27 pp, 8 embedded images, 0 placeholders.
4. **Public clone** (`git archive HEAD | tar -x`; 405 files, no `shots/`, no PDFs):
   compiles → 26 pp, 0 images, 8 placeholders for 8 call sites, exact 1:1 degradation.
   All 19 converted documents: **17 build**; the 2 failures fail *identically in the
   local tree with excerpts present*, so the conversion breaks nothing.
5. **`pgit sync`.** A dummy under `rigor/shots/` was invisible to both `git status -uall`
   and `./pgit status -uall`; `./pgit check` said "on disk 179, tracked 178". Dummy
   deleted, both trees clean.
6. **Python.** `grep -rl '/Users/alex' --include='*.py'` empty; all 148 `.py` compile (no
   `__pycache__` left). `_ROOT` resolves to the project root from depth 1 and 2, cwd-independently.
7. **Release safety.** LICENSE (MIT code / CC BY 4.0 docs), LICENSE-CODE, LICENSE-DOCS,
   THIRD-PARTY.md, refs/restore.sh present, public-tracked, and saying what the card says.
   `git ls-files | grep -E 'shots/|\.pdf$'` empty. **Public history: 413 distinct paths
   ever, 0 matching `shots/` or `.pdf`; largest blob 0.30 MB** — a later push is safe.
   THIRD-PARTY.md's "221 citedbox" also reproduces exactly.

## Defects (none fatal)

- **`next` understates.** It names one non-building document; CHECKLIST.md item 2 says
  *two*. The second fails from a different cause: `referee_implementation_C11` dies at
  l.364 on an undefined `\one`, not the `\lqed` arity. Both pre-existing — the release
  commit's diff for that file is shot conversion only (0 other changed lines).
- **CHECKLIST.md item 4 is off.** It claims thirteen `.out`/`.txt` carry the absolute
  path; measured 12 (10 `.out`, 2 `.txt`), and 14 tracked files once `F2_RESULTS.md` and
  `results_hp14_L120.err` are counted. 31 literal occurrences remain.
- **A second path class is missed entirely.** 10 public-tracked files — 4 `.sh`
  (`numerics/run_hp14.sh`, `run_largezeta.sh`, `run_largezeta2.sh`, `certified/runhp.sh`)
  plus `rigor/README_AGENTS.md` — hardcode a scratchpad venv interpreter that **no longer
  exists**; the portability work covered `.py` only.
- Omitted risks are covered in evidence docs (`git clean -xfd` and the second-machine
  two-clone recipe are in PRIVATE.md, repeated in README_AGENTS.md 4-5). `./pgit check`
  *reports* a shots mismatch but still exits 0, so it is not usable as a CI gate.

## Delta review (REF-INFRA-2)

Verdict: **fail** — one false knowledge-base claim; every other changed claim reproduces.

`gh repo view` says **PRIVATE** for both `cft-cmi` and `cft-cmi-private`; local HEAD =
`origin/main` = `ls-remote` in both (`2bb943f`/`32d7556`), trees clean. Fresh clone of the remote:
**406** files / 5,892,618 B (card: 406 / 5.9 MB), **406 paths ever added, 0 matching `shots/` or
`.pdf`** — history claim holds. `quadratic_limit` builds 27 pp / 8 images locally, 26 pp / 0 in
the clone, as claimed. The four run scripts carry `PY="${PYTHON:-python3}"` and pass `bash -n`;
**no tracked executable** names the dead interpreter, and only the seven captures/briefs CHECKLIST
item 4 allows still do. `next` is right: `implementation_C11`:486 `\lstep{1}{4}{\lqed}` vs
`\lqed[2]` → "Missing number" (TeX says l.488); `referee_implementation_C11`:364 `$\mathbb C\one$`
→ "Undefined control sequence". KB: separate repo at `origin/main`, `kb sync` touches only `git -C
kb`, lint 0 issues, the seven packets in `rigor/` tracked by neither.

**Fatal.** "only two pointers (`doc:refs/VWZ_2307.14434.pdf`) reach into the private repo" is
false: **10 occurrences (9 distinct) on 8 cards** reach 8 private files — 6 `refs/*.pdf` (VWZ ×1,
AlbertiUhlmann02 ×3, BJL, CDIT, Sion1958, Uhlmann76 = 8) plus `doc:CHECKLIST.md` and
`doc:PRIVATE.md`; PRIVATE.md repeats it. **Minor.** "128 … pointers" is 129 (this edit added
`doc:rigor/referee_repo_split.md`); 0 genuinely fail — a naive regex shows 7 (4 trailing stops, 2
prose `doc:...`, 1 prose `num:f3_t0.py`). **Recipe** does rebuild the tree (178 shots, 47 PDFs,
overlap 0, 27 pp / 8) but `clone --bare` sets no fetch refspec or upstream: `./pgit push` dies "no
upstream branch", `origin/main` is unknown, and untracked `info/exclude` leaves `./pgit status`
showing 162 stray files.

## Third pass (REF-INFRA-2b)

Verdict: **fail** — the repaired recipe is right and fully verified; four numbers are not.

**(c) verified.** PRIVATE.md's recipe, run verbatim: `main@{upstream}` = `origin/main`, `./pgit status` and `git status` both 0,
`./pgit check` exits 0 (406/229, overlap 0, shots 178/178), `info/exclude` self-installed byte-identical to `pgit-exclude`, 178
shots + 47 PDFs restored, `quadratic_limit` builds **27 pp / 8 images**.

**(1)** Public is **406** (`git ls-files`), not 407; 229 private is right (`pgit-exclude` is gitignored publicly). **(2)** My rule:
322 cards in `areas/ claims/ evidence/`, tokens `(doc|num|data|ref):PATH`, anchor+trailing punctuation stripped, deduped by PATH →
**130** targets, 129 existing, the one miss (`f3_t0.py`) prose in referee notes, so 0 genuinely fail; front-matter `evidence:` alone
gives **129**, `ev:` 131, zero `data:` tokens — no rule yields 132. **(3)** The 8 private targets are cited by **8** cards; 9 needs
generated INDEX.md or CHANGELOG.md counted as a card. **(4)** `restore.sh` refetches **one** of the six: CDIT is listed as `CDIW21`,
so `getref.sh` writes `refs/CDIW21_1808.02384.pdf` and `ref:refs/CDIT_1808.02384.pdf` stays broken; of the other four only Uhlmann76
is paywalled (AlbertiUhlmann02, BJL are arXiv, Sion1958 free msp; none in restore.sh's table).
