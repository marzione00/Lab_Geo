from pathlib import Path
import base64, csv, hashlib, html, json, re, shutil, subprocess, sys
import fitz
HERE=Path(__file__).resolve().parent
BASE=HERE.parent if HERE.name=='Sorgenti_generazione' else HERE.parent/'M10/03_Notebook_svolti/M10_Futura'
STYLE=(BASE/'R/stile_notebook.css').read_text()
STYLE+='''\n:root{--teal:#1d7890}a{color:#16667e}.codebox>div.sourceCode{margin:0}.codebox pre.sourceCode{margin:0;background:transparent;border:0}pre>code{font-size:inherit}.notebook-status{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 24px}.notebook-status span{background:#edf4f6;color:#294e5d;padding:5px 10px;border-radius:4px;font-size:13px}.toc ul{margin:7px 0}.toc>ul>li{margin-top:12px}#title-block-header{margin:0 0 28px}#title-block-header h1{margin-bottom:10px}h1:not(.title){font-size:30px;margin-top:35px}h1.title{font-size:39px}h2{scroll-margin-top:20px}.subtitle{color:var(--teal);font-weight:700;letter-spacing:.06em}.output pre{white-space:pre;overflow:auto}.sourceCode{overflow:visible}.sourceCode pre{overflow:auto}.footer-note{font-size:13px;color:var(--muted)}@media(max-width:640px){h1.title{font-size:30px}h1:not(.title){font-size:26px}.notebook-status{gap:5px}}\n'''
TEMPLATE='''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="generator" content="R eseguito e Pandoc MathML" />
<title>$pagetitle$ — Futura</title>
<style>'''+STYLE+'''</style>
$if(highlighting-css)$<style>$highlighting-css$</style>$endif$
</head>
<body><main>
$nav$
<header id="title-block-header"><p class="eyebrow">GeoStat Lab · M10 · Previsione e progetto statistico</p><p class="subtitle">$subtitle$</p><h1 class="title">$title$</h1></header>
<div class="notebook-status"><span>5 blocchi R eseguiti</span><span>$figure_label$</span><span>0 errori · 0 avvisi</span><span>Offline · MathML</span></div>
<p class="meta">Codice, output e figure dello stesso svolgimento. Ogni notebook riparte dai dati locali ed è autonomo rispetto agli altri.</p>
$if(toc)$<details class="toc"><summary>Indice di questo notebook</summary>$table-of-contents$</details>$endif$
$body$
<footer><p>Edizione 2026-11-20 · Esecuzione: $r_version$, $runtime$. Gli output sono stati catturati eseguendo i blocchi R; i grafici derivano dai dispositivi PDF di R. HTML prodotto con Pandoc e formule MathML, senza servizi esterni.</p><p><a href="VERIFICA_NOTEBOOK.csv">Registro di esecuzione</a> · <a href="Dati/PROVENIENZA.json">Provenienza dei dati</a> · <a href="README.html">Come riprodurre</a></p></footer>
</main></body></html>
'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def build():
    plan=json.loads((BASE/'Verifiche/piano_esecuzione.json').read_text())
    statuses=list(csv.DictReader((BASE/'Verifiche/esecuzione_blocchi.csv').open()))
    assert len(statuses)==100 and all(r['esito']=='OK' and r['avvisi']=='0' for r in statuses)
    state={(r['id'],r['blocco']):r for r in statuses}
    template=BASE/'Sorgenti_generazione/template_notebook.html'
    template.write_text(TEMPLATE)
    records=[]
    for i,p in enumerate(plan,1):
        ident=p['id']; figure_no=0
        s=(BASE/p['rmd']).read_text()
        assert sha(BASE/p['rmd'])==sha(BASE/'Verifiche'/ident/'sorgente_eseguito.Rmd'), 'Rmd modificato dopo esecuzione: '+ident
        chunks=re.findall(r'```\{r ([^,}\s]+)[^}]*\}\n(.*?)\n```',s,re.S)
        assert len(chunks)==5
        for name,code in chunks:
            st=state[ident,name]
            out=(BASE/st['output']).read_text().strip('\n')
            rendered=f'\n<div class="codebox">\n<div class="code-label">Codice R · {name}</div>\n\n```r\n{code}\n```\n\n</div>\n'
            if out:
                rendered+=f'\n<div class="output"><div class="code-label">Output eseguito</div><pre>{html.escape(out)}</pre></div>\n'
            pdf=BASE/st['grafico_pdf']; doc=fitz.open(pdf)
            for page_i,page in enumerate(doc):
                figure_no+=1
                pix=page.get_pixmap(dpi=150,alpha=False)
                img=pdf.with_name(f'{name}_{page_i+1:02d}.png')
                pix.save(img)
                b64=base64.b64encode(img.read_bytes()).decode()
                alt=f'{ident}, figura {figure_no}: risultato grafico del blocco {name}'
                rendered+=f'\n<figure><img src="data:image/png;base64,{b64}" alt="{alt}" width="1200" height="750" loading="lazy"/><figcaption>Figura {figure_no} · Output del blocco <code>{name}</code>. <a href="{st["grafico_pdf"]}">PDF vettoriale</a>.</figcaption></figure>\n'
            doc.close()
            old=re.escape('```{r '+name+'}')+r'\n.*?\n```'
            s=re.sub(old,lambda _:rendered,s,count=1,flags=re.S)
        nav=['<a href="index.html">← Indice Futura</a>',f'<a href="{ident}.Rmd">Sorgente RMarkdown</a>',f'<a href="R/Originali_corso/{ident}.R">Laboratorio originale</a>']
        if i>1:nav.append(f'<a href="M10_N{i-1:02d}.html">← Precedente</a>')
        if i<20:nav.append(f'<a href="M10_N{i+1:02d}.html">Successivo →</a>')
        temp=BASE/'Verifiche'/ident/'compilato.md';temp.write_text(s)
        cmd=['pandoc',str(temp),'--from=markdown+tex_math_dollars','--to=html5','--standalone','--mathml','--toc','--toc-depth=2','--highlight-style=tango','--template',str(template),'-V','nav=<nav>'+''.join(nav)+'</nav>','-V','figure_label='+str(figure_no)+(' grafico' if figure_no==1 else ' grafici'),'-V','r_version='+state[ident,'preparazione']['R_version'],'-V','runtime='+state[ident,'preparazione']['runtime'],'-o',str(BASE/p['html'])]
        r=subprocess.run(cmd,check=True,capture_output=True,text=True)
        (BASE/'Verifiche'/ident/'pandoc.log').write_text(r.stderr)
        assert not r.stderr.strip(),(ident,r.stderr)
        temp.unlink()
        ss=[q for q in statuses if q['id']==ident]
        records.append(dict(id=ident,titolo=p['titolo'],html=p['html'],rmd=p['rmd'],blocchi_eseguiti=5,grafici=figure_no,errori=0,avvisi=0,secondi=round(sum(float(q['secondi']) for q in ss),3),esito='OK',sha256_Rmd=sha(BASE/p['rmd']),sha256_HTML=sha(BASE/p['html']),R_version=ss[0]['R_version'],runtime=ss[0]['runtime'],data_UTC=ss[-1]['data_UTC']))
    for filename in ['VERIFICA_NOTEBOOK.csv','INDICE_NOTEBOOK.csv']:
        with (BASE/filename).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    (BASE/'Verifiche/esecuzione_notebook.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    copy=BASE/'Sorgenti_generazione/crea_html.py'
    if Path(__file__).resolve()!=copy.resolve():shutil.copy2(__file__,copy)
    print(f'HTML {len(records)}; blocchi {sum(r["blocchi_eseguiti"] for r in records)}; figure {sum(r["grafici"] for r in records)}; errori {sum(r["errori"] for r in records)}; avvisi {sum(r["avvisi"] for r in records)}')

if __name__=='__main__':build()
