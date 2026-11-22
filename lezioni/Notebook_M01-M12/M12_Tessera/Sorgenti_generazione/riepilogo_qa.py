"""Riassume i registri effettivi; eseguire dopo verifica_html.py."""
from pathlib import Path
import csv,json

BASE=Path(__file__).resolve().parent.parent
V=BASE/'Verifiche'
records=json.loads((V/'esecuzione_notebook.json').read_text())
blocks=list(csv.DictReader((V/'esecuzione_blocchi.csv').open()))
offline=json.loads((V/'audit_html_offline.json').read_text())
sources=json.loads((V/'audit_provenienza_finale.json').read_text())
geo=json.loads((V/'audit_geotiff_indipendente.json').read_text())
audit=list(csv.DictReader((BASE/'Risultati/M12_N20/audit_consegna.csv').open()))
tags=list(csv.DictReader((BASE/'Risultati/M12_N20/audit_tag_NoData.csv').open()))
passed=(not offline['errori'] and all(r['esito']=='OK' for r in blocks)
        and all(r['esito']=='OK' for r in geo['controlli'])
        and all(r['esito']=='TRUE' for r in audit)
        and all(r['sentinel_meno9999']=='TRUE' for r in tags))
summary={
 'modulo':'M12 Tessera','stato':'OK' if passed else 'ERRORE',
 'notebook_Rmd':len(records),'notebook_HTML':len(records),
 'pagine_HTML_totali':len(offline['controlli']),
 'blocchi_R_eseguiti':len(blocks),'figure_R':sum(r['grafici'] for r in records),
 'errori_R':sum(r['errori'] for r in records),'avvisi_R':sum(r['avvisi'] for r in records),
 'messaggi_R':sum(int(r['messaggi']) for r in blocks),
 'runtime':records[0]['R_version']+' / '+records[0]['runtime'],
 'terra':{'versione_packageVersion':'1.9.50','rilascio':'1.9-50','GDAL':'3.8.1','PROJ':'9.2.0','GEOS':'3.11.2',
          'notebook':[3,8,18,19,20],
          'operazioni_reali':['rast','resample','readStart','readValues','readStop','shift','writeRaster','describe'],
          'NoData_tag_verificato':-9999,'tipo_GeoTIFF':'FLOAT64 / FLT8S',
          'celle_interne':616,'celle_bordo_NoData':104,
          'CRS':'EPSG:32632 con georeferenziazione esplicitamente fittizia'},
 'audit_indipendente':{'controlli':len(geo['controlli']),'esito':geo['esito'],
                       'rasterio':geo['rasterio'],'GDAL':geo['GDAL'],'numpy':geo['numpy'],
                       'GeoTIFF':geo['GeoTIFF']},
 'provenienza':{'commit':sources['commit'],'file_verificati':len(sources['files']),
               'originali_R':20,'input':3,'algoritmi':['SHA-256','Git blob SHA-1']},
 'offline':{'immagini_incorporate':sum(r['images'] for r in offline['controlli']),
            'formule_MathML':sum(r['mathml'] for r in offline['controlli']),
            'errori':offline['errori'],'collegamenti_mancanti':len(offline['errori'])},
 'visiva':{'figure_ispezionate':20,'anteprime_layout':['index','M12_N08','M12_N17','M12_N20'],
           'metodo':'Montaggio delle figure R e PNG del primo foglio temporaneo WeasyPrint70, media screen1400x1000.',
           'limite':'La verifica layout non equivale a una prova nel browser; WeasyPrint non convalida il rendering MathML.',
           'note':'QA/NOTE_QA.md'},
 'precisione_ricampionamento':{'notebook':'M12_N08','tolleranza_m':1e-4,
                             'scarto_massimo_osservato_m':6.10015e-5,
                             'nota':'Piccolo arrotondamento del percorso di resampling; nessuna promessa di identità bit per bit.'}
}
(V/'RIEPILOGO_QA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(summary['stato'],summary['notebook_Rmd'],'notebook,',summary['blocchi_R_eseguiti'],
      'blocchi,',summary['figure_R'],'figure,',len(offline['errori']),'errori HTML,',len(geo['controlli']),'controlli indipendenti.')
