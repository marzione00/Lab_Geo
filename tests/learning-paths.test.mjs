import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { JSDOM } from 'jsdom';
import { load } from './source.mjs';
const catalogue = JSON.parse(fs.readFileSync('content/catalogue.json', 'utf8'));
function setup() {
  const dom = new JSDOM('<main></main>', { url: 'https://geostat.test/', runScripts: 'outside-only' }),
    w = dom.window;
  w.GEO_CATALOG = catalogue;
  load(w, 'html', 'planets', 'astro-model', 'core', 'learning-paths', 'explorations');
  return { dom, w, main: w.document.querySelector('main') };
}
test('All 85 worlds have an independent path and level; every complementary world opens a scientific reading', () => {
  const { w, main } = setup();
  let courses = 0,
    explorations = 0;
  for (const s of w.GeoAstro.systems)
    for (const p of s.planets) {
      const meta = w.GeoPaths.forPlanet(s, p);
      assert(['Introduttivo', 'Intermedio', 'Avanzato'].includes(meta.level));
      for (const id of meta.prerequisites) assert(catalogue.modules.some(m => m.id === id));
      if (p.isTarget) {
        courses++;
        assert.equal(meta.track, 'course');
        assert.equal(w.GeoExplorations.resolve(p.id), null);
      } else {
        explorations++;
        assert.equal(meta.track, 'exploration');
        w.GeoExplorations.render(main, p.id, 3);
        assert.equal(main.querySelectorAll('tbody tr').length, 5);
        assert(main.querySelector('a[href="#modulo-' + s.id + '"]'));
        assert(main.querySelector('#exploration-save').disabled);
        assert.equal(w.localStorage.length, 0);
        assert(!/undefined|NaN/.test(main.textContent));
        assert(main.querySelector('.path-badge').textContent.includes(meta.symbol));
      }
    }
  assert.equal(courses, 17);
  assert.equal(explorations, 68);
  assert.equal(w.GeoPaths.moduleInfo('M08').level, 'Avanzato');
  assert(
    w.GeoAstro.systems.some(s =>
      s.planets.some(p => !p.isTarget && w.GeoPaths.forPlanet(s, p).level === 'Introduttivo'),
    ),
  );
  w.close();
});
test('Exploration routes reject malformed worlds and variant values', () => {
  const { w } = setup();
  for (const s of w.GeoAstro.systems)
    for (const p of s.planets.filter(p => !p.isTarget)) {
      const route = w.GeoCore.parseRoute('#esplorazione/' + p.id + '?v=9999', catalogue.modules);
      assert.equal(route.type, 'exploration');
      assert.equal(route.world, p.id);
      assert.equal(route.variant, 9999);
    }
  for (const id of [
    'M99-b',
    'M05-z',
    'P01-b',
    '__proto__',
    'M05-e?v=-1',
    'M05-e?v=10000',
    'M05-e?v=01',
    'M05-e?v=<img>',
  ])
    assert.equal(w.GeoCore.parseRoute('#esplorazione/' + id, catalogue.modules).type, 'notfound', id);
  assert.equal(w.GeoExplorations.resolve('M05-e', -1), null);
  assert.equal(w.GeoExplorations.resolve('M05-e', 10000), null);
  w.close();
});
test('Optional annotations require explicit saving, preserve course storage and escape hostile notes', () => {
  const { w, main } = setup(),
    course = '{"version":1,"entries":[]}',
    progress = '{"done":["M05:3"]}';
  w.localStorage.setItem('geostat-fieldbook-v1', course);
  w.localStorage.setItem('geostat-r6-progress', progress);
  const s = w.GeoAstro.generate('M05'),
    p = s.planets.find(p => !p.isTarget);
  w.GeoExplorations.render(main, p.id, 4);
  assert.equal(w.GeoExplorations.records().length, 0);
  const notes = main.querySelector('#exploration-notes');
  notes.value = '<img src=x onerror=alert(1)>';
  notes.dispatchEvent(new w.Event('input'));
  assert.equal(w.GeoExplorations.records().length, 0);
  main.querySelector('#exploration-save').click();
  assert.equal(w.GeoExplorations.records().length, 1);
  assert.equal(w.GeoExplorations.records()[0].completed, false);
  main.querySelector('#exploration-complete').checked = true;
  assert.equal(w.GeoExplorations.records()[0].completed, false);
  main.querySelector('#exploration-save').click();
  assert.equal(w.GeoExplorations.records()[0].completed, true);
  assert.equal(w.localStorage.getItem('geostat-fieldbook-v1'), course);
  assert.equal(w.localStorage.getItem('geostat-r6-progress'), progress);
  w.GeoExplorations.journal(main);
  assert.equal(main.querySelectorAll('.journal-entry').length, 1);
  assert.equal(main.querySelectorAll('[onerror]').length, 0);
  assert(main.textContent.includes('<img src=x onerror=alert(1)>'));
  assert(main.querySelector('a[href="#esplorazione/' + p.id + '?v=4"]'));
  const record = w.GeoExplorations.records()[0];
  for (const invalid of [
    { ...record, notes: ' ' },
    { ...record, notes: 'x'.repeat(6001) },
    { ...record, completed: 'yes' },
    { ...record, date: 'invalid' },
    { ...record, variant: -1 },
    { ...record, id: s.target.id },
  ])
    assert.equal(w.GeoExplorations.save(invalid), false);
  w.localStorage.setItem('geostat-explorations-v1', 'broken');
  assert.equal(w.GeoExplorations.records().length, 0);
  w.close();
});
