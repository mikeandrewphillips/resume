# Resume

One source of truth (`resume.yaml`) rendered to **Markdown**, **LaTeX**,
**PDF** (Deedy two-column), and **Word (.docx)**.

```
resume.yaml              # edit this — all content lives here
templates/
  resume.md.j2           # Markdown template (Jinja2)
  resume.tex.j2          # LaTeX template (Jinja2, LaTeX-safe delimiters)
latex/
  deedy-resume-openfont.cls   # Deedy class, system-font based
build.py                 # renderer / orchestrator
dist/                    # generated output (gitignored)
```

## Setup

```sh
make setup                            # Python venv + deps (Jinja2, PyYAML, python-docx)
```

For PDF only (one-time, needs Homebrew):

```sh
brew install --cask basictex          # provides xelatex
make tlmgr-deps                        # LaTeX packages for the Deedy class
```

Fonts are bundled in `fonts/` and committed — no font install needed.
`make tlmgr-deps` runs `sudo tlmgr`; BasicTeX may also need a new shell so
`xelatex`/`tlmgr` land on `PATH` (or prepend `/Library/TeX/texbin`).

## Build

```sh
make all      # md + tex + pdf + docx  ->  dist/
make md       # just Markdown
make tex      # just LaTeX source
make pdf      # LaTeX -> PDF (xelatex, run twice for positioning)
make docx     # styled Word document
make clean    # wipe dist/
```

Outputs: `dist/resume.{md,tex,pdf,docx}`.

## Pre-commit hook

A tracked hook (`.githooks/pre-commit`) runs `make all` before each commit
when `resume.yaml`, `build.py`, `templates/`, `latex/`, or `fonts/` are
staged, so a broken build blocks the commit. It is enabled by `make setup`
(or `make hooks`), which points `git config core.hooksPath` at `.githooks`.
Commits touching only other files skip the rebuild. Bypass with
`git commit --no-verify` if ever needed.

## Editing content

Edit `resume.yaml` and rebuild. Structure:

- `education`, `certifications`, `technology` → **left column** of the PDF.
- `experience` → **right column** of the PDF (a company has one or more
  `roles`, each with `bullets`).
- Markdown and DOCX render everything in a single linear flow (ATS-friendly).

## Fonts (PDF)

Lato and Raleway are committed under `fonts/` and loaded **by file** so PDF
builds are deterministic and need no system-installed fonts. `build.py`
stages `fonts/` next to the generated `.tex` before compiling. To swap a
weight, drop a file in `fonts/lato/` or `fonts/raleway/` and update the
filename in the FONT CONFIG block of `latex/deedy-resume-openfont.cls`.

(System-font / family-name loading was tried first but XeTeX's font engine
errors on Raleway because Homebrew also installs a variable font that
CoreText resolves to; loading the static files by path avoids this.)

## Notes / content corrections

These typos from the April 2025 PDF were corrected in `resume.yaml`:

- "Terrafrom" → "Terraform"
- "docuemntation" → "documentation"
- "Route 52" → "Route 53" *(AWS DNS service — revert if intentional)*
