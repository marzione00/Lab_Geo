/* Funzioni condivise dalla navigazione e dai controlli automatici. */
(function (root) {
  'use strict';
  const clean = s =>
    String(s ?? '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
  function parseRoute(hash, modules) {
    const key = String(hash || '#indice').replace(/^#/, '');
    if (
      [
        'indice',
        'mappa',
        'catalogo',
        'esperimenti',
        'progetti',
        'materiali',
        'taccuino',
        'taccuino-esplorazioni',
        '',
      ].includes(key)
    )
      return { type: key || 'indice' };
    const exploration = /^esplorazione\/(T00|M(?:0[1-9]|1[0-6]))-([b-f])(?:\?v=(0|[1-9]\d{0,3}))?$/.exec(key);
    if (exploration)
      return modules.some(m => m.id === exploration[1])
        ? {
            type: 'exploration',
            id: exploration[1],
            world: exploration[1] + '-' + exploration[2],
            variant: Number(exploration[3] || 0),
          }
        : { type: 'notfound' };
    const system = /^sistema-(T00|M\d{2})(?:\?v=(0|[1-9]\d{0,3}))?$/.exec(key);
    if (system)
      return modules.some(m => m.id === system[1])
        ? { type: 'system', id: system[1], ...(system[2] === undefined ? {} : { variant: Number(system[2]) }) }
        : { type: 'notfound' };
    const match = /^modulo-(T00|M\d{2}|P\d{2})(?:\/(slide|codici)(?:\/(\d+))?)?$/.exec(key);
    if (!match) return { type: 'notfound' };
    const mod = modules.find(m => m.id === match[1]);
    if (!mod) return { type: 'notfound' };
    if (!match[2]) return { type: 'module', id: mod.id };
    if (match[2] === 'codici') return match[3] ? { type: 'notfound' } : { type: 'code', id: mod.id };
    const page = Number(match[3] || 3);
    return Number.isInteger(page) && page >= 1 && page <= mod.pages
      ? { type: 'slide', id: mod.id, page }
      : { type: 'notfound' };
  }
  function filterModules(modules, query = '', category = 'tutti') {
    const terms = clean(query).split(/\s+/).filter(Boolean);
    return modules.filter(
      m =>
        (category === 'tutti' || m.category === category) &&
        terms.every(t =>
          clean([m.id, m.title, m.subtitle, ...m.sections.map(s => s.title), ...(m.keywords || [])].join(' ')).includes(
            t,
          ),
        ),
    );
  }
  function loadProgress(storage) {
    try {
      const raw = storage.getItem('geostat-r6-progress') || '{}';
      if (raw.length > 200000) return { done: [], last: null };
      const p = JSON.parse(raw);
      if (!p || typeof p !== 'object' || Array.isArray(p)) return { done: [], last: null };
      return {
        done: Array.isArray(p.done)
          ? [...new Set(p.done.slice(0, 2000).filter(x => /^(T00|M\d{2}|P\d{2}):\d+$/.test(x)))]
          : [],
        last: typeof p.last === 'string' && p.last.length < 200 ? p.last : null,
      };
    } catch {
      return { done: [], last: null };
    }
  }
  function saveProgress(storage, p) {
    try {
      storage.setItem('geostat-r6-progress', JSON.stringify(p));
      return true;
    } catch {
      return false;
    }
  }
  // Software rasterisers (SwiftShader, llvmpipe) expose WebGL but draw on the CPU; the canvas renderers are lighter there.
  let softwareGL;
  function softwareRendering() {
    if (softwareGL !== undefined) return softwareGL;
    softwareGL = false;
    try {
      if (root.localStorage?.getItem('geostat:force-webgl') === '1') return softwareGL;
    } catch {
      /* storage unavailable: detect normally */
    }
    try {
      const gl = root.document?.createElement('canvas').getContext('webgl');
      if (gl) {
        const info = gl.getExtension('WEBGL_debug_renderer_info');
        softwareGL = /swiftshader|llvmpipe|softpipe|software rasterizer|basic render driver/i.test(
          String(gl.getParameter(info ? info.UNMASKED_RENDERER_WEBGL : gl.RENDERER) || ''),
        );
        gl.getExtension('WEBGL_lose_context')?.loseContext?.();
      }
    } catch {
      softwareGL = false;
    }
    return softwareGL;
  }
  // True after `count` consecutive frame intervals longer than `limit` ms.
  // Median of the last `count` frame intervals. Intervals are quantised to the display refresh, so a renderer
  // at about 8 fps alternates 117 and 133 ms; a consecutive-frame counter is reset by the shorter interval,
  // while the median is not. A single long frame (shader compilation, texture upload) does not move it.
  function frameWatch(limit = 100, count = 8) {
    const recent = [];
    return interval => {
      recent.push(interval);
      if (recent.length > count) recent.shift();
      if (recent.length < count) return false;
      const sorted = recent.slice().sort((a, b) => a - b);
      return sorted[count >> 1] > limit;
    };
  }
  root.GeoCore = Object.freeze({
    clean,
    parseRoute,
    filterModules,
    loadProgress,
    saveProgress,
    softwareRendering,
    frameWatch,
  });
})(globalThis);
