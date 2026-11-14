(function (root) {
  'use strict';
  const D = root.GEO_LABS,
    E = root.GeoREngine,
    S = root.GeoSecurity,
    N = root.GeoNarrative;
  const activities = D.activities,
    byId = new Map(activities.map(a => [a.id, a]));
  const escape = root.GeoHTML.escape;
  const norm = s =>
    String(s)
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  const path = a => '#laboratorio/' + (typeof a === 'string' ? a : a.id);
  const modulePath = m => '#modulo-' + m;
  const listFor = id => activities.filter(a => a.module === id);
  let api = {},
    dispose = () => {};
  function configure(value) {
    api = value;
  }
  function cleanup() {
    dispose();
    dispose = () => {};
  }
  const planet = (id, cls = '') =>
    '<div class="planet-viewport" aria-hidden="true"><div class="planet-slot ' +
    (root.GeoPlanets.byId[id]?.rings ? 'ringed ' : '') +
    cls +
    '" data-planet="' +
    id +
    '" data-hero="0.35" aria-hidden="true"></div></div>';
  const link = (href, label, cls = '') => '<a class="' + cls + '" href="' + escape(href) + '">' + label + '</a>';
  const button = (id, label, secondary = false) =>
    '<button type="button" id="' +
    id +
    '" class="button' +
    (secondary ? ' secondary' : '') +
    '">' +
    label +
    '</button>';
  function card(a, index) {
    return (
      '<a class="experiment-card" href="' +
      path(a) +
      '"><span class="experiment-module">' +
      a.module +
      ' / ' +
      escape(root.GeoPlanets.byId[a.module].name) +
      '</span>' +
      (index !== undefined ? '<span class="activity-order">' + String(index + 1).padStart(2, '0') + '</span>' : '') +
      '<h3>' +
      escape(a.title) +
      '</h3><p>' +
      escape(a.goal) +
      '</p><span class="card-arrow">Apri l’esperimento →</span></a>'
    );
  }
  function index(main) {
    cleanup();
    main.innerHTML =
      '<div class="wrap"><section class="lab-index-intro"><p class="eyebrow">LABORATORI / STATISTICA E CODING R</p><h1>Un fenomeno da osservare.<br>Un modello da interrogare.</h1><p class="lead">' +
      activities.length +
      ' esperimenti collegano dati, rappresentazioni e formalismo matematico. Ogni configurazione può essere calcolata in R, confrontata con un’altra e riprodotta mediante il proprio codice.</p></section><div class="lab-index-tools"><label class="sr-only" for="search-experiments">Cerca un argomento o un esperimento</label><input id="search-experiments" type="search" placeholder="Cerca: bootstrap, PCA, chiavi, pendenza…"><label class="sr-only" for="filter-experiments">Filtra per modulo</label><select id="filter-experiments"><option value="all">Tutti i moduli</option>' +
      root.GEO_CATALOG.modules
        .filter(m => m.category !== 'progetti')
        .map(m => '<option value="' + m.id + '">' + m.id + ' · ' + escape(m.title) + '</option>')
        .join('') +
      '</select><div class="view-switch" role="group" aria-label="Presentazione"><button type="button" data-view="cards" aria-pressed="true">Schede</button><button type="button" data-view="list" aria-pressed="false">Elenco</button></div></div><p class="lab-count" id="experiment-count" role="status"></p><h2 class="sr-only">Elenco degli esperimenti</h2><div class="experiment-groups" id="experiment-grid"></div></div>';
    const fill = () => {
      const terms = norm(main.querySelector('#search-experiments').value).split(/\s+/).filter(Boolean),
        module = main.querySelector('#filter-experiments').value;
      const found = activities.filter(
        a =>
          (module === 'all' || a.module === module) &&
          terms.every(t => norm(a.module + ' ' + a.title + ' ' + a.goal + ' ' + a.sectionTitle).includes(t)),
      );
      // Grouped by module; groups open only when a search or a module filter narrows the list.
      const narrowed = terms.length > 0 || module !== 'all';
      const groups = root.GEO_CATALOG.modules
        .map(m => [m, found.filter(a => a.module === m.id)])
        .filter(([, items]) => items.length);
      main.querySelector('#experiment-grid').innerHTML =
        groups
          .map(
            ([m, items]) =>
              '<details class="experiment-group"' +
              (narrowed ? ' open' : '') +
              '><summary><span class="hud-label">' +
              m.id +
              ' · ' +
              escape(root.GeoPlanets.byId[m.id].name) +
              '</span><strong>' +
              escape(m.title) +
              '</strong><span class="experiment-group-count">' +
              items.length +
              (items.length === 1 ? ' esperimento' : ' esperimenti') +
              '</span></summary><div class="experiment-grid">' +
              items.map(a => card(a)).join('') +
              '</div></details>',
          )
          .join('') || '<p>Nessun esperimento corrisponde alla ricerca.</p>';
      main.querySelector('#experiment-count').textContent = found.length + ' esperimenti disponibili';
    };
    const groupsBox = main.querySelector('#experiment-grid');
    const setView = view => {
      groupsBox.classList.toggle('is-list', view === 'list');
      main
        .querySelectorAll('[data-view]')
        .forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === view)));
      try {
        localStorage.setItem('geostat:experiments-view', view);
      } catch {
        // Without storage the choice lasts for this visit only.
      }
    };
    main.querySelectorAll('[data-view]').forEach(b => b.addEventListener('click', () => setView(b.dataset.view)));
    let savedView = 'cards';
    try {
      savedView = localStorage.getItem('geostat:experiments-view') === 'list' ? 'list' : 'cards';
    } catch {
      // Storage unavailable: cards by default.
    }
    setView(savedView);
    main.querySelector('#search-experiments').addEventListener('input', fill);
    main.querySelector('#filter-experiments').addEventListener('change', fill);
    fill();
  }
  function materials(m) {
    return (
      '<details class="lab-module-materials"><summary>Materiali di consultazione e riferimenti</summary><p>Presentazione originale, sorgenti e laboratori del corso accompagnano gli esperimenti. Le fonti del corso permettono di approfondire il ragionamento e ricostruire i calcoli.</p><div class="actions">' +
      link(m.pdf, 'Presentazione PDF ↗', 'button secondary') +
      link('#modulo-' + m.id + '/codici', 'Codici del corso ↗', 'button secondary') +
      link('#modulo-' + m.id + '/slide/3', 'Lettura del fascicolo ↗', 'button secondary') +
      '</div></details>'
    );
  }
  function module(main, m) {
    cleanup();
    const items = listFor(m.id),
      p = root.GeoPlanets.byId[m.id];
    const coursePath =
      m.id === 'M05' && N
        ? N.data.sampling.stages
            .map(
              stage =>
                '<section class="narrative-stage"><h3>' +
                escape(stage.title) +
                '</h3><p>' +
                escape(stage.text) +
                '</p><div class="experiment-grid">' +
                stage.ids
                  .map(id =>
                    card(
                      byId.get(id),
                      items.findIndex(a => a.id === id),
                    ),
                  )
                  .join('') +
                '</div></section>',
            )
            .join('')
        : '<div class="experiment-grid">' + items.map(card).join('') + '</div>';
    main.innerHTML =
      '<div class="wrap"><div class="breadcrumb">' +
      link('#mappa', 'Atlante') +
      '<span>/</span>' +
      escape(m.id) +
      '</div><header class="lab-module-header">' +
      planet(m.id, 'module-planet') +
      (root.GeoPaths?.badge({ track: 'course', label: 'Modulo ' + m.id + ' · Corso' }) || '') +
      '<p class="planet-designation"><strong>' +
      escape(p.name.toUpperCase()) +
      '</strong><span>' +
      escape(p.description) +
      '</span></p><p class="eyebrow">' +
      m.id +
      ' / ' +
      items.length +
      ' ESPERIMENTI</p><h1>' +
      escape(m.title) +
      '</h1><p class="lead">' +
      escape(m.subtitle) +
      '.</p>' +
      (N?.moduleIntro(m.id) || '') +
      '<div class="actions">' +
      link(path(items[0]), 'Inizia il laboratorio →', 'button') +
      link('#esperimenti', 'Cerca un altro argomento', 'button secondary') +
      '</div></header><section class="lab-module-activities"><h2>Il percorso sperimentale</h2><p class="lead">Ogni attività dichiara il problema, le ipotesi e le grandezze che puoi modificare.</p>' +
      coursePath +
      '</section>' +
      materials(m) +
      '<div class="cross-nav">' +
      (m.previous ? link(modulePath(m.previous), '← ' + m.previous) : '<span></span>') +
      (m.next ? link(modulePath(m.next), m.next + ' →') : '') +
      '</div></div>';
  }
  const missions = {
    P01: {
      intro:
        'Confronta supporto delle misure, relazione statistica e sensibilità dell’analisi, ricostruendo un’argomentazione su porosità e permeabilità.',
      steps: [
        ['Definire l’unità', 'm01-estimando', 'm01-gerarchia'],
        ['Esaminare la relazione', 'm03-scale', 'm07-minimi-quadrati'],
        ['Valutare la stabilità', 'm07-influenza', 'm05-ricampionamento'],
      ],
    },
    P02: {
      intro:
        'Ricostruisci un confronto fra campagne, distinguendo numerosità delle misure e numero delle unità indipendenti.',
      steps: [
        ['Delimitare il confronto', 'm01-estimando', 'm02-aggregazioni'],
        ['Valutare l’incertezza', 'm06-contrasto', 'm05-ricampionamento'],
        ['Preparare una nuova raccolta', 'm01-disegno', 'm01-confronto-disegni'],
      ],
    },
    P03: {
      intro:
        'Esamina una variazione del livello di una serie idrologica, considerando il ruolo della dipendenza temporale.',
      steps: [
        ['Leggere la serie', 'm09-calendario', 'm09-smoothing'],
        ['Diagnosticare la dipendenza', 'm09-autocorrelazione', 'm09-differenze'],
        ['Sostenere la conclusione', 'm05-blocchi', 'm06-relazione'],
      ],
    },
    P04: {
      intro:
        'Distingui previsione della durata media e previsione di un nuovo evento, conservando una porzione separata per la verifica.',
      steps: [
        ['Separare stima e verifica', 'm07-validazione', 'm07-dominio'],
        ['Costruire il modello', 'm07-minimi-quadrati', 'm07-influenza'],
        ['Interpretare le previsioni', 'm07-previsione', 'm06-relazione'],
      ],
    },
    P05: {
      intro:
        'Separa variazioni stagionali e andamento di lungo periodo in una serie ambientale, verificando calendario e dipendenza.',
      steps: [
        ['Conservare il tempo', 'm09-calendario', 'm09-aggregazione'],
        ['Separare le componenti', 'm09-smoothing', 'm09-differenze'],
        ['Confrontare previsioni', 'm10-riferimenti', 'm10-arima'],
      ],
    },
    P06: {
      intro:
        'Valuta una previsione geografica nel settore non utilizzato per costruire il modello e documenta la copertura territoriale.',
      steps: [
        ['Definire la geometria', 'm11-coordinate', 'm11-copertura'],
        ['Esaminare la struttura', 'm11-vicinati', 'm11-variogramma'],
        ['Verificare altrove', 'm11-interpolazione', 'm11-kriging'],
      ],
    },
    P07: {
      intro:
        'Ricostruisci grandezze morfometriche a partire da un raster, verificando unità, risoluzione e dominio valido.',
      steps: [
        ['Verificare la griglia', 'm12-griglia', 'm12-maschere'],
        ['Derivare e rappresentare', 'm12-pendenza', 'm12-hillshade'],
        ['Valutare la sensibilità', 'm12-ricampionamento', 'm12-allineamento'],
      ],
    },
    P08: {
      intro:
        'Costruisci una cronologia di archivio e segui la propagazione delle incertezze nella datazione di un evento.',
      steps: [
        ['Stabilire le ancore', 'm13-ancore', 'm13-interpolazione'],
        ['Propagare l’incertezza', 'm13-incertezza', 'm13-durate'],
        ['Valutare interpretazioni alternative', 'm13-proxy', 'm13-hiatus'],
      ],
    },
    P09: {
      intro:
        'Stima un livello raro e discuti quanto la conclusione dipenda dalla lunghezza del record e dalla forma della coda.',
      steps: [
        ['Definire l’evento', 'm14-massimi', 'm14-episodi'],
        ['Stimare e ricampionare', 'm14-gumbel', 'm14-livelli-rari'],
        ['Interpretare il rischio', 'm14-gev', 'm14-ritorno', 'm14-conseguenze'],
      ],
    },
    P10: {
      intro:
        'Ricostruisci un’analisi verificabile, rendendo espliciti dati, dipendenze, criteri numerici e piano casuale.',
      steps: [
        ['Controllare i dati', 'm02-join', 'm02-tabella'],
        ['Verificare le funzioni', 'm15-contratti', 'm15-tolleranze'],
        ['Conservare la provenienza', 'm15-integrita', 'm15-provenienza'],
      ],
    },
    P11: {
      intro:
        'Valuta un classificatore su nuove stazioni, distinguendo geometria, probabilità previste e decisioni operative.',
      steps: [
        ['Definire il trasferimento', 'm16-bersaglio', 'm16-geometria'],
        ['Selezionare e addestrare', 'm16-selezione', 'm16-alberi'],
        ['Verificare probabilità e decisioni', 'm16-metriche', 'm16-trasferimento'],
      ],
    },
  };
  function modulesForMission(id) {
    return [
      ...new Set((missions[id]?.steps || []).flatMap(([, ...ids]) => ids.map(activity => byId.get(activity).module))),
    ];
  }
  function mission(main, m) {
    cleanup();
    const mission = missions[m.id];
    main.innerHTML =
      '<div class="wrap"><div class="breadcrumb">' +
      link('#progetti', 'Spedizioni') +
      '<span>/</span>' +
      m.id +
      '</div><header class="lab-module-header">' +
      planet(m.id, 'module-planet') +
      '<p class="eyebrow">SPEDIZIONE ' +
      m.id +
      '</p><h1>' +
      escape(m.title) +
      '</h1><p class="lead">' +
      escape(mission.intro) +
      '</p><p class="lab-footer-note">Gli esperimenti preparatori impiegano dati sintetici dichiarati. I dati e la consegna del caso applicativo sono disponibili nei materiali originali.</p></header><h2 class="sr-only">Fasi della spedizione</h2><div class="mission-stages">' +
      mission.steps
        .map(
          ([title, ...ids]) =>
            '<section class="mission-stage"><div><h3>' +
            escape(title) +
            '</h3>' +
            ids
              .map(id => {
                const a = byId.get(id);
                return '<p>' + escape(a.goal) + '</p>' + link(path(a), escape(a.title) + ' →');
              })
              .join('') +
            '</div></section>',
        )
        .join('') +
      '</div><section class="lab-reading"><h2>Relazione della spedizione</h2><p>Documenta il bersaglio dell’analisi, le unità indipendenti, le assunzioni e almeno un confronto di sensibilità. Esporta le configurazioni degli esperimenti utilizzati e collega la discussione ai dati del caso applicativo.</p></section><div class="course-solution"></div>' +
      materials(m) +
      '</div>';
    const solution = root.GeoSolutions.mountCourse(main.querySelector('.course-solution'), m.id);
    dispose = () => solution.destroy();
  }
  function validate(a, input) {
    return S.parameters(a, input);
  }
  function parseHash(hash) {
    if (typeof hash !== 'string' || hash.length > S.limits.query) return null;
    const m = /^#laboratorio\/([a-z0-9-]+)(?:\?(.*))?$/.exec(hash);
    if (!m) return null;
    const a = byId.get(m[1]);
    if (!a) return { type: 'notfound' };
    return { type: 'experiment', id: a.module, activity: a.id, query: m[2] || '' };
  }
  function controls(a, p) {
    return a.controls
      .map(
        c =>
          '<label class="lab-control" for="param-' +
          c.key +
          '"><span>' +
          escape(c.label) +
          '</span>' +
          (c.type === 'select'
            ? '<select id="param-' +
              c.key +
              '" data-param="' +
              c.key +
              '">' +
              c.options
                .map(
                  o =>
                    '<option value="' +
                    escape(o.value) +
                    '"' +
                    (o.value === p[c.key] ? ' selected' : '') +
                    '>' +
                    escape(o.label) +
                    '</option>',
                )
                .join('') +
              '</select>'
            : '<input id="param-' +
              c.key +
              '" data-param="' +
              c.key +
              '" type="number" min="' +
              c.min +
              '" max="' +
              c.max +
              '" step="' +
              c.step +
              '" value="' +
              p[c.key] +
              '">' +
              (c.key !== 'seed'
                ? '<input type="range" data-range="' +
                  c.key +
                  '" aria-label="' +
                  escape(c.label) +
                  ' · cursore" min="' +
                  c.min +
                  '" max="' +
                  c.max +
                  '" step="' +
                  c.step +
                  '" value="' +
                  p[c.key] +
                  '">'
                : '')) +
          (c.help ? '<small>' + escape(c.help) + '</small>' : '') +
          '</label>',
      )
      .join('');
  }
  function metricMarkup(result) {
    return (
      '<div class="lab-metrics">' +
      (result.metrics || [])
        .map(
          m =>
            '<div class="lab-metric"><span>' +
            escape(m.grandezza) +
            '</span><strong>' +
            escape(m.valore) +
            '</strong></div>',
        )
        .join('') +
      '</div>'
    );
  }
  function tableMarkup(result) {
    const rows = result.data || [],
      keys = Object.keys(rows[0] || {});
    return (
      '<details class="lab-data"><summary>Tabella dei risultati · ' +
      escape(result.rows ?? rows.length) +
      ' righe</summary><p class="lab-footer-note">Anteprima delle prime ' +
      rows.length +
      ' righe. L’esportazione CSV dopo il calcolo contiene l’intera tabella dell’esperimento.</p><div class="lab-table-scroll"><table><thead><tr>' +
      keys.map(k => '<th scope="col">' + escape(k) + '</th>').join('') +
      '</tr></thead><tbody>' +
      rows
        .map(r => '<tr>' + keys.map(k => '<td>' + escape(r[k] === null ? 'NA' : r[k]) + '</td>').join('') + '</tr>')
        .join('') +
      '</tbody></table></div></details>'
    );
  }
  function download(name, text, type = 'text/plain;charset=utf-8') {
    const blob = text instanceof Blob ? text : new Blob([text], { type });
    const url = URL.createObjectURL(blob),
      a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.append(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  }
  function savedNotes(id) {
    try {
      return (localStorage.getItem('geostat-lab-notes:' + id) || '').slice(0, S.limits.notes);
    } catch {
      return '';
    }
  }
  function typeset(el) {
    api.typeset?.(el);
  }
  function labMarkup(a, params, items, pos, m, narrated) {
    return (
      '<div class="wrap lab-shell"><div class="breadcrumb">' +
      link('#esperimenti', 'Esperimenti') +
      '<span>/</span>' +
      link(modulePath(a.module), escape(a.module + ' · ' + m.title)) +
      '</div><header class="lab-activity-head">' +
      planet(a.module) +
      (root.GeoPaths?.badge({ track: 'course', label: 'Modulo ' + a.module + ' · Corso' }) || '') +
      '<p class="lab-location">' +
      escape(root.GeoPlanets.byId[a.module].name.toUpperCase()) +
      ' / ' +
      String(pos + 1).padStart(2, '0') +
      ' DI ' +
      items.length +
      '</p><h1>' +
      escape(a.title) +
      '</h1><p class="lead">' +
      escape(a.goal) +
      '</p></header>' +
      (N?.scene(a) || '') +
      '<div class="lab-mode-bar" role="group" aria-label="Modalità di studio"><button data-mode="guided" aria-pressed="true">Percorso guidato</button><button data-mode="explore" aria-pressed="false">Esplorazione libera</button><button data-mode="formal" aria-pressed="false">Formalismo e codice</button></div><div class="lab-layout"><aside class="lab-control-panel" aria-label="Preparazione dell’esperimento"><h2>Prepara l’esperimento</h2><div class="lab-controls">' +
      controls(a, params) +
      '</div><label class="lab-auto"><input id="lab-auto" type="checkbox" checked>Ricalcola quando modifico i parametri</label>' +
      button('lab-run', 'Esegui in R →') +
      button('lab-stop', 'Interrompi il calcolo', true) +
      '<div class="lab-control-footer"><button id="lab-reset" class="lab-text-button">Ripristina</button><button id="lab-new-seed" class="lab-text-button">Nuovo campione</button></div><p class="lab-footer-note">Il seme rimane fisso quando cambi gli altri parametri. R esegue il calcolo su questo dispositivo.</p></aside><div class="lab-results"><div class="lab-engine-state" id="lab-engine-state" role="status" aria-live="polite"></div><div id="lab-error" class="lab-error" role="alert" hidden></div><section class="lab-reading lab-guided" id="lab-guided"><span class="lab-step-no">1</span><div><h2 class="lab-step-title">Previsione e confronto</h2><p>' +
      escape(narrated ? N.prediction(a) : a.action) +
      '</p>' +
      (narrated ? '<p>' + escape(a.action) + '</p>' : '') +
      '<details class="lab-note-disclosure"><summary>Annota una previsione e le tue osservazioni</summary><label class="lab-note-label" for="lab-notes">Previsione, osservazioni e interpretazione</label><textarea class="lab-notes" id="lab-notes" maxlength="20000" placeholder="Registra una previsione prima di eseguire il confronto…">' +
      escape(savedNotes(a.id)) +
      '</textarea><p class="lab-footer-note">Appunti conservati soltanto in questo browser.</p></details></div></section><p class="lab-pending" id="lab-pending" hidden>La configurazione è cambiata. I risultati visibili si riferiscono al calcolo precedente.</p><div id="lab-result-body" class="lab-result-body"><p class="lab-result-meta" id="lab-result-meta">Apertura della configurazione iniziale verificata in R…</p><div id="lab-metrics"></div><div id="lab-plots"></div><div id="lab-data"></div></div><div class="lab-actions">' +
      button('lab-compare', 'Conserva scenario A', true) +
      button('lab-export-csv', 'Scarica dati CSV', true) +
      button('lab-export-config', 'Esporta configurazione', true) +
      button('lab-import-config', 'Importa configurazione', true) +
      button('lab-share', 'Copia collegamento', true) +
      '<input id="lab-import-file" type="file" accept="application/json,.json" hidden></div><section id="lab-compare-panel" class="lab-reading" hidden><h2>Confronto fra scenari</h2><p id="narrative-comparison" hidden></p><div id="lab-comparison" class="lab-comparison"></div><button id="lab-clear-compare" class="lab-text-button">Svuota il confronto</button></section><section id="lab-interpretation" class="lab-reading lab-guided"><span class="lab-step-no">2</span><div><h3>Interpretare il risultato</h3>' +
      (narrated
        ? '<div class="narrative-result" id="narrative-result" hidden><p class="eyebrow">LETTURA DELLA CONFIGURAZIONE</p><p id="narrative-result-text"></p></div>'
        : '') +
      '<p>' +
      escape(a.conclusion) +
      '</p><p>' +
      escape(a.limits) +
      '</p>' +
      (narrated
        ? '<div class="narrative-journal-actions"><button type="button" id="save-fieldbook" class="button secondary" disabled>Conserva nel taccuino</button><a href="#taccuino">Rileggi il taccuino →</a><p id="fieldbook-status" role="status">Esegui il modello originale in R per documentare la configurazione.</p></div>'
        : '') +
      '</div></section><section class="lab-reading" id="lab-theory"><h2>Modello e formalismo</h2><div class="math">\\[' +
      escape(a.formula) +
      '\\]</div><p class="lab-math-definitions">' +
      escape(a.symbols) +
      '</p>' +
      a.prose.map(p => '<p>' + escape(p) + '</p>').join('') +
      '<p>' +
      link('#modulo-' + a.module + '/slide/' + a.page, 'Approfondimento nel materiale del corso ↗') +
      '</p></section><section class="lab-code-panel" id="lab-code-panel" hidden><h2>Ricostruire il calcolo in R</h2><p>Il codice seguente è quello eseguito dall’esperimento. <code>p</code> contiene i parametri del pannello; le funzioni grafiche comuni sono incluse nello script autonomo scaricabile. Puoi modificare il corpo del calcolo e rieseguirlo. Esegui soltanto codice di cui conosci la provenienza: il browser non costituisce un ambiente adatto ad analizzare programmi ostili.</p><pre class="lab-code-output" id="lab-params-code"></pre><label class="sr-only" for="lab-code-editor">Codice R dell’esperimento</label><textarea class="lab-editor" id="lab-code-editor" maxlength="100000" spellcheck="false">' +
      escape(a.code) +
      '</textarea><div class="lab-actions">' +
      button('lab-run-code', 'Esegui codice modificato') +
      button('lab-download-r', 'Scarica script R completo', true) +
      button('lab-reset-code', 'Ripristina codice', true) +
      '</div><p class="lab-footer-note">Il codice deve produrre <code>data</code> (tabella), <code>metrics</code> (riepilogo) e <code>plots</code> (lista di grafici ggplot). Un calcolo lungo può essere interrotto riavviando il motore.</p></section><div class="lab-actions" id="lab-quick-r">' +
      button('lab-download-r-quick', 'Scarica lo script R della configurazione', true) +
      '</div><p class="lab-footer-note">Dati sintetici · formule e ipotesi dichiarate · figure prodotte con ggplot2. ' +
      (narrated
        ? 'Le figure vengono prodotte dopo l’esecuzione del calcolo in R.'
        : 'La figura iniziale proviene dal collaudo R; ogni modifica viene ricalcolata dall’interprete.') +
      '</p></div></div>' +
      (N?.bridge(a) || '') +
      '<nav class="lab-bottom-nav" aria-label="Attività successive">' +
      (pos > 0
        ? link(path(items[pos - 1]), '← ' + escape(items[pos - 1].title))
        : link(modulePath(a.module), '← Indice del pianeta')) +
      (pos < items.length - 1
        ? link(path(items[pos + 1]), escape(items[pos + 1].title) + ' →')
        : link('#mappa', 'Torna all’atlante →')) +
      '</nav></div>'
    );
  }
  function initialParams(a, query) {
    const defaults = () => Object.fromEntries(a.controls.map(c => [c.key, c.value]));
    try {
      const cfg = new URLSearchParams(query).get('c');
      return { params: cfg ? validate(a, S.parseJSON(cfg, S.limits.query)) : defaults(), configError: null };
    } catch (err) {
      return {
        params: defaults(),
        configError: 'Configurazione del collegamento non valida: sono stati ripristinati i parametri iniziali.',
      };
    }
  }
  function experiment(main, a, query = '') {
    cleanup();
    let { params, configError } = initialParams(a, query);
    let active = true,
      mode = 'guided',
      result = null,
      resultParams = null,
      resultBody = null,
      custom = a.code,
      approvedCode = a.code,
      request = 0,
      timer = null,
      compare = [],
      urls = [],
      compareUrls = [],
      computed = false;
    const items = listFor(a.module),
      pos = items.findIndex(x => x.id === a.id),
      m = root.GEO_CATALOG.modules.find(m => m.id === a.module),
      narrated = !!N?.has(a.id);
    main.innerHTML = labMarkup(a, params, items, pos, m, narrated);
    const $ = s => main.querySelector(s);
    let terminal = null;
    if (root.GeoCodeGuide) {
      const output = $('#lab-result-body'),
        actions = output.nextElementSibling,
        workbench = document.createElement('div'),
        observation = document.createElement('div'),
        consolePanel = document.createElement('section');
      workbench.className = 'lab-code-workbench';
      observation.className = 'lab-observation';
      output.before(workbench);
      observation.append($('#lab-pending'), output, actions);
      workbench.append(observation, consolePanel);
      terminal = root.GeoCodeGuide.mount(consolePanel, a, params, {
        download: () => saveR(),
        edit: () => {
          setMode('formal');
          $('#lab-code-panel').scrollIntoView({ block: 'start' });
          $('#lab-code-editor').focus({ preventScroll: true });
        },
      });
    }
    if (narrated) $('#narrative-scene').after($('#lab-guided'));
    for (const id of ['#lab-compare', '#lab-export-csv', '#lab-export-config']) $(id).disabled = true;
    const unsub = E.subscribe(state => {
      if (!active) return;
      const el = $('#lab-engine-state');
      el.textContent = state.text;
      el.dataset.phase = state.phase;
      $('#lab-stop').hidden = !['loading', 'running'].includes(state.phase);
    });
    function error(err) {
      if (!active) return;
      $('#lab-error').hidden = false;
      $('#lab-error').textContent = String(err?.message || err);
    }
    function updateParamsCode() {
      $('#lab-params-code').textContent = E.paramsCode(params) + '\nset.seed(p$seed)';
      terminal?.update(params, custom);
    }
    function stale(value) {
      $('#lab-pending').hidden = !value;
      $('#lab-result-body').dataset.stale = String(value);
      $('#lab-export-csv').disabled = value || !computed;
      $('#lab-compare').disabled = value || !result;
      $('#lab-export-config').disabled = value || !result;
      if (narrated) {
        $('#narrative-result').hidden = value || !result;
        $('#save-fieldbook').disabled = value || !computed || resultBody !== a.code;
      }
    }
    function markDirty() {
      const changedConfig =
        Boolean(result) && (JSON.stringify(params) !== JSON.stringify(resultParams) || custom !== resultBody);
      stale(true);
      // Only results of a different configuration are dimmed. The verified preview of the configuration on
      // screen stays legible while R recomputes it; before, its dimming depended on which request finished first.
      $('#lab-result-body').dataset.changed = String(changedConfig);
      $('#lab-pending').textContent = changedConfig
        ? 'La configurazione è cambiata. I risultati visibili si riferiscono al calcolo precedente.'
        : 'Calcolo R in corso per la configurazione mostrata.';
      updateParamsCode();
    }
    function sync() {
      for (const c of a.controls) {
        $('#param-' + c.key).value = params[c.key];
        const r = $('[data-range="' + c.key + '"]');
        if (r) r.value = params[c.key];
      }
      updateParamsCode();
    }
    function showResult(r, p, body, live) {
      if (!active) return;
      if (live) {
        S.result(r);
        r = { ...r, figures: r.figures.map(S.svg) };
      }
      urls.forEach(u => URL.revokeObjectURL(u));
      urls = [];
      result = r;
      resultParams = { ...p };
      resultBody = body;
      computed = live;
      $('#lab-metrics').innerHTML = metricMarkup(r);
      const figures = r.figures || r.previewFigures || [];
      $('#lab-plots').innerHTML = figures
        .map((svg, i) => {
          const url = live ? URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' })) : svg;
          if (live) urls.push(url);
          return (
            '<figure class="lab-chart"><img src="' +
            escape(url) +
            '" alt="' +
            escape(a.title) +
            ' · figura ' +
            (i + 1) +
            '" loading="eager"><figcaption>Figura ' +
            (i + 1) +
            ' · ' +
            escape(live ? 'Ricalcolata con ggplot2 ' + r.ggplot2 : 'Configurazione iniziale verificata in R') +
            ' · <a href="' +
            escape(url) +
            '" download="' +
            a.id +
            '-' +
            (i + 1) +
            '.svg">Scarica SVG</a></figcaption></figure>'
          );
        })
        .join('');
      $('#lab-data').innerHTML = tableMarkup(r);
      $('#lab-result-meta').textContent =
        (live ? 'CALCOLO R COMPLETATO' : 'CONFIGURAZIONE INIZIALE') +
        ' · seme ' +
        p.seed +
        ' · ' +
        r.R +
        ' · ggplot2 ' +
        r.ggplot2;
      if (narrated) $('#narrative-result-text').textContent = N.reading(a.id, p, r, body === a.code);
      stale(false);
      $('#lab-export-csv').disabled = !live;
      if (narrated)
        $('#fieldbook-status').textContent =
          body !== a.code
            ? 'Il taccuino guidato documenta il modello originale; esporta la configurazione per conservare il codice personalizzato.'
            : live
              ? 'Puoi conservare questa configurazione, gli scenari confrontati e le tue osservazioni.'
              : 'Esegui il modello in R prima di documentarlo.';
    }
    async function execute() {
      const token = ++request;
      clearTimeout(timer);
      $('#lab-error').hidden = true;
      let p;
      try {
        p = validate(a, params);
      } catch (err) {
        error(err);
        return;
      }
      const body = custom;
      if (body !== approvedCode) {
        error(
          'Il codice è stato modificato o importato. Controllalo nella scheda Formalismo e codice, poi premi Esegui codice modificato.',
        );
        return;
      }
      markDirty();
      root.GeoCore?.cue('r-start');
      try {
        await E.init();
        if (!active || token !== request) return;
        const r = await E.run(a, p, body);
        if (!active || token !== request) return;
        showResult(r, p, body, true);
        root.GeoCore?.cue('r-done');
        try {
          localStorage.setItem('geostat-last-experiment', path(a));
        } catch {
          /* the resume link is optional */
        }
      } catch (err) {
        root.GeoCore?.cue('r-error');
        if (active && token === request) error(err);
      }
    }
    function changed(key, value) {
      request++;
      params[key] = value;
      markDirty();
      if ($('#lab-auto').checked) {
        clearTimeout(timer);
        timer = setTimeout(execute, 650);
      }
    }
    main.querySelectorAll('[data-param]').forEach(el =>
      el.addEventListener(el.tagName === 'SELECT' ? 'change' : 'input', () => {
        const c = a.controls.find(c => c.key === el.dataset.param);
        const v = c.type === 'select' ? el.value : el.value === '' ? NaN : Number(el.value);
        const range = $('[data-range="' + c.key + '"]');
        if (range) range.value = v;
        changed(c.key, v);
      }),
    );
    main.querySelectorAll('[data-range]').forEach(el =>
      el.addEventListener('input', () => {
        $('#param-' + el.dataset.range).value = el.value;
        changed(el.dataset.range, Number(el.value));
      }),
    );
    $('#lab-run').addEventListener('click', execute);
    $('#lab-stop').addEventListener('click', () => {
      request++;
      E.reset();
      markDirty();
    });
    $('#lab-reset').addEventListener('click', () => {
      params = Object.fromEntries(a.controls.map(c => [c.key, c.value]));
      custom = a.code;
      approvedCode = a.code;
      E.reset();
      $('#lab-code-editor').value = custom;
      sync();
      execute();
    });
    $('#lab-new-seed').addEventListener('click', () => {
      params.seed = params.seed >= 99999 ? 1 : params.seed + 1;
      sync();
      execute();
    });
    if (narrated)
      $('#save-fieldbook').addEventListener('click', () => {
        if (!computed || !result || resultBody !== a.code || $('#lab-result-body').dataset.stale === 'true') return;
        const saved = N.save(a, resultParams, result, $('#lab-notes').value, compare);
        $('#fieldbook-status').textContent = saved
          ? 'Configurazione e osservazioni conservate. Una nuova registrazione aggiornerà questa attività.'
          : 'Il browser non ha conservato la registrazione. Usa Esporta configurazione per scaricare una copia.';
      });
    $('#lab-notes').addEventListener('input', () => {
      try {
        localStorage.setItem('geostat-lab-notes:' + a.id, $('#lab-notes').value);
      } catch {
        $('#fieldbook-status').textContent =
          'Il browser non conserva gli appunti. Usa Esporta configurazione per salvarne una copia.';
      }
    });
    function setMode(value) {
      mode = value;
      main
        .querySelectorAll('[data-mode]')
        .forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
      $('#lab-guided').hidden = mode !== 'guided';
      $('#lab-interpretation').hidden = mode === 'formal';
      $('#lab-theory').hidden = mode === 'explore';
      $('#lab-code-panel').hidden = mode !== 'formal';
      if (narrated) $('#narrative-scene').hidden = mode !== 'guided';
      $('#lab-quick-r').hidden = mode === 'formal';
      if (mode === 'formal') typeset($('#lab-theory'));
    }
    main.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));
    $('#lab-run-code').addEventListener('click', () => {
      custom = $('#lab-code-editor').value;
      approvedCode = custom;
      execute();
    });
    $('#lab-code-editor').addEventListener('input', () => {
      request++;
      custom = $('#lab-code-editor').value;
      markDirty();
    });
    $('#lab-reset-code').addEventListener('click', () => {
      custom = a.code;
      approvedCode = a.code;
      E.reset();
      $('#lab-code-editor').value = custom;
      execute();
    });
    const saveR = () => download(a.id + '.R', E.script(a, validate(a, params), custom));
    $('#lab-download-r').addEventListener('click', saveR);
    $('#lab-download-r-quick').addEventListener('click', saveR);
    $('#lab-export-csv').addEventListener('click', () => {
      if (computed && result?.csv) download(a.id + '-dati.csv', S.csv(result.csv), 'text/csv;charset=utf-8');
    });
    $('#lab-export-config').addEventListener('click', () => {
      if (!result) return;
      download(
        a.id + '-configurazione.json',
        JSON.stringify(
          {
            application: 'GeoStatLab',
            version: 1,
            activity: a.id,
            parameters: resultParams,
            code: resultBody,
            notes: $('#lab-notes').value,
            engine: { R: result.R, ggplot2: result.ggplot2 },
            metrics: result.metrics,
            data: result.data,
            rows: result.rows,
          },
          null,
          2,
        ),
        'application/json',
      );
    });
    $('#lab-import-config').addEventListener('click', () => $('#lab-import-file').click());
    $('#lab-import-file').addEventListener('change', async e => {
      const f = e.target.files[0];
      if (!f) return;
      try {
        if (f.size > S.limits.config) throw Error('La configurazione supera 2 MB.');
        const value = S.configuration(a, await f.text());
        if (!active) return;
        request++;
        clearTimeout(timer);
        E.reset();
        params = value.parameters;
        custom = value.code;
        approvedCode = a.code;
        $('#lab-code-editor').value = custom;
        $('#lab-notes').value = value.notes;
        sync();
        if (custom !== a.code) {
          $('#lab-auto').checked = false;
          setMode('formal');
          markDirty();
          error(
            'È stato importato codice personalizzato. Leggilo, quindi premi Esegui codice modificato. Il ricalcolo automatico è disattivato.',
          );
        } else execute();
      } catch (err) {
        error(err);
      } finally {
        e.target.value = '';
      }
    });
    $('#lab-share').addEventListener('click', async () => {
      try {
        if (custom !== a.code)
          throw Error(
            'Per conservare codice personalizzato, esporta la configurazione JSON o lo script R. Il collegamento include i parametri del codice standard.',
          );
        const url =
          location.href.split('#')[0] + path(a) + '?c=' + encodeURIComponent(JSON.stringify(validate(a, params)));
        await navigator.clipboard.writeText(url);
        $('#lab-share').textContent = 'Collegamento copiato';
        setTimeout(() => {
          if (active) $('#lab-share').textContent = 'Copia collegamento';
        }, 1800);
      } catch (err) {
        error(err);
      }
    });
    function showCompare() {
      if (narrated) {
        const el = $('#narrative-comparison');
        el.textContent = N.comparison(a, compare);
        el.hidden = !el.textContent;
      }
      compareUrls.forEach(u => URL.revokeObjectURL(u));
      compareUrls = [];
      const panel = $('#lab-compare-panel');
      panel.hidden = !compare.length;
      $('#lab-comparison').innerHTML = compare
        .map(
          (v, i) =>
            '<article><h3>Scenario ' +
            String.fromCharCode(65 + i) +
            '</h3>' +
            metricMarkup(v.result) +
            (v.result.figures || v.result.previewFigures || [])
              .map((svg, j) => {
                const url = v.result.figures ? URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' })) : svg;
                if (v.result.figures) compareUrls.push(url);
                return (
                  '<figure class="lab-chart"><img src="' +
                  escape(url) +
                  '" alt="Scenario ' +
                  String.fromCharCode(65 + i) +
                  ' · figura ' +
                  (j + 1) +
                  '"></figure>'
                );
              })
              .join('') +
            '<pre>' +
            escape(E.paramsCode(v.params)) +
            '</pre></article>',
        )
        .join('');
      $('#lab-compare').textContent = compare.length ? 'Conserva scenario B' : 'Conserva scenario A';
    }
    $('#lab-compare').addEventListener('click', () => {
      if (result) {
        if (compare.length >= 2) compare = [];
        compare.push({
          params: { ...resultParams },
          standard: resultBody === a.code,
          result: JSON.parse(JSON.stringify(result)),
        });
        showCompare();
      }
    });
    $('#lab-clear-compare').addEventListener('click', () => {
      compare = [];
      showCompare();
    });
    updateParamsCode();
    setMode('guided');
    typeset($('#lab-theory'));
    const defaultParams = Object.fromEntries(a.controls.map(c => [c.key, c.value]));
    const isDefault = JSON.stringify(params) === JSON.stringify(defaultParams);
    if (isDefault && !narrated)
      fetch('assets/experiments/' + a.id + '.json')
        .then(r => {
          if (!r.ok) throw Error('Anteprima indisponibile');
          return r.json();
        })
        .then(r => {
          if (!active || computed || JSON.stringify(params) !== JSON.stringify(defaultParams)) return;
          r.previewFigures = Array.from(
            { length: a.plotCount || 1 },
            (_, i) => 'assets/experiments/' + a.id + '-' + (i + 1) + '.svg',
          );
          showResult(r, defaultParams, a.code, false);
        })
        .catch(() => {});
    // Initial static figure is explicitly labelled. The same configuration is then executed by R.
    if (configError) {
      error(configError);
    } else if (!narrated) timer = setTimeout(execute, 250);
    else
      $('#lab-result-meta').textContent =
        'Formula una previsione, quindi esegui il calcolo in R per osservare il risultato.';
    dispose = () => {
      active = false;
      terminal?.destroy();
      request++;
      if (custom !== a.code) E.reset();
      clearTimeout(timer);
      unsub();
      compareUrls.forEach(u => URL.revokeObjectURL(u));
      urls.forEach(u => URL.revokeObjectURL(u));
      root.MathJax?.typesetClear?.([main]);
    };
  }
  function count(module) {
    return listFor(module).length;
  }
  root.GeoLabs = Object.freeze({
    configure,
    cleanup,
    index,
    module,
    mission,
    experiment,
    parseHash,
    byId,
    listFor,
    count,
    activities,
    validate,
    missions,
    modulesForMission,
    path,
  });
})(window);
