import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { JSDOM } from 'jsdom';
import { load } from './source.mjs';
const research = JSON.parse(fs.readFileSync('content/solution-guides-research.json'));
const course = JSON.parse(fs.readFileSync('content/course-solutions-prepared.json'));
const projects = Object.keys(research).map(id => JSON.parse(fs.readFileSync('content/research-' + id + '.json')));
function setup() {
  const dom = new JSDOM('<main></main>', { runScripts: 'outside-only' }),
    w = dom.window;
  w.GEO_SOLUTIONS = { research, course };
  load(w, 'html', 'code-terminal', 'solution-terminal');
  return { w, host: w.document.querySelector('main') };
}
test('Worked solutions cover all actual research code and the 11 complete course scripts', () => {
  const { w, host } = setup();
  let stages = 0;
  for (const a of projects) {
    const g = research[a.id],
      blocks = a.code.trim().split(/\n\s*\n/);
    assert.deepEqual(
      g.stages.flatMap(s => s.blocks),
      blocks.map((_, i) => i),
    );
    assert.equal(w.GeoSolutions.partialProgram(a, g, g.stages.length - 1), a.code);
    stages += g.stages.length;
  }
  assert.equal(stages, 23);
  assert.equal(Object.keys(course).length, 11);
  for (const [id, g] of Object.entries(course)) {
    const t = w.GeoSolutions.mountCourse(host, id);
    assert.equal(host.querySelectorAll('[data-solution-stage]').length, g.stages.length);
    assert(!host.querySelector('[data-solution-run]'));
    assert(host.textContent.includes('RStudio'));
    assert(g.code.includes('source('));
    t.destroy();
  }
  w.close();
});
test('Hints and code never execute implicitly; staged runs use the real prefix and variants retain their own program', () => {
  const { w, host } = setup(),
    a = projects.find(p => p.id === 'usgs-quakes'),
    g = research[a.id];
  let runs = [],
    downloads = [],
    dirty = [];
  const t = w.GeoSolutions.mount(host, a, g, {
    params: Object.fromEntries(a.controls.map(c => [c.key, c.value])),
    execute: c => runs.push(c),
    dirty: s => dirty.push(s),
    downloadBody: s => downloads.push(s),
  });
  host.querySelector('[data-solution-mode=hints]').click();
  assert.equal(host.querySelector('.solution-hints').hidden, false);
  assert.equal(host.querySelectorAll('.solution-hints details').length, 3);
  host.querySelector('[data-solution-mode=guided]').click();
  host.querySelector('[data-solution-stage="1"]').click();
  assert.equal(runs.length, 0);
  host.querySelector('[data-solution-run=step]').click();
  assert.equal(runs.length, 1);
  assert.equal(runs[0].partial, true);
  assert.equal(runs[0].body, w.GeoSolutions.partialProgram(a, g, 1));
  t.setBusy(true);
  host.querySelector('[data-solution-run=full]').click();
  assert.equal(runs.length, 1);
  t.setBusy(false);
  host.querySelector('[data-solution-mode=code]').click();
  const editor = host.querySelector('textarea');
  const custom = 'stop("<img src=x onerror=alert(1)>")';
  editor.value = custom;
  editor.dispatchEvent(new w.Event('input'));
  assert.equal(runs.length, 1);
  assert(dirty.length);
  host.querySelector('[data-solution-download-variant]').click();
  assert.deepEqual(downloads, [custom]);
  host.querySelector('[data-solution-run=custom]').click();
  assert.equal(runs[1].body, custom);
  assert.equal(runs[1].custom, true);
  assert.equal(host.querySelectorAll('img,[onerror]').length, 0);
  t.completed({ metrics: [] }, runs[1]);
  assert(host.querySelector('.solution-live').hidden);
  assert.match(host.querySelector('.solution-status').textContent, /Variante/);
  t.completed({ metrics: [{ grandezza: 'Eventi selezionati', valore: 42 }] }, { partial: false, custom: false });
  assert(!host.querySelector('.solution-live').hidden);
  assert.match(host.querySelector('.solution-live p').textContent, /42 eventi/);
  t.invalidate('Parametri modificati');
  assert(host.querySelector('.solution-live').hidden);
  t.destroy();
  w.close();
});
test('Project solutions have one stage navigator and one reference download; experiment navigation remains available', () => {
  const { w, host } = setup(),
    a = projects[0],
    params = Object.fromEntries(a.controls.map(c => [c.key, c.value]));
  const standalone = w.GeoCodeGuide.mount(host, a, params);
  assert(!host.querySelector('[data-r=focus]').hidden);
  assert(!host.querySelector('footer').hidden);
  standalone.destroy();
  const solution = w.GeoSolutions.mount(host, a, research[a.id], { params });
  host.querySelector('[data-solution-mode=code]').click();
  for (const selector of [
    '.r-terminal-head',
    '[data-r=focus]',
    '[data-r=edit]',
    '.r-step-tools',
    '.r-step-reading',
    '.r-terminal footer',
  ])
    assert(host.querySelector(selector).hidden, selector);
  assert(!host.querySelector('[data-r=comments]').hidden);
  assert.equal(host.querySelectorAll('[data-solution-download]').length, 1);
  solution.destroy();
  const local = w.GeoSolutions.mountCourse(host, 'P01');
  assert.match(host.querySelector('.r-terminal-state').textContent, /esecuzione locale/);
  local.destroy();
  w.close();
});
