# Resume

A complete master CV (`resume.yaml`) plus small **variant** files that pick
which tagged elements to include. Each variant renders to **Markdown**,
**LaTeX**, **PDF** (Deedy two-column), and **Word (.docx)**.

```
resume.yaml              # the COMPLETE CV — every job/bullet/cert/skill
variants/
  standard.yaml          # DEFAULT: 1-page career overview, mgmt-forward -> resume.*
  networking.yaml        # 1-page network-focused + objective
  product.yaml           # 1-page product/PM-focused + objective
  full.yaml              # the ENTIRE CV, classic multi-page LaTeX layout
templates/
  resume.md.j2           # Markdown template (Jinja2)
  resume.tex.j2          # Deedy one-page two-column LaTeX (one-pagers)
  cv.tex.j2              # classic multi-page LaTeX CV (the `full` layout)
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
make all                       # standard (lean) -> dist/resume.{md,tex,pdf,docx}
make all VARIANT=full          # entire CV -> dist/MichaelPhillips_FullCV.*
make all VARIANT=networking    # -> dist/MichaelPhillips_Networking.*
make variants                  # build every variant in variants/, all formats
make md  VARIANT=product       # one format, one variant
make clean                     # wipe dist/
```

`make all` with no `VARIANT` builds `standard` → `dist/resume.*`. Each
variant's `output:` field sets its `dist/` basename.

### Two PDF layouts

A variant picks its PDF layout with `layout:` (default `deedy`):

| layout    | template        | use                                   |
|-----------|-----------------|---------------------------------------|
| `deedy`   | `resume.tex.j2` | one-page two-column résumé (Deedy)     |
| `classic` | `cv.tex.j2`     | classic multi-page LaTeX CV           |

`standard`, `networking`, `product` are tuned to **one clean Deedy page**
each. `full` uses `layout: classic` — a traditional multi-page CV (article
class, no special fonts) that includes **everything**. Markdown and DOCX
are layout-independent and always render the variant's full linear flow.

## Pre-commit hook

A tracked hook (`.githooks/pre-commit`) runs `make all` before each commit
when `resume.yaml`, `build.py`, `templates/`, `latex/`, or `fonts/` are
staged, so a broken build blocks the commit. It is enabled by `make setup`
(or `make hooks`), which points `git config core.hooksPath` at `.githooks`.
Commits touching only other files skip the rebuild. Bypass with
`git commit --no-verify` if ever needed.

## Editing content

`resume.yaml` is the **complete** CV — never trim it; add everything.
In the Deedy layout `education`, `certifications`, `technology` fill the
left column and `experience` the right; the classic CV and Markdown/DOCX
render one linear flow.

## Variants & tags

Variants decide what shows; you don't edit the CV per resume.

- A **plain string / group with no `tags:`** is *core* — on **every**
  resume (contact, Eastern Illinois + Auburn education, compact certs,
  core tech).
- Each **experience bullet is tagged for its one-pager audience(s)**:
  `overview` (the `standard`, management-forward résumé), `networking`,
  `product`. The current Grainger EM lead bullet carries all three so
  every one-pager leads with the present role.
- Bullets/items for the complete CV only carry lifecycle tags —
  `extended` (present-day depth), `early`, `research`, `academic`,
  `teaching`, `detail` (verbose credential IDs) — and **no** one-pager
  tag, so the one-pagers skip them while `full` keeps them.
- A variant includes core **plus** anything matching its `tags`
  (OR match). Empty sections disappear (no stray headers).

| variant      | `tags:`        | layout    | output                       |
|--------------|----------------|-----------|------------------------------|
| `standard`   | `[overview]`   | deedy     | `resume.*` (1 pg)            |
| `networking` | `[networking]` | deedy     | `MichaelPhillips_Networking` |
| `product`    | `[product]`    | deedy     | `MichaelPhillips_Product`    |
| `full`       | *(omitted)*    | classic   | `MichaelPhillips_FullCV`     |

A variant file:

```yaml
label: Networking                       # human label
output: MichaelPhillips_Networking      # dist/ basename (default: resume)
layout: deedy                           # deedy (default) | classic
objective: >                            # optional summary; renders only if set
  Network architect ...
tags: [networking]                      # omit entirely to include everything
```

To add a focus area: pick a tag word, add it to the relevant experience
bullets in `resume.yaml`, add `variants/<name>.yaml` with
`tags: [<word>]`, then `make all VARIANT=<name>` and trim until the Deedy
PDF is one page (`make variants` builds/validates them all). One-pager
tags: `overview`, `networking`, `product`. Lifecycle (full-CV only):
`extended`, `early`, `research`, `academic`, `teaching`, `detail`.

## Fonts (PDF)

Lato and Raleway are committed under `fonts/` and loaded **by file** so PDF
builds are deterministic and need no system-installed fonts. `build.py`
stages `fonts/` next to the generated `.tex` before compiling. To swap a
weight, drop a file in `fonts/lato/` or `fonts/raleway/` and update the
filename in the FONT CONFIG block of `latex/deedy-resume-openfont.cls`.

(System-font / family-name loading was tried first but XeTeX's font engine
errors on Raleway because Homebrew also installs a variable font that
CoreText resolves to; loading the static files by path avoids this.)

## Notes / content provenance

- `resume.yaml` was reconciled from LinkedIn (2026-05): current title is
  **Engineering Manager** (Grainger, Pipeline / Platform Engineering);
  Grainger is 3 roles, Wolfram is 4, plus the Auburn satellite program,
  research/publications, and WKU/Gatton education added as the complete
  history (most tagged `early` / `research` / `academic`).
- Earlier typo fixes still applied: "Terrafrom"→"Terraform",
  "docuemntation"→"documentation", "Route 52"→"Route 53".
- The old "`full` == byte-identical original resume" guarantee is
  intentionally retired — the master CV was deliberately updated.
