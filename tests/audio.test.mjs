import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { load } from './source.mjs';

// A stand-in for the Web Audio API that records the graph instead of producing sound.
function fakeAudio() {
  const created = { oscillators: 0, sources: 0, convolvers: 0 };
  const param = value => ({
    value,
    setValueAtTime() {},
    linearRampToValueAtTime() {},
    exponentialRampToValueAtTime() {},
    setTargetAtTime(v) {
      this.value = v;
    },
    cancelScheduledValues() {},
  });
  const node = extra => ({ connect: target => target, ...extra });
  const ctx = {
    state: 'running',
    sampleRate: 24000,
    currentTime: 0,
    destination: node(),
    resume() {
      this.state = 'running';
    },
    suspend() {
      this.state = 'suspended';
    },
    createGain: () => node({ gain: param(1) }),
    createBiquadFilter: () => node({ frequency: param(350), Q: param(1), type: 'lowpass' }),
    createDynamicsCompressor: () =>
      node({ threshold: param(0), knee: param(0), ratio: param(1), attack: param(0), release: param(0) }),
    createConvolver: () => (created.convolvers++, node({ buffer: null })),
    createBuffer: (channels, length) => ({
      getChannelData: () => new Float32Array(length),
      numberOfChannels: channels,
    }),
    createOscillator: () => (
      created.oscillators++,
      node({ frequency: param(440), detune: param(0), type: 'sine', start() {}, stop() {} })
    ),
    createBufferSource: () => (created.sources++, node({ buffer: null, loop: false, start() {}, stop() {} })),
  };
  return { ctx, created };
}

function page() {
  const listeners = {};
  const document = {
    hidden: false,
    addEventListener: (type, fn) => (listeners[type] ||= []).push(fn),
    dispatchEvent: e => (listeners[e.type] || []).forEach(fn => fn(e)),
  };
  const context = vm.createContext({ document, performance: { now: () => 0 }, setTimeout, clearTimeout, Math });
  context.window = context;
  context.CustomEvent = class {
    constructor(type, init) {
      this.type = type;
      this.detail = init?.detail;
    }
  };
  return { context, listeners };
}

test('Audio: nessun ascoltatore e nessun nodo prima del consenso', () => {
  const { context, listeners } = page();
  load(context, 'audio');
  assert.ok(context.GeoAudio);
  assert.deepEqual(Object.keys(listeners), []);
  assert.equal(context.GeoAudio.state().enabled, false);
});

test('Audio: il consenso costruisce la catena e i segnali producono suoni', () => {
  const { context } = page();
  load(context, 'audio');
  const { ctx, created } = fakeAudio();
  context.GeoAudio.enable(ctx, 0.5);
  assert.equal(created.convolvers, 1, 'one reverb');
  const padOscillators = created.oscillators;
  assert.ok(padOscillators >= 10, 'ambient pad running');
  for (const name of ['travel', 'arrive', 'r-start', 'r-done', 'select', 'open', 'error']) {
    context.document.dispatchEvent(new context.CustomEvent('geostat:cue', { detail: { name, duration: 1 } }));
  }
  assert.ok(created.oscillators > padOscillators && created.sources > 0);
  context.GeoAudio.disable();
  assert.equal(context.GeoAudio.state().enabled, false);
  const after = created.oscillators;
  context.document.dispatchEvent(new context.CustomEvent('geostat:cue', { detail: { name: 'select' } }));
  assert.equal(created.oscillators, after, 'silent after disable');
});

test('Audio: volume limitato fra 0 e 1', () => {
  const { context } = page();
  load(context, 'audio');
  context.GeoAudio.setVolume(3);
  assert.equal(context.GeoAudio.state().volume, 1);
  context.GeoAudio.setVolume(-1);
  assert.equal(context.GeoAudio.state().volume, 0);
});
