/* Optional scientific readings have their own fieldbook, never course progress. */
(function (root) {
  'use strict';
  const key = 'geostat-explorations-v1',
    esc = root.GeoHTML.escape,
    n = (v, d = 2) => v.toLocaleString('it-IT', { maximumFractionDigits: d });
  function resolve(id, variant = 0) {
    const match = /^(T00|M(?:0[1-9]|1[0-6]))-([b-f])$/.exec(id || '');
    if (!match) return null;
    const s = root.GeoAstro.generate(match[1], variant),
      p = s?.planets.find(p => p.id === id);
    return p && !p.isTarget ? { s, p, meta: root.GeoPaths.forPlanet(s, p) } : null;
  }
  function clean(raw) {
    if (
      !raw ||
      typeof raw.id !== 'string' ||
      !Number.isInteger(raw.variant) ||
      raw.variant < 0 ||
      raw.variant > 9999 ||
      !resolve(raw.id, raw.variant) ||
      typeof raw.notes !== 'string' ||
      !raw.notes.trim() ||
      raw.notes.length > 6000 ||
      typeof raw.completed !== 'boolean' ||
      typeof raw.date !== 'string' ||
      !Number.isFinite(Date.parse(raw.date))
    )
      return null;
    return { id: raw.id, variant: raw.variant, notes: raw.notes, completed: raw.completed, date: raw.date };
  }
  function records() {
    try {
      const raw = localStorage.getItem(key);
      if (!raw || raw.length > 500000) return [];
      const data = JSON.parse(raw);
      if (data.version !== 1 || !Array.isArray(data.entries) || data.entries.length > 68) return [];
      const out = new Map();
      for (const x of data.entries) {
        const r = clean(x);
        if (r) out.set(r.id, r);
      }
      return [...out.values()];
    } catch {
      return [];
    }
  }
  function save(raw) {
    const r = clean(raw);
    if (!r) return false;
    try {
      localStorage.setItem(key, JSON.stringify({ version: 1, entries: [...records().filter(x => x.id !== r.id), r] }));
      return true;
    } catch {
      return false;
    }
  }
  function download(text, name, type) {
    const url = URL.createObjectURL(new Blob([text], { type })),
      a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  }
  function table(s, p) {
    return (
      '<div class="exploration-table" tabindex="0" role="region" aria-label="Confronto dei cinque mondi; tabella scorrevole"><table><caption>Configurazione sintetica ' +
      s.variant +
      ' · stella ' +
      s.star.type +
      ' · confronto entro lo stesso sistema</caption><thead><tr><th scope="col">Mondo</th><th scope="col">Percorso</th><th scope="col">Distanza (UA)</th><th scope="col">Periodo (giorni)</th><th scope="col">Raggio (R⊕)</th><th scope="col">Albedo</th><th scope="col">Flusso (S⊕)</th><th scope="col">T eq (K)</th></tr></thead><tbody>' +
      s.planets
        .map(
          q =>
            '<tr' +
            (q.id === p.id ? ' class="current-world"' : '') +
            '><th scope="row">' +
            esc(q.name) +
            (q.id === p.id ? ' · selezionato' : '') +
            '</th><td>' +
            (q.isTarget ? 'Corso ' + s.id : 'Esplorazione') +
            '</td><td>' +
            n(q.axisAU, 3) +
            '</td><td>' +
            n(q.periodYears * 365.25, 1) +
            '</td><td>' +
            n(q.radiusEarth) +
            '</td><td>' +
            n(q.albedo) +
            '</td><td>' +
            n(q.flux) +
            '</td><td>' +
            n(q.temperature, 1) +
            '</td></tr>',
        )
        .join('') +
      '</tbody></table></div>'
    );
  }
  function csv(s) {
    return [
      'mondo,percorso,semiasse_UA,periodo_giorni,raggio_Rterra,albedo_Bond,flusso_Sterra,temperatura_equilibrio_K',
      ...s.planets.map(p =>
        [
          p.name,
          p.isTarget ? 'corso' : 'esplorazione',
          p.axisAU,
          p.periodYears * 365.25,
          p.radiusEarth,
          p.albedo,
          p.flux,
          p.temperature,
        ].join(','),
      ),
    ].join('\n');
  }
  function render(main, id, variant = 0) {
    const r = resolve(id, variant);
    if (!r) {
      main.innerHTML =
        '<section class="error"><h1>Esplorazione non disponibile</h1><p>Questo collegamento non identifica un pianeta complementare.</p><a href="#indice">Torna alla galassia</a></section>';
      return;
    }
    const { s, p, meta } = r,
      old = records().find(x => x.id === id),
      m = root.GEO_CATALOG.modules.find(x => x.id === s.id);
    main.innerHTML = `<section class="wrap exploration-page" data-exploration="${id}" data-track="exploration"><nav class="exploration-breadcrumb" aria-label="Posizione nel percorso"><a href="#sistema-${s.id}?v=${s.variant}">Sistema ${s.name}</a><span>/</span><span>Esplorazione di ${esc(p.name)}</span></nav><header class="exploration-header">${root.GeoPaths.badge(meta)}${p.familyId ? root.GeoResearch.familyCard(p) : ''}<p class="path-level">Livello ${meta.level.toLowerCase()} · ${meta.project ? 'Mini-progetto su dati reali' : 'Lettura scientifica e confronto dei parametri'}</p><h1>${esc(meta.title)}</h1><p class="lead">${esc(p.name)} · ${esc(meta.introduces)}</p><a class="course-return" href="#modulo-${s.id}">◎ Torna al modulo ${s.id} · ${esc(m.title)} →</a></header><div class="exploration-layout"><article class="exploration-reading"><p class="eyebrow">OSSERVARE E INTERPRETARE</p>${meta.project ? '<div id="research-host"></div>' : meta.paragraphs.map(t => '<p>' + esc(t) + '</p>').join('')}${meta.project ? '' : '<div class="exploration-question"><h2>La tua indagine</h2><p>' + esc(meta.question) + '</p></div>'}${meta.project ? '<details class="research-model-context"><summary>Il sistema immaginario: parametri e modello astronomico</summary>' : ''}${meta.project ? meta.paragraphs.map(t => '<p>' + esc(t) + '</p>').join('') : ''}<h2>Confronta i mondi</h2><p>Per ${esc(p.name)}, il modello restituisce un periodo di ${n(p.periodYears * 365.25, 1)} giorni e una temperatura di equilibrio di ${n(p.temperature, 1)} K. Confronta le grandezze nella tabella mantenendo esplicite le ipotesi del calcolo.</p>${table(s, p)}<button type="button" class="button secondary" id="exploration-csv">Scarica i parametri CSV</button><details class="exploration-assumptions"><summary>Relazioni, unità e ipotesi</summary><p class="equation">P/anno = √[(a/UA)³ / (M★/M☉)]</p><p class="equation">F/S⊕ = (L★/L☉) / (a/UA)²</p><p class="equation">T<sub>eq</sub> = 278,3 K [(1 − A<sub>B</sub>)(F/S⊕)]<sup>¼</sup></p><p>a è il semiasse maggiore, M★ la massa stellare, L★ la luminosità e A<sub>B</sub> l’albedo di Bond. Le orbite sono circolari e la massa planetaria viene trascurata. Il bilancio radiativo assume emissività unitaria e redistribuzione uniforme; atmosfera e calore interno sono esclusi.</p><p>UA indica l’unità astronomica; R⊕ e S⊕ sono rispettivamente il raggio terrestre e il flusso ricevuto dalla Terra. Nella configurazione iniziale le distanze sono scalate con √(L★/L☉): mondi corrispondenti attorno a stelle differenti ricevono lo stesso flusso. Le texture e le scale grafiche sono illustrative.</p></details>${meta.project ? '</details>' : ''}<section class="exploration-record"><h2>Argomenta la tua conclusione</h2><label for="exploration-notes">Rispondi alla domanda, citando i parametri o le ipotesi che sostengono la tua interpretazione.</label><textarea id="exploration-notes" rows="6" maxlength="6000">${esc(old?.notes || '')}</textarea><label class="exploration-complete"><input type="checkbox" id="exploration-complete" ${old?.completed ? 'checked' : ''}> Ho concluso questa esplorazione e riesco a motivare la mia risposta.</label><button class="button" id="exploration-save" type="button">Conserva nel taccuino delle esplorazioni</button><p id="exploration-status" role="status">${old ? 'Hai già un’annotazione per questo mondo. Il salvataggio la aggiornerà.' : 'La visita non registra un completamento. Scrivi una risposta per conservare il lavoro.'}</p><a href="#taccuino-esplorazioni">Apri il taccuino delle esplorazioni →</a></section></article><aside class="exploration-preparation">${root.GeoPaths.prerequisites(meta)}<h2>Collegamento al corso</h2><p>${esc(meta.relation)}</p><p>Questo approfondimento è facoltativo. Le sue annotazioni e i suoi completamenti sono registrati separatamente dalle attività del corso.</p><h2>Fonti scientifiche</h2><ul>${meta.sources
      .map(k => {
        const source = root.GeoPaths.links[k];
        return (
          '<li><a href="' +
          source.url +
          '" target="_blank" rel="noopener noreferrer">' +
          esc(source.label) +
          '</a></li>'
        );
      })
      .join(
        '',
      )}</ul><p class="instrument-note">Parametri del pianeta: modello sintetico GeoStat Lab. Le fonti documentano i concetti e i confronti reali, senza attribuire osservazioni a questo mondo immaginario.</p></aside></div></section>`;
    if (meta.project) root.GeoResearch.mount(main.querySelector('#research-host'), meta.project);
    const notes = main.querySelector('#exploration-notes'),
      button = main.querySelector('#exploration-save'),
      status = main.querySelector('#exploration-status');
    const sync = () => {
      button.disabled = !notes.value.trim();
    };
    notes.addEventListener('input', sync);
    sync();
    button.addEventListener('click', () => {
      const completed = main.querySelector('#exploration-complete').checked;
      const ok = save({ id, variant, notes: notes.value, completed, date: new Date().toISOString() });
      status.textContent = ok
        ? completed
          ? 'Esplorazione conservata come conclusa, secondo la tua autovalutazione.'
          : 'Annotazione conservata; esplorazione ancora in corso.'
        : 'Il browser non consente il salvataggio. Copia la tua risposta per conservarla.';
    });
    main
      .querySelector('#exploration-csv')
      .addEventListener('click', () =>
        download(csv(s), 'GeoStatLab_' + id + '_parametri.csv', 'text/csv;charset=utf-8'),
      );
  }
  function journal(main) {
    const entries = records(),
      done = entries.filter(x => x.completed).length;
    main.innerHTML = `<section class="wrap narrative-journal exploration-journal">${root.GeoPaths.tabs('exploration')}<p class="eyebrow">TACCUINO SCIENTIFICO / ESPLORAZIONI FACOLTATIVE</p><h1>I mondi che hai approfondito.</h1><p class="lead">Annotazioni: ${entries.length} · Esplorazioni concluse per autovalutazione: ${done} su 68 destinazioni complementari.</p><p>Questi risultati appartengono alle esplorazioni e non modificano il percorso del corso. Le annotazioni sono conservate in questo browser; esportale per custodirne una copia.</p><div class="actions"><a class="button secondary" href="#indice">Scegli un sistema →</a><button id="exploration-export" class="button" ${entries.length ? '' : 'disabled'}>Esporta il taccuino delle esplorazioni</button></div><div class="journal-entries">${
      entries
        .map(e => {
          const { s, p, meta } = resolve(e.id, e.variant);
          return `<article class="journal-entry" data-track="exploration">${root.GeoPaths.badge(meta)}<h2>${esc(p.name)} · ${esc(meta.title)}</h2><p>${e.completed ? 'Conclusa per autovalutazione' : 'In corso'} · Configurazione ${e.variant}</p><p class="journal-notes">${esc(e.notes)}</p><a href="#esplorazione/${e.id}?v=${e.variant}">Riapri l’esplorazione →</a> · <a href="#modulo-${s.id}">Torna al modulo ${s.id}</a></article>`;
        })
        .join('') ||
      '<div class="journal-empty"><h2>La prima esplorazione</h2><p>Scegli un pianeta con il richiamo ambra, apri la lettura guidata e conserva la tua interpretazione. Il livello e i prerequisiti sono indicati nella sua scheda.</p></div>'
    }</div></section>`;
    main
      .querySelector('#exploration-export')
      .addEventListener('click', () =>
        download(
          JSON.stringify({ application: 'GeoStatLab', track: 'exploration', version: 1, entries }, null, 2),
          'GeoStatLab_taccuino_esplorazioni.json',
          'application/json',
        ),
      );
  }
  root.GeoExplorations = Object.freeze({ resolve, records, save, render, journal });
})(globalThis);
