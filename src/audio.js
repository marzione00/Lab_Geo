/* Ship audio, synthesised with the Web Audio API: an ambient pad, interface sounds and event sounds.
   No audio files are fetched, so the Content-Security-Policy keeps media-src 'none'. Loaded on demand by
   app.js after the reader turns audio on; app.js creates the AudioContext inside that click. */
(function (root) {
  'use strict';
  const midi = n => 440 * 2 ** ((n - 69) / 12);
  // D minor: i add9, VI maj7, III add9, VII sus2. Each chord holds for CHORD_SECONDS and crossfades.
  const CHORDS = [
    [38, 50, 53, 57, 64],
    [34, 46, 50, 53, 57],
    [41, 48, 53, 57, 67],
    [36, 48, 50, 55, 62],
  ];
  const CHORD_SECONDS = 26,
    PAD_LEVEL = 0.03;

  let ctx = null,
    master = null,
    dry = null,
    wet = null,
    pad = null,
    chordTimer = 0,
    chordIndex = 0,
    voices = [],
    pulse = null,
    enabled = false,
    volume = 0.6,
    lastHover = 0,
    hovered = null;

  const now = () => ctx.currentTime;
  const gain = (value, to) => {
    const g = ctx.createGain();
    g.gain.value = value;
    if (to) g.connect(to);
    return g;
  };

  // Impulse response generated once: mono noise with an exponential decay of 1.8 s, kept short and mono
  // because convolution is the most expensive node of the graph.
  function reverb() {
    const seconds = 1.8,
      length = Math.round(ctx.sampleRate * seconds),
      ir = ctx.createBuffer(1, length, ctx.sampleRate),
      data = ir.getChannelData(0);
    for (let i = 0; i < length; i++) data[i] = (Math.random() * 2 - 1) * Math.exp((-5 * i) / length);
    const node = ctx.createConvolver();
    node.buffer = ir;
    return node;
  }

  function build() {
    const limiter = ctx.createDynamicsCompressor();
    limiter.threshold.value = -10;
    limiter.knee.value = 0;
    limiter.ratio.value = 20;
    limiter.attack.value = 0.003;
    limiter.release.value = 0.25;
    limiter.connect(ctx.destination);
    master = gain(0, limiter);
    dry = gain(1, master);
    const room = reverb();
    room.connect(master);
    wet = gain(0.5, room);
    pad = gain(PAD_LEVEL);
    pad.connect(dry);
    const padSend = gain(0.9, wet);
    pad.connect(padSend);
  }

  let noiseBuffer = null;
  function noise() {
    if (!noiseBuffer) {
      noiseBuffer = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
      const d = noiseBuffer.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    }
    const src = ctx.createBufferSource();
    src.buffer = noiseBuffer;
    src.loop = true;
    return src;
  }

  // Ambient pad: two detuned sawtooth oscillators per note through a slowly breathing low-pass filter.
  function chord() {
    const t = now(),
      filter = ctx.createBiquadFilter(),
      lfo = ctx.createOscillator(),
      depth = gain(450),
      env = gain(0, pad);
    filter.type = 'lowpass';
    filter.frequency.value = 900;
    filter.Q.value = 0.7;
    lfo.frequency.value = 0.035;
    lfo.connect(depth).connect(filter.frequency);
    filter.connect(env);
    env.gain.setValueAtTime(0, t);
    env.gain.linearRampToValueAtTime(1, t + 7);
    const oscillators = [lfo];
    for (const n of CHORDS[chordIndex % CHORDS.length]) {
      for (const cents of [-7, 7]) {
        const o = ctx.createOscillator();
        o.type = 'sawtooth';
        o.frequency.value = midi(n);
        o.detune.value = cents;
        o.connect(gain(0.12, filter));
        oscillators.push(o);
      }
    }
    oscillators.forEach(o => o.start(t));
    for (const v of voices) release(v, 9);
    voices = [{ env, oscillators }];
    chordIndex++;
    chordTimer = setTimeout(chord, CHORD_SECONDS * 1000);
  }

  function release(voice, seconds) {
    const t = now();
    voice.env.gain.cancelScheduledValues(t);
    voice.env.gain.setValueAtTime(voice.env.gain.value, t);
    voice.env.gain.linearRampToValueAtTime(0, t + seconds);
    voice.oscillators.forEach(o => o.stop(t + seconds + 0.1));
  }

  // Short envelopes shared by the interface sounds.
  function tone(type, freq, start, length, level, toFreq) {
    const t = now() + start,
      o = ctx.createOscillator(),
      g = gain(0, dry);
    o.type = type;
    o.frequency.setValueAtTime(freq, t);
    if (toFreq) o.frequency.exponentialRampToValueAtTime(toFreq, t + length);
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(level, t + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, t + length);
    o.connect(g);
    g.connect(gain(0.35, wet));
    o.start(t);
    o.stop(t + length + 0.05);
  }

  function sweep(length, from, to, level, type = 'lowpass') {
    const t = now(),
      src = noise(),
      f = ctx.createBiquadFilter(),
      g = gain(0, dry);
    f.type = type;
    f.frequency.setValueAtTime(from, t);
    f.frequency.exponentialRampToValueAtTime(to, t + length);
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(level, t + length * 0.7);
    g.gain.linearRampToValueAtTime(0, t + length);
    src.connect(f).connect(g);
    g.connect(gain(0.5, wet));
    src.start(t);
    src.stop(t + length + 0.05);
  }

  function tick() {
    const t = now(),
      src = noise(),
      f = ctx.createBiquadFilter(),
      g = gain(0, dry);
    f.type = 'bandpass';
    f.frequency.value = 3200;
    f.Q.value = 4;
    g.gain.setValueAtTime(0.05, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.025);
    src.connect(f).connect(g);
    src.start(t);
    src.stop(t + 0.04);
  }

  function startPulse() {
    if (pulse) return;
    const t = now(),
      o = ctx.createOscillator(),
      lfo = ctx.createOscillator(),
      depth = gain(0.5),
      level = gain(0, dry),
      am = gain(0.5);
    o.frequency.value = midi(62);
    lfo.frequency.value = 0.8;
    lfo.connect(depth).connect(am.gain);
    o.connect(am).connect(level);
    level.gain.linearRampToValueAtTime(0.03, t + 0.6);
    o.start(t);
    lfo.start(t);
    pulse = { level, nodes: [o, lfo], timer: setTimeout(stopPulse, 60000) };
  }

  function stopPulse() {
    if (!pulse) return;
    const t = now();
    pulse.level.gain.cancelScheduledValues(t);
    pulse.level.gain.setValueAtTime(pulse.level.gain.value, t);
    pulse.level.gain.linearRampToValueAtTime(0, t + 0.3);
    pulse.nodes.forEach(n => n.stop(t + 0.35));
    clearTimeout(pulse.timer);
    pulse = null;
  }

  const SOUNDS = {
    hover: tick,
    select: () => {
      tone('sine', midi(74), 0, 0.09, 0.07);
      tone('sine', midi(81), 0.07, 0.12, 0.07);
    },
    open: () => sweep(0.25, 300, 3500, 0.06),
    'briefing-open': () => sweep(0.35, 250, 4000, 0.07),
    'briefing-next': () => SOUNDS.select(),
    'briefing-close': () => {
      tone('sine', midi(81), 0, 0.09, 0.06);
      tone('sine', midi(74), 0.07, 0.14, 0.06);
    },
    error: () => tone('square', 110, 0, 0.16, 0.05, 90),
    travel: d => {
      const length = Math.max(0.6, d.duration || 1.4);
      sweep(length, 200, 4000, 0.09);
      tone('sawtooth', 110, 0, length, 0.03, 220);
    },
    arrive: () => tone('sine', 90, 0, 0.8, 0.2, 50),
    'r-start': startPulse,
    'r-done': () => {
      stopPulse();
      [62, 65, 69].forEach((n, i) => tone('sine', midi(n), i * 0.04, 0.9, 0.05));
    },
    'r-error': () => {
      stopPulse();
      SOUNDS.error();
    },
  };

  function play(name, detail = {}) {
    if (!enabled || ctx?.state !== 'running') return;
    SOUNDS[name]?.(detail);
  }
  const onCue = e => play(e.detail.name, e.detail);

  // Interface sounds come from the page itself: a tick when the mouse enters a control, a chirp on activation.
  const CONTROL = 'a[href], button, summary, select, [role="button"]';
  function onOver(e) {
    if (e.pointerType !== 'mouse') return;
    const el = e.target.closest?.(CONTROL);
    if (!el || el === hovered || el.disabled) return;
    hovered = el;
    const t = performance.now();
    if (t - lastHover > 60) play('hover');
    lastHover = t;
  }
  function onClick(e) {
    const el = e.target.closest?.(CONTROL);
    if (el && !el.closest('.briefing')) play(el.matches('summary') ? 'open' : 'select');
  }
  function onVisibility() {
    if (!ctx || !enabled) return;
    if (document.hidden) ctx.suspend();
    else ctx.resume();
  }

  function enable(context, level = volume) {
    if (!ctx) {
      ctx = context;
      build();
      document.addEventListener('geostat:cue', onCue);
      document.addEventListener('pointerover', onOver, { passive: true });
      document.addEventListener('click', onClick, true);
      document.addEventListener('visibilitychange', onVisibility);
    }
    enabled = true;
    volume = level;
    ctx.resume();
    const t = now();
    master.gain.cancelScheduledValues(t);
    master.gain.setValueAtTime(master.gain.value, t);
    master.gain.linearRampToValueAtTime(volume, t + 1.2);
    if (!chordTimer) chord();
  }

  function disable() {
    if (!ctx || !enabled) return;
    enabled = false;
    stopPulse();
    clearTimeout(chordTimer);
    chordTimer = 0;
    voices.forEach(v => release(v, 0.4));
    voices = [];
    const t = now();
    master.gain.cancelScheduledValues(t);
    master.gain.setValueAtTime(master.gain.value, t);
    master.gain.linearRampToValueAtTime(0, t + 0.4);
    setTimeout(() => !enabled && ctx.suspend(), 500);
  }

  function setVolume(level) {
    volume = Math.max(0, Math.min(1, level));
    if (!ctx || !enabled) return;
    master.gain.setTargetAtTime(volume, now(), 0.05);
  }

  root.GeoAudio = Object.freeze({
    enable,
    disable,
    setVolume,
    state: () => ({ enabled, volume, running: ctx?.state === 'running' }),
  });
})(window);
