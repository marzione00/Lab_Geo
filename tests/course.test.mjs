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
  assert.equal(cat.length, 28);
  assert.equal(
    cat.reduce((n, m) => n + m.pages, 0),
    861,
  );
  assert.deepEqual(
    cat.map(m => m.id),
    [
      'T00',
      ...Array.from({ length: 16 }, (_, i) => 'M' + String(i + 1).padStart(2, '0')),
      ...Array.from({ length: 11 }, (_, i) => 'P' + String(i + 1).padStart(2, '0')),
    ],
  );
  for (const m of cat) {
    const d = read('moduli/' + m.id + '/modulo.json'),
      source = read('materiali/sorgenti/contenuti/' + m.id + '.json');
    assert.equal(d.slides.length, m.pages);
    d.slides.forEach((s, i) => {
      assert.equal(s.page, i + 1);
      if (i >= 2) {
        assert.equal(s.title, source.pagine[i - 2].titolo);
        assert.equal(s.body, source.pagine[i - 2].testo);
        assert.equal(s.formula, source.pagine[i - 2].formula);
      }
    });
  }
});
test('Materiali R6 conservati byte per byte', () => {
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
  assert.deepEqual(C.parseRoute('#modulo-M05/slide/105', cat), { type: 'slide', id: 'M05', page: 105 });
  assert.equal(C.parseRoute('#modulo-P11/codici', cat).type, 'code');
  for (const h of [
    '#modulo-M99',
    '#modulo-M05/slide/106',
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
test('Progresso locale robusto a dati corrotti e storage indisponibile', () => {
  assert.deepEqual(C.loadProgress({ getItem: () => '{bad' }), { done: [], last: null });
  assert.deepEqual(C.loadProgress(null), { done: [], last: null });
  const p = C.loadProgress({
    getItem: () => JSON.stringify({ done: ['M05:3', 'M05:3', 'bad'], last: '#modulo-M05/slide/3' }),
  });
  assert.deepEqual(p.done, ['M05:3']);
  assert.equal(
    C.saveProgress(
      {
        setItem: () => {
          throw Error();
        },
      },
      p,
    ),
    false,
  );
});
