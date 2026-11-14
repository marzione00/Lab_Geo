/* Mission briefing shown on the first visit to the home page, and one-line hints on the first visit to a
   system, a module and a laboratory. Loaded on demand by app.js; the texts come from content/briefing.json. */
(function (root) {
  'use strict';
  const D = root.GEO_BRIEFING,
    { html, raw } = root.GeoHTML;
  const KEY = 'geostat:briefing:v' + D.version;
  const reduced = () => root.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const remember = key => {
    try {
      localStorage.setItem(key, 'seen');
    } catch {
      // Without storage the briefing is offered again on the next visit.
    }
  };
  const cue = name => document.dispatchEvent(new CustomEvent('geostat:cue', { detail: { name } }));
  const counts = () => ({
    N_SYSTEMS: root.GeoAstro.systems.length,
    N_MISSIONS: root.GEO_CATALOG.modules.filter(m => m.category === 'progetti').length,
    N_MODULES: root.GEO_CATALOG.modules.length,
    N_EXPERIMENTS: root.GEO_LABS.activities.length,
  });
  const fill = text => text.replace(/\{\{(\w+)\}\}/g, (_, k) => String(counts()[k] ?? ''));

  let dialog = null,
    index = 0,
    target = null,
    opener = null;

  function actions(card, last) {
    if (card.audioChoice)
      return html`<button type="button" class="button briefing-primary" data-audio="on">Avvia con audio</button
        ><button type="button" class="button secondary" data-audio="off">Avvia in silenzio</button>`;
    return html`<button type="button" class="button secondary" data-move="-1">← Indietro</button
      ><button type="button" class="button briefing-primary" data-move="1">
        ${last ? 'Inizia l’esplorazione' : 'Avanti →'}
      </button>`;
  }

  function markup(card) {
    const n = D.cards.length,
      step = String(index + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0');
    return html`<header class="briefing-head">
        <p class="hud-label"><span>${D.title}</span> <span class="briefing-step">${step} · ${card.label}</span></p>
        <button type="button" class="briefing-skip">Salta</button>
      </header>
      <ol class="briefing-progress" aria-hidden="true">
        ${raw(D.cards.map((_, i) => `<li${i <= index ? ' class="done"' : ''}></li>`).join(''))}
      </ol>
      <h2 id="briefing-title">${card.title}</h2>
      <div id="briefing-body" class="briefing-body">
        ${raw(card.lines.map(line => html`<p class="briefing-line">${fill(line)}</p>`).join(''))}
      </div>
      <div class="briefing-actions">${raw(actions(card, index === n - 1))}</div>`;
  }

  // The spotlight is a frame over the highlighted element; its shadow dims the rest of the page.
  function place() {
    const spot = dialog?.querySelector('.briefing-spot');
    if (!spot) return;
    if (!target?.isConnected) {
      spot.hidden = true;
      return;
    }
    const r = target.getBoundingClientRect();
    spot.hidden = false;
    spot.style.left = r.left - 6 + 'px';
    spot.style.top = r.top - 6 + 'px';
    spot.style.width = r.width + 12 + 'px';
    spot.style.height = r.height + 12 + 'px';
    const card = dialog.querySelector('.briefing-card');
    card.dataset.side = r.left + r.width / 2 < root.innerWidth / 2 ? 'right' : 'left';
    // On a phone the card spans the width: it moves to the top when the element sits in the lower half.
    card.dataset.edge = r.top + Math.min(r.height, root.innerHeight) / 2 > root.innerHeight / 2 ? 'top' : 'bottom';
  }

  function aim(card) {
    target = card.target ? document.querySelector(card.target) : null;
    if (card.focus) root.GeoGalaxy?.focus?.(card.focus);
    const narrow = root.matchMedia('(max-width: 600px)').matches;
    target?.scrollIntoView({
      block: narrow ? 'start' : 'center',
      inline: 'nearest',
      behavior: reduced() ? 'instant' : 'smooth',
    });
    dialog.classList.toggle('has-target', Boolean(target));
    place();
  }

  function show(i) {
    index = Math.max(0, Math.min(D.cards.length - 1, i));
    const card = D.cards[index],
      panel = dialog.querySelector('.briefing-card');
    panel.innerHTML = markup(card);
    panel.querySelector('[data-move="-1"]')?.toggleAttribute('disabled', index === 0);
    panel.querySelector('.briefing-primary').focus();
    aim(card);
  }

  function close() {
    if (!dialog) return;
    remember(KEY);
    root.removeEventListener('resize', place);
    root.removeEventListener('scroll', place, true);
    if (dialog.open) dialog.close();
    dialog.remove();
    dialog = null;
    target = null;
    cue('briefing-close');
    (opener?.isConnected ? opener : document.getElementById('contenuto'))?.focus({ preventScroll: true });
    opener = null;
  }

  function onClick(e) {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.classList.contains('briefing-skip')) return close();
    if (b.dataset.audio) {
      document.dispatchEvent(
        new CustomEvent('geostat:audio-choice', { detail: { enabled: b.dataset.audio === 'on' } }),
      );
      return next(1);
    }
    if (b.dataset.move) next(Number(b.dataset.move));
  }

  function next(step) {
    if (index + step >= D.cards.length) return close();
    cue('briefing-next');
    show(index + step);
  }

  function onKey(e) {
    if (e.altKey || e.ctrlKey || e.metaKey || /INPUT|SELECT|TEXTAREA/.test(e.target.tagName)) return;
    if (e.key === 'ArrowRight' && !D.cards[index].audioChoice) next(1);
    else if (e.key === 'ArrowLeft' && index > 0) next(-1);
    else return;
    e.preventDefault();
  }

  function open(options = {}) {
    if (dialog) return;
    opener = options.opener || null;
    dialog = document.createElement('dialog');
    dialog.className = 'briefing';
    dialog.setAttribute('aria-labelledby', 'briefing-title');
    dialog.setAttribute('aria-describedby', 'briefing-body');
    dialog.innerHTML =
      '<div class="briefing-spot" aria-hidden="true" hidden></div><section class="briefing-card hud-panel" data-tone="action"></section>';
    dialog.addEventListener('click', onClick);
    dialog.addEventListener('keydown', onKey);
    dialog.addEventListener('cancel', e => {
      e.preventDefault();
      close();
    });
    document.body.append(dialog);
    dialog.showModal();
    root.addEventListener('resize', place);
    root.addEventListener('scroll', place, true);
    cue('briefing-open');
    show(0);
  }

  // Hints: one per page, each shown once, placed under its anchor without moving the layout.
  let hintBox = null;
  function dropHint() {
    hintBox?.remove();
    hintBox = null;
  }
  function hint(kind) {
    const h = D.hints[kind],
      anchor = h && document.querySelector(h.anchor);
    if (!anchor || dialog) return;
    dropHint();
    remember('geostat:hint:' + kind);
    hintBox = document.createElement('div');
    hintBox.className = 'briefing-hint hud-panel';
    hintBox.setAttribute('role', 'status');
    hintBox.innerHTML = html`<p>${h.text}</p>
      <button type="button" class="briefing-hint-close">Ho capito</button>`;
    hintBox.querySelector('button').addEventListener('click', dropHint);
    document.body.append(hintBox);
    const r = anchor.getBoundingClientRect(),
      width = hintBox.offsetWidth;
    hintBox.style.top = r.bottom + root.scrollY + 10 + 'px';
    hintBox.style.left = Math.max(12, Math.min(r.left + root.scrollX, root.innerWidth - width - 12)) + 'px';
    anchor.classList.add('briefing-anchor');
    setTimeout(() => anchor.classList.remove('briefing-anchor'), 2400);
  }

  function cleanup() {
    close();
    dropHint();
  }

  root.GeoBriefing = Object.freeze({ open, close, hint, cleanup, key: KEY, isOpen: () => Boolean(dialog) });
})(window);
