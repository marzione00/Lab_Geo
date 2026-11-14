import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import { JSDOM } from 'jsdom';
import { load } from './source.mjs';
const projects = fs
  .readdirSync('content')
  .filter(f => /^research-.*\.json$/.test(f))
  .map(f => JSON.parse(fs.readFileSync('content/' + f)));
const scope = { GEO_RESEARCH: projects };
load(scope, 'html', 'planets', 'planet-families', 'research-projects', 'astro-model');
test('Every optional world has a reproducible family and a real-data mission of the matching level', () => {
  const families = new Set(),
    levels = new Set();
  let course = 0,
    optional = 0;
  for (const s of scope.GeoAstro.systems)
    for (const p of s.planets) {
      if (p.isTarget) {
        course++;
        assert.equal(p.familyId, null);
        assert.equal(p.name, scope.GeoPlanets.byId[s.id].name);
        continue;
      }
      optional++;
      families.add(p.familyId);
      levels.add(p.difficulty);
      const a = scope.GeoResearch.forWorld(p.id);
      assert(a);
      assert.equal(a.level, p.difficulty);
      assert.equal(scope.GeoAstro.generate(s.id, 9999).planets.find(q => q.id === p.id).familyId, p.familyId);
      for (const detail of [false, true]) assert(fs.existsSync(scope.GeoFamilies.texture(p, detail)));
    }
  assert.equal(course, 17);
  assert.equal(optional, 68);
  assert.equal(families.size, 13);
  assert.equal(levels.size, 5);
  assert.equal(new Set(projects.map(p => p.level)).size, 5);
  assert.equal(projects.length, 5);
});
test('Observed-data manifests, R sources and generated bundles agree', () => {
  const report = JSON.parse(fs.readFileSync('qa/research-r.json'));
  assert.equal(report.status, 'passed');
  assert(report.checks.length >= 140);
  for (const p of projects) {
    const path = 'assets/research/' + p.id + '/';
    const provenance = JSON.parse(fs.readFileSync(path + 'provenance.json'));
    assert(provenance.rows > 20);
    assert(p.sources.every(s => new URL(s.url).protocol === 'https:'));
    assert(p.formula && p.formulaExplanation);
    assert.equal(p.code.trimEnd(), fs.readFileSync(path + 'source.R', 'utf8').trimEnd());
    const script = fs.readFileSync(path + p.id + '.R', 'utf8');
    assert(script.includes(p.code));
    assert(script.includes('read.csv("data.csv"'));
    assert(fs.statSync(path + 'project.zip').size > 1000);
    const cases = report.checks.filter(c => c.project === p.id);
    assert(cases.length >= 10);
    assert(cases.every(c => c.status === 'passed' && c.rows > 0));
    const preview = JSON.parse(fs.readFileSync(path + 'preview.json'));
    for (const c of p.controls) assert.equal(preview.parameters[c.key], c.value);
  }
});
function setup() {
  const dom = new JSDOM('<main></main>', { url: 'https://geostat.test/', runScripts: 'outside-only' }),
    w = dom.window;
  w.GEO_SOLUTIONS = { research: JSON.parse(fs.readFileSync('content/solution-guides-research.json')) };
  w.GEO_RESEARCH = projects.map(p => ({
    ...p,
    rows: JSON.parse(fs.readFileSync('assets/research/' + p.id + '/provenance.json')).rows,
    retrievedAt: '2026-11-13',
  }));
  w.GEO_LABS = { common: fs.readFileSync('R/lab-common.R', 'utf8') };
  w.GEO_CATALOG = JSON.parse(fs.readFileSync('content/catalogue.json'));
  w.URL.createObjectURL = () => 'blob:https://geostat.test/test';
  w.URL.revokeObjectURL = () => {};
  load(
    w,
    'html',
    'planets',
    'planet-families',
    'security',
    'code-terminal',
    'solution-terminal',
    'research-projects',
    'astro-model',
    'learning-paths',
    'explorations',
  );
  w.GeoREngine = {
    subscribe: () => () => {},
    reset: () => {},
    run: () => {
      throw Error('Unexpected execution');
    },
  };
  return { dom, w, main: w.document.querySelector('main') };
}
test('Five missions show R, real-data provenance and formulas; parameter edits keep results explicitly stale', () => {
  const { w, main } = setup();
  for (const p of projects) {
    w.GeoResearch.cleanup();
    w.GeoExplorations.render(main, p.worldId);
    assert(main.querySelector('[data-research="' + p.id + '"]'));
    assert(main.querySelector('.research-formalism .math').textContent.includes(p.formula));
    assert.equal(main.querySelectorAll('.r-code-block').length, w.GeoCodeGuide.blocks(p.code).length);
    assert(main.querySelector('a[href="assets/research/' + p.id + '/project.zip"]'));
    assert(main.querySelector('.research-model-context'));
    assert(main.querySelector('#research-stop').hidden);
    assert(!/undefined/.test(main.textContent));
    assert(!/NaN/.test(main.querySelector('.research-provenance').textContent));
    const c = p.controls.find(c => c.key !== 'seed'),
      input = main.querySelector('#research-' + c.key);
    input.value = c.type === 'select' ? c.options.at(-1).value : c.max;
    input.dispatchEvent(new w.Event('input', { bubbles: true }));
    assert(main.querySelector('.research-result-state').textContent.includes('Parametri modificati'));
    assert.equal(w.GeoExplorations.records().length, 0);
  }
  w.GeoResearch.cleanup();
  w.close();
});
test('Frozen dataset loading rejects a changed snapshot before R execution', async () => {
  const p = projects[0],
    bytes = fs.readFileSync('assets/research/' + p.id + '/data.csv');
  const context = {
    GEO_RESEARCH: projects,
    TextDecoder,
    crypto: crypto.webcrypto,
    fetch: async () => ({
      ok: true,
      arrayBuffer: async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
    }),
  };
  load(context, 'html', 'research-projects');
  const meta = { ...p, dataSHA256: crypto.createHash('sha256').update(bytes).digest('hex') };
  assert.equal(await context.GeoResearch.readDataset(meta), bytes.toString());
  await assert.rejects(context.GeoResearch.readDataset({ ...meta, dataSHA256: '0'.repeat(64) }), /non corrisponde/);
});

test('All 68 complementary destinations render a complete mission without missing disciplines or readings', () => {
  const { w, main } = setup();
  for (const s of w.GeoAstro.systems)
    for (const p of s.planets.filter(p => !p.isTarget)) {
      w.GeoResearch.cleanup();
      const meta = w.GeoPaths.forPlanet(s, p);
      assert(meta.symbol && meta.discipline && meta.paragraphs.length);
      assert(meta.sources.every(k => w.GeoPaths.links[k]));
      w.GeoExplorations.render(main, p.id, 9999);
      assert(main.querySelector('.research-mission'));
      assert(!main.textContent.includes('undefined'));
      assert.equal(main.querySelectorAll('.exploration-table tbody tr').length, 5);
    }
  w.GeoResearch.cleanup();
  w.close();
});
test('Stopping while the dataset loads prevents R execution and permits a fresh attempt', async () => {
  const { w, main } = setup();
  w.AbortController = AbortController;
  w.TextDecoder = TextDecoder;
  Object.defineProperty(w.crypto, 'subtle', { value: crypto.webcrypto.subtle });
  const p = projects[0],
    bytes = fs.readFileSync('assets/research/' + p.id + '/data.csv');
  let requests = [],
    runs = 0;
  w.fetch = (_, options) => new Promise(resolve => requests.push({ resolve, signal: options.signal }));
  w.GeoREngine.run = async () => {
    runs++;
    return { figures: [], metrics: [], data: [], rows: 0, R: 'test', ggplot2: 'test', csv: '' };
  };
  w.GeoResearch.mount(main, { ...p, dataSHA256: crypto.createHash('sha256').update(bytes).digest('hex') });
  const submit = () => main.querySelector('#research-form').dispatchEvent(new w.Event('submit', { cancelable: true }));
  const response = () => ({
    ok: true,
    arrayBuffer: async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
  });
  const until = async predicate => {
    for (let i = 0; i < 100 && !predicate(); i++) await new Promise(r => setTimeout(r, 5));
    assert(predicate());
  };
  submit();
  assert.equal(requests.length, 1);
  main.querySelector('#research-stop').click();
  assert(requests[0].signal.aborted);
  requests[0].resolve(response());
  await until(() => main.querySelector('#research-stop').hidden);
  assert.equal(runs, 0);
  assert.match(main.querySelector('#research-engine').textContent, /interrotto/);
  submit();
  assert.equal(requests.length, 2);
  assert(!requests[1].signal.aborted);
  requests[1].resolve(response());
  await until(() => main.querySelector('#research-stop').hidden);
  assert.equal(runs, 1);
  w.GeoResearch.cleanup();
  w.close();
});
test('Exploration return links retain the exact stellar configuration', () => {
  const { w, main } = setup();
  load(w, 'core');
  const p = projects[0];
  w.GeoExplorations.render(main, p.worldId, 18);
  const href = main.querySelector('.exploration-breadcrumb a').getAttribute('href');
  const route = w.GeoCore.parseRoute(href, w.GEO_CATALOG.modules);
  assert.equal(route.variant, 18);
  assert.equal(route.type, 'system');
  const s = w.GeoAstro.generate(route.id, route.variant),
    original = w.GeoExplorations.resolve(p.worldId, 18).s;
  assert.equal(s.star.type, original.star.type);
  assert.equal(s.planets[0].axisAU, original.planets[0].axisAU);
  for (const value of ['-1', '10000', '01', 'foo', '0&x=1'])
    assert.equal(w.GeoCore.parseRoute('#sistema-M01?v=' + value, w.GEO_CATALOG.modules).type, 'notfound');
  w.GeoResearch.cleanup();
  w.close();
});
