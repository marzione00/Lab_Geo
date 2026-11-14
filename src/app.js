(function () {
  'use strict';
  const C = window.GeoCore,
    catalog = window.GEO_CATALOG.modules,
    config = window.GEO_CONFIG;
  const main = document.getElementById('contenuto'),
    announcer = document.getElementById('annuncio');
  const h = window.GeoHTML.escape;
  const route = (id, p) => '#modulo-' + id + (p ? '/slide/' + p : '');
  let storage;
  try {
    storage = window.localStorage;
  } catch {
    storage = null;
  }
  let progress = C.loadProgress(storage),
    current = null,
    view = 'slide',
    renderId = 0,
    selectedCode = 'figure';
  const moduleCache = (window.GEO_MODULES = window.GEO_MODULES || {}),
    pending = {};
  function announce(s) {
    announcer.textContent = s;
  }
  function persist() {
    C.saveProgress(storage, progress);
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
  const link = (url, label, cls = '') => '<a class="' + cls + '" href="' + h(url) + '">' + label + '</a>';
  function breadcrumbs(m, extra = '') {
    return (
      '<div class="breadcrumb">' +
      link('#indice', 'Il corso') +
      '<span>/</span>' +
      link(route(m.id), h(m.id) + ' · ' + h(m.title)) +
      (extra ? '<span>/</span><span>' + h(extra) + '</span>' : '') +
      '</div>'
    );
  }
  function moduleCard(m) {
    return (
      '<article class="module-card ' +
      (m.category === 'progetti' ? 'project' : '') +
      '" data-module="' +
      m.id +
      '"><div class="card-top"><span class="code-tag">' +
      m.id +
      '</span><span class="card-kind">' +
      (m.category === 'progetti' ? 'Macroprogetto' : 'Modulo') +
      '</span></div><h3>' +
      link(route(m.id), h(m.title)) +
      '</h3><p>' +
      h(m.subtitle) +
      '</p>' +
      (m.category === 'progetti'
        ? '<div class="project-parents" aria-label="Moduli preparatori"><span>Moduli preparatori</span>' +
          window.GeoLabs.modulesForMission(m.id)
            .map(id => link(route(id), id))
            .join('') +
          '</div>'
        : '') +
      '<div class="card-foot"><span>' +
      (m.category === 'progetti' ? 'Spedizione integrata' : window.GeoLabs.count(m.id) + ' esperimenti interattivi') +
      '</span>' +
      link(route(m.id), 'Apri ↗') +
      '</div></article>'
    );
  }
  function catalogueSection(category) {
    return (
      '<section class="catalogue" id="catalogo"><div class="section-head"><h2>Il percorso del corso</h2><p>Dai fondamenti del calcolo alle analisi geologiche complete. Ogni modulo raccoglie esperimenti, formalismo e codice R eseguibile.</p></div><div class="filter-bar"><div class="filters" aria-label="Tipo di percorso">' +
      [
        ['tutti', 'Tutto il corso'],
        ['moduli', 'Moduli'],
        ['progetti', 'Macroprogetti'],
      ]
        .map(
          ([id, title]) =>
            '<button data-filter="' + id + '" aria-pressed="' + (category === id) + '">' + title + '</button>',
        )
        .join('') +
      '</div><label class="search"><span aria-hidden="true">⌕</span><input id="cerca-moduli" type="search" aria-label="Cerca modulo o argomento" placeholder="Cerca un modulo o un argomento"></label></div><p id="result-count" class="result-count" role="status"></p><div id="module-cards" class="cards"></div></section>'
    );
  }
  function fillCards(category, query) {
    const list = C.filterModules(catalog, query, category);
    document.getElementById('module-cards').innerHTML = list.length
      ? list.map(moduleCard).join('')
      : '<p class="empty">Nessun modulo corrisponde alla ricerca.</p>';
    document.getElementById('result-count').textContent = list.length + ' unità didattiche';
    main
      .querySelectorAll('[data-filter]')
      .forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === category)));
    window.GeoSpace?.refresh();
  }
  function catalogueHome(type) {
    const category = type === 'progetti' ? 'progetti' : 'tutti';
    main.innerHTML =
      '<div class="wrap">' +
      (category === 'progetti' ? '' : '<h1 class="sr-only">Indice dei moduli</h1>') +
      '<div class="breadcrumb">' +
      link('#indice', 'Il corso') +
      '<span>/</span><span>' +
      (category === 'progetti' ? 'Macroprogetti' : 'Indice dei moduli') +
      '</span></div>' +
      catalogueSection(category) +
      '<section class="resource-band"><div><p class="eyebrow" style="color:var(--mint)">Materiali riproducibili</p><h2>Dalla pagina al calcolo.</h2><p>Le figure del corso sono accompagnate dai sorgenti R, i diagrammi dai file TikZ. Dati, convenzioni e verifiche rimangono disponibili insieme alle presentazioni.</p></div><div class="resource-links">' +
      link('#materiali', 'Dati, codici e istruzioni <span aria-hidden="true">↗</span>') +
      '</div></section></div>';
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
    return (
      '<div class="planet-slot ' +
      (p.rings ? 'ringed ' : '') +
      cls +
      '" data-planet="' +
      id +
      '" data-hero="' +
      hero +
      '" aria-hidden="true"></div>'
    );
  }
  function home(type) {
    if (type !== 'indice') {
      catalogueHome(type);
      if (type === 'progetti') {
        const intro = document.createElement('section');
        intro.className = 'project-intro';
        intro.innerHTML =
          '<p class="eyebrow">SPEDIZIONI APPLICATIVE</p><h1>Porta i metodi sul campo.</h1><p class="lead">Undici indagini collegano i moduli del corso a problemi geologici, ambientali e territoriali. Ogni spedizione riunisce dati, analisi e materiali riproducibili.</p>';
        main.querySelector('.catalogue').before(intro);
      }
      return;
    }
    window.GeoGalaxy.mount(main);
  }
  function toc(m, page) {
    let section = '';
    return (
      '<aside class="reader-sidebar" aria-label="Indice delle slide"><h2>' +
      m.id +
      ' · Indice</h2><input type="search" id="cerca-slide" aria-label="Cerca nell’indice del modulo" placeholder="Cerca una slide">' +
      m.slides
        .map(s => {
          const title = s.section !== section ? '<p class="toc-section">' + h(s.section) + '</p>' : '';
          section = s.section;
          return (
            title +
            '<a class="toc-link" href="' +
            route(m.id, s.page) +
            '" data-search="' +
            h(C.clean(s.title + ' ' + s.section)) +
            '"' +
            (s.page === page ? ' aria-current="page"' : '') +
            '><span>' +
            String(s.page).padStart(2, '0') +
            '</span><span>' +
            h(s.title) +
            '</span></a>'
          );
        })
        .join('') +
      '</aside>'
    );
  }
  function formula(s) {
    return s ? '<div class="math">\\[\\begin{gathered}' + h(s) + '\\end{gathered}\\]</div>' : '';
  }
  function reading(m, s) {
    return (
      '<article class="reading"><p>' +
      h(s.body) +
      '</p>' +
      formula(s.formula) +
      (s.aside ? '<div class="aside-text"><p>' + h(s.aside) + '</p></div>' : '') +
      formula(s.formulaAside) +
      (s.figure || s.diagram
        ? '<figure>' +
          (s.figure
            ? '<img src="assets/visuals/' +
              m.id +
              '/' +
              String(s.page).padStart(3, '0') +
              '.svg" alt="Rappresentazione della slide: ' +
              h(s.title) +
              '">'
            : '<svg class="reading-diagram" xmlns="http://www.w3.org/2000/svg" viewBox="328.819 77.953 211.181 212.598" role="img" aria-label="Diagramma: ' +
              h(s.title) +
              '"><image href="' +
              h(s.image) +
              '" width="566.93" height="354.33"/></svg>') +
          (s.caption
            ? '<figcaption' + (s.diagram ? ' class="sr-only"' : '') + '>' + h(s.caption) + '</figcaption>'
            : '') +
          '</figure>'
        : s.caption
          ? '<p>' + h(s.caption) + '</p>'
          : '') +
      (s.recall ? '<div class="recall"><strong>Richiamo.</strong> ' + h(s.recall) + '</div>' : '') +
      (s.kind === 'indice'
        ? '<ol>' + m.sections.map(x => '<li>' + link(route(m.id, x.page), h(x.title)) + '</li>').join('') + '</ol>'
        : '') +
      '</article>'
    );
  }
  function snippet(m, s) {
    const text = s.code || m.figureCode,
      path = s.codePath || m.script;
    return (
      '<section class="code-panel"><p class="code-note">' +
      (s.code
        ? 'Frammento riportato nella slide.'
        : 'Questa slide non contiene un frammento di codice; è disponibile lo script completo delle figure del modulo.') +
      '</p><div class="code-top"><strong>' +
      h(path) +
      '</strong><div class="code-actions"><button class="button small secondary" data-copy="current-code">Copia codice</button><a class="button small" href="' +
      h(path) +
      '" download>Scarica .R</a></div></div><pre><code id="current-code">' +
      h(text) +
      '</code></pre><p class="code-note">Esegui il codice in R dalla cartella <code>materiali/</code>, dopo aver installato le dipendenze indicate nella guida.</p></section>'
    );
  }
  function slidePanel(m, s) {
    const panel = document.getElementById('slide-panel');
    if (window.MathJax?.typesetClear) window.MathJax.typesetClear([panel]);
    if (view === 'testo') {
      panel.innerHTML = reading(m, s);
      typeset(panel);
    } else if (view === 'codice') {
      panel.innerHTML = snippet(m, s);
    } else {
      panel.innerHTML =
        '<div class="slide-frame"><img src="' +
        s.image +
        '" alt="' +
        h(m.id + ' · pagina ' + s.page + ' · ' + s.title) +
        '. Testo accessibile nella scheda Testo e formule."></div><div class="slide-caption"><span>Template originale · immagine vettoriale</span><a href="' +
        s.image +
        '" target="_blank" rel="noopener">Ingrandisci ↗</a><a href="' +
        m.pdf +
        '#page=' +
        s.page +
        '" target="_blank" rel="noopener">Apri nel PDF ↗</a></div>';
    }
    main.querySelectorAll('[data-view]').forEach(b => {
      b.setAttribute('aria-selected', String(b.dataset.view === view));
      b.tabIndex = b.dataset.view === view ? 0 : -1;
    });
    bindCopy();
  }
  function slidePage(m, page) {
    const s = m.slides[page - 1],
      key = m.id + ':' + page,
      done = progress.done.includes(key);
    progress.last = route(m.id, page);
    persist();
    main.innerHTML =
      planetSlot(m.id, 'reading-planet', 0.15) +
      '<div class="viewer">' +
      breadcrumbs(m, 'Slide ' + page) +
      '<div class="reader-layout">' +
      toc(m, page) +
      '<div class="reader-main"><div class="reader-title"><h1>' +
      h(s.title) +
      '</h1><span class="page-counter">' +
      String(page).padStart(2, '0') +
      ' / ' +
      m.pages +
      '</span></div><div class="reader-tools"><div class="tabs" role="tablist" aria-label="Modalità di lettura">' +
      [
        ['slide', 'Slide'],
        ['testo', 'Testo e formule'],
        ['codice', 'Codice R'],
      ]
        .map(
          ([id, label]) =>
            '<button role="tab" data-view="' +
            id +
            '" id="tab-' +
            id +
            '" aria-controls="slide-panel" aria-selected="' +
            (view === id) +
            '">' +
            label +
            '</button>',
        )
        .join('') +
      '</div><div class="pager"><button data-step="-1" aria-label="Slide precedente"' +
      (page === 1 ? ' disabled' : '') +
      '>←</button><button data-step="1" aria-label="Slide successiva"' +
      (page === m.pages ? ' disabled' : '') +
      '>→</button></div></div><div id="slide-panel" role="tabpanel" aria-labelledby="tab-' +
      view +
      '"></div><div class="study-actions"><button id="mark-done" class="button small secondary ' +
      (done ? 'done' : '') +
      '" aria-pressed="' +
      done +
      '">' +
      (done ? '✓ Segnata come studiata' : 'Segna come studiata') +
      '</button><p>Il progresso resta soltanto in questo browser.</p></div></div></div></div>';
    main.querySelectorAll('[data-view]').forEach(b =>
      b.addEventListener('click', () => {
        view = b.dataset.view;
        document.getElementById('slide-panel').setAttribute('aria-labelledby', 'tab-' + view);
        slidePanel(m, s);
      }),
    );
    main.querySelector('[role="tablist"]').addEventListener('keydown', e => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;
      e.preventDefault();
      e.stopPropagation();
      const tabs = [...main.querySelectorAll('[data-view]')],
        at = tabs.indexOf(document.activeElement);
      const next =
        e.key === 'Home'
          ? 0
          : e.key === 'End'
            ? tabs.length - 1
            : (at + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      tabs[next].click();
      tabs[next].focus();
    });
    main
      .querySelectorAll('[data-step]')
      .forEach(b => b.addEventListener('click', () => (location.hash = route(m.id, page + Number(b.dataset.step)))));
    document.getElementById('cerca-slide').addEventListener('input', e => {
      const q = C.clean(e.target.value);
      main.querySelectorAll('.toc-link').forEach(a => (a.hidden = !a.dataset.search.includes(q)));
    });
    document.getElementById('mark-done').addEventListener('click', e => {
      const isDone = progress.done.includes(key);
      progress.done = isDone ? progress.done.filter(x => x !== key) : [...progress.done, key];
      persist();
      e.currentTarget.classList.toggle('done', !isDone);
      e.currentTarget.setAttribute('aria-pressed', String(!isDone));
      e.currentTarget.textContent = isDone ? 'Segna come studiata' : '✓ Segnata come studiata';
      announce(isDone ? 'Segnalazione rimossa' : 'Pagina segnata come studiata');
    });
    slidePanel(m, s);
    const active = main.querySelector('.toc-link[aria-current="page"]');
    if (active) active.scrollIntoView({ block: 'nearest' });
  }
  function codePage(m) {
    const choices = [
      { id: 'figure', title: 'Analisi e figure · ' + m.id, code: m.figureCode, path: m.script, language: 'R' },
      ...m.laboratories,
    ];
    if (!choices.some(x => x.id === selectedCode)) selectedCode = 'figure';
    main.innerHTML =
      planetSlot(m.id, 'reading-planet', 0.15) +
      '<div class="wrap">' +
      breadcrumbs(m, 'Codici e laboratori') +
      '<section class="module-head"><p class="eyebrow">' +
      m.id +
      ' · Laboratorio</p><h1>Codici e materiali di lavoro</h1><p class="lead">' +
      h(m.title) +
      '</p></section><div class="code-panel"><h2 class="sr-only">Script del modulo</h2><div class="code-top"><label class="sr-only" for="select-code">Scegli lo script</label><select id="select-code">' +
      choices
        .map(
          x =>
            '<option value="' +
            x.id +
            '"' +
            (x.id === selectedCode ? ' selected' : '') +
            '>' +
            h(x.id === 'figure' ? x.title : x.id + ' · ' + x.title) +
            '</option>',
        )
        .join('') +
      '</select><div class="code-actions"><button class="button small secondary" data-copy="current-code">Copia codice</button><a id="download-code" class="button small" download>Scarica script</a></div></div><p id="code-path" class="code-note"></p><pre tabindex="0" role="region" aria-label="Codice dello script selezionato"><code id="current-code"></code></pre><div class="notice"><h3>Riprodurre il calcolo</h3><p>Scarica <a href="assets/downloads/GeoStatLab_codice_dati_R6.zip" download>l’archivio con codice e dati</a> e apri <code>materiali/Corso_Geologia.Rproj</code>. I percorsi degli script sono riferiti alla cartella <code>materiali/</code>. Il codice viene eseguito nell’ambiente R o Python indicato, con i dati e le dipendenze del corso.</p>' +
      link('materiali/Guida_corso_R6.pdf', 'Istruzioni e ambiente di esecuzione ↗') +
      '</div></div></div>';
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
      ? '<p>' + link(config.repositoryUrl, 'Apri il repository GitHub ↗') + '</p>'
      : '';
    main.innerHTML =
      '<div class="wrap resources-page"><p class="eyebrow">Consultazione e riproducibilità</p><h1>I materiali del corso</h1><p class="lead">Le presentazioni e i laboratori originali appartengono all’edizione R6 del corso. Gli esperimenti interattivi e i mini-progetti includono i programmi e i dati necessari a riprodurre le analisi.</p>' +
      external +
      '<div class="actions"><a class="button" href="assets/downloads/GeoStatLab_codice_dati_R6.zip" download>Scarica codice e dati · ZIP ↓</a></div><div class="resources-grid"><section class="resource-card"><h2>Esperimenti interattivi</h2><p>' +
      window.GEO_LABS.activities.length +
      ' programmi R autonomi, con parametri, funzioni grafiche e generatori dei dati. La mappa documenta il raccordo con le sezioni del corso.</p><ul><li><a href="assets/downloads/GeoStatLab_esperimenti_R.zip" download>Scarica i ' +
      window.GEO_LABS.activities.length +
      ' esperimenti R · ZIP</a></li><li><a href="assets/downloads/GeoStatLab_mappa_esperimenti.csv" download>Mappa sezioni–esperimenti · CSV</a></li><li><a href="vendor/r-packages-lock.json">Versioni e impronte dei pacchetti R</a></li></ul></section><section class="resource-card"><h2>Presentazioni e percorso</h2><ul><li>' +
      link('#catalogo', 'Indice dei 28 fascicoli') +
      '</li><li>' +
      link('materiali/Guida_corso_R6.pdf', 'Guida al corso e alla ricostruzione') +
      '</li><li>' +
      link('materiali/Guida_laboratori_M05.pdf', 'Laboratori M05: consegne e soluzioni') +
      '</li><li>' +
      link('materiali/documentazione/catalogo_laboratori.csv', 'Catalogo dei laboratori · CSV') +
      '</li></ul></section><section class="resource-card"><h2>Ambiente di lavoro</h2><p>Le figure sono generate in R; il modulo introduttivo conserva anche i laboratori Python. Gli script si eseguono dalla cartella materiali.</p><ul><li>' +
      link('materiali/R/00_installazione.R', 'Installazione esplicita dei pacchetti R') +
      '</li><li>' +
      link('materiali/R/controlla_ambiente.R', 'Controllo dell’ambiente R') +
      '</li><li>' +
      link('materiali/verifiche/versioni_R.csv', 'Versioni dei pacchetti collaudati') +
      '</li><li>' +
      link('materiali/strumenti/requirements.txt', 'Dipendenze del percorso Python') +
      '</li></ul></section><section class="resource-card"><h2>Provenienza e sorgenti</h2><p>Ogni modulo rimanda ai propri sorgenti R e LaTeX. Dati, figure e diagrammi mantengono gli identificativi del corso.</p><ul><li>' +
      link('materiali/documentazione/fonti_online_R6.json', 'Riferimenti bibliografici e documentazione') +
      '</li><li>' +
      link('materiali/documentazione/raccordo_slide.csv', 'Raccordo con le slide originali') +
      '</li><li>' +
      link('materiali/MANIFEST_SHA256.txt', 'Impronte dei materiali distribuiti') +
      '</li><li>' +
      link('THIRD_PARTY_NOTICES.md', 'Componenti e licenze') +
      '</li></ul></section></div></div>';
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
    mathPromise
      .then(() => {
        if (element.isConnected)
          return window.MathJax.typesetPromise([element]).then(() => scrollableFormulas(element));
      })
      .catch(() => announce('Le formule complete sono consultabili nella scheda Slide e nel PDF.'));
  }
  // Route types rendered from data already in memory; any other type is a module, slide or code page.
  const views = {
    experiment: r => {
      const activity = window.GeoLabs.byId.get(r.activity);
      window.GeoLabs.experiment(main, activity, r.query);
      document.title = config.title + ' · ' + activity.title;
    },
    esperimenti: () => window.GeoLabs.index(main),
    mappa: () => window.GeoGalaxy.mount(main),
    system: r => window.GeoGalaxy.system(main, r.id, r.variant),
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
    taccuino: () => window.GeoNarrative.journal(main),
    indice: r => home(r.type),
    catalogo: r => home(r.type),
    progetti: r => home(r.type),
    materiali: () => materials(),
    notfound: () => {
      main.innerHTML =
        '<section class="error"><h1>Pagina non trovata</h1><p>Il collegamento non corrisponde a un modulo o a una slide del corso.</p>' +
        link('#indice', 'Torna all’indice', 'button') +
        '</section>';
    },
  };
  // Lab details and worked solutions arrive before the views that read them; false if the route changed meanwhile.
  async function routeData(r, token) {
    if (r.type !== 'experiment' && r.type !== 'exploration') return true;
    if (!window.GEO_LABS?.detailed && r.type === 'experiment')
      main.innerHTML = '<p class="loading">Apertura del laboratorio…</p>';
    await Promise.all([labDetails(), r.type === 'exploration' ? solutions() : null]);
    return token === renderId;
  }
  async function moduleView(r, token) {
    main.innerHTML = '<p class="loading">Apertura del modulo ' + r.id + '…</p>';
    const m = await loadModule(r.id);
    if (token !== renderId) return false;
    if (r.type === 'module' && m.category === 'progetti') {
      await Promise.all([labDetails(), solutions()]);
      if (token !== renderId) return false;
    }
    if (r.type === 'module') {
      if (m.category === 'progetti') window.GeoLabs.mission(main, m);
      else window.GeoLabs.module(main, m);
    } else if (r.type === 'slide') slidePage(m, r.page);
    else codePage(m);
    return true;
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
    main.innerHTML =
      '<section class="error"><h1>Il modulo non è disponibile</h1><p>' +
      h(err.message) +
      '</p><p>Verifica che l’intera cartella del sito sia stata copiata.</p>' +
      link('#indice', 'Torna all’indice', 'button') +
      '</section>';
  }
  function cleanupViews() {
    for (const view of [window.GeoResearch, window.GeoLabs, window.GeoGalaxy, window.GeoBriefing]) view?.cleanup();
  }
  async function render() {
    const token = ++renderId;
    current = window.GeoLabs?.parseHash(location.hash) || C.parseRoute(location.hash, catalog);
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
  document.addEventListener('keydown', e => {
    if (
      current?.type !== 'slide' ||
      e.defaultPrevented ||
      e.altKey ||
      e.ctrlKey ||
      e.metaKey ||
      /INPUT|SELECT|TEXTAREA/.test(e.target.tagName) ||
      e.target.isContentEditable
    )
      return;
    if (!['ArrowLeft', 'ArrowRight'].includes(e.key)) return;
    const m = catalog.find(x => x.id === current.id),
      n = current.page + (e.key === 'ArrowRight' ? 1 : -1);
    if (n >= 1 && n <= m.pages) {
      e.preventDefault();
      location.hash = route(m.id, n);
    }
  });
  document.querySelector('.skip').addEventListener('click', event => {
    event.preventDefault();
    main.focus();
    main.scrollIntoView({ block: 'start' });
  });
  window.GeoLabs.configure({ typeset });
  window.addEventListener('hashchange', render);
  render();
})();
