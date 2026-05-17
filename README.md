# Resume

A complete master CV (`resume.yaml`) plus small **variant** files that pick
which tagged elements to include. Each variant renders to **Markdown**,
**LaTeX**, **PDF** (Deedy two-column), and **Word (.docx)**.

```
resume.yaml              # the COMPLETE CV — every job/bullet/cert/skill
variants/
  full.yaml              # everything (== the original resume)
  networking.yaml        # network-focused subset + objective
  product.yaml           # product/PM-focused subset + objective
templates/
  resume.md.j2           # Markdown template (Jinja2)
  resume.tex.j2          # LaTeX template (Jinja2, LaTeX-safe delimiters)
latex/
  deedy-resume-openfont.cls   # Deedy class, bundled-font based
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
make all                       # full variant -> dist/resume.{md,tex,pdf,docx}
make all VARIANT=networking    # -> dist/MichaelPhillips_Networking.*
make variants                  # build every variant in variants/, all formats
make md  VARIANT=product       # one format, one variant
make pdf VARIANT=full          # LaTeX -> PDF (xelatex, run twice)
make clean                     # wipe dist/
```

`make all` with no `VARIANT` builds `full`, which is byte-identical to the
original resume. Each variant's `output:` field sets its `dist/` basename.

## Pre-commit hook

A tracked hook (`.githooks/pre-commit`) runs `make all` before each commit
when `resume.yaml`, `build.py`, `templates/`, `latex/`, or `fonts/` are
staged, so a broken build blocks the commit. It is enabled by `make setup`
(or `make hooks`), which points `git config core.hooksPath` at `.githooks`.
Commits touching only other files skip the rebuild. Bypass with
`git commit --no-verify` if ever needed.

## Editing content

`resume.yaml` is the **complete** CV — never trim it; add everything.
Layout: `education`, `certifications`, `technology` → left column of the
PDF; `experience` → right column (a company has one or more `roles`, each
with `bullets`). Markdown and DOCX render one linear, ATS-friendly flow.

## Variants & tags

Which elements appear in a given resume is decided by `variants/*.yaml`,
not by editing the CV. Tagging model:

- A **plain-string** bullet/item, or a group with **no `tags:`**, is
  *core* — always included in every variant.
- A bullet/item written as `{text: ..., tags: [...]}`, or a group with
  `tags: [...]`, is included only when the variant selects one of those
  tags (OR match). Empty sections disappear (no stray headers).
- The `full` variant selects nothing special → includes everything.

A variant file:

```yaml
label: Networking                       # human label
output: MichaelPhillips_Networking      # dist/ basename (default: resume)
objective: >                            # optional summary; renders only if set
  Network architect ...
tags: [networking, security, leadership]  # omit entirely to include all
```

To add a focus area: pick a tag word, tag the relevant bullets/groups in
`resume.yaml`, add `variants/<name>.yaml`, then `make all VARIANT=<name>`.
Validate every variant at once with `make variants`. Tag vocabulary
currently in use: `networking, devops, cloud, leadership, product,
teaching, security`.

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
