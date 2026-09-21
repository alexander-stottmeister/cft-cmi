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

    return {
        "generator": "tools/build_site_data.py",
        "module": "theta",
        "note": ("theta = sup_G cos^2(u, v_G), the first-order gain constant.  Every entry "
                 "is a measurement, not a theorem.  The taper sweep is the mechanism by which "
                 "the circle model's published 0.300 is a lower bound, not an estimate."),
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

    # ---- Table 9.4: n = 5, lengths (1.0,1.3,0.7,1.9,1.1) -------------------
    for k, (ln1, cells) in enumerate(tex_rows(src, lines, "tab:n5"), start=1):
        start_block = clean(cells[0])
        tup = cells[3].replace("\\,", "").strip().strip("$").strip("()")
        for j, item in enumerate(tup.split(","), start=2):
            v, _ = parse_paren(item)
            if v is None:
                continue
            records.append(record("n5.%s.p%d" % (start_block, j), v, None, src, ln1, "proved",
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-extract and exit non-zero if a committed JSON has drifted")
    args = ap.parse_args(argv)
    builders = (
        ("quadratic-law.json", build_quadratic_law),
        ("constants.json", build_constants),
        ("theta.json", build_theta),
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
