import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read = p => fs.readFileSync(new URL('../' + p, import.meta.url), 'utf8');
const D = JSON.parse(read('content/briefing.json'));
const texts = [...D.cards.flatMap(c => [c.label, c.title, ...c.lines]), ...Object.values(D.hints).map(h => h.text)];

test('Briefing: cinque schede complete e la scelta audio nella prima', () => {
  assert.equal(D.cards.length, 5);
  for (const c of D.cards) {
    assert.ok(c.id && c.label && c.title && c.lines.length >= 1, c.id);
  }
  assert.equal(D.cards[0].audioChoice, true);
  assert.ok(D.cards.slice(1).every(c => !c.audioChoice));
});

test('Briefing: numeri calcolati dai dati, mai scritti nel testo', () => {
  const known = new Set(['N_SYSTEMS', 'N_MISSIONS', 'N_MODULES', 'N_EXPERIMENTS']);
  for (const t of texts) {
    for (const [, k] of t.matchAll(/\{\{(\w+)\}\}/g)) assert.ok(known.has(k), k);
    assert.doesNotMatch(t, /\b\d+\s+(sistemi|spedizioni|moduli|esperimenti|pianeti|laboratori)\b/i, t);
  }
});

test('Briefing: la chiave di memoria segue la versione dei testi', () => {
  const key = 'geostat:briefing:v' + D.version;
  assert.ok(read('src/app.js').includes(`'${key}'`), 'app.js must check ' + key);
  assert.ok(read('src/briefing.js').includes("'geostat:briefing:v' + D.version"));
});

test('Briefing: un suggerimento per sistema, modulo e laboratorio', () => {
  assert.deepEqual(Object.keys(D.hints).sort(), ['experiment', 'module', 'system']);
  for (const h of Object.values(D.hints)) assert.ok(h.anchor && h.text);
});
