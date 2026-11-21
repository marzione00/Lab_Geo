/* Lessons of the planetary systems: one tappa per slide on the main planet, exercises on a companion world. */
(function (root) {
  'use strict';
  const { html } = root.GeoHTML,
    S = root.GeoSecurity,
    key = 'geostat-lessons-v1';
  let typeset = () => {},
    disposers = [];
  const index = () => root.GEO_LESSON_INDEX || {};
  function configure(options) {
    if (typeof options.typeset === 'function') typeset = options.typeset;
  }
  function cleanup() {
    disposers.forEach(fn => fn());
    disposers = [];
  }
  // The companion world of a lesson hosts its exercises; null for every other world.
  function forWorld(world) {
    const hit = Object.entries(index()).find(([, l]) => l.exercisesWorld === world || l.world === world);
    return hit ? { id: hit[0], ...hit[1], role: hit[1].world === world ? 'lesson' : 'exercises' } : null;
  }

  // ---------------------------------------------------------------- progress, local only
  function load() {
    try {
      const raw = localStorage.getItem(key);
      const v = raw && raw.length < 400000 ? JSON.parse(raw) : null;
      if (!v || v.version !== 1 || !Array.isArray(v.done) || typeof v.cards !== 'object' || !v.cards)
        return { version: 1, done: [], cards: {} };
      return {
        version: 1,
        done: v.done.filter(x => typeof x === 'string' && /^[A-Z]\d{2}:\d{1,3}$/.test(x)).slice(0, 2000),
        cards: Object.fromEntries(
          Object.entries(v.cards)
            .filter(([k, c]) => /^[A-Z]\d{2}:\d{1,2}$/.test(k) && c && typeof c === 'object')
            .map(([k, c]) => [
              k,
              {
                values: Object.fromEntries(
                  Object.entries(c.values || {})
                    .filter(([f, x]) => /^[AB]:[a-z_]{1,40}$/.test(f) && typeof x === 'string' && x.length < 40)
                    .slice(0, 40),
                ),
                passed: c.passed === true,
                notes: typeof c.notes === 'string' ? c.notes.slice(0, S.limits.notes) : '',
              },
            ]),
        ),
      };
    } catch {
      return { version: 1, done: [], cards: {} };
    }
  }
  function save(state) {
    try {
      localStorage.setItem(key, JSON.stringify(state));
      return true;
    } catch {
      return false;
    }
  }

  // ---------------------------------------------------------------- text
  function inline(list) {
    return html`${list.map(n => {
      if (typeof n === 'string') return n;
      if (n.t === 'm') return '\\(' + n.v + '\\)';
      if (n.t === 'c') return html`<code>${n.v}</code>`;
      if (n.t === 'b') return html`<strong>${inline(n.c)}</strong>`;
      if (n.t === 'i') return html`<em>${inline(n.c)}</em>`;
      if (n.t === 'a')
        return /^https:/.test(n.h)
          ? html`<a href="${n.h}" target="_blank" rel="noopener noreferrer">${inline(n.c)}</a>`
          : html`<a href="${n.h}">${inline(n.c)}</a>`;
      return '';
    })}`;
  }
  function blocks(list) {
    return html`${list.map(b =>
      b.t === 'h'
        ? html`<h3>${inline(b.c)}</h3>`
        : b.t === 'ul'
          ? html`<ul>${b.items.map(i => html`<li>${inline(i)}</li>`)}</ul>`
          : b.t === 'math'
            ? html`<div class="math">\\[${b.v}\\]</div>`
            : html`<p>${inline(b.c)}</p>`,
    )}`;
  }
  const labUrl = (id, params = {}) =>
    '#laboratorio/' + id + (Object.keys(params).length ? '?c=' + encodeURIComponent(JSON.stringify(params)) : '');
  const paramText = params =>
    Object.entries(params)
      .map(([k, v]) => k + ' = ' + String(v).replace('.', ','))
      .join(' · ');
  function transcript(s) {
    if (s.page === 1) return html`${s.lines.map(t => html`<p>${t}</p>`)}`;
    if (s.page === 2)
      return html`<p class="lesson-slide-label">Domanda centrale</p><p>${s.question}</p><ol>${s.steps.map(t => html`<li>${t}</li>`)}</ol>`;
    return html`${s.items.map(it => {
      if (it.t === 'label') return html`<p class="lesson-slide-label">${inline(it.c)}</p>`;
      if (it.t === 'p') return html`<p>${inline(it.c)}</p>`;
      if (it.t === 'small') return html`<p class="lesson-small">${inline(it.c)}</p>`;
      if (it.t === 'info') return html`<p class="lesson-info">${inline(it.c)}</p>`;
      if (it.t === 'math') return html`<div class="math">\\[${it.v}\\]</div>`;
      if (it.t === 'code')
        return html`<p class="lesson-small">Riquadro di codice «${it.title}»: <code>${it.file}</code>, eseguibile nella sezione Codice R.</p>`;
      if (it.t === 'lab') return html`<p>${inline(it.c)}: <a href="${labUrl(it.lab)}">apri il laboratorio ↗</a></p>`;
      return '';
    })}`;
  }

  // ---------------------------------------------------------------- R code of a slide
  function script(L, file, code) {
    const deps = L.code[file].deps;
    return (
      '# ' +
      L.planet +
      ' · tappa ' +
      Number(file.slice(0, 3)) +
      ' · ' +
      file +
      '\n# Eseguire dalla cartella del progetto ' +
      L.planet +
      ' (archivio della lezione).\n' +
      '# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0\n' +
      '# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)\n\n' +
      'source("setup.R", encoding = "UTF-8")\n' +
      deps.map(d => '\n# Dalla slide ' + Number(d.slice(0, 3)) + ' (' + d + ')\n' + L.code[d].code + '\n').join('') +
      '\n# ' +
      file +
      '\n' +
      code +
      '\n'
    );
  }
  function download(text, name) {
    const url = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' })),
      a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  }
  function codeBox(L, it, opts = {}) {
    const c = L.code[it.file],
      id = 'code-' + it.file.slice(0, 3),
      deps = c.deps.length
        ? html`Prima di questo codice vengono eseguiti, senza mostrarli, <code>setup.R</code> e ${c.deps.map((d, i) => html`${i ? ', ' : ''}<a href="#lezione-${L.id}/${Number(d.slice(0, 3))}"><code>${d}</code></a>`)}.`
        : html`Prima di questo codice viene eseguito, senza mostrarlo, <code>setup.R</code>.`;
    return html`<article class="lesson-code" data-file="${it.file}"><header><h3>${it.title}</h3><code>${opts.path || 'Codice/' + it.file}</code></header><p class="lesson-small">${deps}</p><label class="sr-only" for="${id}">Codice R modificabile · ${it.file}</label><textarea class="lab-editor lesson-editor" id="${id}" spellcheck="false" maxlength="${S.limits.code}" rows="${Math.min(22, c.code.split('\n').length + 1)}">${c.code}</textarea><div class="lab-actions"><button type="button" class="button small" data-run>Esegui in R</button><button type="button" class="button small secondary" data-restore>Ripristina il codice della slide</button><button type="button" class="button small secondary" data-copy-code>Copia</button><button type="button" class="button small secondary" data-download>Scarica .R</button></div><p class="lesson-output-head" data-head>Uscita attesa</p><pre class="lab-code-output lesson-output" tabindex="0" role="region" aria-label="Uscita di R · ${it.file}" data-output>${c.output}</pre><div class="lesson-figures" data-figures></div></article>`;
  }
  function bindCode(host, L, announce) {
    const urls = [];
    disposers.push(() => urls.splice(0).forEach(u => URL.revokeObjectURL(u)));
    host.querySelectorAll('.lesson-code').forEach(box => {
      const file = box.dataset.file,
        original = L.code[file].code,
        $ = s => box.querySelector(s),
        editor = $('textarea');
      $('[data-restore]').addEventListener('click', () => {
        editor.value = original;
        $('[data-head]').textContent = 'Uscita attesa';
        $('[data-output]').textContent = L.code[file].output;
        $('[data-figures]').replaceChildren();
        announce('Codice della slide ripristinato');
      });
      $('[data-copy-code]').addEventListener('click', () =>
        navigator.clipboard?.writeText(editor.value).then(
          () => announce('Codice copiato'),
          () => announce('Copia non riuscita: seleziona il testo manualmente'),
        ),
      );
      $('[data-download]').addEventListener('click', () => download(script(L, file, editor.value), file));
      $('[data-run]').addEventListener('click', async () => {
        const button = $('[data-run]');
        button.disabled = true;
        $('[data-head]').textContent = 'Esecuzione in R nel browser…';
        try {
          const r = await root.GeoREngine.runSnippet({
            project: L.project,
            deps: L.code[file].deps.map(d => L.code[d].code),
            code: editor.value,
            edited: editor.value !== original,
          });
          if (!box.isConnected) return;
          $('[data-head]').textContent =
            (r.status === 'ok' ? 'Uscita di R nel browser · ' : 'Uscita di R con errore · ') + r.R;
          $('[data-output]').textContent = r.output;
          $('[data-figures]').innerHTML = html`${r.figures.map((svg, i) => {
            const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
            urls.push(url);
            return html`<figure><img src="${url}" alt="Grafico ${i + 1} prodotto dal codice ${file}"><figcaption>Grafico ${i + 1} · <a href="${url}" download="${file.replace(/\.R$/, '')}-${i + 1}.svg">Scarica SVG</a></figcaption></figure>`;
          })}`;
          announce(r.status === 'ok' ? 'Codice eseguito' : 'Il codice ha prodotto un errore');
        } catch (err) {
          if (!box.isConnected) return;
          $('[data-head]').textContent = 'Esecuzione non riuscita';
          $('[data-output]').textContent = err.message;
        } finally {
          button.disabled = false;
        }
      });
    });
  }
  function engineState(host) {
    const el = host.querySelector('[data-engine]');
    if (!el || !root.GeoREngine) return;
    disposers.push(root.GeoREngine.subscribe(s => (el.textContent = s.text)));
  }

  // ---------------------------------------------------------------- lesson pages
  const regionName = t => t.charAt(0) + t.slice(1).toLowerCase();
  function sidebar(L, page) {
    return html`<aside class="reader-sidebar lesson-sidebar" aria-label="Tappe della lezione"><h2>${L.planet} · Tappe</h2><input type="search" id="cerca-tappa" aria-label="Cerca fra le tappe" placeholder="Cerca una tappa">${L.sections.map(
      sec =>
        html`<p class="toc-section">${regionName(sec.title)}</p>${L.slides
          .slice(sec.first - 1, sec.last)
          .map(
            s =>
              html`<a class="toc-link" href="#lezione-${L.id}/${s.page}" data-search="${(s.title + ' ' + sec.title).toLowerCase()}"${s.page === page ? html` aria-current="page"` : ''}><span>${String(s.page).padStart(2, '0')}</span><span>${s.title}</span></a>`,
          )}`,
    )}</aside>`;
  }
  function crumbs(L, extra) {
    return html`<div class="breadcrumb"><a href="#indice">Galassia</a><span>/</span><a href="#sistema-${L.id}">Sistema di ${L.planet}</a><span>/</span><a href="#lezione-${L.id}">${L.planet} · Lezione ${L.id}</a>${extra ? html`<span>/</span><span>${extra}</span>` : ''}</div>`;
  }
  function overview(main, L) {
    const done = new Set(load().done);
    main.innerHTML = html`<div class="wrap lesson-overview">${crumbs(L)}<header class="module-head lesson-head"><p class="eyebrow">${L.id} · PIANETA ${L.planet.toUpperCase()} · LEZIONE</p><h1>${L.title}</h1><div class="lesson-intro">${blocks(L.intro)}</div><div class="lab-actions"><a class="button" href="#lezione-${L.id}/2">Inizia dalla tappa 2 →</a><a class="button secondary" href="${L.pdf}" target="_blank" rel="noopener">PDF della lezione con i codici di tappa ↗</a><a class="button secondary" href="${L.download}" download>Progetto R: codice e dati</a><a class="button secondary" href="#esercizi-${L.id}">Quaderno degli esercizi →</a></div></header><section class="lesson-regions" aria-label="Regioni del pianeta">${L.sections
      .filter(sec => sec.first > 2)
      .map(sec => {
        const tappe = L.slides.slice(sec.first - 1, sec.last);
        return html`<article class="lesson-region-card"><p class="eyebrow">Tappe ${sec.first}–${sec.last}</p><h2>${regionName(sec.title)}</h2><p class="lesson-small">${tappe.length} tappe · ${tappe.filter(s => done.has(L.id + ':' + s.page)).length} studiate</p><ol start="${sec.first}">${tappe.map(s => html`<li><a href="#lezione-${L.id}/${s.page}">${s.title}</a></li>`)}</ol></article>`;
      })}</section></div>`;
    typeset(main.querySelector('.lesson-intro'));
  }
  function tappa(main, L, page, announce) {
    const s = L.slides[page - 1],
      sec = L.sections.find(x => page >= x.first && page <= x.last),
      state = load(),
      doneKey = L.id + ':' + page,
      codes = s.items.filter(it => it.t === 'code'),
      labs = [
        ...s.items.filter(it => it.t === 'lab').map(it => ({ id: it.lab, params: {}, title: null })),
        ...(s.labs || []),
      ],
      prev = L.slides[page - 2],
      next = L.slides[page];
    main.innerHTML = html`<div class="viewer lesson-viewer">${crumbs(L, 'Tappa ' + page)}<div class="reader-layout">${sidebar(L, page)}<div class="reader-main lesson-main"><div class="reader-title"><h1>${s.title}</h1><span class="page-counter">${String(page).padStart(2, '0')} / ${L.pages}</span></div><div class="reader-tools"><p class="lesson-stop"><span class="lesson-stop-code">${L.planet} · ${page}</span> ${regionName(sec.title)}${sec.first < sec.last ? ' · tappe ' + sec.first + '–' + sec.last : ''}</p><div class="pager"><button data-step="-1" aria-label="Tappa precedente"${prev ? '' : ' disabled'}>←</button><button data-step="1" aria-label="Tappa successiva"${next ? '' : ' disabled'}>→</button></div></div><figure class="slide-frame lesson-slide"><img src="${s.image}" alt="Slide ${page} della lezione ${L.id}: ${s.title}. Il testo della slide è riportato sotto l’immagine." width="1134" height="709"></figure><div class="slide-caption"><span>Slide della lezione</span><a href="${s.image}" target="_blank" rel="noopener">Ingrandisci ↗</a><a href="${L.pdf}#page=${page}" target="_blank" rel="noopener">Apri nel PDF ↗</a></div>${s.recall.length ? html`<div class="recall lesson-recall"><strong>Da ricordare.</strong> ${inline(s.recall)}</div>` : ''}<section class="lesson-text" aria-label="Testo della slide ${page}"><div class="lesson-transcript-body">${transcript(s)}</div>${L.notes[page] ? html`<div class="lesson-notes">${blocks(L.notes[page])}</div>` : ''}</section>${
      codes.length
        ? html`<section class="lesson-code-section" aria-labelledby="lesson-code-title"><h2 id="lesson-code-title">Codice R della slide</h2><p class="lesson-small">Modifica il codice ed eseguilo: R lavora su questo dispositivo, nella cartella del progetto ${L.planet}. Esegui soltanto codice di cui conosci la provenienza.</p><p class="lab-engine-state" role="status" aria-live="polite" data-engine></p>${codes.map(it => codeBox(L, it))}</section>`
        : ''
    }${
      labs.length
        ? html`<section class="lesson-labs" aria-labelledby="lesson-labs-title"><h2 id="lesson-labs-title">Laboratorio</h2><ul>${labs.map(
            lab => {
              const a = root.GeoLabs?.byId.get(lab.id);
              return a
                ? html`<li><a class="button secondary" href="${labUrl(lab.id, lab.params)}">${a.title}${Object.keys(lab.params).length ? html` · ${paramText(lab.params)}` : ' · parametri iniziali'} ↗</a></li>`
                : '';
            },
          )}</ul><p class="lesson-small">I pulsanti aprono il laboratorio del sito con gli stessi parametri delle chiamate nel codice della slide; i parametri non indicati restano ai valori iniziali.</p></section>`
        : ''
    }<nav class="lesson-pager" aria-label="Tappe vicine">${prev ? html`<a href="#lezione-${L.id}/${prev.page}">← ${prev.page} · ${prev.title}</a>` : html`<span></span>`}${next ? html`<a href="#lezione-${L.id}/${next.page}">${next.page} · ${next.title} →</a>` : html`<a href="#esercizi-${L.id}">Quaderno degli esercizi →</a>`}</nav><div class="study-actions"><button id="lesson-done" class="button small secondary${state.done.includes(doneKey) ? ' done' : ''}" aria-pressed="${state.done.includes(doneKey)}">${state.done.includes(doneKey) ? '✓ Tappa studiata' : 'Segna la tappa come studiata'}</button><p>Il progresso resta soltanto in questo browser.</p></div></div></div></div>`;
    main
      .querySelectorAll('[data-step]')
      .forEach(b =>
        b.addEventListener('click', () => (location.hash = '#lezione-' + L.id + '/' + (page + Number(b.dataset.step)))),
      );
    main.querySelector('#cerca-tappa').addEventListener('input', e => {
      const q = e.target.value.trim().toLowerCase();
      main.querySelectorAll('.lesson-sidebar .toc-link').forEach(a => (a.hidden = !a.dataset.search.includes(q)));
    });
    main.querySelector('#lesson-done').addEventListener('click', e => {
      const st = load(),
        on = !st.done.includes(doneKey);
      st.done = on ? [...st.done, doneKey] : st.done.filter(x => x !== doneKey);
      save(st);
      e.currentTarget.classList.toggle('done', on);
      e.currentTarget.setAttribute('aria-pressed', String(on));
      e.currentTarget.textContent = on ? '✓ Tappa studiata' : 'Segna la tappa come studiata';
      announce(on ? 'Tappa segnata come studiata' : 'Segnalazione rimossa');
    });
    bindCode(main, L, announce);
    engineState(main);
    typeset(main.querySelector('.lesson-main'));
    main.querySelector('.toc-link[aria-current="page"]')?.scrollIntoView({ block: 'nearest' });
  }
  function lesson(main, L, page, announce = () => {}) {
    cleanup();
    if (page) tappa(main, L, page, announce);
    else overview(main, L);
  }

  // ---------------------------------------------------------------- exercises
  const parse = text => {
    const t = String(text).trim().replace(/\s/g, '').replace(',', '.');
    return /^[-+]?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?$/i.test(t) ? Number(t) : NaN;
  };
  const check = (field, text) => {
    const x = parse(text);
    return Number.isFinite(x) && Math.abs(x - field.value) <= field.tol + 1e-12;
  };
  function exercises(main, L, n, announce = () => {}) {
    cleanup();
    const E = L.exercises,
      card = E.cards[n - 1],
      cardKey = L.id + ':' + n,
      state = load(),
      saved = state.cards[cardKey] || { values: {}, passed: false, notes: '' },
      world = root.GeoAstro?.generate(L.id, 0)?.planets.find(p => p.id === L.exercisesWorld),
      worldName = world?.name || L.exercisesWorld,
      fieldKey = f => f.scenario + ':' + f.key;
    const scenario = name =>
      html`<a class="button secondary" href="${labUrl(card.id, card.scenarios[name].link.params)}">Scenario ${name} nel laboratorio${Object.keys(card.scenarios[name].link.params).length ? html` · ${paramText(card.scenarios[name].link.params)}` : ''} ↗</a>`;
    main.innerHTML = html`<div class="wrap lesson-exercises"><div class="breadcrumb"><a href="#indice">Galassia</a><span>/</span><a href="#sistema-${L.id}">Sistema di ${L.planet}</a><span>/</span><a href="#esercizi-${L.id}">${worldName} · Esercizi</a><span>/</span><span>Esercizio ${n}</span></div><header class="module-head lesson-head"><p class="eyebrow">${L.id} · ${worldName.toUpperCase()} · PIANETA DEGLI ESERCIZI</p><h1>Quaderno di ${L.planet}</h1><p class="lead">${E.subtitle} Gli esercizi usano i concetti delle tappe della lezione su ${L.planet}.</p><details class="lesson-common"><summary>Istruzioni comuni</summary><ol>${E.common.map(t => html`<li>${t}</li>`)}</ol></details><div class="lab-actions"><a class="button secondary" href="${L.workbook}" target="_blank" rel="noopener">Quaderno in PDF ↗</a><a class="button secondary" href="${L.download}" download>Progetto R: codice e dati</a><a class="button secondary" href="#lezione-${L.id}">◎ Torna alle tappe di ${L.planet}</a></div></header><nav class="lesson-card-nav" aria-label="Esercizi del quaderno">${E.cards.map(c => html`<a href="#esercizi-${L.id}/${c.n}"${c.n === n ? html` aria-current="page"` : ''}><span>${c.n}</span> ${c.title}${state.cards[L.id + ':' + c.n]?.passed ? html` <b aria-label="verificato">✓</b>` : ''}</a>`)}</nav><article class="lesson-card"><p class="eyebrow">Esercizio ${n} di ${E.cards.length} · laboratorio ${card.id}</p><h2>${card.title}</h2><p class="lead">${card.goal}</p><div class="lesson-card-grid"><section><h3>Parametri iniziali</h3><p>${card.start}</p><div class="lab-actions">${scenario('A')}${scenario('B')}</div><h3>Passi</h3><ol>${card.steps.map(t => html`<li>${t}</li>`)}</ol><h3>Domande</h3><ol>${card.questions.map(t => html`<li>${t}</li>`)}</ol><h3>Consegna</h3><p>${card.deliver}</p><p class="lesson-small"><strong>Limiti del modello.</strong> ${card.limits}</p></section><section class="lesson-verify" aria-labelledby="verify-title"><h3 id="verify-title">Verifica dei risultati</h3><p class="lesson-small">Esegui i due scenari nel laboratorio o con il codice qui sotto, poi riporta gli indicatori come li mostra il sito (tre cifre significative). Il controllo accetta la virgola o il punto decimale e non mostra i valori attesi.</p><form id="verify-form" novalidate>${[
      'A',
      'B',
    ].map(
      name =>
        html`<fieldset><legend>Scenario ${name}</legend>${card.fields
          .filter(f => f.scenario === name)
          .map(
            f =>
              html`<label><span>${f.label}</span><input type="text" inputmode="decimal" autocomplete="off" name="${fieldKey(f)}" value="${saved.values[fieldKey(f)] || ''}" aria-describedby="fb-${f.scenario}-${f.key}"><small id="fb-${f.scenario}-${f.key}" class="lesson-feedback" aria-live="polite"></small></label>`,
          )}</fieldset>`,
    )}<button class="button" type="submit">Verifica</button><p id="verify-status" class="lesson-verify-status" role="status">${saved.passed ? 'Esercizio già verificato in questo browser.' : ''}</p></form><label class="lesson-notes-label" for="card-notes">Risposte alle domande e confronto fra gli scenari</label><textarea id="card-notes" class="lab-notes" rows="6" maxlength="${S.limits.notes}">${saved.notes}</textarea><p class="lesson-small">Valori e risposte restano soltanto in questo browser.</p></section></div><section class="lesson-code-section" aria-labelledby="card-code-title"><h3 id="card-code-title">Codice R dell’esercizio</h3><p class="lesson-small">Lo script del quaderno chiama le funzioni del progetto ${L.planet} con i parametri dei due scenari. Scrivi una previsione prima di eseguirlo.</p><p class="lab-engine-state" role="status" aria-live="polite" data-engine></p><article class="lesson-code" data-card><header><h3>${card.script.file}</h3></header><label class="sr-only" for="card-editor">Codice R modificabile dell’esercizio</label><textarea class="lab-editor lesson-editor" id="card-editor" spellcheck="false" maxlength="${S.limits.code}" rows="${Math.min(22, card.script.code.split('\n').length + 1)}">${card.script.code}</textarea><div class="lab-actions"><button type="button" class="button small" data-run>Esegui in R</button><button type="button" class="button small secondary" data-restore>Ripristina</button><button type="button" class="button small secondary" data-download>Scarica .R</button></div><p class="lesson-output-head" data-head>L’uscita comparirà dopo l’esecuzione.</p><pre class="lab-code-output lesson-output" tabindex="0" role="region" aria-label="Uscita di R dell’esercizio" data-output></pre></article></section><nav class="lesson-pager" aria-label="Esercizi vicini">${n > 1 ? html`<a href="#esercizi-${L.id}/${n - 1}">← Esercizio ${n - 1}</a>` : html`<span></span>`}${n < E.cards.length ? html`<a href="#esercizi-${L.id}/${n + 1}">Esercizio ${n + 1} →</a>` : html`<a href="#lezione-${L.id}">Tappe di ${L.planet} →</a>`}</nav></article></div>`;
    const form = main.querySelector('#verify-form'),
      notes = main.querySelector('#card-notes');
    const persist = patch => {
      const st = load();
      st.cards[cardKey] = { ...(st.cards[cardKey] || { values: {}, passed: false, notes: '' }), ...patch };
      save(st);
    };
    form.addEventListener('submit', e => {
      e.preventDefault();
      const values = {};
      let right = 0;
      for (const f of card.fields) {
        const input = form.elements[fieldKey(f)],
          fb = main.querySelector('#fb-' + f.scenario + '-' + f.key),
          ok = check(f, input.value);
        values[fieldKey(f)] = input.value.slice(0, 39);
        input.setAttribute('aria-invalid', String(!ok && input.value.trim() !== ''));
        fb.textContent = !input.value.trim()
          ? 'Da compilare'
          : ok
            ? '✓ Corrisponde'
            : Number.isFinite(parse(input.value))
              ? 'Non corrisponde: controlla scenario, parametri e arrotondamento'
              : 'Scrivi un numero';
        fb.dataset.ok = String(ok);
        if (ok) right++;
      }
      const passed = right === card.fields.length;
      persist({ values, passed: passed || (load().cards[cardKey]?.passed ?? false) });
      main.querySelector('#verify-status').textContent = passed
        ? 'Tutti gli indicatori corrispondono. Completa le risposte alle domande.'
        : right + ' indicatori su ' + card.fields.length + ' corrispondono.';
      announce(main.querySelector('#verify-status').textContent);
    });
    notes.addEventListener('input', () => persist({ notes: notes.value.slice(0, S.limits.notes) }));
    const box = main.querySelector('[data-card]'),
      editor = box.querySelector('textarea');
    box.querySelector('[data-restore]').addEventListener('click', () => (editor.value = card.script.code));
    box
      .querySelector('[data-download]')
      .addEventListener('click', () => download(editor.value + '\n', card.script.file.split('/').pop()));
    box.querySelector('[data-run]').addEventListener('click', async () => {
      const button = box.querySelector('[data-run]');
      button.disabled = true;
      box.querySelector('[data-head]').textContent = 'Esecuzione in R nel browser…';
      try {
        const r = await root.GeoREngine.runSnippet({
          project: L.project,
          code: editor.value,
          edited: editor.value !== card.script.code,
        });
        if (!box.isConnected) return;
        box.querySelector('[data-head]').textContent =
          (r.status === 'ok' ? 'Uscita di R nel browser · ' : 'Uscita di R con errore · ') + r.R;
        box.querySelector('[data-output]').textContent = r.output;
        announce(r.status === 'ok' ? 'Codice eseguito' : 'Il codice ha prodotto un errore');
      } catch (err) {
        if (!box.isConnected) return;
        box.querySelector('[data-head]').textContent = 'Esecuzione non riuscita';
        box.querySelector('[data-output]').textContent = err.message;
      } finally {
        button.disabled = false;
      }
    });
    engineState(main);
  }
  root.GeoLessons = Object.freeze({ configure, cleanup, forWorld, lesson, exercises, check, parse });
})(globalThis);
