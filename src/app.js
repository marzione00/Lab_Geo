(function () {
  "use strict";
  const C=window.GeoCore, catalog=window.GEO_CATALOG.modules, config=window.GEO_CONFIG;
  const main=document.getElementById("contenuto"), announcer=document.getElementById("annuncio");
  const h=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const route=(id,p)=>"#modulo-"+id+(p?"/slide/"+p:"");
  let storage;try{storage=window.localStorage;}catch{storage=null;}
  let progress=C.loadProgress(storage), current=null, view="slide", renderId=0, selectedCode="figure";
  const moduleCache=window.GEO_MODULES=window.GEO_MODULES||{}, pending={};
  function announce(s){announcer.textContent=s;}
  function persist(){C.saveProgress(storage,progress);}
  function loadModule(id) {
    if(moduleCache[id])return Promise.resolve(moduleCache[id]);
    if(pending[id])return pending[id];
    pending[id]=new Promise((resolve,reject)=>{
      const script=document.createElement("script");script.src="assets/content/"+id+".js";script.integrity=window.GEO_INTEGRITY["assets/content/"+id+".js"];script.crossOrigin="anonymous";
      script.onload=()=>moduleCache[id]?resolve(moduleCache[id]):reject(new Error("Contenuto non disponibile"));
      script.onerror=()=>{delete pending[id];reject(new Error("Impossibile aprire il modulo "+id));};
      document.head.append(script);
    });return pending[id];
  }
  const link=(url,label,cls="")=>'<a class="'+cls+'" href="'+h(url)+'">'+label+'</a>';
  function breadcrumbs(m,extra=""){
    return '<div class="breadcrumb">'+link("#indice","Il corso")+'<span>/</span>'+link(route(m.id),h(m.id)+" · "+h(m.title))+(extra?'<span>/</span><span>'+h(extra)+'</span>':"")+'</div>';
  }
  function moduleCard(m){
    const done=progress.done.filter(x=>x.startsWith(m.id+":")).length;
    return '<article class="module-card '+(m.category==="progetti"?"project":"")+'" data-module="'+m.id+'"><div class="card-top"><span class="code-tag">'+m.id+'</span><span class="card-kind">'+(m.category==="progetti"?"Macroprogetto":"Modulo")+'</span></div><h3>'+link(route(m.id),h(m.title))+'</h3><p>'+h(m.subtitle)+'</p>'+(m.category==='progetti'?'<div class="project-parents">'+(worlds.expeditions[m.id]||[]).map(id=>link(route(id),id)).join('')+'</div>':'')+'<div class="card-foot"><span>'+(m.category==='progetti'?'Spedizione integrata':window.GeoLabs.count(m.id)+' esperimenti interattivi')+'</span>'+link(route(m.id),"Apri ↗")+'</div></article>';
  }
  function catalogueSection(category){
    return '<section class="catalogue" id="catalogo"><div class="section-head"><h2>Il percorso del corso</h2><p>Dai fondamenti del calcolo alle analisi geologiche complete. Ogni modulo raccoglie esperimenti, formalismo e codice R eseguibile.</p></div><div class="filter-bar"><div class="filters" aria-label="Tipo di percorso">'+[["tutti","Tutto il corso"],["moduli","Moduli"],["progetti","Macroprogetti"]].map(([id,title])=>'<button data-filter="'+id+'" aria-pressed="'+(category===id)+'">'+title+'</button>').join("")+'</div><label class="search"><span aria-hidden="true">⌕</span><input id="cerca-moduli" type="search" aria-label="Cerca modulo o argomento" placeholder="Cerca un modulo o un argomento"></label></div><p id="result-count" class="result-count" role="status"></p><div id="module-cards" class="cards"></div></section>';
  }
  function fillCards(category,query){
    const list=C.filterModules(catalog,query,category);
    document.getElementById("module-cards").innerHTML=list.length?list.map(moduleCard).join(""):'<p class="empty">Nessun modulo corrisponde alla ricerca.</p>';
    document.getElementById("result-count").textContent=list.length+" unità didattiche";
    main.querySelectorAll("[data-filter]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.filter===category)));
    window.GeoSpace?.refresh();
  }
  function catalogueHome(type){
    const category=type==="progetti"?"progetti":"tutti";
    main.innerHTML='<div class="wrap">'+'<div class="breadcrumb">'+link("#indice","Il corso")+'<span>/</span><span>'+ (category==="progetti"?"Macroprogetti":"Indice dei moduli")+'</span></div>'+catalogueSection(category)+'<section class="resource-band"><div><p class="eyebrow" style="color:var(--mint)">Materiali riproducibili</p><h2>Dalla pagina al calcolo.</h2><p>Le figure del corso sono accompagnate dai sorgenti R, i diagrammi dai file TikZ. Dati, convenzioni e verifiche rimangono disponibili insieme alle presentazioni.</p></div><div class="resource-links">'+link("#materiali","Dati, codici e istruzioni <span aria-hidden=\"true\">↗</span>")+link("materiali/audit/Rapporto_revisione_R6.pdf","Rapporto della rilettura R6 <span aria-hidden=\"true\">↗</span>")+link("materiali/audit/Registro_slide_R6.html","Registro delle 861 slide <span aria-hidden=\"true\">↗</span>")+'</div></section></div>';
    let active=category;
    fillCards(active,"");
    main.querySelectorAll("[data-filter]").forEach(b=>b.addEventListener("click",()=>{active=b.dataset.filter;fillCards(active,document.getElementById("cerca-moduli").value);}));
    document.getElementById("cerca-moduli").addEventListener("input",e=>fillCards(active,e.target.value));
  }
  const worlds=window.GeoPlanets;
  function planetSlot(id,cls="",hero=0){const p=worlds.byId[id];return '<div class="planet-slot '+(p.rings?'ringed ':'')+cls+'" data-planet="'+id+'" data-hero="'+hero+'" aria-hidden="true"></div>';}
  function worldCard(p){const m=catalog.find(m=>m.id===p.id),done=progress.done.filter(x=>x.startsWith(p.id+':')).length;
    return '<a class="world-card" data-world-card="'+m.id+'" href="'+route(m.id)+'" aria-label="'+h(m.id+' · '+m.title+' · '+p.name)+'"><div class="world-orbit">'+planetSlot(p.id)+'</div><span class="world-name">'+m.id+' / '+h(p.name.toUpperCase())+'</span><h2>'+h(m.title)+'</h2><span class="world-type">'+h(p.description)+'</span>'+(done?'<span class="visited">'+done+' pagine studiate</span>':'')+'</a>';
  }
  function atlas(){
    main.innerHTML='<div class="wrap"><section class="atlas-intro"><div><p class="eyebrow">ATLANTE / 17 DESTINAZIONI</p><h1>La mappa del corso.</h1><p class="lead">Ogni mondo ospita un laboratorio. Scegli una destinazione per modificare dati e ipotesi, osservare i risultati e ricostruire i calcoli in R.</p></div>'+link('#catalogo','Apri l’indice testuale ↗','button secondary')+'</section><div class="atlas-toolbar" aria-label="Regioni del corso">'+['Tutte le regioni',...worlds.sectors].map((name,i)=>'<button type="button" data-sector="'+(i?name:'all')+'" aria-pressed="'+(!i)+'">'+name+'</button>').join('')+'</div><div class="star-map"><svg class="star-routes" aria-hidden="true"></svg><div class="star-grid"></div></div><div class="map-note"><span>La rotta suggerita segue l’ordine T00 → M16. Tutte le destinazioni sono accessibili.</span>'+link('#progetti','Esplora le 11 spedizioni →')+'</div></div>';
    function fill(sector){main.querySelector('.star-grid').innerHTML=worlds.planets.filter(p=>sector==='all'||p.sector===sector).map(worldCard).join('');main.querySelectorAll('[data-sector]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.sector===sector)));window.GeoSpace?.refresh();requestAnimationFrame(drawRoutes);}
    main.querySelectorAll('[data-sector]').forEach(b=>b.addEventListener('click',()=>fill(b.dataset.sector)));fill('all');
  }
  function drawRoutes(){
    const map=main.querySelector('.star-map'),svg=main.querySelector('.star-routes');if(!map||!svg)return;
    const box=map.getBoundingClientRect(),nodes=[...map.querySelectorAll('.world-orbit')].map(el=>{const b=el.getBoundingClientRect();return {x:b.left+b.width/2-box.left,y:b.top+b.height/2-box.top};});
    svg.setAttribute('viewBox','0 0 '+Math.max(1,box.width)+' '+Math.max(1,box.height));
    svg.innerHTML=nodes.slice(1).map((b,i)=>{const a=nodes[i];if(b.x<a.x)return '';return '<path d="M '+a.x+' '+a.y+' C '+(a.x+70)+' '+(a.y-35)+', '+(b.x-70)+' '+(b.y-35)+', '+b.x+' '+b.y+'"/>';}).join('');
  }
  function home(type){
    if(type!=='indice'){catalogueHome(type);if(type==='progetti'){
      const intro=document.createElement('section');intro.className='project-intro';intro.innerHTML='<p class="eyebrow">SPEDIZIONI APPLICATIVE</p><h1>Porta i metodi sul campo.</h1><p class="lead">Undici indagini collegano i moduli del corso a problemi geologici, ambientali e territoriali. Ogni spedizione riunisce dati, analisi e materiali riproducibili.</p>';main.querySelector('.catalogue').before(intro);
    }return;}
    let last=null;try{const value=storage?.getItem('geostat-last-experiment');if(window.GeoLabs.parseHash(value||'')?.type==='experiment')last=value;}catch{}
    main.innerHTML='<div class="wrap"><section class="orbital-home"><div class="home-copy"><p class="eyebrow">STATISTICA E CODING R / SCIENZE DELLA TERRA</p><h1>La Terra,<br><em>un esperimento<br>alla volta.</em></h1><p class="lead">Modifica un’ipotesi, osserva il risultato e ricostruisci il calcolo in R. Un viaggio sperimentale attraverso statistica e scienze della Terra.</p><div class="actions">'+link('#esperimenti','Esplora gli esperimenti →','button')+link(last||'#laboratorio/m05-intervalli',last?'Riprendi l’esperimento':'Prova gli intervalli di confidenza','button secondary')+'</div><p class="home-coordinate">17 MONDI · 11 SPEDIZIONI<br>UN PERCORSO DI CONOSCENZA</p></div><div class="planet-viewport" aria-hidden="true"><div class="home-world">'+planetSlot('M01','',1)+'</div></div><div class="home-world-label"><span>IL NOSTRO PUNTO DI PARTENZA</span><strong>TERRA</strong></div></section><div class="stats"><div class="stat"><strong>17</strong><span>moduli</span></div><div class="stat"><strong>11</strong><span>macroprogetti</span></div><div class="stat"><strong>139</strong><span>esperimenti interattivi</span></div><div class="stat"><strong>R</strong><span>eseguito nel browser</span></div></div><section class="home-section"><div class="section-head"><div><p class="eyebrow">DESTINAZIONI DEL CORSO</p><h2>Ogni mondo,<br>una prospettiva.</h2></div><p>Ogni pianeta riunisce esperimenti guidati e percorsi di esplorazione. Grafici, formalismo e codice condividono la stessa configurazione.</p></div><div class="destination-strip">'+['M04','M09','M14'].map(id=>{const p=worlds.byId[id],m=catalog.find(x=>x.id===id);return '<a class="destination" data-world-card="'+id+'" href="'+route(id)+'">'+planetSlot(id)+'<div><span class="world-name">'+id+' / '+p.name.toUpperCase()+'</span><h3>'+h(m.title)+'</h3><small>'+p.description+' ↗</small></div></a>';}).join('')+'</div></section><section class="resource-band"><div><p class="eyebrow">DAL FENOMENO AL MODELLO</p><h2>Esplorare, comprendere,<br>riprodurre.</h2><p>Confronta scenari, conserva le osservazioni e scarica il codice della configurazione scelta. Le presentazioni originali accompagnano l’approfondimento.</p></div><div class="resource-links">'+link('#esperimenti','Cerca fra i 139 esperimenti ↗')+link('#progetti','Le spedizioni applicative ↗')+link('#materiali','Dati, codici e istruzioni ↗')+'</div></section></div>';
  }
  window.addEventListener('resize',drawRoutes);
  function toc(m,page){
    let section="";
    return '<aside class="reader-sidebar" aria-label="Indice delle slide"><h2>'+m.id+' · Indice</h2><input type="search" id="cerca-slide" aria-label="Cerca nell’indice del modulo" placeholder="Cerca una slide">'+m.slides.map(s=>{
      const title=s.section!==section?'<p class="toc-section">'+h(s.section)+'</p>':"";section=s.section;
      return title+'<a class="toc-link" href="'+route(m.id,s.page)+'" data-search="'+h(C.clean(s.title+" "+s.section))+'"'+(s.page===page?' aria-current="page"':"")+'><span>'+String(s.page).padStart(2,"0")+'</span><span>'+h(s.title)+'</span></a>';
    }).join("")+'</aside>';
  }
  function formula(s){return s?'<div class="math">\\[\\begin{gathered}'+h(s)+'\\end{gathered}\\]</div>':"";}
  function reading(m,s){
    return '<article class="reading"><p>'+h(s.body)+'</p>'+formula(s.formula)+(s.aside?'<div class="aside-text"><p>'+h(s.aside)+'</p></div>':"")+formula(s.formulaAside)+((s.figure||s.diagram)?'<figure>'+(s.figure?'<img src="assets/visuals/'+m.id+'/'+String(s.page).padStart(3,"0")+'.svg" alt="Rappresentazione della slide: '+h(s.title)+'">':'<svg class="reading-diagram" xmlns="http://www.w3.org/2000/svg" viewBox="328.819 77.953 211.181 212.598" role="img" aria-label="Diagramma: '+h(s.title)+'"><image href="'+h(s.image)+'" width="566.93" height="354.33"/></svg>')+(s.caption?'<figcaption'+(s.diagram?' class="sr-only"':"")+'>'+h(s.caption)+'</figcaption>':"")+'</figure>':s.caption?'<p>'+h(s.caption)+'</p>':"")+(s.recall?'<div class="recall"><strong>Richiamo.</strong> '+h(s.recall)+'</div>':"")+(s.kind==="indice"?'<ol>'+m.sections.map(x=>'<li>'+link(route(m.id,x.page),h(x.title))+'</li>').join("")+'</ol>':"")+'</article>';
  }
  function snippet(m,s){
    const text=s.code||m.figureCode, path=s.codePath||m.script;
    return '<section class="code-panel"><p class="code-note">'+(s.code?'Frammento riportato nella slide.':'Questa slide non contiene un frammento di codice; è disponibile lo script completo delle figure del modulo.')+'</p><div class="code-top"><strong>'+h(path)+'</strong><div class="code-actions"><button class="button small secondary" data-copy="current-code">Copia codice</button><a class="button small" href="'+h(path)+'" download>Scarica .R</a></div></div><pre><code id="current-code">'+h(text)+'</code></pre><p class="code-note">Esegui il codice in R dalla cartella <code>materiali/</code>, dopo aver installato le dipendenze indicate nella guida.</p></section>';
  }
  function slidePanel(m,s){
    const panel=document.getElementById("slide-panel");
    if(window.MathJax?.typesetClear)window.MathJax.typesetClear([panel]);
    if(view==="testo"){
      panel.innerHTML=reading(m,s);typeset(panel);
    }else if(view==="codice"){panel.innerHTML=snippet(m,s);}
    else{
      panel.innerHTML='<div class="slide-frame"><img src="'+s.image+'" alt="'+h(m.id+" · pagina "+s.page+" · "+s.title)+'. Testo accessibile nella scheda Testo e formule."></div><div class="slide-caption"><span>Template originale · immagine vettoriale</span><a href="'+s.image+'" target="_blank" rel="noopener">Ingrandisci ↗</a><a href="'+m.pdf+'#page='+s.page+'" target="_blank" rel="noopener">Apri nel PDF ↗</a></div>';
    }
    main.querySelectorAll("[data-view]").forEach(b=>{b.setAttribute("aria-selected",String(b.dataset.view===view));b.tabIndex=b.dataset.view===view?0:-1;});
    bindCopy();
  }
  function slidePage(m,page){
    const s=m.slides[page-1], key=m.id+":"+page, done=progress.done.includes(key);
    progress.last=route(m.id,page);persist();
    main.innerHTML=planetSlot(m.id,'reading-planet',.15)+'<div class="viewer">'+breadcrumbs(m,"Slide "+page)+'<div class="reader-layout">'+toc(m,page)+'<div class="reader-main"><div class="reader-title"><h1>'+h(s.title)+'</h1><span class="page-counter">'+String(page).padStart(2,"0")+' / '+m.pages+'</span></div><div class="reader-tools"><div class="tabs" role="tablist" aria-label="Modalità di lettura">'+[["slide","Slide"],["testo","Testo e formule"],["codice","Codice R"]].map(([id,label])=>'<button role="tab" data-view="'+id+'" id="tab-'+id+'" aria-controls="slide-panel" aria-selected="'+(view===id)+'">'+label+'</button>').join("")+'</div><div class="pager"><button data-step="-1" aria-label="Slide precedente"'+(page===1?" disabled":"")+'>←</button><button data-step="1" aria-label="Slide successiva"'+(page===m.pages?" disabled":"")+'>→</button></div></div><div id="slide-panel" role="tabpanel" aria-labelledby="tab-'+view+'"></div><div class="study-actions"><button id="mark-done" class="button small secondary '+(done?"done":"")+'" aria-pressed="'+done+'">'+(done?"✓ Segnata come studiata":"Segna come studiata")+'</button><p>Il progresso resta soltanto in questo browser.</p></div><details class="review-note"><summary>Nota della rilettura R6</summary><p>'+h(s.review.observation)+'</p><p>'+h(s.review.intervention)+'</p></details></div></div></div>';
    main.querySelectorAll("[data-view]").forEach(b=>b.addEventListener("click",()=>{view=b.dataset.view;document.getElementById("slide-panel").setAttribute("aria-labelledby","tab-"+view);slidePanel(m,s);}));
    main.querySelector('[role="tablist"]').addEventListener("keydown",e=>{
      if(!["ArrowLeft","ArrowRight","Home","End"].includes(e.key))return;
      e.preventDefault();e.stopPropagation();const tabs=[...main.querySelectorAll("[data-view]")],at=tabs.indexOf(document.activeElement);
      const next=e.key==="Home"?0:e.key==="End"?tabs.length-1:(at+(e.key==="ArrowRight"?1:-1)+tabs.length)%tabs.length;
      tabs[next].click();tabs[next].focus();
    });
    main.querySelectorAll("[data-step]").forEach(b=>b.addEventListener("click",()=>location.hash=route(m.id,page+Number(b.dataset.step))));
    document.getElementById("cerca-slide").addEventListener("input",e=>{
      const q=C.clean(e.target.value);main.querySelectorAll(".toc-link").forEach(a=>a.hidden=!a.dataset.search.includes(q));
    });
    document.getElementById("mark-done").addEventListener("click",e=>{
      const isDone=progress.done.includes(key);progress.done=isDone?progress.done.filter(x=>x!==key):[...progress.done,key];persist();
      e.currentTarget.classList.toggle("done",!isDone);e.currentTarget.setAttribute("aria-pressed",String(!isDone));e.currentTarget.textContent=isDone?"Segna come studiata":"✓ Segnata come studiata";announce(isDone?"Segnalazione rimossa":"Pagina segnata come studiata");
    });slidePanel(m,s);
    const active=main.querySelector('.toc-link[aria-current="page"]');if(active)active.scrollIntoView({block:"nearest"});
  }
  function codePage(m){
    const choices=[{id:"figure",title:"Analisi e figure · "+m.id,code:m.figureCode,path:m.script,language:"R"},...m.laboratories];
    if(!choices.some(x=>x.id===selectedCode))selectedCode="figure";
    main.innerHTML=planetSlot(m.id,'reading-planet',.15)+'<div class="wrap">'+breadcrumbs(m,"Codici e laboratori")+'<section class="module-head"><p class="eyebrow">'+m.id+' · Laboratorio</p><h1>Codici e materiali di lavoro</h1><p class="lead">'+h(m.title)+'</p></section><div class="code-panel"><div class="code-top"><label class="sr-only" for="select-code">Scegli lo script</label><select id="select-code">'+choices.map(x=>'<option value="'+x.id+'"'+(x.id===selectedCode?" selected":"")+'>'+h(x.id==="figure"?x.title:x.id+" · "+x.title)+'</option>').join("")+'</select><div class="code-actions"><button class="button small secondary" data-copy="current-code">Copia codice</button><a id="download-code" class="button small" download>Scarica script</a></div></div><p id="code-path" class="code-note"></p><pre><code id="current-code"></code></pre><div class="notice"><h3>Riprodurre il calcolo</h3><p>Scarica <a href="assets/downloads/GeoStatLab_codice_dati_R6.zip" download>l’archivio con codice e dati</a> e apri <code>materiali/Corso_Geologia.Rproj</code>. I percorsi degli script sono riferiti alla cartella <code>materiali/</code>. Il codice viene eseguito nell’ambiente R o Python indicato, con i dati e le dipendenze del corso.</p>'+link("materiali/Guida_corso_R6.pdf","Istruzioni e ambiente di esecuzione ↗")+'</div></div></div>';
    function select(){selectedCode=document.getElementById("select-code").value;const x=choices.find(x=>x.id===selectedCode);document.getElementById("current-code").textContent=x.code;document.getElementById("code-path").textContent=x.path+" · "+x.language;document.getElementById("download-code").href=x.path;}
    document.getElementById("select-code").addEventListener("change",select);select();bindCopy();
  }
  function materials(){
    const external=config.repositoryUrl?'<p>'+link(config.repositoryUrl,"Apri il repository GitHub ↗")+'</p>':"";
    main.innerHTML='<div class="wrap resources-page"><p class="eyebrow">Consultazione e riproducibilità</p><h1>I materiali del corso</h1><p class="lead">Presentazioni, codici, dati e verifiche condividono la stessa edizione R6. L’intero repository conserva la struttura necessaria a ricostruire le analisi.</p>'+external+'<div class="actions"><a class="button" href="assets/downloads/GeoStatLab_codice_dati_R6.zip" download>Scarica codice e dati · ZIP ↓</a></div><div class="resources-grid"><section class="resource-card"><h2>Esperimenti interattivi</h2><p>139 programmi R autonomi, con parametri, funzioni grafiche e generatori dei dati. La mappa documenta il raccordo con le sezioni del corso.</p><ul><li><a href="assets/downloads/GeoStatLab_esperimenti_R.zip" download>Scarica i 139 esperimenti R · ZIP</a></li><li><a href="assets/downloads/GeoStatLab_mappa_esperimenti.csv" download>Mappa sezioni–esperimenti · CSV</a></li><li><a href="vendor/r-packages-lock.json">Versioni e impronte dei pacchetti R</a></li></ul></section><section class="resource-card"><h2>Presentazioni e percorso</h2><ul><li>'+link("#catalogo","Indice dei 28 fascicoli")+'</li><li>'+link("materiali/Guida_corso_R6.pdf","Guida al corso e alla ricostruzione")+'</li><li>'+link("materiali/Guida_laboratori_M05.pdf","Laboratori M05: consegne e soluzioni")+'</li><li>'+link("materiali/documentazione/catalogo_laboratori.csv","Catalogo dei laboratori · CSV")+'</li></ul></section><section class="resource-card"><h2>Ambiente di lavoro</h2><p>Le figure sono generate in R; il modulo introduttivo conserva anche i laboratori Python. Gli script si eseguono dalla cartella materiali.</p><ul><li>'+link("materiali/R/00_installazione.R","Installazione esplicita dei pacchetti R")+'</li><li>'+link("materiali/R/controlla_ambiente.R","Controllo dell’ambiente R")+'</li><li>'+link("materiali/verifiche/versioni_R.csv","Versioni dei pacchetti collaudati")+'</li><li>'+link("materiali/strumenti/requirements.txt","Dipendenze del percorso Python")+'</li></ul></section><section class="resource-card"><h2>Rilettura delle slide</h2><p>Tutte le 861 pagine sono state esaminate; 357 contengono interventi documentati.</p><ul><li>'+link("materiali/audit/Rapporto_revisione_R6.pdf","Rapporto con confronti prima/dopo")+'</li><li>'+link("materiali/audit/Registro_slide_R6.html","Registro completo consultabile")+'</li><li>'+link("materiali/audit/Registro_slide_R6.csv","Registro delle osservazioni · CSV")+'</li><li>'+link("materiali/verifiche/consegna_finale.json","Esito dei controlli della consegna")+'</li></ul></section><section class="resource-card"><h2>Provenienza e sorgenti</h2><p>Ogni modulo rimanda ai propri sorgenti R e LaTeX. Dati, figure e diagrammi mantengono gli identificativi del corso.</p><ul><li>'+link("materiali/documentazione/fonti_online_R6.json","Riferimenti bibliografici e documentazione")+'</li><li>'+link("materiali/documentazione/raccordo_slide.csv","Raccordo con le slide originali")+'</li><li>'+link("materiali/MANIFEST_SHA256.txt","Impronte dei materiali R6")+'</li><li>'+link("THIRD_PARTY_NOTICES.md","Componenti e licenze")+'</li></ul></section></div></div>';
  }
  async function copyCode(button){
    const text=document.getElementById(button.dataset.copy).textContent;
    try{
      if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(text);
      else{const t=document.createElement("textarea");t.value=text;t.className="sr-only";document.body.append(t);t.select();if(!document.execCommand("copy"))throw Error();t.remove();button.focus();}
      const old=button.textContent;button.textContent="Copiato";announce("Codice copiato");setTimeout(()=>button.textContent=old,1800);
    }catch{announce("Copia non disponibile: seleziona il testo del codice.");button.textContent="Seleziona il codice";}
  }
  function bindCopy(){main.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",()=>copyCode(b)));}
  let mathPromise;
  function typeset(element){
    if(!mathPromise){
      mathPromise=new Promise((resolve,reject)=>{
        window.MathJax={tex:{inlineMath:[["$","$"],["\\(","\\)"]],displayMath:[["\\[","\\]"]],packages:["base","ams","newcommand","configmacros","noundefined"],maxMacros:2000,maxBuffer:10000},svg:{fontCache:"local"},startup:{typeset:false},options:{enableMenu:false}};
        const script=document.createElement("script");script.src="vendor/mathjax/tex-svg.js";script.integrity=window.GEO_INTEGRITY["vendor/mathjax/tex-svg.js"];script.crossOrigin="anonymous";
        script.onload=()=>window.MathJax.startup.promise.then(resolve,reject);script.onerror=reject;document.head.append(script);
      });
    }
    mathPromise.then(()=>{if(element.isConnected)return window.MathJax.typesetPromise([element]);}).catch(()=>announce("Le formule complete sono consultabili nella scheda Slide e nel PDF."));
  }
  async function render(){
    const token=++renderId;current=window.GeoLabs?.parseHash(location.hash)||C.parseRoute(location.hash,catalog);
    window.GeoLabs?.cleanup();
    if(window.MathJax?.typesetClear)window.MathJax.typesetClear([main]);
    document.title=config.title+" · "+(current.id?catalog.find(m=>m.id===current.id).title:config.subtitle);
    try{
      if(current.type==="experiment")window.GeoLabs.experiment(main,window.GeoLabs.byId.get(current.activity),current.query);
      else if(current.type==="esperimenti")window.GeoLabs.index(main);
      else if(current.type==="mappa")atlas();
      else if(["indice","catalogo","progetti"].includes(current.type))home(current.type);
      else if(current.type==="materiali")materials();
      else if(current.type==="notfound")main.innerHTML='<section class="error"><h1>Pagina non trovata</h1><p>Il collegamento non corrisponde a un modulo o a una slide del corso.</p>'+link("#indice","Torna all’indice","button")+'</section>';
      else{
        main.innerHTML='<p class="loading">Apertura del modulo '+current.id+'…</p>';
        const m=await loadModule(current.id);if(token!==renderId)return;
        if(current.type==="module"){if(m.category==='progetti')window.GeoLabs.mission(main,m);else window.GeoLabs.module(main,m);}
        else if(current.type==="slide")slidePage(m,current.page);
        else codePage(m);
      }
      window.scrollTo({top:0,behavior:"instant"});
      window.GeoSpace?.onRoute(current);
      document.querySelectorAll(".site-header nav a").forEach(a=>{const active=a.getAttribute("href")==="#"+current.type;if(active)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});
      if(current.type==="mappa")requestAnimationFrame(drawRoutes);
    }catch(err){main.innerHTML='<section class="error"><h1>Il modulo non è disponibile</h1><p>'+h(err.message)+'</p><p>Verifica che l’intera cartella del sito sia stata copiata.</p>'+link("#indice","Torna all’indice","button")+'</section>';}
  }
  document.addEventListener("keydown",e=>{
    if(current?.type!=="slide"||e.defaultPrevented||e.altKey||e.ctrlKey||e.metaKey||/INPUT|SELECT|TEXTAREA/.test(e.target.tagName)||e.target.isContentEditable)return;
    if(!["ArrowLeft","ArrowRight"].includes(e.key))return;
    const m=catalog.find(x=>x.id===current.id),n=current.page+(e.key==="ArrowRight"?1:-1);
    if(n>=1&&n<=m.pages){e.preventDefault();location.hash=route(m.id,n);}
  });
  if(config.mainSiteUrl){
    const homeLink=document.createElement("a");homeLink.href=config.mainSiteUrl;
    homeLink.textContent="Sito principale ↗";
    document.querySelector(".site-footer div:nth-child(2)").append(homeLink);
  }
  document.querySelector('.skip').addEventListener('click',event=>{event.preventDefault();main.focus();main.scrollIntoView({block:'start'});});
  window.GeoLabs.configure({typeset});
  window.addEventListener("hashchange",render);render();
})();
