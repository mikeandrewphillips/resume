# Bundled fonts

These font files are committed so PDF builds are reproducible without any
system font install. `build.py` copies this tree next to the generated
`resume.tex`; the Deedy class loads them by filename (see the FONT CONFIG
block in `latex/deedy-resume-openfont.cls`).

- **Lato** (`fonts/lato/`) — © Łukasz Dziedzic, licensed under the
  SIL Open Font License 1.1.
- **Raleway** (`fonts/raleway/`) — © The Raleway Project Authors, licensed
  under the SIL Open Font License 1.1.

The SIL OFL 1.1 permits bundling and redistribution with software. Keep this
notice with the font files. Full license text: search "SIL Open Font
License 1.1" or see the OFL.txt shipped with each upstream font family.
