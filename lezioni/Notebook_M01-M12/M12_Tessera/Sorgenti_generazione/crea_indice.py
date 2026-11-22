from pathlib import Path
import csv,html,re,shutil,subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M12/03_Notebook_svolti/M12_Tessera'
style=(BASE/'R/stile_notebook.css').read_text()
records=list(csv.DictReader((BASE/'VERIFICA_NOTEBOOK.csv').open()))
slides={r['notebook']:r for r in csv.DictReader((BASE/'MAPPA_SLIDE.csv').open())}
esc=html.escape
head='<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>'+style+'</style></head><body><main>'
tail='<footer><p>GeoStat Lab · M12 Tessera · Edizione 2026-11-20. Dati sintetici e georeferenziazione fittizia; codice e risultati locali. HTML autonomi, immagini incorporate e formule MathML.</p></footer></main></body></html>'
parts=[head.replace('{title}','M12 Tessera — Notebook svolti'),
 '<nav><a href="README.html">Istruzioni e riproducibilità</a><a href="VERIFICA_NOTEBOOK.csv">Registro di esecuzione</a><a href="MAPPA_ORIGINALI.csv">Originali e adattamenti</a><a href="MAPPA_SLIDE.csv">Raccordo con le slide</a></nav>',
 '<p class="eyebrow">GeoStat Lab · M12</p><h1>Tessera</h1><p class="question">Raster, telerilevamento e morfometria<br><small>Dalla geometria della griglia alle grandezze derivate</small></p>',
 '<p>20 laboratori autonomi in R, con gli identificativi e i titoli originali. Ogni svolgimento collega una domanda a codice eseguito, risultati, interpretazione, variante risolta e risposta.</p>',
 f'<div class="callout"><strong>{len(records)} notebook · {sum(int(r["blocchi_eseguiti"]) for r in records)} blocchi eseguiti · {sum(int(r["grafici"]) for r in records)} grafici · 0 errori · 0 avvisi</strong><p>{esc(records[0]["R_version"])} · {esc(records[0]["runtime"])}. I notebook N03, N08, N18, N19 e N20 usano terra reale per leggere, ricampionare, scrivere e rileggere raster.</p></div>',
 '<p class="meta">Per leggere: aprire un HTML. Per eseguire: aprire <code>GeoStat_Lab_Notebooks.Rproj</code> e lo stesso Rmd. I cinque notebook indicati richiedono terra installato prima dell’analisi; gli altri usano R base e pacchetti standard.</p>']
groups=[(1,4,'01 / Geometria della griglia','Celle, centri e bordi; orientamento Sud-Nord del CSV e Nord-Sud del TIFF; NoData distinto da zero.'),
 (5,8,'02 / Dominio e supporto','Ritaglio, area, aggregazione e ricampionamento. La scelta della regola dipende dal significato della variabile.'),
 (9,12,'03 / Derivate e rappresentazione','Piano analitico, pendenza, esposizione circolare e illuminazione del terreno sintetico.'),
 (13,17,'04 / Bande e sintesi spaziali','Indice normalizzato, maschere, zone, coppie dipendenti e bootstrap a blocchi con ipotesi dichiarate.'),
 (18,20,'05 / Leggere, allineare, consegnare','Finestre effettive dal GeoTIFF, griglie traslate e consegna di616pendenze con geometria verificata.')]
for a,b,title,desc in groups:
 desc=desc.replace('di616pendenze','di 616 pendenze')
 parts.extend([f'<h2>{esc(title)}</h2><p>{esc(desc)}</p><div class="module-grid">'])
 for r in records[a-1:b]:
  glabel=r['grafici']+(' grafico' if r['grafici']=='1' else ' grafici')
  dep=' · richiede terra' if int(r['id'][-2:]) in [3,8,18,19,20] else ''
  sl=slides[r['id']];page=re.match(r'\d+',sl['slide'])
  href=sl['pdf']+('#page='+page[0] if page else '')
  parts.append(f'<article class="card"><p class="eyebrow">{r["id"]}</p><h3><a href="{r["html"]}">{esc(r["titolo"])}</a></h3><p class="meta">5 blocchi eseguiti · {glabel}{dep}</p><div class="file-links"><a href="{r["html"]}">Apri svolgimento</a><a href="{r["rmd"]}">RMarkdown</a><a href="R/Originali_corso/{r["id"]}.R">Originale</a></div><p class="meta"><a href="{href}">Slide {esc(sl["slide"])}</a></p></article>')
 parts.append('</div>')
parts.extend(['<h2>Prima di interpretare</h2><p>Il raster di 720 celle e la georeferenziazione UTM sono sintetici. I centri non sono i corner; le quote mancanti non sono zero; un codice di classe non è una misura continua. Le 616 pendenze interne escludono il bordo. I quantili del bootstrap a blocchi dipendono dalle ipotesi e non sono presentati come intervalli a copertura garantita.</p>',
 '<p><a href="Dati/PROVENIENZA.json">Provenienza e impronte degli input</a> · <a href="Verifiche/sessionInfo.txt">Sessione R</a> · <a href="INDICE_NOTEBOOK.csv">Indice CSV</a> · <a href="Risultati/M12_N20/pendenze_interne.tif">GeoTIFF interno verificato</a> · <a href="Risultati/M12_N20/audit_consegna.csv">Audit della consegna</a></p>',tail])
(BASE/'index.html').write_text('\n'.join(parts))
r=subprocess.run(['pandoc',str(BASE/'README.md'),'--from=markdown','--to=html5','--mathml','--highlight-style=tango'],capture_output=True,text=True,check=True)
(BASE/'README.html').write_text(head.replace('{title}','Tessera — Istruzioni')+'<nav><a href="index.html">← Indice Tessera</a><a href="README.md">Testo sorgente</a></nav>'+r.stdout+tail)
dst=BASE/'Sorgenti_generazione/crea_indice.py'
if dst.resolve()!=Path(__file__).resolve():shutil.copy2(__file__,dst)
print('Indice e guida HTML creati.')
