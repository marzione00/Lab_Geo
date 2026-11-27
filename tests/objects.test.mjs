import test from 'node:test';
import assert from 'node:assert/strict';
import { load } from './source.mjs';
const scope = {};
load(scope, 'objects-model', 'objects-geometry', 'galaxy-model', 'core');
const O = scope.GeoObjects,
  G = scope.GeoObjectGeometry,
  M = scope.GeoGalaxyModel;
const close = (a, b, tol, label = '') => assert(Math.abs(a - b) <= tol, `${label} ${a} != ${b} (±${tol})`);

test('Catalogue: five objects with distinct routes and anchors away from the course systems', () => {
  assert.equal(O.objects.map(o => o.id).join(), 'buco-nero,pulsar,asteroidi,cometa,binaria');
  for (const o of O.objects) {
    assert(o.name && o.kind && o.symbol && /^#[0-9a-f]{6}$/.test(o.tone));
    assert(o.anchor.every(Number.isFinite));
    for (const p of Object.values(M.anchors)) assert(Math.hypot(...o.anchor.map((v, i) => v - p[i])) > 1.4, o.id);
    assert.equal(
      JSON.stringify(scope.GeoCore.parseRoute('#oggetto-' + o.id, [])),
      JSON.stringify({ type: 'object', object: o.id }),
    );
  }
  assert.equal(scope.GeoCore.parseRoute('#oggetto-quasar', []).type, 'notfound');
});

test('Black hole: horizon, photon sphere, ISCO and the Page-Thorne flux', () => {
  const m = O.blackHole();
  close(m.rg, (6.6743e-11 * 4.3e6 * 1.98847e30) / 299792458 ** 2, 1e-3 * m.rg, 'rg');
  close(m.schwarzschild / m.rg, 2, 1e-12);
  close(m.shadow / m.rg, 3 * Math.sqrt(3), 1e-12);
  close(m.efficiency, 1 - Math.sqrt(8 / 9), 1e-12);
  close(m.iscoPeriod, 2 * Math.PI * Math.sqrt((6 * m.rg) ** 3 / m.GM), 1e-9);
  // Closed form against direct quadrature of f(r) = -Omega' (E - Omega L)^-2 int (E - Omega L) L' dr.
  const E = r => (1 - 2 / r) / Math.sqrt(1 - 3 / r),
    L = r => Math.sqrt(r) / Math.sqrt(1 - 3 / r),
    W = r => r ** -1.5,
    d = (f, r) => (f(r + 1e-5) - f(r - 1e-5)) / 2e-5;
  for (const r of [7, 9.55, 15, 40]) {
    let integral = 0;
    const n = 20000;
    for (let i = 0; i < n; i++) {
      const x = 6 + ((r - 6) * (i + 0.5)) / n;
      integral += (E(x) - W(x) * L(x)) * d(L, x) * ((r - 6) / n);
    }
    const f = (-d(W, r) / (E(r) - W(r) * L(r)) ** 2) * integral,
      flux = f / (4 * Math.PI * r);
    close(O.diskFluxGeo(r), flux, 1e-4 * flux, 'flux r=' + r);
  }
  close(O.diskPeak.r, 9.55, 0.01, 'peak');
  assert.equal(O.diskFluxGeo(6), 0);
  // Newtonian limit far from the hole.
  close(O.diskFluxGeo(1e6) / ((3 / (8 * Math.PI)) * (1 - Math.sqrt(6e-6)) * 1e-18), 1, 0.01);
  // Static emitter: only the gravitational shift remains.
  close(O.diskRedshift(1e9, 0), 1, 1e-6);
  assert(O.diskRedshift(10, 3) > O.diskRedshift(10, 0) && O.diskRedshift(10, 0) > O.diskRedshift(10, -3));
  close(O.shadowAngle(1e8), (3 * Math.sqrt(3)) / 1e8, 1e-14);
});

test('Lensing tables: the tabulated ray reaches the emitter after the tabulated sweep', () => {
  const rc = 70,
    L = G.lensLevel(rc, { rays: 2048 }),
    nR = 256,
    nPsi = 1024,
    rMin = 3.05,
    rMax = 320,
    psiMax = 3 * Math.PI + 0.2;
  close(L.alphaC, Math.asin((3 * Math.sqrt(3) * Math.sqrt(1 - 2 / rc)) / rc), 1e-12);
  let checked = 0;
  for (const [r, psi] of [
    [8, 0.6],
    [12, 2.4],
    [20, Math.PI - 0.1],
    [20, Math.PI + 0.3],
    [30, 1.2],
    [10, 2 * Math.PI + 0.4],
    [150, 0.3],
  ]) {
    const k = Math.round((Math.log(r / rMin) / Math.log(rMax / rMin)) * (nR - 1)),
      rk = rMin * (rMax / rMin) ** (k / (nR - 1)),
      c = Math.round((psi / psiMax) * (nPsi - 1)),
      pc = (c / (nPsi - 1)) * psiMax,
      alpha = L.lens[k * nPsi + c] / rc;
    assert(alpha >= 0, 'covered ' + r + ' ' + psi);
    // The tabulated ray passes through the emitter: smallest distance between the path and the point.
    const target = [rk * Math.cos(pc), rk * Math.sin(pc)];
    let miss = Infinity;
    G.trace(
      rc,
      alpha,
      (p0, u0, p1, u1) => {
        // Distance from the target to the segment between two consecutive points of the path.
        const a = [Math.cos(p0) / u0, Math.sin(p0) / u0],
          b = [Math.cos(p1) / u1, Math.sin(p1) / u1],
          ab = [b[0] - a[0], b[1] - a[1]],
          t = Math.max(
            0,
            Math.min(1, ((target[0] - a[0]) * ab[0] + (target[1] - a[1]) * ab[1]) / (ab[0] ** 2 + ab[1] ** 2 || 1)),
          );
        miss = Math.min(miss, Math.hypot(a[0] + t * ab[0] - target[0], a[1] + t * ab[1] - target[1]));
      },
      psiMax + 1,
    );
    assert(miss < 0.003 * rk, `r=${rk.toFixed(2)} psi=${pc.toFixed(3)}: distance ${miss.toFixed(4)}`);
    checked++;
  }
  assert.equal(checked, 7);
  // Sky: rays leaving away from the hole are barely deflected; near the shadow the sweep grows without bound.
  close(L.sky[L.sky.length - 1], 0, 1e-6);
  assert(L.sky[1] > 2 * Math.PI && L.sky[1] > L.sky[200] && L.sky[200] > L.sky[1500]);
});

test('Pulsar: dipole field, characteristic age, spin-down power and light cylinder', () => {
  const p = O.pulsar();
  close(p.field, 3.2e19 * Math.sqrt(0.04 * 5e-13), 1);
  close(p.age / (365.25 * 86400), 1267.5, 1);
  close(p.spinDown, (4 * Math.PI ** 2 * 1e38 * 5e-13) / 0.04 ** 3, 1e20);
  close(p.lightCylinder / 1000, 1908.5, 0.5);
  close(p.polarCap, 12e3 * Math.sqrt(12e3 / p.lightCylinder), 1e-6);
  const chi = (50 * Math.PI) / 180;
  const onAxis = O.pulseProfile(chi, chi, 0.4),
    equator = O.pulseProfile(chi, Math.PI / 2, 0.4);
  close(Math.max(...onAxis), 1, 1e-9);
  assert.equal(onAxis.indexOf(Math.max(...onAxis)), 0);
  assert(Math.max(...equator) < 0.01, 'no pulse when the beams miss the line of sight');
});

test('Asteroid belt: resonances follow Kepler’s third law and empty the gaps', () => {
  const b = O.belt();
  for (const r of b.resonances) {
    close(r.a, 5.2 * (r.q / r.p) ** (2 / 3), 1e-12);
    close(r.period / b.giantPeriod, r.q / r.p, 1e-12);
  }
  const at = l => b.resonances.find(r => r.label === l).a;
  for (const l of ['3:1', '5:2', '2:1']) assert(O.beltDensity(at(l), b) < 0.12 * O.beltDensity(2.7, b), l);
  assert(O.beltDensity(at('3:2'), b) > 0.05);
});

test('Comet: Kepler equation, vis-viva and the time spent within 3 AU', () => {
  const c = O.comet();
  close(c.a, 20, 1e-12);
  close(c.period, 20 ** 1.5, 1e-9);
  for (const M of [1e-4, 0.01, 0.3, 1, 2.5, 3.1]) {
    const E = O.keplerE(M, 0.97);
    close(E - 0.97 * Math.sin(E), M, 1e-12);
  }
  for (const t of [-1, -0.2, 0, 0.05, 0.7]) {
    const s = O.cometState(c, t),
      v2 = s.vx * s.vx + s.vy * s.vy;
    close(v2, 4 * Math.PI ** 2 * (2 / s.r - 1 / c.a), 1e-6 * v2, 'vis-viva');
  }
  close(O.cometState(c, 0).r, 0.6, 1e-12);
  // The perihelion speed from vis-viva in km/s.
  close(c.perihelionSpeed / 1000, Math.sqrt((1.3271244e20 * 1.97) / (0.6 * 1.495978707e11)) / 1000, 1e-9);
  assert(c.activeYears > 0.9 && c.activeYears < 1.1);
});

test('Cataclysmic binary: Kepler separation, Roche lobes and eclipses', () => {
  const m = O.binary();
  close(m.a ** 3, (1.3271244e20 * 1.05 * 11520 ** 2) / (4 * Math.PI ** 2), 1e-9 * m.a ** 3);
  close(O.eggleton(1), 0.3789, 1e-4);
  close(O.lagrangeL1(0.5), 0, 1e-9);
  // The donor mesh is the critical equipotential: its volume-equivalent radius matches Eggleton within 1%.
  const d = G.rocheDonor({ mu: m.mu, potential: m.l1Potential, level: 5 }),
    p = d.positions,
    ix = d.indices;
  let V = 0;
  for (let i = 0; i < ix.length; i += 3) {
    const [a, b, c] = [ix[i] * 3, ix[i + 1] * 3, ix[i + 2] * 3];
    V +=
      (p[a] * (p[b + 1] * p[c + 2] - p[b + 2] * p[c + 1]) -
        p[a + 1] * (p[b] * p[c + 2] - p[b + 2] * p[c]) +
        p[a + 2] * (p[b] * p[c + 1] - p[b + 1] * p[c])) /
      6;
  }
  close(Math.cbrt((3 * V) / (4 * Math.PI)) / m.donorLobe, 1, 0.01);
  let tip = 0;
  for (let i = 0; i < p.length; i += 3) tip = Math.min(tip, p[i]);
  close(tip, m.l1 - 1, 0.02, 'tip at L1');
  const low = O.eclipseCurve(m, (60 * Math.PI) / 180),
    free = O.eclipseCurve(m, (60 * Math.PI) / 180, { occultation: false }),
    high = O.eclipseCurve(m, (85 * Math.PI) / 180);
  assert.equal(JSON.stringify(low), JSON.stringify(free), 'no eclipse at 60 degrees');
  assert(Math.min(...high) < 0.05 && high.indexOf(Math.min(...high)) === 0);
  // The hot spot sits on the rim of the disk and its hump peaks shortly before the eclipse (observed: 0.8-0.9).
  const spot = O.hotSpot(m),
    hump = high.indexOf(1) / high.length;
  close(Math.hypot(spot.position[0] + m.mu, spot.position[1]), m.diskRadius, 0.003);
  assert(hump > 0.8 && hump < 0.9, 'hump at phase ' + hump);
});

test('Black-body colours and dense meshes are deterministic', () => {
  const white = O.blackbody(6500),
    red = O.blackbody(3000),
    blue = O.blackbody(20000);
  assert(Math.min(...white) > 0.9);
  assert(red[2] / red[0] < white[2] / white[0] && white[2] / white[0] < blue[2] / blue[0]);
  const a = G.smallBody({ seed: 3, level: 4, craterCount: 200 }),
    b = G.smallBody({ seed: 3, level: 4, craterCount: 200 });
  assert.equal(a.positions.length / 3, 10 * 4 ** 4 + 2);
  assert.deepEqual([...a.positions], [...b.positions]);
  for (let i = 0; i < a.normals.length; i += 3)
    close(Math.hypot(a.normals[i], a.normals[i + 1], a.normals[i + 2]), 1, 1e-5);
  const paths = G.photonPaths({ count: 16, samples: 64 });
  assert.equal(paths.paths.length, 16 * 64 * 4);
});
