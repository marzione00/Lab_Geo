from pathlib import Path
import csv,html,shutil,subprocess
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M10/03_Notebook_svolti/M10_Futura'
style=(BASE/'R/stile_notebook.css').read_text()
records=list(csv.DictReader((BASE/'VERIFICA_NOTEBOOK.csv').open()))
esc=html.escape
head='<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>'+style+'</style></head><body><main>'
tail='<footer><p>GeoStat Lab · M10 Futura · Edizione 2026-11-20. Codice e dati locali; HTML autonomi; formule MathML; nessuna risorsa esterna necessaria alla lettura.</p></footer></main></body></html>'
parts=[head.replace('{title}','M10 Futura — Notebook svolti'),'<nav><a href="README.html">Istruzioni e riproducibilità</a><a href="VERIFICA_NOTEBOOK.csv">Registro di esecuzione</a><a href="MAPPA_ORIGINALI.csv">Corrispondenza con il sito</a></nav>','<p class="eyebrow">GeoStat Lab · M10</p><h1>Futura</h1><p class="question">Previsione e progetto statistico</p>','<p>20 laboratori autonomi, svolti in R. Ogni pagina collega una domanda a codice eseguito, risultati, interpretazione, variante e risposta. I notebook mantengono gli identificativi e gli argomenti del sito.</p>',f'<div class="callout"><strong>{len(records)} notebook · {sum(int(r["blocchi_eseguiti"]) for r in records)} blocchi eseguiti · {sum(int(r["grafici"]) for r in records)} grafici · 0 errori · 0 avvisi</strong><p>Runtime della verifica: {esc(records[0]["R_version"])} · {esc(records[0]["runtime"])}. Gli HTML si leggono offline; gli Rmd consentono di rieseguire e modificare i calcoli.</p></div>','<p class="meta">Per iniziare: aprire una pagina HTML. Per eseguire: aprire <code>GeoStat_Lab_Notebooks.Rproj</code>, poi lo stesso file Rmd. <a href="README.html">Leggere la guida completa</a>.</p>']
groups=[(1,9,'01 / Previsione temporale','CO₂ storica: origine 1998-12, train 168 mesi e test 36 mesi.'),(10,13,'02 / Progetto base','Fossili sintetici: audit, confronto predittivo e relazione argomentata.'),(14,18,'03 / Approfondimento VAR','Sistema sintetico: due equazioni, stabilità, Granger e ricorsione.'),(19,20,'04 / Laboratori applicativi','Due controlli concreti: duplicati e ripetizione stagionale oltre 12 mesi.')]
for a,b,title,desc in groups:
 parts.extend([f'<h2>{esc(title)}</h2><p>{esc(desc)}</p><div class="module-grid">'])
 for r in records[a-1:b]:
  glabel=r['grafici']+(' grafico' if r['grafici']=='1' else ' grafici')
  parts.append(f'<article class="card"><p class="eyebrow">{r["id"]}</p><h3><a href="{r["html"]}">{esc(r["titolo"])}</a></h3><p class="meta">5 blocchi eseguiti · {glabel} · esito OK</p><div class="file-links"><a href="{r["html"]}">Apri svolgimento</a><a href="{r["rmd"]}">RMarkdown</a><a href="R/Originali_corso/{r["id"]}.R">Originale</a></div></article>')
 parts.append('</div>')
parts.extend(['<h2>Prima di interpretare</h2><p>Il test misura un protocollo dichiarato su questi dati. La copertura su una singola traiettoria non dimostra calibrazione universale; il legame geometrico dei fossili e il contributo di Granger non identificano causalità fisica. Natura dei dati, unità e limiti sono esplicitati nei notebook.</p>','<p><a href="Dati/PROVENIENZA.json">Provenienza e impronte dei dati</a> · <a href="Verifiche/sessionInfo.txt">Sessione R</a> · <a href="INDICE_NOTEBOOK.csv">Indice in CSV</a></p>',tail])
(BASE/'index.html').write_text('\n'.join(parts))
r=subprocess.run(['pandoc',str(BASE/'README.md'),'--from=markdown','--to=html5','--mathml','--highlight-style=tango'],capture_output=True,text=True,check=True)
(BASE/'README.html').write_text(head.replace('{title}','Futura — Istruzioni')+'<nav><a href="index.html">← Indice Futura</a><a href="README.md">Testo sorgente</a></nav>'+r.stdout+tail)
dst=BASE/'Sorgenti_generazione/crea_indice.py'
if dst.resolve()!=Path(__file__).resolve():shutil.copy2(__file__,dst)
print('Indice e guida HTML creati.')
