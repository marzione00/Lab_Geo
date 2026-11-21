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
    const hit = Object.entries(index()).find(
      ([, l]) => (l.exercisesWorld === world && (l.cards > 0 || l.notebooks > 0)) || l.world === world,
    );
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
  // The slide rebuilt as a site panel: its boxes in the original columns, figures from the TikZ source.
  function slideItem(L, it, page, label) {
    if (it.t === 'label') return html`<p class="lesson-slide-label">${inline(it.c)}</p>`;
    if (it.t === 'p') return html`<p class="lesson-slide-body">${inline(it.c)}</p>`;
    if (it.t === 'small') return html`<p class="lesson-small">${inline(it.c)}</p>`;
    if (it.t === 'info') return html`<p class="lesson-info">${inline(it.c)}</p>`;
    if (it.t === 'math') return html`<div class="math">\\[${it.v}\\]</div>`;
    if (it.t === 'figure')
      return html`<figure class="lesson-figure"><img src="${it.src}" alt="${it.alt || 'Figura della slide ' + page + (label ? ': ' + label : '')}" width="${it.w}" height="${it.h}" style="width:${Math.round(it.ratio * 1000) / 10}%" loading="lazy"></figure>`;
    if (it.t === 'out') return html`<pre class="lesson-slide-output">${it.v}</pre>`;
    if (it.t === 'code')
      return html`<div class="lesson-slide-code"><div class="lesson-slide-code-head"><span>${it.title}</span><button type="button" data-goto="${it.file}">Modifica ed esegui ↓</button></div><pre><code>${root.GeoCodeGuide ? root.GeoCodeGuide.highlight(L.code[it.file].code) : L.code[it.file].code}</code></pre></div>`;
    if (it.t === 'table')
      return html`<div class="lesson-table-wrap"><table class="lesson-table">${it.head.length ? html`<thead>${it.head.map(r => html`<tr>${r.map(c => html`<th${c.span ? html` colspan="${c.span}"` : ''}>${inline(c.c)}</th>`)}</tr>`)}</thead>` : ''}<tbody>${it.rows.map(r => html`<tr>${r.map(c => html`<td${c.span ? html` colspan="${c.span}"` : ''}>${inline(c.c)}</td>`)}</tr>`)}</tbody></table></div>`;
    if (it.t === 'lab')
      return html`<p><a class="button small secondary" href="${labUrl(it.lab)}">${inline(it.c)} ↗</a></p>`;
    return '';
  }
  function column(L, list, page) {
    let label = '';
    return html`<div class="lesson-col">${list.map(it => {
      if (it.t === 'label') label = text(it.c);
      return slideItem(L, it, page, label);
    })}</div>`;
  }
  const text = list => list.map(n => (typeof n === 'string' ? n : n.v || text(n.c || []))).join('');
  function recallBox(label, nodes) {
    return html`<div class="lesson-panel-recall"><span>${label}</span><p>${inline(nodes)}</p></div>`;
  }
  function slidePanel(L, s) {
    const page = s.page;
    if (s.lines)
      return html`<section class="lesson-panel lesson-slide-panel" aria-label="Slide 1: ${s.title}"><figure class="lesson-figure lesson-cover"><img src="${s.image}" alt="Copertina della lezione: ${s.lines.join(', ')}" width="1134" height="709"></figure></section>`;
    if (s.question)
      return html`<section class="lesson-panel lesson-slide-panel" aria-label="Slide 2: ${s.title}"><p class="lesson-slide-label">Domanda centrale</p><p class="lesson-question">${s.question}</p><div class="lesson-steps">${s.steps.map(
        t => {
          const [head, ...rest] = t.split(' · ');
          return html`<div><span>${head}</span><p>${rest.join(' · ')}</p></div>`;
        },
      )}</div>${recallBox('Idea guida', s.recall)}</section>`;
    const by = col => s.items.filter(it => it.col === col),
      wide = by('W'),
      left = by('L'),
      right = by('R');
    // A full-width box sits above; left and right boxes keep their columns, a single one spans the panel.
    return html`<section class="lesson-panel lesson-slide-panel" aria-label="Slide ${page}: ${s.title}">${
      wide.length ? html`<div class="lesson-columns wide">${column(L, wide, page)}</div>` : ''
    }${
      left.length && right.length
        ? html`<div class="lesson-columns">${column(L, left, page)}${column(L, right, page)}</div>`
        : left.length || right.length
          ? html`<div class="lesson-columns wide">${column(L, [...left, ...right], page)}</div>`
          : ''
    }${s.recall.length ? recallBox('Da ricordare', s.recall) : ''}</section>`;
  }

  // ---------------------------------------------------------------- R code of a slide
  // Slide of a fragment: the numeric prefix of the file (M01-M12) or the first slide citing it (T00, M13-M16).
  const pageOf = (L, file) => L.code[file].page || parseInt(file, 10);
  function script(L, file, code) {
    const c = L.code[file],
      head =
        '# ' +
        L.planet +
        ' · tappa ' +
        pageOf(L, file) +
        ' · ' +
        file +
        '\n# Eseguire dalla cartella del progetto ' +
        L.planet +
        ' (archivio della lezione).\n' +
        '# Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0\n' +
        '# Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)\n\n';
    if (c.lang === 'python') return head + code + '\n';
    return (
      head +
      (L.project.setup ? 'source("' + L.project.setup + '", encoding = "UTF-8")\n' : '') +
      c.deps.map(d => '\n# Dalla slide ' + pageOf(L, d) + ' (' + d + ')\n' + L.code[d].code + '\n').join('') +
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
      id = 'code-' + it.file.replace(/[^\w-]/g, '-'),
      python = c.lang === 'python',
      needs = c.needs || [],
      depLinks = html`${c.deps.map((d, i) => html`${i ? ', ' : ''}<a href="#lezione-${L.id}/${pageOf(L, d)}"><code>${d}</code></a>`)}`,
      deps = python
        ? 'Esempio Python: legge i dati della cartella del progetto.'
        : !L.project.setup
          ? 'Il codice è autonomo: legge i dati della cartella del progetto e non richiede altri file.'
          : c.deps.length
            ? html`Prima di questo codice vengono eseguiti, senza mostrarli, <code>${L.project.setup}</code> e ${depLinks}.`
            : html`Prima di questo codice viene eseguito, senza mostrarlo, <code>${L.project.setup}</code>.`,
      local = python
        ? html`<p class="lesson-local">Il browser esegue soltanto R: scarica lo script ed eseguilo con Python 3 dalla cartella del progetto. L’uscita attesa è quella registrata con Python.</p>`
        : needs.length
          ? html`<p class="lesson-local">Questo codice usa ${needs.map((p, i) => html`${i ? ', ' : ''}<code>${p}</code>`)}, che il browser non può caricare: scaricalo ed eseguilo in R sul computer. L’uscita attesa è quella registrata in R.</p>`
          : '';
    return html`<article class="lesson-code" data-file="${it.file}"><header><h3>${it.title}</h3><code>${opts.path || 'Codice/' + it.file}</code></header><p class="lesson-small">${deps}</p>${local}<label class="sr-only" for="${id}">Codice ${python ? 'Python' : 'R'} modificabile · ${it.file}</label><textarea class="lab-editor lesson-editor" id="${id}" spellcheck="false" maxlength="${S.limits.code}" rows="${Math.min(22, c.code.split('\n').length + 1)}">${c.code}</textarea><div class="lab-actions"><button type="button" class="button small" data-run${needs.length ? ' disabled' : ''}>Esegui in R</button><button type="button" class="button small secondary" data-restore>Ripristina il codice della slide</button><button type="button" class="button small secondary" data-copy-code>Copia</button><button type="button" class="button small secondary" data-download>Scarica ${python ? '.py' : '.R'}</button></div><p class="lesson-output-head" data-head>Uscita attesa</p><pre class="lab-code-output lesson-output" tabindex="0" role="region" aria-label="Uscita di ${python ? 'Python' : 'R'} · ${it.file}" data-output>${c.output}</pre><div class="lesson-figures" data-figures></div></article>`;
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
  // Region names come from the uppercase section titles of the decks: sentence case, keeping the
  // roman numeral of the part, acronyms and proper names.
  const KEEP = new Set(['R', 'ADF', 'ARIMA', 'GEV', 'KPSS', 'PCA']),
    NAMES = {
      BERNOULLI: 'Bernoulli',
      POISSON: 'Poisson',
      GUMBEL: 'Gumbel',
      WARD: 'Ward',
      MONTE: 'Monte',
      CARLO: 'Carlo',
      TERRA: 'Terra',
    };
  const regionName = t => {
    const [, part = '', rest] = /^([IVX]+ · )?(.*)$/.exec(t),
      words = rest
        .split(/(\s+)/)
        .map(w => (KEEP.has(w) ? w : NAMES[w] || w.toLowerCase()))
        .join('');
    return part + words.charAt(0).toUpperCase() + words.slice(1);
  };
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
  // Systems take the name of their star, as in the galaxy view.
  const system = id => root.GeoAstro?.generate(id, 0)?.name || id;
  function crumbs(L, extra) {
    return html`<div class="breadcrumb"><a href="#indice">Galassia</a><span>/</span><a href="#sistema-${L.id}">Sistema ${system(L.id)}</a><span>/</span><a href="#lezione-${L.id}">${L.planet} · Lezione ${L.id}</a>${extra ? html`<span>/</span><span>${extra}</span>` : ''}</div>`;
  }
  function overview(main, L) {
    const done = new Set(load().done);
    main.innerHTML = html`<div class="wrap lesson-overview">${crumbs(L)}<header class="module-head lesson-head"><p class="eyebrow">${L.id} · PIANETA ${L.planet.toUpperCase()} · LEZIONE</p><h1>${L.title}</h1><div class="lesson-intro">${blocks(L.intro)}</div><div class="lab-actions"><a class="button" href="#lezione-${L.id}/2">Inizia dalla tappa 2 →</a><a class="button secondary" href="${L.pdf}" target="_blank" rel="noopener">PDF della lezione con i codici di tappa ↗</a><a class="button secondary" href="${L.download}" download>Progetto R: codice e dati</a>${L.exercises ? html`<a class="button secondary" href="#esercizi-${L.id}">Quaderno degli esercizi →</a>` : ''}</div></header><section class="lesson-regions" aria-label="Regioni del pianeta">${L.sections
      .filter(sec => !L.slides.slice(sec.first - 1, sec.last).every(s => s.lines || s.question))
      .map(sec => {
        const tappe = L.slides.slice(sec.first - 1, sec.last);
        return html`<article class="lesson-region-card"><p class="eyebrow">Tappe ${sec.first}–${sec.last}</p><h2>${regionName(sec.title)}</h2><p class="lesson-small">${tappe.length} tappe · ${tappe.filter(s => done.has(L.id + ':' + s.page)).length} studiate</p><ol start="${sec.first}">${tappe.map(s => html`<li><a href="#lezione-${L.id}/${s.page}">${s.title}</a></li>`)}</ol></article>`;
      })}</section></div>`;
    typeset(main.querySelector('.lesson-intro'));
  }
  function notebookPanel(L, page) {
    const list = (L.notebooks || []).filter(nb => nb.pages.includes(page));
    if (!list.length) return '';
    return html`<section class="lesson-panel lesson-labs" aria-labelledby="lesson-nb-title"><h2 id="lesson-nb-title">Notebook svolto</h2><ul>${list.map(nb => html`<li><a class="button secondary" href="${nb.html}" target="_blank" rel="noopener">${nb.id} · ${nb.title} ↗</a></li>`)}</ul><p class="lesson-small">Il notebook riprende la slide con un’esercitazione svolta in R. I sorgenti sono sul <a href="#esercizi-${L.id}">pianeta compagno</a>.</p></section>`;
  }
  function codePanel(L, codes) {
    if (!codes.length) return '';
    const heading = codes.some(it => L.code[it.file].lang === 'python')
      ? 'Codice R e Python della slide'
      : 'Codice R della slide';
    return html`<section class="lesson-panel lesson-code-section" aria-labelledby="lesson-code-title"><h2 id="lesson-code-title">${heading}</h2><p class="lesson-small">Modifica il codice ed eseguilo: R lavora su questo dispositivo, nella cartella del progetto ${L.planet}. Esegui soltanto codice di cui conosci la provenienza.</p><p class="lab-engine-state" role="status" aria-live="polite" data-engine></p>${codes.map(it => codeBox(L, it))}</section>`;
  }
  function tappa(main, L, page, announce) {
    const s = L.slides[page - 1],
      sec = L.sections.find(x => page >= x.first && page <= x.last),
      state = load(),
      doneKey = L.id + ':' + page,
      // Code cited by the slide, then code of the slide that the PDF shows but the source does not cite.
      codes = [...s.items.filter(it => it.t === 'code'), ...(s.code || [])],
      labs = [
        ...s.items.filter(it => it.t === 'lab').map(it => ({ id: it.lab, params: {}, title: null })),
        ...(s.labs || []),
      ],
      prev = L.slides[page - 2],
      next = L.slides[page];
    main.innerHTML = html`<div class="viewer lesson-viewer">${crumbs(L, 'Tappa ' + page)}<div class="reader-layout">${sidebar(L, page)}<div class="reader-main lesson-main"><div class="reader-title"><h1>${s.title}</h1><span class="page-counter">${String(page).padStart(2, '0')} / ${L.pages}</span></div><div class="reader-tools"><p class="lesson-stop"><span class="lesson-stop-code">${L.planet} · ${page}</span> ${regionName(sec.title)}${sec.first < sec.last ? ' · tappe ' + sec.first + '–' + sec.last : ''}</p><div class="pager"><button data-step="-1" aria-label="Tappa precedente"${prev ? '' : ' disabled'}>←</button><button data-step="1" aria-label="Tappa successiva"${next ? '' : ' disabled'}>→</button></div></div>${slidePanel(L, s)}<div class="slide-caption lesson-caption"><span>Slide originale</span><a href="${L.pdf}#page=${page}" target="_blank" rel="noopener">Pagina ${page} del PDF ↗</a></div>${L.notes[page] ? html`<section class="lesson-panel lesson-notes" aria-label="Commento alla slide ${page}">${blocks(L.notes[page])}</section>` : ''}${codePanel(L, codes)}${notebookPanel(L, page)}${
      labs.length
        ? html`<section class="lesson-panel lesson-labs" aria-labelledby="lesson-labs-title"><h2 id="lesson-labs-title">Laboratorio</h2><ul>${labs.map(
            lab => {
              const a = root.GeoLabs?.byId.get(lab.id);
              return a
                ? html`<li><a class="button secondary" href="${labUrl(lab.id, lab.params)}">${a.title}${Object.keys(lab.params).length ? html` · ${paramText(lab.params)}` : ' · parametri iniziali'} ↗</a></li>`
                : '';
            },
          )}</ul><p class="lesson-small">I pulsanti aprono il laboratorio del sito con i parametri della slide, ricavati dal codice o dallo scenario; i parametri non indicati restano ai valori iniziali.</p></section>`
        : ''
    }<nav class="lesson-pager" aria-label="Tappe vicine">${prev ? html`<a href="#lezione-${L.id}/${prev.page}">← ${prev.page} · ${prev.title}</a>` : html`<span></span>`}${
      next
        ? html`<a href="#lezione-${L.id}/${next.page}">${next.page} · ${next.title} →</a>`
        : L.exercises
          ? html`<a href="#esercizi-${L.id}">Quaderno degli esercizi →</a>`
          : html`<a href="#sistema-${L.id}">Sistema ${system(L.id)} →</a>`
    }</nav><div class="study-actions"><button id="lesson-done" class="button small secondary${state.done.includes(doneKey) ? ' done' : ''}" aria-pressed="${state.done.includes(doneKey)}">${state.done.includes(doneKey) ? '✓ Tappa studiata' : 'Segna la tappa come studiata'}</button><p>Il progresso resta soltanto in questo browser.</p></div></div></div></div>`;
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
    main.querySelectorAll('[data-goto]').forEach(b =>
      b.addEventListener('click', () => {
        const box = main.querySelector('.lesson-code[data-file="' + b.dataset.goto + '"]');
        box?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        box?.querySelector('textarea').focus({ preventScroll: true });
      }),
    );
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
  const fieldKey = f => f.scenario + ':' + f.key;
  // Verification of the indicators, or (workbooks without expected values) the table the workbook asks for.
  function verifySection(card, saved) {
    if (!card.fields.length) {
      const [first, ...cols] = card.table || ['Scenario'];
      return html`<section class="lesson-verify" aria-labelledby="verify-title"><h3 id="verify-title">Tabella del confronto</h3><p class="lesson-small">Esegui i due scenari nel laboratorio o con il codice qui sotto e riporta i valori come li chiede il quaderno. Il quaderno non indica valori attesi: la tabella serve al confronto fra gli scenari.</p><form id="table-form" novalidate><div class="lesson-table-wrap"><table class="lesson-table"><thead><tr><th>${first}</th>${cols.map(c => html`<th>${c}</th>`)}</tr></thead><tbody>${[
        'A',
        'B',
      ].map(
        name =>
          html`<tr><td>Scenario ${name}</td>${cols.map(
            (c, i) =>
              html`<td><input type="text" autocomplete="off" name="${name}:${i}" aria-label="${c}, scenario ${name}" value="${saved.values[name + ':' + i] || ''}"></td>`,
          )}</tr>`,
      )}</tbody></table></div></form>`;
    }
    return html`<section class="lesson-verify" aria-labelledby="verify-title"><h3 id="verify-title">Verifica dei risultati</h3><p class="lesson-small">Esegui i due scenari nel laboratorio o con il codice qui sotto, poi riporta gli indicatori come li mostra il sito (tre cifre significative). Il controllo accetta la virgola o il punto decimale e non mostra i valori attesi.</p><form id="verify-form" novalidate>${[
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
    )}<button class="button" type="submit">Verifica</button><p id="verify-status" class="lesson-verify-status" role="status">${saved.passed ? 'Esercizio già verificato in questo browser.' : ''}</p></form>`;
  }
  // Solved notebooks (M01-M12): pages of their own, opened in a new tab; sources in one archive per lesson.
  function notebooksSection(L) {
    if (!L.notebooks?.length) return '';
    return html`<section class="lesson-panel lesson-notebooks" aria-labelledby="nb-title"><h2 id="nb-title">Notebook svolti</h2><p class="lesson-small">Ogni notebook è un’esercitazione svolta in R Markdown, con domanda, codice eseguito, uscite e grafici. La pagina si apre in una nuova scheda; l’archivio contiene i sorgenti .Rmd, le funzioni comuni e i dati per rieseguirli in RStudio.</p><div class="lab-actions"><a class="button secondary" href="${L.notebookDownload}" download>Sorgenti dei notebook · ZIP</a></div><ol class="lesson-notebook-list">${L.notebooks.map(
      nb =>
        html`<li><a href="${nb.html}" target="_blank" rel="noopener">${nb.id} · ${nb.title} ↗</a><small>${nb.blocks} blocchi eseguiti${nb.figures ? ' · ' + nb.figures + (nb.figures === 1 ? ' grafico' : ' grafici') : ''}${nb.pages.length ? html` · tappe ${nb.pages.map((p, i) => html`${i ? ', ' : ''}<a href="#lezione-${L.id}/${p}">${p}</a>`)}` : ''}</small></li>`,
    )}</ol></section>`;
  }
  function notebookPage(main, L) {
    const world = root.GeoAstro?.generate(L.id, 0)?.planets.find(p => p.id === L.exercisesWorld),
      worldName = world?.name || L.exercisesWorld;
    main.innerHTML = html`<div class="wrap lesson-exercises"><div class="breadcrumb"><a href="#indice">Galassia</a><span>/</span><a href="#sistema-${L.id}">Sistema ${system(L.id)}</a><span>/</span><span>${worldName} · Notebook</span></div><header class="module-head lesson-head"><p class="eyebrow">${L.id} · ${worldName.toUpperCase()} · PIANETA COMPAGNO</p><h1>Notebook di ${L.planet}</h1><p class="lead">${L.notebooks.length} notebook svolti accompagnano la lezione su ${L.planet}: ciascuno riprende i concetti delle tappe con un’esercitazione completa in R.</p><div class="lab-actions"><a class="button secondary" href="#lezione-${L.id}">◎ Torna alle tappe di ${L.planet}</a></div></header>${notebooksSection(L)}</div>`;
  }
  function exercises(main, L, n, announce = () => {}) {
    cleanup();
    if (!L.exercises) return notebookPage(main, L);
    const E = L.exercises,
      card = E.cards[n - 1],
      cardKey = L.id + ':' + n,
      state = load(),
      saved = state.cards[cardKey] || { values: {}, passed: false, notes: '' },
      world = root.GeoAstro?.generate(L.id, 0)?.planets.find(p => p.id === L.exercisesWorld),
      worldName = world?.name || L.exercisesWorld;
    const scenario = name =>
      html`<a class="button secondary" href="${labUrl(card.id, card.scenarios[name].link.params)}">Scenario ${name} nel laboratorio${Object.keys(card.scenarios[name].link.params).length ? html` · ${paramText(card.scenarios[name].link.params)}` : ''} ↗</a>`;
    main.innerHTML = html`<div class="wrap lesson-exercises"><div class="breadcrumb"><a href="#indice">Galassia</a><span>/</span><a href="#sistema-${L.id}">Sistema ${system(L.id)}</a><span>/</span><a href="#esercizi-${L.id}">${worldName} · Esercizi</a><span>/</span><span>Esercizio ${n}</span></div><header class="module-head lesson-head"><p class="eyebrow">${L.id} · ${worldName.toUpperCase()} · PIANETA DEGLI ESERCIZI</p><h1>Quaderno di ${L.planet}</h1><p class="lead">${E.subtitle}${/[.!?]$/.test(E.subtitle) ? '' : '.'} Gli esercizi usano i concetti delle tappe della lezione su ${L.planet}.</p><details class="lesson-common"><summary>Istruzioni comuni</summary><ol>${E.common.map(t => html`<li>${t}</li>`)}</ol></details><div class="lab-actions"><a class="button secondary" href="${L.workbook}" target="_blank" rel="noopener">Quaderno in PDF ↗</a><a class="button secondary" href="${L.download}" download>Progetto R: codice e dati</a><a class="button secondary" href="#lezione-${L.id}">◎ Torna alle tappe di ${L.planet}</a></div></header><nav class="lesson-card-nav" aria-label="Esercizi del quaderno">${E.cards.map(c => html`<a href="#esercizi-${L.id}/${c.n}"${c.n === n ? html` aria-current="page"` : ''}><span>${c.n}</span> ${c.title}${state.cards[L.id + ':' + c.n]?.passed ? html` <b aria-label="verificato">✓</b>` : ''}</a>`)}</nav><article class="lesson-card"><p class="eyebrow">Esercizio ${n} di ${E.cards.length} · laboratorio ${card.id}</p><h2>${card.title}</h2><p class="lead">${card.goal}</p><div class="lesson-card-grid"><section><h3>Parametri iniziali</h3><p>${card.start}</p><div class="lab-actions">${scenario('A')}${scenario('B')}</div><h3>Passi</h3><ol>${card.steps.map(t => html`<li>${t}</li>`)}</ol><h3>Domande</h3><ol>${card.questions.map(t => html`<li>${t}</li>`)}</ol>${card.deliver ? html`<h3>Consegna</h3><p>${card.deliver}</p>` : ''}<p class="lesson-small"><strong>Limiti del modello.</strong> ${card.limits}</p></section>${verifySection(card, saved)}<label class="lesson-notes-label" for="card-notes">Risposte alle domande e confronto fra gli scenari</label><textarea id="card-notes" class="lab-notes" rows="6" maxlength="${S.limits.notes}">${saved.notes}</textarea><p class="lesson-small">Valori e risposte restano soltanto in questo browser.</p></section></div><section class="lesson-panel lesson-code-section" aria-labelledby="card-code-title"><h3 id="card-code-title">Codice R dell’esercizio</h3><p class="lesson-small">Lo script del quaderno chiama le funzioni del progetto ${L.planet} con i parametri dei due scenari. Scrivi una previsione prima di eseguirlo.</p><p class="lab-engine-state" role="status" aria-live="polite" data-engine></p><article class="lesson-code" data-card><header><h3>${card.script.file}</h3></header><label class="sr-only" for="card-editor">Codice R modificabile dell’esercizio</label><textarea class="lab-editor lesson-editor" id="card-editor" spellcheck="false" maxlength="${S.limits.code}" rows="${Math.min(22, card.script.code.split('\n').length + 1)}">${card.script.code}</textarea><div class="lab-actions"><button type="button" class="button small" data-run>Esegui in R</button><button type="button" class="button small secondary" data-restore>Ripristina</button><button type="button" class="button small secondary" data-download>Scarica .R</button></div><p class="lesson-output-head" data-head>L’uscita comparirà dopo l’esecuzione.</p><pre class="lab-code-output lesson-output" tabindex="0" role="region" aria-label="Uscita di R dell’esercizio" data-output></pre></article></section><nav class="lesson-pager" aria-label="Esercizi vicini">${n > 1 ? html`<a href="#esercizi-${L.id}/${n - 1}">← Esercizio ${n - 1}</a>` : html`<span></span>`}${n < E.cards.length ? html`<a href="#esercizi-${L.id}/${n + 1}">Esercizio ${n + 1} →</a>` : html`<a href="#lezione-${L.id}">Tappe di ${L.planet} →</a>`}</nav></article>${notebooksSection(L)}</div>`;
    const form = main.querySelector('#verify-form'),
      table = main.querySelector('#table-form'),
      notes = main.querySelector('#card-notes');
    const persist = patch => {
      const st = load();
      st.cards[cardKey] = { ...(st.cards[cardKey] || { values: {}, passed: false, notes: '' }), ...patch };
      save(st);
    };
    table?.addEventListener('input', () =>
      persist({ values: Object.fromEntries([...table.elements].map(i => [i.name, i.value.slice(0, 39)])) }),
    );
    form?.addEventListener('submit', e => {
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
