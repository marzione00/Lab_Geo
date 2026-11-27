/* Heavy geometry for the notable objects, computed in a worker: null geodesics of a Schwarzschild black hole
   tabulated for the lensing shaders, and dense triangle meshes (asteroids, comet nucleus, Roche-lobe donor). */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2;

  // ------------------------------------------------------------------ null geodesics (G = c = M = 1)
  // Orbit equation of light: u'' = -u + 3u^2 with u = 1/r and ' = d/dphi. A ray is traced backwards from a
  // static camera at radius rc, leaving at angle alpha from the direction of the hole. RK4 with steps that
  // limit the change of u; visit(phi0, u0, phi1, u1) receives every step. Returns the total sweep of an
  // escaping ray, or -1 for a captured ray or one still orbiting at the limit.
  function trace(rc, alpha, visit, limit) {
    const uc = 1 / rc,
      b = (rc * Math.sin(alpha)) / Math.sqrt(1 - 2 * uc);
    let u = uc,
      w = Math.sign(Math.cos(alpha)) * Math.sqrt(Math.max(0, 1 / (b * b) - uc * uc * (1 - 2 * uc))),
      phi = 0;
    if (!Number.isFinite(w)) w = 1e9;
    while (phi < limit) {
      const h = Math.min(0.008, 0.002 / Math.max(Math.abs(w), 1e-9));
      const k1w = -u + 3 * u * u,
        u2 = u + 0.5 * h * w,
        w2 = w + 0.5 * h * k1w,
        k2w = -u2 + 3 * u2 * u2,
        u3 = u + 0.5 * h * w2,
        w3 = w + 0.5 * h * k2w,
        k3w = -u3 + 3 * u3 * u3,
        u4 = u + h * w3,
        w4 = w + h * k3w,
        k4w = -u4 + 3 * u4 * u4;
      const u1 = u + (h / 6) * (w + 2 * w2 + 2 * w3 + w4);
      w += (h / 6) * (k1w + 2 * k2w + 2 * k3w + k4w);
      if (visit) visit(phi, u, phi + h, u1);
      if (u1 >= 0.5) return -1;
      if (u1 <= 0) return phi + (h * u) / (u - u1);
      phi += h;
      u = u1;
    }
    return -1;
  }
  // Ray directions at the camera: dense near the critical angle on both sides, where sweeps diverge.
  function rayAngles(alphaC, count) {
    const out = [],
      captured = Math.round(count * 0.2),
      near = Math.round(count * 0.4),
      wide = count - captured - near;
    for (let i = 0; i < captured; i++) {
      const k = Math.exp(Math.log(0.002) + (i / (captured - 1)) * (Math.log(21) - Math.log(0.002)));
      out.push(alphaC * (1 - Math.exp(-k)));
    }
    for (let i = 0; i < near; i++) out.push(alphaC + (Math.PI - alphaC) * Math.exp(-21 + (21 * i) / (near - 1)));
    for (let i = 1; i <= wide; i++) out.push(alphaC + ((Math.PI - alphaC) * i) / wide - 1e-9);
    return out.sort((a, b) => a - b);
  }
  // Resample the crossings of one emitter radius on a uniform grid of sweeps. Rays arrive in increasing alpha:
  // inbound crossings then have increasing sweep and outbound crossings decreasing sweep, so the sweep-ordered
  // sequence is the inbound list followed by the reversed outbound list. Values are flat [psi, alpha, ...].
  function resampleRow(inbound, outbound, first, out, offset, nPsi, psiMax, scale, tangent = null) {
    const psiAt = [first[0]],
      alphaAt = [first[1]];
    for (let i = 0; i < inbound.length; i += 2) {
      psiAt.push(inbound[i]);
      alphaAt.push(inbound[i + 1]);
    }
    // The ray tangent to the emitter sphere joins the two branches where alpha is largest.
    if (tangent && tangent[0] > psiAt[psiAt.length - 1]) {
      psiAt.push(tangent[0]);
      alphaAt.push(tangent[1]);
    }
    for (let i = outbound.length - 2; i >= 0; i -= 2) {
      psiAt.push(outbound[i]);
      alphaAt.push(outbound[i + 1]);
    }
    const n = psiAt.length;
    let j = 0;
    for (let c = 0; c < nPsi; c++) {
      const psi = (c / (nPsi - 1)) * psiMax;
      while (j < n - 2 && psiAt[j + 1] < psi) j++;
      const p0 = psiAt[j],
        p1 = psiAt[Math.min(j + 1, n - 1)],
        a0 = alphaAt[j],
        a1 = alphaAt[Math.min(j + 1, n - 1)];
      out[offset + c] = psi > p1 + 1e-9 ? -1 : (p1 > p0 ? a0 + ((a1 - a0) * (psi - p0)) / (p1 - p0) : a0) * scale;
    }
  }
  // Ray from the camera with periapsis exactly at radius r (< rc): its apparent angle and the sweep at periapsis.
  function tangentRay(rc, r) {
    if (r >= rc || r <= 3) return null;
    const alpha = Math.asin(Math.min(1, ((r / Math.sqrt(1 - 2 / r)) * Math.sqrt(1 - 2 / rc)) / rc));
    let prev = null,
      found = null;
    trace(
      rc,
      alpha,
      (p0, u0, p1, u1) => {
        if (found === null && prev && u1 < u0) {
          // Parabola through the last three samples: its vertex is the periapsis.
          const [pa, ua] = prev,
            d1 = (u0 - ua) / (p0 - pa),
            d2 = (u1 - u0) / (p1 - p0),
            curv = (d2 - d1) / ((p1 - pa) / 2);
          found = curv < 0 ? (p0 + pa) / 2 - d1 / curv : p0;
        }
        prev = [p0, u0];
      },
      Math.PI * 3,
    );
    return found === null ? null : [found, alpha];
  }
  // Total sweep of the escaping rays on the grid alpha = alphaC + (pi - alphaC) t^2; -1 before the first ray.
  function skyTable(escaped, alphaC, nSky) {
    escaped.sort((a, b) => a[0] - b[0]);
    const sky = new Float32Array(nSky);
    let j = 0;
    for (let i = 0; i < nSky; i++) {
      const t = i / (nSky - 1),
        a = alphaC + (Math.PI - alphaC) * t * t;
      while (j < escaped.length - 2 && escaped[j + 1][0] < a) j++;
      const [a0, s0b] = escaped[j],
        [a1, s1b] = escaped[j + 1];
      sky[i] = a < a0 ? -1 : s0b + ((s1b - s0b) * (a - a0)) / (a1 - a0 || 1);
    }
    return sky;
  }
  // Lensing tables for one camera radius.
  //  lens: for each emitter radius (rows, logarithmic between rMin and rMax) and sweep angle psi in [0, psiMax]
  //        (columns), eta = alpha * rc of the ray from the camera that reaches that point; -1 where none does.
  //  sky:  total sweep of escaping rays, sampled at alpha = alphaC + (pi - alphaC) t^2, t in [0, 1].
  function lensLevel(rc, o = {}) {
    const { rMin = 3.05, rMax = 320, nR = 256, nPsi = 1024, psiMax = 3 * Math.PI + 0.2, nSky = 2048, rays = 3072 } = o;
    const s0 = Math.sqrt(1 - 2 / rc),
      alphaC = Math.asin(Math.min(1, (3 * Math.sqrt(3) * s0) / rc));
    // Row k has u_k = 1 / r_k, decreasing with k.
    const rowU = Float64Array.from({ length: nR }, (_, k) => 1 / (rMin * (rMax / rMin) ** (k / (nR - 1))));
    const inbound = Array.from({ length: nR }, () => []),
      outbound = Array.from({ length: nR }, () => []);
    // First row index whose u is not above v (binary search on the decreasing array).
    const firstBelow = v => {
      let lo = 0,
        hi = nR;
      while (lo < hi) {
        const m = (lo + hi) >> 1;
        if (rowU[m] > v) lo = m + 1;
        else hi = m;
      }
      return lo;
    };
    const escaped = [];
    let alpha = 0;
    const visit = (p0, u0, p1, u1) => {
      if (p0 > psiMax) return;
      const rising = u1 > u0,
        hiU = rising ? u1 : u0,
        loU = rising ? u0 : u1,
        lists = rising ? inbound : outbound;
      for (let k = firstBelow(hiU); k < nR && rowU[k] >= loU; k++)
        lists[k].push(p0 + ((p1 - p0) * (rowU[k] - u0)) / (u1 - u0), alpha);
    };
    for (const a of rayAngles(alphaC, rays)) {
      alpha = a;
      const sweep = trace(rc, a, visit, a > alphaC ? 16 : psiMax + 0.1);
      if (sweep >= 0 && a > alphaC) escaped.push([a, sweep]);
    }
    const lens = new Float32Array(nPsi * nR);
    for (let k = 0; k < nR; k++) {
      const r = 1 / rowU[k];
      resampleRow(
        inbound[k],
        outbound[k],
        [0, r < rc ? 0 : Math.PI],
        lens,
        k * nPsi,
        nPsi,
        psiMax,
        rc,
        tangentRay(rc, r),
      );
    }
    const sky = skyTable(escaped, alphaC, nSky);
    return { rc, alphaC, lens, sky };
  }
  // One light path from radius start toward the hole, in its orbital plane: points [x, y, r] and its fate.
  function photonPath(b, start) {
    const pts = [];
    let u = 1 / start,
      w = Math.sqrt(Math.max(0, 1 / (b * b) - u * u * (1 - 2 * u))),
      phi = 0;
    for (let i = 0; i < 200000 && u > 0 && u < 0.5 && phi < 40 && 1 / u <= start * 1.02; i++) {
      const r = 1 / u;
      pts.push([r * Math.cos(phi), r * Math.sin(phi), r]);
      const h = Math.min(0.004, 0.001 / Math.max(Math.abs(w), 1e-9));
      const k1 = -u + 3 * u * u,
        u2 = u + 0.5 * h * w,
        w2 = w + 0.5 * h * k1,
        k2 = -u2 + 3 * u2 * u2,
        u3 = u + 0.5 * h * w2,
        w3 = w + 0.5 * h * k2,
        k3 = -u3 + 3 * u3 * u3,
        u4 = u + h * w3,
        w4 = w + h * k3,
        k4 = -u4 + 3 * u4 * u4;
      u += (h / 6) * (w + 2 * w2 + 2 * w3 + w4);
      w += (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4);
      phi += h;
    }
    return { pts, captured: u >= 0.5 };
  }
  // Equal-length resampling of a path into out at offset: x, y, alive (0 at a capture), sqrt(1 - 2/r).
  function resamplePath({ pts, captured }, samples, out, offset) {
    const len = [0];
    for (let i = 1; i < pts.length; i++)
      len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const total = len[len.length - 1];
    let j = 0;
    for (let s = 0; s < samples; s++) {
      const target = (s / (samples - 1)) * total;
      while (j < len.length - 2 && len[j + 1] < target) j++;
      const f = (target - len[j]) / (len[j + 1] - len[j] || 1),
        q = pts[j].map((v, k) => v + (pts[j + 1][k] - v) * f);
      out.set(
        [q[0], q[1], captured && s === samples - 1 ? 0 : 1, Math.sqrt(Math.max(0, 1 - 2 / q[2]))],
        offset + s * 4,
      );
    }
  }
  // Light paths for impact parameters from 1 to 16, concentrated near the critical value 3 sqrt(3).
  function photonPaths({ count = 256, samples = 512, start = 60 } = {}) {
    const out = new Float32Array(count * samples * 4),
      bc = 3 * Math.sqrt(3);
    for (let p = 0; p < count; p++) {
      const t = (p + 0.5) / count,
        b = t < 0.5 ? bc - (bc - 1) * (1 - 2 * t) ** 3 : bc + (16 - bc) * (2 * t - 1) ** 3;
      resamplePath(photonPath(b, start), samples, out, p * samples * 4);
    }
    return { paths: out, count, samples };
  }
  // Camera radii of the tabulated levels; the shaders interpolate between the two nearest ones.
  const levelRadii = (count = 12, near = 42, far = 260) =>
    Array.from({ length: count }, (_, i) => near * (far / near) ** (i / (count - 1)));

  // ------------------------------------------------------------------ meshes
  // Geodesic sphere: subdivided icosahedron with shared vertices (10 * 4^level + 2 vertices).
  function icosphere(level) {
    const t = (1 + Math.sqrt(5)) / 2;
    let v = [
      [-1, t, 0],
      [1, t, 0],
      [-1, -t, 0],
      [1, -t, 0],
      [0, -1, t],
      [0, 1, t],
      [0, -1, -t],
      [0, 1, -t],
      [t, 0, -1],
      [t, 0, 1],
      [-t, 0, -1],
      [-t, 0, 1],
    ].map(p => {
      const n = Math.hypot(...p);
      return p.map(x => x / n);
    });
    let f = [
      [0, 11, 5],
      [0, 5, 1],
      [0, 1, 7],
      [0, 7, 10],
      [0, 10, 11],
      [1, 5, 9],
      [5, 11, 4],
      [11, 10, 2],
      [10, 7, 6],
      [7, 1, 8],
      [3, 9, 4],
      [3, 4, 2],
      [3, 2, 6],
      [3, 6, 8],
      [3, 8, 9],
      [4, 9, 5],
      [2, 4, 11],
      [6, 2, 10],
      [8, 6, 7],
      [9, 8, 1],
    ];
    for (let l = 0; l < level; l++) {
      const cache = new Map(),
        next = [];
      const mid = (a, b) => {
        const key = a < b ? a * 1e7 + b : b * 1e7 + a;
        if (cache.has(key)) return cache.get(key);
        const p = v[a].map((x, i) => x + v[b][i]),
          n = Math.hypot(...p);
        v.push(p.map(x => x / n));
        cache.set(key, v.length - 1);
        return v.length - 1;
      };
      for (const [a, b, c] of f) {
        const ab = mid(a, b),
          bc = mid(b, c),
          ca = mid(c, a);
        next.push([a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]);
      }
      f = next;
    }
    const positions = new Float32Array(v.length * 3);
    v.forEach((p, i) => positions.set(p, i * 3));
    const indices = new Uint32Array(f.length * 3);
    f.forEach((tri, i) => indices.set(tri, i * 3));
    return { positions, indices };
  }
  // Hash-based value noise in 3D with smooth interpolation, and fractal sums of it.
  function hash3(x, y, z, seed) {
    let h =
      (Math.imul(x, 374761393) + Math.imul(y, 668265263) + Math.imul(z, 2147483647) + Math.imul(seed, 144665)) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }
  function noise(x, y, z, seed) {
    const xi = Math.floor(x),
      yi = Math.floor(y),
      zi = Math.floor(z);
    const fx = x - xi,
      fy = y - yi,
      fz = z - zi;
    const s = q => q * q * q * (q * (q * 6 - 15) + 10);
    const u = s(fx),
      v = s(fy),
      w = s(fz);
    let out = 0;
    for (let c = 0; c < 8; c++) {
      const dx = c & 1,
        dy = (c >> 1) & 1,
        dz = (c >> 2) & 1;
      out += hash3(xi + dx, yi + dy, zi + dz, seed) * (dx ? u : 1 - u) * (dy ? v : 1 - v) * (dz ? w : 1 - w);
    }
    return out * 2 - 1;
  }
  function fbm(x, y, z, seed, octaves = 6, gain = 0.5) {
    let sum = 0,
      amp = 1,
      freq = 1,
      norm = 0;
    for (let i = 0; i < octaves; i++) {
      sum += amp * noise(x * freq, y * freq, z * freq, seed + i * 17);
      norm += amp;
      amp *= gain;
      freq *= 2.03;
    }
    return sum / norm;
  }
  function seeded(seed) {
    return () => {
      seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  // Crater field: bowl, raised rim and ejecta blanket. Radii follow N(>r) proportional to r^-2, as on real
  // cratered surfaces, between rMin and rMax (unit sphere). Craters are binned on a latitude-longitude grid.
  function craters(seed, count, rMax, rMin = 0.015) {
    const rng = seeded(seed),
      list = [];
    for (let i = 0; i < count; i++) {
      const z = rng() * 2 - 1,
        a = rng() * TAU,
        s = Math.sqrt(1 - z * z);
      const radius = Math.min(rMax, rMin / Math.sqrt(1 - rng() * 0.999));
      list.push({ c: [s * Math.cos(a), z, s * Math.sin(a)], radius, depth: 0.2 + rng() * 0.1 });
    }
    const rows = 32,
      cols = 64,
      grid = Array.from({ length: rows * cols }, () => []);
    for (const k of list) {
      const reach = k.radius * 2.4,
        lat = Math.asin(k.c[1]),
        lon = Math.atan2(k.c[2], k.c[0]);
      const r0 = Math.max(0, Math.floor(((lat - reach) / Math.PI + 0.5) * rows)),
        r1 = Math.min(rows - 1, Math.floor(((lat + reach) / Math.PI + 0.5) * rows));
      const span = Math.abs(lat) + reach > 1.45 ? Math.PI : reach / Math.max(0.05, Math.cos(Math.abs(lat) + reach));
      for (let r = r0; r <= r1; r++)
        for (
          let c = Math.floor(((lon - span) / TAU + 0.5) * cols);
          c <= Math.floor(((lon + span) / TAU + 0.5) * cols);
          c++
        )
          grid[r * cols + (((c % cols) + cols) % cols)].push(k);
    }
    for (const cell of grid) cell.sort((a, b) => b.radius - a.radius);
    return { grid, rows, cols, list };
  }
  function craterHeight(p, field) {
    const n = Math.hypot(p[0], p[1], p[2]),
      lat = Math.asin(p[1] / n),
      lon = Math.atan2(p[2], p[0]);
    const r = Math.min(field.rows - 1, Math.floor((lat / Math.PI + 0.5) * field.rows)),
      c = Math.min(field.cols - 1, Math.floor((lon / TAU + 0.5) * field.cols));
    let h = 0;
    for (const k of field.grid[r * field.cols + c]) {
      const d = Math.hypot(p[0] / n - k.c[0], p[1] / n - k.c[1], p[2] / n - k.c[2]) / k.radius;
      if (d > 2.4) continue;
      if (d < 1) h += k.radius * (k.depth * (d * d - 1) + 0.06 * d ** 6);
      else h += k.radius * 0.06 * Math.exp(-(((d - 1) * 4.2) ** 2)) + k.radius * 0.012 * Math.exp(-(d - 1) * 2.4);
    }
    return h;
  }
  // Irregular small body: an ellipsoid deformed by large-scale noise (and an optional second lobe), then
  // cratered and roughened. Returns positions, smooth normals and indices.
  function smallBody({
    seed = 7,
    level = 7,
    axes = [1.25, 0.86, 0.74],
    lobes = 0,
    craterCount = 2500,
    rough = 0.025,
    largest = 0.34,
  }) {
    const { positions, indices } = icosphere(level),
      list = craters(seed, craterCount, largest),
      n = positions.length / 3;
    for (let i = 0; i < n; i++) {
      const p = [positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]];
      let r =
        1 +
        0.15 * fbm(p[0] * 0.8, p[1] * 0.8, p[2] * 0.8, seed, 3, 0.5) +
        0.05 * fbm(p[0] * 2.4, p[1] * 2.4, p[2] * 2.4, seed + 7, 3, 0.5);
      if (lobes) {
        // Contact binary: two lobes joined by a neck along x.
        const side = Math.tanh(p[0] * 6);
        r *= 1 - 0.34 * Math.exp(-((p[0] / 0.24) ** 2)) * (1 - Math.abs(side) * 0.2);
        r *= 1 + 0.18 * (side > 0 ? 1 : -0.35) * Math.abs(p[0]);
      }
      r += craterHeight(p, list) + rough * fbm(p[0] * 9, p[1] * 9, p[2] * 9, seed + 101, 5, 0.52);
      positions[i * 3] = p[0] * r * axes[0];
      positions[i * 3 + 1] = p[1] * r * axes[1];
      positions[i * 3 + 2] = p[2] * r * axes[2];
    }
    return { positions, normals: normalsOf(positions, indices), indices };
  }
  // Area-weighted vertex normals.
  function normalsOf(positions, indices) {
    const normals = new Float32Array(positions.length);
    for (let i = 0; i < indices.length; i += 3) {
      const a = indices[i] * 3,
        b = indices[i + 1] * 3,
        c = indices[i + 2] * 3;
      const ux = positions[b] - positions[a],
        uy = positions[b + 1] - positions[a + 1],
        uz = positions[b + 2] - positions[a + 2];
      const vx = positions[c] - positions[a],
        vy = positions[c + 1] - positions[a + 1],
        vz = positions[c + 2] - positions[a + 2];
      const nx = uy * vz - uz * vy,
        ny = uz * vx - ux * vz,
        nz = ux * vy - uy * vx;
      for (const k of [a, b, c]) {
        normals[k] += nx;
        normals[k + 1] += ny;
        normals[k + 2] += nz;
      }
    }
    for (let i = 0; i < normals.length; i += 3) {
      const l = Math.hypot(normals[i], normals[i + 1], normals[i + 2]) || 1;
      normals[i] /= l;
      normals[i + 1] /= l;
      normals[i + 2] /= l;
    }
    return normals;
  }
  // Roche-lobe-filling donor: on each direction from the donor centre, the radius where the Roche potential
  // reaches its value at L1 (bisection). Positions in units of the separation, centred on the donor.
  function rocheDonor({ mu, potential, level = 7 }) {
    const { positions, indices } = icosphere(level),
      O = root.GeoObjects,
      x2 = 1 - mu,
      // Slightly inside the critical surface, so that the lobe closes just before L1.
      target = potential * 1.0004;
    const n = positions.length / 3;
    for (let i = 0; i < n; i++) {
      const d = [positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]],
        at = s => O.roche(mu, x2 + s * d[0], s * d[1], s * d[2]);
      // First exit from the lobe along the ray: beyond L1 the potential falls again into the other well.
      let lo = 0.02,
        hi = 0.03;
      while (hi < 1.2 && at(hi) < target) {
        lo = hi;
        hi += 0.01;
      }
      for (let k = 0; k < 50; k++) {
        const s = (lo + hi) / 2;
        if (at(s) < target) lo = s;
        else hi = s;
      }
      const s = (lo + hi) / 2;
      // Scene axes: the orbital pole (Roche z) is vertical, Roche y becomes -z.
      positions.set([s * d[0], s * d[2], -s * d[1]], i * 3);
    }
    return { positions, normals: normalsOf(positions, indices), indices };
  }
  root.GeoObjectGeometry = Object.freeze({
    trace,
    rayAngles,
    lensLevel,
    levelRadii,
    photonPaths,
    icosphere,
    noise,
    fbm,
    seeded,
    smallBody,
    normalsOf,
    rocheDonor,
  });
})(globalThis);
