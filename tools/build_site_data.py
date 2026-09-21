#!/usr/bin/env python3
"""Build docs/data/*.json for the interactive site from the repository's result files.

Every record carries its provenance:

    {"value": <float|null>, "error": <float|null>, "source": "<repo path>",
     "line": <1-based line number>, "status": "<proved|certified|numerical|...>", ...}

A number with no source file does not go in.  The site renders the source under
every number, so a reader can open the file and check the digit.

Usage
-----
    python3 tools/build_site_data.py            # write docs/data/*.json
    python3 tools/build_site_data.py --check    # re-extract, diff, exit 1 on drift

`--check` is byte-exact: the output carries no timestamp, so a difference means
either a source file moved under the JSON or the JSON was edited by hand.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data"

# --------------------------------------------------------------------------
# status vocabulary
#   proved     a theorem, the value is a closed form
#   certified  a rigorous bound (ball arithmetic / spectral window lower bound)
#   numerical  a measurement or an extrapolation, with an error bar where known
# --------------------------------------------------------------------------

_NUM = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"


class Drift(Exception):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read(relpath: str):
    """Return (relpath, [lines]).  Raises if the source has disappeared."""
    p = ROOT / relpath
    if not p.is_file():
        raise Drift("source file missing: %s" % relpath)
    return relpath, p.read_text(encoding="utf-8").splitlines()


def q(x):
    """Round a float to 12 significant digits: enough for every source we read,
    and it keeps rescaling (the 10^2 of the large-zeta table) free of binary dust."""
    if isinstance(x, float) and math.isfinite(x):
        return float("%.12g" % x)
    return x


def record(rid, value, error, source, line, status, **extra):
    r = {
        "value": q(value),
        "error": q(error),
        "source": source,
        "line": line,
        "status": status,
        "id": rid,
    }
    r.update({k: v for k, v in extra.items() if v is not None})
    return r


def clean(cell: str) -> str:
    """Strip the LaTeX / Markdown decoration a table cell may carry."""
    s = cell.strip()
    s = s.replace("\\(", "").replace("\\)", "").replace("\\,", "")
    s = s.replace("**", "").replace("`", "").replace("$", "")
    s = re.sub(r"\\[a-zA-Z]+\{", "", s)
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return s.strip()


def parse_paren(cell: str):
    """'0.008444(1)' -> (0.008444, 1e-06); '3.14' -> (3.14, None); '--' -> (None, None).

    The parenthesis convention is the usual one: the digits in brackets are the
    uncertainty in the last digits of the mantissa.
    """
    raw = clean(cell)
    m = re.fullmatch(r"(%s)\((\d+)\)" % _NUM, raw)
    if m:
        mant, unc = m.group(1), m.group(2)
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return float(mant), int(unc) * 10.0 ** (-dec)
    if re.fullmatch(_NUM, raw):
        return float(raw), None
    return None, None


def leading_number(cell: str):
    """The first number in a cell that carries extra prose.  Used only where the
    calling site says in a comment why taking the first number is the right read."""
    m = re.search(_NUM, clean(cell))
    return float(m.group(0)) if m else None


def tex_rows(relpath: str, lines, label: str):
    """Yield (lineno, [cells]) for the body rows of the tabular carrying \\label{label}."""
    start = None
    for i, ln in enumerate(lines):
        if "\\label{%s}" % label in ln:
            start = i
            break
    if start is None:
        raise Drift("label %s not found in %s" % (label, relpath))
    mid = None
    for i in range(start, len(lines)):
        if "\\midrule" in lines[i]:
            mid = i
            break
    if mid is None:
        raise Drift("no \\midrule after %s in %s" % (label, relpath))
    buf, first = [], None
    for i in range(mid + 1, len(lines)):
        if "\\bottomrule" in lines[i]:
            if buf:
                raise Drift("unterminated row before \\bottomrule in %s" % relpath)
            return
        body = lines[i].strip()
        if not body or body.startswith("%"):
            continue
        if first is None:
            first = i + 1
        buf.append(body)
        joined = " ".join(buf).rstrip()
        if not re.search(r"\\\\(\[[^\]]*\])?$", joined):
            continue                      # the row continues on the next line
        joined = re.sub(r"\\\\(\[[^\]]*\])?$", "", joined).rstrip()
        yield first, [c.strip() for c in joined.split("&")]
        buf, first = [], None
    raise Drift("no \\bottomrule after %s in %s" % (label, relpath))


def dump(name: str, payload: dict, check: bool) -> bool:
    """Write (or verify) docs/data/<name>.  Returns True when in step."""
    text = json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=False) + "\n"
    path = DATA / name
    if check:
        if not path.is_file():
            print("MISSING  docs/data/%s" % name)
            return False
        if path.read_text(encoding="utf-8") != text:
            print("DRIFTED  docs/data/%s (re-extraction differs from the committed file)" % name)
            return False
        print("ok       docs/data/%s" % name)
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote    docs/data/%s  (%d records)" % (name, len(payload.get("records", []))))
    return True


# ==========================================================================
# module 2 — the quadratic law
# ==========================================================================

def build_quadratic_law():
    """docs/data/quadratic-law.json: the measured Phi(zeta) over 0.0083 .. 17.07."""
    records = []

    # ---- high-precision scan, numerics/results_hp2.txt (kappa_c = 25.3) ------
    src, lines = read("numerics/results_hp2.txt")
    pat = re.compile(
        r"kc=(?P<kc>%s).*?zeta=(?P<zeta>%s)\s+-logF_sub=(?P<sub>%s)\s+\+tail=(?P<phi>%s)\s+"
        r"\[(?P<ratio>%s) zeta\^2\]\s+S_sub=(?P<Ssub>%s)\s+\+tail=(?P<S>%s)\s+"
        r"\[(?P<Sratio>%s) zeta\^2\]" % ((_NUM,) * 8)
    )
    n = 0
    for i, ln in enumerate(lines):
        m = pat.search(ln)
        if not m:
            continue
        n += 1
        z = float(m.group("zeta"))
        ln1 = i + 1
        records.append(record("hp2.phi.%d" % n, float(m.group("phi")), None, src, ln1,
                              "numerical", series="phi", x=z,
                              label="Phi(zeta), tail-corrected, kappa_c=%s" % m.group("kc")))
        records.append(record("hp2.phi_sub.%d" % n, float(m.group("sub")), None, src, ln1,
                              "certified", series="phi_sub", x=z,
                              label="windowed lower bound Phi_sub, kappa_c=%s" % m.group("kc")))
        records.append(record("hp2.ratio.%d" % n, float(m.group("ratio")), None, src, ln1,
                              "numerical", series="ratio", x=z, label="Phi/zeta^2"))
        records.append(record("hp2.S.%d" % n, float(m.group("S")), None, src, ln1,
                              "numerical", series="S", x=z,
                              label="relative entropy, tail-corrected"))
        records.append(record("hp2.Sratio.%d" % n, float(m.group("Sratio")), None, src, ln1,
                              "numerical", series="S_ratio", x=z, label="S/zeta^2"))
    if n != 7:
        raise Drift("expected 7 scan lines in %s, found %d" % (src, n))

    # ---- the same scan as printed in the paper, fidelity_tables.tex ---------
    src, lines = read("fidelity_tables.tex")
    for k, (ln1, cells) in enumerate(tex_rows(src, lines, "tab:scan"), start=1):
        z, _ = parse_paren(cells[0])
        for col, series, status, label in (
            (1, "phi_A", "numerical", "Phi, box Lambda=60 kmax=30 eps=1e-8"),
            (2, "phi_B", "numerical", "Phi, box Lambda=120 kmax=45 eps=1e-8"),
            (3, "phi_C", "numerical", "Phi, box Lambda=60 kmax=30 eps=1e-11"),
            (4, "ratio_C", "numerical", "Phi/zeta^2 (C)"),
            (5, "S_inf", "numerical", "relative entropy, 1/kappa_c extrapolated"),
            (6, "S_inf_ratio", "numerical", "S_inf/zeta^2"),
            (7, "cmi_ratio", "numerical", "-2 log F / I(A:C|B)"),
        ):
            v, e = parse_paren(cells[col])
            if v is None:
                continue
            records.append(record("scan.%s.%d" % (series, k), v, e, src, ln1, status,
                                  series=series, x=z, label=label))

    # ---- large cross ratio, fidelity_table_largezeta.tex --------------------
    # The table's footnote: all Phi entries are 10^2 Phi.
    src2, lines2 = read("fidelity_table_largezeta.tex")
    if "All \\(\\Phi\\) entries are \\(10^{2}\\,\\Phi\\)" not in "\n".join(lines2):
        raise Drift("the 10^2 scaling footnote of fidelity_table_largezeta.tex has changed")
    kcs = [18.4, 25.3, 32.2, 39.1, 43.8]
    for k, (ln1, cells) in enumerate(tex_rows(src2, lines2, "tab:largezeta"), start=1):
        z, _ = parse_paren(cells[0])
        best_kc, best_sub = None, None
        for j, kc in enumerate(kcs):
            v, _ = parse_paren(cells[1 + j])
            if v is None:
                continue
            best_kc, best_sub = kc, v
            records.append(record("lz.sub.%d.%s" % (k, kc), v * 1e-2, None, src2, ln1,
                                  "certified", series="lz_window", x=z, kappa_c=kc,
                                  label="windowed lower bound at kappa_c=%s" % kc))
        inf_v, _ = parse_paren(cells[6])
        best_v, best_e = parse_paren(cells[7])
        slope, _ = parse_paren(cells[8])
        lat, _ = parse_paren(cells[9])
        records.append(record("lz.bracket_lo.%d" % k, best_sub * 1e-2, None, src2, ln1,
                              "certified", series="lz_bracket_lo", x=z, kappa_c=best_kc,
                              label="certified lower end of the bracket, kappa_c=%s" % best_kc))
        records.append(record("lz.bracket_hi.%d" % k, inf_v * 1e-2, None, src2, ln1,
                              "numerical", series="lz_bracket_hi", x=z,
                              label="kappa_c -> infinity extrapolation Phi_inf"))
        records.append(record("lz.best.%d" % k, best_v * 1e-2,
                              None if best_e is None else best_e * 1e-2, src2, ln1,
                              "numerical", series="lz_best", x=z, label="best estimate of Phi"))
        records.append(record("lz.slope.%d" % k, slope, None, src2, ln1, "numerical",
                              series="lz_slope", x=z, label="d log Phi / d log zeta"))
        records.append(record("lz.lattice.%d" % k, lat * 1e-2, None, src2, ln1, "numerical",
                              series="lz_lattice", x=z,
                              label="hopping-chain lattice value at the same zeta"))

    return {
        "generator": "tools/build_site_data.py",
        "module": "quadratic-law",
        "note": ("Phi(zeta) = -log F(omega, omega-tilde) for the zero-collar compression, "
                 "free chiral fermion, c = 1.  Records tagged 'certified' are rigorous "
                 "windowed lower bounds; 'numerical' records are tail-corrected values or "
                 "extrapolations.  Entries of fidelity_table_largezeta.tex are stored "
                 "already divided by the table's 10^2 display factor."),
        "records": records,
    }


def md_table(relpath: str, lines, anchor: str, after: str = None):
    """Pipe-table parser.  `anchor` must identify the header row uniquely enough;
    `after`, when given, is a line that must precede it (several tables in
    F3_RESULTS.md share a header prefix).

    Returns (header_lineno, header_cells, [(lineno, cells), ...]).
    """
    begin = 0
    if after is not None:
        begin = next((i for i, ln in enumerate(lines) if after in ln), None)
        if begin is None:
            raise Drift("anchor line %r not found in %s" % (after, relpath))
    hdr = None
    for i in range(begin, len(lines)):
        if lines[i].lstrip().startswith("|") and anchor in lines[i]:
            hdr = i
            break
    if hdr is None:
        raise Drift("markdown table %r not found in %s" % (anchor, relpath))

    def cells_of(ln):
        # split on pipes that are not escaped, so a cell may contain \|u\|^2
        return [c.strip().replace("\\|", "|")
                for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]

    body = []
    for i in range(hdr + 2, len(lines)):          # +2 skips the |---| rule
        if not lines[i].lstrip().startswith("|"):
            break
        body.append((i + 1, cells_of(lines[i])))
    return hdr + 1, cells_of(lines[hdr]), body


# ==========================================================================
# the constants every module quotes
# ==========================================================================

def build_constants():
    records = []

    # the closed forms come from the papers, not from the generated cards, so that
    # this generator and tools/build_docs.py stay independent of each other.
    src, lines = read("paper1/app_conventions.tex")
    hit = [i for i, ln in enumerate(lines)
           if "f_2=\\frac{g_B}8=\\frac{c_{\\rm cft}}{12\\pi^2}" in ln]
    if not hit:
        raise Drift("app_conventions.tex no longer states f_2 = c_cft/(12 pi^2)")
    f2 = 1.0 / (12.0 * math.pi ** 2)
    records.append(record("f2.closed_form", f2, None, src, hit[0] + 1, "proved",
                          series="constants", x=None,
                          label="f2 = c/(12 pi^2), the Theorem-A coefficient, at c = 1"))

    src, lines = read("paper1/sec_setting.tex")
    hit = [i for i, ln in enumerate(lines)
           if "=\\frac r6\\log(1+z)=-\\frac r6\\log\\eta" in ln]
    if not hit:
        raise Drift("sec_setting.tex no longer states I(A:C|B) = (r/6) log(1+z)")
    records.append(record("cmi.coefficient", 1.0 / 6.0, None, src, hit[0] + 1, "proved",
                          series="constants", x=None,
                          label="I(A:C|B) = (c/6) log[(a+b)(b+c)/(b(a+b+c))], coefficient at c = 1"))

    src, lines = read("fidelity_tables.tex")
    rows = list(tex_rows(src, lines, "tab:second-order"))
    for k, (ln1, cells) in enumerate(rows, start=1):
        kc, _ = parse_paren(cells[1])
        if kc is None:                     # the '-> 0 / infinity' extrapolation row
            f2v, f2e = parse_paren(cells[5])
            s2v, s2e = parse_paren(cells[6])
            records.append(record("f2.measured", f2v, f2e, src, ln1, "numerical",
                                  series="constants", x=None,
                                  label="f2 measured, kappa_c -> infinity"))
            records.append(record("s2.measured", s2v, s2e, src, ln1, "numerical",
                                  series="constants", x=None,
                                  label="s2 measured, two-point 1/kappa_c extrapolation"))
            if abs(f2v - 1.0 / (12.0 * math.pi ** 2)) > 2 * (f2e or 1e-6):
                raise Drift("the measured f2 no longer agrees with c/(12 pi^2) "
                            "within twice its quoted error")
            continue
        for col, series, status, label in (
            (4, "f2_sub", "certified", "f2 windowed lower bound"),
            (5, "f2_tail", "numerical", "f2 windowed value plus tail"),
            (6, "s2_sub", "certified", "s2 windowed lower bound"),
        ):
            v, e = parse_paren(cells[col])
            if v is not None:
                records.append(record("so.%s.%d" % (series, k), v, e, src, ln1, status,
                                      series=series, x=kc, label=label))

    # The table's header scales every entry by 10^5; if that changes, every number
    # below is silently ten times wrong, so refuse rather than emit (REF-SITE-P3 D1).
    header = "\n".join(lines)
    for cell in ("10^5\\,\\Phi_{\\mathrm{sub}}",
                 "10^5\\,(\\Phi_{\\mathrm{sub}}+\\text{tail})"):
        if cell not in header:
            raise Drift("the 10^5 scaling of tab:convergence in fidelity_tables.tex "
                        "has changed: %r is gone" % cell)
    for k, (ln1, cells) in enumerate(tex_rows(src, lines, "tab:convergence"), start=1):
        lam, _ = parse_paren(cells[0])
        kmax, _ = parse_paren(cells[1])
        sub, _ = parse_paren(cells[4])
        tot, _ = parse_paren(cells[5])
        records.append(record("conv.sub.%d" % k, sub * 1e-5, None, src, ln1, "certified",
                              series="convergence_sub", x=kmax, box_lambda=lam,
                              label="Phi(1/15) windowed lower bound, Lambda=%g" % lam))
        records.append(record("conv.tail.%d" % k, tot * 1e-5, None, src, ln1, "numerical",
                              series="convergence_tail", x=kmax, box_lambda=lam,
                              label="Phi(1/15) plus tail, Lambda=%g" % lam))

    src, lines = read("paper1/app_conventions.tex")
    hit = [i for i, ln in enumerate(lines) if "\\frac{s_2}{f_2}=\\pi^2" in ln]
    if not hit:
        raise Drift("app_conventions.tex no longer states s_2/f_2 = pi^2")
    records.append(record("s2_over_f2", math.pi ** 2, None, src, hit[0] + 1, "proved",
                          series="constants", x=None, label="s2/f2 = pi^2"))

    return {
        "generator": "tools/build_site_data.py",
        "module": "constants",
        "note": ("The closed forms every module quotes, each with the file and line that "
                 "states it, beside the measurements they are compared with."),
        "records": records,
    }


# ==========================================================================
# module 3 — universality in the central charge
# ==========================================================================

def _needle_re(relpath, lines, pattern, what):
    """Like _needle, but the guard is a regular expression, for sources whose
    column padding is not part of the claim."""
    rx = re.compile(pattern)
    hit = [i + 1 for i, ln in enumerate(lines) if rx.search(ln)]
    if len(hit) != 1:
        raise Drift("%s: expected exactly one line matching %s, found %d"
                    % (relpath, what, len(hit)))
    return hit[0]


def _needle(relpath, lines, needle, what):
    """1-based line number of the unique line carrying `needle`.

    This doubles as the guard demanded by REF-SITE-P3 D1: the value below is
    written out as a closed form in Python, so if the source ever states a
    different constant the extraction must fail rather than emit a stale
    number under a live source link."""
    hit = [i + 1 for i, ln in enumerate(lines) if needle in ln]
    if len(hit) != 1:
        raise Drift("%s: expected exactly one line stating %s, found %d"
                    % (relpath, what, len(hit)))
    return hit[0]


def build_universality():
    """docs/data/universality.json: Theorem B's line, and the three c = 1 points.

    Every measurement here was made AT c = 1.  None of them is rescaled along
    the line: the line is the theorem, the points are the data, and the module
    must not blur the two."""
    records = []

    # ---- the closed forms of eq:constants, paper 1 --------------------------
    src, lines = read("paper1/app_conventions.tex")
    for rid, needle, value, label in (
        ("gb.closed_form", r"g_B=\frac{2c_{\rm cft}}{3\pi^2}", 2.0 / (3.0 * math.pi ** 2),
         "g_B = 2c/(3 pi^2), the one-particle Bures metric, at c = 1"),
        ("gkm.closed_form", r"g_{\mathrm{KM}}=\frac{c_{\rm cft}}6", 1.0 / 6.0,
         "g_KM = c/6, the Kubo-Mori metric, at c = 1"),
        ("s2.closed_form", r"s_2=\frac{g_{\mathrm{KM}}}2=\frac{c_{\rm cft}}{12}", 1.0 / 12.0,
         "s2 = c/12, the relative-entropy coefficient, at c = 1"),
    ):
        records.append(record(rid, value, None, src, _needle(src, lines, needle, rid),
                              "proved", series="closed_form", x=None, label=label))

    # ---- the stress-tensor normalisation that fixes the constant ------------
    src, lines = read("rigor/check_notes_6_7.tex")
    ln1 = _needle(src, lines,
                  r"\langle T(x)T(y)\rangle=\frac{c}{8\pi^2}(x-y-i0)^{-4}",
                  "<TT> = (c/8 pi^2) u^-4")
    records.append(record("tt.normalisation", 1.0 / (8.0 * math.pi ** 2), None, src, ln1,
                          "proved", series="closed_form", x=None,
                          label="<T(x)T(y)> = (c/8 pi^2)(x-y-i0)^-4, at c = 1"))

    # ---- the Mellin transform W-hat, and its independent numerical check ----
    src, lines = read("rigor/collar_and_invariant_formula.tex")
    ln1 = _needle(src, lines, r"=\frac{c}{24\pi}\,\frac{k(k^2+1)}{e^{2\pi k}-1},\qquad",
                  "W-hat(k) = (c/24 pi) k(k^2+1)/(e^{2 pi k}-1)")
    records.append(record("what.prefactor", 1.0 / (24.0 * math.pi), None, src, ln1, "proved",
                          series="closed_form", x=None,
                          label="W-hat(k) = (c/24 pi) k(k^2+1)/(e^{2 pi k}-1), prefactor at c = 1"))

    src, lines = read("rigor/p4_invariant.out")
    if "What(k) = (c/24pi) k(k^2+1)/(e^{2pi k}-1)" not in "\n".join(lines):
        raise Drift("p4_invariant.out no longer checks the same W-hat formula")
    hdr = _needle(src, lines, "Mellin (x-space), Re", "the x-space Mellin check table")
    n = 0
    for i in range(hdr, len(lines)):
        cols = lines[i].split()          # k | Mellin Re | Mellin Im | W-hat(k) | rel.err
        if len(cols) != 5 or not re.fullmatch(_NUM, cols[0]):
            break
        n += 1
        records.append(record("what.check.%d" % n, float(cols[3]), None, src, i + 1,
                              "numerical", series="what_check", x=float(cols[0]),
                              rel_err=float(cols[4]), mellin_re=float(cols[1]),
                              label="W-hat(k) checked against the x-space Mellin transform, k = %s"
                                    % cols[0]))
    if n != 5:
        raise Drift("expected 5 rows in the p4_invariant.out Mellin table, found %d" % n)

    # ---- the bosonic check: U(1) current net, also at c = 1 -----------------
    src, lines = read("numerics/boson/README.md")
    # The "best values" block states the measurement AND the c = 1 closed form it
    # is compared with; requiring both keeps a re-fit from arriving unannounced.
    for rid, pattern, value, err, label in (
        ("boson.f2", r"^\s*f_2 = 0\.00844 \(2\)\s+vs\s+1/\(12 pi\^2\) = 0\.0084434\s*$",
         0.00844, 2e-5, "f2 of the U(1) current net, kappa_c tail fit, c = 1"),
        ("boson.s2", r"^\s*s_2 = 0\.083\s+\(2\)\s+vs\s+1/12\s+= 0\.0833333\s*$",
         0.083, 2e-3, "s2 of the U(1) current net, kappa_c tail fit, c = 1"),
    ):
        records.append(record(rid, value, err, src, _needle_re(src, lines, pattern, rid),
                              "numerical", series="boson_best", x=None, label=label))
    ln1 = _needle(src, lines, "the c-linearity holds to 0.08%", "the boson/fermion overlap ratio")
    m = re.search(r"Tr\(B\^\*B\)/\(2E\) = \S+ = (%s)`" % _NUM, lines[ln1 - 1])
    if not m:
        raise Drift("numerics/boson/README.md no longer prints Tr(B*B)/(2E) before its 0.08% claim")
    records.append(record("boson.clinearity", float(m.group(1)), None, src, ln1, "numerical",
                          series="boson_best", x=None,
                          label="Tr(B*B)/(2E): boson and fermion vacuum overlaps agree at second order"))

    # The kappa_c ladder behind those two numbers.  Guard the header: the columns
    # ARE the spectral-window cutoffs, and a changed header would silently
    # re-label every point.
    _, hdr, body = md_table(src, lines, "| `kappa_c` | 1.58 |")
    kcs = [parse_paren(c)[0] for c in hdr[1:]]
    if kcs != [1.58, 2.31, 3.04, 3.77, 4.51, 5.24]:
        raise Drift("the kappa_c columns of numerics/boson/README.md have changed: %r" % (kcs,))
    for ln1, cells in body:
        name = clean(cells[0])
        series = {"f_2": "boson_f2_kc", "s_2": "boson_s2_kc"}.get(name)
        if series is None:
            continue
        for kc, c in zip(kcs, cells[1:]):
            v, _ = parse_paren(c)
            if v is not None:
                records.append(record("%s.%g" % (series, kc), v, None, src, ln1, "numerical",
                                      series=series, x=kc,
                                      label="%s of the U(1) current net at spectral window kappa_c" % name))

    # ---- the lattice point: one finite-zeta, finite-n measurement, c = 1 ----
    # Two conventions could silently halve this number: the table's own
    # "zeta = 2z", and its last column, headed "Phi_lat/z^2" but printing
    # Phi_lat/zeta^2 (8.520084e-06 / 0.03175^2 = 0.008454).  Guard both.
    src, lines = read("numerics/lattice/petz_lattice.out")
    head = _needle(src, lines, "[1] Phi_lat(zeta) := (1/2)(-log F^(0)) at zeta=2z", "lattice table [1]")
    if "eta_V=L^2/(L+b)^2;  z=eta/(1-eta)" not in "\n".join(lines[:head]):
        raise Drift("petz_lattice.out no longer declares its zeta = 2z convention")
    cols = _needle(src, lines, "ratio Phi_lat/z^2", "the column header of lattice table [1]")
    got = None
    for i in range(cols, len(lines)):
        f = lines[i].split()
        if len(f) != 6:
            break
        if f[0] == "0.03175":
            got = (i + 1, f)
            break
    if got is None:
        raise Drift("the zeta = 0.03175 row of petz_lattice.out table [1] is gone")
    ln1, f = got
    if abs(float(f[2]) / float(f[0]) ** 2 / float(f[5]) - 1.0) > 1e-3:
        raise Drift("petz_lattice.out table [1]: the last column is no longer Phi_lat/zeta^2")
    if abs(float(f[2]) / float(f[3]) / float(f[4]) - 1.0) > 1e-4:
        raise Drift("petz_lattice.out table [1]: the ratio column is no longer lattice/continuum")
    records.append(record("lattice.f2_point", float(f[5]), None, src, ln1, "numerical",
                          series="lattice", x=float(f[0]), n_sites=int(f[1]),
                          label="hopping chain, Phi_lat/zeta^2 at zeta = %s, n = %s sites" % (f[0], f[1])))
    records.append(record("lattice.over_continuum", float(f[4]), None, src, ln1, "numerical",
                          series="lattice", x=float(f[0]), n_sites=int(f[1]),
                          label="lattice / continuum ratio at the same zeta"))

    # ---- the two-chirality law, in units of f2 z^2 --------------------------
    src, lines = read("rigor/optimality_second_order.tex")
    ln1 = _needle(src, lines, r" \text{Petz}:\ 2\Phi(2z)=8f_2z^2+O(z^3),\qquad",
                  "the two-chirality reference values")
    records.append(record("twochirality.petz", 8.0, None, src, ln1, "proved",
                          series="two_chirality", x=None,
                          label="ordinary Petz map, 2D CFT: -log F = 8 f2 z^2 + O(z^3)"))
    records.append(record("twochirality.compression", 2.0, None, src, ln1 + 1, "proved",
                          series="two_chirality", x=None,
                          label="spatial compression, 2D CFT: -log F = 2 f2 z^2 + O(z^3)"))
    for rid, needle, value, label in (
        ("compression.per_chirality", r"gives \(\Phi(z)=f_2z^2+O(z^3)\) per chirality", 1.0,
         "zero-collar compression, per chirality: -log F = f2 z^2 + O(z^3)"),
        ("petz.per_chirality", r"against the Petz \(\Phi(2z)=4f_2z^2+O(z^3)\)", 4.0,
         "ordinary Petz map, per chirality: -log F = 4 f2 z^2 + O(z^3)"),
    ):
        records.append(record(rid, value, None, src, _needle(src, lines, needle, rid),
                              "proved", series="two_chirality", x=None, label=label))

    return {
        "generator": "tools/build_site_data.py",
        "module": "universality",
        "note": ("Theorem B says the second-order coefficient is linear in the central charge: "
                 "f2 = c/(12 pi^2).  The line is the theorem.  Every measurement here — Dirac "
                 "fermion, U(1) current net, hopping chain — was made AT c = 1 and is stored at "
                 "c = 1; none of them is evidence at any other c, and none may be scaled along "
                 "the line."),
        "records": records,
    }


# ==========================================================================
# theta: the first-order gain constant (modules 4 and 5)
# ==========================================================================

def build_theta():
    src, lines = read("numerics/optimality_all/F3_RESULTS.md")
    records = []
    joined = "\n".join(lines)

    def scalar(rid, pattern, status, label):
        m = re.search(pattern, joined)
        if not m:
            raise Drift("pattern %r not found in %s" % (pattern, src))
        ln1 = joined[:m.start()].count("\n") + 1
        err = float(m.group(2)) if m.lastindex and m.lastindex >= 2 else None
        records.append(record(rid, float(m.group(1)), err, src, ln1, status,
                              series="constants", x=None, label=label))

    scalar("theta", r"\*\*theta = (0\.\d+) \+- (0\.\d+)\*\*", "numerical",
           "theta, five mesh families, h -> 0")
    scalar("one_minus_theta", r"1 - theta = (0\.\d+) \+- (0\.\d+)", "numerical",
           "1 - theta, the all-channel second-order gain")
    scalar("order_p", r"\*\*p = log2\(1/rho\) = (0\.\d+) \+- (0\.\d+)\*\*", "numerical",
           "measured convergence order in the mesh width h")
    scalar("circle_published", r"S10's (0\.\d+) \+- (0\.\d+) is a lower bound", "numerical",
           "the circle model's published value: a taper-suppressed LOWER BOUND, not an estimate")

    # h-ladder, Galerkin frame (Sec. 1(b))
    _, hdr, body = md_table(src, lines, "| h | 0.32 | 0.24 | 0.16 | 0.12 | 0.08 | 0.06 | 0.04 |")
    hs = [parse_paren(c)[0] for c in hdr[1:]]
    for ln1, cells in body:
        name = clean(cells[0])
        series = {"theta": "theta_galerkin_h", "gQ/(f2 zeta^2)": "gQ_ratio_h"}.get(name)
        if series is None:
            continue
        for h, c in zip(hs, cells[1:]):
            v, e = parse_paren(c)
            if v is not None:
                records.append(record("%s.%g" % (series, h), v, e, src, ln1, "numerical",
                                      series=series, x=h,
                                      label="%s at mesh width h, Galerkin a=1 L=2 Lambda=12" % name))

    # T0 Wiener-Hopf frame against the Galerkin frame at matched h (Sec. 3(c))
    _, hdr, body = md_table(src, lines, "| h | 0.32 | 0.24 | 0.16 | 0.12 | 0.08 | 0.06 |",
                            after="**(c) T0 reproduces the Galerkin frame at matched h**")
    hs = [parse_paren(c)[0] for c in hdr[1:]]
    for ln1, cells in body:
        name = clean(cells[0])
        if name.startswith("T0"):
            series = "theta_T0_h"
        elif name.startswith("Galerkin"):
            series = "theta_galerkin_matched_h"
        else:
            continue
        for h, c in zip(hs, cells[1:]):
            v, _ = parse_paren(c)
            if v is not None:
                records.append(record("%s.%g" % (series, h), v, None, src, ln1, "numerical",
                                      series=series, x=h, label="theta at h, frame: %s" % name))

    # the Richardson closure, one row per mesh family (Sec. 4(iii))
    _, hdr, body = md_table(src, lines, "| family | ladder | rho | theta(h_min) | theta_inf |")
    for k, (ln1, cells) in enumerate(body, start=1):
        v, e = parse_paren(cells[4])
        note = None
        if v is None:                      # family D prints '0.38369 (+~0.001 window)'
            v = leading_number(cells[4])   # the extrapolate; the bracket is a separate caveat
            note = clean(cells[4])
        hmin, _ = parse_paren(cells[3])
        records.append(record("theta_extrap.%d" % k, v, e, src, ln1, "numerical",
                              series="theta_extrap", x=hmin, label=clean(cells[0]),
                              ladder=clean(cells[1]), rho=clean(cells[2]), note=note))

    # the taper sweep that explains the published 0.300 (Sec. 5(b)); module 5 needs |u|^2
    _, hdr, body = md_table(src, lines, "| taper window uv |")
    windows = [clean(c) for c in hdr[1:]]
    for ln1, cells in body:
        name = clean(cells[0]).replace("|u|^2", "u2")
        series = {"theta": "taper_theta", "u2": "taper_u2"}.get(name)
        if series is None:
            continue
        for j, (w, c) in enumerate(zip(windows, cells[1:])):
            v, _ = parse_paren(c)
            if v is not None:
                records.append(record("%s.%d" % (series, j), v, None, src, ln1, "numerical",
                                      series=series, x=j, window=w,
                                      label="%s at taper window %s, circle model L=256" % (name, w)))

    # the circle model does not converge in 1/L (Sec. 5(a))
    _, hdr, body = md_table(src, lines, "| L | 128 | 192 | 256 |")
    Ls = [parse_paren(c)[0] for c in hdr[1:]]
    for ln1, cells in body:
        name = clean(cells[0])
        series = {"theta": "circle_theta_L", "xi_max of D": "circle_ximax_L"}.get(name)
        if series is None:
            continue
        for L, c in zip(Ls, cells[1:]):
            v, _ = parse_paren(c)
            if v is not None:
                records.append(record("%s.%g" % (series, L), v, None, src, ln1, "numerical",
                                      series=series, x=L,
                                      label="%s, circle model with the S10 taper" % name))

    # ------------------------------------------------------------------
    # module 4 — the h-ladder that is actually animated
    # ------------------------------------------------------------------
    # Family A of the Richardson table: the parameter-free T0 Wiener-Hopf frame
    # at the fixed modular window Y = Ymax = 10, four octaves of h.  The window
    # is part of the ladder's identity (Sec. 4(i) corrects for it), so refuse the
    # file if a row was taken at another window.
    lsrc, llines = read("numerics/optimality_all/f3_t0_hladder2.out")
    lpat = re.compile(r"^T0 h=(%s) Y=(%s) Ymax=(%s) N=(\d+) nA=(\d+) g/f2=(%s) theta=(%s)\b"
                      % ((_NUM,) * 3 + (_NUM,) * 2))
    n = 0
    for i, ln in enumerate(llines):
        m = lpat.match(ln)
        if not m:
            continue
        if (float(m.group(2)), float(m.group(3))) != (10.0, 10.0):
            raise Drift("f3_t0_hladder2.out line %d is no longer at Y = Ymax = 10" % (i + 1))
        n += 1
        h = float(m.group(1))
        records.append(record("theta_T0_ladder.%g" % h, float(m.group(7)), None, lsrc, i + 1,
                              "numerical", series="theta_T0_ladder", x=h, cells=int(m.group(4)),
                              label="theta at mesh width h, T0 frame, Y = Ymax = 10"))
        records.append(record("gQ_T0_ladder.%g" % h, float(m.group(6)), None, lsrc, i + 1,
                              "numerical", series="gQ_T0_ladder", x=h,
                              label="g_Q(delta-dot)/f2 at mesh width h, T0 frame"))
    if n != 5:
        raise Drift("expected 5 rungs in f3_t0_hladder2.out, found %d" % n)

    # The same Galerkin functional on the circle model's own mesh, no taper:
    # family D, and module 5's proof that the mesh is not what suppresses theta.
    mpat = re.compile(r"^MIMIC L=(\d+) a=(%s) Lg=(%s) capR=(%s) extra=(\d+) .*?"
                      r"gQ/\(f2z\^2\)=(%s) theta=(%s)\b" % ((_NUM,) * 5))
    seen = set()
    for relpath in ("numerics/optimality_all/f3_mimic.out",
                    "numerics/optimality_all/f3_mimic_big.out"):
        msrc, mlines = read(relpath)
        for i, ln in enumerate(mlines):
            m = mpat.match(ln)
            if not m:
                continue
            if (m.group(2), m.group(3), m.group(4)) != ("2.0", "1.0", "1.0"):
                raise Drift("%s line %d is no longer the (a,Lg) = (2,1) circle mesh" % (relpath, i + 1))
            if m.group(5) != "0":            # 'extra' deepens the endpoint cap (f3_mimic_deep)
                continue
            L = int(m.group(1))
            if L in seen:
                continue                     # f3_mimic_big.out repeats L = 1024
            seen.add(L)
            records.append(record("theta_mimic_L.%d" % L, float(m.group(7)), None, msrc, i + 1,
                                  "numerical", series="theta_mimic_L", x=float(L),
                                  label="theta on the circle model's own mesh, no taper, no cap"))
    if sorted(seen) != [128, 256, 512, 1024, 2048]:
        raise Drift("the circle-mesh mimic ladder has changed: %r" % (sorted(seen),))

    # ------------------------------------------------------------------
    # module 4 — what the compression is being compared with
    # ------------------------------------------------------------------
    osrc, olines = read("rigor/optimality_second_order.tex")
    ln1 = _needle(osrc, olines, r" \boxed{\;\Erec^{\text{lattice}}\;=\;(1.01\text{--}1.12)\times 2f_2z^2,",
                  "the lattice bracket of eq:main-number")
    for rid, value, label in (("lattice.best_lo", 1.01, "lowest lattice optimum, in units of 2 f2 z^2"),
                              ("lattice.best_hi", 1.12, "highest lattice optimum, in units of 2 f2 z^2")):
        records.append(record(rid, value, None, osrc, ln1, "numerical",
                              series="lattice_bracket", x=None, label=label))
    ln1 = _needle(osrc, olines, r" \qquad \frac{\Erec}{-\log\Fid_{\text{Petz}}}\;=\;0.270,\ 0.280,\ 0.284",
                  "the lattice best/Petz ratios")
    for k, v in enumerate((0.270, 0.280, 0.284), start=1):
        records.append(record("lattice.best_over_petz.%d" % k, v, None, osrc, ln1, "numerical",
                              series="lattice_best_over_petz", x=float(k),
                              label="best lattice channel / ordinary Petz map, reliable row %d" % k))

    # ------------------------------------------------------------------
    # module 4 — the KKT criterion in the parameter-free frame (T4)
    # ------------------------------------------------------------------
    ksrc, klines = read("numerics/optimality_all/F2_RESULTS.md")
    _, _, kbody = md_table(ksrc, klines, "| h | N | theta |",
                           after="### (a) h-ladder at fixed window")
    hs = [parse_paren(c)[0] for c in (row[1][0] for row in kbody)]
    if hs != [0.24, 0.12, 0.06, 0.03]:
        raise Drift("the T4 h-ladder of F2_RESULTS.md has changed: %r" % (hs,))
    for ln1, cells in kbody:
        h, _ = parse_paren(cells[0])
        # columns: h | N | theta | lam_min(M_*) | /g_Q(ddot) | /||M_*|| | ... | rank-1 gain | ...
        viol, _ = parse_paren(cells[5])
        gain, _ = parse_paren(cells[7])
        if viol is None or viol >= 0 or gain is None or gain <= 0:
            raise Drift("F2_RESULTS.md T4 row at h=%s no longer has a negative violation "
                        "and a positive rank-one gain" % h)
        records.append(record("kkt_violation_h.%g" % h, viol, None, ksrc, ln1, "numerical",
                              series="kkt_violation_h", x=h,
                              label="lam_min(M_*)/||M_*||, the condition-(a) violation at mesh width h"))
        records.append(record("kkt_gain_h.%g" % h, gain, None, ksrc, ln1, "numerical",
                              series="kkt_gain_h", x=h,
                              label="best rank-one non-isometric gain, in units of g_Q(delta-dot)"))

    # ------------------------------------------------------------------
    # module 5 — control 1: relax the taper at FIXED transition width
    # ------------------------------------------------------------------
    # Every run of the circle model, one line each, with |u|^2 beside theta.
    # |u|^2 is the health of the model: it is what tells a reader that the two
    # sharp windows and the untapered grid are answering a different question.
    csrc, clines = read("numerics/optimality_all/f3_circ_taper2.out")
    cpat = re.compile(r"^L=(\d+) a=(%s) Lg=(%s) taper=(none|smooth\((%s), (%s)\)) "
                      r"cap=(\S+) al=(%s) \|D\|=(\d+) xi=\[(%s),(%s)\] "
                      r"\|u\|\^2=(%s) theta=(%s)\b" % ((_NUM,) * 9))
    n = 0
    widths = {}
    for i, ln in enumerate(clines):
        m = cpat.match(ln)
        if not m:
            raise Drift("f3_circ_taper2.out line %d is not a run line" % (i + 1))
        if (m.group(2), m.group(3), m.group(8)) != ("2.0", "1.0", "3.0"):
            raise Drift("f3_circ_taper2.out line %d changed model: a, Lg or alpha differ" % (i + 1))
        n += 1
        L = int(m.group(1))
        lo = None if m.group(4) == "none" else float(m.group(5))
        hi = None if m.group(4) == "none" else float(m.group(6))
        width = None if lo is None else q(hi - lo)
        if width is not None:
            widths.setdefault(width, []).append((L, lo, hi))
        common = dict(x=float(L), uv_lo=lo, uv_hi=hi, width=width, cap=m.group(7),
                      cells=int(m.group(9)),
                      window=("none" if lo is None else "(%g,%g)" % (lo, hi)))
        for series, col, what in (("circ_theta_run", 13, "theta"), ("circ_u2_run", 12, "|u|^2")):
            records.append(record("%s.%d" % (series, n), float(m.group(col)), None, csrc, i + 1,
                                  "numerical", series=series,
                                  label="%s, circle model L=%d, taper %s, cap %s"
                                        % (what, L, common["window"], m.group(7)), **common))
    if n != 21:
        raise Drift("expected 21 runs in f3_circ_taper2.out, found %d" % n)
    # The whole point of control 1 is that three windows share ONE transition
    # width; if that stopped being true the control would confound again.
    matched = sorted(widths.get(0.12, []))
    if matched != sorted([(L, lo, hi) for L in (256, 512, 768)
                          for (lo, hi) in ((0.2, 0.32), (0.3, 0.42), (0.35, 0.47))]):
        raise Drift("the width-0.12 sub-sweep of f3_circ_taper2.out has changed: %r" % (matched,))

    # ------------------------------------------------------------------
    # module 5 — the referee's controls (REF-P0-TAPER, 2026-09-21)
    # ------------------------------------------------------------------
    rsrc, rlines = read("rigor/referee_taper_card.md")
    ln1 = _needle(rsrc, rlines, "**New datum the card does not have [REF].**",
                  "the referee's control runs")
    txt = rlines[ln1 - 1]
    m = re.search(r"uv=\(0\.25,0\.49\), transition width 0\.24: \\\|u\\\|\^2 = (%s) .*?"
                  r"\*\*theta = (%s)\*\*" % (_NUM, _NUM), txt)
    if not m:
        raise Drift("referee_taper_card.md no longer states the (0.25,0.49) control")
    controls = [(0.25, 0.49, float(m.group(1)), float(m.group(2)))]
    tail = txt.split("Also [REF]:", 1)
    if len(tail) != 2:
        raise Drift("referee_taper_card.md no longer lists its further controls after 'Also [REF]:'")
    for lo, hi, w, u2, th in re.findall(
            r"\((%s),(%s)\) w=(%s) -> (%s), theta=(%s)" % ((_NUM,) * 5), tail[1]):
        if abs((float(hi) - float(lo)) - float(w)) > 1e-12:
            raise Drift("referee_taper_card.md control (%s,%s) no longer has width %s" % (lo, hi, w))
        controls.append((float(lo), float(hi), float(u2), float(th)))
    if len(controls) != 3:
        raise Drift("expected three referee controls, found %d" % len(controls))
    for k, (lo, hi, u2, th) in enumerate(controls, start=1):
        common = dict(x=q(hi - lo), uv_lo=lo, uv_hi=hi, window="(%g,%g)" % (lo, hi), L=256.0)
        records.append(record("ref_control_theta.%d" % k, th, None, rsrc, ln1, "numerical",
                              series="ref_control_theta",
                              label="theta at taper window (%g,%g), L=256 [REF-P0-TAPER control]"
                                    % (lo, hi), **common))
        records.append(record("ref_control_u2.%d" % k, u2, None, rsrc, ln1, "numerical",
                              series="ref_control_u2",
                              label="|u|^2 at taper window (%g,%g), L=256 [REF-P0-TAPER control]"
                                    % (lo, hi), **common))

    # ------------------------------------------------------------------
    # module 5 — control 2: sharpen the transition at a FIXED upper edge
    # ------------------------------------------------------------------
    # This one exists in |u|^2 and, in theta, only at scattered points, so the
    # module shows |u|^2.  The widths are the axis, so a changed width list must
    # stop the build rather than silently re-label the points.
    ln1 = _needle(rsrc, rlines, "the sharpening control is complete in", "the sharpening scan")
    m = re.search(r"edge (0\.49), widths ([0-9./]+) → ([0-9., ]+); "
                  r"edge (0\.499), widths ([0-9./]+) → ([0-9., ]+)\)", rlines[ln1 - 1])
    if not m:
        raise Drift("referee_taper_card.md no longer carries the two sharpening scans")
    expect = {"0.49": ["0.40", "0.24", "0.12", "0.07"],
              "0.499": ["0.40", "0.24", "0.12", "0.039"]}
    k = 0
    for edge, ws, vs in ((m.group(1), m.group(2), m.group(3)), (m.group(4), m.group(5), m.group(6))):
        widths_l = ws.split("/")
        vals = [v.strip() for v in vs.split(",")]
        if widths_l != expect[edge] or len(vals) != 4:
            raise Drift("the sharpening scan at edge %s has changed: widths %r, %d values"
                        % (edge, widths_l, len(vals)))
        for w, v in zip(widths_l, vals):
            k += 1
            records.append(record("sharpen_u2.%d" % k, float(v), None, rsrc, ln1, "numerical",
                                  series="sharpen_u2", x=float(w), edge=float(edge),
                                  window="(%g,%s)" % (float(edge) - float(w), edge),
                                  label="|u|^2 at upper edge %s, transition width %s, L=256 "
                                        "[REF-P0-TAPER control]" % (edge, w)))

    return {
        "generator": "tools/build_site_data.py",
        "module": "theta",
        "note": ("theta = sup_G cos^2(u, v_G), the first-order gain constant.  Every entry "
                 "is a measurement, not a theorem.  The taper sweep is the mechanism by which "
                 "the circle model's published 0.300 is a lower bound, not an estimate.  "
                 "The circle runs carry |u|^2 beside theta because window position and "
                 "transition width are two different knobs: the five-window sweep of the "
                 "original card varies both at once, and the two must be shown separately "
                 "(REF-P0-TAPER, rigor/referee_taper_card.md)."),
        "records": records,
    }


# ==========================================================================
# module 6 — the corner calculus
# ==========================================================================

def _flatten(lines, start, end):
    """Join lines[start:end) into one string, keeping a char -> source-line map."""
    parts, offs = [], []
    for i in range(start, end):
        s = lines[i].strip()
        parts.append(s + " ")
        offs.extend([i + 1] * (len(s) + 1))
    return "".join(parts), offs


def _block(relpath, lines, label, env="example"):
    begin = None
    for i, ln in enumerate(lines):
        if "\\label{%s}" % label in ln:
            begin = i
            while begin > 0 and "\\begin{%s}" % env not in lines[begin]:
                begin -= 1
            break
    if begin is None:
        raise Drift("label %s not found in %s" % (label, relpath))
    for j in range(begin, len(lines)):
        if "\\end{%s}" % env in lines[j]:
            return _flatten(lines, begin, j + 1)
    raise Drift("unterminated %s for %s in %s" % (env, label, relpath))


def build_networks():
    src, lines = read("rigor/network_corner_calculus.tex")
    records = []

    def grab(text, offs, rid, pattern, status, label, **extra):
        m = re.search(pattern, text)
        if not m:
            raise Drift("pattern %r not found for %s in %s" % (pattern, rid, src))
        return records.append(record(rid, float(eval_frac(m.group(1))), None, src,
                                     offs[m.start(1)], status, label=label, **extra))

    def eval_frac(s):
        if "/" in s:
            a, b = s.split("/")
            return float(a) / float(b)
        return float(s)

    # ---- Example 5.5 (ex:displaced): the mass moves off the junction -------
    txt, offs = _block(src, lines, "ex:displaced")
    m = re.search(r"\(l_1,l_2,l_3,l_4\)=\(([-\d.,]+)\)", txt)
    if not m:
        raise Drift("ex:displaced no longer states its lengths")
    for j, val in enumerate(m.group(1).split(","), start=1):
        records.append(record("displaced.l%d" % j, float(val), None, src, offs[m.start(1)],
                              "proved", series="ex_displaced", x=j,
                              label="chain length l_%d of Example 5.5" % j))
    grab(txt, offs, "displaced.sigma1", r"\\sigma_1=2l_4/\(l_3\(l_3\+l_4\)\)=(%s)" % _NUM,
         "proved", "sigma of step 1 (adjoin A_4 on A_3, corner p_3)", series="ex_displaced")
    grab(txt, offs, "displaced.sigma2",
         r"\\sigma_2=2l_1/\(\(l_2\+l_3\)\(l_1\+l_2\+l_3\)\)=(%s)" % _NUM,
         "proved", "sigma of step 2 (adjoin A_1 on the union A_2A_3, corner p_4)",
         series="ex_displaced")
    grab(txt, offs, "displaced.mass_x0", r"-2\\sigma_1k_2'\(x_0\)=(-%s)" % _NUM,
         "proved", "Theorem 5.2 mass, displaced off the junction", series="ex_displaced")
    grab(txt, offs, "displaced.x0", r"x_0=k_2\^\{-1\}\(p_3\)=(%s)" % _NUM,
         "proved", "x_0 = k_2^{-1}(p_3), where the displaced mass sits", series="ex_displaced")
    grab(txt, offs, "displaced.k2prime", r"\$k_2'\(x_0\)=(%s)\$" % _NUM,
         "proved", "k_2'(x_0), the scaling factor of Theorem 5.2", series="ex_displaced")
    grab(txt, offs, "displaced.measured", r"Measured: \$(-%s)\$ at \$x_0\$" % _NUM,
         "numerical", "mass measured numerically by g1a_calculus.py", series="ex_displaced")

    # ---- Example 5.6 (ex:swallow): the corner is swallowed -----------------
    txt, offs = _block(src, lines, "ex:swallow")
    grab(txt, offs, "swallow.sigma1", r"\\sigma_1=2l_3/\(l_2\(l_2\+l_3\)\)=(%s)" % _NUM,
         "proved", "sigma of step 1 (adjoin A_3 on A_2, corner p_2, degenerate step)",
         series="ex_swallow")
    grab(txt, offs, "swallow.sigma2", r"\\sigma_2=(\d+)", "proved",
         "sigma of step 2 (adjoin A_1 on A_2, corner p_3)", series="ex_swallow")
    grab(txt, offs, "swallow.image_left", r"k_2\\bigl\(\(p_1,p_3\)\\bigr\)=\((\d+/\d+),2\)",
         "proved", "left end of k_2((p_1,p_3)): p_2 = 1 is not in it, so step 1 is swallowed",
         series="ex_swallow")

    # ---- Table 9.3: all n = 4 one-sided protocols, equal lengths -----------
    for k, (ln1, cells) in enumerate(tex_rows(src, lines, "tab:n4"), start=1):
        start_block = clean(cells[0])
        for zv, pk in re.findall(r"\$(%s)\$ at \$p_(\d)\$" % _NUM, cells[3]):
            records.append(record("n4.%s.p%s" % (start_block, pk), float(zv), None, src, ln1,
                                  "proved", series="table_n4", x=int(pk),
                                  start_block=start_block, orders=clean(cells[1]),
                                  label="zeta at p_%s, start %s, equal lengths" % (pk, start_block)))

    def cell_line(first_line, needle, span=6):
        """The 1-based source line carrying `needle`, searched from the row's first
        line: a tabular row may span several lines and the tuple sits on the last
        (REF-SITE-P3 D4)."""
        frag = needle.strip()[:24]
        for off in range(span):
            idx = first_line - 1 + off
            if 0 <= idx < len(lines) and frag and frag in lines[idx]:
                return first_line + off
        return first_line

    # ---- Table 9.4: n = 5, lengths (1.0,1.3,0.7,1.9,1.1) -------------------
    for k, (ln1, cells) in enumerate(tex_rows(src, lines, "tab:n5"), start=1):
        start_block = clean(cells[0])
        tup = cells[3].replace("\\,", "").strip().strip("$").strip("()")
        for j, item in enumerate(tup.split(","), start=2):
            v, _ = parse_paren(item)
            if v is None:
                continue
            records.append(record("n5.%s.p%d" % (start_block, j), v, None, src,
                                  cell_line(ln1, cells[3]), "proved",
                                  series="table_n5", x=j, start_block=start_block,
                                  orders=clean(cells[1]),
                                  label="zeta at p_%d, start %s, l=(1.0,1.3,0.7,1.9,1.1)"
                                        % (j, start_block)))

    # ---- Table 9.5: the VWZ variants and the document's own (H) verdict ----
    for k, (ln1, cells) in enumerate(tex_rows(src, lines, "tab:n4union"), start=1):
        records.append(record("vwz.%d" % k, None, None, src, ln1, "proved",
                              series="table_n4union", x=k, label=clean(cells[0]),
                              steps=clean(cells[1]), corners=clean(cells[2]),
                              hypothesis_H=clean(cells[3])))

    return {
        "generator": "tools/build_site_data.py",
        "module": "networks",
        "note": ("Worked configurations of rigor/network_corner_calculus.tex.  The module "
                 "recomputes each of them live from the Moebius algebra and shows the "
                 "document's number beside its own, so a disagreement is visible."),
        "records": records,
    }


def check_page_records(docs: Path, data: dict) -> list:
    """Every data-record="file:id" on a page must resolve to a record that exists.
    The pages use those attributes for their no-JavaScript fallbacks, so a renamed
    or deleted record would silently leave stale text behind (REF-SITE-P3 D5)."""
    import re as _re
    have = set()
    for fname, payload in data.items():
        stem = Path(fname).stem

        def walk(x):
            if isinstance(x, dict):
                if "id" in x and "value" in x:
                    have.add("%s:%s" % (stem, x["id"]))
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(payload)
    bad = []
    for page in sorted(docs.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        for m in _re.finditer(r'data-record="([^"]+)"', text):
            ref = m.group(1)
            if ref not in have:
                bad.append("%s: data-record=%r resolves to no record"
                           % (page.relative_to(docs).as_posix(), ref))
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-extract and exit non-zero if a committed JSON has drifted")
    args = ap.parse_args(argv)
    builders = (
        ("quadratic-law.json", build_quadratic_law),
        ("constants.json", build_constants),
        ("theta.json", build_theta),
        ("universality.json", build_universality),
        ("networks.json", build_networks),
    )
    try:
        payloads = [(name, fn()) for name, fn in builders]
    except Drift as exc:
        print("EXTRACTION FAILED: %s" % exc, file=sys.stderr)
        return 2
    ok = True
    for name, payload in payloads:
        ok = dump(name, payload, args.check) and ok
    if args.check and not ok:
        print("\ndocs/data is out of step with the repository's result files.\n"
              "Run: python3 tools/build_site_data.py", file=sys.stderr)
        return 1
    if args.check:
        dangling = check_page_records(Path("docs"), dict(payloads))
        for msg in dangling:
            print("  DANGLING %s" % msg, file=sys.stderr)
        if dangling:
            print("\nA page names a record that no longer exists; its no-JavaScript "
                  "fallback would show stale text.", file=sys.stderr)
            return 1
        print("  page record references: all resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
