import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const context = vm.createContext({});
vm.runInContext(fs.readFileSync('src/security.js', 'utf8'), context);
const S = context.GeoSecurity;
const activity = JSON.parse(fs.readFileSync('content/experiments.json')).activities.find(a => a.id === 'm05-intervalli');
const config = more => JSON.stringify({application:'GeoStatLab', version:1, activity:activity.id, parameters:{}, ...more});
test('JSON rejects prototype pollution, excessive nesting and oversize documents', () => {
  for (const key of ['__proto__', 'constructor', 'prototype']) assert.throws(() => S.parseJSON('{"nested":{"' + key + '":{}}}'));
  assert.throws(() => S.parseJSON('['.repeat(14) + '0' + ']'.repeat(14)));
  assert.throws(() => S.parseJSON(' '.repeat(S.limits.config + 1)));
  assert.equal({}.polluted, undefined);
});
test('Parameters reject R injection, coercions and unknown keys', () => {
  for (const v of ['17;system("x")', '17', null, true, {}, [], Infinity, NaN, -1]) assert.throws(() => S.parameters(activity, {seed:v}));
  assert.throws(() => S.parameters(activity, {unknown:1}));
  assert.throws(() => S.parameters(activity, []));
  assert.equal(S.parameters(activity, {seed:17}).seed, 17);
});
test('Imported configuration enforces version, activity and payload limits', () => {
  assert.equal(S.configuration(activity, config({})).code, activity.code);
  for (const more of [{version:2}, {activity:'m01-disegno'}, {code:{}}, {code:'x'.repeat(100001)}, {notes:'x'.repeat(20001)}, {script:'alert(1)'}]) assert.throws(() => S.configuration(activity, config(more)));
  // Code remains data at this boundary; the explicit UI execution gate is tested in the DOM.
  const program = 'stop("review me")'; assert.equal(S.configuration(activity, config({code:program})).code, program);
});
test('Result contract rejects HTML in numeric metadata and oversized tables', () => {
  const good = {rows:1, data:[{x:1}], metrics:[{grandezza:'media',valore:1}], figures:['<svg/>'], csv:'x\n1', R:'R',ggplot2:'4',svglite:'2'};
  assert.equal(S.result(good).rows, 1);
  for (const delta of [{rows:'<img src=x onerror=alert(1)>'}, {rows:100001}, {data:new Array(81).fill({x:1})}, {figures:new Array(7).fill('<svg/>')}, {metrics:[{valore:{html:'x'}}]}, {csv:{}}]) assert.throws(() => S.result({...good,...delta}));
});
test('CSV formula injection is neutralised without changing negative numeric data', () => {
  const input = 'name,value\n"=HYPERLINK(""https://invalid.test"")",-2.5\n"\t=1+1",-1e-3\n"text,comma","line\nbreak"\n@SUM(1),+1\n';
  const out = S.csv(input);
  assert(out.includes('"\'=HYPERLINK(')); assert(out.includes('"\'\t=1+1"')); assert(out.includes('"\'@SUM(1)"')); assert(out.includes('"\'+1"'));
  assert(out.includes('"-2.5"')); assert(out.includes('"-1e-3"')); assert(out.includes('"text,comma"')); assert(out.includes('"line\nbreak"'));
  assert.throws(() => S.csv('"unclosed')); assert.throws(() => S.csv('"closed"payload'));
});
test('R parameter names cannot inject expressions into generated scripts', () => {
  const sandbox = {window:{GeoSecurity:S},setTimeout,clearTimeout};
  vm.runInNewContext(fs.readFileSync('src/lab-engine.js','utf8'),sandbox);
  assert.throws(() => sandbox.window.GeoREngine.paramsCode({'x);stop("oops");list(x':1}));
  assert.match(sandbox.window.GeoREngine.paramsCode({x:'a"b'}), /x="a\\"b"/);
});
