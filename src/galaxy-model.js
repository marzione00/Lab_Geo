/* Deterministic world coordinates and camera math shared by both renderers.
   Distances and planet sizes are illustrative, not astronomical scales. */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2;
  const anchors = {
    T00: [-9.3, 1.1, 8.5],
    M01: [-6.1, 1.7, 4.2],
    M02: [-11.7, 1.0, 0.4],
    M03: [-10, 1.8, -6.5],
    M04: [-5.2, 1.2, -10],
    M05: [-3.8, 1.7, -3.7],
    M06: [-0.3, 1.2, -12],
    M07: [4.4, 1.9, -9.5],
    M08: [8.4, 1.3, -6.4],
    M09: [12, 1.6, -1.7],
    M10: [10.5, 1.4, 4.8],
    M11: [6.6, 1.9, 8.8],
    M12: [2.3, 1.1, 11.6],
    M13: [-2, 1.8, 8.6],
    M14: [3.0, 1.4, 3.5],
    M15: [4.8, 1.1, -3.5],
    M16: [-2.3, 1.7, 1.7],
  };
  const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
  function random(seed) {
    return () => {
      seed |= 0;
      seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const unit = v => {
    const n = Math.hypot(...v) || 1;
    return v.map(x => x / n);
  };
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
  const identity = () => new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
  function multiply(a, b) {
    const o = new Float32Array(16);
    for (let c = 0; c < 4; c++)
      for (let r = 0; r < 4; r++) for (let k = 0; k < 4; k++) o[c * 4 + r] += a[k * 4 + r] * b[c * 4 + k];
    return o;
  }
  function rotation(angle) {
    const c = Math.cos(angle),
      s = Math.sin(angle);
    return new Float32Array([c, 0, -s, 0, 0, 1, 0, 0, s, 0, c, 0, 0, 0, 0, 1]);
  }
  const rotate = (p, a) => [p[0] * Math.cos(a) + p[2] * Math.sin(a), p[1], -p[0] * Math.sin(a) + p[2] * Math.cos(a)];
  const destination = (id, angle) =>
    rotate(
      anchors[id].map((v, i) => (i === 1 ? v : v * 0.72)),
      angle,
    );
  const fitDistance = (width, height, distance = 34) =>
    distance * Math.max(1, width < 580 ? (2 * height) / width : (0.65 * height) / (width - 2 * (156 + 40)));
  function model(p, r, tilt = 0) {
    const c = Math.cos(tilt) * r,
      s = Math.sin(tilt) * r;
    return new Float32Array([c, s, 0, 0, -s, c, 0, 0, 0, 0, r, 0, ...p, 1]);
  }
  function camera(azimuth, elevation, distance, target, aspect) {
    const eye = [
      target[0] + distance * Math.cos(elevation) * Math.sin(azimuth),
      target[1] + distance * Math.sin(elevation),
      target[2] + distance * Math.cos(elevation) * Math.cos(azimuth),
    ];
    const z = unit(eye.map((v, i) => v - target[i])),
      x = unit(cross([0, 1, 0], z)),
      y = cross(z, x);
    const view = new Float32Array([
      x[0],
      y[0],
      z[0],
      0,
      x[1],
      y[1],
      z[1],
      0,
      x[2],
      y[2],
      z[2],
      0,
      -dot(x, eye),
      -dot(y, eye),
      -dot(z, eye),
      1,
    ]);
    const f = 1 / Math.tan((43 * Math.PI) / 360),
      near = 0.1,
      far = 180;
    const projection = new Float32Array([
      f / aspect,
      0,
      0,
      0,
      0,
      f,
      0,
      0,
      0,
      0,
      (far + near) / (near - far),
      -1,
      0,
      0,
      (2 * far * near) / (near - far),
      0,
    ]);
    return { eye, view, projection, vp: multiply(projection, view), f };
  }
  function project(p, m, w, h) {
    const x = m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
      y = m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
      depth = m[3] * p[0] + m[7] * p[1] + m[11] * p[2] + m[15];
    return {
      x: ((x / depth + 1) * w) / 2,
      y: ((1 - y / depth) * h) / 2,
      depth,
      visible: depth > 0.1 && Math.abs(x / depth) < 1.1 && Math.abs(y / depth) < 1.1,
    };
  }
  function labels(worlds, width, height) {
    const narrow = width < 580,
      bw = narrow ? 84 : 156,
      bh = narrow ? 34 : 48,
      margin = narrow ? 7 : 16;
    const sorted = [...worlds].sort((a, b) => a.screen.x - b.screen.x),
      cut = Math.ceil(sorted.length / 2),
      result = [];
    for (const [side, list] of [
      ['left', sorted.slice(0, cut)],
      ['right', sorted.slice(cut)],
    ]) {
      list.sort((a, b) => a.screen.y - b.screen.y);
      const top = 78,
        bottom = height - 70 - bh,
        gap = Math.min(bh + 10, (bottom - top) / Math.max(1, list.length - 1));
      const ys = list.map(p => clamp(p.screen.y - bh / 2, top, bottom));
      for (let i = 1; i < ys.length; i++) ys[i] = Math.max(ys[i], ys[i - 1] + gap);
      if (ys.length && ys[ys.length - 1] > bottom) {
        ys[ys.length - 1] = bottom;
        for (let i = ys.length - 2; i >= 0; i--) ys[i] = Math.min(ys[i], ys[i + 1] - gap);
      }
      list.forEach((p, i) =>
        result.push({
          id: p.id,
          x: side === 'left' ? margin : width - margin - bw,
          y: ys[i],
          width: bw,
          height: bh,
          side,
        }),
      );
    }
    return result;
  }
  function particles(count = 120000) {
    const rng = random(92026),
      stars = [],
      dust = [];
    const normal = () => Math.sqrt(-2 * Math.log(Math.max(1e-7, rng()))) * Math.cos(TAU * rng());
    for (let i = 0; i < count; i++) {
      const bulge = i < count * 0.13,
        field = i > count * 0.95,
        interarm = !bulge && !field && i % 7 === 0;
      const r = bulge ? Math.abs(normal()) * 2.1 : Math.pow(rng(), 0.63) * 19.8 + 0.4;
      const arm = i % 4,
        a =
          field || interarm
            ? rng() * TAU
            : (arm * TAU) / 4 +
              Math.log(r + 0.6) * 1.8 +
              r * 0.11 +
              normal() * (bulge ? 2 : 0.1 + r * 0.004) +
              Math.sin(r * 1.9 + arm) * 0.035;
      const pos = field
        ? [(rng() - 0.5) * 110, (rng() - 0.5) * 55, (rng() - 0.5) * 110]
        : [Math.cos(a) * r, normal() * (bulge ? 0.82 : 0.15 + 0.22 * Math.exp(-r / 8)), Math.sin(a) * r];
      const warm = bulge || r < 4.2,
        pink = !warm && rng() < 0.09;
      const color = warm
        ? [1, 0.82 + rng() * 0.15, 0.65 + rng() * 0.27]
        : pink
          ? [0.83, 0.55, 0.85]
          : [0.57 + rng() * 0.3, 0.74 + rng() * 0.2, 1];
      stars.push({
        p: pos,
        c: color,
        a: bulge ? 0.16 : interarm ? 0.22 : 0.28 + rng() * 0.48,
        size: (field ? 0.025 : 0.011) + Math.pow(rng(), 10) * 0.12,
      });
      if (!field && !interarm && i % 9 === 0)
        dust.push({
          p: pos.map((n, k) => n + (k === 1 ? normal() * 0.2 : normal() * 0.4)),
          c: warm ? [0.9, 0.54, 0.28] : pink ? [0.37, 0.2, 0.48] : [0.22, 0.37, 0.64],
          a: bulge ? 0.009 : 0.014,
          size: bulge ? 1.6 : 0.8 + rng() * 1.8,
        });
    }
    return { stars, dust };
  }
  // Odd sampling strides retain all four arms. Canvas still draws tens of thousands of stars.
  function softwareParticles(data) {
    return [...data.dust.filter((_, i) => i % 3 === 0), ...data.stars.filter((_, i) => i % 3 === 0)];
  }
  root.GeoGalaxyModel = Object.freeze({
    anchors,
    clamp,
    identity,
    multiply,
    rotation,
    rotate,
    destination,
    fitDistance,
    model,
    camera,
    project,
    labels,
    particles,
    softwareParticles,
  });
})(globalThis);
