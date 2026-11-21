#!/usr/bin/env python3
"""Generate the student workbook and nine commented R exercise files.

The source is restricted to student-facing fields before rendering or saving.
No instructor solutions are copied into the generated material.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

HERE = Path(__file__).resolve().parent
PAPER = HexColor("#F8F6F1")
NAVY = HexColor("#15283E")
TEAL = HexColor("#087C74")
INK = HexColor("#26343E")
MUTED = HexColor("#53616B")
RULE = HexColor("#CBD6D5")
TINT = HexColor("#EDF4F1")
CODE_BG = HexColor("#FCFDFC")
W, H = A4
MARGIN = 42
WIDTH = W - 2 * MARGIN
LAB_URL = "https://marzione00.github.io/Lab_Geo/#laboratorio/"
KEEP_EXERCISE = (
    "id", "titolo", "obiettivo", "parametri_iniziali", "passi", "domande",
    "consegna", "verifica_locale", "limiti",
)

def clean(text: str) -> str:
    """Normalize typographic hyphens while preserving mathematical symbols."""
    return str(text).replace("\u2011", "-").replace("\u2013", "-").replace(
        "\u2014", "-"
    ).replace("\u2212", "-")


def student_data(raw: dict) -> dict:
    return {
        "titolo": "Aurea - Quaderno di esercitazione",
        "sottotitolo": raw["sottotitolo"],
        "data": raw["data"],
        "istruzioni_comuni": raw["istruzioni_comuni"],
        "esercizi": [
            {key: e[key] for key in KEEP_EXERCISE}
            for e in raw["esercizi"]
        ],
    }


def font_file(pattern: str) -> str:
    result = subprocess.run(
        ["fc-match", "-f", "%{file}", pattern],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if not Path(result).is_file():
        raise FileNotFoundError(f"Font not found: {pattern}")
    return result


def register_fonts() -> None:
    for name, pattern in (
        ("LiberationSans", "LiberationSans:style=Regular"),
        ("LiberationSans-Bold", "LiberationSans:style=Bold"),
        ("LiberationSans-Italic", "LiberationSans:style=Italic"),
        ("DejaVuSansMono", "DejaVuSansMono:style=Book"),
    ):
        pdfmetrics.registerFont(TTFont(name, font_file(pattern)))
    pdfmetrics.registerFontFamily(
        "LiberationSans", normal="LiberationSans",
        bold="LiberationSans-Bold", italic="LiberationSans-Italic",
        boldItalic="LiberationSans-Bold",
    )


def styles() -> dict[str, ParagraphStyle]:
    base = dict(
        fontName="LiberationSans", textColor=INK, alignment=TA_LEFT,
        splitLongWords=False, allowWidows=False, allowOrphans=False,
    )
    return {
        "body": ParagraphStyle(
            "body", fontSize=10.6, leading=14.0, **base,
        ),
        "small": ParagraphStyle(
            "small", fontSize=10.1, leading=13.2, **base,
        ),
        "title": ParagraphStyle(
            "title", fontName="LiberationSans-Bold", fontSize=21.5,
            leading=24.3, textColor=NAVY, splitLongWords=False,
        ),
        "intro_title": ParagraphStyle(
            "intro_title", fontName="LiberationSans-Bold", fontSize=31,
            leading=35, textColor=NAVY,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", fontName="LiberationSans", fontSize=15,
            leading=19, textColor=NAVY,
        ),
    }


def pheight(text: str, width: float, style: ParagraphStyle) -> float:
    return Paragraph(escape(clean(text)), style).wrap(width, 1000)[1]


def draw_p(c: canvas.Canvas, text: str, x: float, y: float,
           width: float, style: ParagraphStyle, markup=False) -> float:
    content = clean(text) if markup else escape(clean(text))
    p = Paragraph(content, style)
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y - height)
    return y - height


def label(c: canvas.Canvas, title: str, x: float, y: float) -> float:
    c.setFillColor(TEAL)
    c.setFont("LiberationSans-Bold", 8.5)
    c.drawString(x, y - 8.5, title.upper())
    return y - 16.5


def plain_block(c: canvas.Canvas, title: str, text: str,
                y: float, st: dict, style="body") -> float:
    y = label(c, title, MARGIN, y)
    return draw_p(c, text, MARGIN, y, WIDTH, st[style])


def tint_block(c: canvas.Canvas, title: str, text: str, y: float,
               st: dict, color=TINT) -> float:
    inner = WIDTH - 24
    h = 12 + 16.5 + pheight(text, inner, st["body"]) + 10
    c.setFillColor(color)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.55)
    c.roundRect(MARGIN, y - h, WIDTH, h, 5, fill=1, stroke=1)
    c.setFillColor(TEAL)
    c.rect(MARGIN, y - h + 5, 2.2, h - 10, fill=1, stroke=0)
    iy = label(c, title, MARGIN + 12, y - 10)
    draw_p(c, text, MARGIN + 12, iy, inner, st["body"])
    return y - h


def numbered(c: canvas.Canvas, title: str, lines: list[str], y: float,
             st: dict, question=False) -> float:
    y = label(c, title, MARGIN, y)
    for i, text in enumerate(lines, 1):
        c.setFillColor(TEAL if not question else MUTED)
        c.setFont("LiberationSans-Bold", 10.1)
        c.drawString(MARGIN + 1, y - 10.3, f"{i}.")
        y = draw_p(c, text, MARGIN + 19, y, WIDTH - 19, st["body"])
        y -= 3.6
    return y


def verification_lines(e: dict) -> list[str]:
    original = e["verifica_locale"].strip().splitlines()
    return ['source("setup.R", encoding = "UTF-8")', *original]


def draw_code(c: canvas.Canvas, code: list[str], filename: str, y: float,
              title="VERIFICA LOCALE / R") -> float:
    fs, leading = 10.0, 13.0
    pad, bar = 11, 21
    h = bar + 2 * pad + len(code) * leading
    c.setFillColor(CODE_BG)
    c.setStrokeColor(RULE)
    c.setLineWidth(.6)
    c.roundRect(MARGIN, y - h, WIDTH, h, 5, fill=1, stroke=1)
    c.saveState()
    path = c.beginPath()
    path.roundRect(MARGIN, y - h, WIDTH, h, 5)
    c.clipPath(path, stroke=0)
    c.setFillColor(NAVY)
    c.rect(MARGIN, y - bar, WIDTH, bar, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(white)
    c.setFont("LiberationSans-Bold", 8.6)
    c.drawString(MARGIN + 11, y - 14.3, title)
    c.setFont("LiberationSans", 8.5)
    c.drawRightString(W - MARGIN - 11, y - 14.3, filename)
    baseline = y - bar - pad - fs
    c.setFont("DejaVuSansMono", fs)
    for line in code:
        if pdfmetrics.stringWidth(line, "DejaVuSansMono", fs) > WIDTH - 22:
            raise ValueError(f"Code too wide: {filename}: {line}")
        c.setFillColor(TEAL if line.startswith("#") else NAVY)
        c.drawString(MARGIN + pad, baseline, line)
        baseline -= leading
    return y - h


def page_base(c: canvas.Canvas, page: int, lab: int | None = None):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(MARGIN, H - 37, 4, 7, fill=1, stroke=0)
    c.setFont("LiberationSans-Bold", 8.6)
    c.drawString(MARGIN + 11, H - 36, "AUREA / PROBABILITÀ E SIMULAZIONE")
    c.setFillColor(MUTED)
    c.setFont("LiberationSans", 8.6)
    right = "QUADERNO STUDENTI" if lab is None else f"ESPERIMENTO {lab:02d} / 9"
    c.drawRightString(W - MARGIN, H - 36, right)
    c.setStrokeColor(RULE)
    c.setLineWidth(.6)
    c.line(MARGIN, 39, W - MARGIN, 39)
    c.setFillColor(MUTED)
    c.setFont("LiberationSans", 8.3)
    c.drawString(MARGIN, 25, "Aurea · Modulo M04 · Quaderno di esercitazione")
    c.drawRightString(W - MARGIN, 25, f"{page} / 10")
    if page > 1:
        c.linkAbsolute("Indice del quaderno", "indice",
                       Rect=(MARGIN, 18, MARGIN + 255, 34), thickness=0)


def measure_exercise(e: dict, st: dict) -> float:
    h = pheight(e["titolo"], WIDTH, st["title"]) + 24 + 11
    h += 16.5 + pheight(e["obiettivo"], WIDTH, st["body"]) + 9
    h += 12 + 16.5 + pheight(e["parametri_iniziali"], WIDTH - 24, st["body"]) + 10 + 11
    h += 16.5 + sum(pheight(x, WIDTH - 19, st["body"]) + 3.6 for x in e["passi"]) + 7
    h += 16.5 + sum(pheight(x, WIDTH - 19, st["body"]) + 3.6 for x in e["domande"]) + 7
    h += 12 + 16.5 + pheight(e["consegna"], WIDTH - 24, st["body"]) + 10 + 10
    h += 21 + 22 + len(verification_lines(e)) * 13.0 + 10
    h += 16.5 + pheight(e["limiti"], WIDTH, st["small"])
    return h


def exercise_page(c: canvas.Canvas, e: dict, n: int, st: dict) -> dict:
    page_base(c, n + 1, n)
    c.bookmarkPage(e["id"])
    c.addOutlineEntry(f"{n:02d} - {e['titolo']}", e["id"], level=0)
    y = H - 56
    if e["id"] == "m04-composizione":
        title = "Chiusura della composizione<br/>e denominatore comune"
        y = draw_p(c, title, MARGIN, y, WIDTH, st["title"], markup=True)
    else:
        y = draw_p(c, e["titolo"], MARGIN, y, WIDTH, st["title"])
    y -= 8
    c.setFillColor(TEAL)
    c.setFont("LiberationSans", 9.3)
    link = f"Apri il laboratorio: {e['id']}"
    c.drawString(MARGIN, y - 9.3, link)
    c.linkURL(LAB_URL + e["id"],
              (MARGIN, y - 13, MARGIN + pdfmetrics.stringWidth(link, "LiberationSans", 9.3), y),
              relative=0, thickness=0)
    y -= 27
    y = plain_block(c, "Obiettivo", e["obiettivo"], y, st) - 9
    y = tint_block(c, "Parametri iniziali", e["parametri_iniziali"], y, st) - 11
    y = numbered(c, "Procedura", e["passi"], y, st) - 7
    y = numbered(c, "Domande", e["domande"], y, st, question=True) - 7
    y = tint_block(c, "Consegna", e["consegna"], y, st,
                   color=HexColor("#F1F3F3")) - 10
    name = f"{n:02d}_{e['id'].replace('m04-', '')}.R"
    y = draw_code(c, verification_lines(e), f"Esercizi/{name}", y) - 10
    y = plain_block(c, "Limite metodologico", e["limiti"], y, st, style="small")
    if y < 52:
        raise RuntimeError(f"Page {n+1} overflows: content bottom {y:.2f} pt")
    if y < 102:
        raise RuntimeError(f"Page {n+1} overlaps the writing area: {y:.2f} pt")
    label(c, "Calcoli, risultati e annotazioni", MARGIN, y - 17)
    c.setStrokeColor(RULE)
    c.setLineWidth(.4)
    for baseline in range(int(y - 42), 53, -24):
        c.line(MARGIN, baseline, W - MARGIN, baseline)
    c.showPage()
    return {"pagina": n + 1, "id": e["id"], "fondo_contenuto_pt": round(y, 2)}


def intro_page(c: canvas.Canvas, d: dict, st: dict):
    page_base(c, 1)
    c.bookmarkPage("indice")
    c.addOutlineEntry("Come usare il quaderno", "indice", level=0)
    y = H - 62
    y = draw_p(c, "Aurea", MARGIN, y, WIDTH, st["intro_title"]) - 3
    y = draw_p(c, "Quaderno di esercitazione", MARGIN, y, WIDTH, st["subtitle"]) - 14
    y = draw_p(c, d["sottotitolo"], MARGIN, y, WIDTH, st["body"]) - 18
    y = plain_block(
        c, "Prima della verifica",
        "Per ogni esperimento, formulare una previsione, eseguire due scenari "
        "e spiegare le differenze usando parametri, dati e regole del calcolo. "
        "Annotare la previsione prima di leggere gli indicatori restituiti.",
        y, st,
    ) - 13
    instructions = d["istruzioni_comuni"][:4]
    y = numbered(c, "Nel laboratorio online", instructions, y, st) - 10
    y = tint_block(
        c, "Nel progetto R",
        "Aprire Aurea_M04.Rproj. Eseguire gli script dalla cartella del progetto: "
        "setup.R legge i parametri del caso fisico e definisce le funzioni comuni. "
        "Esercizi/ contiene i nove confronti commentati. I dati dei laboratori "
        "sono simulati o calcolati da modelli assegnati; il caso fisico ha unità proprie.",
        y, st,
    ) - 10
    y = draw_code(
        c,
        [
            "# Il primo script carica anche le funzioni comuni.",
            'source("Esercizi/01_eventi.R",',
            '       encoding = "UTF-8", echo = TRUE)',
        ],
        "Dalla cartella del progetto",
        y, title="AVVIO DI UN ESERCIZIO / R",
    ) - 9
    y = draw_p(
        c,
        "rA e rB conservano i due scenari. L'operatore $ estrae una parte "
        "del risultato: dati contiene la tabella, indicatori le statistiche "
        "da confrontare. echo = TRUE mostra i comandi e i risultati.",
        MARGIN, y, WIDTH, st["small"],
    ) - 16
    y = label(c, "Indice degli esperimenti", MARGIN, y)
    row_h = 21
    for n, e in enumerate(d["esercizi"], 1):
        iy = y - (n - 1) * row_h
        c.setFillColor(TEAL)
        c.setFont("LiberationSans-Bold", 9.5)
        c.drawString(MARGIN, iy - 10, f"{n:02d}")
        c.setFillColor(NAVY)
        c.setFont("LiberationSans", 10.2)
        title = e["titolo"]
        c.drawString(MARGIN + 25, iy - 10, title)
        c.setFillColor(MUTED)
        c.drawRightString(W - MARGIN, iy - 10, str(n + 1))
        c.setStrokeColor(RULE)
        c.setLineWidth(.35)
        c.line(MARGIN, iy - 17, W - MARGIN, iy - 17)
        c.linkAbsolute(title, e["id"],
                       Rect=(MARGIN, iy - 20, W - MARGIN, iy + 3), thickness=0)
    y -= len(d["esercizi"]) * row_h
    if y < 51:
        raise RuntimeError(f"Intro page overflows: {y:.2f} pt")
    c.showPage()
    return {"pagina": 1, "id": "introduzione", "fondo_contenuto_pt": round(y, 2)}


def write_scripts(d: dict, out: Path):
    script_dir = out / "Esercizi"
    script_dir.mkdir(exist_ok=True)
    for n, e in enumerate(d["esercizi"], 1):
        name = f"{n:02d}_{e['id'].replace('m04-', '')}.R"
        header = [
            f"# Aurea M04 - esercizio {n:02d}",
            "# " + e["titolo"],
            "# Laboratorio: " + LAB_URL + e["id"],
            "# Aprire Aurea_M04.Rproj prima di eseguire questo file.",
            "# Eseguire a righe oppure con source(..., echo = TRUE).",
            "# Scrivere una previsione prima di leggere gli indicatori.",
            "",
        ]
        text = "\n".join(header + verification_lines(e)) + "\n"
        (script_dir / name).write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    source = args.input
    if source is None:
        source = HERE / "Quaderno_contenuti_studenti.json"
        if not source.exists():
            source = HERE.parent / "support" / "Quaderno_contenuti.json"
    d = student_data(json.loads(source.read_text(encoding="utf-8")))
    if len(d["esercizi"]) != 9:
        raise ValueError("The workbook requires exactly nine exercises.")
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "Quaderno_contenuti_studenti.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_scripts(d, out)
    register_fonts()
    st = styles()
    path = out / "Aurea_M04_quaderno_esercizi.pdf"
    c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    c.setTitle("Aurea - Quaderno di esercitazione")
    c.setSubject("Probabilità, variabilità e simulazione: nove esperimenti del modulo M04")
    c.setAuthor("Materiali didattici Aurea")
    c.setCreator("genera_quaderno.py / ReportLab")
    checks = [intro_page(c, d, st)]
    for n, e in enumerate(d["esercizi"], 1):
        checks.append(exercise_page(c, e, n, st))
    c.save()
    (out / "Verifica_impaginazione.json").write_text(
        json.dumps({
            "pagine": 10, "formato": "A4",
            "corpo_pt": 10.6, "nota_metodologica_pt": 10.1,
            "codice_pt": 10.0,
            "font": ["LiberationSans", "DejaVuSansMono"],
            "soluzioni_docente": False, "verifiche": checks,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(path)
    print(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
