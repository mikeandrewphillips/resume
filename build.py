#!/usr/bin/env python3
"""Generate the resume in Markdown, LaTeX, PDF, and Word from resume.yaml.

Usage:
    python build.py [md|tex|pdf|docx|all]   (default: all)

Outputs land in dist/. PDF requires xelatex on PATH (BasicTeX/MacTeX) plus the
Lato/Raleway system fonts; everything else is pure Python.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

class ToolchainError(RuntimeError):
    """Raised when an external tool (xelatex) is missing or fails."""


ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "resume.yaml"
TPL = ROOT / "templates"
DIST = ROOT / "dist"
CLS = ROOT / "latex" / "deedy-resume-openfont.cls"
FONTS = ROOT / "fonts"

# LaTeX special characters that must be escaped in user-supplied text.
_TEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex_escape(value: object) -> str:
    text = str(value)
    out = []
    for ch in text:
        out.append(_TEX_REPLACEMENTS.get(ch, ch))
    return "".join(out)


def load_resume() -> dict:
    if not SRC.exists():
        sys.exit(f"error: {SRC} not found")
    with SRC.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _markdown_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TPL)),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )


def _latex_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TPL)),
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    env.filters["tex"] = tex_escape
    return env


def build_markdown(resume: dict) -> Path:
    out = DIST / "resume.md"
    rendered = _markdown_env().get_template("resume.md.j2").render(r=resume)
    out.write_text(rendered, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)}")
    return out


def build_latex(resume: dict) -> Path:
    out = DIST / "resume.tex"
    rendered = _latex_env().get_template("resume.tex.j2").render(r=resume)
    out.write_text(rendered, encoding="utf-8")
    shutil.copyfile(CLS, DIST / CLS.name)
    if FONTS.is_dir():
        shutil.copytree(FONTS, DIST / "fonts", dirs_exist_ok=True)
    print(f"  wrote {out.relative_to(ROOT)}")
    return out


def build_pdf(resume: dict) -> Path:
    if shutil.which("xelatex") is None:
        raise ToolchainError(
            "xelatex not found.\n"
            "  Install BasicTeX:  brew install --cask basictex\n"
            "  Then deps:         make tlmgr-deps\n"
            "  And fonts:         brew install --cask font-lato font-raleway"
        )
    build_latex(resume)
    # Two passes so textpos absolute positioning settles.
    for _ in range(2):
        proc = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "resume.tex"],
            cwd=DIST,
            capture_output=True,
            text=True,
        )
    if proc.returncode != 0:
        log = (DIST / "resume.log")
        tail = log.read_text(errors="replace").splitlines()[-25:] if log.exists() else []
        raise ToolchainError("xelatex failed:\n" + "\n".join(tail))
    for ext in (".aux", ".log", ".out"):
        (DIST / f"resume{ext}").unlink(missing_ok=True)
    out = DIST / "resume.pdf"
    print(f"  wrote {out.relative_to(ROOT)}")
    return out


def build_docx(resume: dict) -> Path:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Pt, RGBColor

    HEADING = RGBColor(0x6A, 0x6A, 0x6A)
    SUB = RGBColor(0x33, 0x33, 0x33)
    DATE = RGBColor(0x66, 0x66, 0x66)

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)
    for section in doc.sections:
        section.top_margin = section.bottom_margin = Pt(36)
        section.left_margin = section.right_margin = Pt(54)

    def hr(paragraph) -> None:
        p = paragraph._p.get_or_add_pPr()
        borders = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "AAAAAA")
        borders.append(bottom)
        p.append(borders)

    def section_heading(text: str) -> None:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text.upper())
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = HEADING

    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    nr = name.add_run(resume["name"])
    nr.font.size = Pt(28)
    nr.font.color.rgb = SUB

    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c = resume["contact"]
    cr = contact.add_run(f"{c['address']} | {c['phone']} | {c['email']}")
    cr.font.size = Pt(9)
    cr.font.color.rgb = DATE
    hr(contact)

    section_heading("Experience")
    for company in resume["experience"]:
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(8)
        cp.paragraph_format.space_after = Pt(0)
        cr = cp.add_run(company["company"])
        cr.bold = True
        cr.font.size = Pt(12)
        cr.font.color.rgb = SUB
        for role in company["roles"]:
            rp = doc.add_paragraph()
            rp.paragraph_format.space_after = Pt(2)
            rr = rp.add_run(f"{role['title']}  |  {role['dates']}")
            rr.italic = True
            rr.font.color.rgb = DATE
            for bullet in role["bullets"]:
                bp = doc.add_paragraph(style="List Bullet")
                bp.paragraph_format.space_after = Pt(2)
                bp.add_run(bullet)

    section_heading("Education")
    for e in resume["education"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        er = p.add_run(e["school"])
        er.bold = True
        p.add_run(f" — {e['detail']} ")
        dr = p.add_run(f"({e['dates']})")
        dr.italic = True
        dr.font.color.rgb = DATE

    for title, key in (("Certifications", "certifications"), ("Technology", "technology")):
        section_heading(title)
        for group in resume[key]:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(0)
            gr = p.add_run(group["name"])
            gr.bold = True
            gr.font.color.rgb = SUB
            for item in group["items"]:
                bp = doc.add_paragraph(style="List Bullet")
                bp.paragraph_format.space_after = Pt(1)
                bp.add_run(item)

    out = DIST / "resume.docx"
    doc.save(str(out))
    print(f"  wrote {out.relative_to(ROOT)}")
    return out


BUILDERS = {
    "md": build_markdown,
    "tex": build_latex,
    "pdf": build_pdf,
    "docx": build_docx,
}


def main(argv: list[str]) -> None:
    target = argv[0] if argv else "all"
    if target not in {*BUILDERS, "all"}:
        sys.exit(f"error: unknown target {target!r}; choose md|tex|pdf|docx|all")
    DIST.mkdir(exist_ok=True)
    resume = load_resume()
    # pdf runs last so a missing LaTeX toolchain never blocks the others.
    targets = ["md", "tex", "docx", "pdf"] if target == "all" else [target]
    print(f"building: {', '.join(targets)}")
    for t in targets:
        try:
            BUILDERS[t](resume)
        except ToolchainError as exc:
            if target == "all":
                print(f"  skipped {t}: {exc}")
            else:
                sys.exit(f"error: {exc}")
    print("done.")


if __name__ == "__main__":
    main(sys.argv[1:])
