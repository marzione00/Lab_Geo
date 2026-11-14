import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { JSDOM } from 'jsdom';
import { load } from './source.mjs';
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const data = { ...read('content/narrative.json'), activities: read('content/narrative-m05.json') };
const labs = read('content/experiments.json'),
  catalogue = read('content/catalogue.json');
const sample = id => read('assets/experiments/' + id + '.json');
const params = a => Object.fromEntries(a.controls.map(c => [c.key, c.value]));
function setup() {
  const storage = new Map();
  const context = vm.createContext({
    GEO_NARRATIVE: data,
    GEO_LABS: labs,
    localStorage: { getItem: k => storage.get(k), setItem: (k, v) => storage.set(k, v) },
  });
  load(context, 'html', 'security', 'narrative');
  return { N: context.GeoNarrative, storage };
}
test('Narrative chapters and Pelago stages preserve the catalogue order and unique ownership', () => {
  assert.deepEqual(
    Object.keys(data.chapters),
    catalogue.modules.filter(m => m.category !== 'progetti').map(m => m.id),
  );
  const ids = labs.activities.filter(a => a.module === 'M05').map(a => a.id);
  assert.deepEqual(Object.keys(data.activities), ids);
  assert.deepEqual(
    data.sampling.stages.flatMap(s => s.ids),
    ids,
  );
  for (const entry of Object.values(data.activities))
    for (const key of ['title', 'scene', 'question', 'prediction', 'bridge']) assert(entry[key]?.trim());
  assert.equal(new Set(Object.values(data.activities).map(a => a.scene)).size, 9);
});
test('Every Pelago commentary reads the real R fixture; invalid and custom results cannot claim a model conclusion', () => {
  const { N } = setup();
  for (const a of labs.activities.filter(a => a.module === 'M05')) {
    const r = sample(a.id),
      text = N.reading(a.id, params(a), r);
    assert(text?.length > 150);
    assert(!/NaN|undefined|non è disponibile|non consentono/.test(text), a.id);
    assert(N.reading(a.id, params(a), r, false).includes('sospeso'));
    const bad = structuredClone(r);
    bad.metrics[0].valore = 'NaN';
    assert(N.reading(a.id, params(a), bad).includes('non consentono'));
    assert(!/NaN|undefined/.test(N.reading(a.id, params(a), { metrics: [] })), a.id);
  }
  const a = labs.activities.find(a => a.id === 'm05-selezione'),
    r = sample(a.id);
  assert(N.reading(a.id, { ...params(a), bias: 0 }, r).includes('sistematico è nullo'));
  assert(N.reading(a.id, params(a), r).includes('osservato'));
});
test('Narrative comparisons isolate one changed condition and never infer improvement from multiple changes', () => {
  const { N } = setup(),
    a = labs.activities.find(a => a.id === 'm05-distribuzioni'),
    p = params(a);
  const make = q => ({ params: q, standard: true, result: sample(a.id) });
  assert(N.comparison(a, [make(p), make({ ...p, n: 240 })]).includes('0,5'));
  assert(N.comparison(a, [make(p), make({ ...p, n: 240, seed: 18 })]).includes('non isola'));
  assert(N.comparison(a, [make(p), make(p)]).includes('stessi parametri'));
  assert(N.comparison(a, [make(p), { ...make(p), standard: false }]).includes('personalizzato'));
});
test('Fieldbook rejects malformed storage and preserves one explicit record per activity with validated parameters', () => {
  const { N, storage } = setup(),
    a = labs.activities.find(a => a.id === 'm05-distribuzioni'),
    p = params(a),
    r = sample(a.id);
  assert.equal(N.records().length, 0);
  assert(N.save(a, p, r, 'Osservazione', []));
  assert.equal(N.records().length, 1);
  assert(N.save(a, { ...p, n: 120 }, r, 'Seconda osservazione', []));
  assert.equal(N.records().length, 1);
  assert.equal(N.records()[0].params.n, 120);
  assert(!N.save(a, { ...p, n: -100 }, r, '', []));
  const valid = N.records()[0];
  storage.set(
    'geostat-fieldbook-v1',
    JSON.stringify({ version: 1, entries: [valid, { ...valid, id: '__proto__' }, { ...valid, params: { n: -1 } }] }),
  );
  assert.equal(N.records().length, 1);
  storage.set('geostat-fieldbook-v1', 'invalid');
  assert.equal(N.records().length, 0);
  storage.set('geostat-fieldbook-v1', 'x'.repeat(600001));
  assert.equal(N.records().length, 0);
});
test('Guided lesson waits for execution, invalidates stale narrative and protects stored notes from HTML injection', async () => {
  const dom = new JSDOM('<main></main>', { url: 'https://geostat.test/', runScripts: 'outside-only' }),
    w = dom.window,
    d = w.document;
  let runs = 0;
  w.GEO_NARRATIVE = data;
  w.GEO_LABS = labs;
  w.GEO_CATALOG = catalogue;
  w.GeoPlanets = { byId: Object.fromEntries(catalogue.modules.map(m => [m.id, { name: m.id }])) };
  load(w, 'html', 'security', 'narrative');
  w.URL.createObjectURL = () => '/test-figure.svg';
  w.URL.revokeObjectURL = () => {};
  w.GeoREngine = {
    subscribe: () => () => {},
    paramsCode: () => '',
    reset: () => {},
    init: async () => {},
    run: async () => {
      runs++;
      return {
        ...sample('m05-distribuzioni'),
        csv: 'media\n1',
        svglite: 'test',
        figures: ['<svg xmlns="http://www.w3.org/2000/svg"/>'],
      };
    },
  };
  w.fetch = async () => {
    throw Error('A guided lesson must not fetch its answer before execution');
  };
  w.setTimeout = () => 1;
  w.clearTimeout = () => {};
  load(w, 'experiments');
  const a = labs.activities.find(a => a.id === 'm05-distribuzioni'),
    main = d.querySelector('main');
  w.GeoLabs.experiment(main, a);
  const tick = () => new Promise(r => setTimeout(r, 0));
  assert.equal(runs, 0);
  assert(d.querySelector('#save-fieldbook').disabled);
  assert(d.querySelector('#narrative-result').hidden);
  assert(
    d.querySelector('#lab-guided').compareDocumentPosition(d.querySelector('.lab-layout')) &
      w.Node.DOCUMENT_POSITION_FOLLOWING,
  );
  d.querySelector('#lab-run').click();
  await tick();
  assert.equal(runs, 1);
  assert(!d.querySelector('#save-fieldbook').disabled, d.querySelector('#lab-error').textContent);
  assert(!d.querySelector('#narrative-result').hidden);
  d.querySelector('#lab-notes').value = '<img src=x onerror=alert(1)>';
  d.querySelector('#lab-compare').click();
  d.querySelector('#save-fieldbook').click();
  assert.equal(w.GeoNarrative.records().length, 1);
  d.querySelector('#lab-auto').checked = false;
  d.querySelector('#param-n').value = '120';
  d.querySelector('#param-n').dispatchEvent(new w.Event('input'));
  assert(d.querySelector('#save-fieldbook').disabled);
  assert(d.querySelector('#narrative-result').hidden);
  d.querySelector('#lab-run').click();
  await tick();
  d.querySelector('#lab-compare').click();
  assert(!d.querySelector('#narrative-comparison').hidden);
  d.querySelector('#lab-code-editor').value = 'stop("modified")';
  d.querySelector('#lab-code-editor').dispatchEvent(new w.Event('input'));
  d.querySelector('#lab-run-code').click();
  await tick();
  assert(d.querySelector('#narrative-result-text').textContent.includes('sospeso'));
  assert(d.querySelector('#save-fieldbook').disabled);
  w.GeoLabs.cleanup();
  w.GeoNarrative.journal(main);
  assert.equal(main.querySelectorAll('[onerror]').length, 0);
  assert(main.textContent.includes('<img src=x onerror=alert(1)>'));
  assert.equal(main.querySelectorAll('.journal-entry').length, 1);
  assert(main.querySelector('a[href^="#laboratorio/"]').href.includes('n%22%3A60'));
  w.close();
});
