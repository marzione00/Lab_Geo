/* Validation at the boundaries: URLs, imported JSON, R results and downloads. */
(function (root) {
  'use strict';
  const limits = Object.freeze({
    config: 2000000,
    query: 16000,
    code: 100000,
    notes: 20000,
    result: 16000000,
    figure: 5000000,
    figures: 6,
    rows: 100000,
    cells: 80,
    metrics: 80,
  });
  const forbidden = new Set(['__proto__', 'prototype', 'constructor']);
  const record = v => v !== null && typeof v === 'object' && !Array.isArray(v);
  function inspect(value, depth = 0) {
    if (depth > 12) throw Error('Struttura JSON troppo profonda.');
    if (value && typeof value === 'object')
      for (const key of Object.keys(value)) {
        if (forbidden.has(key)) throw Error('Chiave JSON non ammessa.');
        inspect(value[key], depth + 1);
      }
  }
  function parseJSON(text, max = limits.config) {
    if (typeof text !== 'string' || text.length > max) throw Error('Il documento supera la dimensione consentita.');
    const value = JSON.parse(text);
    inspect(value);
    return value;
  }
  function parameters(activity, input = {}) {
    if (!record(input)) throw Error('I parametri devono essere un oggetto JSON.');
    const allowed = new Set(activity.controls.map(c => c.key));
    for (const key of Object.keys(input))
      if (!allowed.has(key) || forbidden.has(key)) throw Error('Parametro non ammesso: ' + key);
    const result = {};
    for (const c of activity.controls) {
      if (!/^[a-z][a-z0-9_]*$/i.test(c.key) || forbidden.has(c.key))
        throw Error('Identificativo del parametro non valido.');
      const value = Object.hasOwn(input, c.key) ? input[c.key] : c.value;
      if (c.type === 'select') {
        if (typeof value !== 'string' || !c.options.some(o => o.value === value))
          throw Error('Opzione non valida: ' + c.label);
      } else if (
        typeof value !== 'number' ||
        !Number.isFinite(value) ||
        value < c.min ||
        value > c.max ||
        Math.abs((value - c.min) / c.step - Math.round((value - c.min) / c.step)) > 1e-6
      ) {
        throw Error('Valore fuori dominio: ' + c.label);
      }
      result[c.key] = value;
    }
    return result;
  }
  function code(value) {
    if (typeof value !== 'string' || value.length > limits.code || value.includes('\0'))
      throw Error('Codice R non valido o superiore a 100.000 caratteri.');
    return value;
  }
  function configuration(activity, text) {
    const v = parseJSON(text);
    if (!record(v) || v.application !== 'GeoStatLab' || v.version !== 1 || v.activity !== activity.id)
      throw Error('La configurazione appartiene a un altro esperimento o formato.');
    const allowed = new Set([
      'application',
      'version',
      'activity',
      'parameters',
      'code',
      'notes',
      'engine',
      'metrics',
      'data',
      'rows',
    ]);
    if (Object.keys(v).some(k => !allowed.has(k))) throw Error('Campo della configurazione non riconosciuto.');
    if (v.notes !== undefined && (typeof v.notes !== 'string' || v.notes.length > limits.notes))
      throw Error('Appunti non validi o troppo lunghi.');
    return {
      parameters: parameters(activity, v.parameters),
      code: code(v.code ?? activity.code),
      notes: v.notes ?? '',
    };
  }
  const boundedArray = (x, max) => Array.isArray(x) && x.length <= max;
  function resultShape(v, allowEmptyFigures) {
    return (
      record(v) &&
      Number.isSafeInteger(v.rows) &&
      v.rows >= 0 &&
      v.rows <= limits.rows &&
      boundedArray(v.data, 80) &&
      boundedArray(v.metrics, limits.metrics) &&
      boundedArray(v.figures, limits.figures) &&
      (allowEmptyFigures || v.figures.length > 0)
    );
  }
  const scalar = x =>
    x === null ||
    (typeof x === 'string' && x.length <= 20000) ||
    (typeof x === 'number' && Number.isFinite(x)) ||
    typeof x === 'boolean';
  const tableRow = row => record(row) && Object.keys(row).length <= limits.cells && Object.values(row).every(scalar);
  const shortText = (x, max) => typeof x === 'string' && x.length <= max;
  function result(v, { allowEmptyFigures = false } = {}) {
    inspect(v);
    if (!resultShape(v, allowEmptyFigures))
      throw Error('Il risultato R ha un formato o una dimensione non consentiti.');
    if (![...v.data, ...v.metrics].every(tableRow)) throw Error('La tabella R contiene valori non supportati.');
    if (!v.figures.every(f => shortText(f, limits.figure))) throw Error('La figura supera la dimensione consentita.');
    if (!['R', 'ggplot2', 'svglite'].every(k => shortText(v[k], 200))) throw Error('Metadati R non validi.');
    if (!shortText(v.csv, limits.result)) throw Error('Esportazione CSV non valida.');
    return v;
  }
  // SVG is rendered as an image, never inserted into the page as active markup.
  // Restrict downloaded SVG too, because it may later be opened as a document.
  function svg(text) {
    if (typeof text !== 'string' || text.length > limits.figure || /<!DOCTYPE|<!ENTITY/i.test(text))
      throw Error('SVG non consentito.');
    const doc = new root.DOMParser().parseFromString(text, 'image/svg+xml');
    if (doc.querySelector('parsererror') || doc.documentElement.localName !== 'svg') throw Error('SVG non valido.');
    const allowed = new Set(
      'svg g defs style rect circle ellipse line path polyline polygon text tspan title desc clipPath linearGradient radialGradient stop pattern use image mask filter feColorMatrix feComposite feImage'.split(
        ' ',
      ),
    );
    const safeCSS = s =>
      !/@import|@font-face|expression\s*\(|javascript\s*:|\\/i.test(s) &&
      [...s.matchAll(/url\s*\(([^)]*)\)/gi)].every(m => /^\s*['"]?#[\w:.=+-]+['"]?\s*$/.test(m[1]));
    for (const el of doc.querySelectorAll('*')) {
      if (!allowed.has(el.localName) || el.namespaceURI !== 'http://www.w3.org/2000/svg')
        throw Error('Elemento SVG non consentito.');
      if (el.localName === 'style' && !safeCSS(el.textContent)) throw Error('Stile SVG non consentito.');
      for (const attr of el.attributes) {
        const localReference = /^#[\w:.=+-]+$/.test(attr.value);
        const rasterReference =
          ['image', 'feImage'].includes(el.localName) &&
          /^data:image\/(?:png|jpeg|webp);base64,[A-Za-z0-9+/=\s]+$/.test(attr.value);
        if (
          /^on/i.test(attr.localName) ||
          attr.name === 'xml:base' ||
          (/^(href|src)$/i.test(attr.localName) && !(localReference || rasterReference)) ||
          !safeCSS(attr.value)
        )
          throw Error('Attributo SVG non consentito.');
      }
    }
    for (const node of doc.childNodes) if (node.nodeType === 7) throw Error('Istruzione XML non consentita.');
    return new root.XMLSerializer().serializeToString(doc.documentElement);
  }
  // Parse quoted CSV, including embedded newlines, then neutralise formula cells.
  function csv(text) {
    if (typeof text !== 'string' || text.length > limits.result) throw Error('CSV troppo grande.');
    const rows = [];
    let row = [],
      cell = '',
      quoted = false,
      afterQuote = false;
    const pushCell = () => {
      const numeric = /^-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(cell);
      // eslint-disable-next-line no-control-regex -- control characters are exactly what this check rejects
      if (!numeric && /^[\s\u0000-\u001f\u007f]*[=+@\-\t\r\n＝＋－＠]/u.test(cell)) cell = "'" + cell;
      row.push('"' + cell.replace(/"/g, '""') + '"');
      cell = '';
      afterQuote = false;
    };
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (quoted) {
        if (c === '"') {
          if (text[i + 1] === '"') {
            cell += '"';
            i++;
          } else {
            quoted = false;
            afterQuote = true;
          }
        } else cell += c;
      } else if (c === '"' && !cell && !afterQuote) quoted = true;
      else if (c === ',') pushCell();
      else if (c === '\n' || c === '\r') {
        if (c === '\r' && text[i + 1] === '\n') i++;
        pushCell();
        rows.push(row.join(','));
        row = [];
      } else {
        if (afterQuote || c === '"') throw Error('CSV non valido.');
        cell += c;
      }
    }
    if (quoted) throw Error('CSV non valido.');
    if (cell || row.length || afterQuote) {
      pushCell();
      rows.push(row.join(','));
    }
    return rows.join('\r\n') + '\r\n';
  }
  root.GeoSecurity = Object.freeze({ limits, parseJSON, parameters, configuration, result, code, svg, csv });
})(globalThis);
