(function () {
  'use strict';
  const C = window.GeoCore,
    catalog = window.GEO_CATALOG.modules,
    config = window.GEO_CONFIG;
  const main = document.getElementById('contenuto'),
    announcer = document.getElementById('annuncio');
  const { html } = window.GeoHTML;
  const route = id => '#modulo-' + id;
  let current = null,
    renderId = 0,
    selectedCode = 'figure';
  const moduleCache = (window.GEO_MODULES = window.GEO_MODULES || {}),
    pending = {};
  function announce(s) {
    announcer.textContent = s;
  }
  const dataPending = {};
  // Lab details and worked solutions load only on the views that use them (same SRI map as module content).
  function loadData(file, ready) {
    if (ready()) return Promise.resolve();
    if (dataPending[file]) return dataPending[file];
    dataPending[file] = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'assets/' + file;
      script.integrity = window.GEO_INTEGRITY['assets/' + file];
      script.crossOrigin = 'anonymous';
      script.onload = () => (ready() ? resolve() : reject(new Error('Dati non disponibili: ' + file)));
      script.onerror = () => {
        delete dataPending[file];
        reject(new Error('Impossibile caricare ' + file));
      };
      document.head.append(script);
    });
    return dataPending[file];
  }
  const labDetails = () => loadData('experiments-details.js', () => !!window.GEO_LABS?.detailed);
  const solutions = () => loadData('solution-data.js', () => !!window.GEO_SOLUTIONS);
  const lessonData = id => loadData('lessons/' + id + '.js', () => !!window.GEO_LESSONS?.[id]);
  const lessonIndex = window.GEO_LESSON_INDEX || {};
  // Briefing: stylesheet and script, both with SRI, loaded only when the briefing or a hint is shown.
  let briefingStyle = null;
  function briefingAssets() {
    briefingStyle ||= new Promise((resolve, reject) => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'assets/briefing.css';
      link.integrity = window.GEO_INTEGRITY['assets/briefing.css'];
      link.crossOrigin = 'anonymous';
      link.onload = resolve;
      link.onerror = () => {
        briefingStyle = null;
        link.remove();
        reject(new Error('Impossibile caricare briefing.css'));
      };
      document.head.append(link);
    });
    return Promise.all([briefingStyle, loadData('briefing.js', () => !!window.GeoBriefing)]);
  }
  // A key that cannot be read counts as seen: without storage the briefing would return on every visit.
  const seen = key => {
    try {
      return localStorage.getItem(key) !== null;
    } catch {
      return true;
    }
  };
  let replayBriefing = null;
  function firstVisit(route) {
    if (route.type === 'indice' && (replayBriefing || !seen('geostat:briefing:v1'))) {
      const opener = replayBriefing;
      replayBriefing = null;
      briefingAssets()
        .then(() => current === route && window.GeoBriefing.open({ opener }))
        .catch(() => {});
    } else if (['system', 'module', 'experiment'].includes(route.type) && !seen('geostat:hint:' + route.type)) {
      briefingAssets()
        .then(() => current === route && window.GeoBriefing.hint(route.type))
        .catch(() => {});
    }
  }
  // Audio: off unless the reader turns it on. The AudioContext is created inside the click that asks for
  // sound, as browsers require; the synthesiser (audio.js) is loaded only then.
  const audioToggle = document.getElementById('audio-toggle'),
    audioVolume = document.getElementById('audio-volume');
  let audioContext = null;
  const store = (key, value) => {
    try {
      localStorage.setItem(key, value);
    } catch {
      // The choice lasts for this visit only.
    }
  };
  const stored = key => {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  };
  function showAudio(on) {
    audioToggle.setAttribute('aria-pressed', String(on));
    audioVolume.hidden = !on;
  }
  function startAudio() {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    // 24 kHz halves the synthesis cost; the sounds have no content above 12 kHz.
    audioContext ||= new AC({ latencyHint: 'balanced', sampleRate: 24000 });
    audioContext.resume();
    loadData('audio.js', () => !!window.GeoAudio)
      .then(() => window.GeoAudio.enable(audioContext, audioVolume.value / 100))
      .catch(() => showAudio(false));
  }
  function setAudio(on) {
    store('geostat:audio', on ? 'on' : 'off');
    showAudio(on);
    if (on) startAudio();
    else window.GeoAudio?.disable();
  }
  audioToggle.addEventListener('click', () => setAudio(audioToggle.getAttribute('aria-pressed') !== 'true'));
  audioVolume.value = stored('geostat:audio-volume') ?? audioVolume.value;
  audioVolume.addEventListener('input', () => {
    store('geostat:audio-volume', audioVolume.value);
    window.GeoAudio?.setVolume(audioVolume.value / 100);
  });
  document.addEventListener('geostat:audio-choice', e => setAudio(e.detail.enabled));
  if (stored('geostat:audio') === 'on') {
    // A previous visit chose sound: it starts with the first interaction on this page.
    showAudio(true);
    const first = () => {
      document.removeEventListener('pointerdown', first, true);
      document.removeEventListener('keydown', first, true);
      if (audioToggle.getAttribute('aria-pressed') === 'true') startAudio();
    };
    document.addEventListener('pointerdown', first, true);
    document.addEventListener('keydown', first, true);
  }
  document.addEventListener('click', e => {
    const button = e.target.closest('[data-briefing]');
    if (!button) return;
    replayBriefing = button;
    if (current?.type === 'indice') firstVisit(current);
    else location.hash = '#indice';
  });
  function loadModule(id) {
    if (moduleCache[id]) return Promise.resolve(moduleCache[id]);
    if (pending[id]) return pending[id];
    pending[id] = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'assets/content/' + id + '.js';
      script.integrity = window.GEO_INTEGRITY['assets/content/' + id + '.js'];
      script.crossOrigin = 'anonymous';
      script.onload = () =>
        moduleCache[id] ? resolve(moduleCache[id]) : reject(new Error('Contenuto non disponibile'));
      script.onerror = () => {
        delete pending[id];
        reject(new Error('Impossibile aprire il modulo ' + id));
      };
      document.head.append(script);
    });
    return pending[id];
  }
  const link = (url, label, cls = '') => html`<a class="${cls}" href="${url}">${label}</a>`;
  function breadcrumbs(m, extra = '') {
    return html`<div class="breadcrumb">${link('#indice', 'Il corso')}<span>/</span>${link(route(m.id), html`${m.id} · ${m.title}`)}${extra ? html`<span>/</span><span>${extra}</span>` : ''}</div>`;
  }
  function moduleCard(m) {
    return html`<article class="module-card ${m.category === 'progetti' ? 'project' : ''}" data-module="${m.id}"><div class="card-top"><span class="code-tag">${m.id}</span><span class="card-kind">${m.category === 'progetti' ? 'Macroprogetto' : 'Modulo'}</span></div><h3>${link(route(m.id), html`${m.title}`)}</h3><p>${m.subtitle}</p>${
      m.category === 'progetti'
        ? html`<div class="project-parents" aria-label="Moduli preparatori"><span>Moduli preparatori</span>${window.GeoLabs.modulesForMission(
            m.id,
          ).map(id => link(route(id), id))}</div>`
        : ''
    }<div class="card-foot"><span>${m.category === 'progetti' ? 'Spedizione integrata' : window.GeoLabs.count(m.id) + ' esperimenti interattivi'}</span>${link(route(m.id), 'Apri ↗')}</div></article>`;
  }
  function catalogueSection(category) {
    return html`<section class="catalogue" id="catalogo"><div class="section-head"><h2>Il percorso del corso</h2><p>Dai fondamenti del calcolo alle analisi geologiche complete. Ogni modulo raccoglie esperimenti, formalismo e codice R eseguibile.</p></div><div class="filter-bar"><div class="filters" aria-label="Tipo di percorso">${[
      ['tutti', 'Tutto il corso'],
      ['moduli', 'Moduli'],
      ['progetti', 'Macroprogetti'],
    ].map(
      ([id, title]) => html`<button data-filter="${id}" aria-pressed="${category === id}">${title}</button>`,
    )}</div><label class="search"><span aria-hidden="true">⌕</span><input id="cerca-moduli" type="search" aria-label="Cerca modulo o argomento" placeholder="Cerca un modulo o un argomento"></label></div><p id="result-count" class="result-count" role="status"></p><div id="module-cards" class="cards"></div></section>`;
  }
  function fillCards(category, query) {
    const list = C.filterModules(catalog, query, category);
    document.getElementById('module-cards').innerHTML = html`${
      list.length ? html`${list.map(moduleCard)}` : html`<p class="empty">Nessun modulo corrisponde alla ricerca.</p>`
    }`;
    document.getElementById('result-count').textContent = list.length + ' unità didattiche';
    main
      .querySelectorAll('[data-filter]')
      .forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === category)));
    window.GeoSpace?.refresh();
  }
  function catalogueHome(type) {
    const category = type === 'progetti' ? 'progetti' : 'tutti';
    main.innerHTML = html`<div class="wrap">${category === 'progetti' ? '' : html`<h1 class="sr-only">Indice dei moduli</h1>`}<div class="breadcrumb">${link('#indice', 'Il corso')}<span>/</span><span>${category === 'progetti' ? 'Macroprogetti' : 'Indice dei moduli'}</span></div>${catalogueSection(category)}<section class="resource-band"><div><p class="eyebrow" style="color:var(--mint)">Materiali riproducibili</p><h2>Dalla pagina al calcolo.</h2><p>Le figure del corso sono accompagnate dai sorgenti R, i diagrammi dai file TikZ. Dati, convenzioni e verifiche rimangono disponibili insieme alle presentazioni.</p></div><div class="resource-links">${link('#materiali', html`Dati, codici e istruzioni <span aria-hidden="true">↗</span>`)}</div></section></div>`;
    let active = category;
    fillCards(active, '');
    main.querySelectorAll('[data-filter]').forEach(b =>
      b.addEventListener('click', () => {
        active = b.dataset.filter;
        fillCards(active, document.getElementById('cerca-moduli').value);
      }),
    );
    document.getElementById('cerca-moduli').addEventListener('input', e => fillCards(active, e.target.value));
  }
  const worlds = window.GeoPlanets;
  function planetSlot(id, cls = '', hero = 0) {
    const p = worlds.byId[id];
    return html`<div class="planet-slot ${p.rings ? 'ringed ' : ''}${cls}" data-planet="${id}" data-hero="${hero}" aria-hidden="true"></div>`;
  }
  function home(type) {
    if (type !== 'indice') {
      catalogueHome(type);
      if (type === 'progetti') {
        const intro = document.createElement('section');
        intro.className = 'project-intro';
        intro.innerHTML = html`<p class="eyebrow">SPEDIZIONI APPLICATIVE</p><h1>Porta i metodi sul campo.</h1><p class="lead">Undici indagini collegano i moduli del corso a problemi geologici, ambientali e territoriali. Ogni spedizione riunisce dati, analisi e materiali riproducibili.</p>`;
        main.querySelector('.catalogue').before(intro);
      }
      return;
    }
    window.GeoGalaxy.mount(main);
  }
  function codePage(m) {
    const choices = [
      ...(m.figureCode
        ? [{ id: 'figure', title: 'Analisi e figure · ' + m.id, code: m.figureCode, path: m.script, language: 'R' }]
        : []),
      ...m.laboratories,
    ];
    // Modules without scripts of their own (the expeditions) keep code and data in the project of the lesson.
    if (!choices.length) return location.replace('#lezione-' + m.id);
    if (!choices.some(x => x.id === selectedCode)) selectedCode = choices[0].id;
    main.innerHTML = html`${planetSlot(m.id, 'reading-planet', 0.15)}<div class="wrap">${breadcrumbs(m, 'Codici e laboratori')}<section class="module-head"><p class="eyebrow">${m.id} · Laboratorio</p><h1>Codici e materiali di lavoro</h1><p class="lead">${m.title}</p></section><div class="code-panel"><h2 class="sr-only">Script del modulo</h2><div class="code-top"><label class="sr-only" for="select-code">Scegli lo script</label><select id="select-code">${choices.map(
      x =>
        html`<option value="${x.id}"${x.id === selectedCode ? ' selected' : ''}>${x.id === 'figure' ? x.title : x.id + ' · ' + x.title}</option>`,
    )}</select><div class="code-actions"><button class="button small secondary" data-copy="current-code">Copia codice</button><a id="download-code" class="button small" download>Scarica script</a></div></div><p id="code-path" class="code-note"></p><pre tabindex="0" role="region" aria-label="Codice dello script selezionato"><code id="current-code"></code></pre><div class="notice"><h3>Riprodurre il calcolo</h3><p>Scarica <a href="assets/downloads/GeoStatLab_codice_dati.zip" download>l’archivio con codice e dati</a> e apri <code>materiali/Corso_Geologia.Rproj</code>. I percorsi degli script sono riferiti alla cartella <code>materiali/</code>. Il codice viene eseguito nell’ambiente R o Python indicato, con i dati e le dipendenze del corso.</p>${link('materiali/LEGGIMI.txt', 'Istruzioni e ambiente di esecuzione ↗')}</div></div></div>`;
    function select() {
      selectedCode = document.getElementById('select-code').value;
      const x = choices.find(x => x.id === selectedCode);
      document.getElementById('current-code').textContent = x.code;
      document.getElementById('code-path').textContent = x.path + ' · ' + x.language;
      document.getElementById('download-code').href = x.path;
    }
    document.getElementById('select-code').addEventListener('change', select);
    select();
    bindCopy();
  }
  function materials() {
    const external = config.repositoryUrl
      ? html`<p>${link(config.repositoryUrl, 'Apri il repository GitHub ↗')}</p>`
      : '';
    main.innerHTML = html`<div class="wrap resources-page"><p class="eyebrow">Consultazione e riproducibilità</p><h1>I materiali del corso</h1><p class="lead">Ogni lezione ha la propria presentazione, le tappe sul sito e i laboratori con gli stessi parametri. Gli esperimenti interattivi e i mini-progetti includono i programmi e i dati necessari a riprodurre le analisi.</p>${external}<div class="actions"><a class="button" href="assets/downloads/GeoStatLab_codice_dati.zip" download>Scarica codice e dati · ZIP ↓</a></div><div class="resources-grid"><section class="resource-card"><h2>Esperimenti interattivi</h2><p>${window.GEO_LABS.activities.length} programmi R autonomi, con parametri, funzioni grafiche e generatori dei dati. La mappa documenta il raccordo con le sezioni del corso.</p><ul><li><a href="assets/downloads/GeoStatLab_esperimenti_R.zip" download>Scarica i ${window.GEO_LABS.activities.length} esperimenti R · ZIP</a></li><li><a href="assets/downloads/GeoStatLab_mappa_esperimenti.csv" download>Mappa sezioni–esperimenti · CSV</a></li><li><a href="vendor/r-packages-lock.json">Versioni e impronte dei pacchetti R</a></li></ul></section><section class="resource-card"><h2>Presentazioni e percorso</h2><ul><li>${link('#catalogo', 'Indice delle lezioni e dei macroprogetti')}</li><li>${link('materiali/documentazione/catalogo_laboratori.csv', 'Catalogo dei laboratori · CSV')}</li></ul></section><section class="resource-card"><h2>Ambiente di lavoro</h2><p>Le figure sono generate in R; il modulo introduttivo conserva anche i laboratori Python. Gli script si eseguono dalla cartella materiali.</p><ul><li>${link('materiali/R/00_installazione.R', 'Installazione esplicita dei pacchetti R')}</li><li>${link('materiali/R/controlla_ambiente.R', 'Controllo dell’ambiente R')}</li><li>${link('materiali/verifiche/versioni_R.csv', 'Versioni dei pacchetti collaudati')}</li><li>${link('materiali/strumenti/requirements.txt', 'Dipendenze del percorso Python')}</li></ul></section><section class="resource-card"><h2>Provenienza e sorgenti</h2><p>Ogni modulo rimanda ai propri sorgenti R e LaTeX. Dati, figure e diagrammi mantengono gli identificativi del corso.</p><ul><li>${link('materiali/MANIFEST_SHA256.txt', 'Impronte dei materiali distribuiti')}</li><li>${link('LICENSE.md', 'Licenze: materiali CC BY-NC-SA 4.0, codice PolyForm Noncommercial 1.0.0')}</li><li>${link('LICENSE-CODE.md', 'Testo della licenza PolyForm Noncommercial 1.0.0')}</li><li>${link('THIRD_PARTY_NOTICES.md', 'Componenti e licenze')}</li></ul></section></div></div>`;
  }
  async function copyCode(button) {
    const text = document.getElementById(button.dataset.copy).textContent;
    try {
      if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(text);
      else {
        const t = document.createElement('textarea');
        t.value = text;
        t.className = 'sr-only';
        document.body.append(t);
        t.select();
        if (!document.execCommand('copy')) throw Error();
        t.remove();
        button.focus();
      }
      const old = button.textContent;
      button.textContent = 'Copiato';
      announce('Codice copiato');
      setTimeout(() => (button.textContent = old), 1800);
    } catch {
      announce('Copia non disponibile: seleziona il testo del codice.');
      button.textContent = 'Seleziona il codice';
    }
  }
  function bindCopy() {
    main.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', () => copyCode(b)));
  }
  let mathPromise;
  // A typeset formula wider than its column scrolls horizontally; keyboard users need a focus stop to scroll it.
  function scrollableFormulas(element) {
    for (const block of element.querySelectorAll('.math')) {
      if (block.scrollWidth <= block.clientWidth + 1 || block.hasAttribute('tabindex')) continue;
      block.tabIndex = 0;
      block.setAttribute('role', 'group');
      block.setAttribute('aria-label', 'Formula scorrevole in orizzontale');
    }
  }
  function typeset(element) {
    if (!mathPromise) {
      mathPromise = new Promise((resolve, reject) => {
        window.MathJax = {
          tex: {
            inlineMath: [
              ['$', '$'],
              ['\\(', '\\)'],
            ],
            displayMath: [['\\[', '\\]']],
            packages: ['base', 'ams', 'newcommand', 'configmacros', 'noundefined'],
            maxMacros: 2000,
            maxBuffer: 10000,
          },
          svg: { fontCache: 'local' },
          startup: { typeset: false },
          options: { enableMenu: false },
        };
        const script = document.createElement('script');
        script.src = 'vendor/mathjax/tex-svg.js';
        script.integrity = window.GEO_INTEGRITY['vendor/mathjax/tex-svg.js'];
        script.crossOrigin = 'anonymous';
        script.onload = () => window.MathJax.startup.promise.then(resolve, reject);
        script.onerror = reject;
        document.head.append(script);
      });
    }
    // A page left while MathJax was still composing it keeps no math items: they would retain the old page.
    mathPromise
      .then(() => {
        if (element.isConnected)
          return window.MathJax.typesetPromise([element]).then(() =>
            element.isConnected ? scrollableFormulas(element) : window.MathJax.typesetClear([element]),
          );
      })
      .catch(() => announce('Le formule complete sono consultabili nel PDF della lezione.'));
  }
  // Route types rendered from data already in memory; any other type is a module or code page.
  const views = {
    experiment: r => {
      const activity = window.GeoLabs.byId.get(r.activity);
      window.GeoLabs.experiment(main, activity, r.query);
      document.title = config.title + ' · ' + activity.title;
    },
    esperimenti: () => window.GeoLabs.index(main),
    mappa: () => window.GeoGalaxy.mount(main),
    system: r => window.GeoGalaxy.system(main, r.id, r.variant),
    object: r => {
      window.GeoObjectPages.render(main, r.object);
      const o = window.GeoObjects.byId[r.object];
      document.title = config.title + ' · ' + o.name + ' · ' + o.kind;
      announce(o.kind + ' ' + o.name);
    },
    exploration: r => {
      window.GeoExplorations.render(main, r.world, r.variant);
      typeset(main);
      const heading = main.querySelector('h1').textContent;
      document.title = config.title + ' · Esplorazione · ' + heading;
      announce('Esplorazione · ' + heading);
    },
    'taccuino-esplorazioni': () => {
      window.GeoExplorations.journal(main);
      document.title = config.title + ' · Taccuino delle esplorazioni';
      announce('Taccuino delle esplorazioni');
    },
    lesson: r => {
      const L = window.GEO_LESSONS[r.id];
      window.GeoLessons.lesson(main, L, r.page, announce);
      document.title = config.title + ' · ' + L.planet + (r.page ? ' · Tappa ' + r.page : ' · Lezione ' + r.id);
      announce(r.page ? 'Tappa ' + r.page + ' · ' + L.slides[r.page - 1].title : 'Lezione ' + r.id + ' · ' + L.title);
    },
    exercises: r => {
      window.GeoLessons.exercises(main, window.GEO_LESSONS[r.id], r.card, announce);
      const L = window.GEO_LESSONS[r.id];
      document.title =
        config.title +
        (L.exercises ? ' · Quaderno di ' + L.planet + ' · Esercizio ' + r.card : ' · Notebook di ' + L.planet);
      announce(L.exercises ? 'Esercizio ' + r.card : 'Notebook svolti di ' + L.planet);
    },
    taccuino: () => window.GeoNarrative.journal(main),
    indice: r => home(r.type),
    catalogo: r => home(r.type),
    progetti: r => home(r.type),
    materiali: () => materials(),
    notfound: () => {
      main.innerHTML = html`<section class="error"><h1>Pagina non trovata</h1><p>Il collegamento non corrisponde a un modulo o a una tappa del corso.</p>${link('#indice', 'Torna all’indice', 'button')}</section>`;
    },
  };
  // Lab details and worked solutions arrive before the views that read them; false if the route changed meanwhile.
  async function routeData(r, token) {
    if (r.type === 'lesson' || r.type === 'exercises') {
      if (!window.GEO_LESSONS?.[r.id]) main.innerHTML = html`<p class="loading">Apertura della lezione ${r.id}…</p>`;
      // The R engine reads the pinned packages and common functions from the laboratory details.
      await Promise.all([lessonData(r.id), labDetails()]);
      return token === renderId;
    }
    if (r.type !== 'experiment' && r.type !== 'exploration') return true;
    if (!window.GEO_LABS?.detailed && r.type === 'experiment')
      main.innerHTML = html`<p class="loading">Apertura del laboratorio…</p>`;
    await Promise.all([labDetails(), r.type === 'exploration' ? solutions() : null]);
    return token === renderId;
  }
  async function moduleView(r, token) {
    main.innerHTML = html`<p class="loading">Apertura del modulo ${r.id}…</p>`;
    const m = await loadModule(r.id);
    if (token !== renderId) return false;
    if (r.type === 'module' && m.category === 'progetti') {
      await Promise.all([labDetails(), solutions()]);
      if (token !== renderId) return false;
    }
    if (r.type === 'module') {
      if (m.category === 'progetti') window.GeoLabs.mission(main, m);
      else window.GeoLabs.module(main, m);
      lessonNotice(m);
    } else codePage(m);
    return true;
  }
  const companionText = l =>
    l.cards && l.notebooks
      ? ' Gli esercizi del quaderno e i ' + l.notebooks + ' notebook svolti sono sul pianeta compagno del sistema.'
      : l.cards
        ? ' Gli esercizi del quaderno sono sul pianeta compagno del sistema.'
        : l.notebooks
          ? ' I ' + l.notebooks + ' notebook svolti sono sul pianeta compagno del sistema.'
          : '';
  // Modules with a lesson point to its tappe, which replace the earlier slides.
  function lessonNotice(m) {
    const l = lessonIndex[m.id];
    if (!l) return;
    const box = document.createElement('section');
    box.className = 'lesson-notice';
    box.innerHTML = html`<p class="eyebrow">LEZIONE A TAPPE</p><h2>${l.planet}: ${l.title}</h2><p>Ognuna delle ${l.pages} slide della lezione ha una tappa sul sito, con il testo, il codice R eseguibile e i laboratori con gli stessi parametri.${companionText(l)}</p><div class="lab-actions"><a class="button" href="#lezione-${m.id}">Tappe della lezione →</a>${l.cards || l.notebooks ? html`<a class="button secondary" href="#esercizi-${m.id}">${l.cards ? 'Quaderno degli esercizi' : 'Notebook svolti'} →</a>` : ''}</div>`;
    (main.querySelector('.module-head') || main.firstElementChild)?.after(box);
  }
  function markNavigation(r) {
    document.querySelectorAll('.site-header nav a').forEach(a => {
      const active =
        a.getAttribute('href') === '#' + r.type ||
        (r.type === 'taccuino-esplorazioni' && a.getAttribute('href') === '#taccuino');
      if (active) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }
  function renderError(err) {
    main.innerHTML = html`<section class="error"><h1>Il modulo non è disponibile</h1><p>${err.message}</p><p>Verifica che l’intera cartella del sito sia stata copiata.</p>${link('#indice', 'Torna all’indice', 'button')}</section>`;
  }
  function cleanupViews() {
    for (const view of [
      window.GeoResearch,
      window.GeoLabs,
      window.GeoGalaxy,
      window.GeoBriefing,
      window.GeoLessons,
      window.GeoObjectPages,
    ])
      view?.cleanup();
  }
  function resolveRoute() {
    const r = window.GeoLabs?.parseHash(location.hash) || C.parseRoute(location.hash, catalog, lessonIndex);
    if (r.legacy) {
      history.replaceState(null, '', '#lezione-' + r.id);
      return { type: 'lesson', id: r.id, page: null };
    }
    // The companion world of a lesson hosts its exercises instead of the optional exploration.
    const companion = r.type === 'exploration' && window.GeoLessons?.forWorld(r.world);
    if (companion?.role !== 'exercises') return r;
    history.replaceState(null, '', '#esercizi-' + companion.id);
    return { type: 'exercises', id: companion.id, card: 1 };
  }
  async function render() {
    const token = ++renderId;
    current = resolveRoute();
    cleanupViews();
    if (window.MathJax?.typesetClear) window.MathJax.typesetClear([main]);
    document.title =
      config.title + ' · ' + (current.id ? catalog.find(m => m.id === current.id).title : config.subtitle);
    try {
      if (!(await routeData(current, token))) return;
      const view = Object.hasOwn(views, current.type) ? views[current.type] : null;
      if (view) view(current);
      else if (!(await moduleView(current, token))) return;
      window.scrollTo({ top: 0, behavior: 'instant' });
      window.GeoSpace?.onRoute(current);
      markNavigation(current);
      firstVisit(current);
    } catch (err) {
      renderError(err);
    }
  }
  // Arrow keys move between tappe as they move between slides.
  function stepLesson(e) {
    const n = (current.page || 1) + (e.key === 'ArrowRight' ? 1 : -1);
    if (!current.page || n < 1 || n > lessonIndex[current.id].pages) return;
    e.preventDefault();
    location.hash = '#lezione-' + current.id + '/' + n;
  }
  document.addEventListener('keydown', e => {
    if (
      current?.type !== 'lesson' ||
      e.defaultPrevented ||
      e.altKey ||
      e.ctrlKey ||
      e.metaKey ||
      /INPUT|SELECT|TEXTAREA/.test(e.target.tagName) ||
      e.target.isContentEditable
    )
      return;
    if (['ArrowLeft', 'ArrowRight'].includes(e.key)) stepLesson(e);
  });
  document.querySelector('.skip').addEventListener('click', event => {
    event.preventDefault();
    main.focus();
    main.scrollIntoView({ block: 'start' });
  });
  window.GeoLabs.configure({ typeset });
  window.GeoLessons?.configure({ typeset });
  window.addEventListener('hashchange', render);
  render();
})();
