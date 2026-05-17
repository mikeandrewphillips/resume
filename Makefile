VENV := .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help setup hooks all md tex pdf docx tlmgr-deps clean

help: ## Show this help
	@echo "Resume build system"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
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

all: ## Build every format (md, tex, pdf, docx)
	$(PY) build.py all

md: ## Build Markdown only
	$(PY) build.py md

tex: ## Build LaTeX source only
	$(PY) build.py tex

pdf: ## Build PDF (needs xelatex + fonts)
	$(PY) build.py pdf

docx: ## Build Word .docx only
	$(PY) build.py docx

tlmgr-deps: ## Install LaTeX packages the Deedy class needs
	sudo tlmgr update --self
	sudo tlmgr install geometry hyperref cite xcolor fontspec \
	  textpos isodate substr titlesec fancyhdr xkeyval

clean: ## Remove build outputs
	rm -rf dist
