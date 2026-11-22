from pathlib import Path
import csv,html,shutil,subprocess,re
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M11/03_Notebook_svolti/M11_Locus'
style=(BASE/'R/stile_notebook.css').read_text(encoding='utf-8')
records=list(csv.DictReader((BASE/'VERIFICA_NOTEBOOK.csv').open(encoding='utf-8')))
slides={r['notebook']:r for r in csv.DictReader((BASE/'MAPPA_SLIDE.csv').open(encoding='utf-8'))}
esc=html.escape
head='<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>'+style+'</style></head><body><main>'
tail='<footer><p>GeoStat Lab · M11 Locus · Edizione 2026-11-20. Dati sintetici, codice e risultati locali. HTML autonomi e formule MathML; nessuna risorsa esterna necessaria alla lettura.</p></footer></main></body></html>'
parts=[head.replace('{title}','M11 Locus — Notebook svolti'),'<nav><a href="README.html">Istruzioni e riproducibilità</a><a href="VERIFICA_NOTEBOOK.csv">Registro di esecuzione</a><a href="MAPPA_ORIGINALI.csv">Originali e adattamenti</a><a href="MAPPA_SLIDE.csv">Raccordo con le slide</a></nav>',
'<p class="eyebrow">GeoStat Lab · M11</p><h1>Locus</h1><p class="question">Statistica spaziale<br><small>Coordinate, associazione e previsione nel territorio</small></p>',
'<p>20 laboratori autonomi in R, con gli identificativi e i titoli originali del corso. Ogni pagina collega una domanda a codice eseguito, risultati, interpretazione, variante risolta e risposta.</p>',
f'<div class="callout"><strong>{len(records)} notebook · {sum(int(r["blocchi_eseguiti"]) for r in records)} blocchi eseguiti · {sum(int(r["grafici"]) for r in records)} grafici · 0 errori · 0 avvisi</strong><p>{esc(records[0]["R_version"])} · {esc(records[0]["runtime"])}. Nei notebook N05, N06 e N20 sono state eseguite le funzioni reali di sf: trasformazione, rietichettatura, scrittura e rilettura GeoJSON.</p></div>',
'<p class="meta">Per leggere: aprire un HTML. Per eseguire: aprire <code>GeoStat_Lab_Notebooks.Rproj</code> e lo stesso file Rmd. N05, N06 e N20 richiedono sf installato; gli altri usano R base e pacchetti standard.</p>']
groups=[(1,6,'01 / Coordinate e riferimenti','Audit, ordine degli assi, distanze e CRS. Il piano locale metrico rimane privo di EPSG.'),(7,10,'02 / Carte e appartenenze','Supporto puntuale, confini, relazioni multiple e scala dei buffer.'),(11,14,'03 / Vicinati e associazione','Pareggi, A binaria, W normalizzata, Moran e permutazioni dichiarate.'),(15,17,'04 / Distanza e supporto della sintesi','Coppie non indipendenti, copertura geografica e medie di blocco.'),(18,20,'05 / Prevedere, verificare, consegnare','IDW, settore Est escluso e GeoJSON geografico verificato per ID.')]
for a,b,title,desc in groups:
 parts.extend([f'<h2>{esc(title)}</h2><p>{esc(desc)}</p><div class="module-grid">'])
 for r in records[a-1:b]:
  glabel=r['grafici']+(' grafico' if r['grafici']=='1' else ' grafici')
  sf=' · richiede sf' if r['id'] in ['M11_N05','M11_N06','M11_N20'] else ''
  sl=slides[r['id']];page=re.match(r'\d+',sl['slide'])[0]
  parts.append(f'<article class="card"><p class="eyebrow">{r["id"]}</p><h3><a href="{r["html"]}">{esc(r["titolo"])}</a></h3><p class="meta">5 blocchi eseguiti · {glabel}{sf}</p><div class="file-links"><a href="{r["html"]}">Apri svolgimento</a><a href="{r["rmd"]}">RMarkdown</a><a href="R/Originali_corso/{r["id"]}.R">Originale</a></div><p class="meta"><a href="{sl["pdf"]}#page={page}">Slide {esc(sl["slide"])}</a></p></article>')
 parts.append('</div>')
parts.extend(['<h2>Prima di interpretare</h2><p>I 64 siti sono sintetici e le concentrazioni sono in unità arbitrarie. La geometria, il supporto, i pesi e il disegno della verifica definiscono ciò che una sintesi può dire. Le 2016 coppie condividono osservazioni; il test geografico contiene 24 siti esclusi; il riferimento di permutazione richiede scambiabilità.</p>',
'<p><a href="Dati/PROVENIENZA.json">Provenienza e impronte dei dati</a> · <a href="Verifiche/sessionInfo.txt">Sessione R</a> · <a href="INDICE_NOTEBOOK.csv">Indice in CSV</a> · <a href="Risultati/M11_N20/campioni.geojson">GeoJSON verificato</a></p>',tail])
(BASE/'index.html').write_text('\n'.join(parts),encoding='utf-8')
r=subprocess.run(['pandoc',str(BASE/'README.md'),'--from=markdown','--to=html5','--mathml','--highlight-style=tango'],capture_output=True,text=True,encoding='utf-8',check=True)
(BASE/'README.html').write_text(head.replace('{title}','Locus — Istruzioni')+'<nav><a href="index.html">← Indice Locus</a><a href="README.md">Testo sorgente</a></nav>'+r.stdout+tail,encoding='utf-8')
dst=BASE/'Sorgenti_generazione/crea_indice.py'
if dst.resolve()!=Path(__file__).resolve():shutil.copy2(__file__,dst)
print('Indice e guida HTML creati.')
