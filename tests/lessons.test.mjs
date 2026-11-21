import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { explanations, inline } from '../scripts/lessons/build-lessons.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const config = JSON.parse(read('lezioni/lezioni.json'));
const cat = JSON.parse(read('content/catalogue.json')).modules;
await import('../src/core.js');
const C = globalThis.GeoCore;

for (const [id, cfg] of Object.entries(config)) {
  const L = JSON.parse(read('content/lezioni/' + id + '.json')),
    E = cfg.workbook ? JSON.parse(read('content/esercizi/' + id + '.json')) : null,
    md = fs.existsSync(path.join(root, 'content/lezioni/' + id + '.md')),
    labs = new Map(JSON.parse(read('content/experiments.json')).activities.map(a => [a.id, a]));

  test(id + ': una tappa per pagina, con titolo, sezione, copertina e PDF timbrato', () => {
    assert.equal(L.slides.length, L.pages);
    L.slides.forEach((s, i) => {
      assert.equal(s.page, i + 1);
      assert.ok(s.title && s.section);
      assert.equal(Boolean(s.image), s.page === 1, 'immagine soltanto in copertina');
    });
    assert.ok(fs.existsSync(path.join(root, L.slides[0].image)), L.slides[0].image);
    assert.ok(fs.existsSync(path.join(root, L.pdf)), L.pdf);
    assert.equal(L.sections.at(-1).last, L.pages);
    L.sections.forEach((sec, i) => i && assert.equal(sec.first, L.sections[i - 1].last + 1));
  });

  test(id + ': riquadri in colonna e figure ricavate dal sorgente TikZ', () => {
    for (const s of L.slides.slice(2)) {
      assert.ok(s.items.length > 0, 'slide ' + s.page);
      const cols = [...new Set(s.items.map(it => it.col))].sort().join('');
      // Full width alone, two columns, or (M10-M12) a full-width box above the right column.
      assert.ok(['W', 'LR', 'RW'].includes(cols), 'colonne della slide ' + s.page + ': ' + cols);
      for (const it of s.items.filter(x => x.t === 'figure')) {
        assert.ok(fs.existsSync(path.join(root, it.src)), it.src);
        assert.ok(it.ratio > 0.3 && it.ratio <= 1 && it.w > 0 && it.h > 0, it.src);
        assert.ok(!('tex' in it));
      }
    }
  });

  test(id + ': ogni file di codice appartiene alla sua slide e dipende solo da slide precedenti', () => {
    if (cfg.standalone) {
      // T00, M13-M16: script autonomi per capitolo, collegati alla prima slide che li cita.
      const cited = L.slides.flatMap(s => s.items.filter(x => x.t === 'code').map(x => [x.file, s.page]));
      assert.deepEqual(Object.keys(L.code).sort(), [...new Set(cited.map(c => c[0]))].sort());
      for (const [file, page] of cited) {
        assert.equal(L.code[file].page, Math.min(...cited.filter(c => c[0] === file).map(c => c[1])), file);
        assert.ok(L.code[file].page <= page);
        assert.deepEqual(L.code[file].deps, []);
        assert.equal(L.code[file].code, read(path.join(cfg.source, 'Codice', file)).replace(/\n+$/, ''));
        assert.equal(L.code[file].lang === 'python', file.endsWith('.py'));
      }
      assert.ok(!('setup' in L.project));
      return;
    }
    const files = fs.readdirSync(path.join(root, cfg.source, 'Codice')).filter(f => /^\d{2,3}_.*\.R$/.test(f));
    assert.deepEqual(Object.keys(L.code).sort(), files.sort());
    for (const s of L.slides)
      for (const it of [...s.items.filter(x => x.t === 'code'), ...(s.code || [])]) {
        assert.equal(parseInt(it.file, 10), s.page);
        assert.equal(L.code[it.file].code, read(path.join(cfg.source, 'Codice', it.file)).replace(/\n+$/, ''));
        for (const d of L.code[it.file].deps) assert.ok(parseInt(d, 10) < s.page && L.code[d], it.file + ' → ' + d);
      }
  });

  test(id + ': i laboratori citati esistono e i parametri sono nel loro dominio', () => {
    for (const s of L.slides)
      for (const lab of [
        ...(s.labs || []),
        ...s.items.filter(x => x.t === 'lab').map(x => ({ id: x.lab, params: {} })),
      ]) {
        const a = labs.get(lab.id);
        assert.ok(a, lab.id);
        for (const [k, v] of Object.entries(lab.params)) {
          const c = a.controls.find(x => x.key === k);
          assert.ok(c, lab.id + '.' + k);
          if (c.type !== 'select') assert.ok(v >= c.min && v <= c.max, lab.id + '.' + k + '=' + v);
        }
      }
  });

  test(id + ': spiegazioni estese con titoli identici alle slide e solo collegamenti ammessi', { skip: !md }, () => {
    const { intro, notes } = explanations(read('content/lezioni/' + id + '.md'), L.slides);
    assert.ok(intro.length > 0);
    assert.ok(Object.keys(notes).length > 0);
    assert.throws(() => inline('[x](javascript:alert(1))'), /Destinazione non ammessa/);
    assert.throws(() => explanations('## 16 · Titolo diverso\n\nTesto.', L.slides), /diverso dalla slide/);
    for (const blocks of [intro, ...Object.values(notes)])
      for (const b of blocks) assert.ok(b.t === 'p' || b.t === 'math', 'solo paragrafi e formule');
    assert.throws(
      () => explanations('## 16 · ' + L.slides[15].title + '\n\n### Titolo\n\nTesto.', L.slides),
      /Solo paragrafi/,
    );
    assert.throws(() => explanations('## 16 · ' + L.slides[15].title + '\n\n- voce', L.slides), /Solo paragrafi/);
    const text = read('content/lezioni/' + id + '.md');
    for (const banned of ['—', 'non solo', 'Inoltre', 'In sintesi', 'fondamentale', 'cruciale', 'Conviene', 'Prova a'])
      assert.ok(!text.includes(banned), 'espressione da evitare: ' + banned);
  });

  test(id + ': schede del quaderno con scenari validi e controlli numerici', { skip: !E }, () => {
    assert.ok(E.cards.length >= 9);
    for (const c of E.cards) {
      assert.ok(labs.has(c.id));
      assert.deepEqual(Object.keys(c.scenarios).sort(), ['A', 'B']);
      // Quaderni con valori attesi: indicatori da verificare; senza (M06): la tabella del confronto.
      assert.ok(cfg.expected ? c.fields.length >= 1 : c.fields.length === 0 && c.table.length >= 2, c.id);
      assert.ok(fs.existsSync(path.join(root, cfg.source, c.script.file)), c.script.file);
      for (const f of c.fields) {
        assert.ok(Number.isFinite(f.value) && f.tol >= 0);
        assert.ok(!/\.\d+(\.\d+)?%$/.test(f.label), f.label);
      }
    }
  });

  test(id + ': percorsi della lezione e degli esercizi', () => {
    const index = { [id]: { pages: L.pages, cards: E ? E.cards.length : 0 } };
    assert.deepEqual(C.parseRoute('#lezione-' + id, cat, index), { type: 'lesson', id, page: null });
    assert.deepEqual(C.parseRoute('#lezione-' + id + '/16', cat, index), { type: 'lesson', id, page: 16 });
    assert.equal(C.parseRoute('#lezione-' + id + '/' + (L.pages + 1), cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-' + id + '/0', cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-' + id + '/016', cat, index).type, 'notfound');
    if (E) {
      assert.deepEqual(C.parseRoute('#esercizi-' + id, cat, index), { type: 'exercises', id, card: 1 });
      assert.equal(C.parseRoute('#esercizi-' + id + '/' + (E.cards.length + 1), cat, index).type, 'notfound');
    } else assert.equal(C.parseRoute('#esercizi-' + id, cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-M99', cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-' + id, cat).type, 'notfound');
  });
}

test('Verifica numerica delle schede: virgola, tolleranza e testo non numerico', () => {
  const ctx = vm.createContext({
    GeoHTML: { html: () => '' },
    GeoSecurity: { limits: { notes: 20000, code: 100000 } },
  });
  vm.runInContext(read('src/lessons.js'), ctx);
  const { check, parse } = ctx.GeoLessons;
  const se = { value: 0.258198889747161, tol: 0.0005 },
    exact = { value: -1, tol: 0 };
  assert.ok(check(se, '0,258'));
  assert.ok(check(se, ' 0.2582 '));
  assert.ok(!check(se, '0.26'));
  assert.ok(check(exact, '-1'));
  assert.ok(!check(exact, '-1.001'));
  assert.ok(Number.isNaN(parse('1,2,3')));
  assert.ok(Number.isNaN(parse('abc')));
});
