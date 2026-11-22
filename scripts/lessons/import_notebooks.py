#!/usr/bin/env python3
"""GeoStat Lab: importa i notebook svolti M01-M12 nei pianeti compagni.

Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)

Uso dalla radice del repository:
    python3 -I scripts/lessons/import_notebooks.py

Legge lezioni/Notebook_M01-M12/INDICE_NOTEBOOK.csv e produce content/notebook.json, con titolo, numero di
blocchi e di grafici e le tappe che rimandano a ciascun notebook (i piè di pagina di M10-M12), e un archivio
per modulo con i sorgenti Rmd, le funzioni comuni e i dati (assets/lezioni/<ID>/<pianeta>_<ID>_notebook.zip).
Le pagine HTML dei notebook, autosufficienti e prive di script, e i file che citano sono copiati dalla
compilazione del sito in notebook/, con la stessa struttura di cartelle.
"""
import csv
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'lezioni/Notebook_M01-M12'
# Contenuti attivi o risorse caricate da altri siti: una pagina che li contiene non viene pubblicata.
# I collegamenti ordinari a pagine esterne restano ammessi.
ACTIVE = re.compile(r'<script|<iframe|<object|<embed|<link\b|<form|\bon[a-z]+\s*=|'
                    r'\bsrc\s*=\s*["\']?(?:https?:|//)|href\s*=\s*["\']?javascript:', re.I)


def deck_pages(cfg, lid):
    """Tappe che citano un notebook nel piè di pagina della slide."""
    tex = (ROOT / cfg['source'] / cfg['tex']).read_text(encoding='utf-8')
    body = tex[tex.index(r'\begin{document}'):]
    pages = {}
    for fm in re.finditer(r'\\begin\{frame\}(?:\[[^\]]*\])?(.*?)\\end\{frame\}', body, re.S):
        page = int(re.search(r'\\hypertarget\{slide(\d+)\}', fm.group(1)).group(1))
        for nb in set(re.findall(r'03_Notebook_svolti/%s_[A-Za-z]+/(%s_N\d{2})\.html' % (lid, lid), fm.group(1))):
            pages.setdefault(nb, []).append(page)
    return pages


def archive(out, rows, folder, planet, lid, shared):
    """Sorgenti Rmd del modulo con funzioni comuni e dati; date fisse e ordine stabile."""
    root = '%s_%s_notebook' % (planet, lid)
    base = SRC / folder
    files = [(SRC / r['rmd'], r['rmd'].split('/', 1)[1]) for r in rows]
    if shared:  # M01-M09: progetto comune alla radice della raccolta
        files += [(p, p.relative_to(SRC).as_posix()) for p in sorted(SRC.glob('R/*')) + sorted(SRC.glob('Dati/*'))]
        files.append((SRC / 'GeoStat_Lab_Notebooks.Rproj', 'GeoStat_Lab_Notebooks.Rproj'))
        files = [(p, n if n.startswith(('R/', 'Dati/', 'GeoStat')) else folder + '/' + n) for p, n in files]
    else:  # M10-M12: progetto autonomo nella cartella del modulo
        for pattern in ('R/*', 'Dati/**/*', '*.Rproj', 'README.md', 'INDICE_NOTEBOOK.csv'):
            files += [(p, p.relative_to(base).as_posix()) for p in sorted(base.glob(pattern)) if p.is_file()]
    readme = ('Notebook svolti di %s (%s).\n\nAprire GeoStat_Lab_Notebooks.Rproj in RStudio e lavorare i notebook '
              "nell'ordine; ogni notebook scrive i propri file in Risultati/.\n\nTappe e notebook: "
              'https://marzione00.github.io/Lab_Geo/#esercizi-%s\nMateriali CC BY-NC-SA 4.0; codice PolyForm '
              'Noncommercial 1.0.0.\n') % (planet, lid, lid)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        def add(name, data):
            info = zipfile.ZipInfo(root + '/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
        add('LEGGIMI.txt', readme.encode('utf-8'))
        for f in ('LICENSE.md', 'LICENSE-CODE.md'):
            add(f, (ROOT / f).read_bytes())
        for p, name in sorted(set(files), key=lambda x: x[1]):
            add(name, p.read_bytes())


def main():
    config = json.loads((ROOT / 'lezioni/lezioni.json').read_text(encoding='utf-8'))
    with open(SRC / 'INDICE_NOTEBOOK.csv', encoding='utf-8-sig') as fh:
        rows = list(csv.DictReader(fh))
    out = {}
    for lid in sorted({r['modulo'] for r in rows}):
        cfg = config[lid]
        mine = [r for r in rows if r['modulo'] == lid]
        if any(r['pianeta'] != cfg['planet'] for r in mine):
            raise ValueError('pianeta dei notebook diverso dalla lezione %s' % lid)
        pages = deck_pages(cfg, lid)
        items = []
        for r in mine:
            html = (SRC / r['html']).read_text(encoding='utf-8')
            if ACTIVE.search(html):
                raise ValueError('contenuto attivo o risorsa esterna in %s' % r['html'])
            if not (SRC / r['rmd']).is_file():
                raise ValueError('sorgente assente: ' + r['rmd'])
            items.append({'id': r['id'], 'title': r['titolo'], 'html': 'notebook/' + r['html'],
                          'blocks': int(r['blocchi_eseguiti']), 'figures': int(r['grafici']),
                          'pages': sorted(pages.get(r['id'], []))})
        unknown = set(pages) - {i['id'] for i in items}
        if unknown:
            raise ValueError('la lezione %s cita notebook assenti: %s' % (lid, sorted(unknown)))
        folder = mine[0]['html'].split('/')[0]
        zname = '%s_%s_notebook.zip' % (cfg['planet'], lid)
        (ROOT / 'assets/lezioni' / lid).mkdir(parents=True, exist_ok=True)
        archive(ROOT / 'assets/lezioni' / lid / zname, mine, folder, cfg['planet'], lid,
                shared=not (SRC / folder / 'GeoStat_Lab_Notebooks.Rproj').is_file())
        out[lid] = {'download': 'assets/lezioni/%s/%s' % (lid, zname), 'notebooks': items}
        print('%s: %d notebook, %d citati dalle tappe' % (lid, len(items), sum(1 for i in items if i['pages'])))
    (ROOT / 'content/notebook.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n',
                                                encoding='utf-8')


if __name__ == '__main__':
    sys.exit(main())
