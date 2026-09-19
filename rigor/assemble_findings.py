"""Assemble rigor/findings.tex from findings_entries.tex (entries \finding{SEV}{location}{agent}{text}), grouped by severity."""
import re
src=open('findings_entries.tex').read()
# parse entries with balanced braces
entries=[]; i=0
def grab(s,i):
    assert s[i]=='{'; d=0; j=i
    while True:
        if s[j]=='{': d+=1
        elif s[j]=='}':
            d-=1
            if d==0: return s[i+1:j], j+1
        j+=1
while True:
    k=src.find(r'\finding{',i)
    if k<0: break
    j=k+len(r'\finding'); args=[]
    for _ in range(4):
        a,j=grab(src,j); args.append(a)
    entries.append(args); i=j
order=['BREAK','BREAK-IN-SOURCE','DISPUTED','RESOLVED','GAP','MINOR','OK']
titles={'BREAK':'Proof-breaking issues in the notes (as stated)','BREAK-IN-SOURCE':'Errors found in the cited sources','DISPUTED':'Disputed items (superseded by a resolution below)','RESOLVED':'Resolutions of disputed items','GAP':'Gaps (repairable)','MINOR':'Minor issues','OK':'Verified items and independent confirmations'}
out=[r"""\documentclass[11pt]{article}\input{rigor_preamble}
\title{Consolidated findings of the verification program\\[0.3em]\large Notes N1--N7 of the CMI / Petz-recovery series}\author{}\date{Assembled from the agent reports (rigor/findings\_entries.tex)}
\begin{document}\maketitle\tableofcontents\clearpage
\section{Scope and method}
Fourteen Opus agents re-derived every stated result of the seven notes in Lamport's structured-proof style (documents listed in \texttt{rigor/INDEX.md}), downloaded the cited references (\texttt{refs/}, 38 PDFs; a few paywalled items were replaced by open restatements, marked NOT OBTAINED), transcribed the exact cited statements with screenshots (\texttt{cited\_R1--R4.tex}), and attacked the four remaining rigor items of Note~7 (\texttt{lemma\_second\_variation}, \texttt{quadratic\_limit}, \texttt{kernel\_identity}, \texttt{collar\_and\_invariant\_formula}). Severity: BREAK = invalidates a statement as written; GAP = missing argument, likely repairable; MINOR = presentation or attribution. Each entry names the note (N1--N7), the location, the reporting agent, and the finding.
"""]
for sev in order:
    items=[e for e in entries if e[0]==sev]
    if not items: continue
    out.append(f"\\section{{{titles[sev]}}}\n\\begin{{enumerate}}[leftmargin=1.6em,itemsep=6pt]")
    for sev_,loc,agent,text in items:
        out.append(f"\\item \\textbf{{[{sev_}]}} \\emph{{{loc}}} \\hfill\\textsc{{{agent}}}\\\\ {text}")
    out.append(r"\end{enumerate}")
out.append(r"\input{findings_tail}"+"\n"+r"\end{document}")
open('findings.tex','w').write("\n".join(out)); print(f"findings.tex assembled with {len(entries)} entries:", {s:sum(1 for e in entries if e[0]==s) for s in order})
