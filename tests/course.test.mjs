import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const cat = read('content/catalogue.json').modules;
await import('../src/core.js');
const C = globalThis.GeoCore;
test('Copertura integrale del corso e continuità delle pagine', () => {
  assert.equal(cat.length, 29);
  assert.deepEqual(
    cat.map(m => m.id),
    [
      'T00',
      ...Array.from({ length: 17 }, (_, i) => 'M' + String(i + 1).padStart(2, '0')),
      ...Array.from({ length: 11 }, (_, i) => 'P' + String(i + 1).padStart(2, '0')),
    ],
  );
  // Every module and expedition is a lesson a tappe: no slides, figures or sources of an earlier edition.
  const lessons = read('lezioni/lezioni.json');
  for (const m of cat) {
    const d = read('moduli/' + m.id + '/modulo.json'),
      L = read('content/lezioni/' + m.id + '.json');
    assert(!d.slides && !d.figureCode && !m.pages && !m.pdf && !m.script, m.id);
    assert.equal(L.slides.length, L.pages, m.id);
    L.slides.forEach((s, i) => assert.equal(s.page, i + 1, m.id));
    assert(fs.existsSync(path.join(root, lessons[m.id].source, lessons[m.id].tex)), m.id);
  }
  for (const dir of [
    'assets/slides',
    'assets/visuals',
    'materiali/pdf',
    'materiali/sorgenti',
    'materiali/figure',
    'materiali/tikz',
    'materiali/estratti',
  ])
    assert(!fs.existsSync(path.join(root, dir)), dir);
});
test('Materiali conservati byte per byte', () => {
  const lines = fs.readFileSync(path.join(root, 'materiali/MANIFEST_SHA256.txt'), 'utf8').trim().split('\n');
  for (const line of lines) {
    const [sha, p] = line.split('  ');
    const b = fs.readFileSync(path.join(root, 'materiali', p));
    assert.equal(crypto.createHash('sha256').update(b).digest('hex'), sha, p);
  }
});
test('Laboratori collegati alle versioni collaudate', () => {
  let r = 0,
    py = 0;
  for (const m of cat) {
    for (const l of read('moduli/' + m.id + '/modulo.json').laboratories) {
      assert.equal(
        crypto
          .createHash('sha256')
          .update(fs.readFileSync(path.join(root, l.path)))
          .digest('hex'),
        l.sha256,
      );
      assert.equal(l.code, fs.readFileSync(path.join(root, l.path), 'utf8'));
      if (l.language === 'R') r++;
      else py++;
    }
  }
  assert.equal(r, 340);
  assert.equal(py, 20);
});
test('Rotte valide, limiti e input malformati', () => {
  assert.equal(C.parseRoute('#modulo-P11/codici', cat).type, 'code');
  // Modules have no slides: every old slide address opens the tappe of the lesson.
  const lessons = { M05: { pages: 109 }, P01: { pages: 31 } };
  assert.deepEqual(C.parseRoute('#modulo-M05/slide/105', cat, lessons), {
    type: 'lesson',
    id: 'M05',
    page: null,
    legacy: true,
  });
  assert.deepEqual(C.parseRoute('#modulo-M05/slide', cat, lessons).legacy, true);
  assert.equal(C.parseRoute('#modulo-M05/slide/106', cat, lessons).legacy, true);
  assert.deepEqual(C.parseRoute('#modulo-P01/slide/21', cat, lessons).legacy, true);
  assert.deepEqual(C.parseRoute('#lezione-P01/31', cat, lessons), { type: 'lesson', id: 'P01', page: 31 });
  assert.equal(C.parseRoute('#lezione-P01/32', cat, lessons).type, 'notfound');
  assert.equal(C.parseRoute('#esercizi-P01', cat, lessons).type, 'notfound');
  for (const h of [
    '#modulo-M99',
    '#modulo-M05/slide/3',
    '#modulo-P01/slide/22',
    '#modulo-T00/slide/0',
    '#modulo-M05/codici/2',
    '#%bad',
    '#modulo-M05/slide/1.5',
  ])
    assert.equal(C.parseRoute(h, cat).type, 'notfound');
});
test('Controllo dei fotogrammi lenti: mediana su otto intervalli', () => {
  const feed = (watch, xs) => xs.map(watch).at(-1);
  // Software WebGL measured in Chromium: intervals alternate across the 120 ms mark.
  assert.equal(feed(C.frameWatch(), [117, 133, 117, 133, 117, 133, 117, 133]), true);
  assert.equal(feed(C.frameWatch(), [117, 133, 117, 133, 117, 133, 117]), false);
  // A single shader compilation among smooth frames is tolerated.
  assert.equal(feed(C.frameWatch(), [16, 16, 900, 16, 16, 16, 16, 16]), false);
  assert.equal(feed(C.frameWatch(), [33, 33, 50, 33, 33, 33, 50, 33]), false);
});
test('Ricerca accenti, sezioni e combinazione con categoria', () => {
  assert(C.filterModules(cat, 'probabilita').some(m => m.id === 'M04'));
  assert.equal(C.filterModules(cat, 'P11', 'progetti')[0].id, 'P11');
  assert.equal(C.filterModules(cat, 'P11', 'moduli').length, 0);
  assert(C.filterModules(cat, 'bootstrap').length > 1);
});
