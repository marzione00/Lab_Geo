/* Five reproducible investigations on frozen observations; fictional worlds are navigation. */
(function (root) {
  'use strict';
  const esc = root.GeoHTML.escape;
  const projects = root.GEO_RESEARCH || [],
    byWorld = Object.fromEntries(projects.map(p => [p.worldId, p]));
  let dispose = null;
  function forWorld(id) {
    if (byWorld[id]) return byWorld[id];
    const m = /^(T00|M(?:0[1-9]|1[0-6]))-([b-f])$/.exec(id || '');
    if (!m) return null;
    const f = root.GeoFamilies.forWorld(m[1] === 'T00' ? 0 : Number(m[1].slice(1)), m[2].charCodeAt(0) - 98, id);
    return projects.find(p => p.level === f.level) || null;
  }
  function cleanup() {
    dispose?.();
    dispose = null;
  }
  function familyCard(p) {
    const f = root.GeoFamilies.byId[p.familyId];
    if (!f) return '';
    return `<div class="family-card" data-level="${f.level}"><span>L${f.level} / ${esc(root.GeoFamilies.levels[f.level])}</span><strong>${esc(f.name)}</strong><p>${esc(root.GeoFamilies.hospitality[f.level])} · ${esc(f.description)}</p><details><summary>Come leggere il livello</summary><p>${esc(root.GeoFamilies.criteria[f.level])}</p><p>${esc(root.GeoFamilies.note)}</p></details></div>`;
  }
  function index() {
    if (!projects.length) return '';
    return `<details class="research-index"><summary><span>MISSIONI SU DATI REALI</span><strong>Cinque progetti · da L1 a L5</strong><small>USGS · NASA/JPL · NOAA/NSIDC · NASA</small></summary><p class="research-intro">Scegli il grado di autonomia con cui vuoi lavorare. Le cinque missioni sono condivise dai mondi di pari livello; ciascuna conserva il campione osservato, la sua provenienza e il programma R che produce le figure.</p><div class="research-cards">${projects.map(p => `<a href="#esplorazione/${p.worldId}"><span>L${p.level} · ${esc(root.GeoFamilies.levels[p.level])}</span><strong>${esc(p.title)}</strong><small>${esc(p.question)}</small><b>Apri la missione ↗</b></a>`).join('')}</div><p class="instrument-note">${esc(root.GeoFamilies.note)}</p></details>`;
  }
  function script(p, params, body = p.code) {
    return (
      '# GeoStat Lab · ' +
      p.title +
      '\n# Dati osservati: consultare provenance.json.\n# Estrarre il pacchetto; impostare questa cartella come directory di lavoro.\n# install.packages("ggplot2")\n\n' +
      root.GEO_LABS.common +
      '\n' +
      root.GeoCodeGuide.parameterScript(p, params) +
      '\n\n# Legge la copia locale documentata, senza interrogare servizi esterni.\nobservations <- read.csv("data.csv", stringsAsFactors=FALSE, check.names=FALSE)\n\n' +
      body +
      '\n\nprint(metrics, row.names=FALSE)\nfor (i in seq_along(plots)) {\n  print(plots[[i]])\n  ggsave(paste0("figura_",i,".pdf"),plots[[i]],width=9,height=5.5)\n}\nwrite.csv(data,"risultati.csv",row.names=FALSE)\n'
    );
  }
  function download(text, name, type) {
    const u = URL.createObjectURL(new Blob([text], { type })),
      a = document.createElement('a');
    a.href = u;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(u), 1500);
  }
  async function readDataset(p, signal) {
    const response = await fetch('assets/research/' + p.id + '/data.csv', { signal, credentials: 'same-origin' });
    if (!response.ok) throw Error('Il campione non è disponibile: scarica il pacchetto della missione.');
    const bytes = await response.arrayBuffer();
    if (bytes.byteLength > 2000000) throw Error('Campione oltre il limite previsto.');
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), b =>
      b.toString(16).padStart(2, '0'),
    ).join('');
    if (hash !== p.dataSHA256)
      throw Error('Il campione non corrisponde alla versione documentata. Ricarica la pagina.');
    return new TextDecoder().decode(bytes);
  }
  function mount(host, p) {
    cleanup();
    let active = true,
      busy = false,
      urls = [],
      result = null,
      controller = null;
    let params = Object.fromEntries(p.controls.map(c => [c.key, c.value]));
    const path = 'assets/research/' + p.id + '/';
    host.innerHTML = `<section class="research-mission" data-research="${esc(p.id)}"><p class="eyebrow">ARCHIVIO OSSERVATIVO / MISSIONE L${p.level}</p>${p.narrative.map(t => '<p>' + esc(t) + '</p>').join('')}<div class="research-brief"><h2>Il problema da indagare</h2><p>${esc(p.question)}</p><ol>${p.steps.map(t => '<li>' + esc(t) + '</li>').join('')}</ol></div><section class="research-formalism"><h2>Relazione statistica</h2><div class="math">\\[${esc(p.formula)}\\]</div><p>${esc(p.formulaExplanation)}</p></section><div class="research-provenance"><strong>Campione locale · ${p.rows} osservazioni</strong><span>Acquisizione: ${esc(p.retrievedAt || 'documentata nel manifesto')}</span><a href="${path}provenance.json" download>Provenienza e dizionario dei dati ↓</a></div><div class="research-workbench"><section class="research-controls" aria-labelledby="research-control-title"><h2 id="research-control-title">Configura l’indagine</h2><form id="research-form">${p.controls.map(c => `<label for="research-${c.key}">${esc(c.label)}${c.type === 'select' ? `<select id="research-${c.key}" name="${c.key}">${c.options.map(o => `<option value="${esc(o.value)}"${o.value === c.value ? ' selected' : ''}>${esc(o.label)}</option>`).join('')}</select>` : `<input id="research-${c.key}" name="${c.key}" type="number" value="${c.value}" min="${c.min}" max="${c.max}" step="${c.step}">`}${c.help ? '<small>' + esc(c.help) + '</small>' : ''}</label>`).join('')}<button class="button" type="submit">Esegui l’analisi in R</button><button class="button secondary" type="button" id="research-stop" hidden>Interrompi il calcolo</button></form><p id="research-engine" role="status">R viene avviato al primo calcolo.</p><a class="research-download" href="${path}project.zip" download>Pacchetto R + dati + provenienza ↓</a><a class="research-download" href="${path}data.csv" download>Campione CSV ↓</a></section><div class="research-terminal-column"><p class="research-input-code">Il campione viene caricato nell’oggetto <code>observations</code>. Nel programma scaricabile: <code>observations &lt;- read.csv("data.csv")</code>.</p><div class="research-terminal"></div></div></div><section class="research-results" aria-labelledby="research-results-title"><h2 id="research-results-title">Risultati dell’indagine</h2><p class="research-result-state" role="status">Anteprima calcolata in R con i parametri iniziali. Il pulsante ricalcola figure e statistiche sul tuo dispositivo.</p><div class="research-figures">${Array.from({ length: p.plotCount || 1 }, (_, i) => `<figure><a href="${path}figure-${i + 1}.svg" target="_blank" rel="noopener" aria-label="Ingrandisci figura ${i + 1}"><img src="${path}figure-${i + 1}.svg" alt="${esc(p.title)}: figura ${i + 1} prodotta dal codice R, parametri iniziali"></a><figcaption>Figura ${i + 1} · configurazione iniziale · seleziona per ingrandire</figcaption></figure>`).join('')}</div><div class="research-metrics"></div><div class="research-table"></div><button class="button secondary" id="research-export" type="button" hidden>Scarica i risultati CSV</button></section><details class="research-limits" open><summary>Interpretazione e limiti</summary><ul>${p.limitations.map(t => '<li>' + esc(t) + '</li>').join('')}</ul></details><section class="research-sources"><h2>Fonti dei dati</h2><ul>${p.sources.map(s => '<li><a href="' + esc(s.url) + '" target="_blank" rel="noopener noreferrer">' + esc(s.label) + '</a></li>').join('')}</ul><p>Il pianeta è una destinazione immaginaria: le osservazioni riguardano gli oggetti reali descritti nelle fonti.</p></section></section>`;
    const $ = s => host.querySelector(s),
      form = $('#research-form'),
      status = $('#research-engine'),
      state = $('.research-result-state');
    const terminal = root.GeoSolutions.mount($('.research-terminal'), p, root.GeoSolutions.guides().research[p.id], {
      params,
      execute: execute,
      dirty: markDirty,
      download: () => download(script(p, params), p.id + '.R', 'text/plain;charset=utf-8'),
      downloadBody: body => download(script(p, params, body), p.id + '-variante.R', 'text/plain;charset=utf-8'),
    });
    function read() {
      const values = {};
      for (const c of p.controls)
        values[c.key] = c.type === 'select' ? form.elements[c.key].value : Number(form.elements[c.key].value);
      return root.GeoSecurity.parameters(p, values);
    }
    function markDirty(message) {
      state.textContent = message;
      terminal.invalidate(message);
      $('#research-export').disabled = true;
    }
    form.addEventListener('input', () => {
      try {
        params = read();
        terminal.update(params);
        markDirty(
          'Parametri modificati. I grafici mostrano l’ultima configurazione calcolata; esegui R per aggiornarli.',
        );
      } catch {
        markDirty('Controlla i valori: ogni parametro deve rispettare il proprio intervallo.');
      }
    });
    const unsubscribe = root.GeoREngine.subscribe(s => {
      if (active && busy) status.textContent = s.text;
    });
    $('#research-stop').addEventListener('click', () => {
      controller?.abort();
      root.GeoREngine.reset();
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      execute({ body: p.code, partial: false, custom: false, step: null });
    });
    async function execute(context) {
      if (busy) return;
      controller = new AbortController();
      const signal = controller.signal;
      try {
        params = read();
        terminal.update(params);
        busy = true;
        terminal.setBusy(true);
        markDirty('Calcolo in corso; i risultati precedenti restano distinti dalla nuova esecuzione.');
        form.querySelector('[type="submit"]').disabled = true;
        for (const input of form.querySelectorAll('input,select')) input.disabled = true;
        $('#research-stop').hidden = false;
        status.textContent = 'Verifica della copia locale del campione…';
        const csv = await readDataset(p, signal);
        if (!active) return;
        signal.throwIfAborted();
        const computed = await root.GeoREngine.run(
          context.partial ? { ...p, code: context.body } : p,
          params,
          context.body,
          csv,
          { partial: context.partial },
        );
        if (!active) return;
        signal.throwIfAborted();
        result = computed;
        for (const u of urls) URL.revokeObjectURL(u);
        urls = [];
        const figures = $('.research-figures');
        figures.replaceChildren();
        if (!result.figures.length) {
          const note = document.createElement('p');
          note.textContent =
            'Questo passaggio produce una tabella o statistiche intermedie; i grafici vengono costruiti nei passaggi successivi.';
          figures.append(note);
        }
        for (const [i, svg] of result.figures.entries()) {
          const figure = document.createElement('figure'),
            im = document.createElement('img'),
            caption = document.createElement('figcaption');
          const u = URL.createObjectURL(new Blob([root.GeoSecurity.svg(svg)], { type: 'image/svg+xml' }));
          urls.push(u);
          im.src = u;
          im.alt = p.title + ' · figura ' + (i + 1);
          caption.textContent = 'Figura ' + (i + 1) + ' · ricalcolata in R';
          const link = document.createElement('a');
          link.href = u;
          link.target = '_blank';
          link.rel = 'noopener';
          link.setAttribute('aria-label', 'Ingrandisci figura ' + (i + 1));
          link.append(im);
          caption.textContent += ' · seleziona per ingrandire';
          figure.append(link, caption);
          figures.append(figure);
        }
        $('.research-metrics').innerHTML =
          '<dl>' +
          result.metrics
            .map(
              row =>
                '<div><dt>' +
                esc(row.grandezza ?? Object.values(row)[0]) +
                '</dt><dd>' +
                esc(row.valore ?? Object.values(row)[1]) +
                '</dd></div>',
            )
            .join('') +
          '</dl>';
        const columns = Object.keys(result.data[0] || {}).slice(0, 8);
        $('.research-table').innerHTML =
          '<details><summary>Osservazioni del risultato · prime ' +
          result.data.length +
          ' righe, fino a 8 colonne</summary><div class="solution-table-scroll" tabindex="0" role="region" aria-label="Dati calcolati"><table><thead><tr>' +
          columns.map(k => '<th scope="col">' + esc(k) + '</th>').join('') +
          '</tr></thead><tbody>' +
          result.data
            .map(row => '<tr>' + columns.map(k => '<td>' + esc(row[k]) + '</td>').join('') + '</tr>')
            .join('') +
          '</tbody></table></div></details>';
        terminal.completed(result, context);
        state.textContent =
          (context.custom ? 'Variante ricalcolata' : context.partial ? 'Risultato intermedio' : 'Analisi ricalcolata') +
          ' · ' +
          result.rows +
          ' righe nel risultato · ' +
          result.R +
          ' · ggplot2 ' +
          result.ggplot2;
        status.textContent = 'Calcolo completato sul dispositivo.';
        $('#research-export').hidden = false;
        $('#research-export').disabled = false;
      } catch (error) {
        if (active) {
          status.textContent = signal.aborted
            ? 'Calcolo interrotto. Puoi avviare una nuova esecuzione.'
            : 'Analisi non completata: ' + error.message;
          markDirty(
            'Calcolo non completato. I risultati precedenti restano visibili e non corrispondono a una nuova esecuzione riuscita.',
          );
        }
      } finally {
        if (active) {
          busy = false;
          terminal.setBusy(false);
          form.querySelector('[type="submit"]').disabled = false;
          for (const input of form.querySelectorAll('input,select')) input.disabled = false;
          $('#research-stop').hidden = true;
        }
      }
    }
    $('#research-export').addEventListener('click', () => {
      if (result) download(root.GeoSecurity.csv(result.csv), p.id + '-risultati.csv', 'text/csv;charset=utf-8');
    });
    dispose = () => {
      active = false;
      controller?.abort();
      unsubscribe();
      terminal.destroy();
      for (const u of urls) URL.revokeObjectURL(u);
      if (busy) root.GeoREngine.reset();
    };
  }
  root.GeoResearch = Object.freeze({ projects, forWorld, familyCard, index, mount, cleanup, script, readDataset });
})(globalThis);
