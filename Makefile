# cft_cmi — build the public surface.  NOTE: docs/ records each card's review
# state, and so does the claim map's data, so a referee verdict makes `make check`
# fail until both are rebuilt.  Run `make docs data` before committing after any
# knowledge-base change.
#  Every target is re-runnable and writes
# only inside the repository.  See rigor/public_site_plan.md section 4.
PYTHON ?= python3
.PHONY: all docs figures data papers check site clean-site help

help:
	@echo "make docs     regenerate docs/ from the knowledge base"
	@echo "make figures  regenerate docs/assets/*.svg"
	@echo "make data     regenerate docs/data/*.json from the result files"
	@echo "make papers   compile paper1 and paper2 (twice each)"
	@echo "make check    links, documentation drift, site data drift"
	@echo "make rigor    compile every rigor document against the known-failure baseline"
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
	@test -f tools/build_site_data_extra.py && $(PYTHON) tools/build_site_data_extra.py || true

papers:
	cd paper1 && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null
	cd paper2 && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null && pdflatex -halt-on-error -interaction=nonstopmode main.tex >/dev/null
	@echo "paper1 and paper2 built"

# The gate: documentation must match the knowledge base, and every number on the
# site must still match the file it was extracted from.
check:
	$(PYTHON) tools/check_links.py
	$(PYTHON) tools/build_docs.py --check
	@if [ -f tools/build_site_data.py ]; then $(PYTHON) tools/build_site_data.py --check; else echo "site data: no extractor yet, skipped"; fi
	@if [ -f tools/build_site_data_extra.py ]; then $(PYTHON) tools/build_site_data_extra.py --check; fi

site: figures data docs
	@echo "serving docs/ at http://localhost:8000  (ctrl-c to stop)"
	cd docs && $(PYTHON) -m http.server 8000

# Compile every rigor document and compare with rigor/known_build_failures.json,
# which is empty since 21 September: any failure is now a regression.  It also
# fails if a listed failure starts building, so the list stays honest; --update
# rewrites it deliberately.
rigor:
	$(PYTHON) tools/check_rigor_builds.py
