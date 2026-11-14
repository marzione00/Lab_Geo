/* Orthographic sphere renderer for browsers without WebGL.
   Texture coordinates rotate on a sphere; lighting and the limb remain fixed. */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2;
  function create(canvas, onTexture = () => window.GeoSpace?.refresh()) {
    const ctx = canvas.getContext('2d', { alpha: true }),
      textures = new Map(),
      pending = new Set(),
      cache = new Map();
    if (!ctx) throw Error('Canvas 2D non disponibile');
    let cloud = null,
      night = null,
      disposed = false,
      cachePixels = 0;
    function load(src) {
      return new Promise((resolve, reject) => {
        const im = new Image();
        im.onload = () => {
          const c = document.createElement('canvas');
          c.width = im.width;
          c.height = im.height;
          const x = c.getContext('2d', { willReadFrequently: true });
          x.drawImage(im, 0, 0);
          resolve({ w: c.width, h: c.height, p: x.getImageData(0, 0, c.width, c.height).data });
        };
        im.onerror = reject;
        im.src = src;
      });
    }
    function texture(id, p) {
      if (disposed) return null;
      if (textures.has(id)) return textures.get(id);
      if (!pending.has(id)) {
        pending.add(id);
        load(
          root.GeoFamilies
            ? root.GeoFamilies.texture(p)
            : 'assets/space/' + (id === 'M01' ? 'day' : 'p-' + id) + '.webp',
        )
          .then(t => {
            if (disposed) return;
            textures.set(id, t);
            onTexture();
          })
          .catch(() => pending.delete(id));
      }
      return null;
    }
    function projection(p, res, hero, light) {
      const lightKey = light ? light.map(v => Math.round(v * 32) / 32).join(',') : 'default';
      const key = p.id + ':' + res + ':' + hero + ':' + lightKey;
      if (cache.has(key)) return cache.get(key);
      const c = document.createElement('canvas');
      c.width = res;
      c.height = res;
      const x = c.getContext('2d');
      const im = x.createImageData(res, res);
      const indices = [],
        uv = [],
        lights = [],
        rims = [],
        specs = [];
      const axis = -p.tilt,
        ca = Math.cos(axis),
        sa = Math.sin(axis),
        cx = Math.cos(-0.24),
        sx = Math.sin(-0.24);
      let lx = hero ? -0.42 : -0.6,
        ly = hero ? 0.84 : 0.65,
        lz = hero ? -0.36 : 0.8;
      if (light) {
        [lx, ly, lz] = lightKey.split(',').map(Number);
      }
      let len = Math.hypot(lx, ly, lz) || 1;
      lx /= len;
      ly /= len;
      lz /= len;
      const hx = lx,
        hy = ly,
        hz = lz + 1,
        hn = Math.hypot(hx, hy, hz);
      for (let y = 0; y < res; y++)
        for (let xx = 0; xx < res; xx++) {
          const nx = ((xx + 0.5) / res) * 2 - 1,
            ny = 1 - ((y + 0.5) / res) * 2,
            d = nx * nx + ny * ny;
          if (d >= 1) continue;
          const nz = Math.sqrt(1 - d),
            qx = ca * nx - sa * ny,
            qy = sa * nx + ca * ny,
            qz = nz;
          const yy = cx * qy - sx * qz,
            zz = sx * qy + cx * qz;
          const pixel = (y * res + xx) * 4;
          indices.push(pixel);
          im.data[pixel + 3] = Math.min(255, (1 - Math.sqrt(d)) * res * 0.5 * 255);
          uv.push(0.5 - Math.atan2(zz, qx) / TAU, 0.5 - Math.asin(Math.max(-1, Math.min(1, yy))) / Math.PI);
          const lit = nx * lx + ny * ly + nz * lz;
          lights.push(lit);
          rims.push(Math.pow(1 - nz, 4.2) * (0.03 + Math.max(0, lit) * 0.4));
          specs.push(Math.pow(Math.max(0, (nx * hx + ny * hy + nz * hz) / hn), 100) * 0.5);
        }
      const result = {
        c,
        x,
        im,
        indices: new Uint32Array(indices),
        uv: new Float32Array(uv),
        lights: new Float32Array(lights),
        rims: new Float32Array(rims),
        specs: new Float32Array(specs),
      };
      while (cache.size && (cachePixels + res * res > 1400000 || cache.size >= 16)) {
        const oldest = cache.keys().next().value;
        const removed = cache.get(oldest);
        cachePixels -= removed.c.width * removed.c.height;
        cache.delete(oldest);
      }
      cache.set(key, result);
      cachePixels += res * res;
      return result;
    }
    // Hot loop: one pass per surface sample (at most 20 Hz). Kept inline on purpose; splitting it into
    // per-pixel helpers measured about 20% slower in Chromium, and this renderer runs without a GPU.
    // eslint-disable-next-line complexity
    function resampleSurface(p, a, tex, res, time, angle, shift) {
      const out = a.im.data;
      const atm = [1, 3, 5].map(i => parseInt(p.atmosphere.slice(i, i + 2), 16));
      for (let i = 0; i < a.indices.length; i++) {
        const v = a.uv[i * 2 + 1],
          flow = p.kind === 4 || p.kind === 10 ? (time * 0.004 * (1 - 2 * v)) / TAU : 0;
        const u = (a.uv[i * 2] + shift + flow) % 1,
          un = u < 0 ? u + 1 : u,
          idx = (Math.min(tex.h - 1, Math.floor(v * tex.h)) * tex.w + Math.min(tex.w - 1, Math.floor(un * tex.w))) * 4;
        let r = tex.p[idx],
          gg = tex.p[idx + 1],
          b = tex.p[idx + 2],
          light = a.lights[i],
          shade = 0.12 + Math.max(0, light) * 0.91;
        if (res >= 320) {
          const tx = un * tex.w - 0.5,
            ty = Math.max(0, Math.min(tex.h - 1, v * tex.h - 0.5));
          const x0 = (Math.floor(tx) + tex.w) % tex.w,
            x1 = (x0 + 1) % tex.w,
            y0 = Math.floor(ty),
            y1 = Math.min(tex.h - 1, y0 + 1),
            fx = tx - Math.floor(tx),
            fy = ty - y0;
          const i0 = (y0 * tex.w + x0) * 4,
            i1 = (y0 * tex.w + x1) * 4,
            i2 = (y1 * tex.w + x0) * 4,
            i3 = (y1 * tex.w + x1) * 4;
          const a0 = (1 - fx) * (1 - fy),
            a1 = fx * (1 - fy),
            a2 = (1 - fx) * fy,
            a3 = fx * fy;
          r = tex.p[i0] * a0 + tex.p[i1] * a1 + tex.p[i2] * a2 + tex.p[i3] * a3;
          gg = tex.p[i0 + 1] * a0 + tex.p[i1 + 1] * a1 + tex.p[i2 + 1] * a2 + tex.p[i3 + 1] * a3;
          b = tex.p[i0 + 2] * a0 + tex.p[i1 + 2] * a1 + tex.p[i2 + 2] * a2 + tex.p[i3 + 2] * a3;
        }
        if (p.kind === 14 && r > gg * 1.8 && r > 100) {
          shade = Math.max(0.8, shade);
        }
        let rr = r * shade,
          gc = gg * shade,
          bb = b * shade;
        if (p.kind === 0 && !p.familyId && cloud) {
          const cu = (a.uv[i * 2] + (angle * 1.012 + 0.04) / TAU) % 1,
            cv = cu < 0 ? cu + 1 : cu;
          const ci =
            (Math.min(cloud.h - 1, Math.floor(v * cloud.h)) * cloud.w +
              Math.min(cloud.w - 1, Math.floor(cv * cloud.w))) *
            4;
          const cl = Math.max(0, Math.min(0.88, (cloud.p[ci + 2] / 255 - 0.2) / 0.72)) * 0.88;
          const white = 255 * (0.07 + Math.max(0, light) * 0.86);
          rr = rr * (1 - cl) + white * 0.88 * cl;
          gc = gc * (1 - cl) + white * 0.94 * cl;
          bb = bb * (1 - cl) + white * cl;
          const water =
            1 -
            cloud.p[
              (Math.min(cloud.h - 1, Math.floor(v * cloud.h)) * cloud.w +
                Math.min(cloud.w - 1, Math.floor(un * cloud.w))) *
                4 +
                1
            ] /
              255;
          const spec = a.specs[i] * water * (1 - cl) * 150;
          rr += spec;
          gc += spec;
          bb += spec;
          if (light < 0.08 && night) {
            const ni =
                (Math.min(night.h - 1, Math.floor(v * night.h)) * night.w +
                  Math.min(night.w - 1, Math.floor(un * night.w))) *
                4,
              nf = Math.min(1, (0.08 - light) * 5);
            rr += night.p[ni] * nf * 0.65;
            gc += night.p[ni + 1] * nf * 0.65;
            bb += night.p[ni + 2] * nf * 0.65;
          }
        }
        if (p.kind === 14 && r > gg * 1.8 && r > 100) {
          rr *= 1.3;
          gc *= 1.4;
          bb *= 1.5;
        }
        const o = a.indices[i],
          rim = a.rims[i];
        out[o] = Math.min(255, rr + atm[0] * rim);
        out[o + 1] = Math.min(255, gc + atm[1] * rim);
        out[o + 2] = Math.min(255, bb + atm[2] * rim);
      }
      a.x.putImageData(a.im, 0, 0);
    }
    // Texture resolution of the projected disc, by its radius on screen.
    const resolution = r => (r > 170 ? 640 : r > 90 ? 320 : r > 35 ? 160 : 80);
    function paint(p, g, time, opacity = 1, offset = 0) {
      const tex = texture(p.familyId || p.textureId || p.id, p);
      if (!tex) return;
      const res = resolution(g.r),
        hero = g.hero > 0.4 ? 1 : 0;
      const a = projection(p, res, hero, g.light);
      // Keep smooth sphere placement at the display frame rate; resample surface at 20 Hz.
      const sampleTime = Math.floor(time * 20) / 20,
        angle = p.phase - sampleTime * p.speed + offset,
        shift = angle / TAU;
      const surfaceKey = [
        p.familyId || p.textureId || p.id,
        p.kind,
        p.phase,
        p.speed,
        sampleTime,
        offset,
        p.atmosphere,
        Boolean(cloud),
        Boolean(night),
      ].join(':');
      if (a.surfaceKey !== surfaceKey) {
        resampleSurface(p, a, tex, res, time, angle, shift);
        a.surfaceKey = surfaceKey;
      }
      ctx.save();
      ctx.globalAlpha = opacity;
      const glow = ctx.createRadialGradient(g.x, g.y, g.r * 0.995, g.x, g.y, g.r * 1.035);
      glow.addColorStop(0, p.atmosphere + '44');
      glow.addColorStop(0.16, p.atmosphere + '16');
      glow.addColorStop(1, p.atmosphere + '00');
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(g.x, g.y, g.r * 1.04, 0, TAU);
      ctx.fill();
      if (hero) {
        const sunx = g.x - g.r * 0.452,
          suny = g.y - g.r * 0.905,
          sun = ctx.createRadialGradient(sunx, suny, 0, sunx, suny, g.r * 0.07);
        sun.addColorStop(0, '#fff4dcff');
        sun.addColorStop(0.06, '#ffe8bdc9');
        sun.addColorStop(0.2, '#f4c0884d');
        sun.addColorStop(1, '#f4c08800');
        ctx.fillStyle = sun;
        ctx.beginPath();
        ctx.arc(sunx, suny, g.r * 0.07, 0, TAU);
        ctx.fill();
      }
      function rings(front) {
        ctx.save();
        ctx.translate(g.x, g.y);
        ctx.rotate(-0.34);
        ctx.scale(1, 0.43);
        for (let k = 0; k < 30; k++) {
          let radius = g.r * (1.22 + k * 0.025);
          if (k > 15 && k < 18) continue;
          ctx.strokeStyle = p.high + (k % 3 ? '72' : 'b0');
          ctx.lineWidth = g.r * 0.018;
          ctx.beginPath();
          ctx.arc(0, 0, radius, front ? 0 : 0, front ? Math.PI : TAU);
          ctx.stroke();
        }
        ctx.restore();
      }
      if (p.rings) rings(false);
      ctx.drawImage(a.c, g.x - g.r, g.y - g.r, g.r * 2, g.r * 2);
      if (p.rings) rings(true);
      ctx.restore();
    }
    const ready = Promise.all([
      load('assets/space/day.webp').then(t => {
        if (!disposed) textures.set('M01', t);
      }),
      load('assets/space/surface.webp').then(t => {
        if (!disposed) cloud = t;
      }),
      load('assets/space/night.webp').then(t => {
        if (!disposed) night = t;
      }),
    ]);
    return {
      ctx,
      ready,
      paint,
      textureCount: () => textures.size,
      clear(w, h, dpr) {
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, w, h);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      },
      dispose() {
        disposed = true;
        textures.clear();
        pending.clear();
        cache.clear();
        cachePixels = 0;
        cloud = null;
        night = null;
      },
    };
  }
  root.GeoCPU = Object.freeze({ create });
})(globalThis);
