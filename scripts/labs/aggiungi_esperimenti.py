"""Aggiunge o aggiorna esperimenti del catalogo pubblicato (content/experiments.json) a partire da una specifica.

Uso: python3 -I scripts/labs/aggiungi_esperimenti.py content/esperimenti/<file>.json [...]
La specifica elenca le attività con i campi del catalogo; il codice viene formattato con deparse() di R, una
riga vuota fra le istruzioni di primo livello come nel catalogo esistente. Lo script scrive R/experiments/<id>.R,
aggiorna attività e copertura in content/experiments.json e content/experiments-draft.json e la fonte
editoriale (testo, simboli, limiti) in content/prose-estensioni.json. Il resto del
catalogo resta invariato byte per byte.

Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAMPI = ['id', 'module', 'section', 'sectionTitle', 'page', 'title', 'goal', 'action', 'conclusion', 'formula',
         'controls', 'prose', 'limits', 'presets', 'source', 'code', 'symbols']
SEME = {'key': 'seed', 'label': 'Seme casuale', 'type': 'number', 'value': 17, 'min': 1, 'max': 99999, 'step': 1,
        'help': 'A parità di ambiente R, il seme permette di ricostruire la simulazione.'}
FORMATO = r'''
args <- commandArgs(TRUE)
src <- readLines(args[1], warn = FALSE, encoding = 'UTF-8')
ex <- parse(text = src, keep.source = FALSE)
out <- vapply(ex, function(e) paste(deparse(e, width.cutoff = 100L), collapse = '\n'), '')
writeLines(paste(out, collapse = '\n\n'), args[2], useBytes = TRUE)
'''


def formatta(codice):
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / 'f.R').write_text(FORMATO)
        (t / 'in.R').write_text(codice)
        subprocess.run(['Rscript', str(t / 'f.R'), str(t / 'in.R'), str(t / 'out.R')], check=True,
                       env={'LC_ALL': 'C.UTF-8', 'PATH': '/usr/local/bin:/usr/bin:/bin'})
        return (t / 'out.R').read_text().rstrip('\n')


def valore_r(v):
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, int) or (isinstance(v, float) and v.is_integer()):
        return str(int(v)) + 'L'
    return repr(v)


def script(a):
    comune = (ROOT / 'R/lab-common.R').read_text()
    p = 'p <- list(' + ', '.join(c['key'] + ' = ' + valore_r(c['value']) for c in a['controls']) + ')'
    testa = ('# GeoStat Lab · ' + a['title'] + '\n# ' + a['goal'] + '\n# Dati sintetici; parametri e ambiente '
             'dichiarati.\n# Dipendenze: install.packages(c("ggplot2", "jsonlite", "svglite"))\n# Codice: PolyForm '
             'Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0\n# Required Notice: '
             'Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)\n\n')
    coda = ('\n\nprint(metrics, row.names = FALSE)\nif (!interactive()) grDevices::cairo_pdf("figure_esperimento.pdf", '
            'width=9, height=5.5)\nfor (g in plots) print(g)\nif (!interactive()) grDevices::dev.off()\n'
            '# write.csv(data, "dati_esperimento.csv", row.names = FALSE)\n'
            '# ggsave("figura.svg", plots[[1]], width = 9, height = 5.5)\n\n')
    return testa + comune + '\n' + p + '\nset.seed(p$seed)\n\n' + a['code'] + coda


def main(files):
    cat_path, draft_path = ROOT / 'content/experiments.json', ROOT / 'content/experiments-draft.json'
    cat = json.loads(cat_path.read_text())
    draft = json.loads(draft_path.read_text())
    prosa_path = ROOT / 'content/prose-estensioni.json'
    prosa = json.loads(prosa_path.read_text()) if prosa_path.exists() else {}
    for f in files:
        for spec in json.loads(Path(f).read_text()):
            a = dict(spec)
            a['controls'] = a['controls'] + [SEME]
            a.setdefault('presets', [])
            a['source'] = 'R/experiments/' + a['id'] + '.R'
            a['code'] = formatta(a['code'])
            a = {k: a[k] for k in CAMPI}
            (ROOT / a['source']).write_text(script(a))
            for lista in (cat['activities'], draft):
                i = next((k for k, b in enumerate(lista) if b['id'] == a['id']), None)
                if i is None:
                    lista.append(a)
                else:
                    lista[i] = a
            cov = next((c for c in cat['coverage'] if c['module'] == a['module'] and c['section'] == a['section']), None)
            if cov is None:
                cat['coverage'].append({'module': a['module'], 'section': a['section'], 'title': a['sectionTitle'],
                                        'role': 'esperimento', 'activities': [a['id']]})
            elif a['id'] not in cov['activities']:
                cov['activities'].append(a['id'])
            prosa[a['id']] = {k: a[k] for k in ('prose', 'symbols', 'limits')}
            print('Esperimento', a['id'], '->', a['source'])
    ids = [a['id'] for a in cat['activities']]
    assert len(ids) == len(set(ids)), 'identificativi ripetuti'
    assert len({a['limits'] for a in cat['activities']}) == len(ids), 'limiti ripetuti'
    cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + '\n')
    draft_path.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + '\n')
    prosa_path.write_text(json.dumps(prosa, ensure_ascii=False, indent=2) + '\n')
    print(len(ids), 'attività nel catalogo')


if __name__ == '__main__':
    main(sys.argv[1:])
