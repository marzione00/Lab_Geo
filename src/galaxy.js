/* One navigator: galaxy → stellar system → world → course module. */
(function () {
  'use strict';
  const A = window.GeoAstro,
    N = window.GeoNarrative,
    P = window.GeoPaths,
    esc = window.GeoHTML.escape;
  const n = (v, d = 2) => v.toLocaleString('it-IT', { maximumFractionDigits: d, minimumFractionDigits: 0 });
  let scene = null,
    hoverTimer = 0,
    focusSystem = null;
  const variants = new Map();
  const getModule = id => window.GEO_CATALOG.modules.find(m => m.id === id);
  const stat = (label, value, unit) => `<div><dt>${label}</dt><dd>${value} <small>${unit}</small></dd></div>`;
  const footer = () =>
    `<div class="galaxy-footer"><p><span class="galaxy-beacon"></span>${window.GeoAstro.systems.length} pianeti del corso · ${window.GeoAstro.systems.reduce((n, s) => n + s.planets.filter(p => !p.isTarget).length, 0)} esplorazioni complementari <span class="galaxy-separator">/</span> ${window.GEO_LABS.activities.length} esperimenti R</p><a href="#catalogo">Indice dei moduli →</a></div>`;
  const note = '<p class="model-note">Sistemi immaginari · dimensioni e distanze grafiche non in scala.</p>';
  function cleanup() {
    clearTimeout(hoverTimer);
    scene?.dispose();
    scene = null;
    focusSystem = null;
  }
  function starFacts(s) {
    return `<dl class="astro-stats">${stat('Temperatura effettiva', n(s.star.temperature, 0), 'K')}${stat('Massa stellare', n(s.star.mass), 'M☉')}${stat('Raggio stellare', n(s.star.radius), 'R☉')}${stat('Luminosità', n(s.star.luminosity, 3), 'L☉')}</dl>`;
  }
  function mount(main) {
    cleanup();
    let selected = 'M05';
    const systems = A.systems.map(s => A.generate(s.id, variants.get(s.id) || 0));
    main.innerHTML = `<section class="galaxy-home" aria-labelledby="galaxy-title"><div class="galaxy-heading"><div><p class="eyebrow">ATLANTE SCIENTIFICO / CARTOGRAFIA STELLARE</p><h1 id="galaxy-title">${esc(N.data.home.title)}</h1><p>Una spedizione nella conoscenza, fra astronomia, statistica e codice R.</p></div><a class="galaxy-index" href="#catalogo">Indice del corso ↗</a></div>
   <div class="exploration-steps"><span class="active">01 <b>Galassia</b></span><span>02 Sistema stellare</span><span>03 Pianeta e laboratorio</span></div>
   <div class="galaxy-navigation"><div class="galaxy-chart" role="group" aria-label="Galassia tridimensionale e sistemi stellari">
    <canvas id="galaxy-viewport" tabindex="0" role="img" aria-label="Galassia ruotabile. Trascina o usa le frecce; più e meno regolano lo zoom. Seleziona un punto stellare per entrare nel sistema."></canvas>
    <svg class="galaxy-leaders" aria-hidden="true">${systems.map(s => `<g data-leader="${s.id}"><path class="leader-line"/><circle class="leader-pin" r="2.4"/><circle class="leader-target"/></g>`).join('')}</svg><div class="galaxy-corners" aria-hidden="true"></div>
    <div class="galaxy-chart-heading"><span class="galaxy-beacon"></span><span>ATLANTE GALATTICO<small>${window.GeoAstro.systems.length} SISTEMI / SEQUENZA PRINCIPALE</small></span></div>
    <div class="galaxy-camera" aria-label="Controlli della camera"><button type="button" data-camera="in" aria-label="Avvicina la camera">+</button><button type="button" data-camera="out" aria-label="Allontana la camera">−</button><button type="button" data-camera="reset" aria-label="Ripristina la vista della galassia">↺</button></div>
    ${systems.map(s => `<button class="galaxy-node" type="button" data-destination="${s.id}" aria-pressed="false" aria-controls="destination-detail" aria-label="${s.id} ${s.name}, ${s.star.type} · ${esc(s.subject)}: esplora il sistema del modulo ${esc(getModule(s.id).title)}"><span class="galaxy-node-label"><span class="galaxy-node-name"><small>${s.id}</small> <strong>${s.name}</strong> <i aria-hidden="true">↗</i></span> <span class="galaxy-node-subject">${s.star.type} · ${s.subject}</span></span></button>`).join('')}
    <div class="galaxy-map-caption"><span>TRASCINA PER RUOTARE · CLICCA UN SISTEMA</span><span>MAPPA ILLUSTRATIVA</span></div><div class="galaxy-flight"><span>AVVICINAMENTO A <strong class="galaxy-flight-name"></strong></span><button class="galaxy-skip" type="button">Entra nel sistema →</button></div>
   </div><aside id="destination-detail" class="destination-detail system-preview hud-panel" data-tone="action" aria-labelledby="destination-name"></aside><a class="destination-dock" href="#sistema-${selected}"><span class="hud-label">Sistema selezionato</span><strong></strong><span class="destination-dock-go">Esplora ↗</span></a></div>
   <section class="galaxy-dossier" aria-labelledby="dossier-title"><h2 id="dossier-title" class="hud-label">Dossier della spedizione</h2>${N.home()}${window.GeoResearch.index()}</section>${P.legend()}${note}${footer()}</section>`;
    function select(id) {
      clearTimeout(hoverTimer);
      const s = A.generate(id, variants.get(id) || 0);
      if (!s) return;
      selected = id;
      const m = getModule(id);
      main
        .querySelectorAll('[data-destination]')
        .forEach(b => b.setAttribute('aria-pressed', String(b.dataset.destination === id)));
      main.querySelector('#destination-detail').innerHTML =
        `<p class="destination-signal"><span></span> SISTEMA SELEZIONATO</p><div class="spectral-emblem" style="--star-color:${s.star.color}" aria-hidden="true"><span>${s.star.type[0]}</span><i></i></div><p class="destination-sector">${id} / SEQUENZA PRINCIPALE</p><h2 id="destination-name">${s.name}</h2><p class="destination-type">Stella di classe ${s.star.type} · ${s.planets.length} pianeti</p><p class="stellar-abstract">${s.star.description}</p>${starFacts(s)}${N.destination(id)}<div class="module-destination"><small>DESTINAZIONE DEL CORSO</small><strong>${s.target.name}</strong><span>${esc(m.title)}</span></div><a id="galaxy-travel" class="galaxy-travel" href="#sistema-${id}">Esplora il sistema <span>↗</span></a><p class="galaxy-help">I punti luminosi indicano sistemi stellari. I pianeti diventano visibili durante l’avvicinamento.</p>`;
      main.querySelector('#galaxy-travel').addEventListener('click', e => {
        if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();
        enter(id);
      });
      const dock = main.querySelector('.destination-dock');
      dock.href = '#sistema-' + id;
      dock.querySelector('strong').textContent = `${id} ${s.name}`;
      scene?.select(id);
    }
    function enter(id) {
      select(id);
      const arrive = () => {
        window.GeoCore?.cue('arrive');
        location.hash = '#sistema-' + id;
      };
      if (scene) {
        window.GeoCore?.cue('travel', { duration: 1.35 });
        scene.travel(id, arrive);
      } else arrive();
    }
    main.querySelector('.destination-dock').addEventListener('click', e => {
      if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      enter(selected);
    });
    const buttons = [...main.querySelectorAll('[data-destination]')];
    buttons.forEach((b, i) => {
      b.addEventListener('pointerenter', e => {
        clearTimeout(hoverTimer);
        if (e.pointerType !== 'touch') hoverTimer = setTimeout(() => select(b.dataset.destination), 220);
      });
      b.addEventListener('pointerleave', () => clearTimeout(hoverTimer));
      b.addEventListener('focus', () => select(b.dataset.destination));
      b.addEventListener('click', () => enter(b.dataset.destination));
      b.addEventListener('keydown', e => {
        const k = e.key;
        if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(k)) return;
        e.preventDefault();
        buttons[
          k === 'Home'
            ? 0
            : k === 'End'
              ? buttons.length - 1
              : (i + (['ArrowLeft', 'ArrowUp'].includes(k) ? -1 : 1) + buttons.length) % buttons.length
        ].focus();
      });
    });
    scene = window.GeoGalaxyScene.create(main.querySelector('.galaxy-chart'), select, enter);
    select(selected);
    focusSystem = select;
  }
  function scientificNotes() {
    return `<section class="astro-learning" aria-labelledby="astro-learning-title"><div><p class="eyebrow">LEGGERE IL MODELLO</p><h2 id="astro-learning-title">Tre relazioni per esplorare un sistema.</h2><p>I valori mostrati nelle schede derivano da queste relazioni. Le orbite del modello sono circolari e la massa dei pianeti è trascurata nel calcolo del periodo.</p></div><div class="astro-equations">
  <article><small>01 / RADIAZIONE</small><h3>Luminosità stellare</h3><p class="equation">L/L☉ = (R/R☉)² (T/5772 K)⁴</p><p>Il raggio e la temperatura effettiva determinano la potenza irradiata. L☉ e R☉ indicano luminosità e raggio solari.</p></article>
  <article><small>02 / GRAVITAZIONE</small><h3>Periodo orbitale</h3><p class="equation">P/anno ≃ √[(a/UA)³ / (M/M☉)]</p><p>Aumentando il semiasse maggiore a, il periodo cresce. UA è l’unità astronomica; la massa M è quella della stella.</p></article>
  <article><small>03 / BILANCIO ENERGETICO</small><h3>Temperatura di equilibrio</h3><p class="equation">T<sub>eq</sub> = 278,3 K [(L/L☉)(1 − A<sub>B</sub>)/(a/UA)²]<sup>¼</sup></p><p>A<sub>B</sub> è l’albedo di Bond. Il calcolo assume emissività unitaria e redistribuzione uniforme del calore; esclude effetto serra e calore interno.</p></article></div>
  <details class="astro-method"><summary>Ipotesi, scale e fonti scientifiche</summary><p>Le stelle sono estratte con uguale probabilità fra quattro esempi sintetici di sequenza principale F, G, K e M. Questa scelta offre varietà didattica e non riproduce le frequenze stellari della galassia. Il seme iniziale è stabile; «Nuova configurazione» cambia l’estrazione nella sessione.</p><p>I nomi dei mondi identificano i moduli: anche Terra è qui una destinazione convenzionale, non una ricostruzione del Sistema solare. Superfici, raggi visivi e separazioni delle orbite sono illustrativi; i valori fisici si leggono nelle schede. Una sola scala temporale conserva i rapporti fra i periodi orbitali, mentre la rotazione delle superfici è illustrativa.</p><p>La temperatura di equilibrio non è la temperatura superficiale né un criterio sufficiente di abitabilità. Per stimare un clima occorrono atmosfera, nubi e altri processi.</p><ul><li><a href="https://science.nasa.gov/exoplanets/stars/" target="_blank" rel="noopener noreferrer">NASA · Classi stellari e pianeti</a></li><li><a href="https://science.nasa.gov/solar-system/orbits-and-keplers-laws/" target="_blank" rel="noopener noreferrer">NASA · Orbite e leggi di Keplero</a></li><li><a href="https://exoplanetarchive.ipac.caltech.edu/docs/pscp_calc.html" target="_blank" rel="noopener noreferrer">NASA Exoplanet Archive · Relazioni fra parametri fisici</a></li></ul></details></section>`;
  }
  function system(main, id, variant) {
    if (variant !== undefined) {
      if (!Number.isInteger(variant) || variant < 0 || variant > 9999) return;
      variants.set(id, variant);
    }
    cleanup();
    const s = A.generate(id, variants.get(id) || 0);
    if (!s) return;
    const m = getModule(id);
    main.innerHTML = `<section class="galaxy-home stellar-home" aria-labelledby="system-title"><div class="galaxy-heading"><div><p class="eyebrow">${id} / SISTEMA PLANETARIO SINTETICO</p><h1 id="system-title" tabindex="-1">Sistema ${s.name}<span>.</span></h1><p>Cinque mondi attorno a una stella. Esplora le orbite e raggiungi ${s.target.name}.</p></div><a class="galaxy-index" href="#indice">← Torna alla galassia</a></div>
   ${N.system(s)}${P.legend()}<div class="course-wayfinder">${P.badge(P.forPlanet(s, s.target))}<span>${esc(s.target.name)} · ${esc(m.title)}</span><a href="#modulo-${id}">Entra nel modulo →</a></div><div class="exploration-steps"><a href="#indice">01 Galassia</a><span class="active">02 <b>Sistema stellare</b></span><span id="exploration-step">03 Pianeta e laboratorio</span></div>
   <div class="galaxy-navigation system-navigation"><div class="system-stage"><div class="system-chart" role="group" aria-label="Sistema stellare ${s.name}">
    <svg class="system-orbits" aria-hidden="true">${s.planets.map(() => '<path/>').join('')}</svg><svg class="system-rings" aria-hidden="true">${s.planets.map(p => `<g data-ring="${p.id}" class="${p.isTarget ? 'course-ring' : 'exploration-ring'}"><circle/>${p.isTarget ? '<circle/>' : ''}<path/></g>`).join('')}</svg><canvas id="system-viewport" tabindex="0" role="img" aria-label="Sistema tridimensionale: trascina o usa le frecce per ruotare. Seleziona un pianeta per avvicinarti; Home ripristina la vista."></canvas><div class="galaxy-corners" aria-hidden="true"></div>
    <div class="galaxy-chart-heading"><span class="galaxy-beacon"></span><span>TELEMETRIA ORBITALE<small>${s.name.toUpperCase()} / CLASSE ${s.star.type}</small></span></div>
    <div class="galaxy-camera"><button type="button" data-system-camera="in" aria-label="Avvicina la camera">+</button><button type="button" data-system-camera="out" aria-label="Allontana la camera">−</button><button type="button" data-system-camera="reset" aria-label="Vista completa del sistema">↺</button></div>
    <button type="button" class="body-label star-label" data-body-label="star">${s.name}<small>${s.star.type}</small></button>
    ${s.planets
      .map(p => {
        const meta = P.forPlanet(s, p);
        return `<button type="button" class="body-label ${p.isTarget ? 'module-world' : 'exploration-world'}" data-body-label="${p.id}" aria-controls="body-detail" aria-label="${esc(p.name)} ${p.isTarget ? 'modulo ' + id + ' · corso' : 'esplorazione · ' + esc(meta.discipline) + ' · ' + meta.level} · ${esc(meta.label)} · Livello ${meta.level}"><span aria-hidden="true">${meta.symbol}</span> ${p.name} <small>${p.isTarget ? 'MODULO ' + id + ' · CORSO' : 'ESPLORAZIONE'}</small>${p.isTarget ? '' : ` <span class="body-label-more">${meta.discipline} · ${meta.level}</span>`}</button>`;
      })
      .join('')}
    <div class="galaxy-map-caption"><span>TRASCINA · SELEZIONA UN PIANETA PER AVVICINARTI</span><span>ORBITA CIRCOLARE / e = 0</span></div></div>
    <div class="system-bodies" aria-label="Corpi esplorabili"><button type="button" data-body="star" aria-pressed="true"><i style="--body-color:${s.star.color}">☉</i><span>${s.name}<small>STELLA ${s.star.type}</small></span></button>${s.planets.map(p => `<button type="button" data-body="${p.id}" aria-pressed="false" class="${p.isTarget ? 'target-body' : 'exploration-body'}" aria-controls="body-detail"><i style="--body-color:${p.atmosphere}">${p.isTarget ? '◎' : P.forPlanet(s, p).symbol}</i><span>${p.name}<small>${p.isTarget ? 'CORSO · ' + id : 'ESPLORAZIONE'}</small></span></button>`).join('')}</div><div class="system-scale"><span>Tempo orbitale: 1 s ≈ ${n(s.yearsPerSecond * 365.25, 2)} giorni simulati</span><button type="button" id="new-system">↻ Nuova configurazione</button></div></div>
    <aside id="body-detail" class="destination-detail body-detail" aria-labelledby="body-name"></aside></div>${note}${scientificNotes()}${footer()}</section>`;
    function select(body, zoom = true) {
      clearTimeout(hoverTimer);
      const p = s.planets.find(p => p.id === body);
      if (body !== 'star' && !p) return;
      const meta = p ? P.forPlanet(s, p) : null;
      main.querySelector('#body-detail').dataset.track = meta?.track || 'star';
      main
        .querySelectorAll('[data-body], [data-body-label]')
        .forEach(b => b.setAttribute('aria-pressed', String((b.dataset.body || b.dataset.bodyLabel) === body)));
      main.querySelector('#exploration-step').classList.toggle('active', body !== 'star');
      main.querySelector('#body-detail').innerHTML =
        body === 'star'
          ? `<p class="destination-signal"><span></span> OSSERVAZIONE STELLARE</p><div class="spectral-class"><strong>${s.star.type[0]}</strong><span>CLASSE SPETTRALE<small>V · sequenza principale</small></span></div><h2 id="body-name">${s.name}</h2><p class="stellar-abstract">${s.star.description}</p>${starFacts(s)}<div class="spectral-scale" aria-label="Sequenza delle classi mostrate, da più calda a più fredda">${A.classes.map(c => `<span class="${c.type === s.star.type ? 'current' : ''}" style="--star-color:${c.color}">${c.type[0]}<small>${n(c.temperature, 0)} K</small></span>`).join('')}</div><p class="instrument-note">Temperatura effettiva: temperatura del corpo nero che emetterebbe la stessa potenza per unità di superficie.</p><button class="galaxy-travel" type="button" id="locate-module">Localizza ${s.target.name} <span>↗</span></button><p class="galaxy-help">Il modulo ${id}, «${esc(m.title)}», si trova su ${s.target.name}.</p>`
          : `${P.badge(meta)}${p.familyId ? window.GeoResearch.familyCard(p) : ''}<p class="path-level">Livello ${meta.level.toLowerCase()}${p.isTarget ? '' : ' · Facoltativa'}</p><p class="destination-sector">${s.name} / ORBITA ${p.label.toUpperCase()}</p><h2 id="body-name" tabindex="-1">${p.name}</h2>
   ${p.isTarget ? `<div class="module-destination"><strong>${esc(m.title)}</strong><small>${window.GeoLabs.count(id)} ESPERIMENTI / R + GGPLOT2</small></div><a class="galaxy-travel" id="enter-module" href="#modulo-${id}">Entra nel modulo <span>↗</span></a>` : `<h3 class="exploration-card-title">${esc(meta.title)}</h3><p class="path-introduces">${esc(meta.introduces)}</p><a class="galaxy-travel exploration-travel" id="start-exploration" href="#esplorazione/${p.id}?v=${s.variant}">${meta.project ? (p.category === 'gas' ? 'Accedi all’osservatorio' : 'Avvia il mini-progetto') : 'Avvia l’esplorazione'} <span>↗</span></a><a class="course-return" href="#modulo-${id}">◎ Torna al modulo ${id} →</a>`}
   ${P.prerequisites(meta)}${p.isTarget ? '' : `<p class="path-relation">${esc(meta.relation)}</p>`}
   <details class="body-science"><summary>Parametri e lettura del pianeta</summary><p class="destination-type">${p.description}</p><dl class="astro-stats">${stat('Semiasse maggiore', n(p.axisAU, 3), 'UA')}${stat('Periodo orbitale', n(p.periodYears * 365.25, 1), 'giorni')}${stat('Raggio del modello', n(p.radiusEarth), 'R⊕')}${stat('T di equilibrio', n(p.temperature, 0), 'K')}${stat('Flusso incidente', n(p.flux, 2), 'S⊕')}${stat('Albedo di Bond', n(p.albedo), '')}</dl><div class="planet-lesson"><h3>${p.lesson.title}</h3><p>${p.lesson.text}</p></div>${N.planet(s, p)}<p class="instrument-note">R⊕: raggio terrestre. S⊕: flusso ricevuto dalla Terra. T di equilibrio: bilancio radiativo ideale, senza effetto serra.</p></details><button class="system-overview" type="button" id="system-overview">← Vista completa del sistema</button>`;
      main.querySelector('#locate-module')?.addEventListener('click', () => select(s.target.id));
      main.querySelector('#system-overview')?.addEventListener('click', () => select('star'));
      main.querySelector('#enter-module')?.addEventListener('click', e => {
        if (e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();
        location.hash = '#modulo-' + id;
      });
      if (zoom) {
        scene?.focus(body);
        const chart = main.querySelector('.system-chart');
        if (chart.getBoundingClientRect().top < -80) chart.scrollIntoView({ block: 'start', behavior: 'instant' });
      }
      document.getElementById('annuncio').textContent =
        body === 'star' ? 'Stella ' + s.name : p.name + ' · ' + meta.label + ' · livello ' + meta.level.toLowerCase();
    }
    main.querySelectorAll('[data-body], [data-body-label]').forEach(b => {
      const body = b.dataset.body || b.dataset.bodyLabel;
      b.addEventListener('click', () => select(body));
      b.addEventListener('focus', () => select(body, false));
      b.addEventListener('pointerenter', e => {
        if (e.pointerType === 'touch') return;
        clearTimeout(hoverTimer);
        hoverTimer = setTimeout(() => select(body, false), 250);
      });
      b.addEventListener('pointerleave', () => clearTimeout(hoverTimer));
    });
    main.querySelector('#new-system').addEventListener('click', () => {
      const next = (s.variant + 1) % 10000;
      history.replaceState(null, '', '#sistema-' + id + '?v=' + next);
      system(main, id, next);
      main.querySelector('#system-title').focus({ preventScroll: true });
      document.getElementById('annuncio').textContent = 'Nuova configurazione del sistema ' + s.name;
    });
    scene = window.GeoSystemScene.create(main.querySelector('.system-chart'), s, select);
    select('star', false);
  }
  // The briefing highlights a system without starting the flight.
  const focus = id => focusSystem?.(id);
  window.GeoGalaxy = Object.freeze({ mount, system, cleanup, focus, debug: () => scene?.debug() || null });
})();
