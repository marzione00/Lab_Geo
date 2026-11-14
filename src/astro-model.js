/* Synthetic systems: seeded educational models, never an observed catalogue. */
(function (root) {
  'use strict';
  const TAU = Math.PI * 2;
  const classes = [
    { type: 'F V', mass: 1.3, radius: 1.3, temperature: 6500, color: '#fff0d9' },
    { type: 'G V', mass: 1, radius: 1, temperature: 5772, color: '#ffe3ad' },
    { type: 'K V', mass: 0.75, radius: 0.72, temperature: 4700, color: '#ffc08a' },
    { type: 'M V', mass: 0.3, radius: 0.31, temperature: 3400, color: '#ff9a69' },
  ];
  const stellarText = {
    F: 'La temperatura della fotosfera supera quella solare. A parità di distanza, la maggiore luminosità produce un flusso incidente più intenso sui pianeti.',
    G: 'La classe G comprende il Sole. Nella sequenza principale, la fusione dell’idrogeno nel nucleo sostiene l’emissione di energia della stella.',
    K: 'Una stella di classe K è più fredda e meno luminosa del Sole. Per ricevere un flusso confrontabile con quello terrestre, un pianeta deve orbitare più vicino.',
    M: 'Le nane rosse hanno massa e luminosità ridotte. Le orbite irradiate quanto la Terra sono molto vicine alla stella; l’attività magnetica può influenzare le atmosfere planetarie.',
  };
  const names = [
    'Aster',
    'Elio',
    'Keplero',
    'Lyra',
    'Aurin',
    'Nereide',
    'Dione',
    'Cassini',
    'Ione',
    'Nivalis',
    'Cobalto',
    'Siro',
    'Aeria',
    'Chronos',
    'Pyra',
    'Lumen',
    'Talos',
  ];
  const subjects = [
    'Calcolo scientifico',
    'Dati e misura',
    'Programmare in R',
    'Visualizzazione',
    'Probabilità',
    'Stima e incertezza',
    'Test di ipotesi',
    'Regressione',
    'Analisi multivariata',
    'Serie temporali',
    'Previsione',
    'Statistica spaziale',
    'Raster e morfometria',
    'Archivi sedimentari',
    'Estremi e rischio',
    'Riproducibilità',
    'Classificazione',
  ];
  const lessons = {
    rock: {
      title: 'Superfici rocciose',
      text: 'Crateri e fratture conservano tracce della storia geologica. La loro distribuzione dipende dagli impatti e dai processi che rinnovano la superficie; la sola immagine non consente di ricavare età o composizione.',
      texture: 'T00',
      radius: 0.54,
      albedo: 0.16,
    },
    lava: {
      title: 'Vulcanismo e calore interno',
      text: 'Una superficie vulcanica richiede un apporto di energia. Calore residuo, decadimento radioattivo e dissipazione mareale possono contribuire; la temperatura di equilibrio radiativo non descrive queste sorgenti.',
      texture: 'M14',
      radius: 0.92,
      albedo: 0.13,
    },
    terrestrial: {
      title: 'Atmosfera e bilancio energetico',
      text: 'L’energia assorbita dipende dalla luminosità stellare, dalla distanza e dall’albedo. La temperatura superficiale richiede anche un modello dell’atmosfera e del trasporto del calore.',
      texture: 'M01',
      radius: 1,
      albedo: 0.3,
    },
    gas: {
      title: 'Un’atmosfera profonda',
      text: 'Le bande di un gigante gassoso rappresentano strutture atmosferiche, non una superficie solida. Rotazione e moti del fluido organizzano nubi e correnti; il colore da solo non identifica la composizione.',
      texture: 'M04',
      radius: 9.2,
      albedo: 0.4,
    },
    ice: {
      title: 'Ghiacci e radiazione',
      text: 'Un’albedo elevata riduce la frazione di energia assorbita. Ghiaccio e atmosfera interagiscono però con lo spettro della stella: il modello qui impiegato riassume tale dipendenza in un solo parametro.',
      texture: 'M09',
      radius: 1.52,
      albedo: 0.55,
    },
    desert: {
      title: 'Rilievi e trasporto',
      text: 'Bacini, rilievi e depositi suggeriscono processi geologici differenti. Per distinguere erosione, sedimentazione e tettonica occorrono misure; le superfici di questo atlante sono rappresentazioni sintetiche.',
      texture: 'M11',
      radius: 0.78,
      albedo: 0.25,
    },
  };
  function random(seed) {
    return () => {
      seed |= 0;
      seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const luminosity = (r, t) => r * r * (t / 5772) ** 4;
  const period = (a, m) => Math.sqrt((a * a * a) / m);
  const equilibrium = (l, a, albedo = 0.3) => 278.3 * ((l * (1 - albedo)) / (a * a)) ** 0.25;
  function category(p) {
    if ([4, 7, 10].includes(p.kind)) return 'gas';
    if (p.kind === 14) return 'lava';
    if (p.kind === 9) return 'ice';
    if ([0, 5, 6].includes(p.kind)) return 'terrestrial';
    if ([2, 11, 12, 13].includes(p.kind)) return 'desert';
    return 'rock';
  }
  function generate(id, variant = 0) {
    if (!/^(T00|M(?:0[1-9]|1[0-6]))$/.test(id)) return null;
    const index = id === 'T00' ? 0 : Number(id.slice(1));
    const target = root.GeoPlanets.byId[id];
    if (!target || index < 0 || index > 16 || !Number.isInteger(variant) || variant < 0 || variant > 9999) return null;
    const rng = random(20261113 + index * 7919 + variant * 104729),
      base = classes[Math.floor(rng() * classes.length)];
    const star = {
      ...base,
      luminosity: luminosity(base.radius, base.temperature),
      description: stellarText[base.type[0]],
    };
    const kind = category(target),
      targetIndex = kind === 'gas' ? 3 : kind === 'ice' ? 4 : kind === 'lava' ? 0 : 2;
    const kinds = ['rock', 'lava', 'terrestrial', 'gas', 'ice'];
    kinds[targetIndex] = kind;
    const planets = kinds.map((k, i) => {
      const isTarget = i === targetIndex,
        worldId = id + '-' + String.fromCharCode(98 + i),
        family = isTarget ? null : root.GeoFamilies?.forWorld(index, i, worldId);
      if (family) k = family.category;
      const lesson = lessons[k],
        appearance = isTarget ? target : root.GeoPlanets.byId[family?.template || lesson.texture];
      const a =
          (family ? family.axis * (1 + i * 0.015) : [0.24, 0.48, 1, 2.4, 5.5][i]) *
          Math.sqrt(star.luminosity) *
          (variant ? 0.96 + rng() * 0.08 : 1),
        albedo = family?.albedo ?? lesson.albedo;
      const radiusEarth = isTarget ? lesson.radius : (family?.radius ?? lesson.radius) * (0.9 + rng() * 0.2);
      return {
        ...appearance,
        familyId: family?.id || null,
        difficulty: family?.level || null,
        id: id + '-' + String.fromCharCode(98 + i),
        textureId: appearance.id,
        moduleId: isTarget ? id : null,
        name: isTarget ? target.name : names[index] + ' ' + String.fromCharCode(98 + i),
        label: String.fromCharCode(98 + i),
        isTarget,
        category: k,
        lesson,
        axisAU: a,
        periodYears: period(a, star.mass),
        temperature: equilibrium(star.luminosity, a, albedo),
        flux: star.luminosity / (a * a),
        albedo,
        radiusEarth,
        orbitRadius: [3.2, 5.5, 8, 10.7, 14][i],
        orbitPhase: [2.6, 0.65, 4.4, 1.5, 3.5][i] + index * 0.12,
        visualRadius: isTarget ? 0.9 : k === 'gas' ? 1.05 : k === 'ice' ? 0.7 : 0.55,
      };
    });
    planets.sort((a, b) => a.axisAU - b.axisAU);
    planets.forEach((p, i) => {
      if (i && p.axisAU < planets[i - 1].axisAU * 1.08) {
        p.axisAU = planets[i - 1].axisAU * 1.08;
        p.periodYears = period(p.axisAU, star.mass);
        p.temperature = equilibrium(star.luminosity, p.axisAU, p.albedo);
        p.flux = star.luminosity / (p.axisAU * p.axisAU);
      }
      p.orbitRadius = [3.2, 5.5, 8, 10.7, 14][i];
    });
    return {
      id,
      name: names[index],
      subject: subjects[index],
      variant,
      star,
      planets,
      target: planets.find(p => p.isTarget),
      yearsPerSecond: planets[0].periodYears / 55,
    };
  }
  const systems = root.GeoPlanets.planets.map(p => generate(p.id));
  function position(p, years) {
    const a = p.orbitPhase + (TAU * years) / p.periodYears;
    return [Math.cos(a) * p.orbitRadius, 0, Math.sin(a) * p.orbitRadius];
  }
  root.GeoAstro = Object.freeze({
    classes,
    systems,
    byId: Object.fromEntries(systems.map(s => [s.id, s])),
    generate,
    luminosity,
    period,
    equilibrium,
    position,
    lessons,
  });
})(globalThis);
