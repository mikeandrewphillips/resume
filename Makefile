VENV    := .venv
PY      := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
VARIANT ?= full

.DEFAULT_GOAL := help

.PHONY: help setup hooks all md tex pdf docx variants tlmgr-deps clean

help: ## Show this help
	@echo "Resume build system"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo "Variants live in variants/. Build one with VARIANT=<name>:"
	@echo "  make all VARIANT=networking      # -> dist/MichaelPhillips_Networking.*"
	@echo "  make variants                    # build every variant, all formats"
	@echo "  make all                         # default VARIANT=full -> dist/resume.*"
	@echo
	@echo "First-time setup:"
	@echo "  make setup                              # python venv + deps"
	@echo "  brew install --cask basictex            # LaTeX engine (xelatex)"
	@echo "  make tlmgr-deps                          # LaTeX packages"
	@echo "  (fonts are bundled in fonts/ - nothing to install)"

setup: hooks ## Create venv, install Python deps, enable git hooks
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

hooks: ## Enable the tracked git pre-commit hook
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

all: ## Build every format for VARIANT (default full)
	$(PY) build.py all $(VARIANT)

md: ## Build Markdown only (VARIANT=...)
	$(PY) build.py md $(VARIANT)

tex: ## Build LaTeX source only (VARIANT=...)
	$(PY) build.py tex $(VARIANT)

pdf: ## Build PDF only (VARIANT=...; needs xelatex)
	$(PY) build.py pdf $(VARIANT)

docx: ## Build Word .docx only (VARIANT=...)
	$(PY) build.py docx $(VARIANT)

variants: ## Build all formats for every variant in variants/
	@for f in variants/*.yaml; do \
	  v=$$(basename $$f .yaml); \
	  $(PY) build.py all $$v || exit 1; \
	done

tlmgr-deps: ## Install LaTeX packages the Deedy class needs
	sudo tlmgr update --self
	sudo tlmgr install geometry hyperref cite xcolor fontspec \
	  textpos isodate substr titlesec fancyhdr xkeyval

clean: ## Remove build outputs
	rm -rf dist
