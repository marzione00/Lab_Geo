#!/usr/bin/env python3
"""GeoStat Lab: importa una lezione Beamer nel sito.

Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)

Uso dalla radice del repository:
    python3 -I scripts/lessons/import_lesson.py M05 [--no-images] [--no-r]

Legge lezioni/lezioni.json e produce:
  content/lezioni/<ID>.json      tappe, testo delle slide, codice, uscite di riferimento, laboratori
  content/esercizi/<ID>.json     schede del quaderno con i controlli numerici
  assets/lezioni/<ID>/           PDF con i codici di tappa, immagini delle slide
Il PDF e le slide restano quelli forniti: il codice di tappa viene sovrapposto alle pagine.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = 'https://marzione00.github.io/Lab_Geo/'
CODE = re.compile(r'^(\d{2,3})_.*\.R$')

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print('avviso: ' + msg, file=sys.stderr)


# ---------------------------------------------------------------- LaTeX minimo
def group(s, i):
    """Restituisce (contenuto, indice dopo la graffa) per il gruppo che inizia in s[i] == '{'."""
    if s[i] != '{':
        raise ValueError('gruppo atteso alla posizione %d: %r' % (i, s[i:i + 40]))
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('graffa non chiusa')


def args(s, i, n):
    out = []
    for _ in range(n):
        while s[i] in ' \n%':
            i += 1
        a, i = group(s, i)
        out.append(a)
    return out, i


SIMPLE = {
    r'\par': ' ', r'\%': '%', r'\&': '&', r'\#': '#', r'\_': '_', r'\{': '{', r'\}': '}', r'\ldots': '…',
    r'\textcopyright{}': '©', r'\,': '\u202f', r'\ ': ' ', r'\-': '',
    r'\textasciicircum{}': '^', r'\textasciitilde{}': '~',
}
# Testo monospaziato delle uscite registrate: soltanto gli escape dei caratteri speciali.
TT = {r'\ ': ' ', r'\_': '_', r'\%': '%', r'\&': '&', r'\#': '#', r'\{': '{', r'\}': '}', r'\$': '$',
      r'\textasciicircum{}': '^', r'\textasciitilde{}': '~', r'\textbackslash{}': '\\'}


def tt(t):
    for k, v in TT.items():
        t = t.replace(k, v)
    return t


def plain(t):
    t = t.replace('~', '\u00a0')  # legatura di TeX; \\textasciitilde{} resta una tilde
    for k, v in SIMPLE.items():
        t = t.replace(k, v)
    t = t.replace('---', '—').replace('--', '–')
    t = re.sub(r'\\\\(\[[^\]]*\])?', ' ', t)
    return t


SPACING = re.compile(r'\\rule\{[^{}]*\}\{[^{}]*\}|\\(?:vspace|hspace)\*?\{[^{}]*\}|\\(?:smallskip|medskip|bigskip|noindent|centering|raggedright|newline|linebreak|allowbreak)\b\s*')


def inline(tex):
    tex = SPACING.sub(' ', tex)
    return _inline(tex)


def _inline(tex):
    """LaTeX di un paragrafo → lista di nodi: testo, {t:m} formula, {t:c} codice, {t:b}, {t:i}, {t:a}."""
    nodes, i, buf = [], 0, ''

    def flush():
        nonlocal buf
        if buf:
            nodes.append(plain(buf))
            buf = ''

    while i < len(tex):
        if tex[i] == '$':
            j = tex.index('$', i + 1)
            flush()
            nodes.append({'t': 'm', 'v': tex[i + 1:j].strip()})
            i = j + 1
            continue
        if tex.startswith(r'\(', i):
            j = tex.index(r'\)', i + 2)
            flush()
            nodes.append({'t': 'm', 'v': tex[i + 2:j].strip()})
            i = j + 2
            continue
        m = re.match(r'\\(texttt|textbf|emph|textit|href|mbox|text|textsc|MakeUppercase|textcolor|texorpdfstring|hyperlink|shortstack)\b',
                     tex[i:])
        if m:
            name = m.group(1)
            flush()
            j = i + len(m.group(0))
            if name == 'href':
                (url, label), j = args(tex, j, 2)
                nodes.append({'t': 'a', 'h': site_url(url), 'c': inline(bare(label))})
            elif name == 'hyperlink':
                (target, body), j = args(tex, j, 2)
                m2 = re.fullmatch(r'slide(\d+)', target)
                if m2:  # rimando a un'altra slide: diventa la tappa corrispondente
                    nodes.append({'t': 'a', 'h': '#tappa-' + m2.group(1), 'c': inline(bare(body))})
                else:
                    nodes.extend(inline(body))
            elif name == 'textcolor':
                (_, body), j = args(tex, j, 2)
                nodes.extend(inline(body))
            elif name == 'texorpdfstring':
                (body, _), j = args(tex, j, 2)
                nodes.extend(inline(body))
            else:
                (body,), j = args(tex, j, 1)
                if name == 'texttt':
                    nodes.append({'t': 'c', 'v': plain(body)})
                elif name == 'textbf':
                    nodes.append({'t': 'b', 'c': inline(body)})
                elif name in ('emph', 'textit'):
                    nodes.append({'t': 'i', 'c': inline(body)})
                else:
                    nodes.extend(inline(body))
            i = j
            continue
        key = next((k for k in [r'\\'] + list(SIMPLE) if tex.startswith(k, i)), None)
        if key:
            buf += key
            i += len(key)
            continue
        m = re.match(r'\\([A-Za-z]+)', tex[i:])
        if m:
            raise ValueError('macro non gestita nel testo: \\%s in %r' % (m.group(1), tex[:80]))
        buf += tex[i]
        i += 1
    flush()
    merged = []
    for n in nodes:
        if isinstance(n, str) and merged and isinstance(merged[-1], str):
            merged[-1] += n
        else:
            merged.append(n)
    if merged and isinstance(merged[0], str):
        merged[0] = re.sub(r'^\s+', '', merged[0])
    if merged and isinstance(merged[-1], str):
        merged[-1] = re.sub(r'\s+$', '', merged[-1])
    return [re.sub(r'\s+', ' ', n) if isinstance(n, str) else n for n in merged if n != '']


SITE = 'https://marzione00.github.io/Lab_Geo/'
REPO = re.compile(r'https://github\.com/marzione00/Lab_Geo/blob/[0-9a-f]{7,40}/(materiali/[\w./-]+)$')


def bare(t):
    """Testo di un'etichetta senza colori, corpi e grassetti dichiarati (\\color, \\fontsize, \\bfseries)."""
    t = re.sub(r'\\hfill\s*', ' · ', t)
    return unwrap(LAYOUT.sub(' ', re.sub(r'\\(?:bfseries|normalfont|sffamily|small)\b', '', t)))


def site_url(url):
    """Indirizzi del sito e dei materiali del repository resi relativi al sito."""
    url = url.replace(r'\#', '#').replace(r'\_', '_')
    if url.startswith(SITE):
        return url[len(SITE):] or '#indice'
    m = REPO.match(url)
    return m.group(1) if m else url


def text_of(nodes):
    out = ''
    for n in nodes:
        if isinstance(n, str):
            out += n
        elif n['t'] in ('m', 'c'):
            out += n['v']
        else:
            out += text_of(n['c'])
    return out


ITEM = re.compile(r'\\(PLabel|PBody|PSmall|PInfo|PCode|PLab)\{|(?<!\\)\\\[|\\begin\{tikzpicture\}|'
                  r'\\includegraphics(?:\[([^\]]*)\])?\{([^}]*)\}|\\begin\{tabular\}|'
                  r'\\resizebox\{([\d.]*)\\linewidth\}\{!\}\{\\input\{([^}]*)\}\}|\\input\{([^}]*)\}|'
                  r'\\adjustbox\{[^{}]*\}\{(?=\$)|\\begin\{tcolorbox\}')
# Formattazione e spaziature fra i riquadri: non producono testo.
LAYOUT = re.compile(r'\\begin\{minipage\}(?:\[[^\]]*\])?\{[^}]*\}|\\end\{minipage\}|\\(?:begin|end)\{center\}|'
                    r'\\color\{[^}]*\}|\\fontsize\{[^}]*\}\{[^}]*\}|\\selectfont|\\raggedright|\\centering|'
                    r'\\renewcommand\{\\arraystretch\}\{[^}]*\}|\\(?:vspace|hspace)\*?\{[^}]*\}|\\par\b|\\nointerlineskip|'
                    r'\\hfill|\\(?:small|med|big)skip|\\noindent|\\rule\{[^}]*\}\{[^}]*\}|%[^\n]*')


def unwrap(text):
    """Toglie le graffe dei gruppi nudi ({\\bfseries ...}); conserva quelle degli argomenti delle macro."""
    out, i, chain = '', 0, -1  # chain: fine dell'ultimo argomento di macro emesso in out
    while i < len(text):
        c = text[i]
        if c == '\\':
            out += text[i:i + 2]
            i += 2
            continue
        if c == '{':
            try:
                body, j = group(text, i)
            except ValueError:  # gruppo aperto prima di un riquadro e chiuso dopo
                i += 1
                continue
            # Argomento: segue il nome di una macro o un argomento precedente della stessa macro.
            arg = re.search(r'\\[A-Za-z]+\*?\s*$', out) or (chain >= 0 and not out[chain:].strip())
            if arg:
                out += '{' + unwrap(body) + '}'
                chain = len(out)
            else:
                out += unwrap(body)
                chain = -1
            i = j
            continue
        if c == '}':
            i += 1
            continue
        out += c
        if not c.isspace():
            chain = -1
        i += 1
    return out


def split_top(text, sep):
    """Divide al separatore (regex) soltanto fuori dalle graffe."""
    out, depth, start, i = [], 0, 0, 0
    pat = re.compile(sep)
    while i < len(text):
        c = text[i]
        if c == '\\' and depth == 0:
            m = pat.match(text, i)
            if m:
                out.append(text[start:i])
                start = i = m.end()
                continue
            i += 2
            continue
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif depth == 0 and pat.pattern == '&' and c == '&':
            out.append(text[start:i])
            start = i = i + 1
            continue
        i += 1
    out.append(text[start:])
    return out


def table(spec_body):
    """tabular → intestazione e righe di celle (nodi in linea); \\multicolumn conserva l'estensione."""
    body = re.sub(r'\\(?:toprule|bottomrule|hline)\b|\\cmidrule(?:\([^)]*\))?\{[^}]*\}', '', spec_body)
    parts = re.split(r'\\midrule\b', body, maxsplit=1)
    def rows(text):
        out = []
        for r in split_top(text, r'\\\\(?:\[[^\]]*\])?'):
            if not r.strip():
                continue
            cells = []
            for c in split_top(r, '&'):
                span = 1
                mc = re.match(r'\s*\\multicolumn\{(\d+)\}\{[^}]*\}\{(.*)\}\s*$', c, re.S)
                if mc:
                    span, c = int(mc.group(1)), mc.group(2)
                c = re.sub(r'\\(?:bfseries|centering|raggedright|arraybackslash)\b', '', c)
                cells.append({'c': inline(c.strip()), 'span': span} if span > 1 else {'c': inline(c.strip())})
            out.append(cells)
        return out
    head = rows(parts[0]) if len(parts) == 2 else []
    return {'t': 'table', 'head': head, 'rows': rows(parts[-1])}


def raw_text(text):
    """Testo libero fra i riquadri (per esempio un paragrafo in grassetto): un paragrafo per ogni \\par."""
    out = []
    # Nell'indice il numero di pagina dopo \\hfill ripete la destinazione del collegamento.
    text = re.sub(r'\\hfill\s*\d+(?=\s*\})', '', text)
    t = unwrap(LAYOUT.sub(' ', re.sub(r'\\par\b', '\0', text)))
    for piece in t.split('\0'):
        bold = r'\bfseries' in piece
        nodes = inline(piece.replace(r'\bfseries', '')) if piece.strip() else []
        if nodes:
            out.append({'t': 'p', 'c': [{'t': 'b', 'c': nodes}] if bold else nodes})
    return out


def items(chunk):
    out, i = [], 0
    while True:
        m = ITEM.search(chunk, i)
        out.extend(raw_text(chunk[i:m.start() if m else len(chunk)]))
        if not m:
            return out
        tok = m.group(0)
        if tok == r'\[':
            j = re.compile(r'(?<!\\)\\\]').search(chunk, m.end()).start()
            out.append({'t': 'math', 'v': re.sub(r'\s+', ' ', chunk[m.end():j]).strip()})
            i = j + 2
        elif tok.startswith(r'\begin{tikz'):
            j = chunk.index(r'\end{tikzpicture}', m.end()) + len(r'\end{tikzpicture}')
            out.append({'t': 'figure', 'tex': chunk[m.start():j]})
            i = j
        elif tok.startswith(r'\includegraphics'):
            out.append({'t': 'figure', 'file': m.group(3), 'opts': m.group(2) or ''})
            i = m.end()
        elif tok.startswith(r'\resizebox') or tok.startswith(r'\input'):
            # Diagramma TikZ in un file a parte, eventualmente scalato alla larghezza della colonna.
            path = m.group(5) or m.group(6)
            it = {'t': 'figure', 'input': path if path.endswith('.tex') else path + '.tex'}
            if m.group(5):
                it['scale'] = float(m.group(4) or 1)
            out.append(it)
            i = m.end()
        elif tok.startswith(r'\adjustbox'):
            body, i = group(chunk, m.end() - 1)
            out.append({'t': 'math', 'v': re.sub(r'\s+', ' ', body.strip().strip('$')).replace(r'\displaystyle', '').strip()})
        elif tok.startswith(r'\begin{tcolorbox'):
            j = m.end()
            opts = ''
            if chunk.startswith('[', j):
                depth, k = 0, j
                while True:
                    depth += {'[': 1, ']': -1}.get(chunk[k], 0)
                    if depth == 0:
                        break
                    k += 1
                opts, j = chunk[j + 1:k], k + 1
            k = chunk.index(r'\end{tcolorbox}', j)
            out.extend(tcolorbox(opts, chunk[j:k]))
            i = k + len(r'\end{tcolorbox}')
        elif tok.startswith(r'\begin{tabular'):
            _, j = group(chunk, m.end())
            k = chunk.index(r'\end{tabular}', j)
            out.append(table(chunk[j:k]))
            i = k + len(r'\end{tabular}')
        else:
            name = m.group(1)
            n = 2 if name in ('PCode', 'PLab') else 1
            a, i = args(chunk, m.end() - 1, n)
            if name == 'PCode':
                out.append({'t': 'code', 'title': plain(a[0]), 'file': a[1]})
            elif name == 'PLab':
                out.append({'t': 'lab', 'url': a[0].replace(r'\#', '#'), 'c': inline(a[1])})
            else:
                out.append({'t': {'PLabel': 'label', 'PBody': 'p', 'PSmall': 'small', 'PInfo': 'info'}[name],
                            'c': inline(a[0])})


def tcolorbox(opts, body):
    """Riquadri tcolorbox delle presentazioni T00 e M13-M16: codice da file o uscita registrata di R."""
    lst = re.search(r'\\lstinputlisting(?:\[([^\]]*)\])?\{Codice/([^}]*)\}', body)
    if lst:
        title = re.search(r'title=\{([^{}]*)\}', opts)
        return [{'t': 'code', 'title': plain(title.group(1)) if title else 'Codice', 'file': lst.group(2)}]
    if r'\ttfamily' in body:
        lines = [tt(ln) for ln in re.findall(r'\\mbox\{((?:[^{}]|\{[^{}]*\})*)\}', body)]
        return [{'t': 'out', 'v': '\n'.join(lines)}]
    return items(body)


BOXES = {'PilotLeftBox': 'L', 'PilotRightBox': 'R', 'FullWideBox': 'W', 'TitleBox': None, 'RecallBox': None}
# Colonne \Colonna{larghezza}{...} delle presentazioni T00 e M13-M16.
COLONNE = {'9.40': 'L', '8.16': 'R'}


def boxes(pre, page):
    """Riquadri della slide: colonna sinistra, destra o a tutta larghezza, con la larghezza in cm."""
    out = []
    for m in re.finditer(r'\\Colonna\{([\d.]+)cm\}\{', pre):
        body, _ = group(pre, m.end() - 1)
        for it in items(body):
            it['col'] = COLONNE[m.group(1)]
            if it['t'] == 'figure':
                it['box'] = float(m.group(1))
            out.append(it)
    for m in re.finditer(r'\\begin\{lrbox\}\{\\(\w+)\}(.*?)\\end\{lrbox\}', pre, re.S):
        # Titolo e «Da ricordare» ripetono gli argomenti di \PilotChrome.
        if BOXES[m.group(1)] is None:
            continue
        width = float(re.search(r'\\begin\{minipage\}\[t\]\{([\d.]+)cm\}', m.group(2)).group(1))
        for it in items(m.group(2)):
            it['col'] = BOXES[m.group(1)]
            if it['t'] == 'figure':
                it['box'] = width
            out.append(it)
    if not out:
        return []
    k = 0
    for it in out:
        if it['t'] == 'figure':
            k += 1
            it['fig'] = '%03d-%d' % (page, k)
    return out


def parse_tex(path):
    tex = path.read_text(encoding='utf-8')
    body = tex[tex.index(r'\begin{document}'):]
    slides, pre_start = [], 0
    for fm in re.finditer(r'\\begin\{frame\}(?:\[[^\]]*\])?(.*?)\\end\{frame\}', body, re.S):
        frame, pre = fm.group(1), body[pre_start:fm.start()]
        pre_start = fm.end()
        page = int(re.search(r'\\hypertarget\{slide(\d+)\}', frame).group(1))
        s = {'page': page}
        c = frame.find(r'\PilotChrome{')
        if c >= 0:
            (title, section, num, recall), _ = args(frame, c + len(r'\PilotChrome'), 4)
            if int(num) != page:
                raise ValueError('numero di pagina incoerente nella slide %d' % page)
            s.update(title=text_of(inline(bare(title))), section=text_of(inline(section)), recall=inline(recall))
            # I riquadri possono precedere il frame (M03-M06) o stare al suo interno (M07-M16).
            s['items'] = boxes(pre + frame, page)
            for it in s['items']:
                if 'input' in it:
                    it['tex'] = (path.parent / it.pop('input')).read_text(encoding='utf-8')
            if r'\Colonna{' in frame:
                s['footer'] = footer_links(frame)
        else:
            s['items'] = []
            s['custom'] = frame
        slides.append(s)
    return tex, slides


def footer_links(frame):
    """Collegamenti nel piè di pagina (T00, M13-M16): laboratorio del sito o script R6 dei materiali."""
    out, spans = [], []
    for m in re.finditer(r'\\Colonna\{[\d.]+cm\}\{', frame):
        _, j = group(frame, m.end() - 1)
        spans.append((m.start(), j))
    for m in re.finditer(r'\\href\{', frame):
        if any(a <= m.start() < b for a, b in spans):
            continue
        (url, label), _ = args(frame, m.end() - 1, 2)
        out.append({'h': site_url(url), 'c': inline(bare(label))})
    return out


FORMAT = re.compile(r'\\(?:color|fontsize|begin\{minipage\})(?:\{[^{}]*\}){1,2}|\\end\{minipage\}|'
                    r'\\(?:bfseries|normalfont|raggedright|selectfont)\b')


def node_texts(frame):
    """Testo dei nodi TikZ di una pagina composta a mano (copertina, domanda centrale)."""
    out = []
    for m in re.finditer(r'\\node\[[^\]]*\](?:\s*\([^)]*\))?\s*at\s*\((?:[^()]|\([^()]*\))*\)\s*\{', frame):
        body, _ = group(frame, m.end() - 1)
        body = FORMAT.sub('', body)
        body = re.sub(r'\\includegraphics(\[[^\]]*\])?\{[^}]*\}', '', body)
        body = re.sub(r'\\hyperlink\{[^}]*\}', '', body)
        body = re.sub(r'\\\\\[[^\]]*\]', ' · ', body)
        t = text_of(inline(body)).strip()
        if t:
            out.append(t)
    return out


def custom_pages(slides, meta_title):
    for s in slides:
        if 'custom' not in s:
            continue
        texts = node_texts(s.pop('custom'))
        if s['page'] == 1:
            s.update(title=meta_title, section='COPERTINA', lines=texts, recall=[])
        else:
            guide = texts.index('IDEA GUIDA')
            s.update(title=texts[0], section='DOMANDA CENTRALE', question=texts[1], steps=texts[2:guide],
                     recall=[texts[guide + 1]])


# ---------------------------------------------------------------- PDF
def pdf_pages(pdf):
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', info).group(1))


def pdf_text(pdf, page):
    return subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-layout', str(pdf), '-'],
                          capture_output=True, text=True, check=True).stdout


def norm(t):
    t = t.replace('’', "'").replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    return re.sub(r'[^a-z0-9àèéìòù]+', '', t.lower())


def stamp_pdf(src_pdf, out_pdf, lesson_id, planet, pages, workdir, colour='087C74'):
    """Sovrappone a ogni pagina, dalla terza, il codice di tappa con il collegamento al sito.

    Un PDF compilato dal sorgente aggiornato (\\PilotChrome con il codice di tappa) lo contiene già:
    in quel caso il file viene soltanto compattato."""
    if all('Sul sito: %s · %d' % (planet, p) in pdf_text(src_pdf, p) for p in (3, pages)):
        subprocess.run(['qpdf', '--object-streams=generate', '--compress-streams=y', '--deterministic-id',
                        str(src_pdf), str(out_pdf)], check=True)
        return 'presente nel PDF'
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, FloatObject, NameObject, NumberObject, TextStringObject
    w, h = 566.93, 354.33
    tex = [r'\documentclass{article}', r'\usepackage[paperwidth=566.93bp,paperheight=354.33bp,margin=0pt]{geometry}',
           r'\usepackage{fontspec}\setmainfont{Nimbus Sans}', r'\usepackage{xcolor}',
           r'\definecolor{Classical}{HTML}{' + colour + '}', r'\pagestyle{empty}\usepackage{tikz}', r'\begin{document}']
    for p in range(1, pages + 1):
        tex.append(r'\begin{tikzpicture}[remember picture,overlay]')
        if p >= 3:
            tex.append(r'\node[anchor=north,inner sep=0] at ([xshift=10cm,yshift=-12.06cm]current page.north west)'
                       r' {\color{Classical}\fontsize{7.7}{9.2}\selectfont Sul sito: ' + planet + r' · ' + str(p) + '};')
        tex.append(r'\end{tikzpicture}\newpage')
    tex.append(r'\end{document}')
    (workdir / 'stamp.tex').write_text('\n'.join(tex), encoding='utf-8')
    for _ in range(2):
        subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'stamp.tex'], cwd=workdir,
                       capture_output=True, check=True,
                       env={**os.environ, 'SOURCE_DATE_EPOCH': '1767225600', 'FORCE_SOURCE_DATE': '1'})
    base, over = PdfReader(str(src_pdf)), PdfReader(str(workdir / 'stamp.pdf'))
    if len(over.pages) != pages:
        raise ValueError('pagine sovrapposte: %d invece di %d' % (len(over.pages), pages))
    writer = PdfWriter(clone_from=base)
    for p in range(3, pages + 1):
        page = writer.pages[p - 1]
        page.merge_page(over.pages[p - 1])
        # Area attiva sopra il codice di tappa: 10 cm dal margine sinistro, 12,06 cm dall'alto.
        cx, top = 10 / 2.54 * 72, h - 12.06 / 2.54 * 72
        rect = [cx - 60, top - 10, cx + 60, top + 2]
        link = DictionaryObject({
            NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Link'),
            NameObject('/Rect'): ArrayObject([FloatObject(v) for v in rect]),
            NameObject('/Border'): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]),
            NameObject('/A'): DictionaryObject({
                NameObject('/S'): NameObject('/URI'),
                NameObject('/URI'): TextStringObject(SITE + '#lezione-' + lesson_id + '/' + str(p))}),
        })
        annots = page.get('/Annots')
        if annots is None:
            page[NameObject('/Annots')] = ArrayObject()
            annots = page['/Annots']
        annots.get_object().append(writer._add_object(link))
    writer.add_metadata({'/Subject': 'Codici di tappa: ' + SITE + '#lezione-' + lesson_id})
    with open(workdir / 'stamped.pdf', 'wb') as f:
        writer.write(f)
    # pypdf scrive oggetti non compressi: qpdf ricostruisce flussi e tabelle compatte.
    subprocess.run(['qpdf', '--object-streams=generate', '--compress-streams=y', '--recompress-flate',
                    '--compression-level=9', '--deterministic-id', str(workdir / 'stamped.pdf'), str(out_pdf)], check=True)
    return 'sovrapposto'


SVG_HEAD = re.compile(r'<svg([^>]*?) width="[\d.]+" height="[\d.]+" viewBox="[\d. ]+"')


def crop_svg(svg, x, y, w, h):
    """Restringe la vista di una pagina SVG di pdftocairo al rettangolo indicato (in punti)."""
    out, n = SVG_HEAD.subn(lambda m: '<svg%s width="%g" height="%g" viewBox="%g %g %g %g"' % (m.group(1), w, h, x, y, w, h),
                           svg, count=1)
    if n != 1:
        raise ValueError('intestazione SVG inattesa')
    return out


def graphic(src, name):
    r"""Percorso di un \includegraphics: relativo alla lezione o alle cartelle di \graphicspath."""
    for base in (src, src / 'Risorse' / 'Figure'):
        for ext in ('', '.pdf', '.png', '.jpg'):
            p = base / (name + ext)
            if p.is_file():
                return p
    hits = [p for p in src.rglob(Path(name).name + '*') if p.suffix.lower() in ('.pdf', '.png', '.jpg')]
    if len(hits) == 1:
        return hits[0]
    raise ValueError('grafico non trovato: ' + name)


def width_cm(opts, box):
    m = re.search(r'width=([\d.]+)\s*(cm|mm)', opts)
    if m:
        return float(m.group(1)) / (10 if m.group(2) == 'mm' else 1)
    m = re.search(r'width=([\d.]*)\\(?:linewidth|textwidth)', opts)
    if m:
        return (float(m.group(1)) if m.group(1) else 1) * box
    return None


def figures(tex, slides, cfg, src, pdf, outdir, lesson_id, workdir):
    """Figure dei riquadri: TikZ compilato con il preambolo della lezione, grafici inclusi convertiti in SVG,
    ritagli dichiarati del PDF per le parti assenti dal sorgente."""
    outdir.mkdir(parents=True, exist_ok=True)
    for old in list(outdir.glob('*.svg')) + list(outdir.glob('*.webp')):
        old.unlink()
    figs = [(s, it) for s in slides for it in s['items'] if it['t'] == 'figure']
    build = [(s, it) for s, it in figs if it.get('tex', '').count('\\') > 2]
    env = {**os.environ, 'TEXINPUTS': str(src) + '//:', 'SOURCE_DATE_EPOCH': '1767225600'}
    bp = 72 / 72.27
    if build:
        preamble = tex[:tex.index(r'\begin{document}')]
        fc = subprocess.run(['fc-list', ':family=Nimbus Sans'], capture_output=True, text=True).stdout
        doc = [preamble, r'\setsansfont{Nimbus Sans}\setmainfont{Nimbus Sans}' if fc.strip() else '',
               r'\begin{document}']
        for i, (s, it) in enumerate(build):
            doc.append(r'\begin{frame}[plain]\setbox0=\hbox{\color{Ink}\fontsize{11.3}{14.8}\selectfont ' + it['tex'] +
                       '}' r'\typeout{FIGBOX:' + str(i) + r':\the\wd0:\the\ht0:\the\dp0}'
                       r'\begin{tikzpicture}[remember picture,overlay]\node[anchor=north west,inner sep=0] at '
                       r'([xshift=3bp,yshift=-3bp]current page.north west) {\copy0};\end{tikzpicture}\end{frame}')
        doc.append(r'\end{document}')
        (workdir / 'figure.tex').write_text('\n'.join(doc), encoding='utf-8')
        for _ in range(2):
            r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'figure.tex'], cwd=workdir,
                               capture_output=True, text=True, env=env)
            if r.returncode:
                raise ValueError('compilazione delle figure non riuscita:\n' + r.stdout[-3000:])
        log = (workdir / 'figure.log').read_text(encoding='utf-8', errors='replace')
        dims = {int(m[1]): (float(m[2]), float(m[3]) + float(m[4]))
                for m in re.finditer(r'FIGBOX:(\d+):([\d.]+)pt:([\d.]+)pt:([\d.]+)pt', log)}
        if len(dims) != len(build):
            raise ValueError('dimensioni delle figure incomplete: %d su %d' % (len(dims), len(build)))
        for i, (s, it) in enumerate(build):
            w, h = math.ceil(dims[i][0] * bp) + 6, math.ceil(dims[i][1] * bp) + 6
            subprocess.run(['pdftocairo', '-svg', '-f', str(i + 1), '-l', str(i + 1), str(workdir / 'figure.pdf'),
                            str(workdir / 'f.svg')], check=True)
            svg = crop_svg((workdir / 'f.svg').read_text(encoding='utf-8'), 0, 0, w, h)
            (outdir / (it['fig'] + '.svg')).write_text(svg, encoding='utf-8')
            it.update(w=w, h=h, ext='svg')
    crops = cfg.get('fromPdfFigures', {})
    for s, it in figs:
        if any(it is b for _, b in build):
            continue
        if 'file' in it:
            path = graphic(src, it['file'])
            if path.suffix.lower() == '.pdf':
                subprocess.run(['pdftocairo', '-svg', '-f', '1', '-l', '1', str(path), str(outdir / (it['fig'] + '.svg'))],
                               check=True)
                head = (outdir / (it['fig'] + '.svg')).read_text(encoding='utf-8')[:600]
                m = re.search(r'width="([\d.]+)(?:pt)?" height="([\d.]+)(?:pt)?"', head)
                w, h, ext = float(m.group(1)), float(m.group(2)), 'svg'
            else:
                from PIL import Image
                im = Image.open(path).convert('RGB')
                im.save(outdir / (it['fig'] + '.webp'), quality=84, method=6)
                w, h, ext = im.size[0] * 72 / 150, im.size[1] * 72 / 150, 'webp'
            opts = it.pop('opts')
            wanted = width_cm(opts, it['box'])
            if wanted:
                h, w = h * (wanted / 2.54 * 72) / w, wanted / 2.54 * 72
            cap = re.search(r'height=([\d.]+)cm', opts)
            if cap and 'keepaspectratio' in opts and h > float(cap.group(1)) / 2.54 * 72:
                w, h = w * float(cap.group(1)) / 2.54 * 72 / h, float(cap.group(1)) / 2.54 * 72
            it.update(w=round(w), h=round(h), ext=ext, source=str(path.relative_to(src)))
            it.pop('file')
            continue
        rect = crops.get(str(s['page']), [25, 58, 516, 236])
        subprocess.run(['pdftocairo', '-svg', '-f', str(s['page']), '-l', str(s['page']), str(pdf),
                        str(workdir / 'f.svg')], check=True)
        svg = crop_svg((workdir / 'f.svg').read_text(encoding='utf-8'), *rect)
        (outdir / (it['fig'] + '.svg')).write_text(svg, encoding='utf-8')
        it.update(w=rect[2], h=rect[3], ext='svg')
    # Le figure vivono nel pannello scuro delle tappe: stessi ruoli di colore, sfondo del pannello.
    tone = load_tone()
    for s, it in figs:
        if it['ext'] == 'svg':
            path = outdir / (it['fig'] + '.svg')
            path.write_text(tone(path.read_text(encoding='utf-8')), encoding='utf-8')
    for s, it in figs:
        it['src'] = 'assets/lezioni/%s/figure/%s.%s' % (lesson_id, it['fig'], it.pop('ext'))
        box = it.pop('box') / 2.54 * 72
        # \resizebox{f\linewidth}: la figura occupa la frazione f della colonna qualunque sia la sua misura.
        it['ratio'] = round(it.pop('scale'), 3) if 'scale' in it else round(min(1, it['w'] / box), 3)
        it.pop('tex', None)
    return len(figs)


def load_tone():
    """Funzione di figure_tone.py, caricata dal file accanto a questo script."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('figure_tone', Path(__file__).with_name('figure_tone.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.tone


def project_zip(src, out, cfg):
    """Archivio per lavorare in RStudio: codice delle slide, dati, esercizi. Date fisse, ordine stabile."""
    import zipfile
    z = cfg['zip']
    names = []
    for pattern in z['include']:
        names += [p for p in sorted(src.glob(pattern)) if p.is_file()]
    root = z['folder']
    readme = '\n'.join(z['readme']) + '\n'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        def add(name, data):
            info = zipfile.ZipInfo(root + '/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
        add('LEGGIMI.txt', readme.encode('utf-8'))
        for f in ('LICENSE.md', 'LICENSE-CODE.md'):
            add(f, (ROOT / f).read_bytes())
        for p in names:
            add(p.relative_to(src).as_posix(), p.read_bytes())


# ---------------------------------------------------------------- laboratori
def lab_catalogue():
    acts = json.loads((ROOT / 'content/experiments.json').read_text(encoding='utf-8'))['activities']
    return {a['id']: a for a in acts}


def lab_link(acts, lab_id, params):
    a = acts.get(lab_id)
    if not a:
        raise ValueError('laboratorio inesistente: ' + lab_id)
    controls = {c['key']: c for c in a['controls']}
    for k, v in params.items():
        c = controls.get(k)
        if not c:
            raise ValueError('parametro %s assente in %s' % (k, lab_id))
        if c['type'] == 'select':
            if v not in [o['value'] for o in c['options']]:
                raise ValueError('opzione %r non valida per %s.%s' % (v, lab_id, k))
        else:
            steps = (v - c['min']) / c['step']
            if not (c['min'] <= v <= c['max']) or abs(steps - round(steps)) > 1e-6:
                raise ValueError('valore %r fuori dominio per %s.%s' % (v, lab_id, k))
    return {'id': lab_id, 'title': a['title'], 'params': params}


R_ARG = re.compile(r'([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*("[^"]*"|-?[0-9.]+)')


def labs_in_code(code, acts, prefix):
    out = []
    for m in re.finditer(r'\blab_([a-z]+)\(([^()]*)\)', code):
        params = {}
        for k, v in R_ARG.findall(m.group(2)):
            params[k] = v.strip('"') if v.startswith('"') else (int(v) if re.fullmatch(r'-?\d+', v) else float(v))
        try:
            out.append(lab_link(acts, prefix + m.group(1), params))
        except ValueError as e:
            warn('chiamata lab_%s senza laboratorio corrispondente nel sito (%s)' % (m.group(1), e))
    return out


# ---------------------------------------------------------------- esercizi
def tolerance(v):
    if float(v).is_integer():
        return 0
    from math import floor, log10
    return 0.5 * 10 ** (floor(log10(abs(v))) - 2)


def exercise_spec(cfg, src, book, prefix):
    """Specifica per exercise_checks.R: laboratorio, scenari A e B e valori attesi di ogni scheda.

    Le chiamate lab_*() della verifica locale danno gli scenari (M02-M05); in alternativa un file di
    scenari con i parametri (M06). I valori attesi vengono da Risultati_attesi_laboratori.csv, nelle
    sue varianti di colonne; expectedMap traduce gli scenari con nome (M02) in laboratorio e A o B."""
    spec = {'labs_file': cfg.get('labs'), 'cards': []}
    expected = {}
    if cfg.get('expected'):
        with open(src / cfg['expected'], encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                lab, sc = r.get('laboratorio'), r['scenario']
                if cfg.get('expectedMap'):
                    lab, sc = cfg['expectedMap'][sc]
                if r['valore'] == 'NA':  # indicatore non definito: il sito lo mostra senza valore
                    continue
                expected.setdefault(lab, {'A': [], 'B': []})[sc].append(
                    {'parametro': r.get('parametro') or r['indicatore'], 'valore': float(r['valore'])})
    scenarios = {}
    if cfg.get('scenarios'):
        for r in json.loads((src / cfg['scenarios']).read_text(encoding='utf-8')):
            scenarios.setdefault(prefix + r['id'], {})['A' if r['scenario'] == 'base' else 'B'] = r['parametri']
    for e in book['esercizi']:
        lab = e['id'] if e['id'].startswith(prefix) else prefix + e['id']
        card = {'id': lab, 'expected': expected.get(lab, {'A': [], 'B': []})}
        if lab in scenarios:
            card['params'] = scenarios[lab]
        else:
            calls = dict(re.findall(r'^r([AB]) <- (lab_[a-z_]+\(.*\))\s*$', e['verifica_locale'], re.M))
            if sorted(calls) != ['A', 'B']:
                raise ValueError('scenari A e B non trovati nella verifica di %s' % lab)
            card['calls'] = calls
        if cfg.get('expected') and not any(card['expected'].values()):
            raise ValueError('nessun valore atteso per %s' % lab)
        spec['cards'].append(card)
    return spec


def exercises(cfg, src, acts, workdir, prefix):
    book = json.loads((src / cfg['workbook']).read_text(encoding='utf-8'))
    spec_file, checks_file = workdir / 'spec.json', workdir / 'checks.json'
    spec_file.write_text(json.dumps(exercise_spec(cfg, src, book, prefix), ensure_ascii=False), encoding='utf-8')
    subprocess.run(['Rscript', str(ROOT / 'scripts/lessons/exercise_checks.R'), str(ROOT), str(src), str(spec_file),
                    str(checks_file)], check=True, env={'LC_ALL': 'C.UTF-8', 'PATH': '/usr/bin:/bin'})
    checks = json.loads(checks_file.read_text(encoding='utf-8'))
    cards = []
    for n, e in enumerate(book['esercizi'], 1):
        lab = e['id'] if e['id'].startswith(prefix) else prefix + e['id']
        ck = checks[lab]
        for m in ck.get('missing', []):
            warn('%s, scenario %s: indicatore %s del progetto non mostrato dal laboratorio del sito' % (
                lab, m['scenario'], m['parametro']))
        keys = {c['key'] for c in acts[lab]['controls']}
        labels = {}
        for c in ck['checks']:
            if c['scenario'] == 'A' and c['metrica']:
                # Il nome di quantile() resta attaccato all'etichetta («Percentile 2,5%.2.5%»): lo si toglie.
                labels[c['parametro']] = re.sub(r'\.\d+(?:\.\d+)?%$', '', c['metrica'])
        script = sorted((src / 'Esercizi').glob('%02d_*.R' % n))
        if len(script) != 1:
            raise ValueError('script dell\'esercizio %d non trovato' % n)
        scen = {name: {'link': lab_link(acts, lab, sc['params'] or {}), 'full': sc['full']}
                for name, sc in ck['scenarios'].items()}
        fields = []
        for c in ck['checks']:
            # Gli indicatori che ripetono un parametro dello scenario non verificano nulla.
            if c['parametro'] in cfg.get('echo', []) or c['parametro'] in keys or not labels.get(c['parametro']):
                continue
            fields.append({'scenario': c['scenario'], 'key': c['parametro'], 'label': labels[c['parametro']],
                           'value': c['valore'], 'tol': tolerance(c['valore'])})
        if 'domande' in e:
            text = {'goal': e['obiettivo'], 'start': e['parametri_iniziali'], 'steps': e['passi'],
                    'questions': e['domande'], 'deliver': e['consegna'], 'limits': e['limiti']}
        else:  # quaderno con previsione, tabella da compilare, domanda e limite (M06)
            text = {'goal': e['obiettivo'], 'start': e['parametri'], 'steps': e['passi'],
                    'questions': [e['previsione'], e['domanda']], 'table': e['tabella'], 'limits': e['limite']}
        cards.append({'n': n, 'id': lab, 'title': e['titolo'], **text, 'scenarios': scen, 'fields': fields,
                      'script': {'file': 'Esercizi/' + script[0].name,
                                 'code': script[0].read_text(encoding='utf-8').rstrip('\n')}})
    return {'title': book['titolo'], 'subtitle': book['sottotitolo'], 'common': book.get('istruzioni_comuni', []),
            'cards': cards}


# ---------------------------------------------------------------- principale
def region_text(pdf, page, rect):
    x, y, w, h = rect
    t = subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-x', str(x), '-y', str(y), '-W', str(w),
                        '-H', str(h), str(pdf), '-'], capture_output=True, text=True, check=True).stdout
    return re.sub(r'\s+', ' ', t.replace('-\n', '')).strip()


def fragment_hashes(lesson, src):
    """Impronta di ciò da cui dipende un frammento: file del progetto, preludio, dipendenze e codice.
    L'uscita registrata in webR vale come riferimento finché l'impronta resta la stessa."""
    p = lesson['project']
    h = hashlib.sha256(p.get('setup', 'setup.R').encode())
    for f in sorted(p['files']):
        h.update(f.encode() + b'\0' + (src / f).read_bytes())
    base = h.hexdigest()
    return {f: hashlib.sha256(json.dumps([base] + [lesson['code'][d]['code'] for d in c['deps']] + [c['code']])
                              .encode()).hexdigest()[:20] for f, c in lesson['code'].items()}


def author_log(src, cfg, f):
    """Uscita di un frammento nel registro di esecuzione dell'autore, se esiste."""
    log = src / cfg.get('log', 'Verifiche/esecuzione_frammenti_slide.log')
    if not log.is_file():
        return None
    text = log.read_text(encoding='utf-8')
    m = re.search(r'^stdout SLIDE %s\n(.*?)(?=^stdout SLIDE |\Z)' % f[:3], text, re.S | re.M)
    if not m:
        return None
    lines = [re.sub(r'^stdout ?', '', l) for l in m.group(1).splitlines() if l.startswith('stdout')]
    return '\n'.join(lines).strip('\n')


def browser_run(src, work, cfg):
    """Esegue i frammenti con i soli pacchetti R del sito (libreria temporanea di collegamenti)."""
    lock = json.loads((ROOT / 'vendor/r-packages-lock.json').read_text(encoding='utf-8'))
    lib = work / 'webr-lib'
    lib.mkdir()
    for p in lock:
        for base in ('/usr/local/lib/R/site-library', '/usr/lib/R/site-library'):
            if Path(base, p['package']).is_dir():
                (lib / p['package']).symlink_to(Path(base, p['package']))
                break
    standalone = cfg.get('standalone', False)
    subprocess.run(['Rscript', str(ROOT / 'scripts/lessons/run_slides.R'), str(src), str(work / 'browser.json'),
                    '' if standalone else cfg.get('setup', 'setup.R')], check=True,
                   env={'LC_ALL': 'C.UTF-8', 'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME'], 'GEOSTAT_ROOT': str(ROOT),
                        'GEOSTAT_BROWSER': '1', 'R_LIBS_SITE': str(lib), 'R_LIBS_USER': str(work / 'nessuna'),
                        'GEOSTAT_STANDALONE': '1' if standalone else ''})
    return json.loads((work / 'browser.json').read_text(encoding='utf-8'))


def project_files(src, cfg):
    """File da scrivere nel file system di webR: testo come stringa, binari in base64."""
    import base64
    out = {}
    for pattern in cfg['project']['files']:
        for p in sorted(src.glob(pattern)):
            if not p.is_file():
                continue
            rel = p.relative_to(src).as_posix()
            data = p.read_bytes()
            try:
                out[rel] = data.decode('utf-8')
            except UnicodeDecodeError:
                out[rel] = {'b64': base64.b64encode(data).decode('ascii')}
    return out


def footer_items(slides, src, acts):
    """Piè di pagina di T00 e M13-M16: il laboratorio entra nel pannello dei laboratori con i parametri dello
    scenario della slide (A nella pagina dello scenario, B in quella del confronto); lo script R6 dei materiali
    diventa un rimando in fondo alla colonna destra."""
    for s in slides:
        for link in s.pop('footer', []):
            m = re.fullmatch(r'#laboratorio/([a-z0-9-]+)', link['h'])
            if not m:
                s['items'].append({'t': 'small', 'c': [{'t': 'a', 'h': link['h'], 'c': link['c']}], 'col': 'R'})
                continue
            lab = m.group(1)
            labels = ' '.join(text_of(it['c']) for it in s['items'] if it['t'] == 'label')
            scenario = 0 if 'Scenario A' in labels else 1 if 'Confronto' in labels else None
            params = {}
            exp = src / 'Esperimenti' / (lab + '.json')
            if scenario is not None and exp.is_file():
                params = dict(json.loads(exp.read_text(encoding='utf-8'))[scenario]['params'])
            try:
                s.setdefault('labs', []).append(lab_link(acts, lab, params))
            except ValueError as e:
                warn('slide %d: %s' % (s['page'], e))
                s.setdefault('labs', []).append(lab_link(acts, lab, {}))


def python_runs(src, files, work):
    """Uscita registrata degli esempi Python (T00): stdout dello script eseguito nella cartella della lezione."""
    out = {}
    if not files:
        return out
    copy = work / 'python'
    shutil.copytree(src, copy)
    for f in files:
        r = subprocess.run(['python3', '-I', str(copy / 'Codice' / f)], cwd=copy, capture_output=True, text=True,
                           timeout=120)
        if r.returncode:
            warn('errore nello script Python %s: %s' % (f, r.stderr.strip().splitlines()[-1][:160]))
        out[f] = {'output': (r.stdout + r.stderr).rstrip('\n'), 'status': 'ok' if not r.returncode else 'error',
                  'deps': [], 'needs': ['Python 3']}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson')
    ap.add_argument('--no-r', action='store_true')
    o = ap.parse_args()
    cfg = json.loads((ROOT / 'lezioni/lezioni.json').read_text(encoding='utf-8'))[o.lesson]
    src = ROOT / cfg['source']
    pdf = src / cfg['pdf']
    tex, slides = parse_tex(src / cfg['tex'])
    pages = pdf_pages(pdf)
    if [s['page'] for s in slides] != list(range(1, pages + 1)):
        raise ValueError('il sorgente non descrive tutte le %d pagine del PDF' % pages)
    custom_pages(slides, cfg['title'])
    # Riquadri assenti nel sorgente ma presenti nel PDF distribuito: trascrizione dichiarata o ritaglio.
    for page, snippet in cfg.get('fromPdf', {}).items():
        s = slides[int(page) - 1]
        if s['items']:
            raise ValueError('la slide %s ha già un contenuto nel sorgente' % page)
        s['items'] = boxes(snippet, s['page'])
        for it in s['items']:
            if it['t'] in ('p', 'small', 'info', 'label') and norm(text_of(it['c'])[:30]) not in norm(
                    pdf_text(pdf, s['page'])):
                raise ValueError('testo trascritto assente nel PDF a pagina %s' % page)
    for s in slides:
        if 'lines' not in s and 'question' not in s and not s['items']:
            rect = cfg.get('fromPdfFigures', {}).get(str(s['page']), [25, 58, 516, 236])
            warn('slide %d senza riquadri nel sorgente: corpo della pagina ritagliato dal PDF' % s['page'])
            s['items'] = [{'t': 'figure', 'col': 'W', 'box': 18.1, 'fig': '%03d-1' % s['page'],
                           'alt': region_text(pdf, s['page'], rect)}]
    for s in slides:
        plain_title = re.sub(r'\\[A-Za-z]+|[{}^_]', '', s['title'])
        if s['page'] > 1 and norm(plain_title[:40]) not in norm(pdf_text(pdf, s['page'])):
            raise ValueError('titolo della slide %d assente nel PDF: %s' % (s['page'], s['title']))
    acts = lab_catalogue()
    prefix = o.lesson.lower() + '-'
    standalone = cfg.get('standalone', False)
    used = [it['file'] for s in slides for it in s['items'] if it['t'] == 'code']
    if standalone:
        # Script autonomi per capitolo: si pubblicano quelli citati dalle slide, R e Python.
        files = sorted(set(used))
        footer_items(slides, src, acts)
    else:
        for s in slides:
            s.pop('footer', None)
        files = sorted((p.name for p in (src / 'Codice').iterdir() if CODE.match(p.name)),
                       key=lambda f: (int(CODE.match(f).group(1)), f))
    missing = sorted(set(used) - set(files))
    if missing:
        raise ValueError('file di codice citati ma assenti: %s' % missing)
    for f in sorted(set(files) - set(used)):
        page = int(CODE.match(f).group(1))
        if page <= pages:
            # Codice della slide che il sorgente non cita (per esempio la slide 3 ritagliata dal PDF).
            slides[page - 1].setdefault('code', []).append({'t': 'code', 'title': 'Codice della slide', 'file': f})
        else:
            warn('file di codice senza slide corrispondente: %s' % f)
    for s in slides:
        for it in s['items']:
            if it['t'] == 'code' and not standalone and int(CODE.match(it['file']).group(1)) != s['page']:
                warn('il file %s è citato nella slide %d' % (it['file'], s['page']))
    colour = re.search(r'\\definecolor\{Classical\}\{HTML\}\{([0-9A-Fa-f]{6})\}', tex)
    with tempfile.TemporaryDirectory() as t:
        work = Path(t)
        out_json = ROOT / 'content/lezioni' / (o.lesson + '.json')
        old = json.loads(out_json.read_text(encoding='utf-8')) if out_json.exists() else {}
        if o.no_r:
            runs = {f: {k: old['code'][f].get(k, []) for k in ('output', 'deps', 'needs')} for f in files}
            r_version = old['reference'].get('native', old['reference']['R'])
            prelude_needs = old['project'].get('needs', [])
        else:
            subprocess.run(['Rscript', str(ROOT / 'scripts/lessons/run_slides.R'), str(src), str(work / 'run.json'),
                            '' if standalone else cfg.get('setup', 'setup.R')],
                           check=True, env={'LC_ALL': 'C.UTF-8', 'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME'],
                                            'GEOSTAT_ROOT': str(ROOT), 'GEOSTAT_STANDALONE': '1' if standalone else ''})
            run = json.loads((work / 'run.json').read_text(encoding='utf-8'))
            if standalone:
                run['files'] = {f: v for f, v in run['files'].items() if f in files}
                run['files'].update(python_runs(src, [f for f in files if f.endswith('.py')], work))
            logged = 0
            for f in run['files']:
                out = author_log(src, cfg, f)
                if out is not None:
                    # Il registro dell'autore è stato prodotto con l'R del sito (webR): vale come uscita attesa.
                    run['files'][f].update(output=out, status='ok')
                    logged += 1
            if logged:
                r_log = (src / 'Verifiche/SESSIONE_R.txt')
                m = re.search(r'R version [^\n]*', r_log.read_text(encoding='utf-8')) if r_log.is_file() else None
                run['meta']['R'] = (m.group(0) if m else 'R del sito') + ', registro di esecuzione della lezione'
            for f, v in run['files'].items():
                if v['status'] != 'ok':
                    warn('errore nel frammento %s: %s' % (f, v['output'].splitlines()[-1][:160]))
            runs = run['files']
            r_version = run['meta']['R']
            prelude_needs = run['meta']['prelude_needs']
            if prelude_needs or any(v.get('needs') for f, v in runs.items() if f.endswith('.R')):
                for f, ok in browser_run(src, work, cfg).items():
                    if f not in runs:
                        continue
                    if ok != 'ok' and runs[f]['status'] == 'ok' and not runs[f].get('needs'):
                        runs[f]['needs'] = prelude_needs or ['pacchetti esterni']
        # Uscite registrate in webR (scripts/lessons/verify_webr.py): sono quelle che lo studente vede
        # eseguendo il codice nel sito, quindi prevalgono dove il frammento gira in webR.
        reference = {'R': r_version, 'note': 'Uscite registrate eseguendo il codice delle slide in ordine.'}
        webr_file = ROOT / 'lezioni/webr' / (o.lesson + '.json')
        if webr_file.is_file():
            webr = json.loads(webr_file.read_text(encoding='utf-8'))
            probe = {'project': {'setup': cfg.get('setup', 'setup.R'), 'files': sorted(project_files(src, cfg))},
                     'code': {f: {'code': (src / 'Codice' / f).read_text(encoding='utf-8').rstrip('\n'),
                                  'deps': runs[f]['deps']} for f in files}}
            hashes, used = fragment_hashes(probe, src), 0
            for f in files:
                w = webr['fragments'].get(f)
                if not w or 'skipped' in w or runs[f].get('needs'):
                    continue
                if w.get('hash') != hashes[f]:
                    warn('uscita webR da rigenerare per %s (codice, dipendenze o dati cambiati)' % f)
                elif w['status'] != runs[f].get('status', 'ok'):
                    warn('in webR il frammento %s termina con stato %s' % (f, w['status']))
                else:
                    runs[f]['output'] = w['output']
                    used += 1
            if used:
                local = sum(1 for f in files if runs[f].get('needs'))
                reference = {'R': webr['R'] + ', webR nel browser', 'native': r_version,
                             'note': 'Uscite registrate eseguendo il codice delle slide in ordine nel browser.' + (
                                 ' I %d frammenti che richiedono pacchetti assenti in webR riportano '
                                 "l'uscita di %s." % (local, r_version) if local else '')}
        code = {}
        for f in files:
            text = (src / 'Codice' / f).read_text(encoding='utf-8').rstrip('\n')
            code[f] = {'code': text, 'output': runs[f]['output'], 'deps': runs[f]['deps']}
            if runs[f].get('needs'):
                code[f]['needs'] = runs[f]['needs']
            if standalone:
                code[f]['page'] = min(s['page'] for s in slides for it in s['items']
                                      if it['t'] == 'code' and it['file'] == f)
            if f.endswith('.py'):
                code[f]['lang'] = 'python'
        for s in slides:
            labs = []
            for it in s['items']:
                if it['t'] == 'code':
                    labs += labs_in_code(code[it['file']]['code'], acts, prefix)
                if it['t'] == 'lab':
                    m = re.search(r'#laboratorio/([a-z0-9-]+)', it['url'])
                    if m and m.group(1) in acts:
                        it['lab'] = m.group(1)
                    else:
                        warn('collegamento di laboratorio non riconosciuto nella slide %d: %s' % (s['page'], it['url']))
            if labs:
                s['labs'] = labs
        project = cfg['project']
        lesson = {
            'id': o.lesson, 'title': cfg['title'], 'planet': cfg['planet'], 'world': cfg['world'],
            'exercisesWorld': cfg.get('exercisesWorld'), 'pages': pages,
            'pdf': 'assets/lezioni/%s/%s' % (o.lesson, cfg['pdf']),
            'project': {'dir': project['dir'], 'files': sorted(project_files(src, cfg))},
            'reference': reference,
            'sections': [], 'slides': slides, 'code': code,
        }
        if not standalone:
            lesson['project']['setup'] = cfg.get('setup', 'setup.R')
        if prelude_needs:
            lesson['project']['needs'] = prelude_needs
        # Rimandi fra slide: la tappa corrispondente della lezione.
        def tappe(nodes):
            for n in nodes:
                if isinstance(n, dict):
                    if n['t'] == 'a' and n['h'].startswith('#tappa-'):
                        n['h'] = '#lezione-%s/%s' % (o.lesson, n['h'][len('#tappa-'):])
                    tappe(n.get('c', []))
        for s in slides:
            tappe(s.get('recall', []))
            for it in s['items']:
                tappe(it.get('c', []))
                for row in it.get('head', []) + it.get('rows', []):
                    for cell in row:
                        tappe(cell['c'])
        if cfg.get('workbookPdf'):
            lesson['workbook'] = 'assets/lezioni/%s/%s' % (o.lesson, cfg['workbookPdf'])
        for s in slides:
            if not lesson['sections'] or lesson['sections'][-1]['title'] != s['section']:
                lesson['sections'].append({'title': s['section'], 'first': s['page'], 'last': s['page']})
            lesson['sections'][-1]['last'] = s['page']
        assets = ROOT / 'assets/lezioni' / o.lesson
        assets.mkdir(parents=True, exist_ok=True)
        stamp_pdf(pdf, assets / cfg['pdf'], o.lesson, cfg['planet'], pages, work,
                  colour.group(1).upper() if colour else '087C74')
        if cfg.get('workbookPdf'):
            shutil.copyfile(src / cfg['workbookPdf'], assets / cfg['workbookPdf'])
        lesson['download'] = 'assets/lezioni/%s/%s' % (o.lesson, cfg['zip']['name'])
        project_zip(src, assets / cfg['zip']['name'], cfg)
        nfig = figures(tex, slides, cfg, src, pdf, assets / 'figure', o.lesson, work)
        # La copertina è ricomposta come testo del pannello: nessuna immagine della pagina.
        for old in assets.glob('[0-9][0-9][0-9].*'):
            old.unlink()
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(lesson, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        ncards = 0
        ex_json = ROOT / 'content/esercizi' / (o.lesson + '.json')
        if cfg.get('workbook'):
            ex = exercises(cfg, src, acts, work, prefix)
            ex.update(lesson=o.lesson, world=cfg['exercisesWorld'], planet=cfg['planet'])
            ex_json.parent.mkdir(parents=True, exist_ok=True)
            ex_json.write_text(json.dumps(ex, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            ncards = len(ex['cards'])
    print('%s: %d slide, %d sezioni, %d figure, %d file di codice, %d esercizi, %d avvisi' % (
        o.lesson, pages, len(lesson['sections']), nfig, len(code), ncards, len(WARNINGS)))


if __name__ == '__main__':
    sys.exit(main())
