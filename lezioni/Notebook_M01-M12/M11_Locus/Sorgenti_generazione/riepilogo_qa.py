"""Riepilogo dei registri esistenti, da aggiornare dopo verifica_html.py.

Non esegue analisi R e non sostituisce la revisione visiva documentata.
"""
from pathlib import Path
import csv, json

BASE = Path(__file__).resolve().parent.parent
v = BASE / 'Verifiche'
notebook = json.loads((v / 'esecuzione_notebook.json').read_text())
html = json.loads((v / 'audit_html_offline.json').read_text())
provenienza = json.loads((v / 'audit_provenienza_finale.json').read_text())
geo = list(csv.DictReader((BASE / 'Risultati/M11_N20/audit_geometria_GeoJSON.csv').open()))
errors = html['errori']
pending_pdf = [e for e in errors if len(e) == 3 and e[1] == 'missing file'
               and e[2].startswith('../../02_PDF/M11_Locus/Locus_M11_statistica_spaziale.pdf')]
other_errors = [e for e in errors if e not in pending_pdf]
summary = {
    'modulo': 'M11 Locus',
    'stato': 'ERRORE' if other_errors else ('IN_ATTESA_PDF' if pending_pdf else 'OK'),
    'notebook_Rmd': len(notebook),
    'notebook_HTML': len(notebook),
    'pagine_HTML_totali': len(html['controlli']),
    'blocchi_R_eseguiti': sum(n['blocchi_eseguiti'] for n in notebook),
    'figure_R': sum(n['grafici'] for n in notebook),
    'errori_R_non_gestiti': sum(n['errori'] for n in notebook),
    'avvisi_R': sum(n['avvisi'] for n in notebook),
    'runtime': notebook[0]['R_version'] + ' / ' + notebook[0]['runtime'],
    'sf': {'versione_packageVersion': '1.1.3', 'GEOS': '3.11.2',
           'GDAL': '3.8.1', 'PROJ': '9.2.0',
           'funzioni_eseguite': ['st_as_sf', 'st_transform', 'st_set_crs', 'st_write', 'st_read'],
           'GeoJSON_coordinate_precision': 10,
           'GeoJSON_scarto_massimo_gradi': max(float(r['massimo_scarto_gradi']) for r in geo)},
    'provenienza_git': {'commit': provenienza['commit'],
                       'file_verificati': len(provenienza['files']),
                       'originali_R': 20, 'dataset_CSV': 2,
                       'algoritmi': ['SHA-256', 'Git blob SHA-1'],
                       'esito': 'OK'},
    'offline': {'immagini_incorporate': sum(n['images'] for n in html['controlli']),
                'formule_MathML': sum(n['mathml'] for n in html['controlli']),
                'errori_oltre_PDF_pendente': other_errors,
                'collegamenti_in_attesa_PDF': len(pending_pdf),
                'PDF': '../../02_PDF/M11_Locus/Locus_M11_statistica_spaziale.pdf'},
    'verifica_visiva': {'figure_R_ispezionate': 20,
                       'ritocchi_riverificati': ['N01 etichette superiori', 'N05 assi UTM',
                                                'N15 numerosità delle classi'],
                       'anteprime_layout': ['index', 'M11_N05', 'M11_N13', 'M11_N20'],
                       'metodo_layout': 'Primo foglio temporaneo WeasyPrint 70, media screen, 1400 x 1000 px; ispezione PNG.',
                       'limite': 'Il controllo layout non è una prova nel browser; WeasyPrint non convalida il rendering MathML. Nessun PDF temporaneo è distribuito come notebook.',
                       'documentazione': 'QA/NOTE_QA.md'},
    'errore_didattico_gestito': 'N06 cattura intenzionalmente la trasformazione senza CRS; non è un errore di esecuzione non gestito.'
}
(v / 'RIEPILOGO_QA.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
print(summary['stato'], ':', summary['notebook_Rmd'], 'notebook,',
      summary['blocchi_R_eseguiti'], 'blocchi,', len(pending_pdf), 'link PDF pendenti,',
      len(other_errors), 'altri errori.')
