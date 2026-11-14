import test from 'node:test';
import assert from 'node:assert/strict';
import { load } from './source.mjs';
test('Procedural nebula worker produces bounded, deterministic RGBA pixels and rejects oversized requests', () => {
  const outputs = [],
    self = { postMessage: v => outputs.push(v) };
  load({ self }, 'cosmos-worker');
  self.onmessage({ data: { id: 1, width: 48, height: 32 } });
  assert.equal(outputs.length, 1);
  const first = new Uint8ClampedArray(outputs[0].pixels);
  assert.equal(first.length, 48 * 32 * 4);
  for (let i = 3; i < first.length; i += 4) assert.equal(first[i], 255);
  assert(new Set(first).size > 50, 'Nebula must contain visible detail');
  self.onmessage({ data: { id: 2, width: 48, height: 32 } });
  assert.deepEqual(new Uint8ClampedArray(outputs[1].pixels), first);
  self.onmessage({ data: { id: 3, width: 100000, height: 100000 } });
  assert.equal(outputs.length, 2);
});
