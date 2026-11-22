import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { explanations, inline } from '../scripts/lessons/build-lessons.mjs';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const config = JSON.parse(read('lezioni/lezioni.json'));
const cat = JSON.parse(read('content/catalogue.json')).modules;
const NB = JSON.parse(read('content/notebook.json'));
await import('../src/core.js');
const C = globalThis.GeoCore;

// Stile delle spiegazioni estese: prosa accademica senza formule di contrapposizione ricorrenti
// e senza frasi che descrivono la slide al posto del concetto. Le righe di titolo sono escluse,
// perché riportano alla lettera i titoli delle slide.
const STYLE = [
  /—/,
  /\bnon solo\b/,
  /\bnon soltanto\b/,
  /\b[Ii]noltre\b/,
  /\bIn sintesi\b/,
  /\b[Ff]ondamental[ei]\b/,
  /\b[Cc]rucial[ei]\b/,
  /\b[Cc]onvien[ea]\b/,
  /\bProva a\b/,
  /\bsenza essere\b/,
  /(?<!\p{L})anziché(?!\p{L})/u,
  /\bma non\b/,
  /, e non\b/,
  /\binvece d(?:i|el|ella|ello|egli|elle|ei)\b/,
  /\b[Ii]l richiamo (?:riassume|ricorda|indica|fissa|descrive|delimita|applica|distingue|elenca|chiude|sintetizza|dichiara|riprende)\b/,
  /\bNel richiamo\b/,
  /\b[Ll]a domanda (?:della slide )?chiede\b/,
  /\btesto risponde\b/,
  /\b[Ii]l testo della slide\b/,
];
const styleIssues = text =>
  text
    .split('\n')
    .flatMap((line, i) =>
      line.startsWith('## ') ? [] : STYLE.filter(p => p.test(line)).map(p => i + 1 + ': ' + p.source),
    );

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
      assert.ok(!s.image, 'nessuna pagina come immagine: slide ' + s.page);
    });
    // Copertina ricomposta come testo: pianeta o spedizione, modulo, titolo, sottotitoli, autore, licenza.
    const cover = L.slides[0].lines;
    assert.ok(
      cover.length >= 6 && /^(MODULO|MACROPROGETTO) /.test(cover[1]) && /CC BY-NC-SA 4\.0/.test(cover.at(-1)),
      cover.join(' | '),
    );
    assert.ok(!fs.readdirSync(path.join(root, 'assets/lezioni', id)).some(f => /^\d{3}\./.test(f)), 'pagina raster');
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
      // Nessuna pagina ritagliata intera: i riquadri sono testo del pannello, le figure soltanto diagrammi.
      assert.ok(!(s.items.length === 1 && s.items[0].t === 'figure'), 'slide ' + s.page + ' ritagliata dal PDF');
      for (const it of s.items.filter(x => x.t === 'figure')) {
        assert.ok(fs.existsSync(path.join(root, it.src)), it.src);
        assert.ok(it.ratio > 0.3 && it.ratio <= 1 && it.w > 0 && it.h > 0, it.src);
        assert.ok(!('tex' in it));
        // Figure portate sul pannello scuro: nessuno sfondo chiaro della pagina.
        assert.ok(it.src.endsWith('.svg') && read(it.src).slice(0, 2000).includes('data-tono="pannello"'), it.src);
      }
    }
  });

  test(id + ': ogni file di codice appartiene alla sua slide e dipende solo da slide precedenti', () => {
    if (cfg.standalone) {
      // T00, M13-M16 e spedizioni: script autonomi, collegati alla prima slide che li cita.
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
    const { intro, notes, chapters } = explanations(read('content/lezioni/' + id + '.md'), L.slides, L.sections);
    assert.ok(intro.length > 0);
    assert.ok(Object.keys(notes).length > 0);
    // Ogni capitolo di almeno quattro tappe ha un'introduzione discorsiva, salvo le sezioni di cornice.
    const frame =
      /^(COPERTINA|PERCORSO|IL CASO GUIDA|SINTESI|RIFERIMENTI|DOMANDA CENTRALE|CONCLUSIONI|LABORATORI DELLA SPEDIZIONE)$/;
    const due = L.sections.filter(sec => !frame.test(sec.title) && sec.last - sec.first >= 3).map(sec => sec.first);
    assert.deepEqual(Object.keys(chapters).map(Number), due, 'introduzioni ai capitoli');
    assert.throws(
      () => explanations('## Capitolo · INESISTENTE\n\nTesto.', L.slides, L.sections),
      /Capitolo inesistente/,
    );
    assert.throws(() => inline('[x](javascript:alert(1))'), /Destinazione non ammessa/);
    assert.throws(() => explanations('## 16 · Titolo diverso\n\nTesto.', L.slides), /diverso dalla slide/);
    for (const blocks of [intro, ...Object.values(notes)])
      for (const b of blocks) assert.ok(b.t === 'p' || b.t === 'math', 'solo paragrafi e formule');
    assert.throws(
      () => explanations('## 16 · ' + L.slides[15].title + '\n\n### Titolo\n\nTesto.', L.slides),
      /Solo paragrafi/,
    );
    assert.throws(() => explanations('## 16 · ' + L.slides[15].title + '\n\n- voce', L.slides), /Solo paragrafi/);
    assert.deepEqual(styleIssues(read('content/lezioni/' + id + '.md')), [], 'espressioni da evitare');
    assert.deepEqual(styleIssues('## 3 · Quando conviene\n\nTesto.'), [], 'i titoli delle slide restano esclusi');
    assert.equal(styleIssues('Il richiamo riassume la regola.\nUna stima, e non una misura.').length, 2);
  });

  test(id + ': schede del quaderno con scenari validi, senza domande né controlli', { skip: !E }, () => {
    assert.ok(E.cards.length >= 9);
    for (const c of E.cards) {
      assert.ok(labs.has(c.id));
      assert.deepEqual(Object.keys(c.scenarios).sort(), ['A', 'B']);
      // Quaderni con valori attesi: gli indicatori danno le colonne della tabella; senza (M06): la tabella del quaderno.
      assert.ok(!('questions' in c), c.id);
      assert.ok(cfg.expected ? c.fields.length >= 1 : c.fields.length === 0 && c.table.length >= 2, c.id);
      assert.ok(fs.existsSync(path.join(root, cfg.source, c.script.file)), c.script.file);
      for (const f of c.fields) {
        assert.ok(Number.isFinite(f.value) && f.tol >= 0);
        assert.ok(!/\.\d+(\.\d+)?%$/.test(f.label), f.label);
      }
    }
  });

  test(id + ': percorsi della lezione e degli esercizi', () => {
    const nb = NB[id]?.notebooks.length || 0,
      index = { [id]: { pages: L.pages, cards: E ? E.cards.length : 0, notebooks: nb } };
    assert.deepEqual(C.parseRoute('#lezione-' + id, cat, index), { type: 'lesson', id, page: null });
    assert.deepEqual(C.parseRoute('#lezione-' + id + '/16', cat, index), { type: 'lesson', id, page: 16 });
    assert.equal(C.parseRoute('#lezione-' + id + '/' + (L.pages + 1), cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-' + id + '/0', cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-' + id + '/016', cat, index).type, 'notfound');
    if (E) {
      assert.deepEqual(C.parseRoute('#esercizi-' + id, cat, index), { type: 'exercises', id, card: 1 });
      assert.equal(C.parseRoute('#esercizi-' + id + '/' + (E.cards.length + 1), cat, index).type, 'notfound');
    } else if (nb) {
      // Companion world with notebooks only: the page exists, a card number does not.
      assert.deepEqual(C.parseRoute('#esercizi-' + id, cat, index), { type: 'exercises', id, card: 1 });
      assert.equal(C.parseRoute('#esercizi-' + id + '/1', cat, index).type, 'notfound');
    } else assert.equal(C.parseRoute('#esercizi-' + id, cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-M99', cat, index).type, 'notfound');
    assert.equal(C.parseRoute('#lezione-' + id, cat).type, 'notfound');
  });
}

test('Notebook svolti: venti per lezione M01-M12, pagine e tappe esistenti, archivio dei sorgenti', () => {
  assert.deepEqual(
    Object.keys(NB).sort(),
    Object.keys(config)
      .filter(id => /^M(0\d|1[0-2])$/.test(id))
      .sort(),
  );
  for (const [id, nb] of Object.entries(NB)) {
    const L = JSON.parse(read('content/lezioni/' + id + '.json'));
    assert.equal(nb.notebooks.length, 20, id);
    assert.ok(fs.existsSync(path.join(root, nb.download)), nb.download);
    for (const n of nb.notebooks) {
      assert.ok(fs.existsSync(path.join(root, 'lezioni/Notebook_M01-M12', n.html.replace(/^notebook\//, ''))), n.html);
      assert.ok(
        n.pages.every(p => p >= 1 && p <= L.pages),
        n.id,
      );
      // Le presentazioni M10-M12 citano ogni notebook nel piè di pagina di almeno una slide.
      if (['M10', 'M11', 'M12'].includes(id)) assert.ok(n.pages.length > 0, n.id);
    }
  }
});
