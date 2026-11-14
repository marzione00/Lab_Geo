/* Worked solutions remain a stable reference while the learner explores variants. */
(function (root) {
  'use strict';
  const esc = root.GeoHTML.escape;
  const guides = () => root.GEO_SOLUTIONS || { research: {}, course: {} };
  function paragraphs(code) {
    return code.trim().split(/\n\s*\n/);
  }
  function stageCode(a, g, index) {
    const stage = g.stages[index];
    return stage.code ?? stage.blocks.map(i => paragraphs(a.code)[i]).join('\n\n');
  }
  function partialProgram(a, g, index) {
    if (index === g.stages.length - 1) return a.code;
    return (
      g.stages
        .slice(0, index + 1)
        .map((_, i) => stageCode(a, g, i))
        .join('\n\n') +
      '\n\n# Riepilogo del punto raggiunto; il calcolo successivo riparte dagli stessi dati.\nif (!exists("data", inherits=FALSE)) data <- observations\nif (!exists("metrics", inherits=FALSE)) metrics <- metric("Righe disponibili" = nrow(data))\nplots <- list()\nfor (name in c("g1", "g2")) {\n  if (exists(name, inherits=FALSE)) plots[[length(plots)+1]] <- get(name)\n}\n'
    );
  }
  function reading(id, r, p) {
    const m = Object.fromEntries(r.metrics.map(row => [row.grandezza, row.valore]));
    const v = k => m[k] ?? 'non disponibile';
    switch (id) {
      case 'usgs-quakes':
        return `La soglia ${p.min_mag} conserva ${v('Eventi selezionati')} eventi dei ${v('Eventi nel CSV')} presenti nella copia locale. La magnitudo mediana è ${v('Mediana magnitudo')}, mentre la profondità mediana è ${v('Mediana profondità [km]')} km. Le ${p.bins} classi agiscono sulla rappresentazione: mantenendo la soglia, i conteggi e le mediane devono rimanere invariati. Questo catalogo delimitato non consente da solo una previsione sismica.`;
      case 'jpl-asteroids':
        return `Fra ${v('Coppie disponibili prima della soglia')} coppie diametro–albedo disponibili, il filtro mantiene ${v('Oggetti selezionati')} oggetti. La correlazione di rango è ${v('Correlazione di Spearman')}; riassume l’ordinamento congiunto delle due variabili nel sottocampione selezionato. Poiché l’esclusione dei dati mancanti e la soglia modificano la popolazione osservata, occorre riportare entrambi i criteri nella conclusione.`;
      case 'sea-ice':
        return `Per ${p.month === '3' ? 'marzo' : 'settembre'}, dal ${p.start_year} al 2024, la pendenza stimata è ${v('Pendenza [milioni km2 / decennio]')} milioni di km² per decennio, pari al ${v('Pendenza [% del riferimento / decennio]')}% del riferimento 1981–2010 del medesimo mese. La correlazione residua al ritardo 1 è ${v('Correlazione residua al ritardo 1')}. La lettura della serie dei residui rimane necessaria: questo coefficiente isolato non dimostra indipendenza né giustifica proiezioni climatiche.`;
      case 'solar-flares':
        return `La selezione di classe ${p.minimum_class} conduce a ${v('Eventi nel modello')} eventi utilizzabili, dopo l’esclusione di ${v('Picchi saturati esclusi dal modello')} picchi saturati. La pendenza logaritmica è ${v('Pendenza in scala log10')} e la correlazione di Spearman è ${v('Correlazione di Spearman')}. Il coefficiente descrive un’associazione durata–irradiamento condizionata ai filtri; la diagnostica dei residui e la selezione dei primi eventi consentono di valutarne la sensibilità.`;
      case 'exoplanet-mass-radius':
        return `I filtri conservano ${v('Pianeti dopo i filtri')} pianeti. La separazione riguarda ${v('Sistemi di stima')} sistemi di stima e ${v('Sistemi di verifica')} sistemi di verifica, evitando di distribuire pianeti della stessa stella fra i due gruppi. L’RMSE sui sistemi esclusi dalla stima è ${v('RMSE verifica [dex]')} dex, contro ${v('RMSE previsione costante [dex]')} dex del riferimento costante. La pendenza ${v('Pendenza beta')} descrive il campione selezionato; non identifica composizione o abitabilità e non corregge gli errori di misura.`;
      default:
        return '';
    }
  }
  function save(text, name) {
    const u = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' })),
      a = document.createElement('a');
    a.href = u;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(u), 1500);
  }
  function mount(host, a, g, options = {}) {
    if (!g?.stages?.length) throw Error('Soluzione guidata assente: ' + a.id);
    let selected = 0,
      mode = 'guided',
      params = options.params || {},
      busy = false,
      active = true;
    host.classList.add('solution-terminal');
    host.setAttribute('aria-label', 'Soluzione ragionata e codice R');
    host.innerHTML = `<header class="solution-head"><span aria-hidden="true">R /</span><div><h2>Soluzione ragionata</h2><p>${esc(a.title)}</p></div><small>${options.local ? 'R / RStudio' : 'R sul dispositivo'}</small></header><div class="solution-tabs" role="group" aria-label="Supporto alla soluzione"><button type="button" data-solution-mode="hints" aria-pressed="false">Suggerimento</button><button type="button" data-solution-mode="guided" aria-pressed="true">Soluzione guidata</button><button type="button" data-solution-mode="code" aria-pressed="false">Codice completo</button></div><p class="solution-introduction">${esc(g.introduction)}</p><section class="solution-hints" hidden><h3>Indizi per impostare il ragionamento</h3>${g.hints.map((h, i) => `<details><summary>Indizio ${i + 1}</summary><p>${esc(h)}</p></details>`).join('')}</section><section class="solution-guided"><nav class="solution-stages" aria-label="Passaggi della soluzione">${g.stages.map((s, i) => `<button type="button" data-solution-stage="${i}" aria-pressed="${i === 0}"><span>${String(i + 1).padStart(2, '0')}</span>${esc(s.title)}</button>`).join('')}</nav><div class="solution-explanation"><h3></h3><p></p></div><pre class="solution-snippet" tabindex="0" aria-label="Codice del passaggio selezionato"><code></code></pre><div class="solution-observe"><h4>Come leggere questo passaggio</h4><p></p></div>${options.local ? '' : `<button type="button" class="button" data-solution-run="step">Esegui fino a questo passaggio</button><p class="solution-note">Ogni esecuzione riparte dai dati e dal seme indicati, ricostruendo i passaggi precedenti.</p>`}</section><section class="solution-code" hidden><div class="solution-full-code"></div>${options.local ? '' : `<details class="solution-variant"><summary>Scrivi e verifica una variante</summary><label>Corpo del programma R<textarea class="solution-editor" spellcheck="false" maxlength="100000"></textarea></label><p>La variante usa il campione <code>observations</code> e deve produrre <code>data</code>, <code>metrics</code> e <code>plots</code>. Controlla il programma prima di eseguirlo.</p><div class="solution-actions"><button type="button" class="button" data-solution-run="custom">Esegui la variante</button><button type="button" class="button secondary" data-solution-download-variant>Scarica la variante R</button><button type="button" class="button secondary" data-solution-restore>Ripristina il codice di riferimento</button></div></details>`}</section><div class="solution-actions">${options.local ? '' : `<button type="button" class="button" data-solution-run="full">Esegui la soluzione completa</button>`}<button type="button" class="button secondary" data-solution-download>Scarica la soluzione R</button></div>${options.local ? `<details class="solution-local" open><summary>Esecuzione in RStudio</summary><p>Estrai l’archivio dei dati e delle dipendenze, apri <code>materiali/Corso_Geologia.Rproj</code> e salva lo script scaricato nella cartella <code>materiali</code>. Puoi eseguire il codice dei passaggi in ordine, oppure l’intero script. Questi programmi producono file e richiedono R locale.</p><pre><code>${esc('source("' + a.id + '_soluzione.R", encoding="UTF-8")')}</code></pre><ul>${(g.localRequirements || []).map(t => '<li>' + esc(t) + '</li>').join('')}</ul><a href="assets/downloads/GeoStatLab_codice_dati_R6.zip" download>Dati e dipendenze del corso ↓</a></details>` : ''}<p class="solution-status" role="status">${options.local ? 'Soluzione riferita ai dati e ai programmi originali del corso.' : 'Soluzione di riferimento · scegli un passaggio oppure esegui il programma completo.'}</p><section class="solution-live" hidden><h3>Lettura del calcolo eseguito</h3><p></p></section><details class="solution-reference"><summary>Interpretazione della soluzione di riferimento</summary>${g.interpretation.map(t => '<p>' + esc(t) + '</p>').join('')}${(g.alternatives || []).map(t => '<p>' + esc(t) + '</p>').join('')}<h4>Controlli prima della conclusione</h4><ul>${g.pitfalls.map(t => '<li>' + esc(t) + '</li>').join('')}</ul></details>`;
    const $ = s => host.querySelector(s),
      full = root.GeoCodeGuide.mount($('.solution-full-code'), a, params, { embedded: true, local: options.local });
    if ($('.solution-editor')) $('.solution-editor').value = a.code;
    function show() {
      const s = g.stages[selected];
      $('.solution-explanation h3').textContent = s.title;
      $('.solution-explanation p').textContent = s.explanation;
      $('.solution-snippet code').innerHTML = root.GeoCodeGuide.highlight(stageCode(a, g, selected));
      $('.solution-observe p').textContent = s.observe;
      for (const b of host.querySelectorAll('[data-solution-stage]'))
        b.setAttribute('aria-pressed', String(Number(b.dataset.solutionStage) === selected));
    }
    for (const b of host.querySelectorAll('[data-solution-mode]'))
      b.addEventListener('click', () => {
        mode = b.dataset.solutionMode;
        for (const t of host.querySelectorAll('[data-solution-mode]')) t.setAttribute('aria-pressed', String(t === b));
        $('.solution-hints').hidden = mode !== 'hints';
        $('.solution-guided').hidden = mode !== 'guided';
        $('.solution-code').hidden = mode !== 'code';
      });
    for (const b of host.querySelectorAll('[data-solution-stage]'))
      b.addEventListener('click', () => {
        selected = Number(b.dataset.solutionStage);
        show();
      });
    for (const b of host.querySelectorAll('[data-solution-run]'))
      b.addEventListener('click', () => {
        if (busy) return;
        const kind = b.dataset.solutionRun;
        const step = kind === 'step' ? selected : null,
          partial = step !== null && step < g.stages.length - 1,
          custom = kind === 'custom';
        const body = custom ? $('.solution-editor').value : step === null ? a.code : partialProgram(a, g, step);
        options.execute?.({ body, partial, custom, step });
      });
    $('.solution-editor')?.addEventListener('input', () =>
      options.dirty?.('Codice della variante modificato. Premi Esegui la variante per verificarlo.'),
    );
    $('[data-solution-restore]')?.addEventListener('click', () => {
      $('.solution-editor').value = a.code;
      options.dirty?.('Codice di riferimento ripristinato; esegui per aggiornare i risultati.');
    });
    domDownloadVariant();
    function domDownloadVariant() {
      $('[data-solution-download-variant]')?.addEventListener('click', () =>
        options.downloadBody?.($('.solution-editor').value),
      );
    }
    $('[data-solution-download]').addEventListener('click', () => options.download?.());
    show();
    return {
      update(p) {
        params = p;
        full.update(params);
      },
      invalidate(message) {
        if (!active) return;
        $('.solution-status').textContent = message;
        $('.solution-live').hidden = true;
      },
      setBusy(value) {
        busy = value;
        for (const b of host.querySelectorAll('[data-solution-run],[data-solution-restore]')) b.disabled = value;
        if ($('.solution-editor')) $('.solution-editor').disabled = value;
      },
      completed(result, context) {
        if (!active) return;
        const { custom, partial, step } = context;
        $('.solution-status').textContent = custom
          ? 'Variante eseguita. La spiegazione di riferimento riguarda il programma originale.'
          : partial
            ? 'Calcolo completato fino a «' + g.stages[step].title + '». I risultati sono intermedi.'
            : 'Soluzione completa eseguita con i parametri correnti.';
        $('.solution-live').hidden = custom || partial;
        $('.solution-live p').textContent = custom || partial ? '' : reading(a.id, result, params);
      },
      destroy() {
        active = false;
        full.destroy();
        host.replaceChildren();
      },
    };
  }
  function mountCourse(host, id) {
    const g = guides().course[id];
    if (!g) throw Error('Soluzione del progetto assente: ' + id);
    const a = { id, title: g.title, code: g.code, controls: [] };
    return mount(host, a, g, { local: true, download: () => save(g.code, id + '_soluzione.R') });
  }
  root.GeoSolutions = Object.freeze({ guides, mount, mountCourse, partialProgram, stageCode, reading });
})(globalThis);
