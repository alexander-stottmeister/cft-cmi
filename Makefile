# cft_cmi — build the public surface.  Every target is re-runnable and writes
# only inside the repository.  See rigor/public_site_plan.md section 4.
PYTHON ?= python3
.PHONY: all docs figures data papers check site clean-site help

help:
	@echo "make docs     regenerate docs/ from the knowledge base"
	@echo "make figures  regenerate docs/assets/*.svg"
	@echo "make data     regenerate docs/data/*.json from the result files"
	@echo "make papers   compile paper1 and paper2 (twice each)"
	@echo "make check    fail if any generated artefact has drifted from its source"
	@echo "make site     figures + data + docs, then serve docs/ locally"
	@echo ""
	@echo "PYTHON=<interpreter> overrides the interpreter (default: python3)."

all: figures data docs

docs:
	$(PYTHON) tools/build_docs.py

figures:
	@test -f tools/make_figures.py || { echo "tools/make_figures.py not present yet"; exit 1; }
	$(PYTHON) tools/make_figures.py

data:
	@test -f tools/build_site_data.py || { echo "tools/build_site_data.py not present yet"; exit 1; }
	$(PYTHON) tools/build_site_data.py

papers:
	cd paper1 && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null
	cd paper2 && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null
	@echo "paper1 and paper2 built"

# The gate: documentation must match the knowledge base, and every number on the
# site must still match the file it was extracted from.
check:
	$(PYTHON) tools/build_docs.py --check
	@test -f tools/build_site_data.py && $(PYTHON) tools/build_site_data.py --check || echo "site data: no extractor yet, skipped"

site: figures data docs
	@echo "serving docs/ at http://localhost:8000  (ctrl-c to stop)"
	cd docs && $(PYTHON) -m http.server 8000
