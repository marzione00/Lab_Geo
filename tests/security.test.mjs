import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { load } from './source.mjs';
const context = vm.createContext({});
load(context, 'security');
const S = context.GeoSecurity;
const activity = JSON.parse(fs.readFileSync('content/experiments.json')).activities.find(
  a => a.id === 'm05-intervalli',
);
const config = more =>
  JSON.stringify({ application: 'GeoStatLab', version: 1, activity: activity.id, parameters: {}, ...more });
test('JSON rejects prototype pollution, excessive nesting and oversize documents', () => {
  for (const key of ['__proto__', 'constructor', 'prototype'])
    assert.throws(() => S.parseJSON('{"nested":{"' + key + '":{}}}'));
  assert.throws(() => S.parseJSON('['.repeat(14) + '0' + ']'.repeat(14)));
  assert.throws(() => S.parseJSON(' '.repeat(S.limits.config + 1)));
  assert.equal({}.polluted, undefined);
});
test('Parameters reject R injection, coercions and unknown keys', () => {
  for (const v of ['17;system("x")', '17', null, true, {}, [], Infinity, NaN, -1])
    assert.throws(() => S.parameters(activity, { seed: v }));
  assert.throws(() => S.parameters(activity, { unknown: 1 }));
  assert.throws(() => S.parameters(activity, []));
  assert.equal(S.parameters(activity, { seed: 17 }).seed, 17);
});
test('Imported configuration enforces version, activity and payload limits', () => {
  assert.equal(S.configuration(activity, config({})).code, activity.code);
  for (const more of [
    { version: 2 },
    { activity: 'm01-disegno' },
    { code: {} },
    { code: 'x'.repeat(100001) },
    { notes: 'x'.repeat(20001) },
    { script: 'alert(1)' },
  ])
    assert.throws(() => S.configuration(activity, config(more)));
  // Code remains data at this boundary; the explicit UI execution gate is tested in the DOM.
  const program = 'stop("review me")';
  assert.equal(S.configuration(activity, config({ code: program })).code, program);
});
test('Result contract rejects HTML in numeric metadata and oversized tables', () => {
  const good = {
    rows: 1,
    data: [{ x: 1 }],
    metrics: [{ grandezza: 'media', valore: 1 }],
    figures: ['<svg/>'],
    csv: 'x\n1',
    R: 'R',
    ggplot2: '4',
    svglite: '2',
  };
  assert.equal(S.result(good).rows, 1);
  assert.throws(() => S.result({ ...good, figures: [] }));
  assert.equal(S.result({ ...good, figures: [] }, { allowEmptyFigures: true }).figures.length, 0);
  assert.throws(() => S.result({ ...good, figures: [], rows: 100001 }, { allowEmptyFigures: true }));
  for (const delta of [
    { rows: '<img src=x onerror=alert(1)>' },
    { rows: 100001 },
    { data: new Array(81).fill({ x: 1 }) },
    { figures: new Array(7).fill('<svg/>') },
    { metrics: [{ valore: { html: 'x' } }] },
    { csv: {} },
  ])
    assert.throws(() => S.result({ ...good, ...delta }));
});
test('CSV formula injection is neutralised without changing negative numeric data', () => {
  const input =
    'name,value\n"=HYPERLINK(""https://invalid.test"")",-2.5\n"\t=1+1",-1e-3\n"text,comma","line\nbreak"\n@SUM(1),+1\n';
  const out = S.csv(input);
  assert(out.includes('"\'=HYPERLINK('));
  assert(out.includes('"\'\t=1+1"'));
  assert(out.includes('"\'@SUM(1)"'));
  assert(out.includes('"\'+1"'));
  assert(out.includes('"-2.5"'));
  assert(out.includes('"-1e-3"'));
  assert(out.includes('"text,comma"'));
  assert(out.includes('"line\nbreak"'));
  assert.throws(() => S.csv('"unclosed'));
  assert.throws(() => S.csv('"closed"payload'));
});
test('R parameter names cannot inject expressions into generated scripts', () => {
  const sandbox = { window: { GeoSecurity: S }, setTimeout, clearTimeout };
  load(sandbox, 'lab-engine');
  assert.throws(() => sandbox.window.GeoREngine.paramsCode({ 'x);stop("oops");list(x': 1 }));
  assert.match(sandbox.window.GeoREngine.paramsCode({ x: 'a"b' }), /x="a\\"b"/);
});
test('Installed R packages must match the pinned lock', () => {
  const sandbox = { window: { GeoSecurity: S }, setTimeout, clearTimeout };
  load(sandbox, 'lab-engine');
  const drift = sandbox.window.GeoREngine.packageDrift;
  const lock = JSON.parse(fs.readFileSync('vendor/r-packages-lock.json', 'utf8'));
  const listing = lock
    .filter(p => p.package !== 'cpp11')
    .map(p => p.package + '=' + p.version)
    .concat(['base=4.6.0', 'stats=4.6.0'])
    .join(';');
  assert.deepEqual([...drift(lock, listing)], []);
  assert.match(drift(lock, listing.replace(/ggplot2=[^;]+/, 'ggplot2=9.9.9')).join(), /ggplot2 9\.9\.9/);
  assert.match(drift(lock, listing.replace(/svglite=[^;]+;?/, '')).join(), /svglite assente/);
});
test('R result validation keeps its contract (characterisation)', () => {
  const ok = () => ({
    rows: 3,
    data: [{ x: 1 }],
    metrics: [{ name: 'a', value: 1 }],
    figures: ['<svg/>'],
    R: '4.6.0',
    ggplot2: '4.0.3',
    svglite: '2.2',
    csv: 'x\n1',
  });
  assert.equal(S.result(ok()).rows, 3);
  assert.equal(S.result({ ...ok(), figures: [] }, { allowEmptyFigures: true }).figures.length, 0);
  const cases = [
    [{ ...ok(), rows: -1 }, /formato o una dimensione/],
    [{ ...ok(), rows: 1.5 }, /formato o una dimensione/],
    [{ ...ok(), rows: S.limits.rows + 1 }, /formato o una dimensione/],
    [{ ...ok(), data: 'x' }, /formato o una dimensione/],
    [{ ...ok(), data: Array.from({ length: 81 }, () => ({ x: 1 })) }, /formato o una dimensione/],
    [{ ...ok(), metrics: Array.from({ length: S.limits.metrics + 1 }, () => ({ x: 1 })) }, /formato o una dimensione/],
    [{ ...ok(), figures: [] }, /formato o una dimensione/],
    [{ ...ok(), figures: Array.from({ length: S.limits.figures + 1 }, () => '<svg/>') }, /formato o una dimensione/],
    [{ ...ok(), data: [{ x: {} }] }, /valori non supportati/],
    [{ ...ok(), metrics: [{ x: Infinity }] }, /valori non supportati/],
    [
      { ...ok(), data: [Object.fromEntries(Array.from({ length: S.limits.cells + 1 }, (_, i) => ['c' + i, i]))] },
      /valori non supportati/,
    ],
    [{ ...ok(), data: [{ x: 'y'.repeat(20001) }] }, /valori non supportati/],
    [{ ...ok(), figures: [1] }, /dimensione consentita/],
    [{ ...ok(), ggplot2: 4 }, /Metadati R non validi/],
    [{ ...ok(), R: 'r'.repeat(201) }, /Metadati R non validi/],
    [{ ...ok(), csv: 7 }, /Esportazione CSV non valida/],
  ];
  for (const [value, message] of cases) assert.throws(() => S.result(value), message);
});
