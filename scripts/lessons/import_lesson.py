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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = 'https://marzione00.github.io/Lab_Geo/'


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
    r'\%': '%', r'\&': '&', r'\#': '#', r'\_': '_', r'\{': '{', r'\}': '}', r'\ldots': '…',
    r'\textcopyright{}': '©', r'\,': '\u202f', r'\ ': ' ', r'\-': '',
}


def plain(t):
    for k, v in SIMPLE.items():
        t = t.replace(k, v)
    t = t.replace('---', '—').replace('--', '–').replace('~', '\u00a0')
    t = re.sub(r'\\\\(\[[^\]]*\])?', ' ', t)
    return t


def inline(tex):
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
        m = re.match(r'\\(texttt|textbf|emph|textit|href|mbox|text|textsc|MakeUppercase)\b', tex[i:])
        if m:
            name = m.group(1)
            flush()
            j = i + len(m.group(0))
            if name == 'href':
                (url, label), j = args(tex, j, 2)
                nodes.append({'t': 'a', 'h': url.replace(r'\#', '#'), 'c': inline(label)})
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


ITEM = re.compile(r'\\(PLabel|PBody|PSmall|PInfo|PCode|PLab)\{|\\\[|\\begin\{tikzpicture\}')


def items(chunk):
    out, i = [], 0
    while True:
        m = ITEM.search(chunk, i)
        if not m:
            return out
        tok = m.group(0)
        if tok == r'\[':
            j = chunk.index(r'\]', m.end())
            out.append({'t': 'math', 'v': re.sub(r'\s+', ' ', chunk[m.end():j]).strip()})
            i = j + 2
        elif tok.startswith(r'\begin{tikz'):
            j = chunk.index(r'\end{tikzpicture}', m.end())
            if not out or out[-1]['t'] != 'figure':
                out.append({'t': 'figure'})
            i = j
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
            s.update(title=text_of(inline(title)), section=text_of(inline(section)), recall=inline(recall))
            s['items'] = items(pre)
        else:
            s['items'] = []
            s['custom'] = frame
        slides.append(s)
    return tex, slides


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


def stamp_pdf(src_pdf, out_pdf, lesson_id, planet, pages, workdir):
    """Sovrappone a ogni pagina, dalla terza, il codice di tappa con il collegamento al sito."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, FloatObject, NameObject, NumberObject, TextStringObject
    w, h = 566.93, 354.33
    tex = [r'\documentclass{article}', r'\usepackage[paperwidth=566.93bp,paperheight=354.33bp,margin=0pt]{geometry}',
           r'\usepackage{fontspec}\setmainfont{Nimbus Sans}', r'\usepackage{xcolor}',
           r'\definecolor{Classical}{HTML}{087C74}', r'\pagestyle{empty}\usepackage{tikz}', r'\begin{document}']
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


def images(pdf, outdir, pages):
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob('*.svg'):
        old.unlink()
    for p in range(2, pages + 1):
        subprocess.run(['pdftocairo', '-svg', '-f', str(p), '-l', str(p), str(pdf), str(outdir / ('%03d.svg' % p))],
                       check=True)
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['pdftocairo', '-png', '-r', '216', '-f', '1', '-l', '1', '-singlefile', str(pdf),
                        str(Path(t) / 'cover')], check=True)
        from PIL import Image
        Image.open(Path(t) / 'cover.png').convert('RGB').save(outdir / '001.webp', quality=84, method=6)


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
        out.append(lab_link(acts, prefix + m.group(1), params))
    return out


# ---------------------------------------------------------------- esercizi
def tolerance(v):
    if float(v).is_integer():
        return 0
    from math import floor, log10
    return 0.5 * 10 ** (floor(log10(abs(v))) - 2)


def exercises(cfg, src, acts, workdir):
    checks_file = workdir / 'checks.json'
    subprocess.run(['Rscript', str(ROOT / 'scripts/lessons/exercise_checks.R'), str(ROOT), str(src),
                    str(src / cfg['workbook']), str(src / cfg['expected']), str(checks_file)],
                   check=True, env={'LC_ALL': 'C.UTF-8', 'PATH': '/usr/bin:/bin'})
    checks = json.loads(checks_file.read_text(encoding='utf-8'))
    book = json.loads((src / cfg['workbook']).read_text(encoding='utf-8'))
    cards = []
    for n, e in enumerate(book['esercizi'], 1):
        ck = checks[e['id']]
        labels = {}
        for c in ck['checks']:
            if c['scenario'] == 'A' and c['metrica']:
                # Il nome di quantile() resta attaccato all'etichetta («Percentile 2,5%.2.5%»): lo si toglie.
                labels[c['parametro']] = re.sub(r'\.\d+(?:\.\d+)?%$', '', c['metrica'])
        script = sorted((src / 'Esercizi').glob('%02d_*.R' % n))
        if len(script) != 1:
            raise ValueError('script dell\'esercizio %d non trovato' % n)
        scen = {}
        for name, sc in ck['scenarios'].items():
            scen[name] = {'link': lab_link(acts, e['id'], sc['params'] or {}), 'full': sc['full']}
        fields = []
        for c in ck['checks']:
            if c['parametro'] in cfg.get('echo', []) or not labels.get(c['parametro']):
                continue
            fields.append({'scenario': c['scenario'], 'key': c['parametro'], 'label': labels[c['parametro']],
                           'value': c['valore'], 'tol': tolerance(c['valore'])})
        cards.append({
            'n': n, 'id': e['id'], 'title': e['titolo'], 'goal': e['obiettivo'], 'start': e['parametri_iniziali'],
            'steps': e['passi'], 'questions': e['domande'], 'deliver': e['consegna'], 'limits': e['limiti'],
            'scenarios': scen, 'fields': fields,
            'script': {'file': 'Esercizi/' + script[0].name,
                       'code': script[0].read_text(encoding='utf-8').rstrip('\n')},
        })
    return {'title': book['titolo'], 'subtitle': book['sottotitolo'], 'common': book['istruzioni_comuni'],
            'cards': cards}


# ---------------------------------------------------------------- principale
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson')
    ap.add_argument('--no-images', action='store_true')
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
    # Riquadri assenti nel sorgente ma presenti nel PDF distribuito: trascrizione dichiarata.
    for page, snippet in cfg.get('fromPdf', {}).items():
        s = slides[int(page) - 1]
        if s['items']:
            raise ValueError('la slide %s ha già un contenuto nel sorgente' % page)
        s['items'] = items(snippet)
        s['transcribed'] = True
        for it in s['items']:
            if it['t'] in ('p', 'small', 'info', 'label') and norm(text_of(it['c'])[:30]) not in norm(
                    pdf_text(pdf, s['page'])):
                raise ValueError('testo trascritto assente nel PDF a pagina %s' % page)
    # Corrispondenza fra titoli del sorgente e testo del PDF distribuito.
    for s in slides:
        if s['page'] > 1 and norm(s['title'][:40]) not in norm(pdf_text(pdf, s['page'])):
            raise ValueError('titolo della slide %d assente nel PDF: %s' % (s['page'], s['title']))
    acts = lab_catalogue()
    prefix = o.lesson.lower() + '-'
    files = sorted(p.name for p in (src / 'Codice').glob('[0-9][0-9][0-9]_*.R'))
    used = [it['file'] for s in slides for it in s['items'] if it['t'] == 'code']
    if sorted(used) != files:
        raise ValueError('file di codice non citati o mancanti: %s' % sorted(set(files) ^ set(used)))
    for s in slides:
        for it in s['items']:
            if it['t'] == 'code' and int(it['file'][:3]) != s['page']:
                raise ValueError('il file %s non corrisponde alla slide %d' % (it['file'], s['page']))
    with tempfile.TemporaryDirectory() as t:
        work = Path(t)
        out_json = ROOT / 'content/lezioni' / (o.lesson + '.json')
        old = json.loads(out_json.read_text(encoding='utf-8')) if out_json.exists() else {}
        if o.no_r:
            runs = {f: {k: old['code'][f][k] for k in ('output', 'deps')} for f in files}
            r_version = old['reference']['R']
        else:
            subprocess.run(['Rscript', str(ROOT / 'scripts/lessons/run_slides.R'), str(src), str(work / 'run.json')],
                           check=True, env={'LC_ALL': 'C.UTF-8', 'PATH': '/usr/bin:/bin'})
            run = json.loads((work / 'run.json').read_text(encoding='utf-8'))
            if run['meta']['errors']:
                raise ValueError('errori nel codice delle slide: %s' % run['meta']['errors'])
            runs = run['files']
            r_version = run['meta']['R']
        code = {}
        for f in files:
            text = (src / 'Codice' / f).read_text(encoding='utf-8').rstrip('\n')
            code[f] = {'code': text, 'output': runs[f]['output'], 'deps': runs[f]['deps']}
        for s in slides:
            labs = []
            for it in s['items']:
                if it['t'] == 'code':
                    labs += labs_in_code(code[it['file']]['code'], acts, prefix)
                if it['t'] == 'lab':
                    m = re.search(r'#laboratorio/([a-z0-9-]+)', it['url'])
                    it['lab'] = lab_link(acts, m.group(1), {})['id']
            if labs:
                s['labs'] = labs
        project = cfg['project']
        lesson = {
            'id': o.lesson, 'title': cfg['title'], 'planet': cfg['planet'], 'world': cfg['world'],
            'exercisesWorld': cfg['exercisesWorld'], 'pages': pages,
            'pdf': 'assets/lezioni/%s/%s' % (o.lesson, cfg['pdf']),
            'workbook': 'assets/lezioni/%s/%s' % (o.lesson, cfg['workbookPdf']),
            'project': {'dir': project['dir'], 'files': project['files']},
            'reference': {'R': r_version, 'note': 'Uscite registrate eseguendo il codice delle slide in ordine.'},
            'sections': [], 'slides': slides, 'code': code,
        }
        for s in slides:
            if not lesson['sections'] or lesson['sections'][-1]['title'] != s['section']:
                lesson['sections'].append({'title': s['section'], 'first': s['page'], 'last': s['page']})
            lesson['sections'][-1]['last'] = s['page']
        assets = ROOT / 'assets/lezioni' / o.lesson
        assets.mkdir(parents=True, exist_ok=True)
        stamped = assets / cfg['pdf']
        stamp_pdf(pdf, stamped, o.lesson, cfg['planet'], pages, work)
        shutil.copyfile(src / cfg['workbookPdf'], assets / cfg['workbookPdf'])
        lesson['download'] = 'assets/lezioni/%s/%s' % (o.lesson, cfg['zip']['name'])
        project_zip(src, assets / cfg['zip']['name'], cfg)
        if not o.no_images:
            images(stamped, assets, pages)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(lesson, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        ex = exercises(cfg, src, acts, work)
        ex.update(lesson=o.lesson, world=cfg['exercisesWorld'], planet=cfg['planet'])
        ex_json = ROOT / 'content/esercizi' / (o.lesson + '.json')
        ex_json.parent.mkdir(parents=True, exist_ok=True)
        ex_json.write_text(json.dumps(ex, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('%s: %d slide, %d sezioni, %d file R, %d esercizi' % (
        o.lesson, pages, len(lesson['sections']), len(code), len(ex['cards'])))


if __name__ == '__main__':
    sys.exit(main())
