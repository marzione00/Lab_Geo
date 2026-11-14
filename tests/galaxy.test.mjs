import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { load } from './source.mjs';
const scope = {};
load(scope, 'galaxy-model');
const M = scope.GeoGalaxyModel;
const near = (a, b) => assert(Math.abs(a - b) < 0.0001, `${a} != ${b}`);

test('Galaxy catalogue maps each course module to a distinct 3D position', () => {
  const modules = JSON.parse(fs.readFileSync('content/catalogue.json')).modules.filter(m => m.category !== 'progetti');
  assert.deepEqual(Object.keys(M.anchors).sort(), modules.map(m => m.id).sort());
  assert.equal(new Set(Object.values(M.anchors).map(p => JSON.stringify(p))).size, 17);
  for (const p of Object.values(M.anchors)) {
    assert(p.every(Number.isFinite));
    const q = M.rotate(p, 0.83);
    near(Math.hypot(...q), Math.hypot(...p));
    near(q[1], p[1]);
    const back = M.rotate(q, -0.83);
    p.forEach((v, i) => near(v, back[i]));
  }
});

test('Perspective camera preserves its target, depth and zoom at different viewpoints', () => {
  for (const azimuth of [0, 0.7, 2.4])
    for (const elevation of [0.25, 0.83, 1.36]) {
      const camera = M.camera(azimuth, elevation, 37, [0, 0, 0], 1.5);
      const centre = M.project([0, 0, 0], camera.vp, 900, 600);
      near(centre.x, 450);
      near(centre.y, 300);
      near(centre.depth, 37);
      assert(centre.visible);
      const behind = camera.eye.map(v => v * 2);
      assert(!M.project(behind, camera.vp, 900, 600).visible);
    }
  const far = M.project([4, 0, 0], M.camera(0, 0.83, 37, [0, 0, 0], 1.5).vp, 900, 600);
  const close = M.project([4, 0, 0], M.camera(0, 0.83, 22, [0, 0, 0], 1.5).vp, 900, 600);
  assert(close.x > far.x);
});

test('Default portrait and desktop cameras keep all destinations in the scene', () => {
  for (const [width, height] of [
    [300, 600],
    [390, 600],
    [660, 740],
    [970, 790],
  ]) {
    const distance = M.fitDistance(width, height);
    for (const angle of [0, 0.8, 1.7, 3.14]) {
      const vp = M.camera(0, 0.66, distance, [0, 0, 0], width / height).vp;
      for (const id of Object.keys(M.anchors)) assert(M.project(M.destination(id, angle), vp, width, height).visible);
    }
  }
});

test('Particles are reproducible and volumetric; software sampling retains all spiral arms', () => {
  const a = M.particles(),
    b = M.particles();
  assert.equal(JSON.stringify(a), JSON.stringify(b));
  assert.equal(a.stars.length, 120000);
  assert(a.stars.every(p => [...p.p, ...p.c, p.a, p.size].every(Number.isFinite)));
  assert(a.stars.some(p => p.p[1] > 0.5) && a.stars.some(p => p.p[1] < -0.5));
  const simplified = M.softwareParticles(a),
    arms = [0, 0, 0, 0];
  const indices = new Map(a.stars.map((p, i) => [p, i]));
  for (const p of simplified) {
    const i = indices.get(p);
    if (i > 20000 && i < 110000) arms[i % 4]++;
  }
  assert(
    arms.every(n => n > 7000),
    JSON.stringify(arms),
  );
  assert(Math.max(...arms) - Math.min(...arms) <= 1);
});

test('Callouts remain separated and inside the chart after camera rotations', () => {
  for (const [width, height] of [
    [300, 600],
    [390, 600],
    [660, 740],
    [970, 790],
  ])
    for (const angle of [0, 0.7, 1.7, 3.14]) {
      const camera = M.camera(0.3, 0.66, M.fitDistance(width, height), [0, 0, 0], width / height);
      const worlds = Object.keys(M.anchors).map(id => ({
        id,
        screen: M.project(M.destination(id, angle), camera.vp, width, height),
      }));
      const labels = M.labels(worlds, width, height);
      assert.equal(labels.length, 17);
      for (const l of labels) {
        assert(l.x >= 0 && l.x + l.width <= width);
        assert(l.y >= 70 && l.y + l.height <= height - 50);
      }
      for (const side of ['left', 'right']) {
        const list = labels.filter(l => l.side === side).sort((a, b) => a.y - b.y);
        for (let i = 1; i < list.length; i++) assert(list[i].y >= list[i - 1].y + list[i - 1].height);
      }
    }
});
