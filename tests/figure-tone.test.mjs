import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

// The browser and the importer map figure colours with the same function. The fixture comes from
// scripts/lessons/figure_tone.py (python3 scripts/lessons/figure_tone.py --fixture tests/figure-tone.fixture.json).
const read = f => fs.readFileSync(new URL('../' + f, import.meta.url), 'utf8');
const ctx = vm.createContext({ GeoHTML: { html: () => '' }, GeoSecurity: { limits: {} } });
vm.runInContext(read('src/lessons.js'), ctx);
const { tone } = ctx.GeoLessons;
const colours = s => [...s.matchAll(/#([0-9A-F]{6})\b/gi)].map(m => m[1]);

for (const c of JSON.parse(read('tests/figure-tone.fixture.json')))
  test('Figure sul pannello, stessa trasformazione in Python e nel browser: ' + c.name, () => {
    const got = tone(c.input),
      a = colours(got),
      b = colours(c.expected);
    assert.equal(got.replace(/#[0-9A-F]{6}\b/gi, '#'), c.expected.replace(/#[0-9A-F]{6}\b/gi, '#'));
    assert.equal(a.length, b.length);
    a.forEach((h, i) => {
      // pow() may differ in the last bit between engines: one unit per channel at most.
      for (const k of [0, 2, 4])
        assert.ok(Math.abs(parseInt(h.slice(k, k + 2), 16) - parseInt(b[i].slice(k, k + 2), 16)) <= 1, h + ' ' + b[i]);
    });
  });

test('Testo e tratti chiari sullo sfondo del pannello', () => {
  const out = tone(
    '<svg><path fill="#F8F6F1" d=""/><g fill="#253344"><use xlink:href="#glyph-0-1"/></g><path stroke="#087C74"/></svg>',
  );
  assert.match(out, /fill="#0B192B"/);
  assert.match(out, /<g fill="#E3EEF5"><use/);
  assert.match(out, /stroke="#5CC9B8"/);
});
