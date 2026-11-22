#!/usr/bin/env python3
"""Genera il quaderno degli undici esperimenti di Gemina.

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
    "id", "titolo", "obiettivo", "parametri_iniziali", "passi",
    "consegna", "verifica_locale", "limiti",
)

def clean(text: str) -> str:
    """Normalize typographic hyphens while preserving mathematical symbols."""
    return str(text).replace("\u2011", "-").replace("\u2013", "-").replace(
        "\u2014", "-"
    ).replace("\u2212", "-")


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
    return ['source("setup.R", encoding = "UTF-8")',
            'rA <- lab_'+e['id']+'()',
            'rB <- lab_'+e['id']+'('+e['variante']+')',
            'rbind(base = rA$metrics, variante = rB$metrics)']


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


def page_base(c, page, lab=None):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(TEAL); c.rect(MARGIN,H-37,4,7,fill=1,stroke=0)
    c.setFont('LiberationSans-Bold',8.6)
    c.drawString(MARGIN+11,H-36,'GEMINA / CONFRONTI FRA GRUPPI')
    c.setFillColor(MUTED); c.setFont('LiberationSans',8.6)
    c.drawRightString(W-MARGIN,H-36,'QUADERNO STUDENTI' if lab is None else f'ESPERIMENTO {lab:02d} / 11')
    c.setStrokeColor(RULE); c.setLineWidth(.6)
    c.line(MARGIN,39,W-MARGIN,39)
    c.setFont('LiberationSans',8.3)
    c.drawString(MARGIN,25,'Gemina · Modulo M06 · Quaderno di esercitazione')
    c.drawRightString(W-MARGIN,25,f'{page} / 12')
    if page>1:c.linkAbsolute('Indice','indice',Rect=(MARGIN,18,MARGIN+270,34),thickness=0)

def writing_lines(c,y,n=2):
    c.setStrokeColor(RULE);c.setLineWidth(.4)
    for i in range(n):c.line(MARGIN,y-15-i*19,W-MARGIN,y-15-i*19)
    return y-n*19-3

def result_table(c,e,y):
    y=label(c,'Risultati da completare',MARGIN,y)
    widths=[76,(WIDTH-76)/3,(WIDTH-76)/3,(WIDTH-76)/3]
    header_h=30;row_h=28;bottom=y-header_h-2*row_h
    c.setFillColor(NAVY);c.rect(MARGIN,y-header_h,WIDTH,header_h,stroke=0,fill=1)
    x=MARGIN
    hs=ParagraphStyle('table',fontName='LiberationSans-Bold',fontSize=9.4,leading=11.4,textColor=white)
    for name,width in zip(e['tabella'],widths):
        draw_p(c,name,x+7,y-5,width-14,hs);x+=width
    c.setStrokeColor(RULE);c.setLineWidth(.5)
    for k in range(3):c.line(MARGIN,y-header_h-k*row_h,W-MARGIN,y-header_h-k*row_h)
    x=MARGIN
    for width in widths:
        c.line(x,y-header_h,x,bottom);x+=width
    c.line(x,y-header_h,x,bottom)
    c.setFillColor(INK);c.setFont('LiberationSans',10.2)
    for i,name in enumerate(['Base','Variante']):c.drawString(MARGIN+7,y-header_h-18-i*row_h,name)
    return bottom

def exercise_page(c,e,n,st):
    page_base(c,n+1,n)
    key='m06-'+e['id'];c.bookmarkPage(key)
    c.addOutlineEntry(f'{n:02d} - '+e['titolo'],key,level=0)
    y=H-57
    y=draw_p(c,e['titolo'],MARGIN,y,WIDTH,st['title'])-8
    c.setFillColor(TEAL);c.setFont('LiberationSans',9.3)
    link='Apri il laboratorio: '+key
    c.drawString(MARGIN,y-9.3,link)
    c.linkURL(LAB_URL+key,(MARGIN,y-13,MARGIN+pdfmetrics.stringWidth(link,'LiberationSans',9.3),y),relative=0,thickness=0)
    y-=25
    y=plain_block(c,'Obiettivo',e['obiettivo'],y,st)-9
    y=tint_block(c,'Impostazioni del confronto',e['parametri'],y,st)-10
    y=numbered(c,'Procedura',e['passi'],y,st)-7
    y=result_table(c,e,y)-12
    filename=f'Esercizi/{n:02d}_{e["id"]}.R'
    y=draw_code(c,verification_lines(e),filename,y)-10
    y=plain_block(c,'Condizioni e limiti',e['limite'],y,st,style='small')
    if y<54:raise RuntimeError(f'Pagina {n+1}: contenuto troppo basso ({y:.1f} pt)')
    c.showPage()
    return {'pagina':n+1,'id':key,'fondo_contenuto_pt':round(y,2)}

def intro_page(c,d,st):
    page_base(c,1);c.bookmarkPage('indice');c.addOutlineEntry('Come usare il quaderno','indice',0)
    y=H-63
    y=draw_p(c,'Gemina',MARGIN,y,WIDTH,st['intro_title'])-3
    y=draw_p(c,'Quaderno di esercitazione',MARGIN,y,WIDTH,st['subtitle'])-13
    y=draw_p(c,d['sottotitolo'],MARGIN,y,WIDTH,st['body'])-17
    y=numbered(c,'Come lavorare',[
      'Esegui lo scenario base e la variante, cambiando soltanto il parametro indicato.',
      'Annota i risultati senza ridurli alla dicitura significativo/non significativo. Specifica contrasto, unità e condizioni del confronto.',
      'Completa la tabella. Il seme riproduce una simulazione nello stesso ambiente R.'
    ],y,st)-12
    y=tint_block(c,'Nel progetto R',
       'Apri Gemina_M06.Rproj. Gli script in Esercizi/ caricano setup.R e le funzioni lab_*. '
       'Ogni funzione restituisce data (dati), metrics (statistiche non arrotondate) e parametri. '
       'Il codice usa soltanto R base; non richiede installazioni aggiuntive.',y,st)-12
    y=draw_code(c,[
      '# Dalla cartella del progetto:',
      'source("Esercizi/01_contrasto.R",',
      '       encoding = "UTF-8", echo = TRUE)'],
      'Avvio di un esercizio',y)-13
    y=draw_p(c,'I dati dei laboratori sono sintetici e senza unità fisiche assegnate. '
      'I CSV del corso nella cartella Dati/ sono casi distinti. '
      'Le soluzioni e i valori attesi si trovano nei materiali per il docente.',MARGIN,y,WIDTH,st['small'])-16
    y=label(c,'Indice degli esperimenti',MARGIN,y)
    for i,e in enumerate(d['esercizi'],1):
        c.setFillColor(TEAL);c.setFont('LiberationSans-Bold',9.5)
        c.drawString(MARGIN,y-10,f'{i:02d}')
        c.setFillColor(NAVY);c.setFont('LiberationSans',10.2)
        c.drawString(MARGIN+25,y-10,e['titolo'])
        c.setFillColor(MUTED);c.drawRightString(W-MARGIN,y-10,str(i+1))
        c.setStrokeColor(RULE);c.setLineWidth(.35);c.line(MARGIN,y-17,W-MARGIN,y-17)
        c.linkAbsolute(e['titolo'],'m06-'+e['id'],Rect=(MARGIN,y-19,W-MARGIN,y+3),thickness=0)
        y-=21
    if y<51:raise RuntimeError(f'Indice: contenuto troppo basso {y}')
    c.showPage();return {'pagina':1,'id':'introduzione','fondo_contenuto_pt':round(y,2)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=HERE)
    args=parser.parse_args();out=args.output_dir;out.mkdir(exist_ok=True,parents=True)
    d=json.loads((HERE/'Quaderno_contenuti_studenti.json').read_text())
    assert len(d['esercizi'])==11
    register_fonts();st=styles();path=out/'Gemina_M06_quaderno_esercizi.pdf'
    c=canvas.Canvas(str(path),pagesize=A4,pageCompression=1)
    c.setTitle('Gemina - Quaderno di esercitazione');c.setAuthor('Marzio De Corato')
    c.setSubject('Undici esperimenti: confronti, ipotesi e interpretazione')
    checks=[intro_page(c,d,st)]
    for n,e in enumerate(d['esercizi'],1):checks.append(exercise_page(c,e,n,st))
    c.save()
    (out/'Verifica_impaginazione.json').write_text(json.dumps({'pagine':12,'corpo_pt':10.6,'codice_pt':10,'verifiche':checks},ensure_ascii=False,indent=2))
    print(path);print(checks)
if __name__=='__main__':main()
