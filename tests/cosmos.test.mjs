import test from 'node:test';
import assert from 'node:assert/strict';
import { load } from './source.mjs';

test('Packed galaxy has 1.2 million finite 3D stars, bounded colors and a compact payload', () => {
  const scope = load({}, 'galaxy-model');
  const data = scope.GeoGalaxyModel.packedParticles();
  assert.equal(data.starCount, 1200000);
  assert.equal(data.stars.length, 1200000 * 8);
  assert.equal(data.stars.byteLength, 38400000);
  assert.equal(data.dust.length, data.dustCount * 8);
  let above = 0,
    below = 0;
  for (let i = 0; i < data.stars.length; i += 8) {
    for (let j = 0; j < 8; j++) assert(Number.isFinite(data.stars[i + j]));
    for (let j = 3; j < 7; j++) assert(data.stars[i + j] >= 0 && data.stars[i + j] <= 1);
    assert(data.stars[i + 7] > 0);
    if (data.stars[i + 1] > 0.5) above++;
    if (data.stars[i + 1] < -0.5) below++;
  }
  assert(above > 20000 && below > 20000, 'Galaxy has thickness on both sides of its plane');
  const small = scope.GeoGalaxyModel.packedParticles(1000);
  assert.deepEqual(small, scope.GeoGalaxyModel.packedParticles(1000));
  for (const bad of [0, -1, 2.5, 2000001, NaN]) assert.throws(() => scope.GeoGalaxyModel.packedParticles(bad));
});

test('Worker transfers packed buffers and ignores invalid workloads', () => {
  const outputs = [],
    scope = {};
  scope.self = scope;
  scope.postMessage = (data, transfers) => outputs.push({ data, transfers });
  scope.importScripts = name => {
    assert.equal(name, 'galaxy-model.js');
    load(scope, 'galaxy-model');
  };
  load(scope, 'cosmos-worker');
  scope.onmessage({ data: { count: 9000000 } });
  assert.equal(outputs.length, 0);
  scope.onmessage({ data: { count: 1200000 } });
  assert.equal(outputs.length, 1);
  assert.equal(outputs[0].data.starCount, 1200000);
  assert.equal(outputs[0].transfers[0], outputs[0].data.stars.buffer);
  assert.equal(outputs[0].transfers[1], outputs[0].data.dust.buffer);
});

test('Shared environment has deterministic volumetric stellar coordinates', () => {
  const scope = load({}, 'galaxy-model', 'universe');
  const data = scope.GeoUniverse.skyData();
  assert.equal(data.length / 8, 52000);
  assert.equal(data, scope.GeoUniverse.skyData());
  assert(data.every(Number.isFinite));
  const octants = new Set();
  for (let i = 0; i < data.length; i += 8) octants.add([0, 1, 2].map(j => (data[i + j] >= 0 ? 1 : 0)).join(''));
  assert.equal(octants.size, 8);
});

test('GPU path submits the full galaxy and disposes its environment resources', () => {
  const calls = [],
    created = new Map(),
    deleted = new Map();
  const constants = { MAX_TEXTURE_SIZE: 3379, FRAMEBUFFER_COMPLETE: 36053, POINTS: 0 };
  const gl = new Proxy(
    {},
    {
      get(_, key) {
        if (key.toUpperCase() === key) return constants[key] ?? 1;
        if (key === 'getParameter') return () => 4096;
        if (key === 'getShaderParameter' || key === 'getProgramParameter') return () => true;
        if (key === 'checkFramebufferStatus') return () => constants.FRAMEBUFFER_COMPLETE;
        if (key === 'getAttribLocation') return () => 0;
        if (key === 'getUniformLocation') return (_, name) => name;
        if (key.startsWith('create'))
          return () => {
            created.set(key.slice(6), (created.get(key.slice(6)) || 0) + 1);
            return {};
          };
        if (key.startsWith('delete'))
          return () => {
            deleted.set(key.slice(6), (deleted.get(key.slice(6)) || 0) + 1);
          };
        return (...args) => calls.push([key, ...args]);
      },
    },
  );
  const scope = load({}, 'galaxy-model', 'universe', 'galaxy-scene');
  const data = scope.GeoGalaxyModel.packedParticles();
  const renderer = scope.GeoGalaxyScene.webgl(
    { width: 960, height: 600, getContext: () => gl },
    { stars: [], dust: [] },
    [],
    () => {},
  );
  renderer.updateParticles(data);
  renderer.draw({ camera: scope.GeoGalaxyModel.camera(0, 0.66, 34, [0, 0, 0], 1.6), worlds: [], angle: 0 });
  assert(calls.some(c => c[0] === 'drawArrays' && c[1] === gl.POINTS && c[3] === 1200000));
  assert(calls.some(c => c[0] === 'drawArrays' && c[1] === gl.POINTS && c[3] === 52000));
  renderer.reduceDetail();
  renderer.dispose();
  for (const kind of ['Program', 'Shader', 'Buffer', 'Texture', 'Framebuffer'])
    assert.equal(deleted.get(kind), created.get(kind), kind);
});

test('Software WebGL bounds volume work on portrait screens and reuses a stationary view', () => {
  const calls = [];
  const gl = new Proxy(
    {},
    {
      get(_, key) {
        if (key.toUpperCase() === key) return key;
        if (key === 'getExtension') return () => ({ UNMASKED_RENDERER_WEBGL: 'renderer' });
        if (key === 'getParameter') return () => 'ANGLE (SwiftShader Device)';
        if (key === 'getShaderParameter' || key === 'getProgramParameter') return () => true;
        if (key === 'checkFramebufferStatus') return () => 'FRAMEBUFFER_COMPLETE';
        if (key === 'getUniformLocation') return (_, name) => name;
        if (key === 'getAttribLocation') return () => 0;
        if (key.startsWith('create')) return () => ({});
        return (...args) => calls.push([key, ...args]);
      },
    },
  );
  const scope = load({ GeoCore: { softwareRendering: () => false } }, 'galaxy-model', 'universe');
  const renderer = scope.GeoUniverse.create(gl);
  const camera = scope.GeoGalaxyModel.camera(0, 0.6, 35, [0, 0, 0], 390 / 844);
  renderer.draw(camera, 390, 844);
  const allocation = calls.find(c => c[0] === 'texImage2D');
  assert(allocation[4] * allocation[5] <= 4096, 'CPU rasterisation must stay bounded in portrait orientation');
  assert(calls.some(c => c[0] === 'uniform1f' && c[1] === 'uSteps' && c[2] <= 16));
  assert(calls.some(c => c[0] === 'drawArrays' && c[1] === 'POINTS' && c[3] === 52000));
  const before = calls.length;
  renderer.draw(camera, 390, 844);
  assert.equal(
    calls.slice(before).filter(c => c[0] === 'drawArrays' && c[1] === 'TRIANGLES').length,
    1,
    'A stationary camera only composites the cached volume',
  );
  renderer.reduce();
  renderer.draw(camera, 390, 844);
  assert(renderer.debug().nebulaWidth <= 64, 'Adaptation must never increase CPU workload');
  renderer.dispose();
});
