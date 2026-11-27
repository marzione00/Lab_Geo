/* Notable objects of the atlas: physical parameters, analytic relations and the catalogue read by the
   galaxy, the object pages, the scene worker and the tests. Every value shown on a page is computed here. */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2,
    SQRT3 = Math.sqrt(3);
  // CODATA 2018 and IAU 2015 nominal values (SI units).
  const SI = Object.freeze({
    G: 6.6743e-11,
    c: 299792458,
    GMsun: 1.3271244e20,
    Msun: 1.98847e30,
    Rsun: 6.957e8,
    AU: 1.495978707e11,
    sigma: 5.670374419e-8,
    year: 365.25 * 86400,
    eddington: 1.2572e31, // W per solar mass, electron scattering opacity of ionised hydrogen
  });

  // ------------------------------------------------------------------ Schwarzschild black hole
  // Relativistic thin-disk flux (Page & Thorne 1974) for a = 0 in units of Mdot c^6/(GM)^2, x = sqrt(r/M).
  function diskFluxGeo(r) {
    if (r <= 6) return 0;
    const y = Math.sqrt(r),
      y0 = Math.sqrt(6);
    const log = v => Math.log((v - SQRT3) / (v + SQRT3));
    const integral = y - y0 - (SQRT3 / 2) * (log(y) - log(y0));
    return ((3 / (8 * Math.PI)) * integral) / (y ** 5 * (y * y - 3));
  }
  // Peak of the flux profile, searched on a fine logarithmic grid between the ISCO and 200 M.
  function diskPeak() {
    let best = { r: 6, flux: 0 };
    for (let i = 0; i <= 20000; i++) {
      const r = 6 * Math.exp((i / 20000) * Math.log(200 / 6)),
        flux = diskFluxGeo(r);
      if (flux > best.flux) best = { r, flux };
    }
    return best;
  }
  const PEAK = diskPeak();
  function blackHole({ mass = 4.3e6, eddington = 0.1, display = 7500 } = {}) {
    const GM = SI.GMsun * mass,
      rg = GM / SI.c ** 2,
      efficiency = 1 - Math.sqrt(8 / 9),
      luminosity = eddington * SI.eddington * mass,
      mdot = luminosity / (efficiency * SI.c ** 2);
    const fluxScale = (mdot * SI.c ** 6) / GM ** 2,
      peakFlux = PEAK.flux * fluxScale,
      peakTemperature = (peakFlux / SI.sigma) ** 0.25;
    return {
      mass,
      GM,
      rg,
      schwarzschild: 2 * rg,
      photonSphere: 3 * rg,
      isco: 6 * rg,
      shadow: 3 * SQRT3 * rg,
      iscoPeriod: TAU * Math.sqrt((6 * rg) ** 3 / GM),
      efficiency,
      eddington,
      luminosity,
      mdot,
      mdotSolarPerYear: (mdot * SI.year) / SI.Msun,
      peakRadius: PEAK.r,
      peakFlux,
      peakTemperature,
      displayPeak: display,
      displayFactor: display / peakTemperature,
    };
  }
  // Circular-orbit redshift factor seen by a static observer at rc: g = sqrt(1-3/r) / (sqrt(1-2/rc)(1 - Omega lambda)).
  function diskRedshift(r, lambda, rc = Infinity) {
    const observer = Number.isFinite(rc) ? Math.sqrt(1 - 2 / rc) : 1;
    return Math.sqrt(1 - 3 / r) / (observer * (1 - lambda * r ** -1.5));
  }
  // Apparent radius of the shadow (critical impact parameter) seen from radius rc, in radians.
  const shadowAngle = rc => Math.asin(Math.min(1, (3 * SQRT3 * Math.sqrt(1 - 2 / rc)) / rc));

  // ------------------------------------------------------------------ pulsar
  function pulsar({ period = 0.04, pdot = 5e-13, mass = 1.4, radius = 12e3, inertia = 1e38, inclination = 50 } = {}) {
    const GM = SI.GMsun * mass,
      lightCylinder = (SI.c * period) / TAU;
    return {
      period,
      pdot,
      mass,
      radius,
      inertia,
      inclination,
      frequency: 1 / period,
      // Vacuum dipole estimate at the magnetic equator, B = 3.2e19 sqrt(P Pdot) gauss.
      field: 3.2e19 * Math.sqrt(period * pdot),
      age: period / (2 * pdot),
      spinDown: (4 * Math.PI ** 2 * inertia * pdot) / period ** 3,
      lightCylinder,
      polarCap: radius * Math.sqrt(radius / lightCylinder),
      gravity: GM / radius ** 2,
      escape: Math.sqrt((2 * GM) / radius),
      compactness: (2 * GM) / (radius * SI.c ** 2),
      density: (mass * SI.Msun) / ((4 / 3) * Math.PI * radius ** 3),
      equatorSpeed: (TAU * radius) / period,
    };
  }
  // Rotating-vector geometry: angle between the line of sight and each magnetic pole during a turn.
  // chi: magnetic inclination, zeta: angle between spin axis and line of sight, width: beam half-opening (radians).
  function pulseProfile(chi, zeta, width, samples = 360) {
    const out = [];
    for (let i = 0; i < samples; i++) {
      const phase = (i / samples) * TAU,
        c = Math.cos(chi) * Math.cos(zeta) + Math.sin(chi) * Math.sin(zeta) * Math.cos(phase);
      const a = Math.acos(Math.max(-1, Math.min(1, c))),
        b = Math.PI - a,
        s = width / 2;
      out.push(Math.exp((-a * a) / (2 * s * s)) + Math.exp((-b * b) / (2 * s * s)));
    }
    return out;
  }

  // ------------------------------------------------------------------ asteroid belt
  const resonances = [
    { p: 4, q: 1, label: '4:1' },
    { p: 3, q: 1, label: '3:1' },
    { p: 5, q: 2, label: '5:2' },
    { p: 7, q: 3, label: '7:3' },
    { p: 2, q: 1, label: '2:1' },
    { p: 3, q: 2, label: '3:2' },
    { p: 1, q: 1, label: '1:1' },
  ];
  function belt({ giant = 5.2, star = 1 } = {}) {
    const period = a => Math.sqrt(a ** 3 / star);
    return {
      giant,
      star,
      giantPeriod: period(giant),
      period,
      resonances: resonances.map(r => ({
        ...r,
        a: giant * (r.q / r.p) ** (2 / 3),
        period: period(giant) * (r.q / r.p),
      })),
    };
  }
  // Distribution of semimajor axes for the synthetic belt: a smooth main belt with Kirkwood gaps carved at the
  // 3:1, 5:2, 7:3 and 2:1 resonances, an inner edge near the 4:1 resonance, the Hilda group at 3:2 and the
  // Trojans at 1:1. Returned as a density on a grid; the scene samples it with the inverse CDF.
  function beltDensity(a, model = belt()) {
    const at = label => model.resonances.find(r => r.label === label).a;
    const edge = (x, x0, w) => 1 / (1 + Math.exp(-(x - x0) / w));
    let d = edge(a, at('4:1') + 0.04, 0.035) * (1 - edge(a, at('2:1') + 0.02, 0.03));
    d *= 0.55 + 0.45 * Math.exp(-(((a - 2.75) / 0.42) ** 2));
    const gap = (label, width, depth) => 1 - depth * Math.exp(-(((a - at(label)) / width) ** 2));
    d *= gap('3:1', 0.022, 0.97) * gap('5:2', 0.018, 0.93) * gap('7:3', 0.011, 0.8) * gap('2:1', 0.025, 0.95);
    d += 0.11 * Math.exp(-(((a - at('3:2')) / 0.05) ** 2));
    return d;
  }

  // ------------------------------------------------------------------ comet
  function keplerE(M, e) {
    let E = e < 0.8 ? M : Math.PI;
    for (let i = 0; i < 40; i++) {
      const f = E - e * Math.sin(E) - M,
        step = f / (1 - e * Math.cos(E));
      E -= step;
      if (Math.abs(step) < 1e-14) break;
    }
    return E;
  }
  function comet({ perihelion = 0.6, eccentricity = 0.97, star = 1, active = 3 } = {}) {
    const a = perihelion / (1 - eccentricity),
      GM = SI.GMsun * star,
      period = Math.sqrt(a ** 3 / star);
    // Time spent within the activity distance: r = a(1 - e cos E) = active.
    const cosE = (1 - active / a) / eccentricity,
      E = Math.acos(Math.max(-1, Math.min(1, cosE))),
      M = E - eccentricity * Math.sin(E);
    return {
      perihelion,
      eccentricity,
      star,
      a,
      aphelion: a * (1 + eccentricity),
      period,
      perihelionSpeed: Math.sqrt((GM * (1 + eccentricity)) / (perihelion * SI.AU)),
      aphelionSpeed: Math.sqrt((GM * (1 - eccentricity)) / (a * (1 + eccentricity) * SI.AU)),
      active,
      activeYears: (2 * M * period) / TAU,
    };
  }
  // Position on the orbit (AU, orbital plane) after t years from perihelion.
  function cometState(model, years) {
    const n = TAU / model.period,
      M = ((((n * years) % TAU) + TAU + Math.PI) % TAU) - Math.PI,
      E = keplerE(M, model.eccentricity),
      e = model.eccentricity,
      a = model.a;
    const x = a * (Math.cos(E) - e),
      y = a * Math.sqrt(1 - e * e) * Math.sin(E),
      r = a * (1 - e * Math.cos(E));
    // Speed in AU per year: sqrt(GM / a) / (1 - e cos E), with GM = 4 pi^2 AU^3 yr^-2 per solar mass.
    const vScale = Math.sqrt((model.star ?? 1) / a) / (1 - e * Math.cos(E));
    return { x, y, r, E, M, vx: -vScale * Math.sin(E) * TAU, vy: vScale * Math.sqrt(1 - e * e) * Math.cos(E) * TAU };
  }

  // ------------------------------------------------------------------ cataclysmic binary
  // Eggleton (1983): Roche-lobe radius over separation for mass ratio q = M_lobe / M_other.
  const eggleton = q => (0.49 * q ** (2 / 3)) / (0.6 * q ** (2 / 3) + Math.log(1 + q ** (1 / 3)));
  // Roche potential in the corotating frame, separation 1, total mass 1, origin at the centre of mass.
  function roche(mu, x, y, z) {
    const x1 = -mu,
      x2 = 1 - mu;
    const r1 = Math.hypot(x - x1, y, z),
      r2 = Math.hypot(x - x2, y, z);
    return -(1 - mu) / r1 - mu / r2 - 0.5 * (x * x + y * y);
  }
  // Inner Lagrange point on the axis between the two stars (bisection on dPhi/dx).
  function lagrangeL1(mu) {
    const d = x => {
      const h = 1e-7;
      return (roche(mu, x + h, 0, 0) - roche(mu, x - h, 0, 0)) / (2 * h);
    };
    let lo = -mu + 1e-4,
      hi = 1 - mu - 1e-4;
    for (let i = 0; i < 200; i++) {
      const mid = (lo + hi) / 2;
      if (d(lo) * d(mid) <= 0) hi = mid;
      else lo = mid;
    }
    return (lo + hi) / 2;
  }
  function binary({ primary = 0.8, donor = 0.25, hours = 3.2, inclination = 78 } = {}) {
    const total = primary + donor,
      period = hours * 3600,
      a = Math.cbrt((SI.GMsun * total * period ** 2) / (4 * Math.PI ** 2)),
      q = donor / primary,
      mu = donor / total,
      l1 = lagrangeL1(mu);
    const sinI = Math.sin((inclination * Math.PI) / 180);
    return {
      primary,
      donor,
      hours,
      period,
      inclination,
      a,
      q,
      mu,
      donorLobe: eggleton(q),
      primaryLobe: eggleton(1 / q),
      // Distance of L1 from the white dwarf, in units of the separation.
      l1: l1 + mu,
      l1Potential: roche(mu, l1, 0, 0),
      // Circularisation radius of the stream (Warner 1995, eq. 2.19), q = M_donor / M_primary.
      circularisation: (1 + q) * (0.5 - 0.227 * Math.log10(q)) ** 4,
      // Outer radius of the disk drawn in the scene: 0.765 of the Roche lobe of the white dwarf.
      diskRadius: 0.765 * eggleton(1 / q),
      // Mean density of a lobe-filling donor, fixed by the period: rho = 3 pi mu / (G P^2 f^3), f = R_L / a.
      donorDensity: (3 * Math.PI * mu) / (SI.G * period ** 2 * eggleton(q) ** 3),
      K1: ((TAU * a) / period) * (donor / total) * sinI,
      K2: ((TAU * a) / period) * (primary / total) * sinI,
    };
  }

  // Ballistic stream from L1 in the corotating frame (separation 1, G(M1+M2) = 1, angular velocity 1 along +z,
  // origin at the centre of mass), integrated with RK4 until it reaches the given distance from the accretor.
  // Returns the path and the final state.
  function rocheStream(mu, l1, radius) {
    const x1 = -mu,
      h = 0.0004,
      acc = (x, y, vx, vy) => {
        const r1 = Math.hypot(x - x1, y) ** 3,
          r2 = Math.hypot(x - (1 - mu), y) ** 3;
        return [
          2 * vy + x - ((1 - mu) * (x - x1)) / r1 - (mu * (x - (1 - mu))) / r2,
          -2 * vx + y - ((1 - mu) * y) / r1 - (mu * y) / r2,
        ];
      };
    const f = q => [q[2], q[3], ...acc(q[0], q[1], q[2], q[3])],
      add = (a, b, k) => a.map((v, j) => v + b[j] * k);
    let s = [l1 - 0.002, 0, -0.01, -0.005];
    const path = [[s[0], s[1]]];
    for (let i = 0; i < 40000; i++) {
      const k1 = f(s),
        k2 = f(add(s, k1, h / 2)),
        k3 = f(add(s, k2, h / 2)),
        k4 = f(add(s, k3, h));
      s = s.map((v, j) => v + (h / 6) * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]));
      if (i % 20 === 0) path.push([s[0], s[1]]);
      if (Math.hypot(s[0] - x1, s[1]) < radius) break;
    }
    path.push([s[0], s[1]]);
    return { path, position: [s[0], s[1]], velocity: [s[2], s[3]] };
  }
  // Hot spot where the stream reaches the rim of the disk. The shocked gas faces the flow that hits it: the
  // normal is opposite to the velocity of the stream relative to the Keplerian gas of the rim. Both velocities are
  // in the corotating frame, where the rim gas moves with angular velocity Omega_K - 1 around the white dwarf.
  const spots = new WeakMap();
  function hotSpot(model) {
    if (spots.has(model)) return spots.get(model);
    const mu = model.mu,
      { position, velocity } = rocheStream(mu, model.l1 - mu, model.diskRadius),
      rx = position[0] + mu,
      ry = position[1],
      spin = Math.sqrt((1 - mu) / Math.hypot(rx, ry) ** 3) - 1,
      rel = [velocity[0] + spin * ry, velocity[1] - spin * rx],
      norm = Math.hypot(rel[0], rel[1]);
    const spot = { position, normal: [-rel[0] / norm, -rel[1] / norm] };
    spots.set(model, spot);
    return spot;
  }

  // Light curve of a cataclysmic binary at inclination i (radians): disk, hot spot and white dwarf, eclipsed by the
  // donor, approximated by the sphere of its Roche-lobe radius. Roche coordinates (separation 1, centre of mass at
  // the origin, orbital plane xy); phase 0 puts the donor between the white dwarf and the observer. The hot spot
  // radiates mostly along its normal and produces the orbital hump. Values are normalised to the maximum.
  function eclipseCurve(model, inclination, { samples = 200, occultation = true } = {}) {
    const mu = model.mu,
      xw = -mu,
      xd = 1 - mu,
      rL = model.donorLobe,
      rOut = model.diskRadius,
      rIn = 0.012,
      spot = hotSpot(model);
    const points = [];
    for (let i = 0; i < 1500; i++) {
      const r = rIn * (rOut / rIn) ** ((i + 0.5) / 1500),
        a = i * 2.399963;
      // Emission of a ring of the disk, proportional to r^-3 times its area 2 pi r dr (dr proportional to r).
      points.push([xw + r * Math.cos(a), r * Math.sin(a), 0, (rIn / r) ** 1]);
    }
    const disc = points.reduce((s, p) => s + p[3], 0);
    points.push([xw, 0, 0, disc * 0.25]);
    // Hot spot: an isotropic part and a beamed part proportional to the projection of its normal on the line of sight.
    points.push([...spot.position, 0, disc * 0.35]);
    const si = Math.sin(inclination),
      ci = Math.cos(inclination),
      raw = [];
    for (let k = 0; k < samples; k++) {
      const phase = (k / samples) * TAU,
        los = [si * Math.cos(phase), -si * Math.sin(phase), ci],
        beam = 0.3 + 1.4 * Math.max(0, spot.normal[0] * los[0] + spot.normal[1] * los[1]);
      let seen = 0;
      points.forEach((p, j) => {
        const d = [xd - p[0], -p[1], -p[2]],
          t = d[0] * los[0] + d[1] * los[1] + d[2] * los[2],
          hidden = occultation && t > 0 && d[0] * d[0] + d[1] * d[1] + d[2] * d[2] - t * t <= rL * rL;
        if (!hidden) seen += p[3] * (j === points.length - 1 ? beam : 1);
      });
      raw.push(seen);
    }
    const top = Math.max(...raw);
    return raw.map(v => v / top);
  }

  // ------------------------------------------------------------------ colour of a black body
  // CIE 1931 2-degree colour-matching functions, multi-lobe fit of Wyman, Sloan and Shirley (2013).
  const lobe = (x, mu, s1, s2) => Math.exp(-0.5 * ((x - mu) / (x < mu ? s1 : s2)) ** 2);
  function cie(lambda) {
    return [
      1.056 * lobe(lambda, 599.8, 37.9, 31) +
        0.362 * lobe(lambda, 442, 16, 26.7) -
        0.065 * lobe(lambda, 501.1, 20.4, 26.2),
      0.821 * lobe(lambda, 568.8, 46.9, 40.5) + 0.286 * lobe(lambda, 530.9, 16.3, 31.1),
      1.217 * lobe(lambda, 437, 11.8, 36) + 0.681 * lobe(lambda, 459, 26, 13.8),
    ];
  }
  // Linear sRGB chromaticity of a black body at temperature T (K), scaled so that the largest channel is 1.
  function blackbody(T) {
    const h = 6.62607015e-34,
      k = 1.380649e-23;
    const xyz = [0, 0, 0];
    for (let l = 380; l <= 780; l += 2) {
      const m = l * 1e-9,
        radiance = 1 / (m ** 5 * (Math.exp((h * SI.c) / (m * k * T)) - 1)),
        cmf = cie(l);
      for (let i = 0; i < 3; i++) xyz[i] += radiance * cmf[i];
    }
    const [X, Y, Z] = xyz;
    const rgb = [
      3.2406 * X - 1.5372 * Y - 0.4986 * Z,
      -0.9689 * X + 1.8758 * Y + 0.0415 * Z,
      0.0557 * X - 0.204 * Y + 1.057 * Z,
    ].map(v => Math.max(0, v));
    const top = Math.max(...rgb);
    return rgb.map(v => v / top);
  }
  // Table of colours from 1000 K to 40000 K on a logarithmic scale, used by the shaders.
  function blackbodyTable(n = 256, low = 1000, high = 40000) {
    const out = new Float32Array(n * 4);
    for (let i = 0; i < n; i++) {
      const T = low * (high / low) ** (i / (n - 1));
      out.set([...blackbody(T), T], i * 4);
    }
    return out;
  }

  // ------------------------------------------------------------------ catalogue
  const BH = blackHole(),
    PSR = pulsar(),
    BELT = belt(),
    COMET = comet(),
    CV = binary();
  const objects = [
    {
      id: 'buco-nero',
      name: 'Erebo',
      kind: 'Buco nero supermassiccio',
      short: 'Buco nero',
      symbol: '●',
      tone: '#ffb15c',
      anchor: [0, 0.32, 0],
      model: BH,
    },
    {
      id: 'pulsar',
      name: 'Faro',
      kind: 'Pulsar giovane',
      short: 'Pulsar',
      symbol: '✳',
      tone: '#8fd0ff',
      anchor: [7.3, 0.9, -2.6],
      model: PSR,
    },
    {
      id: 'asteroidi',
      name: 'Lapis',
      kind: 'Sistema con fascia di asteroidi',
      short: 'Fascia di asteroidi',
      symbol: '⁘',
      tone: '#d9c29a',
      anchor: [-7.6, 0.7, -2.4],
      model: BELT,
    },
    {
      id: 'cometa',
      name: 'Clio',
      kind: 'Cometa periodica',
      short: 'Cometa',
      symbol: '☄',
      tone: '#9fe6ff',
      anchor: [1.4, 0.8, -7.6],
      model: COMET,
    },
    {
      id: 'binaria',
      name: 'Diade',
      kind: 'Binaria cataclismica',
      short: 'Nana bianca in binaria',
      symbol: '◐',
      tone: '#c6b5ff',
      anchor: [-4.4, 0.6, 7.1],
      model: CV,
    },
  ];
  root.GeoObjects = Object.freeze({
    SI,
    objects,
    byId: Object.fromEntries(objects.map(o => [o.id, o])),
    blackHole,
    diskFluxGeo,
    diskPeak: PEAK,
    diskRedshift,
    shadowAngle,
    pulsar,
    pulseProfile,
    belt,
    beltDensity,
    comet,
    cometState,
    keplerE,
    binary,
    eggleton,
    roche,
    lagrangeL1,
    rocheStream,
    hotSpot,
    eclipseCurve,
    blackbody,
    blackbodyTable,
  });
})(globalThis);
