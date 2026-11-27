/* Pages of the notable objects: the 3D scene, its controls and the scientific card. The engine and the scenes
   load on the first visit (one file with SRI); the catalogue and the texts are already in memory. */
(function (root) {
  'use strict';
  const O = root.GeoObjects,
    { html } = root.GeoHTML;
  const n = (v, d = 2) => v.toLocaleString('it-IT', { maximumFractionDigits: d, minimumFractionDigits: 0 });
  // Number in scientific notation with an Italian decimal comma: 3,2 × 10¹³.
  const sci = (v, d = 2) => {
    if (v === 0) return '0';
    const e = Math.floor(Math.log10(Math.abs(v))),
      m = v / 10 ** e;
    const sup = String(e).replace(/[-0-9]/g, c => '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'['-0123456789'.indexOf(c)]);
    return n(Number(m.toFixed(d)), d) + ' × 10' + sup;
  };
  let engine = null,
    scene = null,
    loading = null,
    token = 0;
  const base = root.document?.currentScript?.src || root.location?.href;
  function cleanup() {
    token++;
    try {
      engine?.dispose();
    } catch {
      /* already released */
    }
    engine = null;
    scene = null;
  }
  // Engine and scenes: one script with SRI, loaded on demand.
  function scenes() {
    if (root.GeoObjectEngine && root.GeoObjectScenes) return Promise.resolve();
    loading ||= new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = new URL('objects-scenes.js', base).href;
      const key = 'assets/objects-scenes.js';
      if (root.GEO_INTEGRITY?.[key]) s.integrity = root.GEO_INTEGRITY[key];
      s.crossOrigin = 'anonymous';
      s.onload = () => (root.GeoObjectEngine ? resolve() : reject(Error('Motore non disponibile')));
      s.onerror = () => {
        loading = null;
        reject(Error('Impossibile caricare la scena'));
      };
      document.head.append(s);
    });
    return loading;
  }
  const C = () => root.GeoObjectTexts;
  function facts(o) {
    return html`<dl class="astro-stats object-stats">${C()
      .facts(o)
      .map(([label, value, unit]) => html`<div><dt>${label}</dt><dd>${value} <small>${unit}</small></dd></div>`)}</dl>`;
  }
  function switcher(id) {
    return html`<nav class="object-switch" aria-label="Oggetti notevoli">${O.objects.map(
      o =>
        html`<a href="#oggetto-${o.id}" class="${o.id === id ? 'current' : ''}" ${o.id === id ? html`aria-current="page"` : ''} style="--object-tone:${o.tone}"><span aria-hidden="true">${o.symbol}</span> ${o.name}<small>${o.short}</small></a>`,
    )}</nav>`;
  }
  function controls(o) {
    const views = C().views?.(o.id) || [];
    return html`<div class="object-controls" role="group" aria-label="Vista ed elementi della scena">${views.map(
      (v, i) =>
        html`<button type="button" class="object-view" data-view="${v.key}" aria-pressed="${String(i === 0)}">${v.label}</button>`,
    )}${C()
      .controls(o.id)
      .map(
        c =>
          html`<button type="button" class="object-toggle" data-option="${c.key}" aria-pressed="${String(c.on)}"><i aria-hidden="true"></i>${c.label}</button>`,
      )}</div>`;
  }
  function render(main, id) {
    cleanup();
    const o = O.byId[id];
    if (!o) return;
    const t = C().page(o, { n, sci });
    main.innerHTML = html`<section class="galaxy-home object-home" aria-labelledby="object-title" style="--object-tone:${o.tone}"><div class="galaxy-heading"><div><p class="eyebrow">OGGETTO NOTEVOLE / ${o.kind.toUpperCase()}</p><h1 id="object-title" tabindex="-1">${o.name}<span>.</span></h1><p>${t.lead}</p></div><a class="galaxy-index" href="#indice">← Torna alla galassia</a></div>
   ${switcher(id)}
   <div class="galaxy-navigation system-navigation object-navigation"><div class="system-stage"><div class="object-chart" role="group" aria-label="${o.kind} ${o.name}" data-object="${o.id}">
    <canvas id="object-viewport" tabindex="0" role="img" aria-label="${t.canvas}"></canvas><div class="galaxy-corners" aria-hidden="true"></div>
    <div class="galaxy-chart-heading"><span class="galaxy-beacon"></span><span>${t.instrument}<small>${o.name.toUpperCase()} / ${t.scale}</small></span></div>
    <div class="galaxy-camera"><button type="button" data-object-camera="in" aria-label="Avvicina la camera">+</button><button type="button" data-object-camera="out" aria-label="Allontana la camera">−</button><button type="button" data-object-camera="reset" aria-label="Ripristina la vista">↺</button></div>
    <p class="object-status" role="status"></p>
    <div class="object-essential"><p>${t.essential}</p></div>
    <div class="galaxy-map-caption"><span>TRASCINA PER RUOTARE · ROTELLA O + − PER LO ZOOM</span><span>${t.caption}</span></div></div>
    ${controls(o)}</div>
    <aside id="object-detail" class="destination-detail object-detail" aria-labelledby="object-name"><p class="destination-signal"><span></span> ${t.signal}</p><p class="destination-sector">${o.kind}</p><h2 id="object-name">${o.name}</h2><p class="stellar-abstract">${t.abstract}</p>${facts(o)}${t.figure || ''}<p class="instrument-note">${t.note}</p></aside></div>
   <section class="astro-learning object-learning" aria-labelledby="object-learning-title"><div><p class="eyebrow">${t.learningEyebrow}</p><h2 id="object-learning-title">${t.learningTitle}</h2>${t.learningIntro}</div><div class="astro-equations">${t.equations}</div>${t.sections}<details class="astro-method"><summary>Come è costruita la scena</summary>${t.method}</details>${t.course}<div class="object-sources"><h3>Fonti</h3><ul>${t.sources.map(s => html`<li><a href="${s.href}" target="_blank" rel="noopener noreferrer">${s.label}</a></li>`)}</ul></div></section>
   <p class="model-note">${t.modelNote}</p></section>`;
    mountScene(main, o);
  }
  function mountScene(main, o) {
    const chart = main.querySelector('.object-chart'),
      status = main.querySelector('.object-status'),
      mine = ++token;
    const ui = {
      chart,
      status: text => {
        if (status.isConnected) status.textContent = text;
      },
      figure: data => C().updateFigure?.(main, o, data),
    };
    chart.dataset.renderer = 'loading';
    scenes()
      .then(() => {
        if (mine !== token || !chart.isConnected) return;
        const S = root.GeoObjectScenes[o.id];
        engine = root.GeoObjectEngine.create(chart, {
          ...S.camera,
          exposure: S.exposure ?? 1,
          bloom: S.bloom ?? 0.06,
          base,
          onLost: () => (scene = null),
        });
        scene = S.create(engine, ui);
        engine.setScene(scene);
        chart.dataset.renderer = 'webgl2';
        chart.dataset.tier = engine.tier;
        chart.classList.add('scene-ready');
        for (const b of main.querySelectorAll('[data-option]')) {
          b.setAttribute('aria-pressed', String(Boolean(scene.options[b.dataset.option])));
          b.addEventListener('click', () => {
            const on = b.getAttribute('aria-pressed') !== 'true';
            b.setAttribute('aria-pressed', String(on));
            scene.setOption(b.dataset.option, on);
          });
        }
        for (const b of main.querySelectorAll('[data-view]'))
          b.addEventListener('click', () => {
            for (const x of main.querySelectorAll('[data-view]')) x.setAttribute('aria-pressed', String(x === b));
            scene.view?.(b.dataset.view);
          });
      })
      .catch(err => {
        if (mine !== token) return;
        root.console?.warn('GeoStat: scena non disponibile.', err);
        cleanup();
        chart.dataset.renderer = 'essential';
        ui.status('');
      });
  }
  root.GeoObjectPages = Object.freeze({
    render,
    cleanup,
    base: () => base,
    debug: () => (engine ? engine.debug() : null),
    // Live scene and engine, for the browser checks.
    inspect: () => ({ engine, scene }),
  });
})(globalThis);
