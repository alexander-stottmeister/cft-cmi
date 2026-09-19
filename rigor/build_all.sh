#!/bin/bash
# Compile every standalone .tex in rigor/ twice; report failures and overfull counts.
cd "$(dirname "$0")"
for f in *.tex; do
  case "$f" in rigor_preamble.tex|findings_skeleton.tex|findings_entries.tex|findings_tail.tex|_*) continue;; esac
  b="${f%.tex}"
  ok=1
  for i in 1 2; do pdflatex -interaction=nonstopmode -halt-on-error "$f" > "/tmp/rigor_build_$b.log" 2>&1 || { ok=0; break; }; done
  if [ $ok -eq 1 ]; then
    echo "OK   $f  ($(grep -c Overfull /tmp/rigor_build_$b.log) overfull, $(grep -c 'undefined' /tmp/rigor_build_$b.log) undefined-ref lines, $(grep 'Output written' /tmp/rigor_build_$b.log | sed -E 's/.*\(([0-9]+) pages.*/\1/') pages)"
  else
    echo "FAIL $f"; grep -A3 '^!' "/tmp/rigor_build_$b.log" | head -8
  fi
  rm -f "$b.aux" "$b.log" "$b.out" "$b.toc"
done
